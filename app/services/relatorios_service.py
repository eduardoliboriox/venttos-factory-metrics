# app/services/relatorios_service.py
from app.extensions import get_db
from psycopg.rows import dict_row
from datetime import date, timedelta


def gerar_relatorio(setor, tipo):
    hoje = date.today()

    if tipo == "SEMANAL":
        data_inicial = hoje - timedelta(days=7)
    elif tipo == "MENSAL":
        data_inicial = hoje.replace(day=1)
    else:
        data_inicial = hoje.replace(month=1, day=1)

    query = """
        SELECT
            l.linha,
            COALESCE(SUM(lc.quantidade), 0) AS total_faltas,
            ROUND(
                COALESCE(SUM(lc.quantidade), 0) * 100.0
                / NULLIF(SUM(SUM(lc.quantidade)) OVER (), 0),
                1
            ) AS percentual
        FROM lancamentos l
        JOIN lancamentos_cargos lc ON lc.lancamento_id = l.id
        WHERE lc.tipo = 'FALTA'
          AND l.data BETWEEN %s AND %s
          AND (%s IS NULL OR l.setor = %s)
        GROUP BY l.linha
        ORDER BY total_faltas DESC
        LIMIT 10
    """


    with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                query,
                (data_inicial, hoje, setor, setor)
            )
            linhas = cur.fetchall() or []

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
        "periodo": f"{data_inicial} até {hoje}",
        "linhas": linhas,
        "cargo_critico": cargo
    }
