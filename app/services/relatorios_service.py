# app/services/relatorios_service.py
from app.extensions import get_db
from psycopg.rows import dict_row
from datetime import date, timedelta


def _formatar_data_br(d: date) -> str:
    """Formata data para padrão brasileiro DD-MM-YYYY"""
    return d.strftime("%d-%m-%Y")


def gerar_relatorio(setor, tipo):
    hoje = date.today()

    if tipo == "SEMANAL":
        data_inicial = hoje - timedelta(days=7)
    elif tipo == "MENSAL":
        data_inicial = hoje.replace(day=1)
    else:
        data_inicial = hoje.replace(month=1, day=1)

    where = [
        "lc.tipo = 'FALTA'",
        "l.data BETWEEN %s AND %s"
    ]
    params = [data_inicial, hoje]

    if setor:
        where.append("l.setor = %s")
        params.append(setor)

    where_sql = " AND ".join(where)

    query = f"""
        SELECT
            l.linha,
            SUM(lc.quantidade) AS total_faltas
        FROM lancamentos l
        JOIN lancamentos_cargos lc ON lc.lancamento_id = l.id
        WHERE {where_sql}
        GROUP BY l.linha
        ORDER BY total_faltas DESC
    """

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(query, params)
            linhas = cur.fetchall() or []

    total_faltas = sum(l["total_faltas"] for l in linhas)
    linhas_criticas = [l for l in linhas if l["total_faltas"] > 0]

    cargo_query = """
        SELECT
            c.nome,
            SUM(lc.quantidade) AS total
        FROM lancamentos_cargos lc
        JOIN cargos c ON c.id = lc.cargo_id
        JOIN lancamentos l ON l.id = lc.lancamento_id
        WHERE lc.tipo = 'FALTA'
          AND l.data BETWEEN %s AND %s
        GROUP BY c.nome
        ORDER BY total DESC
        LIMIT 1
    """

    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(cargo_query, (data_inicial, hoje))
            cargo = cur.fetchone()

    return {
        "periodo": f"{_formatar_data_br(data_inicial)} até {_formatar_data_br(hoje)}",
        "kpis": {
            "total_faltas": total_faltas,
            "linhas_afetadas": len(linhas_criticas),
            "linhas_totais": len(linhas)
        },
        "linhas": linhas[:10],
        "cargo_critico": cargo,
        "insight": (
            "Nível de absenteísmo elevado requer atenção gerencial."
            if total_faltas > 0 else
            "Não foram identificadas faltas relevantes no período."
        )
    }
