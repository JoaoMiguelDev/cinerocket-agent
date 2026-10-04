# Decisões de Design

Documento com as principais escolhas técnicas do projeto e suas justificativas.

---

## Por que Smolagents?

- **Leve** — poucas dependências, ideal para um projeto pequeno.
- **Compatível com qualquer endpoint OpenAI**, incluindo OpenRouter.
- **Loop curto** — cada pergunta consome ~2 requests (essencial no free tier).
- **Tool calling nativo** — o modelo chama `run_sql` diretamente.

---

## Por que o schema vai no system prompt?

Ler o schema é **local e gratuito** (via `PRAGMA table_info`). Colocá-lo no
prompt evita gastar uma chamada de LLM só para "descobrir" as tabelas.
Isso é essencial dentro do limite de 50 requests/dia do OpenRouter free.

---

## Por que apenas uma tool?

Frameworks multi-agente queimam cota. Aqui, o agente tem uma **única tool**
(`run_sql`) e decide sozinho quando usá-la. Loop enxuto.

---

## Por que cache?

O limite é de 50 requests/dia. Perguntas repetidas (comuns em demonstrações)
retornam instantaneamente do cache local (`.cache/`), sem gastar cota.

---

## Por que fallback entre modelos?

O OpenRouter pode retornar `429 (upstream_provider)` quando o pool do
provider está lotado — **não é a cota do usuário**. Trocar de modelo resolve.
Lista de fallbacks em `config.py`:

```python
MODEL_FALLBACKS = [
    "nvidia/nemotron-3.5-lightning:free",
    "z-ai/glm-5.2:free",
    "google/gemma-4-26b-a4b-it:free",
]
```

---

## Por que o guardrail é regex simples?

Bloquear palavras-chave (`DROP`, `DELETE`, `UPDATE`...) e exigir que a query
comece com `SELECT`/`WITH` cobre 99% dos casos em demonstração. Em produção,
usaríamos um usuário SQL read-only no banco.

Validações implementadas em `db.is_safe_select()`:
- Precisa começar com `SELECT` ou `WITH`
- Bloqueia múltiplas queries (`;`)
- Bloqueia palavras proibidas (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `TRUNCATE`, `PRAGMA`, `VACUUM`, etc.)

---

## Anti-loop

O modelo gratuito ocasionalmente **repete a mesma tool call** múltiplas
vezes. Mitigações aplicadas:

1. Instruções explícitas no system prompt (regras 9-11) proibindo repetição.
2. `MAX_STEPS = 3` no agente.
3. Instrução para preferir resposta parcial a múltiplas tentativas.

---

## Limitações conhecidas

### Do modelo

- `nvidia/nemotron-3.5-lightning:free` ainda pode repetir tool calls em
  perguntas complexas. Um modelo maior (pago) reduziria isso.

### Do dataset

- Apenas **~3.400 dos ~95.600 filmes** têm `receita_usd` e `orcamento_usd`.
  Rankings financeiros trabalham sobre esse subconjunto.
- A coluna `popularidade` tem valores **suspeitos** em alguns registros
  (ex: `2018.0`, `2019.0` — parecem anos). Retornamos o que está no banco.
- O catálogo contém muito conteúdo **WWE**, o que domina rankings de
  "atores/diretores que mais trabalharam juntos". Característica real
  dos dados, não bug.
- `dim_reviews` tem **múltiplas linhas por filme** — contagens agregadas
  com `SUM()`.

### Da arquitetura

- Sem memória de conversa entre perguntas.
- Sem busca semântica nas sinopses (evolução futura).
- Guardrails regex não são à prova de SQL ofuscado.