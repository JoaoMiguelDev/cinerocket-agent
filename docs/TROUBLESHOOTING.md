# Erros Comuns

---

## `❌ Chave OpenRouter não encontrada ou inválida`

**Causa:** o arquivo `.env` não foi encontrado ou está mal formatado.

**Verificações:**

1. O arquivo se chama `.env` (não `.env.txt`)?
   - **Windows:** ative "Extensões de nomes de arquivos" no Explorer.
2. Está na **raiz do projeto** (mesmo nível de `src/`)?
3. O formato está correto?

   ✅ Correto:
   ```
   OPENROUTER_API_KEY=sk-or-v1-abc123
   ```

   ❌ Errado:
   ```
   OPENROUTER_API_KEY = sk-or-v1-abc123
   OPENROUTER_API_KEY="sk-or-v1-abc123"
   OPENROUTER_API_KEY=sk-or-v1-abc123;
   ```

---

## `❌ Erro na chamada OpenRouter: 401`

**Causa:** chave inválida ou expirada.

**Solução:** gere uma nova em [openrouter.ai/keys](https://openrouter.ai/keys)
e atualize o `.env`.

---

## `❌ 429 upstream_provider`

**Causa:** pool do provider lotado. **Não é a sua cota.**

**Solução:** o agente já troca de modelo automaticamente. Se persistir,
aguarde alguns minutos.

---

## `❌ 429` (sem menção a provider)

**Causa:** cota diária de 50 requests atingida.

**Solução:**
- Verifique em [openrouter.ai/activity](https://openrouter.ai/activity).
- O reset ocorre à **meia-noite UTC** — **21h no horário de Brasília**.

---

## `ModuleNotFoundError: No module named 'src'`

**Causa:** comando executado de dentro de `src/`.

**Solução:** rode da **raiz do projeto**, usando `python -m src.main`
(com o `-m`).

---

## `sqlite3.OperationalError: no such table: ...`

**Causa:** arquivo `cinerocket.db` não está em `data/`.

**Solução:** coloque o arquivo em `data/cinerocket.db`. Verifique com:

```bash
python -c "from src.db import list_tables; print(list_tables())"
```

Saída esperada: 10 tabelas do modelo dimensional.

---

## Agente repetindo a mesma query

**Causa:** limitação do modelo gratuito `nvidia/nemotron-3.5-lightning:free`.

**Mitigações já aplicadas:**
- Regras anti-loop no system prompt.
- `MAX_STEPS = 3` em `config.py`.

**Se persistir:**
- Reduza `MAX_STEPS` para 2.
- Troque o modelo principal em `config.py` para outro da lista.

---

## Cache retornando resposta antiga

**Causa:** após ajustar o prompt, o cache guarda respostas do prompt anterior.

**Solução:** apague o cache:

```bash
# Windows
Remove-Item .cache -Recurse -Force

# macOS/Linux
rm -rf .cache
```

Rode novamente — a próxima execução vai regenerar.