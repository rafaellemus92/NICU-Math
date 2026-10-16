import Mathlib

/-!
# Blow-up scalings: what the exponents imply

A candidate Navier–Stokes singularity at time `t_b`, written with
`τ = t_b − t → 0⁺` (from the slides): radial length `l_r ~ τ^{1/2}`, radial
speed `u_r ~ τ^{−1/2}`, swirl length `l_θ ~ τ^{1/2 − h}`, swirl speed
`u_θ ~ τ^{−(1/2 + h)}`, with `0 < h < 0.01`.

Proved here, about these power laws only:

* the radial Reynolds number `u_r l_r` is constant: that is the Navier–Stokes
  scaling `u ~ τ^{−1/2}, l ~ τ^{1/2}`;
* the swirl Reynolds number `u_θ l_θ = τ^{−2h}` blows up, so viscosity cannot
  keep pace with the swirl;
* lengths shrink to zero and speeds blow up;
* vorticity `~ u_r/l_r = 1/τ` is not integrable up to `t_b`, which is exactly the
  divergence the Beale–Kato–Majda criterion requires of any blow-up.

This is arithmetic about the stated exponents. It does **not** prove that a
solution with these scalings exists, which is the open Millennium problem. The
λ tables on the slides (CCF, IPM, Boussinesq) are high-precision numerical
solutions, not proofs.
-/

namespace Wyrd.SharedAir

open Filter Topology

/-- Radial Reynolds number is constant: `τ^{1/2} · τ^{−1/2} = 1`. -/
theorem radial_reynolds_const {τ : ℝ} (hτ : 0 < τ) :
    τ ^ ((1 : ℝ) / 2) * τ ^ (-(1 : ℝ) / 2) = 1 := by
  sorry

/-- Swirl Reynolds number `τ^{1/2 − h} · τ^{−(1/2 + h)} = τ^{−2h}`. -/
theorem swirl_reynolds_eq {τ h : ℝ} (hτ : 0 < τ) :
    τ ^ ((1 : ℝ) / 2 - h) * τ ^ (-((1 : ℝ) / 2 + h)) = τ ^ (-2 * h) := by
  sorry

/-- **The swirl Reynolds number blows up** as `τ → 0⁺`, for any `h > 0`. -/
theorem swirl_reynolds_blowup {h : ℝ} (hh : 0 < h) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - h) * τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  sorry

/-- The swirl length shrinks to zero (for `h < 1/2`). -/
theorem swirl_length_shrinks {h : ℝ} (hh : h < 1 / 2) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - h)) (𝓝[>] 0) (𝓝 0) := by
  sorry

/-- The swirl speed blows up (for `h > −1/2`). -/
theorem swirl_speed_blowup {h : ℝ} (hh : -(1 / 2) < h) :
    Tendsto (fun τ : ℝ => τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  sorry

/-- **Vorticity `~ 1/(t_b − t)` is not integrable up to `t_b`** (Beale–Kato–Majda). -/
theorem vorticity_not_integrable {tb : ℝ} (htb : 0 < tb) :
    ¬ IntervalIntegrable (fun t : ℝ => 1 / (tb - t)) MeasureTheory.volume 0 tb := by
  sorry

end Wyrd.SharedAir
