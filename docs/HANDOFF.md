# Startup and collaboration handoff — 2026-10-18

## Finite-time enstrophy error bound (current, Claude)

Owner: Claude Code (session "Navier Stokes-Speech"). Branch
`claude/enstrophy-finite-time-bound`, based on main `2b14eeaa3d6a432e357f9ae0b9b2c936a725f6aa`.
User authorized one bounded mathematical task after PR #19: an explicit, certified
finite-time bound on the enstrophy error of the phase family after subtracting its
quadratic response in b, with one targeted reviewer and no paid runs, long DNS, website
edits, merges or overwriting of archived outputs. Scope: the new folder
`math/all-time-phase-response/finite-time/` (note, two scripts, logs), one index row in
`math/README.md` and `docs/RESEARCH_INDEX.md`, and this section. Nothing else is changed.

Result (paper argument with every constant explicit, evaluated in validated interval
arithmetic with directed rounding): a certified admissible radius β₁(T) at the H¹ level and
|Z(u_b) − Z(U) − b²Z2| ≤ C_Z(T) b⁴ on [0, T] for |b| < β₁(T), strict. At a = c = d = 1,
ν = 1/28 exactly: β₁ = 1.08×10⁻³ (T = 0.25), 2.11×10⁻⁴ (T = 0.5), 6.33×10⁻⁶ (T = 1), rounded
down, against the all-time ceiling 7.2×10⁻²²; C_Z = 2.64×10¹², 5.14×10¹⁹, 6.02×10³⁸, rounded
up, which is 10¹⁶–10⁴⁰ above the measured remainder. The obstructing estimate
(Agmon/dissipation source bounds, not the propagator) and one improvement are documented in
the note, together with the estimate any improvement of the radius still needs: a certified
H¹ bound on the nonlinear remainder v − bq₁, without which validated norms of q₁ give no
radius. Labels: mathematical proof with symbolic→evaluated constants (not formalized);
numerical evidence only for the consistency checks.

Validation: `constants.py` (about 90 s; interval arithmetic with directed rounding, complete
rounding budget printed as the maximal enclosure width 3×10⁻³¹, parameter range ν > 0, T > 0,
|c| + |d| ≥ ν enforced), `check_bounds.py` (N = 24, dt = 0.005, T = 1, b = 10⁻³, 10⁻², 0.05;
the solves were run once, about 15 s, and the third commit re-rendered its tables from the
saved measurements without re-running any solve; every bound is consistent with, i.e.
exceeds, its measurement; the six-term Section 5 identity holds to 6×10⁻¹⁶; b = 10⁻² and
0.05 lie outside every certified radius and b = 10⁻³ inside it at T = 0.25 (hence for every
T ≤ 0.25) but not at T = 0.5, 1, so this is
a check of the b → 0 limits, not of a certified case, and the saved samples every 0.05
certify nothing in between), certified lattice sum for the Agmon constant (`lattice_sums.py`,
about 6 s). Not run: Lean, any DNS beyond N = 24 and T = 1, the all-time package's own pilots
(unchanged). Independent review: one targeted reviewer re-derived every step and confirmed
the theorem with the constants as evaluated; its eight minor/nit findings are applied in the
branch's second commit (folder README). A read-only audit of the second commit (bfbe2b0)
asked for directed rounding, a validated error budget or a weaker label, the removal of the
claim that validated q₁ norms alone give a larger radius, a narrower description of Table C,
and the b = 10⁻³ status at T = 0.5, 1; the third commit applies all of it. One targeted reviewer verified
that commit independently (random tests of the interval arithmetic against exact rationals,
the exponential and square-root bounds against 80-digit references, the trap against bare
decimal operations, the range enforcement, agreement of the interval chain with the audited
float chain to 10⁻⁹, the re-render without solves, and every number of the note against the
logs); verdict: all five audit items met, nothing blocking. Its two cosmetic findings (two
printed cross-check values rounded to nearest instead of up) and eight nits are applied in
the fourth commit.

## PR19 independent-review corrections (historical, Codex)

Owner: Codex. Base e55d74e336270f5a5c3ae52c45a78c6523ef9347.
See [correction dispositions and fresh verification](reconciliation/CORRECTIONS.md).
Authorized: bounded correction/push, existing PR19 updates, automatic preview/CI
and source archival tag. No main merge, production deployment or source PR retirement.

## Consolidated local review (historical e55d74e)

Owner: Codex; base efff6a5b43d699c22eb6bef8c0ce666837d3d785; isolated branch
`codex/reconcile-research-review`. The [review record](reconciliation/REVIEW.md)
is authoritative for current scope, source decisions and fresh tests. All
sections below describe their historical source commits. Independent AI
review is required before human integration; no external action is authorized.



## API homepage claim wording and asset guard (historical source context, Claude)

Owner: Claude Code. Branch `claude/new-session-sbrl43`, based on PR #17 head
`43160952f2c851e2c9e340a66b48651a6a285046`. User authorized fixing the homepage
claims; the branch is published to `origin/claude/new-session-sbrl43` for review,
following the session's branch instructions. No merge, settings change or
deployment. The Next.js homepage (`web/app/page.tsx`) was corrected by Codex in
PR #16 (`745e846`); PR #17 changed no `web/` files, and this branch does not
change `web/`. Scope: the FastAPI homepage `api/app/homepage.py` and its test.

- `/docs` is Swagger UI whose HTML references three external assets on two hosts
  (script and stylesheet from cdn.jsdelivr.net, icon from fastapi.tiangolo.com),
  and `/redoc` loads from cdn.jsdelivr.net and fonts.googleapis.com; the homepage
  now says so instead of implying an offline documentation page. `/openapi.json`
  is served locally.
- The intro no longer reads as if a respiratory/hemodynamic model were delivered;
  the limits list points to the closed-form two-compartment teaching model in
  `physiology/`, which this API does not serve.
- `tests/test_smoke.py`: the external-asset guard now checks every attribute value
  on every tag (no `//` prefix, no URL scheme), forbids asset/embedding tags,
  `meta http-equiv`, event-handler and `ping`/`background`/`xlink:href`/`style`
  attributes, and scans the lower-cased page for `//`, `@import`, `url(`,
  `image-set(`, `src(`, `image(`, `http-equiv` and any URL scheme. The first
  version of this guard (`316117a`) was case-sensitive and attribute-name based;
  an adversarial probe set showed it passing `URL(`, `@IMPORT`, `image-set(`,
  `meta refresh`, `ping`, `onload` and `xlink:href` injections. A new test renders
  the evidence-mode copy without the client.

Validation (offline-only venv, Python 3.12.3, NumPy 2.0.2, credentials unset):
- `NICU_OFFLINE=1 .venv/bin/python -m unittest tests.test_smoke tests.test_requirements tests.test_optional_pdf -v`:
  **12 tests, 10 passed, 2 optional PDF tests skipped**.
- `python -m compileall -q api ui tests physiology navier_stokes` and `git diff --check`: passed.
- Mutation probes on a scratch copy (37 injections written by an adversarial
  reviewer: external `link`/`img`/`base`/`form`/`formaction`/`picture`, uppercase
  tags, entity-encoded and slash-less schemes, `javascript:` and `data:` URLs,
  CSS `@import`/`@IMPORT`/escaped `@\69 mport`, `url(`/`URL(`/`image-set(`,
  `@font-face`, inline `style`, `onload` handlers, `meta refresh` and CSP
  `report-uri`, `ping`, `body background`, `xlink:href`, `manifest`, an SVG
  script): **36/37 caught**. The one uncaught probe is a legitimate `<h1 class>`
  edit, which should pass. Four of the caught probes are also legitimate-looking
  edits (a same-origin favicon `link`, an `/openapi.json` link, an HTML comment
  containing a URL, `url(#fragment)`) rejected by design: the test pins the exact
  link set and forbids asset tags, so such edits must update the test.
- Live loopback uvicorn: `/`, `/healthz`, `/docs`, `/openapi.json`, `/redoc` HTTP 200;
  Streamlit `/_stcore/health` ok. Chromium at 1440, 390 and 320 px: no horizontal
  overflow, one h1, skip link is the first Tab stop, **zero external requests on `/`**;
  `/docs` requests two jsdelivr assets, which the page now states. Servers stopped.
- Not run: optional PDF environment, Docker, hosted preview, web build (web
  unchanged), research pytest suites (unchanged).

## Synthetic breath analysis repair (historical source context)

Owner: Codex. Branch `codex/fix-synthetic-breath-analysis`, based on verified
PR #16 head `14fe98a43ca49784540de8fcb03a9f931754975e`. User authorized a
separate stacked draft PR targeting `codex/correct-fluid-claims`, testing,
independent review and push. Repository intentionally public, synthetic code
only. No patient data, schema work, settings, merge or manual deployment.

Failing regressions were committed first in `660945e`: 50 prescribed breaths
produced 48 clean or 468 noisy segments, both assertions failed on the base.
Acceptance criteria were recorded in `navier_stokes/CLAIMS.md` before repair.
Implementation replaces flow-tail crossings with confirmed pressure phases,
adds explicit complete/partial acquisition-edge policy, and uses one consistent
piecewise RC solution for pressure, volume and interval-average flow. Tau no
longer has a hidden floor. The waveform descriptor remains distinct from
prescribed compliance and retains measurable noise bias. DecayFit reports
invalid/unresolved outcomes without manufacturing a finite horizon.

Scope also includes physiology precision/provenance wording and verified Node
minimum/handoff corrections. No convexity theorem, renderer hardening, web
consumer changes, dependency changes, or unrelated research runs.
Validation at the repair implementation:
- `/tmp/nicu-integration-venv/bin/python -m pytest -q -s tests/navier_stokes tests/physiology`:
  **138 passed** (66 new pipeline cases, 31 prior claim corrections,
  41 physiology cases). NumPy 2.0.2 / SciPy 1.18.1; ODE errors unchanged at
  7.981e−11 and 2.604e−11. No periodic-flow/Lean or unrelated research suite run.
- `NICU_OFFLINE=1 /tmp/nicu-integration-venv/bin/python -m unittest
  tests.test_smoke tests.test_requirements tests.test_optional_pdf -v`:
  **11 tests, OK**, 1.266s. Expected Streamlit bare-mode warning only.
- compileall for navier_stokes/physiology/api/ui/tests, the noisy CLI demo and
  whitespace checks passed. No web consumer/source changed, so web builds are
  not rerun for this Python/docs-only follow-up.
- Before/after metrics, noise bias and tested detector limits are recorded in
  `navier_stokes/CLAIMS.md`; the 0.8609 default noisy descriptor is not C=1.0.
Independent review of `2943d08312d0d9e8920488240b9147f904933c53` confirmed
RC sampling/fit consistency and found one unknown-leading-edge bug. A regression
reproduced the extra partial cycle at t=0.21 s; unknown edges now require a
confirmed low phase before onset detection. Timing options are keyword-only to
prevent old positional flow thresholds from silently becoming seconds. Two new
regressions failed before these fixes; all 138 cases then passed. Final exact
follow-up review and automatic checks are reported in the draft PR.


## Fluid/respiratory claim correction (completed draft PR #16)

Owner: Codex. Branch: `codex/correct-fluid-claims`, based on exact integration
commit `ab448aaa429bf3bc3c4c5bc2a41b5be6778e1f28`. User authorized a separate
correction-only draft PR targeting `codex/integrate-research-workspace`, plus
commit/push and independent review. No merge, manual deployment or settings change.

Scope: invalid deductions in Python/web proof outlines, synthetic waveform labels
and diagnostic units, analytical sanity checks, focused tests, and correction
ledger. See `navier_stokes/CLAIMS.md` for exact before/after statements and
`navier_stokes/README.md` for derivations and limitations. No assertion about the
current general Navier–Stokes problem status is made. The closed material sphere
and static equilibrium arguments concern the explicitly stated unforced model.

Preserved: periodic-flow/Lean artifacts, two-compartment result, Shared Air code
and placeholder multipliers, dependency manifests and deployment configuration.
No patient schema enablement, migration, access or removal; separate review needed.
Legacy metadata/CSV parsing is not approved for patient-data use. Misleading
Python helper names were replaced; external callers must migrate as documented.

Validation so far:
- `/tmp/nicu-integration-venv/bin/python -m pytest -q tests/navier_stokes`:
  **31 passed in 0.17s**.
- `node --experimental-strip-types --test web/tests/ns.test.mjs`: **4 passed**.
  Node 24 emits a non-failing module-type inference warning; no manifest changes.
- `NICU_OFFLINE=1 /tmp/nicu-integration-venv/bin/python -m unittest
  tests.test_smoke tests.test_requirements tests.test_optional_pdf -v`:
  **11 tests, OK** (1.476s); synthetic/offline, no external services.
- Python compileall for navier_stokes/api/ui/tests and synthetic CLI demo passed.
- Clean npm ci, Next.js 16.4.2 production build and TypeScript noEmit passed.
- Browser checks and exact-commit independent review recorded in the follow-up below.

Browser review (local production server, Chromium): all five routes /, /demo,
/proof, /shared-air and /shared-air/index.html returned HTTP 200. Corrected labels,
recovery checkbox/number, decay slider, proof expand/collapse and 390x844 mobile
layout passed with zero page errors. The first harness assertion mismatched CSS
uppercase text; corrected harness then passed. Independent reviewer found that
negative/fractional recovery indices could throw during render. The follow-up
clamps typed indices to finite integers within bounds; browser cases -1, 1.5,
empty and 10000 passed without errors. Build and tsc passed again after the fix.
The CLI now uses zero noise because the legacy flow-crossing segmenter overcounts
noisy fixtures; this limitation is documented, not presented as clinical validation.

Independent review of implementation `745e846634033478beadda96da27951660d93678`
found the core mathematical corrections sound under stated assumptions and no
changes to protected research/schema/dependency files. Follow-up commit
`14fe98a43ca49784540de8fcb03a9f931754975e` received independent review with
no remaining blockers. Draft PR #16 targets the integration branch; Vercel
deployment, Preview Comments and Agent Review succeeded (zero suggestions).
No GitHub Actions runs were listed. Nothing was merged.

No unrelated research runs, clinical validation, database tests or general PDE
verification were performed. Numerical samples check the implementation of
analytically derived identities, not universal propositions.


## Next.js security migration (completed on PR #14)

Owner: Codex. Base: `8226201409adaf43e432398ad54ef522b5fade8f` on
`codex/integrate-research-workspace` / PR #14. User explicitly authorized a major
Next.js migration with React/types alignment and necessary compatibility fixes,
verification and push. No merge, settings change or manual deployment.

Version decision (2026-10-18): official support policy lists 14.x unsupported,
15.x Maintenance LTS and 16.x Active LTS. December's 14.2.35 patch does not cover
current advisories. October 14 advisories GHSA-2464-fhr4-w9xw (image optimization)
and GHSA-p3m5-59mp-jv5r (Server Actions DoS) list patches in 15.5.28/16.4.1.
Selected verified stable Next.js **16.4.2**; 15.5.28 still bundled an audited
PostCSS version. React/React DOM **19.3.1**, matching types **19.3.0**.
Primary sources: https://nextjs.org/support-policy,
https://github.com/vercel/next.js/security/advisories/GHSA-2464-fhr4-w9xw,
https://github.com/vercel/next.js/security/advisories/GHSA-p3m5-59mp-jv5r,
https://nextjs.org/docs/app/guides/upgrading/version-16.

Only web dependencies/lockfile and Next-generated TypeScript compatibility
changes were needed: react-jsx, ES2017 target, generated route/root-param types
and dev type inclusion. Application source, UI features, web hosting settings,
math/physiology code and research records are unchanged. The full locked tree requires Node >=22 (Supabase 2.118.0);
Next.js alone requires >=20.9;
local verification used Node 24.19.0. No new lint framework installed.

Passed:
- Clean `npm ci --cache /tmp/nicu-integration-npm-cache --no-audit --no-fund`.
- `NEXT_TELEMETRY_DISABLED=1 npm run build` (Next 16.4.2 / Turbopack).
- `npx --no-install tsc --noEmit --incremental false`; dependency tree has no
  invalid peer dependencies. Transitional install warning about old React 18
  disappeared after clean install; final tree uses React 19.3.1 consistently.
- Chromium production-browser smoke: /, /demo, /proof, /shared-air and
  /shared-air/index.html HTTP 200; no page errors. Demo checkbox/number/slider
  interactions passed. Shared Air pause/speed/world controls passed; no experiment
  buttons run. Mobile demo 390x844 had no horizontal overflow. Server stopped.
- Whitespace check; only intended migration/configuration and handoff changes.

Audit remains nonzero: **8 affected packages (5 high, 2 moderate, 1 low)**,
versus baseline 10 (1 critical, 6 high, 2 moderate, 1 low). Next.js and PostCSS
are no longer reported. Remaining full-tree findings: Tailwind CSS, braces,
chokidar, fast-glob, micromatch, postcss-nested, postcss-selector-parser, KaTeX.
`npm audit --omit=dev` reports **1 low (KaTeX)**. Tailwind/KaTeX migrations are
separate scope. Audit counts are dependency advisories, not demonstrated runtime
exploitability or a comprehensive security assessment. Reports are temporary
`/tmp/nicu-next-audit-{before,after,prod}.json`, not committed artifacts.

Existing homepage/demo/proof content still surfaces regularity/blowup and
clinical-transition language; preservation is not scientific or clinical
validation. The subsequent content correction is recorded in PR #16; no patient-data feature was
enabled. Python/research suites were not rerun for web-only dependency changes.
Exact commit, independent review and automatic preview outcome are recorded in
PR #14 and final delivery. Historical implementation/test evidence follows.

## Integration of main, startup PR #7 and physiology PR #13 (historical base)

Implementation owner: Codex. Branch: `codex/integrate-research-workspace`.
User explicitly approved the broader integration, testing, push and a new draft
PR against main. No rewriting/closing source PRs, self-merge, settings changes,
manual deployment, paid API calls or patient data. Exact integration SHA and
automatic check results are recorded in the new PR and final delivery.

Fresh sources:
- main: `efff6a5b43d699c22eb6bef8c0ce666837d3d785`, including PR #11 Shared Air.
- startup PR #7: `b606b03d9295fca8f89932970a37936afdc08cb3`.
- physiology PR #13: `49c5f82889b0535ab7272aaaafa03842cbda574e`.

Started from current main and merged the existing startup branch, resolving the
only Git conflict by combining both `.gitignore` policies. Retained its dependency
repairs, offline default, package layout, synthetic tests and reconciled guidance.
Imported PR #13's five new files byte-for-byte and adapted only its existing
claim entry into the startup ledger: candidate clinical references remain
unverified and all other entries are preserved. Updated current guidance/index
and physiology README to reflect the implemented teaching model. No old PR #5
spine wholesale replacement. PRs #7/#13 remain separate and open.

Preserved main's `web/`, `navier_stokes/`, `math/`, Lean workflow and existing
patch byte-for-byte. This includes the new Shared Air route and existing
`web/vercel.json` Next.js framework override. The screenshot's FastAPI + root
`web` configuration mismatches this web app; recommend Next.js + root `web`,
build/install/output overrides off. No dashboard settings changed. Prior PR #7
FastAPI preview success is not evidence for the current Next.js deployment.

Validation on the integrated tree:
- Fresh `/tmp/nicu-integration-venv`: install existing requirements.txt and
  requirements-test.txt plus pytest/scipy; `pip check`: no broken requirements.
- `NICU_OFFLINE=1 .../python -m unittest tests.test_smoke tests.test_requirements tests.test_optional_pdf -v`:
  **11 tests passed, zero skipped** (including optional in-memory synthetic PDF).
- `.../python -m pytest -q -s tests/physiology`: **41 passed in 0.58s**.
  solve_ivp maximum absolute volume errors: symmetric 7.981e-11,
  heterogeneous 2.604e-11; no unrelated research suite run.
- `python -m compileall -q api ui tests physiology`; `git diff --check`: passed.
- `npm ci --cache /tmp/nicu-integration-npm-cache --no-audit --no-fund`, then
  `NEXT_TELEMETRY_DISABLED=1 npm run build`: production build passed.
  `npx --no-install tsc --noEmit --incremental false`: passed.
  No standalone lint script or ESLint configuration exists; no new lint
  dependencies/configuration added, and no standalone lint pass claimed.
- Local production server: `/`, `/demo`, `/proof`, `/shared-air`, and
  `/shared-air/index.html` all HTTP 200; temporary server stopped.
- Source preservation diff against main for math/navier_stokes/web/Lean/patch:
  empty. No generated cache/build files staged; pre-existing tracked root
  bytecode removed as part of PR #7's cleanup.

Initial npm install failed because its default home cache is unwritable; using a
writable /tmp cache succeeded without changing manifests. npm warned that the
inherited Next.js 14.2.21 has a published security vulnerability. No dependency
upgrade was authorized by this integration; this warning is retained as a limit,
not a whole-stack security review. No changes to web manifests or lockfile.

Independent Codex review of the integration found broad unittest discovery would
import physiology tests without their optional pytest/scipy dependencies. Current
AGENTS.md and README.md now use explicit startup test modules and document the
separate physiology command. Historical commands below are preserved as history.
Exact-commit review is recorded in the PR; no independent Claude review claimed.

Not run: Docker rebuild, hosted browser/runtime checks, Postgres/schema, external
retrieval/ingestion, paid services, unrelated research/Lean suites or clinical
validation. Existing hosting and Docker historical limits below remain historical.

## Homepage follow-up (historical)

Implementation owner: Codex. Base: `53353b71517191a43e031a8687aea17cf759d514`.
Branch: `codex/startup-collaboration`; target is the commit containing this section
(exact SHA recorded in PR #7 and delivery). User authorized a minimal FastAPI
homepage, local checks, commit/push and observation of automatic checks. No manual
deployment, settings changes or merge is authorized.

Before this change `/` returned 404 while `/healthz` and `/docs` worked locally.
The user also confirmed hosted `/healthz` returned offline/ok. Added a responsive,
dependency-free HTML homepage with links to documentation and health, explicit
synthetic-only limitations, and a clear explanation that Streamlit runs separately.
No forms, uploads, credentials, external page assets or services added.

Passed for this change:
- Optional environment unittest discovery: **11 passed**.
- Offline-only `.venv` unittest discovery: **9 passed, 2 optional PDF tests skipped**.
- `python -m compileall -q api ui tests` and `git diff --check`.
- Live local API homepage, documentation and health, and Streamlit health: HTTP 200.
- Chromium/Playwright at 1440x1000 and 390x844: no horizontal overflow, one h1,
  keyboard skip/docs focus, working health navigation, no external page requests.
  Screenshots reviewed at `/tmp/nicu-home-desktop.png` and
  `/tmp/nicu-home-mobile.png` (temporary evidence, not repository artifacts).

No new local test failures. Prior networked Docker build DNS blocker remains;
Docker builds, math suites and optional external services were not rerun for this
HTML-only change. No clinical validation or independent Claude review performed.

At base `53353b7`, automatic Lean build, Vercel Agent Review (zero suggestions),
Vercel Preview Comments and Vercel deployment status all succeeded. Those are
historical results, not checks of this new commit. Current-commit automatic results
will be recorded in PR #7 and delivery after push. Direct preview HTTP access from
this environment is blocked (proxy 403), so hosted rendering is not verified here.

## Reconciliation of PRs #3, #5 and #7 (base 53353b7)

Implementation owner: Codex. User authorized reconciliation/testing/pushing on
`codex/startup-collaboration` and updating draft #7, not merging to main, closing
other PRs or deploying. Independent Codex findings from the earlier review remain
credited below; this reconciliation has not yet received independent review.

### Inspected remote snapshots

- main: `7ddd793ff940d0a32f1cdc43d5992fb9fc15fe3c` (math consolidation).
- PR #3: `b80ba850441bd9c1c1c41d6dd7a3c9aefbd6239f` (`claude/baseline-restructure`).
- PR #5: `2a9b9a87d0916535eab8139a0239b20740a193d1` (`claude/research-spine`).
- Our pre-reconciliation head: `a93da8389ed12b256cbde5fbd421a22b40429abd`.

Merged current main into this review branch, resolving the README overlap by
retaining both startup instructions and the math index. The final merge commit
hash is reported in the delivery/PR. There is no force push or merge into main.

### Integration decisions and remaining differences

| Source | Retained/adapted | Deliberately not adopted |
| --- | --- | --- |
| main | Entire `math/` tree and existing Lean workflow, byte-for-byte. | No rewriting of mathematical claims or research artifacts. |
| PR #3 | `api/app` and `ui` boundaries, relative API imports, separate minimal service Dockerfiles/dependencies, removal of tracked root bytecode and useful ignore rules. | Required keys/DB on startup, PDF serving/library mount, obsolete UI pins, unused heavyweight packages and removal of `nano hybrid.patch`. The patch is preserved. |
| PR #5 | RESEARCH.md, track ledgers/scaffolds, shared-instrument plan, claim tiers, pre-registration, preservation of negative results and cross-AI handoffs. | Assertions that unlanded scripts/libraries already exist or prove results, stale PR/path references, mandatory credentials, and conflicting AI-specific policies. |
| PR #7 | Tested offline default, compatible PDF pins, no dead document links, synthetic-only labels, regression checks and handoff. | Previous flat application layout; root main.py remains only a compatibility re-export. |

AGENTS.md is shared guidance; CLAUDE.md imports it and adds nonconflicting workflow
notes. RESEARCH.md frames convergence as a hypothesis/motivation, not a universal
mathematical or physiological link. Existing source-branch clinical reference
notes are explicitly unverified, not promoted to evidence. Planned exact/model
work remains planned; no patient studies, datasets or uploaded documents added.
PR #6 is separate and not integrated. Other PRs remain open and need their authors
to reconcile any remaining differences; do not merge #3/#5 blindly after #7.

The root requirements manifest is now flat and checked against the per-service
manifests. It removes both main's invalid package names and the `-r` input rejected
in the user-supplied Vercel preview diagnosis. Local convenience manifests still
use pip includes. See HOSTING.md: FastAPI build support does not demonstrate
Streamlit hosting. No Vercel project/configuration/credentials were changed.

### Validation of reconciled tree

Passed:
- Fresh `/tmp/nicu-reconcile-optional` venv: resolution and install of
  `requirements.txt` + `requirements-test.txt`; after flattening, repeated
  `pip install --dry-run --ignore-installed -r requirements.txt`, install and
  `pip check`, all successful.
- `NICU_OFFLINE=1 /tmp/nicu-reconcile-optional/bin/python -m unittest discover -s tests -v`:
  **10 passed, zero skipped**. Includes package/compatibility imports, flat-root
  manifest parity, offline API/scenario/UI checks and optional synthetic PDF tests.
- Offline-only `.venv`: **8 passed, 2 optional PDF tests skipped**.
- `python -m compileall -q api ui tests`, `docker compose config --quiet`,
  `git diff --cached --check origin/main`.
- Live canonical `uvicorn api.app.main:app` and `streamlit run ui/app.py`:
  HTTP 200 for both health endpoints and synthetic scenario; processes stopped.
- `python math/prime-pangram/search/tests/test_solutions.py`: 17 fast checks,
  zero failures. Full research sweeps and proofs are not inferred from this.
- `git diff --exit-code origin/main -- math .github/workflows/lean.yml`:
  unchanged research tree/workflow. The user's existing patch is preserved.
- Python 3.11 container runtime via temporary offline-wheel builds: both health
  endpoints HTTP 200; real UI-to-API AppTest scenario rendered four summary
  metrics without errors; `pip check` passed in each service. Local project
  `nicu-reconcile` containers/network stopped and removed after checks.

Failed/environment limitation:
- A staged whitespace check against the old branch tip reports pre-existing
  whitespace in main's imported math artifacts. The review diff against current
  main passes; those artifacts are deliberately preserved byte-for-byte.
- Standard Compose build and separate `docker build --network=host` attempts
  failed at pip because of container DNS. This remains a standard-build blocker.
- To isolate runtime from DNS, downloaded binary Python 3.11 wheels on the host
  (`pip download --only-binary=:all: --python-version 311 --implementation cp
  --abi cp311 --platform manylinux2014_x86_64 -r requirements-offline.txt`).
  Temporary Dockerfiles under /tmp added a wheelhouse COPY and replaced only the
  pip install with `--no-index --find-links=/wheels`. Built with `--network=none`
  and named build context `wheelhouse=/tmp/nicu-wheels311`; used those images for
  `docker compose -p nicu-reconcile up --no-build`. No wheelhouse or alternate
  build configuration committed; normal networked Docker builds are not claimed
  to pass. Streamlit bare-mode/Altair warnings were nonfatal.

Not run: Vercel build/deployment or production verification, Postgres/schema and
external evidence integration, paid APIs, full numerical sweeps/Lean proof builds
(`lake` not installed), PR #6 tests, clinical validation or whole-stack security
audit. Empty track scaffolds have no runnable research suite and are not counted
as passing tests. The existing Lean workflow is preserved, not manually dispatched.

## Earlier review corrections (historical)


- Implementation owner: Codex. The two findings below were reported by an
  **independent Codex review**, not Claude. Claude has not been contacted.
- Follow-up base: `9d64cc63a1b5c16fdac7d0be81c02bb30b719c67`.
- Branch: `codex/startup-collaboration`. User authorized fixing and pushing both
  findings to the existing private repository; no merge or deployment.
- Target: the commit containing this update; exact SHA supplied in delivery.

### Reproduced findings and fixes

1. P2: `python -m pip install --dry-run -r requirements.txt` failed with
   `ResolutionImpossible`: pdfplumber 0.11.4 requires pdfminer.six 20231228,
   conflicting with our 20240706 pin. Changed only these two dependency pins to
   pdfplumber 0.11.9 / pdfminer.six 20251230.
   The [maintainer advisory](https://github.com/pdfminer/pdfminer.six/security/advisories/GHSA-wf5f-4jwr-ppcp)
   identifies versions before 20251230 as affected by arbitrary code execution.
   This avoids downgrading to the affected 20231228 release.
   [pdfplumber release notes](https://github.com/jsvine/pdfplumber/releases/tag/v0.11.9)
   and PyPI metadata confirm the exact dependency. Version 0.11.10 requires
   Pillow >=12.2.0, incompatible with existing Streamlit 1.39.0 Pillow <11;
   0.11.9 avoids expanding this repair into a UI-stack upgrade. This is a targeted
   compatibility/security decision, not a whole-stack security certification.
2. P3: the new Streamlit regression test failed before the fix because a synthetic
   source path rendered `[Open PDF](http://localhost:8000/files/example.pdf)`
   even though document serving is disabled. Removed link generation and its
   unused URL-quoting import; source titles/excerpts remain. No serving enabled.

### Follow-up validation

Passed:
- Fresh `python -m venv /tmp/nicu-review-optional`; both dry-run resolution and
  installation with `-r requirements.txt -r requirements-test.txt` succeeded.
- `/tmp/nicu-review-optional/bin/python -m pip check`: no broken requirements.
- `NICU_OFFLINE=1 /tmp/nicu-review-optional/bin/python -m unittest discover -s tests -v`:
  **8 passed, zero skipped**. Includes PDF pin/installed metadata compatibility,
  in-memory synthetic PDF extraction, UI source rendering without dead links,
  and all prior API/UI offline checks. No PDF fixture saved or ingested.
- Original offline-only `.venv`: same discovery command, **6 passed, 2 optional
  PDF tests skipped**; pip check passed.
- Live localhost Uvicorn health and synthetic extubation request: HTTP 200;
  Streamlit health: HTTP 200. Both processes stopped. Credentials unset.
- `docker compose config --quiet` and `git diff --check`.

Expected pre-fix failures: dependency resolver conflict and new dead-link UI test,
now fixed. No failures remain in the executed follow-up checks.

Not run: Docker build/startup (prior container DNS failure below remains unresolved),
Python 3.11 checks, Postgres ingestion/retrieval integration, paid APIs, full pangram
reproduction, clinical validation, whole-stack security audit or a second review of
this follow-up. Fresh optional install/PDF tests supersede the earlier optional
installation not-run status, but do not validate the full evidence pipeline.

## Initial implementation record (historical)

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

Historical startup status above is retained for chronology. Subsequent user
authorization permitted publication, and the repository is intentionally public.
Current scoped work remains synthetic-only; no patient data, secrets or
restricted source PDFs may be published. No merge or manual deployment is authorized.


## Selective flow research import (historical PR15 record)

Owner: Codex; branch `codex/import-flow-research`. Fixed base
`ab448aaa429bf3bc3c4c5bc2a41b5be6778e1f28`; target
`codex/integrate-research-workspace`. User authorized selective import,
focused checks, commit/push and a draft PR, with no merge/manual deployment.
Full scope, source SHA, provenance map, validation and deferred-runtime estimate:
[import record](../math/ns-phase-audit/enstrophy-jet/IMPORT.md). No global guidance or app
changes. Exact-commit independent review is pending and will be recorded in the
PR; human integration remains required.

The pending-review wording above is historical; the PR15 independent review
and later integration decisions are recorded in the reconciliation review.


## Route B first stage (Codex, 2026-10-19; local review only)

Owner: Codex. Branch `codex/phase-route-b-dissipation`; exact base
`419e6c3d2e0321816849ca550ad8da5cf34ba75a`. User authorized bounded research and
small interval postprocessing, not publication or integration. Scope: new
`math/all-time-phase-response/finite-time/route-b-dissipation/`, this handoff,
and one research-index row. Completed absorption scripts, inputs, arrays and
archived outputs are unchanged. No additional trajectory download, simulation,
validator rerun, parameter sweep, subagent, paid resource, push, PR or merge.

Preregistered target: |R_Z| < 0.01 at |b|=0.003, T=1/4, with fixed unit a,c,d,
nu=1/28, phi=37/100. The new paper derivation retains W2's nu/8 dissipation,
includes the initial H1 energy in the separate cell formula, and yields
integral ||Delta w||² <= b^4 * 86107. The direct full-r equation r=w-b²q2,
its Fourier-support mean cancellation and an exact three-term observable
identity give |R_Z| <= b^4 * C_B with C_B <= 87807; evaluation of the full
interval product at b=0.003 gives |R_Z| <= 7.1123e-6. Thus the fixed milestone
is met by the derived interval bound. This is not a measured error. Optional
q2 bounds use the validated q1 source; their norms do not enter C_B.

Validation: seven focused tests pass (exact rational W2 coefficients;
nonzero cell initial energy; independent 80-digit linear formulas; Fourier
support/normalization; tamper rejection; output preservation; exact result
reproduction and upward display rounding). See the new folder's results/.
A mistaken initial test-file path caused a test-discovery invocation failure;
it was corrected before running these tests, with the diagnostic retained in
/tmp/route-b-initial-test-invocation.log. No numerical experiment failed or was
retuned. No broad app/physics/Lean suites were run because they are unchanged.

Review required: independently check NOTE.md equations (W), (1)-(8), particularly
the retained dissipation, per-cell initial terms, b/nu powers, the full-r versus
mean-r distinction and mode cancellations. Review every source term and interval
operation against results/bounds.json and pinned inputs. Independent mathematical
review remains pending; no separate agent was launched, per user instruction.
Stop at this first-stage result. Cellwise sharpening and subsequent Route B work
need a new scoped decision; neither is underway.

### Route B review follow-up (local only)

User relayed NS-Speech's conditional AI acceptance of 375e399; actual reviewer
model unverified. See route-b-dissipation/REVIEW.md for attribution, findings and
limits. Corrected the absolute-milestone versus quadratic-dominance distinction,
NumPy import dependency, initial-data distinctions and structural-test labeling.
Added explicit fixed-scope guards and focused mutation tests. Eight tests pass
under Python 3.12. Separate bounds.review.json preserves new source provenance;
all numerical fields and pinned inputs match the original bounds.json exactly.
Original archived results and analytic formulas are unchanged. No push authorized
for this follow-up; no new scientific stage was started.

## Fixed-endpoint Z2 first stage (Codex, local review only)

User authorized pushing exact correction 2af8fe4b3abceee08547f0fee699d78b5ac29bf2
and then a bounded coefficient-certification investigation. That correction push
was completed without force/LFS upload and the remote SHA verified. New branch
`codex/phase-z2-endpoint` starts at that commit; new work is not authorized for push.

Scope: new finite-time/z2-endpoint folder, this handoff/index, and a necessary
prose correction in Route B NOTE/REVIEW. Fixed unit a,c,d, nu=1/28, phi=37/100,
T=1/4, beta=.003. Exact rational sums of the existing verified endpoint arrays,
plus inherited interval errors and the analytic q2 norm bound, yield the
conditional enclosure Z2(T) in [-0.89785,1.4598]. It includes zero. Its available
|Z2| lower bound is 0, versus beta² times the existing C_B upper endpoint in
[.79025,.79026]. Original-target dominance is NOT certified; no smaller-amplitude
success is substituted. This does not establish failure of physical dominance.

Important correction: for the coefficient actually defined in these notes,
Z2(0)=1/4, not zero. q2(0)=0 and ||grad q1(0)||²=1/2. The earlier review wording
was repeated incorrectly in Route B explanatory prose; corrected here and
covered by an exact normalization test. All archived numbers/formulas are intact.

Validation: nine focused implementation tests pass in Python 3.12.14. A first
invocation caught Decimal abs() rounding under the outer Inexact trap; fixed
using exact copy_abs and covered by a regression test, with failure retained.
No new evolution, full validator, sweep, download, paid resource or extra agent.

The blocker is the signed scalar <-Delta U(T),bar(q2(T))>. NOTE.md derives an
adjoint identity and concrete mean-q2 alternative, error budgets, support/tail
requirements and unbenchmarked cost estimates before any larger work. A new
pilot/evolution would require review first. Independent mathematical review
of this new enclosure/plan remains pending. Stop at this first-stage result.


## Forward mean-q2 bounded pilot (Codex, local review only)

Base bc305995c49f3303352e1c1a4e13a50dbf90d965; branch
`codex/phase-mean-q2-pilot`. Scope is only the authorized correctness/runtime
pilot, not a full evolution, full validator or coefficient certificate.
See `math/all-time-phase-response/finite-time/mean-q2-pilot/NOTE.md` for
operator/source conventions, complete-support residual derivation, inherited
error budget, measured resources and gated full-run plan.

Ten focused tests pass on Python 3.12.14 / NumPy 2.0.2. Three actual Q/W
cell pairs with zero/synthetic V probes took 2.3589 seconds including hashes;
all numerical invocations together took under three seconds, within 300 seconds.
An initial missing /usr/bin/time invocation did not execute tests; log preserved.
Residual-only extrapolation is 112–115 minutes, not a runtime guarantee.
Peak pilot RSS 34832 KiB; planned 251-node mean payload 20,252,688 bytes.
The full-horizon inherited source allowance is <=3.3118e-5 before propagation;
the actual mean trajectory residual is unknown. Total-Z2 dominance remains
uncertified at beta=.003. No retargeting or new scientific success is claimed.

Review the exact mean operator (no w*d_z V), real-harmonic source factors,
zero-mode distinction, spatial tails, polynomial time residual and frozen-shear
correction. Independent mathematical review remains pending. Original archives
and source arrays are unchanged; no new downloads, full runs, pushes or external
actions. Stop here; the concrete full-run plan needs separate authorization.

## Bounded analytic Route B tightening (Codex, local review)

Branch codex/route-b-analytic-tightening, base
4bf68e0a6dcddc0d38b77c0123006fbea90d5f89. See
`math/all-time-phase-response/finite-time/route-b-tightening/NOTE.md`.
Fixed original parameters and beta=.003. New weighted Fourier inequality uses
inherited L2 information in the sup-norm estimate; zero-initial Duhamel cap
reduces integrated H1 loss without changing pointwise K. Candidate directed
bounds C_global<15128.8003 and C_endpoint<6921.6485 (endpoint G dependency)
replace the old87806.1462 majorant only for this proposed derivation. No original
archive changed. Dominance remains unproved; no measured coefficient is assumed.

One independent read-only AI review accepted the derivations and corrected
scripts. It caught upper-endpoint viscosity being used as a point; failed
candidate outputs/code are preserved and final outputs use exact1/28. Endpoint
scope/hash checks and both plan versions are retained. Eight focused tests
pass; less than5 seconds total computation, within300-second budget. Review
is not human refereeing; final documentation/commit has not been reviewed.

Smallest next proposal: enclose integral norm of mean q1 quadratic forcing
using250 interval hulls covering all fine nodes. If its certified total is<=.05,
then Z2>=.100907792>.06230 suffices with the candidate endpoint remainder.
This antecedent is NOT established. No mean-q2 evolution, source-only hull run,
DNS, full validator, downloads, pushes or merges. Stop for parent independent
review of the candidate formulas and exact local commit.

## Source-only mean forcing validation (Codex, local review)

Base f6cdc6d3eeed4c4e947eef0b56f48f1cc0b1eccd; branch codex/mean-source-hull.
See math/all-time-phase-response/finite-time/source-only-hull/NOTE.md.
All250 coarse hulls cover exactly the inherited12500 projected affine qN cells.
Physical LF in [0,.01163410], below fixed.05 checkpoint. Conditional Z2(T)
in [.23903543,.32288008] has lower endpoint above unchanged beta²C_endpoint
upper.06229484. Endpoint dominance comparison passes subject to inherited
certificates and focused review of this new implementation; no signed M solve.

Zero spatial mean/Poincare hypotheses documented for W,e,q2,r and mean fields;
M1>=nu explicitly asserted with exact1/28. Actual raw Q hash matches manifest,
validator and chain; exact Fraction accumulation independently checks interval
summation.17 tests pass. Pilot fits budget; full run36.62s; aggregate<45s<300s.
A postprocessing nested-key lookup failure was preserved and corrected; no
source output changed. No new reviewer, DNS, mean solver, downloads or external
writes. New code/outputs require parent-side focused independent review.
