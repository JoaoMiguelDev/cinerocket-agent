# Conjunto de Avaliação

O projeto inclui **12 perguntas com ground truth SQL**, cobrindo todas as
categorias do enunciado. Cada item contém:

- Pergunta em linguagem natural
- Query SQL esperada (`sql_ground_truth`)
- Termos-chave que a resposta deve conter (`must_contain`)

Arquivo: [`tests/eval_questions.json`](../tests/eval_questions.json)

---

## Categorias cobertas

| # | Categoria | Pergunta |
|---|---|---|
| 1 | Bilheteria e Finanças | Top 5 filmes por receita em R$ |
| 2 | Bilheteria e Finanças | Lucro médio por gênero (com receita informada) |
| 3 | Bilheteria e Finanças | Maior margem de lucro |
| 4 | Popularidade e Engajamento | 5 filmes mais populares |
| 5 | Popularidade e Engajamento | Maior divergência nota TMDB vs IMDb |
| 6 | Popularidade e Engajamento | Nota média IMDb por ano (2021-2025) |
| 7 | Elenco e Equipe | Diretores com maior nota média (mín. 5 filmes) |
| 8 | Elenco e Equipe | Dupla ator-diretor que mais trabalhou junta |
| 9 | Gêneros e Produtoras | 5 gêneros com mais filmes |
| 10 | Gêneros e Produtoras | Produtora com maior lucro total |
| 11 | Avaliações dos Usuários | Filmes mais avaliados |
| 12 | Avaliações dos Usuários | Maior divergência nota usuários vs IMDb |

---

## Como rodar

**Só validar as SQLs (não gasta requests):**
```bash
python -m tests.run_eval --no-agent
```

**Rodar perguntas específicas:**
```bash
python -m tests.run_eval --only 1 4 7
```

**Rodar todas as 12 (consome ~30 requests):**
```bash
python -m tests.run_eval
```