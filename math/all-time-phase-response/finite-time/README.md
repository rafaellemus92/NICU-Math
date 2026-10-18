# finite-time: a certified bound on the enstrophy error beyond the b² response

Owner: Claude (session "Navier Stokes-Speech"), 18 October 2026. Base: main `2b14eeaa`.
Branch `claude/enstrophy-finite-time-bound`. Scope: one bounded mathematical task
(docs/HANDOFF.md, "Finite-time enstrophy error bound"); nothing else in the repository
is changed, and no archived result is modified.

- [NOTE.md](NOTE.md): the mathematics. Section 1 extracts the constants of
  [../PROOF.md](../PROOF.md) and names its largest loss (the Sobolev level s ≥ 4 applied to
  the sheared base flow). Sections 2–5 prove, for ν > 0 and any horizon T, with every
  constant explicit:
  - a certified admissible radius β₁(T) (Proposition 1) below which the solution is smooth
    on [0, T], obtained at the enstrophy (H¹) level with one Agmon constant and
    maximum-principle bounds on two derivatives of the base flow;
  - |Z(u_b) − Z(U) − b² Z2| ≤ C_Z(T) b⁴ on [0, T] for |b| < β₁(T) (Theorem, Section 5),
    through the mean/oscillating decomposition and the k_z parity of the coefficients.
- [constants.py](constants.py): evaluates every constant as an upper bound of its definition
  (upper Riemann sums, monotone factors at their worst cell endpoint, certified Agmon
  constant) in validated interval arithmetic: decimal endpoints of 40 digits with directed
  rounding, square roots verified by exact squaring, exponentials from a Taylor polynomial with
  an explicit remainder, cancellation and nesting enclosed, and the maximal enclosure width
  printed as the rounding budget (3×10⁻³¹). Admissible radii are printed rounded down and error
  constants rounded up, so every printed number is a valid bound; the supported parameter range
  (ν > 0, T > 0, |c| + |d| ≥ ν) is enforced. [results/constants.log](results/constants.log) is
  its output at a = c = d = 1, ν = 1/28 exactly, for T ∈ {0.1, 0.25, 0.5, 1}.
- [check_bounds.py](check_bounds.py): full nonlinear solves on the repository's solver
  (N = 24, dt = 0.005, T = 1, φ = 0.37, b = 10⁻³, 10⁻² and 0.05) measuring the quantities the
  chain bounds — ‖∇v‖/|b|, ‖∇v̄‖/b², ‖∇ẽ₂‖/|b|³, ‖ē₂‖/b⁴, R_Z/b⁴ — against the bounds,
  the exact six-term identity of Section 5, and the base-flow derivative bounds of Section 2
  against a fine one-dimensional solve. [results/check_bounds.log](results/check_bounds.log).
  These are consistency checks (every bound exceeds its measurement), not certificates: the
  solves carry no validated error and are sampled every 0.05 in time; b = 10⁻² and 0.05 lie
  outside every certified radius and b = 10⁻³ inside it at T = 0.25 (hence for every T ≤ 0.25) but
  not at T = 0.5, 1, so the comparison
  is with the b → 0 limits of the scaled quantities; and a check passed by factors of
  10⁵–10⁴⁰ cannot detect a moderate error in a late constant. Table C (G₁, D₁ replaced by
  measured linear quantities) is a what-if for this particular majorant, not a radius and not
  a lower bound on other estimates.
- [results/lattice_sums.log](results/lattice_sums.log): certified bound of the lattice sum
  Λ₄ = Σ_{k≠0}|k|⁻⁴ (partial sum plus an integral tail bound), hence of C_A = Λ₄^{1/2}.

Headline (from the logs): the certified finite-time radius is between 8×10¹⁵ (T = 1) and
4×10¹⁸ (T = 0.1) times the all-time ceiling (1.08×10⁻³ at T = 0.25 against 7.2×10⁻²²), but
C_Z is 10¹⁶–10⁴⁰ above the measured remainder; the single obstructing estimate, the one
proposed improvement and the nonlinear remainder estimate it still needs (a certified H¹ bound
on v − bq₁) are in NOTE.md §7. Nothing here concerns b = 1 or regularity in general.

Independent review: one targeted reviewer (a separate agent of the same session) re-derived
every step of NOTE.md Sections 2–5, checked (I3)–(I4) and the Section 5 identity numerically,
solved Lemma 2's inequality independently (G₁, D₁ agree with constants.py to 10⁻⁵–6×10⁻⁴
relative) and reproduced the measurements; verdict: the theorem holds as stated with the
constants as evaluated. Its eight minor/nit findings (the mechanism claimed for the
"improvement", the b = 10⁻² caveat, the six-term identity check, monotone m_Δ, incremental
loss ratios, the rounding error budget, and wording) are applied in the second commit of the
branch.

A read-only audit of that commit (bfbe2b0) asked for: directed rounding of the printed radii
(down) and constants (up) with the strict inequality kept; either a complete validated error
budget or the weaker label "numerical estimates of analytic bounds", with the supported
parameter range enforced; removal of the claim that validated linear q₁ norms alone give a
larger nonlinear radius, with the missing remainder estimate stated; Table C's 10¹¹ excess
described as a result for that majorant, not a lower bound on improvements; and the statement
that b = 10⁻³ is outside the computed radius at T = 0.5 and 1 and that saved samples certify
nothing between times. The third commit applies all of it; the validated budget was chosen
over the weaker label (interval arithmetic in constants.py), no solve was re-run
(check_bounds.py re-renders from the saved measurements), and one targeted reviewer checked
the correction (verdict: all five items met, nothing blocking; its two cosmetic directed-rounding
findings on printed cross-check values and eight nits are applied in the fourth commit).

Run from this folder (Python 3 and NumPy; the check needs the repository solver two levels up):

```sh
python3 -I -B lattice_sums.py > results/lattice_sums.log      # about 6 s; certifies C_A
python3 -I -B constants.py > results/constants.log            # about 90 s (interval arithmetic, n = 20000)
python3 -B check_bounds.py > results/check_bounds.log         # about 15 s of N = 24 solves + 2 min of bounds
python3 -B check_bounds.py --from-json results/measurements.json > results/check_bounds.log   # no solve; bounds only
```

`lattice_sums.py` was written by a helper agent of the same session (its tail-bound argument is
in its docstring and was checked here); the other files are by the session itself.
