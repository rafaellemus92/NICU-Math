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
Automatic deployment status for `53353b7` subsequently succeeded, under the
Vercel project configuration in effect at that time (root directory at the
repository root, FastAPI detected from `main.py`). No manual deployment was run.
The user confirmed hosted `/healthz` reports offline/ok under that configuration.
The supplied report is distinct from the main-branch invalid-package failure.
See "Hosting on main has moved to `web/`" below for what changed afterwards.

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

The homepage document itself has no script, form, iframe or external asset.
The linked `/docs` page is FastAPI's default Swagger UI, which loads
`swagger-ui-bundle.js` and `swagger-ui.css` from `cdn.jsdelivr.net` and its
favicon from `fastapi.tiangolo.com`; that is unchanged, pre-existing FastAPI
behaviour, so "no external requests" is a statement about `/` only.

## Hosting on main has moved to `web/`

After this branch's base was taken, main changed what the Vercel project builds:

- `4ec82bb` (PR #8) added a Next.js application under `web/` with its own
  homepage (`web/app/page.tsx`).
- `d9b01c4`, an empty commit titled "Trigger Vercel redeploy with root directory
  set to web/", records that the project's root directory was switched to `web/`.
- `efff6a5` (PR #11) added `web/vercel.json` with `"framework": "nextjs"`.

Consequences for this branch:

- The FastAPI homepage at `/` on this branch is not what the Vercel project
  serves from main; main's `/` is the Next.js page.
- The automatic preview success recorded for `b606b03` (deployment status at
  08:01:45Z on 18 October) predates the root-directory change (`d9b01c4`,
  08:02:55Z). This branch has no `web/` directory, so a preview build under the
  new setting is not expected to succeed. This was not verified: no Vercel
  settings were inspected or changed from here.
- The earlier statements in this file about FastAPI discovery from root
  `main.py` describe the previous configuration, not the current one.

Which `/` the repository should serve, and from where, is an integration
decision for the maintainer, not something this branch settles.
