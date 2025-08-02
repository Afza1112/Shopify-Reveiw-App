from flask import Flask
from config import Config
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprints(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
