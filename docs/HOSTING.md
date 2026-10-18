# Hosting assessment — automatic preview observed

## What failed on current main

Main `7ddd793ff940d0a32f1cdc43d5992fb9fc15fe3c` still contains the invalid
requirements `pdfmine8733` and `r.six`, matching the reported Vercel resolver
failure. This review branch replaces them with compatible verified PDF package
pins and resolves dependencies locally. That fixes this dependency input; it
is not evidence that a Vercel deployment builds or runs successfully.

The user also supplied a preview-build diagnosis for branch commit `a93da83`:
`PYTHON_REQUIREMENTS_PARSE_ERROR` at the root `-r requirements-offline.txt` include.
The included file existed; the parser reason was not established. This branch now
uses a flat root manifest, with a regression check against the service manifests.
Automatic deployment status for `53353b7` subsequently succeeded. No manual
deployment was run. The user confirmed hosted `/healthz` reports offline/ok.
The supplied report is distinct from the main-branch invalid-package failure.

## FastAPI and Streamlit are separate services

- API: `api.app.main:app`; root `main.py` re-exports the same app for compatibility.
  Default offline startup needs only `api/requirements-offline.txt` and makes no
  paid API or DB calls. Vercel documents FastAPI discovery from root `main.py` or
  `app/main.py`. Actual project root, framework detection, bundle size, runtime
  limits and installed dependencies still need an authorized hosting review.
  [Vercel FastAPI documentation](https://vercel.com/docs/frameworks/backend/fastapi).
- UI: `streamlit run ui/app.py` starts its own server with browser sessions and
  persistent WebSocket communication. A FastAPI function export does not start
  that service or serve its UI. No Streamlit adapter/routing for Vercel is included.
  [Streamlit architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture).
- Current Vercel documentation describes WebSocket support in public beta, with
  duration limits and reconnect/shared-state considerations. Therefore this is
  **not** a blanket claim that Vercel cannot support WebSockets. It also does not
  establish compatibility of the pinned Streamlit server or its session lifecycle.
  [Vercel WebSocket guidance](https://vercel.com/kb/guide/do-vercel-serverless-functions-support-websocket-connections).

The combined root `requirements.txt` is for local development and includes UI and
optional PDF/DB packages. It is not a minimal function deployment manifest. An
API-only hosting configuration should be assessed separately rather than assuming
this entire repository, math artifacts and UI should be bundled into a function.

## Current decision boundary

Local Uvicorn/Streamlit and Compose are the supported development paths documented
here. No Vercel credentials, project settings, build commands, environment values,
rewrites or deployment hooks were inspected or changed. No `vercel deploy`, hosted
production deployment was requested. Authorized branch pushes triggered the existing
automatic preview integration; those results were observed without changing settings.
Keep document serving disabled.
Do not treat a successful local dependency resolution or API health response as
proof of Streamlit hosting, production security or clinical validity.

## Homepage follow-up

The API now serves a simple HTML introduction at `/`, with `/docs` and `/healthz`
links and synthetic-research limitations. It is not the Streamlit application.
Local desktop/mobile rendering and API/UI health checks passed; see HANDOFF.md.
Direct preview requests from this environment are blocked by the network proxy
(403), so local render checks do not claim hosted browser verification.
