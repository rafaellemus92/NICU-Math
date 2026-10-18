# Startup and collaboration handoff — 2026-10-18

- Implementation owner: Codex. Independent reviewer: Claude Code, pending; not contacted.
- Branch: `codex/startup-collaboration` (local only).
- Base: `4babdcdf50d6d5aed780319daeebb0deb65075ea` on original branch `work`.
- Review target: the commit containing this handoff, identified by its exact hash in
  the delivery message. Resolve with `git log -1 --format=%H codex/startup-collaboration`.
- Initial checkout was clean. `/workspace/.agents` was empty; no repository
  `.agents/skills`, AGENTS.md or CLAUDE.md was present. Existing pangram work,
  tracked bytecode and `nano hybrid.patch` were preserved unchanged.

## Verified baseline
Environment startup eventually returned `ready`; no setup failure was reported.
Python 3.12.14 and Docker server 28.4.0 were available.

| Command/check before edits | Outcome |
| --- | --- |
| `docker compose config --quiet` | Failed: required `.env` absent; `.env.example` also absent. |
| `python -m pip install --dry-run --no-index -r api/requirements.txt` | Failed: path absent. |
| Same command for `ui/requirements.txt` | Failed: path absent. |
| `env -u OPENAI_API_KEY -u NICU_OPENAI_KEY python -m uvicorn app.main:app --app-dir api/app` | Failed: resolves root Streamlit `app.py`, then missing `requests`. Expected API package paths absent. |
| `python -m streamlit run ui/app.py` | Failed: Streamlit absent; documented UI path also absent. |
| `python -m unittest discover -v` | Zero tests discovered. This is not passing test coverage. |
| Static inspection | Compose build contexts `api`/`ui` and Dockerfile `COPY app` absent; root API had package-relative imports. Root requirements had malformed `pdfmine8733` and `r.six`, lacked direct UI/PDF imports, and included unused heavyweight sentence-transformers. Search created an OpenAI client during import. |

No database was started and no PDF was ingested during baseline reproduction.

## Changes and rationale
- Keep the flat layout and correct import/startup paths; default offline FastAPI
  lifespan skips DB/client imports. `/healthz` explicitly reports its mode.
- Offline `/search` and `/answer` return 503; scenarios remain available. Removed
  static PDF serving and wildcard CORS from this local-only startup. Streamlit
  calls the API server-side, so cross-origin browser access is unnecessary.
- Split minimal offline/test requirements from optional evidence/PDF dependencies;
  repair malformed package names, add directly imported packages, remove unused
  sentence-transformers. Optional dependency install/integration remains untested.
- Align Dockerfile/Compose with root files; no `.env` dependency, loopback host
  ports, optional database profile, no library mounts or secret forwarding.
- Add synthetic-only UI/model labeling and remove the duplicate error handler
  that read an undefined/stale response after failed requests. Legacy LLM prompts
  no longer request doses or bedside action plans. No model coefficients changed.
- Correct legacy helper imports and guard clients with offline mode; this does not
  certify their database/schema compatibility or external behavior.
- Add shared instructions, Claude import, research index and repository/build
  ignores. No patient-data upload interface was added.

## Validation after changes
Passed:
- Fresh `.venv`: `python -m venv .venv` and
  `.venv/bin/python -m pip install -r requirements-test.txt`.
- `NICU_OFFLINE=1 .venv/bin/python -m unittest discover -s tests -v`: **5 tests**.
  Covers default mode with a dummy credential, no external client imports, API
  lifespan/health, disabled evidence, no `/files` route, all three seeded scenarios,
  histogram conservation, bounded/ordered summaries, request sample limits, UI
  initial render and failed scenario handling. Tests block outbound socket connects.
- `.venv/bin/python -m pip check`: no broken requirements.
- Live Uvicorn at `127.0.0.1:18000`: `/healthz` HTTP 200, mode offline; synthetic
  `/scenario/extubation` HTTP 200 with histogram count 100. Live Streamlit at
  `127.0.0.1:18501/_stcore/health`: HTTP 200. Both temporary processes stopped.
  Subprocesses had both key variables and NICU_OFFLINE unset, exercising the default.
- `docker compose config --quiet` and root Python AST parse.
- `git diff --check`.

Failed/blocked:
- Initial Docker build could not write `/home/agent/.docker/buildx` (read-only).
  Retried with an empty writable `DOCKER_CONFIG=/tmp/nicu-docker-config`.
- `DOCKER_CONFIG=/tmp/nicu-docker-config docker compose -p nicu-smoke-20261018 build`
  pulled the Python base image but failed in pip: `Temporary failure in name
  resolution`, followed by no matching distribution. Container build DNS is the
  remaining blocker; local venv installation of the same pins succeeded. No
  automatic approval rejection occurred and no host network configuration changed.

Not run:
- Compose services/end-to-end containers, because build failed; Python 3.11 runtime
  checks (Docker target); optional evidence dependency installation; Postgres/schema,
  ingestion, real retrieval or OpenAI integration; full multi-hour pangram suite;
  clinical validation and independent Claude review. These are not implied by smoke success.

## Credential diagnosis
At the base commit, `git grep -l NICU_OPENAI_KEY 4babdcd -- ':!*.pyc'` found no
tracked text reference. Application code uses `OPENAI_API_KEY` for optional paid
embeddings/answers. Codex did not request, generate, configure, inspect or display
credential values in this task, and made no paid API calls. Checkout and offline
checks succeeded without either key. There is no accessible environment setup
configuration/log identifying who requested the custom `NICU_OPENAI_KEY` name;
its exact external source and storage remain unverified. Do not infer an app-key
requirement for GitHub cloning or synthetic tests. If diagnosing that prompt,
request only its non-secret label/location or setup command, never the value.

## Next review and decision
Claude should review the exact base-to-target diff, rerun smoke checks, and report
findings with paths/lines. Pay attention to offline isolation, dependency scope,
legacy behavior changes and clinical claim boundaries. No second implementation
owner should edit this task concurrently. A human decides subsequent integration.

The branch is not pushed. To review from another checkout, the user must decide
whether to authorize publishing this branch to the existing private repository or
transfer the commit locally. Neither visibility changes nor additional access are
required by this handoff. Do not automatically push, merge or deploy.
