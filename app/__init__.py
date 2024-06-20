from flask import Flask
from flask_talisman import Talisman
from app.routes import main as main_blueprint

app = Flask(__name__)

# Configure Content Security Policy
csp = {
    'default-src': [
        "'self'",
        'https://www.d2clantracker.com'
    ],
    'style-src': [
        "'self'",
        "'unsafe-inline'",
        'https://maxcdn.bootstrapcdn.com',
        'https://cdnjs.cloudflare.com'
    ],
    'script-src': [
        "'self'",
        "'unsafe-inline'",
        'https://ajax.googleapis.com',
        'https://cdnjs.cloudflare.com',
        'https://maxcdn.bootstrapcdn.com'
    ],
    'font-src': [
        "'self'",
        'https://cdnjs.cloudflare.com'
    ],
    'img-src': [
        "'self'",
        'data:',
        'blob:',
        'https://www.d2clantracker.com'
    ]
}

Talisman(app, content_security_policy=csp)

app.config.from_object('app.config')
app.register_blueprint(main_blueprint)

@app.template_filter('capitalize_properly')
def capitalize_properly(value):
    return ' '.join(word.capitalize() if word.lower() != "of" else word.lower() for word in value.split())

from app import routes
