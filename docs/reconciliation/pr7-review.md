# Startup and collaboration handoff — 2026-10-18


## Documentation corrections after independent review (current)

Owner of this change: Claude Code, at the user's request ("fix the homepage
claims"), on top of Codex's `b606b03`. Scope: `docs/HOSTING.md` and this file
only; no application code, tests or dependencies changed.

An independent review of `b606b03` was performed on 18 October from a detached
worktree: the offline unittest discovery gave **9 passed, 2 optional PDF tests
skipped**, and **11 passed, zero skipped** with the optional dependencies
installed; `compileall` and `git diff --check` were clean; live loopback API
(`/`, `/docs`, `/healthz`) and Streamlit health returned 200; the Chromium
checks (1440x1000 and 390x844: no overflow, one h1, skip link first in tab order,
zero scripts, zero external requests from the homepage document) were reproduced.
The findings were four Low items, none blocking. Two were documentation claims,
corrected here:

- "No external page requests" holds for the homepage document only; the linked
  `/docs` page is FastAPI's Swagger UI and loads its assets from
  `cdn.jsdelivr.net` (pre-existing, unchanged).
- The hosting notes described the Vercel project as building this FastAPI app.
  Since `d9b01c4` on main the project's root directory is `web/`, a Next.js
  application this branch does not contain; the preview success recorded for
  `b606b03` predates that change. HOSTING.md now says so.

The other two (the evidence-mode homepage text has no test; the homepage links
are root-absolute) are left as noted. The merge conflict with main is a single
add/add in `.gitignore`; the hosting and guidance differences are recorded in
HOSTING.md for the maintainer. Validation of this docs-only commit: the same
offline discovery command, `compileall` and `git diff --check`, rerun after the
edits.
