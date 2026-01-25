from flask import Blueprint, request, jsonify

from app.services import modelos_service, cargos_service
from app.services.lancamentos_service import (
    criar_lancamento,
    faltas_por_linha,
    ferias_por_linha_cargos
)
from app.services.pcp_service import ranking_linhas_ferias
from app.services.atestados_service import registrar_atestado
from app.services.relatorios_service import gerar_relatorio


bp = Blueprint("api", __name__)

# =========================
# MODELOS
# =========================
@bp.route("/modelos", methods=["GET"])
def listar():
    return jsonify(modelos_service.listar_modelos())


@bp.route("/modelos", methods=["POST"])
def cadastrar():
    return jsonify(modelos_service.cadastrar_modelo(request.form))


@bp.route("/modelos", methods=["DELETE"])
def excluir():
    return jsonify(modelos_service.excluir_modelo(request.form))


# =========================
# CARGOS
# =========================
@bp.route("/cargos", methods=["GET"])
def listar_cargos():
    return jsonify(cargos_service.listar())


@bp.route("/cargos", methods=["POST"])
def cadastrar_cargo():
    return jsonify(cargos_service.cadastrar(request.form))


@bp.route("/cargos", methods=["PUT"])
def atualizar_cargo():
    return jsonify(cargos_service.atualizar(request.form))


@bp.route("/cargos", methods=["DELETE"])
def excluir_cargo():
    return jsonify(cargos_service.excluir(request.form))


# =========================
# LANÇAMENTOS
# =========================
@bp.route("/lancamentos", methods=["POST"])
def api_criar_lancamento():
    dados = request.form
    resultado = criar_lancamento(dados)
    status_code = 200 if resultado.get("success") else 400
    return jsonify(resultado), status_code


# =========================
# DASHBOARD
# =========================

# Ranking de linhas com férias (AGRUPADO POR LINHA)
@bp.route("/dashboard/linhas/ferias", methods=["GET"])
def api_ranking_linhas_ferias():
    filtros = {
        "data_inicial": request.args.get("data_inicial"),
        "data_final": request.args.get("data_final"),
        "turno": request.args.get("turno"),
        "filial": request.args.get("filial")
    }
    return jsonify(ranking_linhas_ferias(filtros))


# Faltas por linha (modal)
@bp.route("/dashboard/linha/cargos", methods=["GET"])
def api_faltas_linha():
    filtros = {
        "data_inicial": request.args.get("data_inicial"),
        "data_final": request.args.get("data_final"),
        "turno": request.args.get("turno"),
        "filial": request.args.get("filial")
    }
    linha = request.args.get("linha")
    return jsonify(faltas_por_linha(linha, filtros))


# Férias por linha (modal)
@bp.route("/dashboard/linha/ferias_cargos", methods=["GET"])
def api_ferias_linha_cargos():
    filtros = {
        "data_inicial": request.args.get("data_inicial"),
        "data_final": request.args.get("data_final"),
        "turno": request.args.get("turno"),
        "filial": request.args.get("filial")
    }
    linha = request.args.get("linha")
    return jsonify(ferias_por_linha_cargos(linha, filtros))

@bp.route("/atestados", methods=["POST"])
def api_atestado():
    return jsonify(registrar_atestado(request.form))

@bp.route("/linhas", methods=["GET"])
def api_linhas_por_setor():
    setor = request.args.get("setor")
    linhas = {
        "IM": ["IM-01", "IM-02"],
        "PA": ["PA-01", "PA-02"],
        "SMT": ["SMT-01", "SMT-02"],
        "PTH": ["PTH-01"],
        "VTT": ["VTT-01"]
    }
    if not setor or setor == "Todos":
        return jsonify([])
    return jsonify(linhas.get(setor, []))

@bp.route("/relatorios", methods=["GET"])
def api_relatorios():
    setor = request.args.get("setor") or None
    tipo = request.args.get("tipo", "MENSAL")

    dados = gerar_relatorio(setor, tipo)
    return jsonify(dados)


