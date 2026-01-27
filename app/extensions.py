import psycopg
from psycopg.rows import dict_row
from flask import current_app
from flask_login import LoginManager

# 🔐 Flask-Login (instanciado UMA vez)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def get_db():
    return psycopg.connect(
        current_app.config["DATABASE_URL"],
        row_factory=dict_row,
        sslmode="require"
    )
