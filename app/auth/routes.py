from flask import Blueprint, redirect, url_for
from flask_login import login_user, logout_user
from authlib.integrations.flask_client import OAuth
from app.auth.service import get_or_create_user
from app.auth.models import User

bp = Blueprint("auth", __name__)
oauth = OAuth()

@bp.route("/login")
def login():
    return render_template("auth/login.html")

@bp.route("/login/google")
def login_google():
    return oauth.google.authorize_redirect(
        url_for("auth.google_callback", _external=True)
    )

@bp.route("/auth/google")
def google_callback():
    token = oauth.google.authorize_access_token()
    profile = oauth.google.parse_id_token(token)

    user_data = get_or_create_user(profile, "google")
    login_user(User(user_data))
    return redirect("/dashboard")

@bp.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
