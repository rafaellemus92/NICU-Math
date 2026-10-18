# AGENTS.md — NICU-Math

Instructions for Codex (ChatGPT cloud environment) working in this
repository.

> **Start by reading `RESEARCH.md` in this same directory.** It carries
> the research thesis, track structure, claim ledger, and voice.
> Everything below is operational advice specific to Codex's workflow.

---

## 1. The repo's spine lives in three files

- **`RESEARCH.md`** — thesis, methodology, claim ledger. Both AI
  collaborators read it.
- **`AGENTS.md`** — this file.
- **`CLAUDE.md`** — Claude-specific operational advice.

Never contradict RESEARCH.md from here. If you need to update the
spine, change RESEARCH.md explicitly and reference the change in your
commit message.

## 2. The two-AI workflow

Claude also contributes to this repo (via Claude Code / the GitHub
integration). You and Claude coordinate only through:

1. The repository itself (branches, PRs, PR comments).
2. The claim ledgers (`<track>/CLAIMS.md`).
3. This spine.

You will not see Claude's chat history and should not assume it. Treat
anything that isn't in the repo as not-yet-communicated.

**Branch naming** — Use `codex/<short-slug>` for every branch. Claude
uses `claude/<short-slug>`. Keep branches small; one logical change
per PR.

**Hand-off pattern (current)** — Codex drafts changes in its cloud
environment; the user reviews and either merges your branch or pastes
your diff into Claude for continuation. Treat each environment session
as a draft handed to the human, not an autonomous commit.

## 3. Code hygiene

- `python -m compileall -q <path>` and `pytest -q <path>` before each
  hand-off.
- `.gitignore` catches `.pyc`, `__pycache__/`, `.env`, PDFs. Do not
  bypass it.
- Match the existing module style under `api/app/` — plain FastAPI,
  pydantic models, no extra framework layering unless the task
  specifically needs it.
- When adding dependencies, pin to a specific version in the matching
  `requirements.txt`.

## 4. Claim discipline

Before writing a mathematical statement into a doc, decide its tier
from RESEARCH.md §3 (Proposed mechanism / Mathematical result / Exact
computation / Numerical evidence / Clinical evidence / Contradicted or
unresolved).

Negative numerical results are first-class. Pre-register the hypothesis
in the relevant `CLAIMS.md` before running. Do not re-tune a test to
make a null result go away. If a prior claim turns out to be wrong,
move it under `# Retired` with the superseding commit SHA — do not
delete it.

## 5. Writing voice

The sibling project [sgrounds](https://github.com/rafaellemus92/sgrounds)
treats a Norse mythological layer (Norns weaving the tapestry, wyrd as
the pattern across threads, Loki as the revealing twist, the semicolon
`;` as the shuttle of the loom) as load-bearing conceptual
infrastructure. We preserve that voice in prose where it fits. We
*never* let it leak into theorem statements, dosing tables, or
clinical guidance.

## 6. Clinical caveat (always)

Nothing here is validated for patient care. Scenario models are
research instruments. Say so explicitly in any UI copy, docstring, or
README that a clinician might read.

## 7. Working with the existing stack

- The FastAPI service entrypoint is `api/app/main:app`. Local run:
  `uvicorn app.main:app --app-dir api/app --reload`.
- The Streamlit UI is `ui/app.py`. Local run: `streamlit run ui/app.py`.
- Docker: `docker compose up --build` after `cp .env.example .env` and
  filling in `OPENAI_API_KEY`.
- Postgres uses pgvector. Schema is applied on API startup from
  `api/app/schema.sql` via the lifespan handler.

## 8. Related in-tree work to be aware of

- `hou-luo/` — adaptive-mesh 1D Hou-Luo singularity tracking
  (PR #1). Inviscid blow-up candidate study. Companion to the viscous
  phase-organization work in `fluids/`.
- `pangram/` — unrelated prime-word research. Leave alone unless asked.
- Open `claude/` branches at the time of this file's creation each
  likely touch root-level files from before the restructure in PR #3
  and will need rebase.
