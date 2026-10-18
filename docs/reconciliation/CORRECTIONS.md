# Independent-review corrections to PR19

Correction base: `e55d74e336270f5a5c3ae52c45a78c6523ef9347`.
Owner: Codex. These are bounded follow-up corrections, not a new numerical
campaign. The original integration review remains historical evidence.
The user authorized correction commits, PR19 updates, automatic preview/CI,
and a non-release archival tag for the missing older source. Main merge,
production deployment and retirement of source PRs remain separate decisions.

## Disposition of reviewed findings

| Finding | Verification and correction |
|---|---|
| 1. Input index reverted | Confirmed. Restored `math/inputs/README.md` exactly from 1245d0c: v2's delay claims are attributed and corrected, proof-audit README.txt and all-time ZIP row restored. No payload modified. |
| 2. Perturbation overclaims | Confirmed. Replaced “theorem is true,” “wrong by eighty orders,” and b=1 theorem-prediction wording with an unrefereed application of known stability, uncertified sampled constants, and empirical finite-grid scaling. No inferred working radius or stability boundary. |
| 3. Letter's site checklist | Confirmed stale. Describes this tree's `/outline` and `/proof` redirect; requires checking actual production before sending. A review branch/preview is not production. No correspondence sent. |
| 4. Jet run guide | Confirmed. Combined suite is 18 cases; lists all five import/provenance files. Commands first copy the audit subtree to a fresh scratch directory, preserving sibling dependencies. Current nmax=14 float guard requires even phases >32; use 36 and a separate rerun log. Historical 32-phase output is preserved. |
| 5. Missing 77916bb source | Confirmed in original bundle and checkout. Exact-SHA fetch recovered full commit; all 46 manifest source/blob pairs verified. Five previously missing blobs listed in SOURCES.md. Prepared annotated non-release archival tag and verified supplemental bundle; no rewritten manifest hashes. |
| 6. Missing map/index rows | Added evidence-labelled rows for phase-family checks, perturbation, oscillation, respiratory code/site and speech motivations in both indexes; all-time entry also explicit. |
| 7. Standard label absent | Added Standard, Refuted and Synthetic definitions to the linked math legend. Standard means established result under assumptions, not novelty or a Lean certificate. |
| 8. Missing Helical payloads | Source path, byte size and SHA256 documented for all three omitted files, read from pinned 0c3fe5d. Available in source history, absent from selected working tree; no licensed payload import. Optional ensemble rerun requires a verified authorized ZIP and writes to a fresh scratch path. |
| 9. Novelty statement | Removed “new part” assertion; explicit response calculation does not establish novelty. |
| Favicon | Restored PR18's inline SVG icon metadata and standalone Shared Air data icon without changing model code or dependencies. Browser checks confirm icons and no resource 404s. |
| PR7 hosting corrections | Historical root-FastAPI success distinguished from current Next.js target; separate API deployment requires its own review. Historical decision boundary and authorized PR19 preview status clarified. |
| PR15 handoff/authorization | Restored historical selective-import section and its authorization limits, with canonical link and explicit historical pending-review context. |
| Import record dates/banners | IMPORT*.md labelled historical PR15 narratives; current guide and this fresh-validation record linked. Historical passes are not represented as new runs. |
| Root math navigation | Added links for jets, Shared Air, letters, all-time response and distinct checks/perturbation/oscillation folders. |
| “Unchanged scripts” | Review README now discloses the two comment lines and one runtime warning added to the historical radius script; calculations/results remain unchanged. |
| Perturbation run commands | All internally writing and redirected commands now operate in a full scratch copy, never the repository archive. No campaign executed. |
| Weak negative controls | Assertions now require exact exit codes, intended mismatch/missing-order diagnostics and absence of unrelated traceback. Six guard cases independently rerun. |
| Objective.lean zero-delay wording | Stored theory log/AUDIT §3 establish τ=0.02 s for g=2.98. Corrected comment to one-step minimum delay; executable source unchanged. |
| s≥4 rationale | Canonical Kato–Ponce/first-derivative estimates hold for integer s≥3. Corrected the unnecessary second-derivative requirement; chosen s≥4 theorem/radius figures and R≥8 common-K ceiling remain unchanged. |

## Scaling and radius interpretation

For the finite-b quotient `(O_b−O₀)/b²`, the deviation from the variational
coefficient is expected to be O(b²), corresponding to an O(b⁴) **raw** remainder.
Changing b from 1/4 to 1 multiplies b² by 16; an approximately sixteenfold
quotient-error increase is an empirical observation outside the proved regime.
The separate raw-remainder ratios near 16 on halving b are quartic checks,
not b² scaling. Their values (including finite-time ratios near 15.3–15.9)
must be interpreted using the stated normalization, not relabelled wholesale.
Smooth discrete-map asymptotics do not certify the all-time PDE estimates.

The checked ceilings 7.1421232402e−22 and 1.6265634771e−80 remain upper bounds
on thresholds from sufficient conditions. Neither is a certified working
radius, a necessary regularity condition or a stability boundary. No new DNS
or proof-novelty claim was introduced.

## Source preservation

Recovered source commit: `77916bb51ea88ea6e1b2cddd2cd6e9309993383f`.
Annotated archival tag: `archive/research-source-77916bb-20261018`.
Tag object: `e56953e97454f331eb5205df226f87f979a858da`.
This is not a release. The correction handoff reports actual remote publication
status after review; this local record does not presume it.

The original delivery bundle lacked that commit and five blobs, as independently
confirmed using a bare clone of the original bundle. It remains unchanged.
`recovered-source-77916bb.bundle` is a supplemental complete-history bundle;
`git bundle verify` passes. A future full package must include this supplement.
The existing 110 archive hashes, source maps, Next/React manifests/lockfile and
root `nano hybrid.patch` are unchanged.

## Fresh bounded verification

Same Python 3.12.14 environment and pinned runtime dependencies as the original
integration. Logs: `/tmp/nicu-correction-evidence/` plus web build/type/test logs
under `/tmp/nicu-correction-*.log`.

- Jet suite: **18 passed**, including six strengthened import guard cases.
- Respiratory/physiology: **138 passed**, including the 41 physiology cases.
- Offline suite: **12 passed**, no skips.
- Phase-response suite: **9 passed**.
- Web suite: **4 passed**; production build and TypeScript check passed.
- Initial browser check exposed the separately missing Shared Air icon; restored
  that exact PR18 icon too, then reran the check.
- Chromium: 12 route/viewport checks at 390/1440px across `/`, `/outline`,
  `/proof` redirect, `/demo` and both Shared Air routes; no page/HTTP errors or
  horizontal overflow; inline icons present. Expanded outline checked.
- All **110** archive hashes match; dependency files/root patch unchanged.
- Objective.lean source after the initial comment is byte-identical to e55d74e.
- Input index byte-identical to 1245d0c; all **46** source-map entries verified
  against recovered 77916bb; supplemental source bundle verifies.
- `git diff --check` passes for this correction diff.

Independent read-only review of the working correction diff found no substantive
blocker, independently checked source mappings and reran **six** guard cases.
Exact correction-commit review and hosted results are reported in the PR handoff.
No long numerical campaign, local Lean kernel build, production deployment or
clinical validation is claimed. Existing e55d74e hosted success does not validate
this follow-up commit until its own checks run.
