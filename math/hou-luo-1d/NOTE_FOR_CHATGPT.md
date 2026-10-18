# What this is

The code and raw outputs behind the Hou–Luo charts. It is copied unchanged from
`github.com/rafaellemus92/NICU-Module`, branch `claude/peaceful-wozniak-oaprql`,
folder `hou-luo/`, at commit 8cb11e6.

**It is the 1D Hou–Luo model, not a 3D computation.** We searched every Claude
session and artifact on this account. There is no 3D strip-fitting code, no
3D spectra, and no fitted law of the form `S ≤ C Z^0.75 D^0.2`.

The "width → 0" and "grid gives up" panels are these:

- `baseline_check.png` (uniform grid, `hou_luo.py`): panel A marks where the
  uniform N = 8192 grid can no longer follow the spike (max|ω| ≈ 9.4 at t ≈ 0.761).
- `step1_reciprocal.png` (adaptive mesh, `step1_adaptive.py`):
  1/max|ω| goes linearly to zero at T = 0.844513. Rescaled profiles collapse,
  with peak position x* ∝ (T − t)^3.001.

## Where each number lives

| What | File |
|---|---|
| Analyticity-width (strip) diagnostic on the uniform grid, δ ≈ 7.6 cells when it stops | `baseline_check.log` / `.json` |
| Run outputs: raw states and series | `step1_N*.npz` |
| Fit numbers | `step1_N*.json` |
| Step logs | `step1_N*.log` |
| Fit-model systematics: T, p, c with spreads | `step1_results.json` |
| Plan, method and the ground-rule check | `step1_plan.md` |
| Validation ladder | `step1_tests.py` |

Only the N = 4096, 8192 and 16384 `.npz` files are in git; the variant runs
keep their numbers in `.json`.

## Caveats, as the lab's own `CLAUDE.md` states them

- **A toy model.** Nothing here is evidence about 3D Navier–Stokes.
- **Grid exhaustion.** It means loss of resolution, not a singularity.
- **What the exponent comparison covers.** c = 3.000 ± 0.003 is compared with
  λ = 2.99870 from Chen, Hou & Huang (Annals of PDE 2022). That result concerns
  this 1D model.
- **Chen–Hou.** Their 3D result is for inviscid axisymmetric Euler with a
  boundary, a different problem from periodic viscous Navier–Stokes.
