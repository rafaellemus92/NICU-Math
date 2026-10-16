# Step 1 plan — follow the inviscid singularity past max|ω| = 1000

Written before the Step 1 code. Status notes at the bottom are filled in as the
work proceeds.

## 0. Baseline reproduced (2026-10-16)
`python hou_luo.py --check` reproduces `hou_luo_results.json` to every printed
digit (inviscid N=8192: max|ω| = 9.433 at t = 0.761169, T_fit = 0.90395,
p = 1.016, c = 4.318; viscous peaks 4.954 / 6.283 / 7.880 / 9.616 / 11.99,
exponent −0.190; N=16384 reaches 11.45 at t = 0.778). Note the fitted T drifts
with N (0.926 → 0.904 → 0.881): the fit window is pre-asymptotic, as CLAUDE.md
says.

## 1. Why a uniform grid cannot do it
Calibration on the uniform solver at the moment its tail criterion fires:
the |ω| peak sits ~17 cells from x = 0 and the spectral analyticity width
δ (from the decay rate of |ω̂_k|) is ~7.6 cells, i.e. δ ≈ 0.45 x*. Between
max|ω| = 7.6 and 9.4 the width fell 2.3×, i.e. width ∝ max|ω|^(−3.9) locally.
Going from 9.4 to 1000 shrinks the inner scale by ~10^8 (10^6 even if the
asymptotic exponent is 3). No uniform grid gets there. Moving the points is
the only option; dynamic rescaling (Step 2) is the other, and is deferred as
the roadmap asks.

## 2. Method: analytic mesh map + exact Hilbert transform on the mapped grid
**Coordinates.** Uniform computational grid α ∈ [−1/2, 1/2), physical
x = x(α) with x' = ρ(α) > 0, ρ even, periodic, analytic, ∫ρ = 1. The map is a
periodic sinh-type map:

    ρ(α) ∝ z/(1+z),   z = r · cosh(L · sin(πα)/π)

Near α = 0 the cell size is ≈ r/N (a plateau ~N/L cells wide), then it grows
geometrically with N/L points per e-fold of |x| (the "ramp"), and saturates at
≈ 1/N in the far field. Only r changes with time; L is fixed so that N and 2N
runs use the *same* map and differ only in the number of points. The design
rule is cell size ≤ 0.45·|x|/18 (from §1), i.e. N/L ≥ 40 cells per e-fold.

**Equations in α.** With w(α,t) = ω(x(α),t), ϑ = θ(x(α),t):

    w_t = −(u/ρ) w_α + ϑ_α/ρ,     ϑ_t = −(u/ρ) ϑ_α

**Hilbert transform (the hard part).** Hω(x) = PV ∫ ω(y) cot(π(x−y)) dy is not
a convolution in α. Split off the α-grid Hilbert transform:

    Hω(x(α)) = H_α w(α)  +  ∫ w(β) K(α,β) dβ,
    K(α,β) = ρ(β) cot(π(x(α)−x(β))) − cot(π(α−β)),   K(α,α) = −ρ'(α)/(2πρ(α))

H_α is an FFT; K is smooth (removable singularity on the diagonal), so the
trapezoid rule on the uniform α grid is spectrally accurate. K is a dense
N×N matrix that depends only on the mesh, so it is built once per mesh and
applied by BLAS matvec. Odd symmetry of ω halves each dimension (N/2 × N/2).
u_x = Hω, then u from u_α = u_x ρ by FFT integration with u(0) = 0.

**Time stepping.** RK4 (Lawson reduces to RK4 at ν = 0), Hou–Li filter in α,
dt = min(cfl/(N max|u/ρ|), 0.05/max|ω|, 0.05/√max|θ_x|, 1e−2). Fields are
projected onto the odd/even symmetry class after each step (removes round-off
asymmetry only; the exact solution is in that class).

**Remeshing.** The mesh is static between remesh events (so K is reused).
Trigger: the |ω| peak is closer than 48 h_min to x = 0. New r puts the peak at
192 h_min. Interpolation old → new grid is by evaluating the trigonometric
interpolant of w and ϑ at the new points (spectral accuracy; the solution is
resolved to ~1e−12 at that moment by construction). The x(α) values are
computed by cumulative Gauss–Legendre quadrature of ρ outward from 0, so x is
accurate *relative to its own size* near 0 (an FFT antiderivative would carry
an absolute 1e−16 error that would swamp x ~ 1e−12).

**Stop.** Stop when max|ω| reaches the target, or when the α-spectral tail
(energy fraction at k > N/4) exceeds 1e−6 (the baseline's "unresolved" rule),
or when dt underflows relative to t.

**Known limit (as planned).** u near x = 0 comes from an FFT antiderivative
with absolute error ~1e−16; I estimated this would matter at max|ω| ~ 3e4.
*Measured afterwards (§6): it does not* — the FFT u agrees with a local
quadrature to 1.5e−8 at the spike at max|ω| = 1e4. The real double-precision
ceiling is elsewhere: θ_x = θ_α/ρ divides the FFT derivative of an O(1)
function by ρ(0) ~ 1e−10, giving a white noise floor ~eps·π/h_min in θ_x,
i.e. ~1e−10 relative at max|ω| = 1e4 and ~1e−6 (the stop criterion) near
max|ω| ~ 1e5. Dynamic rescaling (Step 2) has no such problem.

## 3. Validation ladder (ground rule 2)
1. Hilbert transform on a strongly stretched mesh vs. analytic H of
   (a) sin(2πkx) and (b) the periodic Lorentzian-like spike
   g = sin(2πx)/(cosh η − cos 2πx), Hg = 1 − sinh η/(cosh η − cos 2πx),
   with η = 1e−6 (spike width 1.6e−7). Expect ~1e−13.
2. Uniform map (ρ ≡ 1, K ≡ 0): must reproduce hou_luo.py's max|ω|(t) to
   round-off. Mildly stretched map: must agree with the baseline to ~1e−8
   while the baseline is still resolved (t < 0.74 at N = 8192).
3. Production: N = 4096, 8192, 16384 with the same L. Compare max|ω|(t),
   T estimates and p, c. Halve cfl at one N. Change the remesh factor at one N.
4. Report where each run stopped and why, and the max spectral tail it ever had.

## 4. Diagnostics for the deliverable
- Reciprocal plot: 1/max|ω| vs t, N and 2N overlaid, with the late-window
  linear fit and T. Residuals of the fit.
- Local blowup-time estimate T_loc(t) = t + max|ω| / (d max|ω|/dt): must
  flatten to a constant if max|ω| ~ (T−t)^(−1).
- Growth exponent p and width exponent c from the last decade(s).
- ω(x) snapshots on a log-|x| axis to show the self-similar narrowing.
Figure: tall stacked panels, large text (CLAUDE.md conventions).

## 5. Ground-rule check
1. Toy model: every title, caption and summary says "1D Hou–Luo model".
   Nothing about 3D Navier–Stokes is inferred.
2. Resolution: N vs 2N at fixed map, plus time-step and remesh-rule checks,
   all before any number is quoted. Each run's stop reason is reported.
3. Citations: verified by search on 2026-10-16 —
   Luo & Hou, "Potentially singular solutions of the 3D axisymmetric Euler
   equations", PNAS 111(36) 2014, doi:10.1073/pnas.1405238111 / arXiv:1310.0497 (adaptive moving meshes,
   3×10^8-fold vorticity growth); Hou & Luo arXiv:1311.2613 (the 1D model);
   Choi, Hou, Kiselev, Luo, Šverák & Yao, CPAM 70(11) 2017, 2218–2243 /
   arXiv:1407.4776 (blowup proof for the 1D model); Chen, Hou & Huang,
   Annals of PDE 2022 / arXiv:2106.05422 (asymptotically self-similar blowup;
   abstract: θ bounded in C^γ, γ ≈ 1/3). The value "c ≈ 3" quoted later is
   *derived* from γ ≈ 1/3 and the scaling relations, not read off a paper.
4. Pushback: the baseline's c ≈ 4.3 and T ≈ 0.90 are not trusted (fit window
   pre-asymptotic, drifts with N). Expect both to change.
5. Plain explanations in the write-up; analogies only where exact.

## 6. Status (2026-10-16) — Step 1 done
Validation ladder: (1) Hilbert transform on a 1e5:1 stretched mesh correct
to 2e−15 for smooth and spike test functions; (2) uniform map reproduces
hou_luo.py to 3e−12 (same step count, same dt); stretched N = 4096 and 8192
agree with uniform N = 16384 to 5e−11 in max|ω| and both L2 norms up to
t = 0.70 (`python step1_tests.py`, all pass).

Production (`step1_adaptive.py`, L = 128, target max|ω| = 1e4; every run
stopped because it *reached the target*, none for loss of resolution):

| run | max|ω| at stop | t at stop | T (last decade) | p | c | tail_max | remeshes |
|---|---|---|---|---|---|---|---|
| N = 2048 (16 cells/e-fold, stress test) | 10062 | 0.844444 | 0.8445131 | 1.0002 | 3.000 | 5e−8 | 16 |
| N = 4096 | 10070 | 0.844445 | 0.8445131 | 1.0002 | 3.001 | 2.7e−10 | 15 |
| N = 4096, dt halved | 10035 | 0.844444 | 0.8445131 | 1.0002 | 3.001 | 2.3e−10 | 15 |
| N = 4096, remesh at 64 cells | 10035 | 0.844444 | 0.8445131 | 1.0002 | 3.001 | 3.1e−10 | 13 |
| N = 4096, L = 96 | 10041 | 0.844444 | 0.8445131 | 1.0002 | 3.001 | 1.7e−10 | 16 |
| N = 4096, L = 192 | 10006 | 0.844444 | 0.8445131 | 1.0002 | 3.001 | 1.8e−10 | 15 |
| N = 8192 | 10030 | 0.844444 | 0.8445131 | 1.0003 | 3.001 | 2.3e−10 | 15 |
| N = 16384 | 10022 | 0.844444 | 0.844444FIT | 1.0002 | 3.001 | 0.844444AIL | 14 |

T agrees to 7 digits across every resolution, time step, remesh rule and map
steepness. Over the last two decades (max|ω| 100 → 1e4) the fit gives
T = 0.844516, p = 1.006: the approach to the 1/(T − t) law is still visible
at max|ω| ~ 100 and gone by 1000. The smallest cell at the end is 1e−14 and
the |ω| peak sits at x* ≈ 1e−12. Width ∝ (T − t)^3.001 (both width measures).

The baseline's T ≈ 0.90 and c ≈ 4.3 were artefacts of fitting before the
asymptotic regime, as suspected. c = 3 is what the Chen–Hou–Huang abstract's
"θ bounded in C^{1/3}" implies via the scaling relations (c_θ/c_l = 1/3,
c_l − c_θ = 2); Step 2 should check the published profile directly.

The T, p, c columns above are "model A" (straight line through 1/max|ω|,
then p and c against that T). See §7 for why that is not the whole story.

Outputs: `step1_N*.json/.npz/.log`, `step1_results.json`,
`step1_reciprocal.png` (figure: reciprocal plot, zoom, local-T convergence,
self-similar collapse).

## 7. Independent verification (same day) and what it changed
Three checkers were run that did not see the conclusions above, then two
skeptics per claimed defect.

**Blind re-fit from the raw .npz series** (numpy only): T = 0.8445130973
(N = 8192) and 0.8445130962 (N = 16384), p = 1.00025, c = 3.0007 — identical
to the table. It also found that the straight-line residual (8e−4) is not
scatter but smooth curvature, the same at both N: 1/max|ω| ≈ 1.451 τ (1 − 1.54 τ),
τ = T − t. A quadratic fit gives T = 0.8445130; sub-window straight-line fits
converge monotonically (max|ω| 5e3…1e4: T = 0.84451299, p = 1.000007).

**Code audit** (re-derived the kernel diagonal, checked H and u signs,
Fourier phase/Nyquist conventions, symmetry mirrors, remesh interpolation,
inverse map, RK4 vs the baseline's Lawson RK4, peak refinement — all correct
to round-off). One finding survived both skeptics: `blowup_fit` fixed T by
a p = 1 straight line and then measured p and c against that T, so p was
pulled toward 1 by construction (a synthetic p = 0.95 series is reported as
1.016). The bias is identical for every N, dt and remesh rule, so the
convergence ladder cannot see it. **Fixed:** `blowup_fit` now reports three
models and their spread; `step1_results.json` carries all of them:

| model (last decade, every run) | T | p | c |
|---|---|---|---|
| A straight line, p fixed at 1 | 0.8445131 | 1.0002 | 3.0007 |
| B quadratic in t | 0.8445130 | – | – |
| C free exponent (T, p both free) | 0.8445129 | 0.9993 | 2.9977 |

So the defensible statement is **T = 0.844513 (±1e−7 from the fit model;
±1e−9 from the numerics), p = 1.000 ± 0.001, c = 3.000 ± 0.003**. Two
minor fixes from the same audit: rows the grid did not resolve are excluded
from fits (never occurred in the reported runs), and the duplicate history
row written at each remesh is gone.

**Citations:** all four verified with DOIs (the PNAS title corrected above).
The checker also found the published exponent: Chen, Hou & Huang 2022,
Theorem 1, as quoted by the checker: λ = c_l/|c_ω| = 2.99870 ± 6e−5 and
γ = 0.33304 ± 2e−5, with the dynamic-rescaling steady state c̄_l = 3,
c̄_ω ≈ −1.00043. Our c = 3.000 ± 0.003 is consistent with λ = 2.9987; the
difference (1.3e−3) is inside our fit-model spread, so Step 1 cannot
distinguish 3 from 2.9987. Step 2 should read Theorem 1 directly and compute
the profile.
