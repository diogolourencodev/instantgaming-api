# Instant Gaming API — Detailed Documentation

This project is a Flask application that exposes an API to search game prices on Instant Gaming and, when possible, prioritizes "Latin America" pricing. Documentation is provided in English and Portuguese to match the embedded docs in `index.html`.

— Base URL (local): `http://127.0.0.1:5000`
— Base URL (Vercel): `https://instantgaming.vercel.app` (if deployed)

---

## English (EN)

### Overview

- Purpose: Query Instant Gaming search results using only a query string, optionally enriching with Latin America prices.
- Framework: Flask
- Entry: `app.py`
- Templates: `templates/`
- Static assets: `static/`
- Search logic: `reqs.py`
- Language policy: Requests use English headers (`Accept-Language: en-US,en;q=0.9`).

### Routes

- `GET /` — Home, embedded documentation (EN/PT).
- `GET /search` — UI page to search games.
- `GET /health` — Simple health check.

### API Endpoint

`GET /api/search?query=QUERY`

- Query parameters:

  - `query` (string, required): game name. Example: `elden ring`.
  - `latam_priority` (optional): `1` (default) enriches results by checking product pages; `0` skips for speed.
  - `max_details` (optional, integer): number of items to enrich when `latam_priority=1` (default `6`).
  - `concurrency` (optional, integer): concurrency level for enrichment (default `6`).
- Legacy route: `GET /api/search/<game>` — Redirects to `GET /api/search?query=<game>`.
- Underlying IG URL (no filters):

  - `https://www.instant-gaming.com/pt/pesquisar/?query=QUERY`

### Response

Returns a JSON array of objects:

```
[
	{
		"link": "https://www.instant-gaming.com/pt/awdadwadwd",
		"origin": "Instant Gaming",
		"price": "R$ 25,67",
		"title": awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdadwadwad",
		"origin": "Instant Gaming",
		"price": "R$ 158,47",
		"title": "awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdadwad",
		"origin": "Instant Gaming",
		"price": "R$ 11,03",
		"title": "awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdawdawda",
		"origin": "Instant Gaming",
		"price": "R$ 20,50",
		"title": "awd"
	}
]
```

- Empty results: returns `[]`.
- Errors: missing `query` returns `{ "error": "Missing 'query' parameter" }` with status `400`.

### Examples

```
# Local
curl "http://127.0.0.1:5000/api/search?query=elden%20ring"

# Vercel
curl "https://instantgaming.vercel.app/api/search?query=elden%20ring"

# Faster (skip LATAM enrichment)
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&latam_priority=0"

# Tune concurrency and max enriched items
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&concurrency=4&max_details=4"
```

### Performance & Behavior

- Connection reuse with `requests.Session` for faster requests.
- Optional LATAM enrichment on product pages using concurrent requests.
- Timeouts: `20s` for search page, `12s` for product pages.
- Filters (platform/type/gametype) are disabled and will return later.
- Currency may differ when deployed (IG serves varying locales).

### Project Structure

- `app.py` — Flask app and route definitions.
- `reqs.py` — Search implementation and enrichment logic.
- `templates/` — HTML templates (`index.html`, `search.html`).
- `static/` — CSS and other static assets.

### Run Locally (Windows)

```
git clone https://github.com/diogolourencodev/latamgaming.git
cd latamgaming
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

### Deploy (Vercel)

- Connect your GitHub repo.
- Import project; Vercel detects Flask automatically.
- Set root to the repo folder if needed; deploy.
- Test `GET /api/search?query=elden%20ring`.

### Roadmap

- Reintroduce filter parameters (platform, type, gametype).
- Provide `POST /api/search` with JSON body.
- Add caching, pagination, and currency normalization.
- Improve `/search` UI with bilingual support and filter controls.

---

## Português (PT-BR)

### Visão Geral

- Propósito: Consultar resultados de busca da Instant Gaming usando apenas a string de pesquisa, opcionalmente enriquecendo com preços da América Latina.
- Framework: Flask
- Entrada: `app.py`
- Templates: `templates/`
- Arquivos estáticos: `static/`
- Lógica de busca: `reqs.py`
- Política de idioma: Requisições usam cabeçalhos em inglês (`Accept-Language: en-US,en;q=0.9`).

### Rotas

- `GET /` — Página inicial, documentação incorporada (EN/PT).
- `GET /search` — Página de UI para buscar jogos.
- `GET /health` — Verificação simples de saúde.

### Endpoint da API

`GET /api/search?query=QUERY`

- Parâmetros de query:

  - `query` (string, obrigatório): nome do jogo. Ex.: `elden ring`.
  - `latam_priority` (opcional): `1` (padrão) enriquece resultados consultando páginas de produto; `0` para velocidade.
  - `max_details` (opcional, inteiro): quantidade de itens a enriquecer quando `latam_priority=1` (padrão `6`).
  - `concurrency` (opcional, inteiro): nível de concorrência para enriquecimento (padrão `6`).
- Rota legada: `GET /api/search/<game>` — Redireciona para `GET /api/search?query=<game>`.
- URL do IG (sem filtros):

  - `https://www.instant-gaming.com/pt/pesquisar/?query=QUERY`

### Resposta

Retorna um array JSON de objetos:

```
[
	{
		"link": "https://www.instant-gaming.com/pt/awdadwadwd",
		"origin": "Instant Gaming",
		"price": "R$ 25,67",
		"title": awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdadwadwad",
		"origin": "Instant Gaming",
		"price": "R$ 158,47",
		"title": "awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdadwad",
		"origin": "Instant Gaming",
		"price": "R$ 11,03",
		"title": "awd"
	},
	{
		"link": "https://www.instant-gaming.com/pt/awdawdawda",
		"origin": "Instant Gaming",
		"price": "R$ 20,50",
		"title": "awd"
	}
]
```

- Resultados vazios: retorna `[]`.
- Erros: ausência de `query` retorna `{ "error": "Missing 'query' parameter" }` com status `400`.

### Exemplos

```
# Local
curl "http://127.0.0.1:5000/api/search?query=elden%20ring"

# Vercel
curl "https://instantgaming.vercel.app/api/search?query=elden%20ring"

# Mais rápido (sem enriquecimento LATAM)
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&latam_priority=0"

# Ajustar concorrência e itens enriquecidos
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&concurrency=4&max_details=4"
```

### Desempenho & Comportamento

- Reutilização de conexões com `requests.Session` para respostas mais rápidas.
- Enriquecimento opcional de páginas de produto usando requisições concorrentes.
- Timeouts: `20s` para a página de busca, `12s` para páginas de produto.
- Filtros (platform/type/gametype) estão desativados e retornarão futuramente.
- Moeda pode variar quando implantado (IG serve diferentes localidades).

### Estrutura do Projeto

- `app.py` — Aplicação Flask e definição das rotas.
- `reqs.py` — Implementação da busca e lógica de enriquecimento.
- `templates/` — Templates HTML (`index.html`, `search.html`).
- `static/` — CSS e arquivos estáticos.

### Executar Localmente (Windows)

```
git clone https://github.com/diogolourencodev/latamgaming.git
cd latamgaming
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python app.py
# abrir http://127.0.0.1:5000
```

### Deploy (Vercel)

- Conecte seu repositório GitHub.
- Importe o projeto; o Vercel detecta Flask automaticamente.
- Ajuste o root para a pasta do repositório se necessário; faça o deploy.
- Teste `GET /api/search?query=elden%20ring`.

### Roadmap

- Reintroduzir parâmetros de filtro (platform, type, gametype).
- Disponibilizar `POST /api/search` com corpo JSON.
- Adicionar cache, paginação e normalização de moeda.
- Melhorar a UI de `/search` com suporte bilíngue e filtros.
