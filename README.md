# Instant Gaming API

Open-source, non-profit API to search game prices on Instant Gaming, prioritizing "Latin America" pricing when available.

Deploy: https://instantgaming.vercel.app (if configured)

## About

This is an open-source and non-profit project that provides a simple API to query game prices on Instant Gaming. When available, it prioritizes the "Latin America" region pricing, often surfacing BRL.

Note: Vercel servers are not located in Latin America. Results may differ from local BRL pricing when running in Vercel. For more consistent BRL results, run locally.

## Features

- Search API: `GET /api/search/<query>` with optional filters
- Web UI at `/search` with client-side price sorting
- English API parameters and responses
- Multi-platform search using Instant Gaming filters
- Responsive interface (desktop and mobile)

## Supported Platforms (IG keys)

- `steam`
- `epic+games`
- `battle.net`
- `gog.com`
- `microsoft+store`
- `playstation+store`
- `nintendo+eshop`
- `ea+app`
- `ubisoft+connect`
- `rockstar`
- `ncsoft`
- `instant+gaming`
- `other`

## API Endpoint

### GET `/api/search/<query>`

Quick search with optional filters.

Path parameter:

- `query`: game name (URL-encoded, e.g., `elden%20ring`).

Optional query parameters (English):

- `platform`: IG platform key (e.g., `steam`, `epic+games`). Empty means no platform filter.
- `type`: IG type key (e.g., `games`, `games-and-dlc`). Empty means no type filter.
- `gametype`: IG gametype (e.g., `games`, `all`). Empty means no gametype filter.
- `latam_priority`: `1` (default) to enrich prices by fetching product pages; `0` to skip for speed.
- `max_details`: how many items to enrich with LATAM pricing (default `6`).
- `concurrency`: number of concurrent detail fetches (default `6`).

Default IG URL when `platform` and `type` are empty:
`https://www.instant-gaming.com/pt/pesquisar/?platform[]=PLATAFORMA&type[]=TIPO&gametype=&query=QUERY`

Examples:

```bash
# Simple search
curl "http://127.0.0.1:5000/api/search/elden%20ring"

# With filters (English)
curl "http://127.0.0.1:5000/api/search/elden%20ring?platform=steam&type=games&gametype=games"

# Faster (skip LATAM), still English params
curl "http://127.0.0.1:5000/api/search/elden%20ring?latam_priority=0"
```

## Run Locally

```powershell
# 1) Clone the repository
git clone https://github.com/diogolourencodev/latamgaming.git
cd latamgaming

# 2) Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Start the server
python app.py

# 5) Open in browser
# http://127.0.0.1:5000
```

## Project Structure

```
instant-gaming-api/
├── app.py              # Flask application
├── reqs.py             # Instant Gaming search logic
├── requirements.txt    # Python dependencies
├── docs.md             # Detailed API documentation (English)
├── static/
│   └── style.css       # Web UI styles
└── templates/
    ├── index.html      # Landing page
    └── search.html     # Search interface
```

## Full Docs

For detailed API docs, usage examples, and behavior, see `docs.md`.

## Contributing

This is an open-source project. Contributions are welcome:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am "Add new feature"`)
4. Push the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## License

Open-source and non-profit. Built for the Brazilian and Latin American gaming community.

## Credits

Created by https://github.com/diogolourencodev

---

Disclaimer: This project is not affiliated with Instant Gaming. It is an independent tool to facilitate price search.
