# All-time phase response: proof and bounded numerical pilot

Written by Codex (ChatGPT), 18 October 2026, and delivered as a patch on
`efff6a5` (its local commit `ddbca048`). The verbatim delivery is kept as
uploaded in
[`../inputs/all-time-phase-response.zip`](../inputs/all-time-phase-response.zip).
A verbatim copy was also pushed by another session as branch
`codex/all-time-phase-response` (12ea61f); this folder supersedes it. The
files here differ from the delivery only as [Changes on entry](#changes-on-entry)
lists. How it was reviewed here, and how it relates to the rest of `math/`, is
under [How this fits the repository](#how-this-fits-the-repository).

**In one paragraph.** For the phase family u0 = (a sin y, b sin z, c cos x −
d cos(x+y+φ)) with ν > 0, [PROOF.md](PROOF.md) argues on paper that some
b0(a,c,d,ν) > 0 exists such that every |b| ≤ b0 gives a smooth solution for
all time, and that E, Z and S then equal their b=0 values plus b² times
computable coefficients E2, Z2, S2, up to an error of order b⁴ that decays in
time. It is a standard perturbation argument, an instance of classical
stability results (PROOF.md, "What this is not, and where it sits"). b0 is
never computed. At the tested parameters a=c=d=1, ν=1/28 the proof's own
condition certifies no |b| above 7.2×10⁻²², whatever values its uncomputed
constants take ([review/radius_ceiling.py](review/radius_ceiling.py)). The
numerics confirm the formulas for E2, Z2, S2 on finite grids at T=0.5; they do
not test the all-time bounds or the radius. Nothing here is about b=1,
statement (B) or the Millennium problem.

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
- [review/](review/README.md): the scripts and logs behind the numbers that this
  README and PROOF.md quote from the review made here.

From this directory, with Python 3 and NumPy. The commands write new
`*.rerun.json` files; the scripts refuse to overwrite the archived results.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -I -B -m unittest discover -v -s . -p test_response.py   # 9 tests, about 2 s; the variable keeps the test's pilot.py subprocess from writing __pycache__
python3 -I -B pilot.py --coarse-N 12 --output results/pilot.rerun.json    # the preserved FAIL, about 1 min
python3 -I -B pilot.py --coarse-N 18 --output results/refined.rerun.json  # passes, under 2 min
python3 -I -B pilot.py --recheck-saved results/pilot.json results/refined.json --output results/recheck.rerun.json
python3 -I -B check_observable_remainder.py --output results/observable_remainder.rerun.json  # about 18 s
```

The first pilot (12³→18³) **fails** the pre-registered spatial tolerance
(3.16e−4 > 2e−4, in S2 at φ=0), deliberately preserved in
[results/pilot.json](results/pilot.json). Do not present that command as a
passing test. The refined pilot (18³→24³) passes in
[results/refined.json](results/refined.json). Both use a=c=d=1, ν=1/28, T=0.5.
The nine tests pass ([log](results/tests.txt)): five are mathematical
(including one exact-jet check of the t⁶ cos 2φ monomial), three test the
command-line tooling, and one demonstrates phase aliasing.

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
spectrum exactly: on 8 phases, for example, cos(5φ) is indistinguishable from
cos(3φ). So the 8-versus-12-phase differences over all harmonics m=0..3
(6.7e−12 and 4.5e−12 in [results/recheck.json](results/recheck.json)) measure
only phase aliasing (of harmonics |m|≥5): both phase sets use the same grid and
time step, and their shared phases φ=0, π/2, π, 3π/2 give identical values.
They are not error bars for the discretisation.
No long-time phase-optimization or harmonic-tail claim is made.

## Changes on entry

The delivery's own provenance notes (its inspection of PR #15, PR #18 and
`claude/phase-family-b2`, GitHub API errors, paths in the Codex workspace)
stay in the uploaded ZIP. Two of them are now out of date: `claude/phase-family-b2`
(a6c0739) calls its 10⁻⁸⁰ "evaluated, not certified" and has fixed its
dealiasing cutoff (its `math/phase-family-perturbation/README.md`). Changes
made when this folder entered the repository:

- PROOF.md: the dependence of the constants on a, c, d and ν; a Kato–Ponce
  citation and the test-pair lower bound on K_s; a ceiling on the radius in
  (1); the Galerkin wording; a pointer to the standard analytic dependence on
  the data (no specific reference; it is not used in the argument) in place of
  the parameter-differentiability sketch; links to P1 and Rule B, with the
  onset orders for E2, Z2 and S2; a section "What this is not, and where it
  sits", with references; the appendix's "independently audited" reworded.
- This README: a new header and summary, commands that work under
  `python3 -I` and write `*.rerun.json`, this section in place of the
  delivery's provenance notes, the section below, and a reworded review
  heading. The new folder [review/](review/README.md) holds the review's
  scripts and logs.
- `pilot.py` and `check_observable_remainder.py` now run under `python3 -I`
  (they put their own folder on `sys.path`), record `null` instead of
  crashing when there is no git checkout, write `*.rerun.json` by default and
  refuse to overwrite the archived results. `check_observable_remainder.py`
  gained `--output`. No numerical code changed; `response.py` and
  `test_response.py` are unchanged.
- The archived results are kept byte for byte. `results/pilot.json` and
  `results/refined.json` were written by two earlier versions of `pilot.py`
  (sha256 `d42b429a…` and `a9d54d90…`, recorded inside them), and
  `results/observable_remainder.json` by the delivered
  `check_observable_remainder.py` (`1ff38a94…`) at a Codex-local commit
  `abfb739` that is not in this repository. Re-running reproduces every stored
  number except `errors.phase`, which the current pilot takes over all
  harmonics m=0..3; that value equals [results/recheck.json](results/recheck.json).

## How this fits the repository

- **How it was checked here.** Four review passes by Claude agents (proof,
  reproduction, exact series, claims), each re-checked by a second agent,
  found no mathematical error. A few routine steps are only sketched (local
  existence, smoothness in b, the Galerkin wording); PROOF.md now cites
  standard sources for them or rewords them. They re-derived the b=0 base, the energy and comparison argument,
  the q-equations and their bounds, and the remainder equation. The
  computations behind the numbers quoted here are saved, with their logs, in
  [review/](review/README.md):
  - [`review/exact_b2_check.py`](review/exact_b2_check.py)
    ([log](review/exact_b2_check.log)) interpolates the repository's exact
    series (`../ns-phase-audit/audit_v2/exact/nsseries.py`, ν symbolic,
    through t¹⁰) exactly in b. Every coefficient of E, Z and S is even in b,
    (E2, Z2, S2)(0) = (1/4, 1/4, 0) exactly, and within the computed orders
    each |m| ≥ 2 harmonic first appears at the earliest order that PROOF.md
    section 5 allows. `response.py`'s E2
    and Z2 agree with the series to 13–15 digits for t ≤ 0.1, and its S2 to
    about 13 digits for t ≤ 0.05; at t = 0.1 its S2 differs by 1.1e−12, less
    than the last series term (3.6e−12).
  - [`review/audit_t1_check.py`](review/audit_t1_check.py)
    ([log](review/audit_t1_check.log)): the variational Z2 cos 2φ coefficient
    at T=1 (Laurent −1.207722e−3) matches the finite-β DNS of
    [AUDIT.md](../ns-phase-audit/audit_v2/AUDIT.md) §4.3, extrapolated to
    β→0, to 4.5e−7 relative, as close as the 7 printed digits of the audit's
    log allow (same `dns/ns.py` discretisation, different method).
  - [`review/radius_ceiling.py`](review/radius_ceiling.py)
    ([log](review/radius_ceiling.log)): the ceiling of 7.2×10⁻²² on the
    radius, explained in PROOF.md section 2.
- **What the numerics test.** A ratio near 16 is what any smooth response that
  is even in b gives once its b² coefficient is right. So it checks the
  E2/Z2/S2 formulas and the q1/q2 code on finite grids at T=0.5 (νT≈0.018).
  It does not test the radius, the decay rates, uniformity in φ or the cubic
  field claim (q3 is not computed). Run further at b=0.1/0.05, the ratio stays
  within 0.05% of 16 up to t=1 and within 2.4% at t=2 on a 32³ grid (5.2% on
  24³), but leaves the 14–18 window by t=4 on both grids (Z 18.0–18.2,
  S 13.6–13.7; [review/longtime_ratio.py](review/longtime_ratio.py),
  [log](review/longtime_ratio.log)). That only says b=0.1 is no longer small
  there.
- **What it adds.** A written all-time paper proof (not refereed) of P1 at the
  solution level, for E, Z and S (PROOF.md sections 1 and 5; the same argument for Z is in
  [enstrophy-jet/RESULTS.md](../ns-phase-audit/enstrophy-jet/RESULTS.md)
  §4.2). Evenness in b matches the audit's "#β even", and the b² response is
  consistent with Rule B. It is a statement uniform in time, next to the
  repository's exact series, which is exact at t=0 but of no use at t ≥ 2
  ([enstrophy-jet/RESULTS.md](../ns-phase-audit/enstrophy-jet/RESULTS.md) §6).
- **What it leaves open.** Every b=1 item: no remainder bound for the time
  series, no reach to t≈2 at b=1, and no continuum estimate for the b=1
  Galerkin results ([AUDIT.md](../ns-phase-audit/audit_v2/AUDIT.md) §7.1,
  §7.2).

## Remaining limits

The theorem is a paper argument, not formal verification. Constants have not
been optimized or evaluated with certified quadrature, truncation and infinite-
time tails. Numerical evidence stops at T=.5 and finite spatial/phase grids.
There is no continuum a-posteriori certificate, fourth-variation numerical
solver, long-time convergence study, or proof of exact finite phase bandwidth.
The source hashes distinguish the preserved first pilot from the subsequently
parameterized pilot CLI. The computation and proof address only this family,
and only |b| below a radius that is never computed and is far smaller than any
simulated b (PROOF.md section 2). For what this is not (b=1, the Millennium
problem) and the classical results it is an instance of, see PROOF.md, "What
this is not, and where it sits".

## Review by separate AI reviewers (Codex workflow)

As far as the delivery shows, these reviewers were other AI agents in the same
ChatGPT/Codex workflow, not referees, and none of them reran the exact-jet test
or any full solve.

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

The added bounded check is reproducible. It writes a new file and keeps the
archived JSON:

```sh
python3 -I -B check_observable_remainder.py --output results/observable_remainder.rerun.json
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
