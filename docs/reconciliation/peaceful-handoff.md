# Historical peaceful-branch handoff

Source: 43d41e916957b02359a5b0959057019fb8cf6950.
Statements describe that source tree; reconciliation corrections take precedence.

## Status labels, outline page, phase-family results (current, Claude)

Owner: Claude. Branch `claude/peaceful-wozniak-oaprql`, based on the PR #17 head
`43160952f2c851e2c9e340a66b48651a6a285046` (stacked on #16 and #14). User
authorized: rebuild on the Codex chain instead of `main`, relabel, fix the
homepage claims, import the reviewed all-time response package, push the branch.
No merge, deployment or settings change. Nothing is attributed to Codex that
Codex did not write; the imported package is Codex's work.

Scope:
- Repository-wide status labels (the `math/README.md` scheme) on every web page
  (`StatusBanner`), in `navier_stokes/` module docstrings, README and CLAIMS, and
  in `math/README.md` rows for `navier_stokes/`, `web/` and the new folders.
- The "Conjecture and Gaps" page moves from `/proof` to `/outline` with a redirect;
  its legend states what each step label means; clinical motivation is a separate
  section, apart from the mathematics. Homepage: banner, pointer, open-airway
  clarification of the closed-sphere identity.
- `math/all-time-phase-response/`: Codex's patch (local commit `ddbca048`,
  uploaded by the user) applied unchanged except for this handoff; its tests,
  remainder check and refined pilot were re-run here and pass; its bundled audit
  modules are byte-identical to `main`.
- `math/phase-family-checks/`: this session's numerical checks (β = 0 reduction,
  b² response, independent reproduction of the Codex response, compliance table).
- `math/ns-phase-audit/audit_v2/AUDIT.md` §7.5 pointers; research index rows.
- Independent review of the imported package by three referee agents in this
  session (`math/phase-family-checks/review/`, scripts with paths made relative,
  outputs as produced): sound with corrections, no blocking error. Findings are
  recorded in `math/phase-family-checks/README.md`.

Validation at this commit, in the session container (Python 3.13.x, Node 22.22,
NumPy 2.0.2, SciPy 1.18.1, Next.js 16.4.2):
- web: `npm ci && npm run build` passes (TypeScript included);
  `node --experimental-strip-types --test web/tests/ns.test.mjs`: 4 tests pass;
  a local `next start` returns 307 from `/proof` to `/outline` and 200 for
  `/`, `/outline`, `/demo`, `/shared-air`.
- `python -m pytest -q tests/navier_stokes tests/physiology`: **138 passed**.
- `NICU_OFFLINE=1 python -m unittest tests.test_smoke tests.test_requirements
  tests.test_optional_pdf`: 9 of 11 pass, 2 skipped (optional PDF). The two
  `StreamlitSmoke` cases error on `import altair` under this container's
  Python 3.13 (`_TypedDictMeta.__new__() got an unexpected keyword argument
  'closed'`); they fail identically on the untouched PR #17 head, so the failure
  is the environment, not this change. The project instructions call for
  Python 3.11 or 3.12 in a virtual environment.
- `python -m compileall -q api ui tests navier_stokes math/phase-family-checks
  math/all-time-phase-response` passes; `python -m navier_stokes.demo` runs.
- `math/all-time-phase-response`: `python -m unittest -v test_response` 9 pass;
  `python check_observable_remainder.py` passes (ratios 15.9986 to 15.9993);
  `python pilot.py --coarse-N 18` passes (space 9.7e-7, time 3.0e-10,
  phase 4.5e-12, ratios 3.99966 and 7.99936) and reproduces the stored
  `results/refined.json` harmonics exactly.
- `math/phase-family-checks/check_p1.py` and `compliance/ls_repro.py` re-run
  from their repository locations with the stored numbers.
Not run: Lean builds, the pangram suites, the long numerical runs of
`phase-family-checks` (their stored results are from this session).
