# Current integration hosting scope — 2026-10-18

The web application and Python services are separate deployment targets.
Current main `efff6a5b43d699c22eb6bef8c0ce666837d3d785` supplies `web/`
(Next.js, including Shared Air) and `web/vercel.json` with framework `nextjs`.
Both are preserved by this integration. The user-supplied settings screenshot
showed FastAPI with Root Directory `web` and overrides off: those settings do
not describe the web application's framework.

Proposed web settings: Framework Preset **Next.js**, Root Directory **web**,
Build/Install/Output overrides **off**. The existing build script is
`npm run build` (`next build`); routes begin at `web/app/page.tsx` and
`web/app/layout.tsx`. No project setting or deployment was manually changed.
The existing committed framework override may supersede the dashboard preset;
observe the exact integration commit's automatic checks before attributing a failure.

PR #7's earlier successful preview served its FastAPI root compatibility entrypoint;
that result is historical and does not establish Next.js deployment success.
PR #13's old base lacked `web/`; this integration brings it from current main.
Python dependency repairs from PR #7 are retained separately. Do not deploy the
Streamlit server by assuming FastAPI or Next.js automatically hosts it.

The following is historical evidence from the startup branch, not validation of
this integration commit. Current checks are recorded in HANDOFF.md.

## Historical hosting assessment — automatic preview observed

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
Automatic deployment status for `53353b7` succeeded under the earlier root
FastAPI configuration, before the switch to `web/`. The user confirmed
`/healthz` was offline/ok there. Neither observation validates the current
Next.js target; no manual deployment was run.
The supplied report is distinct from the main-branch invalid-package failure.

## FastAPI and Streamlit are separate services

- API: `api.app.main:app`; root `main.py` re-exports the same app for compatibility.
  Default offline startup needs only `api/requirements-offline.txt` and makes no
  paid API or DB calls. The earlier FastAPI deployment used root `main.py`;
  that historical discovery path does not host the API from the current
  `web/` Next.js target. Any separate API deployment needs its own review.
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

## Historical decision boundary (before PR19 publication)

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

## PR7 follow-up retained

The no-external-request observation applies only to the FastAPI homepage
document. Its linked `/docs` Swagger UI loads assets from cdn.jsdelivr.net and
a favicon from fastapi.tiangolo.com. Historical API preview success predates
the change to the `web/` Next.js root; it does not validate this site's hosting.
See [the original review record](reconciliation/pr7-review.md).

## PR19 publication and correction boundary

The user subsequently authorized PR19 publication and automatic preview checks.
At e55d74e both hosted Lean workflows and Vercel preview/review checks passed;
this is not production deployment or independent hosted-browser verification.
The current follow-up corrects reviewed content; main merge, production
deployment and retirement of source PRs remain unauthorized.
