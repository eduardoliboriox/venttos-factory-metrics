from flask import Flask

from app.config import Config
from app.extensions import login_manager

from app.routes.pages import bp as pages_bp
from app.routes.api import bp as api_bp
from app.auth.routes import bp as auth_bp
from app.auth.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🔐 Flask-Login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # 📌 Blueprints
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
