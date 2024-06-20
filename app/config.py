import os

SECRET_KEY = os.getenv('SECRET_KEY')  # Use fixed secret key in production
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
API_KEY = os.getenv('API_KEY')
REDIRECT_URI = os.getenv('REDIRECT_URI')
