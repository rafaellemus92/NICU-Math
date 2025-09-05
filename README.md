# NICU Evidence Search & Scenario Engine — Extended (Full Code)

**Features**
- PDF ingestion (folder or single file)
- Hybrid retrieval: pgvector semantic + Postgres full‑text (FTS)
- Cross‑encoder reranker (MS‑MARCO MiniLM) for precision
- PICO‑lite extraction (year, N, study type, effect) from snippets
- Bayesian scenario endpoint (priors + LRs ± CI → posterior)
- Streamlit UI: Evidence (table), Scenario, Admin ingest
- Docker Compose for db/api/ui

## Quickstart (Docker)
1) Copy `.env.example` → `.env`
2) Put a few PDFs into `./library/`
3) `docker compose up --build`
4) Open http://localhost:8501 → Evidence → “Search & Build Table”

## Local (no Docker)
- Start Postgres with pgvector (e.g. `docker run --name nicu-db -e POSTGRES_PASSWORD=nicu -p 5432:5432 -d pgvector/pgvector:pg16`)
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r api/requirements.txt`
- `uvicorn app.main:app --app-dir api/app --reload`
- `pip install -r ui/requirements.txt`
- `streamlit run ui/app.py`
