import re
import sqlite3
from contextlib import contextmanager
from typing import Iterator

from .config import DB_PATH, MAX_ROWS

# Palavras proibidas (bloqueio de escrita/DDL/DCL)
_FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter", "create",
    "truncate", "replace", "attach", "detach", "pragma",
    "vacuum", "reindex", "grant", "revoke",
}


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Abre uma conexão SQLite com row_factory configurado."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def list_tables() -> list[str]:
    """Retorna as tabelas do modelo dimensional (ignora sqlite_* e alembic_version)."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table'
              AND name NOT LIKE 'sqlite_%'
              AND name != 'alembic_version'
            ORDER BY name;
            """
        )
        return [row["name"] for row in cur.fetchall()]


def get_schema() -> str:
    """
    Monta uma representação textual do schema:
    tabela(coluna TIPO, coluna TIPO, ...)
    Isso vai direto no system prompt do agente.
    """
    linhas = []
    with get_connection() as conn:
        cur = conn.cursor()
        for tabela in list_tables():
            cur.execute(f"PRAGMA table_info({tabela});")
            cols = cur.fetchall()
            col_defs = ", ".join(f"{c['name']} {c['type'] or 'TEXT'}" for c in cols)
            linhas.append(f"{tabela}({col_defs})")
    return "\n".join(linhas)


def is_safe_select(sql: str) -> tuple[bool, str]:
    """
    Verifica se a query é um SELECT somente-leitura.
    Retorna (True, "") se ok, ou (False, motivo) se bloqueada.
    """
    if not sql or not sql.strip():
        return False, "Query vazia."

    normalized = sql.strip().lower()

    # Precisa começar com SELECT ou WITH (CTE)
    if not (normalized.startswith("select") or normalized.startswith("with")):
        return False, "Apenas consultas SELECT são permitidas."

    # Bloqueia múltiplas queries (ex: SELECT ...; DROP ...)
    if ";" in normalized.rstrip(";").rstrip():
        return False, "Múltiplas queries não são permitidas."

    # Bloqueia palavras proibidas (busca por palavra inteira)
    for palavra in _FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{palavra}\b", normalized):
            return False, f"Comando proibido detectado: {palavra.upper()}."

    return True, ""


def execute_query(sql: str, max_rows: int = MAX_ROWS) -> list[dict]:
    """Executa um SELECT validado e retorna lista de dicionários."""
    ok, motivo = is_safe_select(sql)
    if not ok:
        raise ValueError(f"Query bloqueada pelo guardrail: {motivo}")

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchmany(max_rows)
        return [dict(row) for row in rows]