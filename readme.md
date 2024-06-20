
# Destiny Clan Tracker

## Project Overview
The Destiny Clan Tracker is a Flask-based web application that allows Destiny 2 clan leaders to track weekly clears of dungeons and raids by clan members. The application authenticates users via Bungie's OAuth service and utilizes the Bungie API to fetch relevant clan data.

## Features
- User authentication with Bungie.net accounts.
- Display of authenticated user's clan information.
- Tracking of weekly clears for raids and dungeons.

## Technology Stack
- **Flask**: Python web framework used for server-side logic.
- **Requests**: Library used to handle HTTP requests to the Bungie API.
- **Jinja**: Templating engine for rendering the frontend.

## Getting Started

### Prerequisites
- Python 3.6+
- Flask
- Requests

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/destiny-clan-tracker.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

### Configuration
- Ensure you have the `client_id`, `client_secret`, and `api_key` set in your environment variables or directly in the application.

## Contributing
Contributions are welcome! Please read the contributing guidelines and code of conduct before making pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
