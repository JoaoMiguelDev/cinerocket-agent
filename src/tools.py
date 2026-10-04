import json
from smolagents import tool

from .db import execute_query


@tool
def run_sql(query: str) -> str:
    """
    Executa uma consulta SELECT no banco SQLite do catálogo CineData e retorna
    o resultado em formato JSON.

    Use esta tool SEMPRE que precisar consultar dados de filmes, gêneros,
    pessoas, produtoras, avaliações, bilheteria, lucro, popularidade, etc.

    Args:
        query: A consulta SQL (somente SELECT) a ser executada no banco.
    """
    try:
        rows = execute_query(query)
        return json.dumps(rows, ensure_ascii=False, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)