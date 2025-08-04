from flask import Flask
from config import Config
from routes import register_blueprints
from datetime import datetime
from routes.auth import auth_bp


def datetimeformat(value):
    """Convert UNIX timestamp (int/str) to readable date string."""
    try:
        dt = datetime.fromtimestamp(int(value))
        return dt.strftime('%b %d, %Y %I:%M%p')
    except Exception:
        return str(value)  # fallback

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    # Register the filter AFTER app is created
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.register_blueprint(auth_bp)
    return app

app = create_app()  # This line is crucial for Gunicorn/production

if __name__ == '__main__':
    app.run(debug=True)
