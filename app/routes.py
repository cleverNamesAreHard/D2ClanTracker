import asyncio
import datetime
import logging
import aiobungie
from flask import Blueprint, request, redirect, session, render_template, url_for, current_app
from functools import wraps

main = Blueprint('main', __name__)
logging.basicConfig(level=logging.INFO)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

# Hardcoded raid hashes
RAID_HASHES = {
    'Last Wish': [2122313384],
    'Garden of Salvation': [1042180643],
    'Deep Stone Crypt': [910380154],
    'Vault of Glass': [1681562271, 3711931140, 3881495763, 1485585878],
    'Vow of the Disciple': [2906950631, 4217492330, 4156879541, 1441982566],
    'King\'s Fall': [2897223272, 3257594522, 1063970578, 1374392663],
    'Root of Nightmares': [2381413764, 2918919505],
    'Crota\'s End': [4179289725, 107319834, 156253568, 1507509200],
    'Salvation\'s Edge': [1541433876, 4129614942]
}

@main.route('/')
def home():
    logging.info('Rendering home page')
    return render_template('home.html')

@main.route('/login')
def login():
    login_url = f"https://www.bungie.net/en/OAuth/Authorize?client_id={current_app.config['CLIENT_ID']}&response_type=code&redirect_uri={url_for('main.oauth_callback', _external=True)}"
    logging.info(f'Redirecting to login URL: {login_url}')
    return redirect(login_url)

@main.route('/oauth_callback')
def oauth_callback():
    code = request.args.get('code')
    logging.info(f'Received code: {code}')
    if code:
        try:
            async def handle_callback():
                client = aiobungie.RESTPool(
                    current_app.config['API_KEY'],
                    client_secret=current_app.config['CLIENT_SECRET'],
                    client_id=current_app.config['CLIENT_ID']
                )

                async with client.acquire() as rest:
                    tokens = await rest.fetch_oauth2_tokens(code)
                    access_token = tokens.access_token
                    session['access_token'] = access_token

                    profile_response = await rest.fetch_current_user_memberships(access_token)
                    logging.info(f'Profile response: {profile_response}')

                    destiny_memberships = profile_response['destinyMemberships']
                    if not destiny_memberships:
                        logging.error("Error: No destiny memberships found in the response.")
                        return 'Failed to obtain destiny memberships', 500

                    destiny_membership_id = destiny_memberships[0]['membershipId']
                    membership_type = destiny_memberships[0]['membershipType']

                    clans_response = await rest.fetch_groups_for_member(destiny_membership_id, membership_type)
                    logging.info(f'Clans response: {clans_response}')
                    clans = clans_response['results']
                    if not clans:
                        logging.error("Error: No clans found in the response.")
                        return 'Failed to obtain clan ID', 500

                    clan_id = clans[0]['group']['groupId']
                    return redirect(url_for('main.clan_page', clan_id=clan_id))

            return asyncio.run(handle_callback())
        except aiobungie.HTTPError as e:
            logging.error(f'HTTP error occurred: {e}')
            return 'Authorization failed', 400

    return 'Authorization failed', 400

@main.route('/clan/<clan_id>')
@login_required
def clan_page(clan_id):
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('main.login'))

    async def fetch_clan_data():
        client = aiobungie.RESTPool(
            current_app.config['API_KEY'],
            client_secret=current_app.config['CLIENT_SECRET'],
            client_id=current_app.config['CLIENT_ID']
        )

        async with client.acquire() as rest:
            clan_response = await rest.fetch_clan_from_id(clan_id)
            logging.info(f'Clan response: {clan_response}')
            members_response = await rest.fetch_clan_members(clan_id)
            logging.info(f'Members response: {members_response}')

            clan_data = clan_response['detail']
            members_data = members_response['results']

            members_list = [
                {
                    'membershipId': member['destinyUserInfo']['membershipId'],
                    'displayName': member['destinyUserInfo']['bungieGlobalDisplayName'],
                    'memberType': member['memberType']
                }
                for member in members_data
            ]

            return render_template('clan.html', clan_data=clan_data, members=members_list)

    return asyncio.run(fetch_clan_data())

@main.route('/reports/<report_name>', methods=['GET'])
@login_required
def reports(report_name):
    clan_id = request.args.get('clan_id')
    if not clan_id:
        return redirect(url_for('main.home'))

    async def fetch_report_data():
        client = aiobungie.RESTPool(
            current_app.config['API_KEY'],
            client_secret=current_app.config['CLIENT_SECRET'],
            client_id=current_app.config['CLIENT_ID']
        )

        async with client.acquire() as rest:
            members_response = await rest.fetch_clan_members(clan_id)
            members_data = members_response['results']

            reset_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=datetime.datetime.now(datetime.timezone.utc).weekday() + 6) + datetime.timedelta(hours=12, minutes=30)

            raid_completions = {}
            for member in members_data:
                membership_id = member['destinyUserInfo']['membershipId']
                member_type = member['memberType']

                # Initialize raid completions for this member
                raid_completions[membership_id] = {}
                for raid in RAID_HASHES.keys():
                    raid_completions[membership_id][raid] = None

                try:
                    characters_response = await rest.fetch_profile(membership_id, member_type, [aiobungie.ComponentType.CHARACTERS])
                    characters = characters_response['characters']['data'].values()

                    for character in characters:
                        character_id = character['characterId']
                        activities_response = await rest.fetch_activities(membership_id, character_id, aiobungie.GameMode.RAID, membership_type=member_type, page=0, limit=10)
                        activities = activities_response.get('activities', [])

                        for activity in activities:
                            period = datetime.datetime.fromisoformat(activity['period'].replace('Z', '+00:00'))
                            if period > reset_time:
                                reference_id = activity['activityDetails']['referenceId']
                                for raid, hashes in RAID_HASHES.items():
                                    if reference_id in hashes:
                                        if reference_id in [1681562271, 4217492330, 3257594522, 2918919505, 1507509200, 4129614942]:
                                            raid_completions[membership_id][raid] = 'master'
                                        elif reference_id in [1485585878, 4156879541, 1063970578, 2381413764, 107319834, 1541433876]:
                                            raid_completions[membership_id][raid] = 'contest'
                                        else:
                                            raid_completions[membership_id][raid] = 'standard'

                except aiobungie.error.MembershipTypeError as e:
                    logging.error(f'Membership type error for user {membership_id}: {e}')
                except aiobungie.error.InternalServerError as e:
                    logging.error(f'Internal server error for user {membership_id}: {e}')

            members_data = [
                {
                    'displayName': member['destinyUserInfo']['bungieGlobalDisplayName'],
                    'raids': raid_completions[member['destinyUserInfo']['membershipId']]
                }
                for member in members_data
            ]

            return render_template('reports.html', report_name=report_name, members=members_data, raid_names=list(RAID_HASHES.keys()))

    return asyncio.run(fetch_report_data())

@main.route('/error')
def error_page():
    error_message = request.args.get('error_message', 'An error occurred')
    return render_template('error.html', error_message=error_message)
