# Phase-family checks: the β = 0 reduction, the b² response and the compliance table

**Status: Checked numerically.** The analytic argument for the β = 0 reduction
was reviewed here and is written out by Codex in
[`../all-time-phase-response/PROOF.md`](../all-time-phase-response/PROOF.md);
nothing in this folder is a proof or a Lean artefact. Labels follow
[`../README.md`](../README.md) ("Status labels").

Owner of this folder: Claude (session of 18 October 2026). The scripts need
only NumPy; each one writes or prints its own numbers. All runs use the
periodic box `[0, 2π]³`, torus averages, and the family

    u₀ = (a sin y, b sin z, c cos x − d cos(x + y + φ)),   a = c = d = 1, ν = 1/28

unless stated. `E = ½⟨|u|²⟩`, `Z = ½⟨|ω|²⟩`, `S = ⟨ω_i ω_j ∂_j u_i⟩`.
Phase harmonics are reported as cosine coefficients `A_m = 2 Re ĥ_m` of the
Fourier series in φ (the audit's convention is half of this).

## What was checked

| Claim | Script | Result | Status |
|---|---|---|---|
| β = 0: the flow is 2½-dimensional, every x-averaged quadratic quantity has phase harmonics of order ≤ 1, no sine term; inviscid `Z = (a²+c²+2d²)/4 + acd t cos φ/4 + a²t²(c²+d²)/8` | [`check_p1.py`](check_p1.py) | formula vs quadrature to 4e-15; viscous reduction: sine and m ≥ 2 harmonics at 1e-17; full 3D run vs reduction to 1e-12 | Checked numerically; argument reviewed (closes AUDIT.md §7.5 "P1 at the solution level") |
| b ≠ 0, T = 1: `c₂(Z)/b²` and `c₂(S)/b²` tend to constants as b → 0 | [`v2/rerun_all.py`](v2/rerun_all.py) | see table below; agrees with the audit's −1.2075e-3 (half-coefficient convention) to four figures | Checked numerically |
| The b² constant grows with T and the quadratic law loses accuracy | [`v2/rerun_all.py`](v2/rerun_all.py), 16 phases | see table below | Checked numerically |
| Codex's second-order response at T = 0.5 (`../all-time-phase-response`) | [`v2/check_T05.py`](v2/check_T05.py) | b → 0 extrapolation of `(O(u_b) − O(U))/b²` from a different solver reproduces their variational `E2, Z2, S2` at all 12 phases to six figures | Checked numerically |
| Compliance table of PR #17: range descriptor, least-squares C and R | [`compliance/ls_repro.py`](compliance/ls_repro.py) | reproduced from the generator; R bias is regression dilution | Checked numerically |

## Numbers

T = 1, N = 32, dt = 0.01, 8 phases (strict 2/3 cutoff K = (N−1)/3):

| b | c₂(Z)/b² | c₂(S)/b² |
|---|---|---|
| 0.05 | −2.41478e-3 | −1.25158e-2 |
| 0.10 | −2.41319e-3 | −1.25049e-2 |
| 0.20 | −2.40686e-3 | −1.24612e-2 |
| 0.40 | −2.38164e-3 | −1.22889e-2 |

The leading Taylor term `−(6487/1555200) a²b²c²d² t⁶` gives −4.17e-3 at t = 1,
70 percent above the finite-time value. The b → 0 limit of `c₂(Z)/b²` at T = 1 by
Richardson extrapolation from b = 0.05 and 0.1 is −2.4153e-3, which agrees with
the variational coefficient of the Codex package (−2.41531e-3 at N = 30) to 1e-5;
the b = 0.05 value quoted earlier in the session was not yet the limit.

Long time, N = 24, dt = 0.02, 16 phases:

| T | c₂(Z)/b², b = 0.1 | c₂(Z)/b², b = 0.2 | c₂(S)/b², b = 0.1 | c₂(S)/b², b = 0.2 |
|---|---|---|---|---|
| 1 | −0.0024 | −0.0024 | −0.0125 | −0.0125 |
| 2 | −0.0609 | −0.0601 | −0.1262 | −0.1249 |
| 4 | −0.384 | −0.346 | −0.550 | −0.546 |
| 8 | +1.062 | +0.349 | +0.079 | +0.207 |

At T = 8 the two amplitudes no longer scale together. Independent small-b runs
(b = 0.00625 and 0.0125, by a referee in the same session) put the b → 0
limit at `c₂(Z)/b² = 1.114 ± 0.002` and `c₂(S)/b² ≈ −3.0`, so at T = 8 the
quadratic law holds to 10 percent only for |b| below about 0.03, the b = 0.1
value is close by accident, and the S entry at b = 0.1 has the wrong sign as
an estimate of the leading coefficient. This is a statement about the accuracy
of a truncated expansion in a smooth parameter. All computed flows are smooth
and decaying through T = 8 at converged resolution; that is numerical evidence
for regularity of the PDE solutions, not a proof, and it says nothing about a
stability boundary in b.

The mechanism is transient amplification: the difference field `u_b − u₀` grows
by up to 13× in L² and 28× in H¹ while the base flow decays faster, so
`‖u_b − u₀‖/(b‖u₀‖)` reaches about 11 at T = 8 and 30 at T = 24. Nonlinear
corrections scale as the square of b times that ratio.

Two cautions about our own numbers, found during review:

- An earlier run used six phases, where the m = 4 harmonic aliases onto m = 2;
  it moved the T = 8, b = 0.2 value from 0.35 to 0.40. Use at least 8 phases at
  T ≤ 4 and 16 at T = 8.
- The first solver used the cutoff `K = N//3`, which for N divisible by 3
  leaves the outermost retained shell aliased. The present scripts use
  `K = (N−1)//3`. The T = 1 numbers did not change to six figures.

## The compliance table

[`compliance/ls_repro.py`](compliance/ls_repro.py) runs the PR #17 generator
(`navier_stokes/ventilator_ingest.py`: pressure noise 0.05 of the swing, flow
noise 0.05 of peak flow, both independent per sample; volume is the cumulative
integral of the noisy flow; square-wave pressure control with inspiration 35
percent of the cycle). With midpoint-aligned volume, seed 42 and 50 breaths:

| noise, Hz | range descriptor | least-squares C | least-squares R (true 80) |
|---|---|---|---|
| 0, 100 | 0.998 | 0.9996 | 80.03 |
| 0.05, 100 | 0.861 | 1.008 ± 0.052 | 76.91 |
| 0.05, 1000 | 0.772 | 0.999 ± 0.015 | 76.39 |
| 0.10, 100 | 0.772 | 1.022 ± 0.100 | 68.71 |

Forty-seed ensemble means for R: 76.86, 76.49 and 68.75. The R bias is
errors-in-variables attenuation by `R·s/(1+s)`, `s` the ratio of flow-noise
variance to the variance of flow residualised on volume; the prediction from
the noiseless signals is 76.72, 76.46 and 68.31. The bias scales with the
noise variance (s from the 0.05 row predicts a bias of 11.1 at 0.10; observed
11.2) and does not depend on the sampling rate for fixed per-sample noise.
Fitting with left-edge volume against interval-averaged pressure and flow adds
`dt/(2C)` to R, which is 5 units at 100 Hz. C is protected because V and dV/dt
are orthogonal over a complete breath; the small positive residual is a
discretisation leak that shrinks with the sampling rate. The range descriptor
falls with noise through extreme-value inflation of the pressure range; the
extra drop at 1000 Hz comes from the volume numerator, whose random-walk noise
shrinks with the sampling rate.

A correction for R: multiply by `var(Q⊥)/(var(Q⊥) − σ_Q²)`, with `σ_Q²`
estimated from the high-frequency content of the flow. It is not identifiable
from the least-squares residual. Low-pass filtering the flow regressor alone
adds a structural bias; any filter must be applied identically to P, V and Q.

## Independent review of the all-time response package

Three referee agents in this session read `PROOF.md`, `README.md`, the code, the
results and the reused audit solver of
[`../all-time-phase-response/`](../all-time-phase-response/), tried to refute
them, and ran their own computations. Their scripts and outputs are in
[`review/`](review/); the scripts' paths were made relative to this folder after
the fact and the outputs are as produced. Verdict of all three: **sound with
corrections, no blocking error.**

Verified:

- The β = 0 base flow solves Navier–Stokes exactly; the H^j estimate and both
  e^{−νt} factors; the norm bookkeeping (F_s = 2^{(s−1)/2}, the (2+n²)^m weight);
  the three energy inequalities for integer s ≥ 4 (the cubic one needs
  ‖D²h‖_∞ ≤ C‖h‖₄, which is the reason for s ≥ 4); Poincaré with constant 1;
  the Riccati comparison, which is exact.
- The equations for q₁, q₂, q₃, the bounds with one derivative lost per level, the
  remainder equation, the estimate for e, the observable expansion with six
  stretching slots, and the translation parity. The b⁴ term is genuine:
  ⟨q₁,q₃⟩ = −2.76e-3 at T = 0.5.
- First numerical confirmation of the quartic field claim, which the note had
  left analytic: after subtracting b³q₃ the field remainder scales with ratio
  16.0, after b⁴q₄ with 32.0 (N = 18, T = 0.5, φ = 0.37).
- `response.py`'s convolution and `second()` agree with exact polynomial
  coefficients of the full right-hand side to 1e-14; the b² response agrees with
  the exact rational jet through t⁸; the T = 0.5 cos 2φ coefficients are
  reproduced by an independent small-b extrapolation to 5e-8 for Z and S.
- The spatial convergence chain N = 12 → 36 is clean spectral convergence
  (3.2e-4, 9.7e-7, 1.9e-9, 2.7e-12). Checksums, patch blobs and the quoted
  run times verify.

Corrections and caveats:

- **The certified radius.** With the note's own explicit majorant and a proved
  lower bound on the energy constant (K ≥ 0.1564 at s = 4, K ≥ 0.0762 at R = 8),
  condition (1) certifies at most |b| ≤ 10^(−1.4·10⁷⁰) for the all-time theorem
  and 10^(−1.3·10²⁷⁷) for the observable theorem. With the exact base-flow
  integral in place of the majorant, which overestimates it by 10⁶⁸ (m = 5) and
  10²⁷² (m = 9), the bounds are 10^(−160.6) and 10^(−63796). The order b⁴ is
  testable; the certified radius is not. No value such as 10⁻⁸⁰ is within reach
  of (1) under any reading.
- **What the factor-16 checks test.** The stacked RK4 system is the exact
  b-Taylor expansion of the discrete map, so the ratios 4, 8 and 16 are
  identities of any discrete map that depends smoothly and evenly on b. They
  test implementation consistency at T = 0.5, not the theorem, and their
  insensitivity to dt says nothing about continuum accuracy.
- **The short-time regime does not persist.** At φ = 0.37, N = 24 and 30, the raw
  remainder ratios for (E, Z, S) are (15.7, 16.8, 15.9) at T = 2, (17.6, 18.2,
  13.7) at T = 4 and (8.4, 15.3, 6.0) at T = 8; at T = 8, b = 0.1 the quartic
  remainder is 81 percent of the b² term for E. Z₂ grows from 0.32 at T = 0.5 to
  10.2 at T = 8 while Z(U) decays to 0.31, and E₂ turns negative. Nothing in the
  note is contradicted, since its evidence stops at T = 0.5 and its decay is
  asymptotic, but no decay is visible for t ≤ 8, and "exponential time decay"
  must not be read as observed.
- Of the nine tests, four are substantive (factorial convention, six stretching
  slots, z-support and parity, base reduction); the parity check is a tautology
  of the grid symmetry; the exact-jet test exercises the reused `nsseries.py`,
  not `response.py`.
- Provenance: three versions of `pilot.py` exist. The shipped one reproduces
  every stored number except the phase error (4.5e-12 with all harmonics against
  the stored 4.7e-15 from the earlier cos 2φ-only check); `observable_remainder.json`
  records an intermediate commit; `refined.json` lacks the full-solve parameters.
  The package README discloses most of this.
- Minor: the note's "Sobolev embedding controls first derivatives" should say
  second derivatives or cite Kato–Ponce; the shift-norm L and the majorant L_j
  share a letter; the (1+n²) weight fails the shift bound at n = 1 and the
  appendix's (2+n²) weight is the right one; "independent of the Galerkin
  cutoff" is true but unargued.
- On this folder's own numbers: the K = N//3 boundary aliasing of the first
  solver changes E, Z and the cos 2φ coefficient by at most 6.5e-5 relative at
  T = 1 and is sub-dominant to resolution at T = 8; the earlier numbers stand.

## Files

- `check_p1.py`: the three β = 0 checks.
- `v2/ns3d.py`: the strictly dealiased pseudo-spectral solver (Lawson RK4).
- `v2/rerun_all.py`, `v2/results.json`: the T = 1 sweep and the long-time table.
- `v2/check_T05.py`, `v2/check_T05.json`: comparison with Codex's variational response.
- `compliance/ls_repro.py`: the compliance-table reproduction; run from the
  repository root as `python3 math/phase-family-checks/compliance/ls_repro.py .`
- `review/`: the referee scripts and their outputs (`out/`); `run_pkg.sh` re-runs
  the package's own tests and pilots. Heavy scripts (`K_effect_full.py`,
  `late_time.py`, `true_base_norm.py`) take minutes.

Run times on four cores: `check_p1.py` about 20 s, `rerun_all.py` about 8 min,
`check_T05.py` about 1 min, `ls_repro.py` about 1 min.

## What this does not show

No regularity boundary in b, no bound valid at b = 1, no continuum
certificate for any computed number (the audit's §7.1 route has not been
run), and nothing about the inviscid b ≠ 0 problem.
