from flask import Flask
from config import Config
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    return app

app = create_app()  # <-- This line is crucial for Gunicorn/production

if __name__ == '__main__':
    app.run(debug=True)
