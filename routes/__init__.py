from .main import main_bp
from .review import review_bp
from .admin import admin_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)
