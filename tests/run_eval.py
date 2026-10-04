"""
Executa o conjunto de avaliação: roda cada SQL esperada no banco (ground truth),
depois consulta o agente e verifica se a resposta contém as palavras-chave.

Uso:
    python -m tests.run_eval            # roda todas
    python -m tests.run_eval --only 1 4 # roda só alguns IDs
    python -m tests.run_eval --no-agent # só valida as SQLs esperadas (não gasta requests)
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.agent import ask
from src.db import execute_query

EVAL_FILE = Path(__file__).parent / "eval_questions.json"


def load_questions() -> list[dict]:
    return json.loads(EVAL_FILE.read_text(encoding="utf-8"))


def run_ground_truth(sql: str) -> list[dict]:
    return execute_query(sql)


def check_answer(answer: str, must_contain: list[str]) -> bool:
    if not must_contain:
        return True
    answer_lower = answer.lower()
    return all(termo.lower() in answer_lower for termo in must_contain)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=int, nargs="*", help="IDs para rodar")
    parser.add_argument("--no-agent", action="store_true",
                        help="Só roda ground truth (não chama o LLM)")
    args = parser.parse_args()

    questions = load_questions()
    if args.only:
        questions = [q for q in questions if q["id"] in args.only]

    passou = 0
    falhou = 0
    resultados = []

    for q in questions:
        print(f"\n{'='*70}")
        print(f"[{q['id']}] {q['categoria']}")
        print(f"❓ {q['pergunta']}")
        print(f"{'='*70}")

        # Ground truth
        try:
            gt = run_ground_truth(q["sql_ground_truth"])
        except Exception as e:
            print(f"❌ Erro na SQL ground truth: {e}")
            falhou += 1
            continue

        print(f"📊 Ground truth ({len(gt)} linhas):")
        for row in gt[:5]:
            print(f"   {row}")

        if args.no_agent:
            continue

        # Agente
        t0 = time.time()
        try:
            resposta = ask(q["pergunta"])
        except Exception as e:
            print(f"❌ Erro no agente: {e}")
            falhou += 1
            continue
        dt = time.time() - t0

        print(f"\n🤖 Resposta do agente ({dt:.1f}s):")
        print(f"   {resposta[:500]}{'...' if len(resposta) > 500 else ''}")

        # Check
        ok = check_answer(resposta, q.get("must_contain", []))
        status = "✅ PASSOU" if ok else "❌ FALHOU"
        print(f"\n{status}")
        if not ok:
            print(f"   Esperado conter: {q['must_contain']}")

        resultados.append({"id": q["id"], "passou": ok, "tempo": dt})
        if ok:
            passou += 1
        else:
            falhou += 1

    print(f"\n{'='*70}")
    print(f"RESUMO: {passou} passou / {falhou} falhou / {passou+falhou} total")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()