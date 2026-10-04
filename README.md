# 🎬 CineData Agent

Agente **Text-to-SQL** que permite fazer perguntas em português sobre o
catálogo de filmes da CineData Analytics e receber respostas em linguagem
natural. O agente gera SQL automaticamente, executa com guardrail
(SELECT-only) e formata a resposta.

Projeto desenvolvido para o **Rocket Lab 26.2 — GenAI**.

---

## Como funciona

```
Pergunta em PT  →  LLM gera SQL  →  Guardrail  →  SQLite  →  Resposta em PT
```

O agente usa a tool `run_sql` para consultar as 10 tabelas da camada
Gold do projeto CineData (arquivo `cinerocket.db`).

---

## Stack

- **Python 3.10+**
- **Smolagents** (framework de agentes da Hugging Face)
- **OpenRouter** com modelos gratuitos (`nvidia/nemotron-3.5-lightning:free`)
- **SQLite3** (embutido no Python)

---

## Setup

### 1. Clonar e criar ambiente virtual

```bash
git clone https://github.com/SEU_USUARIO/cinerocket-agent.git
cd cinerocket-agent
python -m venv venv
```

Ativar o venv:
- **Windows:** `venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source venv/bin/activate`

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Obter chave do OpenRouter

1. Crie uma conta gratuita em [openrouter.ai](https://openrouter.ai).
2. Acesse [openrouter.ai/keys](https://openrouter.ai/keys) → **Create Key**.
3. Copie a chave (começa com `sk-or-v1-...`).

### 4. Criar o arquivo `.env`

Na raiz do projeto, crie um arquivo `.env` (começa com ponto):

```env
OPENROUTER_API_KEY=sk-or-v1-sua_chave_aqui
```

> ⚠️ **Windows:** o Bloco de Notas pode salvar como `.env.txt`. Ative
> "Extensões de nomes de arquivos" no Explorer para conferir.

### 5. Colocar o banco em `data/`

Mova o arquivo `cinerocket.db` para a pasta `data/`:

```
cinerocket-agent/
├─ data/
│  └─ cinerocket.db
```

### 6. Validar setup

```bash
python -m src.test_setup
```

Saída esperada:
```
✅ Chave OpenRouter carregada.
✅ Banco acessível. Tabelas encontradas: 11
✅ OpenRouter respondeu: OK
```

Se algo falhar, veja [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

---

## Como usar

### Pergunta única

```bash
python -m src.main "Quais são os 5 filmes com maior receita em R$?"
```

### Modo interativo

```bash
python -m src.main
```

```
🎬 CineData Agent — pergunte sobre o catálogo de filmes
   (digite 'sair' ou Ctrl+C para encerrar)

❓ Qual a produtora com maior lucro total?

A produtora com maior lucro total é a Marvel Studios, com um lucro
total de US$ 15.638.957.726.
```

### Exemplos de perguntas

- Top 10 filmes com maior receita em R$
- Os 5 filmes mais populares
- Diretores com maior nota média (mínimo de 5 filmes)
- Quantidade de filmes por gênero
- Filmes mais avaliados pelos usuários

---

## Estrutura do projeto

```
cinerocket-agent/
├─ data/
│  └─ cinerocket.db          # banco Gold (não versionado)
├─ docs/
│  ├─ DESIGN.md              # decisões de arquitetura
│  ├─ EVAL.md                # conjunto de avaliação
│  └─ TROUBLESHOOTING.md     # erros comuns
├─ src/
│  ├─ config.py              # configuração e fallbacks
│  ├─ db.py                  # conexão + guardrail
│  ├─ tools.py               # tool run_sql
│  ├─ agent.py               # agente + cache
│  └─ main.py                # CLI
├─ tests/
│  ├─ eval_questions.json
│  └─ run_eval.py
├─ .env.example
├─ requirements.txt
└─ README.md
```

---

## Documentação adicional

- [**Decisões de design**](docs/DESIGN.md) — por que Smolagents, cache, fallbacks, guardrail
- [**Conjunto de avaliação**](docs/EVAL.md) — 12 perguntas com ground truth
- [**Erros comuns**](docs/TROUBLESHOOTING.md) — `.env.txt`, 429, módulo não encontrado

