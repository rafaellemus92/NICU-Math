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

## Math lab (math/)

The `math/` folder is separate from the app above: nothing in the app uses it.
It holds Lean 4 proofs, audits and numerical checks done with Claude in
October 2026: the coupled prime-26 pangram (smallest sum 4296, proved in Lean),
Lean + Mathlib proofs about the rainbow, body water, the Shared Air model and
periodic Navier–Stokes fields, an audit of ChatGPT's Navier–Stokes phase lab
with a second exact enstrophy series (`math/ns-phase-audit/enstrophy-jet/`),
an audit of the Shared Air page (`math/shared-air/`; the page itself is
`web/public/shared-air/`, live at https://nicu-math.vercel.app/shared-air),
a physics and biology fact-check with a plain-language companion and a draft
letter (`math/letters/`), a 1D Hou–Luo blowup lab, and the prime-word
perfect-pangram search (formerly `pangram/` at the root).

Start with [`math/README.md`](math/README.md). CI builds both Lean projects on
push ([`.github/workflows/lean.yml`](.github/workflows/lean.yml)).
