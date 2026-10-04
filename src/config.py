import os
from pathlib import Path
from dotenv import load_dotenv

# Raiz do projeto (um nível acima de src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega .env sempre da raiz, independente do cwd
load_dotenv(BASE_DIR / ".env")

# ---- OpenRouter ----
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ---- Banco ----
DB_PATH = BASE_DIR / "data" / "cinerocket.db"

# ---- Modelos (ordem = prioridade de fallback) ----
MODEL_FALLBACKS = [
    "nvidia/nemotron-3.5-lightning:free",
    "z-ai/glm-5.2:free",
    "google/gemma-4-26b-a4b-it:free",
]

# ---- Limites do agente ----
MAX_STEPS = 4          # máximo de iterações do agente por pergunta
MAX_ROWS = 500         # máximo de linhas retornadas por query


def validate_config() -> None:
    """Valida configuração essencial no start do app."""
    if not OPENROUTER_API_KEY or not OPENROUTER_API_KEY.startswith("sk-or-v1-"):
        raise ValueError(
            "OPENROUTER_API_KEY não configurada corretamente. "
            "Verifique o arquivo .env na raiz do projeto "
            "(e confirme que ele não virou .env.txt)."
        )
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Banco não encontrado em: {DB_PATH}")