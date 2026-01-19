from flask import Blueprint, jsonify, request
from app.services.pcp_service import criar_planejamento

bp = Blueprint("api", __name__)

@bp.post("/planejamento")
def criar():
    data = request.json
    resultado = criar_planejamento(data)
    return jsonify(resultado), 201
