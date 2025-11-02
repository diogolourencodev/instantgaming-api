# Instant Gaming API

Open-source, non-profit API and UI to search game prices on Instant Gaming, optionally prioritizing Latin America pricing when available.

Base URL (local): `http://127.0.0.1:5000`
Base URL (Vercel): `https://instantgaming.vercel.app` (if deployed)

---

## English (EN)

### Overview

- Purpose: Query Instant Gaming search results using only a query string, optionally enriching with Latin America prices.
- Framework: Flask · Entry: `app.py` · Templates: `templates/` · Static: `static/` · Logic: `reqs.py`
- Language policy: Requests use English headers (`Accept-Language: en-US,en;q=0.9`).
- Note: When running on Vercel, pricing may reflect a different locale; for consistent BRL, run locally.

### Routes

- `GET /` — Home with embedded bilingual docs.
- `GET /search` — UI page to search games.
- `GET /health` — Health check.

### API Endpoint

`GET /api/search?query=QUERY`

- Query parameters:
  - `query` (string, required): game name (e.g., `elden ring`).
  - `latam_priority` (optional): `1` (default) enriches results by checking product pages; `0` skips for speed.
  - `max_details` (optional, integer): number of items to enrich when `latam_priority=1` (default `6`).
  - `concurrency` (optional, integer): concurrency level for enrichment (default `6`).
- Legacy route: `GET /api/search/<game>` — Redirects to `GET /api/search?query=<game>`.

Examples:

```bash
# Local
curl "http://127.0.0.1:5000/api/search?query=elden%20ring"

# Faster (skip LATAM enrichment)
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&latam_priority=0"

# Adjust concurrency and max enriched items
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&concurrency=4&max_details=4"
```

### Run Locally (Windows)

```powershell
git clone https://github.com/diogolourencodev/latamgaming.git
cd latamgaming
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

### Project Structure

```
instantgaming-api/
├── app.py              # Flask app and route definitions
├── reqs.py             # Search implementation and enrichment logic
├── requirements.txt    # Python dependencies
├── docs.md             # Detailed documentation (EN and PT-BR)
├── static/
│   └── style.css       # Web UI styles
└── templates/
    ├── index.html      # Embedded docs (EN/PT)
    └── search.html     # Search UI
```

### Full Docs

For complete details, examples, and behavior notes, see `docs.md`.

---

## Português (PT-BR)

### Visão Geral

- Propósito: Consultar resultados de busca da Instant Gaming usando apenas a string de pesquisa, enriquecendo opcionalmente com preços da América Latina.
- Framework: Flask · Entrada: `app.py` · Templates: `templates/` · Estáticos: `static/` · Lógica: `reqs.py`
- Política de idioma: Requisições usam cabeçalhos em inglês (`Accept-Language: en-US,en;q=0.9`).
- Observação: Em Vercel, os preços podem refletir outra localidade; para BRL consistente, execute localmente.

### Rotas

- `GET /` — Página inicial com docs bilíngues.
- `GET /search` — Página de busca de jogos.
- `GET /health` — Verificação de saúde.

### Endpoint da API

`GET /api/search?query=QUERY`

- Parâmetros de consulta:
  - `query` (string, obrigatório): nome do jogo (ex.: `elden ring`).
  - `latam_priority` (opcional): `1` (padrão) enriquece resultados checando páginas de produto; `0` evita por desempenho.
  - `max_details` (opcional, inteiro): quantidade de itens enriquecidos quando `latam_priority=1` (padrão `6`).
  - `concurrency` (opcional, inteiro): nível de concorrência para enriquecimento (padrão `6`).
- Rota legada: `GET /api/search/<game>` — Redireciona para `GET /api/search?query=<game>`.

Exemplos:

```bash
# Local
curl "http://127.0.0.1:5000/api/search?query=elden%20ring"

# Mais rápido (sem enriquecimento LATAM)
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&latam_priority=0"

# Ajustar concorrência e itens enriquecidos
curl "http://127.0.0.1:5000/api/search?query=elden%20ring&concurrency=4&max_details=4"
```

### Executar Localmente (Windows)

```powershell
git clone https://github.com/diogolourencodev/latamgaming.git
cd latamgaming
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
# abrir http://127.0.0.1:5000
```

### Estrutura do Projeto

```
instantgaming-api/
├── app.py              # Aplicação Flask e rotas
├── reqs.py             # Implementação da busca e enriquecimento
├── requirements.txt    # Dependências Python
├── docs.md             # Documentação detalhada (EN e PT-BR)
├── static/
│   └── style.css       # Estilos da UI web
└── templates/
    ├── index.html      # Docs incorporados (EN/PT)
    └── search.html     # UI de busca
```

### Documentação Completa

Para detalhes completos, exemplos e comportamento, consulte `docs.md`.

---

## Contributing / Contribuição

Contributions are welcome! / Contribuições são bem-vindas!

1. Fork the repository / Faça um fork do repositório
2. Create a feature branch / Crie uma branch de feature
3. Commit your changes / Faça o commit
4. Push the branch / Faça o push
5. Open a Pull Request / Abra um Pull Request

## License / Licença

Open-source and non-profit. Built for the Brazilian and Latin American gaming community.

## Credits / Créditos

Created by https://github.com/diogolourencodev

---

Disclaimer: This project is not affiliated with Instant Gaming. It is an independent tool to facilitate price search.
