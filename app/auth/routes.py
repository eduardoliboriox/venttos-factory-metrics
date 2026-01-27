from flask import Blueprint, redirect, url_for, render_template, current_app
from flask_login import login_user, logout_user
from authlib.integrations.flask_client import OAuth
from app.auth.service import get_or_create_user
from app.auth.models import User

bp = Blueprint("auth", __name__)
oauth = OAuth()

@bp.record_once
def setup_oauth(state):
    app = state.app
    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    oauth.register(
        name="github",
        client_id=app.config["GITHUB_CLIENT_ID"],
        client_secret=app.config["GITHUB_CLIENT_SECRET"],
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "user:email"},
    )

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
    userinfo = oauth.google.parse_id_token(token)

    user_data = get_or_create_user(userinfo, "google")
    login_user(User(user_data))

    return redirect(url_for("pages.dashboard"))

@bp.route("/login/github")
def login_github():
    return oauth.github.authorize_redirect(
        url_for("auth.github_callback", _external=True)
    )

@bp.route("/auth/github")
def github_callback():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get("user")
    profile = resp.json()

    # email no GitHub pode vir separado
    if not profile.get("email"):
        emails = oauth.github.get("user/emails").json()
        primary = next(e for e in emails if e["primary"])
        profile["email"] = primary["email"]

    user_data = get_or_create_user(profile, "github")
    login_user(User(user_data))

    return redirect(url_for("pages.dashboard"))

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
