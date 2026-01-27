from flask import Flask
from flask_login import LoginManager
from .routes import pages, api
from app.auth.models import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(pages.bp)
    app.register_blueprint(api.bp, url_prefix="/api")

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app
