# Documentary reconciliation of the external PDF review

Scope: repository evidence only, based on repairs commit
`0f83002654040c88e4bc652c4589550696cae3bf`; compared with the earlier technical
note at `3161f059c24878c9b5ea05e6cc081e72fb53bbc5`. The external review was
supplied by the user. Its separate solver and PDF were not available in this
worktree; their reported values are not independently verified here. No PDE
computation, scalar postprocessor rerun, LFS download or external research.
This is a documentation patch, not a revised theorem or certificate.

## Current corrections for the PDF

The technical note now explicitly defines H0 (inherited existence, uniqueness
and smoothness on [0,T]), spatial mean zero for W=w/b², the Frobenius norm for
m1, and translation z→z+pi giving H_-b=H_b by uniqueness. These clarify inherited
hypotheses/identities, not additional validation. W here is the nonlinear
scaled remainder, not the similarly named base-flow array in absorption-b003.

It defines d1,d2 as older upper bounds on ||X(T)||2, d_div as the improved
upper bound on the same scaled response, and

    ||Y(T)||2 <= nonself = smooth + err_adv + err_grad,
    integral_0^{t_(j+1)} ||Delta W(s)||2² ds <= D_w,j.

D_w,j is cumulative, scaled dissipation, not instantaneous dissipation and not
an increment inferred by differencing upper bounds. The old bounds are given
explicitly by the source-cell propagation/Abel formulas from endpoint-sign
PLAN E and scripts/tr_remainder.py. Tables should label C_one,TR and C_new
as **coefficients in R_Z >= -b^4 C**, and d1,d2,d_div as **norm bounds on
scaled X**. C_new<=377.312890, whereas beta² C_new<=0.003395816008963.
No archived numeric output or proof source is overwritten.

## Source/evidence map and historical wording

Paths below are relative to `finite-time/`, unless otherwise stated.

| Issue | Repository evidence | Interpretation for current presentation |
| --- | --- | --- |
| Upstream provenance | `endpoint-beta003/AUDIT_FOLLOWUP.md` items 1–2, current `check.py`, `results/followup/regression.json`, current ENDPOINT_CERTIFICATE appendix | Already repaired at 0f830026: time_refinement.final.json is hash-checked but not parsed by the final postprocessor; its global D_r enters the upstream err_grad calculation. It remains a mathematical/arithmetic dependency. |
| Historical provenance-only wording | ENDPOINT_CERTIFICATE at 3161f059; `endpoint-beta003/AUDIT_REPAIRS.md`; `results/repair/regression.json` and `.log` | The older wording can imply no upstream dependency if read out of context. Preserve it as stage-specific history and link current AUDIT_FOLLOWUP. Do not copy it into the new PDF. |
| Original certificate links | ENDPOINT_CERTIFICATE appendix links to 0f258a1/check.py and candidate.json | Intentionally pinned original implementation and result, not current repaired code/status. Identify them as historical evidence; current code and follow-up are at 0f830026. |
| Historical first-stage status | `endpoint-sign/DERIVATION.md` opening says review pending | It describes the frozen first stage. Later `endpoint-sign/REVIEW.md` and README record completed targeted reviews; the opening is not current overall review status. |
| Six tests | `endpoint-beta003/results/tests.log`, original REVIEW.md, original 0f258a1 stage | Six tests were recorded then. |
| Seven tests | `endpoint-beta003/results/repair/tests.log`, AUDIT_REPAIRS.md, 3161f059 stage | Seven tests were recorded after production-helper/toy changes. |
| Eight tests | `endpoint-beta003/results/followup/tests.log`, AUDIT_FOLLOWUP.md, current test_check.py at 0f830026 | Current source has eight test methods and the retained log reports eight passing tests. Not rerun for this documentary patch. |
| Separate six-test suite | `endpoint-sign/scripts/test_tr.py`, endpoint-sign README/REVIEW | A different suite; do not combine it with endpoint-beta003 counts. |

## G versus G-prime: precise distinction

`endpoint-sign/DERIVATION.md` equation (6) defines G'=1.8534 as a safe upper
bound and uses it in its first-stage C_one/C_end formula. That remains a valid
looser inequality. The time-resolved value C_one,TR≈1201.9175374897753 is instead
computed by `endpoint-sign/scripts/tr_remainder.py`, which reads
`z2-endpoint/results/endpoint.json`, key
`bounds.base_true_laplacian_upper.hi`:

    G_upper = 1.853301043405617417583187640523750362023.

The script asserts this endpoint <=1.8534, then evaluates
`Cone = G * tr['Nbar'] + S * tr['Er']`. The full decimal endpoint is an
inherited evaluated **upper bound**, not an assertion of the exact true norm.
The separate `endpoint-sign/scripts/sign_enclosure.py` uses 1.8534 for its
global comparison. PLAN F documents the time-resolved G formula. Current
`endpoint-beta003/check.py` likewise reads G_upper and checks <=1.8534.
Therefore the PDF must not attribute 1201.917537... to literal substitution of
1.8534 into the first-stage equation (6); identify the tighter time-resolved
input/formula. Historical files and original outputs remain unchanged.

## What prior checks do and do not establish

`absorption-b003/NOTE.md` under artifact availability records an author-side
full check_artifact.py --full (about 11 min), with fresh validator output and
chain matching apart from timing. It also records an **independent reproduction
reported by the user at e9aa28a**: numerical values agreed from LFS arrays, with
a metadata-only Python-version mismatch (3.13.16 versus 3.12.14). These are
repository records of earlier runs, not fresh verification in this task.

`endpoint-sign/REVIEW.md` records independent per-cell and A–F reproduction;
`endpoint-beta003/AUDIT_REPAIRS.md` records the separately implemented directed
Decimal scalar reproduction at b03bfa45ae25d3543d7ecbd3a2361f990d01120f and
resolved-field algebra checks. That audit explicitly did not rerun inherited
certificates. AUDIT_FOLLOWUP records targeted code/proof checks of later repairs.
The b03bfa4 independent-checks folder is linked at its own commit and is not
present on this repair branch; this reconciliation uses the local report of
that audit, not a new inspection of its remote implementation.

Thus “the entire inherited chain was never independently checked” is too
broad relative to repository records. Distinguish the reported full-validator
reproduction, targeted proof/code checks and independent scalar reproduction
from an end-to-end human review or formal verification: no such latter
verification is established by the evidence inspected here. AI audit is not
human refereeing. Preserve all hypotheses of the conditional theorem.

## Margin and numerical-comparison cautions

The threshold J2_lo/beta²≈911.19 compared with C_new≈377.31 measures slack only
in the final sufficient scalar comparison **with J2_lo, beta and assumptions
held fixed**. It does not permit arbitrary 2.4-fold errors in upstream constants.
Those constants enter nonlinear products, squares, exponentials, square roots,
and multiple dependent enclosures; some also affect J2_lo and closure. A
changed input requires a justified propagation, not a blanket error allowance.

The review's ratio 377.3/(6.4e-5) is about 5.9 million, not 5.9 thousand.
Even if the denominator is a valid empirical estimate of a remainder
coefficient, numerical agreement does not make it a rigorous remainder bound.
Neither that value nor the review's separate ns_check.py run is verified here:
the review reports H/b²≈0.0210133542 at grids 24,32,48, but its scripts, outputs,
parameters and normalization must be obtained before claiming reproduction.
The published paired-DNS package at f9a1b224 instead records our three specific
configurations, including N24 temporal refinement and N32 spatial refinement;
it makes no N48 claim.

The review's decomposition of the quadratic coefficient into approximately
+0.0354 from the q1-gradient **excess over heat** and -0.0144 from mean pairing
is compatible with, but different from, integrated stretching/dissipation:

    J2 = [||grad q1(T)||²/2 - exp(-2nu T)/4]
         + <-Delta U(T), mean(q2(T))>,
    H_b(T) = S_b(T) - nu R_b(T).

The former splits the b² coefficient at the endpoint; the latter splits the
finite-b energy balance over time. The raw ||grad q1||²/2 itself is not +0.0354
without heat subtraction. Negative mean pairing is not negative excess
dissipation. Neither decomposition's component signs imply those of the other.
Only the identities and compatibility are assessed here; the externally
reported component values are not independently verified.

## Validation and handoff

Documentation-only changes: ENDPOINT_CERTIFICATE, this reconciliation, and
required HANDOFF/RESEARCH_INDEX additions. No source, logs, outputs or historical
manifests changed. Whitespace and changed-path checks performed; no simulations
or tests rerun. The parent/PDF worker should review this local patch and use
its clarifications with the already published scalar and numerical artifacts.
No new independent review of this patch is claimed. No push, merge or deployment.
