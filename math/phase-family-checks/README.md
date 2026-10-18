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
70 percent above the finite-time value.

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

## Files

- `check_p1.py`: the three β = 0 checks.
- `v2/ns3d.py`: the strictly dealiased pseudo-spectral solver (Lawson RK4).
- `v2/rerun_all.py`, `v2/results.json`: the T = 1 sweep and the long-time table.
- `v2/check_T05.py`, `v2/check_T05.json`: comparison with Codex's variational response.
- `compliance/ls_repro.py`: the compliance-table reproduction; run from the
  repository root as `python3 math/phase-family-checks/compliance/ls_repro.py .`

Run times on four cores: `check_p1.py` about 20 s, `rerun_all.py` about 8 min,
`check_T05.py` about 1 min, `ls_repro.py` about 1 min.

## What this does not show

No regularity boundary in b, no bound valid at b = 1, no continuum
certificate for any computed number (the audit's §7.1 route has not been
run), and nothing about the inviscid b ≠ 0 problem.
