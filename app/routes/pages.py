from flask import Blueprint, render_template
from app.services.pcp_service import listar_dashboard

bp = Blueprint("pages", __name__)

@bp.route("/")
def dashboard():
    dados = listar_dashboard()
    return render_template("dashboard.html", dados=dados)
