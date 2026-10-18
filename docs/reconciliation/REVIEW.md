# Local reconciliation review — 2026-10-18

Implementation owner: Codex. Branch `codex/reconcile-research-review` in
`/workspace/NICU-Math-reconcile`, based on fresh main
`efff6a5b43d699c22eb6bef8c0ce666837d3d785`. Original checkout
`/workspace/NICU-Math` remains on `work` at that commit, clean and unchanged.
No push, PR mutation, main merge, deployment, settings/credentials change,
paid API call or patient data was involved. The user reports all three Claude
sessions paused and clean; source heads are rechecked immediately before commit.

## Source matrix and overlap

[SOURCES.md](SOURCES.md) gives every full SHA and main-relative diff size;
[source-heads.json](source-heads.json) is machine-readable.
[pr-metadata.json](pr-metadata.json) records the read-only GitHub metadata snapshot.
All seven inspected PRs (#7, #13–18) are open; #7 is conflicting and has a stale
body targeting b606b03 despite head 6131438. #13–17 are drafts; #18 is not.
The metadata tool's base_sha may describe a stale base; the git main head above
is the baseline used here. No new remote PR heads appeared in the inventory.

This is a substantial consolidation (~300 files, predominantly historical
research logs), not a small patch. There was no whole-branch merge. Selection:

| Source | Decision |
|---|---|
| #14 ab448aaa | Application layout, offline defaults, two-compartment physiology, Next 16.4.2/React 19.3.1 and exact dependency lock retained. |
| #7 6131438 | Its unique documentation correction retained in HOSTING.md and [original review](pr7-review.md); its older no-web tree is not restored. |
| #16 14fe98a / #17 4316095 | Corrected formulas, counterexamples, RC sampling/segmentation and tests retained; failed-before-fixed provenance remains in historical handoff. |
| #18 6f874a2 / all-time 1245d0c | Latest selected research prose, letters, Shared Air and jet results, Lean comment corrections; its alternate site presentation is superseded by the combined claim audit. |
| #15 a9aaf1f | Failure guards and negative-control tests adapted into `math/ns-phase-audit/enstrophy-jet/`; original blob map/import record and speech-motivation note preserved. No duplicate jet implementation. |
| peaceful 43d41e9 | `/outline`, `/proof` redirect, status banner, navigation and distinct `math/phase-family-checks/` evidence retained. Its duplicate all-time package is superseded by 1245d0c. [Historical handoff](peaceful-handoff.md) preserved separately. |
| codex/all-time 12ea61f | Original delivery retained in the uploaded source ZIP and source git ref; 1245d0c supplies the canonical reviewed package. |
| phase-family-b2 a6c0739 / locking 0c3fe5d | Distinct perturbation and oscillation packages retained with finite-grid/uncertified-radius caveats. Additional uploaded PDFs/ensemble ZIP not newly copied because licensing is unestablished; source refs preserve access. |
| new-session a5e20d3 | Two unique commits on PR17: homepage intent/docs-host wording and hardened asset guard/evidence-mode test, byte-identical source files. Handoff section manually retained with historical context. |

The all-time source branch is based on older PR18 history; selections were made
against pinned file content, without assuming it descends from current PR18.
Shared Air's later results remain canonical. Two differing PR15 outputs live
under `math/shared-air/results/pr15-original/`; incompatible logs were not
silently overwritten. The 110 result files in
[archive-hashes.json](archive-hashes.json) are byte-identical to their named sources.
The failed initial pilot remains FAIL; phase rechecking does not repair its
spatial tolerance failure. Sourcehash/version provenance remains unchanged.

## Scientific and presentation decisions

- The site retains PR16's false Sobolev deduction, inadmissible shrinking closed
  sphere and stationary-sphere counterexample explicitly. Standard identities,
  refuted deductions, open gaps and clinical analogies have separate labels.
  A global “everything is open/unverified” banner was corrected.
- Stokes flow is described only as an approximation requiring negligible
  inertia at specified scales, not an exact model of all alveolar dynamics.
  No clinical collapse/PDE singularity equivalence or general NS solution.
  Unsupported universal clinical numbers/treatment timing in the alternate
  outline were replaced by model motivations and assumptions.
- The canonical all-time note retains bibliographic attribution, explicit scope,
  protected output paths, archived failed pilot and review scripts from 1245d0c.
  It applies known large-solution stability; neither novelty nor human referee
  approval is established. AI reviewers are labeled as such.
- Ratios near 16 test finite-system local response implementation. Finite-b
  ratios are asymptotic, not exact identities. All-time exponential upper
  envelopes allow transient growth. b-evenness alone does not establish the
  separate 3|m| phase-onset rule.
- The checked s=4 lower-norm argument gives κ₄=9/(16√2), I₄≥112,
  F₄=2√2, hence r₄≤exp(−63/√2)/63=7.1421232402e−22. For R≥8 and
  common K≥κ₄, β≤exp(−252/√2)/252=1.6265634771e−80. Upper ceilings are
  not certified usable radii/stability boundaries. Historical enormous
  ceilings derived from sampled norms/upper majorants are retracted in the
  evidence README and carry a standalone script warning. Archived outputs
  remain intact. The other branch's evaluated 1e−80 is a different, uncertified
  calculation, not this theorem's usable radius.
- Next.js remains the hosted frontend; FastAPI and Streamlit remain separate
  offline/local services. Swagger/ReDoc external documentation hosts are
  disclosed. No patient infrastructure or uploads were added.

## Fresh verification

Python 3.12.14, NumPy 2.0.2, SciPy 1.18.1, python-flint 0.9.0, pytest 9.1.1;
Node 24.19.0. Temporary environment `/tmp/nicu-reconcile-venv`.
Evidence logs are included in the downloadable review archive.

| Command (from repo root unless noted) | Actual result |
|---|---|
| `python -m pytest -q tests/navier_stokes tests/physiology` | **138 passed**: 66 synthetic pipeline + 31 claim corrections + 41 physiology, 0.67s. 138 is the combined count, not 138 plus 41. |
| `NICU_OFFLINE=1 python -m unittest tests.test_smoke tests.test_requirements tests.test_optional_pdf -v` after a5e20d3 import | **12 passed**, no skips, 1.359s. Earlier 11-test runs do not validate the final homepage addition. |
| `python -m pytest -q math/ns-phase-audit/enstrophy-jet/tests` | **18 passed**, 6.09s; includes mismatch/missing-order negative controls. |
| `PYTHONDONTWRITEBYTECODE=1 python -I -B -m unittest discover -v -s . -p test_response.py` in all-time folder | **9 passed**, 1.704s. |
| all-time `pilot.py --recheck-saved ... --output /tmp/.../recheck.json` | Phase checks pass for both saved runs; first pilot still FAIL spatially. No DNS rerun. |
| all-time `review/radius_ceiling.py` | FFT/formula norm assertions pass; supported ceilings reproduced. |
| jet `compare_audit_v2.py` | Exact Fraction equality: 61 Z and 53 E harmonic polynomials through order 12; zero mismatches. Stored-output comparison, not regeneration through 14. |
| `node math/shared-air/tools/quick_check.js` | All 16 DEF.pulse fields match. |
| oscillation `python test_locking.py`, `python test_triads.py` in its folder | 11 lock checks and three phase-family checks pass. |
| `npm ci --cache /tmp/nicu-npm-cache` in web | Pass; no manifest/lockfile changes. |
| `npm run build` in web | Pass, rerun after final metadata wording edit. |
| `npx tsc --noEmit --incremental false` | Pass. |
| `node --experimental-strip-types --test web/tests/ns.test.mjs` | **4 passed**; module-type inference warning only. |
| Chromium production routes at 390 and 1440px | `/`, `/outline` expanded, `/proof` expanded after redirect, `/demo`, `/shared-air`, `/shared-air/index.html`: HTTP 200 final responses, no page errors or horizontal overflow. |
| `python -m compileall -q api ui tests physiology navier_stokes`; `python -m pip check` | Pass. |
| Lean comment-stripped token comparison | All six changed `.lean` files match main's executable tokens. |
| Archive/dependency preservation and secret-pattern review | 110 archives match; web pins/lock match #14; no new secret-like values found. Synthetic data/results only in selected additions. |

Failures/limitations accurately retained:

- Initial npm ci failed because `/home/agent/.npm` was unwritable; a fresh
  writable temporary cache resolved it. No network/security settings changed.
- Initial offline run skipped two optional PDF tests; pinned PDF dependencies
  were installed, and final 12-test run passed without skips.
- An attempted unittest discovery of oscillation scripts reported `SystemExit:0`
  as import errors. Those are standalone scripts, not unittest modules; their
  documented direct commands then passed. No tests were changed to hide this.
- `git diff --check` flags whitespace in original Shared Air archived render
  logs and `corrections.diff` only. These bytes are intentionally preserved.
- Lean/lake is unavailable, so no fresh kernel build. No full order-14/40 jet
  regeneration, broad numerical campaigns, long DNS, Docker rebuild, hosted
  runtime/CI, database/paid evidence integration or clinical validation run.
- This retains #14's dependency fixes; it is not a new whole-stack security
  certification. Historical remaining advisory findings remain deferred.

## Patch provenance and preservation

Root `nano hybrid.patch` is unchanged. It entered in
`d10fbbb75aba181505db73262a1849d4a2b3d1ef` (“Add files via upload”), with placeholder
blob indices and hybrid FTS/cache changes. Its exact generator and whether all
changes are already represented are unestablished. It is not safely classified
as an obsolete reproducible generated diff, so it was preserved, not removed.

Pinned commits are additionally protected by local `refs/reconcile-sources/*`.
The review archive contains a binary-capable patch, full selected tree, source
bundle, source matrix and test logs. Original branches/commits and checkout are
untouched. Import adaptations are attributed; no authorship is reassigned.

## Proposed approval sequence — not enacted

1. Review this local consolidated commit against efff6a5, including its pinned
   source matrix, archive hash audit and independent AI review. Resolve any
   source drift before publication. This is the single proposed integration.
2. Only after explicit authorization, publish the consolidation and prepare one
   PR against current main. Do not separately merge #18 into #14 or stack the
   duplicate all-time copies. Publishing may trigger existing preview automation.
3. After approved integration and observed checks, mark #7 and #13 superseded
   by the baseline; #14 by the consolidated security/application baseline;
   #15 and #18 by the single canonical jet/Shared Air/letters selection;
   #16 and #17 by the corrected respiratory stack and tests. Close/retarget
   nothing until the user approves the concrete PR retirement map.
4. Record the all-time, peaceful, phase-family, lock-map and new-session source
   SHAs as incorporated/superseded at file level, retaining their branches or
   archive refs. Do not delete source branches. Recheck older #3/#5 only as a
   separate retirement decision because #7 already adapted their scope.
5. Merge/deployment are later, separate decisions. Keep the Claude sessions
   paused through this combined review; no further commands are needed now.
