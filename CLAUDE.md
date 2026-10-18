# CLAUDE.md — NICU-Math

Instructions for Claude (Claude Code / Claude via GitHub integration)
working in this repository.

> **Start by reading `RESEARCH.md` in this same directory.** It carries
> the research thesis, track structure, claim ledger, and voice.
> Everything below is operational advice specific to Claude's tools.

---

## 1. The repo's spine lives in three files

- **`RESEARCH.md`** — thesis, methodology, claim ledger. Both AI
  collaborators read it.
- **`AGENTS.md`** — Codex-specific operational advice.
- **`CLAUDE.md`** — this file.

Never contradict RESEARCH.md from here. If you need to update the
spine, change RESEARCH.md explicitly and reference the change in your
commit message.

## 2. The two-AI workflow

Codex also commits to this repo (currently via its cloud environment →
drafts handed back for the user to merge). You and Codex coordinate
only through:

1. The repository itself (branches, PRs, PR comments).
2. The claim ledgers (`<track>/CLAIMS.md`).
3. This spine.

You will not see Codex's chat history and should not assume it. Treat
anything that isn't in the repo as not-yet-communicated.

**Branch naming** — Use `claude/<short-slug>` for every branch. Codex
uses `codex/<short-slug>`. Keep branches small; one logical change per
PR; prefer multiple small PRs over one big one.

**PRs are reviews, not merges** — You open PRs; the user merges. Never
self-merge, never force-push to `main`, never close an open PR you
didn't open. If you need to revise a PR, push additional commits to
the same branch.

## 3. Code hygiene

- `python -m compileall -q <path>` before every commit for syntax check.
- `pytest -q <path>` for anything with tests.
- Keep per-file imports minimal; prefer function-local imports when a
  heavy dependency (sentence-transformers, PyMuPDF) is only used in
  one entry point.
- Never commit `.pyc`, `__pycache__/`, `.env`, PDFs, or large binary
  artifacts. `.gitignore` covers these; verify.
- Follow the existing module style — the `api/app/` files use plain
  FastAPI patterns, pydantic models, no heavy framework layering.
  Match that.

## 4. Claim discipline

Before writing a mathematical statement into a doc, decide its tier
from RESEARCH.md §3:

- *Proposed mechanism*: file in `<track>/CLAIMS.md` under **Proposed**;
  one paragraph; name what would make it testable.
- *Exact computation*: write a deterministic script under
  `<track>/exact/`, a pytest under `tests/`, record the result in
  `CLAIMS.md` with the script path and the commit SHA.
- *Numerical evidence*: pre-register the hypothesis in `CLAIMS.md`
  **before** running. Save seeds. Save held-out outputs. Do not re-tune
  the test until the result improves.
- *Clinical evidence*: cite the primary source (DOI, year, n). Keep a
  per-paper note in `physiology/references/`.

**If you cannot name the tier, you are not ready to file the result.**

## 5. Writing voice

Match the sgrounds CLAUDE.md convention when writing prose: the Norse
mythological layer (Norns, wyrd, Loki, Yggdrasil, the semicolon `;` as
the shuttle of the loom) is load-bearing and should be preserved in
voice. But equations and physiology stay strict; no mythological terms
inside a theorem statement or a dosing table.

## 6. Clinical caveat (always)

Nothing here is validated for patient care. Scenario models are
research instruments. Say so explicitly in any UI copy, docstring, or
README that a clinician might read.

## 7. GitHub operations

- Prefer the GitHub integration tools over the `gh` CLI.
- Searches that take `repo:owner/repo` should be scoped to
  `repo:rafaellemus92/NICU-Math` unless the task explicitly spans
  multiple repos.
- `pangram/` is unrelated prime-word research merged via PR #2.
  Leave it alone unless asked.

## 8. Session attribution

Commits authored from this session end with:

```
Co-Authored-By: Claude <noreply@anthropic.com>
```

(The specific model is set per-session; follow whatever your current
session's attribution reminder says.)

PR descriptions end with the Claude Code attribution block the current
session mandates.
