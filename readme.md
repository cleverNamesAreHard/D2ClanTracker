# Destiny Clan Tracker

## Project Overview
The [Destiny 2 Clan Tracker](https://www.d2clantracker.com/) is a Flask-based web application designed for Destiny 2 memers to monitor weekly activity completions by clan members. The app authenticates users via Bungie's OAuth service and retrieves clan data using the Bungie API.

## Features
- User authentication with Bungie.net accounts.
- Display of authenticated user's clan information.
- Tracking of weekly clears for raids and dungeons.

## Technology Stack
- **Flask**: Python web framework for server-side logic.
- **Flask-Talisman**: Security extension for setting HTTP headers.
- **Gunicorn**: WSGI HTTP Server for UNIX.
- **Jinja**: Templating engine for rendering the frontend.
- **asyncio**: Asynchronous I/O for handling Bungie API requests.
- **[aiobungie](https://github.com/nxtlo/aiobungie)**: Asynchronous Bungie API wrapper. 

## Shout-Out
I just wanted to give the folks over at `aiobungie` (see [here](https://github.com/nxtlo/aiobungie)) a **MASSIVE** shout-out.  I'm not affiliated, but when fighting with the Bungie API failed, their project saved me.  Their stuff is incredibly well-documented, and designed to make it easy for folks to roll out new software based off the Bungie API.  Amazing, amazing job, team!  Thank you for all your hard work on this!  I'll work to ensure there's a footer on my page pointing to y'all as well.