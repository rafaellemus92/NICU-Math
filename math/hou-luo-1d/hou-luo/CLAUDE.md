# Hou–Luo blowup lab — project brief for Claude Code

## What this project is
A learning lab, run by Rafael (neonatologist, math undergrad, fractal geometry
background), for building intuition about finite-time blowup in fluid
equations, the question at the heart of the Navier–Stokes Millennium problem.

The vehicle is the **1D Hou–Luo model**, a caricature of the flow on the wall of
a swirling pipe flow, which is the setting of the rigorously proven 3D Euler
blowup (Chen & Hou):

    omega_t + u omega_x = theta_x + nu    omega_xx
    theta_t + u theta_x =           kappa theta_xx
    u_x = H(omega)              (Hilbert transform), x in [-1/2, 1/2) periodic

Initial data: omega0 = 0, theta0 = 1 - cos(2 pi x). The singularity forms at the
stagnation point x = 0.

## Ground rules (read before every task)
1. **This is a toy. Nothing here is evidence about the 3D Navier–Stokes
   equations.** Never write a summary, comment, or plot title that implies
   otherwise. "Observed in this 1D model at these parameters" is not "proven".
2. **No numerical claim without a resolution check.** Before reporting a number,
   rerun at 2N (and a smaller tolerance where relevant) and show they agree.
   A uniform grid cannot follow a true singularity; say where a run stopped
   and why.
3. **Verify every citation** by searching before relying on it. Don't invent
   papers or exponents from memory.
4. Rafael wants rigorous pushback, not validation. If an idea won't work, say
   so plainly and say why.
5. Explain PDE concepts plainly. Use physiological analogies only when they are
   accurate, and flag where an analogy breaks.

## Files
- `hou_luo.py` — solver (pseudo-spectral in x, Lawson integrating-factor RK4,
  adaptive dt, Hou–Li filter). `python hou_luo.py --help`.
- `plot_results.py` — the three-panel figure.
- `hou_luo_results.json` / `.png` — baseline outputs (N = 8192).
- `step1_adaptive.py` — Step 1 solver: inviscid model on an adaptive
  (analytically stretched, remeshed) grid with the exact Hilbert transform on
  the stretched grid. `step1_tests.py` is its validation ladder,
  `step1_plot.py` draws `step1_reciprocal.png`, `step1_plan.md` is the plan,
  method, ground-rule check and results table.
- `step1_N*.json/.npz/.log`, `step1_results.json` — Step 1 outputs.

## Baseline results (N = 8192 unless noted)
- **Inviscid (nu = 0):** faster-than-exponential growth; max|omega| reaches
  ~9.4 at t ~ 0.761 before the grid loses resolution (N = 16384 reaches ~11.5 at
  t ~ 0.778). N = 8192 and 16384 agree to 6 digits wherever both are resolved.
- The reciprocal-plot fit gives T ~ 0.90, but the fit window (max|omega| from 4.7
  to 9.4) is **before** the asymptotic regime, so treat it as unreliable. The
  viscous runs peak near t ~ 0.84–0.86, which suggests the true T is lower.
- **Viscous sweep, nu = 3e-3 … 3e-5:** every run peaks and decays. The peak
  rises as nu falls: peak max|omega| ~ nu^(-0.19) over two decades. Converged
  (nu = 3e-5 at N = 8192 vs 16384: peaks agree to 8 digits).

## Step 1 results (2026-10-16, adaptive mesh, see step1_plan.md)
- Inviscid run followed to max|omega| = 1e4 (t = 0.844444), smallest cell
  1e-14, spectral tail never above 3e-10. Numerically converged: N = 2048 …
  16384, halved dt, two remesh rules and three map steepnesses agree on T to
  1e-9. Every run stopped because it reached the target, not for resolution.
- **T = 0.844513, p = 1.000 ± 0.001, c = 3.000 ± 0.003** over max|omega| from
  1e3 to 1e4. The ± is the fit-model systematic (straight line with p fixed
  at 1 gives T = 0.8445131, p = 1.0002, c = 3.0007; a free-exponent fit gives
  T = 0.8445129, p = 0.9993, c = 2.9977); it is far larger than the numerical
  error and was found by an independent audit, not by the refinement ladder.
- Consistent with the published exponent lambda = 2.99870 ± 6e-5 (Chen, Hou &
  Huang, Annals of PDE 2022, Theorem 1, doi:10.1007/s40818-022-00140-7, as
  quoted by a citation-checking agent; read it directly in Step 2).
- The baseline's T ~ 0.90 and c ~ 4.3 were pre-asymptotic artefacts. Local
  fits of T converge only once max|omega| > ~100.
- Rescaled profiles omega/max|omega| vs x/x* collapse onto one curve from
  max|omega| = 16 to 8e3 (x* shrinking by 1e9): the blowup looks self-similar,
  which is what Step 2 will compute directly.
- Double-precision ceiling of this method: theta_x = theta_alpha/rho amplifies
  round-off by 1/h_min; the noise floor (1e-10 at max|omega| = 1e4) would reach
  the 1e-6 stop near max|omega| ~ 1e5. Dynamic rescaling avoids it.

## Roadmap
**Step 1 — DONE (see above). Original goal:** follow the inviscid singularity further. The uniform grid stalls
at max|omega| ~ 10. Goal: reach max|omega| >= 1e3 with a converged run, then show
1/max|omega| is linear in t and the T estimate is stable under refinement.
Options: (a) a time-dependent mesh map that concentrates points near x = 0
(Luo & Hou's approach), where the Hilbert transform must be computed on the
mapped grid; (b) skip ahead to Step 2, which sidesteps the problem.

**Step 2 — Dynamic rescaling.** Rescale space and time around x = 0 so the
blowup becomes a steady profile (the formulation Chen & Hou used to make the
proof computer-assisted). Find the self-similar profile and the length-scale
exponent c, where width ~ (T - t)^c. Compare with published values once you've
found and verified the source.

**Step 3 — Does viscosity always win in this toy?** Hypothesis to test, not a
fact: near blowup, viscous/inertial ~ nu (T - t)^(1 - 2c), so if c > 1/2 viscosity
eventually dominates at any nu > 0. Check it against Step 2's c, extend the nu
sweep downward with resolution checks, and plot nu * max|omega_xx| / max|theta_x|
over time. Then explain why this argument does **not** carry over to 3D
Navier–Stokes. In 3D, the equation's own scaling fixes the relationship, and the
problem is supercritical.

**Step 4 (optional) — Read the formal statements.** Look at how blowup is stated
in Lean in the public Navier–Stokes formalization, as a reading exercise.

## Conventions
- Python 3 + numpy + matplotlib only, unless a step clearly needs more.
- Keep figures phone-friendly: tall, stacked panels, large text.
- Save each new experiment as its own script (`step1_*.py`, …) with its own
  JSON output; don't break `hou_luo.py`'s baseline.
