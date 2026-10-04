import sys

from .agent import ask
from .config import validate_config


def main() -> None:
    validate_config()

    # Modo one-shot: python -m src.main "pergunta"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(ask(question))
        return

    # Modo interativo
    print("🎬 CineData Agent — pergunte sobre o catálogo de filmes")
    print("   (digite 'sair' ou Ctrl+C para encerrar)\n")

    while True:
        try:
            question = input("❓ ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not question or question.lower() in {"sair", "exit", "quit"}:
            break

        try:
            print("\n🤖 Pensando...\n")
            print(ask(question))
            print()
        except Exception as e:
            print(f"❌ Erro: {e}\n")


if __name__ == "__main__":
    main()