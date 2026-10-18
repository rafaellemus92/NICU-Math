# NICU-Math

Math and models from the NICU: evidence search, breathing and heart rhythms, and fluid equations.
Each folder is self-contained, with its own README and reproduction commands.

| Part | What it is |
|---|---|
| top level | **NICU Evidence Search & Scenario Engine**: PDF ingestion, hybrid search and a Bayesian scenario calculator (described below). Note: its quickstart refers to `api/` and `ui/` folders, but the files currently sit at the top level. |
| [`shared-air/`](shared-air/) | **Shared Air**: an interactive cells-to-pair model of mother–infant heart and breathing coupling, corrected after an independent audit (`AUDIT.md`), with scripts that reproduce every check. |
| [`navier-stokes-jet/`](navier-stokes-jet/) | The **exact time series of enstrophy** for a family of 3D Navier–Stokes flows, through t¹⁴, with two selection rules and an honest account of how far the series can be trusted. |
| [`hou-luo/`](hou-luo/) | A **1D Hou–Luo blowup lab**: an adaptive-mesh solver that follows the model's inviscid singularity (a toy model, not 3D Navier–Stokes). |
| [`letters/`](letters/) | A draft email to Steven Strogatz and **"The words that drew me in"**: the shared vocabulary of breath, loops and turbulence, with every claim labeled true, open, analogy or doesn't hold, and full sources. |
| [`pangram/`](pangram/) | Prime perfect pangrams: reproduction, relaxation and an exact count. |

---

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
