# All-time phase response: proof and bounded numerical pilot

Owner: Codex. Base: `efff6a5b43d699c22eb6bef8c0ce666837d3d785` (current main at
inspection). Branch: `codex/all-time-phase-response`, isolated worktree
`/workspace/all-time-phase-response`. Local-only task; no merge, push or deploy.

- [PROOF.md](PROOF.md): analytic all-time small-b theorem, coefficient variations,
  derivative budget, uniform cubic field and quartic observable remainders.
  Constants are symbolic; no numerical regularity radius is certified.
- [response.py](response.py): directly integrates U,q1,q2 and computes E2,Z2,S2.
  Imports the existing [audit solver](../ns-phase-audit/audit_v2/dns/ns.py);
  its normalized real FFT, projection, strict cutoff K=floor((N−1)/3), and
  classical RK4 are reused unchanged. No duplicate full NS solver is added.
- [test_response.py](test_response.py): nine focused tests, including an
  independent one-dimensional base solve, exact rational jets from the existing
  audit, factorial convention, six stretching slots, and phase aliasing.
- [pilot.py](pilot.py): reproducible refinement and full-solve comparisons.
  Stores parameters, source hashes, Python/NumPy versions, actual time step,
  normalized norms, units, seed (none: deterministic), CPU and wall time.
  Any failed acceptance check returns nonzero. No result is machine-precision DNS.

From this directory with Python and NumPy already installed:

```sh
python -m unittest -v test_response
python pilot.py --output results/pilot.json
python pilot.py --coarse-N 18 --output results/refined.json
python pilot.py --recheck-saved results/pilot.json results/refined.json --output results/recheck.json
```

The first pilot **fails** the pre-registered spatial tolerance, deliberately
preserved in [results/pilot.json](results/pilot.json). Do not present that command
as a passing test. The refined pilot passes in
[results/refined.json](results/refined.json). Both use a=c=d=1, ν=1/28, T=0.5.
The nine unit/exact tests pass ([log](results/tests.txt)).
The first attempt to invoke the test file used an incorrect working directory
and failed import before any tests ran; the corrected command above ran all tests.

| Check | First pilot (12³→18³) | Refined (18³→24³) | Pre-set limit |
| --- | ---: | ---: | ---: |
| Time-step difference in E2/Z2/S2, dt=.01→.005 | 2.92e−10 | 2.97e−10 | 2e−7 |
| Spatial difference in E2/Z2/S2 | 3.16e−4 **FAIL** | 9.72e−7 | 2e−4 |
| cos(2φ) response difference, 8→12 phases | 2.18e−15 | 4.67e−15 | 2e−6 |
| Wall time | 67.1 s | 102.3 s | bounded pilot |

Differences are componentwise maximum absolute errors, not rigorous error bars.
At φ=.37, N=18, dt=.005, ±b full solves with |b|=.1,.05 give a second-response
error ratio 3.99966 (expected 4) and a second-order field L² remainder ratio
7.99936 (expected 8). These are finite-system checks at moderate b, **not**
certificates that those b lie inside the analytic smallness radius. The refined
phase experiment still uses N=18 for these separate full-solve checks.

At T=.5 the resolved cos(2φ) coefficient of the b² response, ordered E2,Z2,S2,
is approximately `(2.79029e−7, −5.28576e−5, −6.05631e−4)`, stored at
`runs[-1].harmonics_E_Z_S["2"].cos` in the refined JSON. Values
are computed by the variational equations; full-solve differences only validate
them. The exact jet test independently recomputes
`[t⁶ cos(2φ)] Z = −6487 a²b²c²d² / 1555200` with symbolic viscosity at unit and
generic rational amplitudes, and checks lower-order absence and zero ν powers.
It checks the full exact jet and the known leading b² monomial, not a certified
error bound for the variational time integration.

Phase quadrature agreement is limited evidence. On six equispaced phases,
cos(4φ) aliases into cos(2φ); a regression test demonstrates this exactly up to
floating-point rounding. Neither 8 nor 12 points integrates an infinite phase
spectrum exactly. No long-time phase-optimization or harmonic-tail claim is made.

## Provenance, contradictions and integration overlap

Main contains no root AGENTS.md, CLAUDE.md, RESEARCH.md or docs/HANDOFF.md.
Their PR15 versions were read before editing, together with the math/audit
instructions and relevant source files. `/workspace/.agents` is empty. The
only checked-in CLAUDE.md on main belongs to the separate Hou–Luo project;
its numerical claim discipline was read, but that project was not modified.
This directory records the scoped handoff instead of importing PR15's unrelated
application/documentation reorganization.

Inspected remote heads:

- PR18: `0664aaf81c87de115a8fcad054397a70b740ba2e`.
- `claude/phase-family-b2`: `f7709be13cbe5cf7c481ab2246450f79e09c4815`.

PR18's API/check-state lookup was attempted once via `gh pr view` and rejected
by GitHub (GraphQL Forbidden); a REST metadata fallback also returned HTTP 403.
The git PR head fetched successfully. **PR state and CI checks remain unknown**;
no merge/watch instructions were followed. PR15's git head was inspected for
instructions and overlap, not integrated.

PR18 and PR15 both touch README.md, math/README.md, and the Shared Air audit,
tools and result paths. They also carry conceptually overlapping exact jets
under different paths (`ns-phase-audit/enstrophy-jet` versus
`math/navier-stokes-jet`). This task adds only the new math directory and one
math index row; that index row is the only direct file overlap. Exact-jet code
already on main is reused, so no PR18/PR15 jet copy is introduced here.

The phase-family branch's README still says “it proves that b=10^−80 is safe”.
That numerical certificate is **not established** by sampled gradient norms,
unverified constants and incomplete tail/phase enclosures. The parent reports
that newer Claude messages retract this language and the old six-phase late-time
estimates; those messages are not a modification of the inspected commit.
The new analytic result does not adopt either claim. Observed long-time ratios
at b=.1/.2 are not regularity thresholds. Additionally, that branch's full DNS
uses K=N//3 at N divisible by three; retained boundary modes can alias. The
solver reused here instead enforces N>3K, which also makes the spatial average
of the cubic stretching product exact for the retained trigonometric polynomial.

## Remaining limits

The theorem is a paper argument, not formal verification. Constants have not
been optimized or evaluated with certified quadrature, truncation and infinite-
time tails. Numerical evidence stops at T=.5 and finite spatial/phase grids.
There is no continuum a-posteriori certificate, fourth-variation numerical
solver, long-time convergence study, or proof of exact finite phase bandwidth.
The source hashes distinguish the preserved first pilot from the subsequently
parameterized pilot CLI. The computation and proof address only this family.

## Independent adversarial review

A separate read-only reviewer inspected PROOF.md, the implementation and tests,
then independently ran all six original floating-point VariationTests (passed,
1.120 s). No blocking proof or implementation error was found. The reviewer
confirmed the derivative budget, residual equation, coefficient normalization,
and exact cubic spatial averaging under N>3K. Exact rational tests were inspected
but not independently rerun by that reviewer (the implementation owner ran them).

Two review findings were addressed: future pilot runs now test **all** reported
phase cosines and sines m=0,…,3, and explicitly store the fixed full-solve grid,
phase and time step. A regression test exercises a previously unchecked m=3 sine
component. The existing integration results were preserved, then reanalyzed
without rerunning DNS: [results/recheck.json](results/recheck.json) records source
hashes, the supplied full-solve metadata, and all-harmonic phase differences
6.69e−12 (first) and 4.54e−12 (refined), both below the unchanged 2e−6 tolerance.
This phase-only recheck does **not** change the first pilot's spatial failure.
Review fixes do not modify the integrator or response formulas.

A final review caught a recheck output/input collision hazard. The CLI now uses
a separate recheck default and rejects every explicit input/output collision;
a subprocess regression verifies a nonzero exit and unchanged input bytes.

## Clarification: which remainders and which ratios?

For O in (E,Z,S), define the **raw** observable remainder
`R_O(b)=O(u_b)−O(U)−b²O2`. The original `second_error` is

```
max_O |[O(u_+b)+O(u_−b)−2O(U)]/(2b²)−O2|
  = max_O |[R_O(+b)+R_O(−b)]/(2b²)|.
```

Its ratio 3.999658882 compares b=.1 to b=.05, after dividing the raw remainder
by b². It is dominated by S at this point. The corresponding maximum raw
even-observable remainder ratio is four times that value, 15.998635529.
The raw magnitude is 9.19762199e−7 at b=.1 and 5.74900402e−8 at b=.05.
This aggregate check alone did not separately test E and Z quartic scaling.

The ratio 7.999362229 instead compares
`||u_+b−U−bq1−b²q2||_L²` at b=.1 and b=.05: the norms were
1.169885763e−5 and 1.462473794e−6. It is a **second-order field truncation**,
expected to be cubic, not the residual after a cubic field truncation.
There is no numerical q3 implementation and no measured quartic field residual.
The original labels did not explicitly assert such a test, but were too terse;
future pilot JSON now includes these definitions. Archived outputs are unchanged.

All those full solves used a=c=d=1, ν=1/28, T=.5, φ=.37, N=18 (K=5),
dt=.005, and b=±.1,±.05. They used one phase, not phase quadrature.
The separate response-harmonic convergence experiments used 8 and 12 uniformly
spaced phases, with N=12/18 in the first pilot and N=18/24 in the refined pilot.

The added bounded check is independently reproducible:

```sh
python check_observable_remainder.py
```

[results/observable_remainder.json](results/observable_remainder.json) stores
**each** signed raw E/Z/S remainder for both ±b, their even averages, and
componentwise ratios. Acceptance [14,18] was set before the run; any failure
exits nonzero. At the same amplitudes, ν, T and φ:

| Grid / time step | raw E ratio | raw Z ratio | raw S ratio |
| --- | ---: | ---: | ---: |
| N=18, dt=.005 | 15.999124 | 15.998931 | 15.998636 |
| N=18, dt=.0025 | 15.999341 | 15.998929 | 15.998635 |
| N=24, dt=.005 | 15.998947 | 15.998935 | 15.998635 |

All nine componentwise checks passed. The new run took 18.0 seconds; total pilot
CPU time remains below 200 seconds, within the original approximate ten-minute
budget. These ratios are empirical finite-system order checks, not a bound on
continuum error or verification of the analytic constants. The proof's quartic
field claim remains analytic only. The appendix to PROOF.md records the parent
proof cross-check, its explicit phase-uniform base estimate, and the exact
mapping of the different trilinear slot conventions.

A separate follow-up reviewer independently recalculated all nine raw ratios and
even averages from the saved JSON, verified the script hash, and checked the
appendix. No new blocker was found. The smallest E remainder is about 4.65e−11,
so its ratio is more sensitive to subtraction cancellation than Z/S; the modest
variation under refinement is reported, not presented as machine accuracy.
