import sys
from .db import execute_query


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python -m src.run_query \"SELECT ...\"")
        return
    query = sys.argv[1]
    try:
        rows = execute_query(query)
        for r in rows:
            print(r)
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()