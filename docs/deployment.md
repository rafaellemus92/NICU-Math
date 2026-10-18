# Deployment plan

The hosting commitments both AI collaborators design to. Keeps the
mathematical fundamentals unconstrained while moving the research
toward something a clinician or mathematician can actually open and
use.

> Status: **plan only.** Nothing is provisioned, nothing is paid for.
> Each row below becomes action when its "trigger" lands.

---

## Summary

| Layer | Where | Trigger | Monthly cost (rough) |
|---|---|---|---|
| Repo | GitHub, private | now | $0 |
| Vercel auto-deploy | **paused** (ignored build step `exit 0`) | until the baseline is green | $0 |
| Static docs site | Vercel, built from Markdown | after baseline merges | $0 (hobby tier) |
| Next.js UI shell (`/nicu`) | Vercel | after the first UI iteration | $0 → $20 (Pro, if needed) |
| FastAPI backend | **Railway** | when the UI needs it web-reachable | $5–10 |
| Postgres + pgvector | Railway managed add-on | with the backend | included or ~$5 |
| Auth | reuse sgrounds' Supabase, JWT-validated by FastAPI | when NICU-Math needs sign-in | $0 (shared project) |

## Vercel

**Now:** auto-deploy is paused. In the Vercel project
(`rafaellemus92s-projects/nicu-math`): Settings → Git → **Ignored
Build Step** set to `exit 0`. Every push is a no-op; no red checks,
no build minutes consumed. Reversible by clearing the field.

**Soon (after PR #3 merges):** a static docs site. One `vercel.json`
+ a static-site generator (MkDocs is the simplest; Docusaurus or
mdBook also fine) building a browsable surface from the Markdown
already in the repo:

- `RESEARCH.md`, `AGENTS.md`, `CLAUDE.md` (the spine)
- `fluids/CLAIMS.md`, `physiology/CLAIMS.md` (the ledgers)
- `fluids/exact/README.md`, `fluids/exact/phi_family.py` output
- `physiology/references/` (per-paper notes)
- Each PR's description, rendered

Every PR then gets a Vercel preview URL that both AIs (and any human
reviewer) can link to without cloning the repo. Low effort, high
coordination value.

**Later:** a Next.js UI shell at the repo root, consuming the
FastAPI backend. Same visual language as sgrounds `/piano` so a case
and a piano session look like siblings. Starts with one tab (Evidence
browser) and grows one tab per iteration. Streamlit stays live for
anything the Next.js shell hasn't reached yet.

## FastAPI backend: Railway (recommendation)

Chosen specifically so hosting ergonomics don't force mathematical
compromises.

- **Why Railway over Vercel serverless Python:** persistent processes.
  `ensure_schema()` runs once per container, not per request. Warm
  connections to Postgres. No per-invocation cold start on a
  simulation request. Container is just your `api/Dockerfile`
  unmodified.
- **Why Railway over Fly.io:** less infra knowledge required, friendlier
  dashboard, Postgres+pgvector add-on is one click. Fly is a good fit
  if we outgrow Railway's limits; the FastAPI code moves without
  change.
- **Why not Supabase Edge Functions:** Deno runtime. numpy/scipy work
  doesn't belong there.
- **Why not a VPS:** more control, more sysadmin work. Keep in reserve.

### Postgres + pgvector

Railway's Postgres add-on supports pgvector. Current schema in
`api/app/schema.sql` applies at startup via the lifespan hook,
unchanged. Backups: Railway handles managed snapshots at the
infrastructure level.

If we later want unified auth with sgrounds (one Supabase account
spans both projects), the pattern is: Supabase hosts auth and
whatever cross-project tables make sense; Railway hosts
NICU-Math-specific tables (chunks, documents, scenario_runs); FastAPI
on Railway validates Supabase JWTs on each request against the
project's JWKS. No data migration needed; `pg_dump` from Supabase
and `pg_restore` to Railway is a backup path if that ever reverses.

## Auth path (when it matters)

Three-stage escalation:

1. **No auth** — current state. Private repo, local dev only.
2. **IP-restricted preview URLs** on Vercel for the docs site when it
   contains anything not meant for the open internet (per-paper
   references with content excerpts).
3. **Supabase JWT** validated by FastAPI, same account as sgrounds.
   Users sign in once; both projects recognize them. When this
   lands, document it in `AGENTS.md` and `CLAUDE.md` so neither AI
   writes code that bypasses it.

## Clinical caveat (always)

Nothing hosted anywhere here is validated for patient care. Any
deployment page that a clinician could reach must say so at the top,
plainly. See `physiology/README.md`.

## Decision table

Future me, Codex, or any human reviewer, when you're about to add
hosting infrastructure: this doc is the first thing you check.

| Decision | Source |
|---|---|
| Backend hosting | Railway (this doc, §FastAPI backend) |
| Static docs | Vercel (this doc, §Vercel) |
| UI framework | Next.js when ready (this doc, §Vercel) |
| Auth | Supabase JWT (this doc, §Auth path) |
| Database | Postgres + pgvector on Railway (this doc, §Postgres + pgvector) |
| Deployment of simulations | Local Docker today; Railway container with budget override later if runs grow (`fluids/CLAIMS.md` constraints) |

If a decision above needs revisiting, open a PR against this file
and name what changed in the commit message. The spine in
`RESEARCH.md` is deliberately silent on hosting so the two can
evolve independently; this file is where hosting choices live.
