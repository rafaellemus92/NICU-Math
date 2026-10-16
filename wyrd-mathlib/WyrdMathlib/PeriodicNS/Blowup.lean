import Mathlib

/-!
# Blow-up scalings: what the exponents imply

A candidate Navier–Stokes singularity at time `t_b`, written with
`τ = t_b − t → 0⁺` (from the slides): radial length `l_r ~ τ^{1/2}`, radial
speed `u_r ~ τ^{−1/2}`, swirl length `l_θ ~ τ^{1/2 − h}`, swirl speed
`u_θ ~ τ^{−(1/2 + h)}`, with `0 < h < 0.01`. (This `h` is the slides' exponent, unrelated to the
Shared Air coefficient `h`.)

Proved here, about these power laws only:

* the radial Reynolds number `u_r l_r` is constant: that is the Navier–Stokes
  scaling `u ~ τ^{−1/2}, l ~ τ^{1/2}`;
* the swirl Reynolds number `u_θ l_θ = τ^{−2h}` blows up (heuristically, viscosity
  cannot keep pace with the swirl; that reading is not proved);
* lengths shrink to zero and speeds blow up;
* vorticity `~ u_r/l_r = 1/τ` is not integrable up to `t_b`, which is exactly the
  divergence the Beale–Kato–Majda criterion requires of any blow-up.

This is arithmetic about the stated exponents. It does **not** prove that a
solution with these scalings exists; that existence is open, and a smooth
finite-energy example would settle the Millennium problem in the blow-up direction. The
λ tables on the slides (CCF, IPM, Boussinesq) are high-precision numerical
solutions, not proofs.
-/

namespace Wyrd.PeriodicNS

open Filter Topology

/-- Radial Reynolds number is constant: `τ^{1/2} · τ^{−1/2} = 1`. -/
theorem radial_reynolds_const {τ : ℝ} (hτ : 0 < τ) :
    τ ^ ((1 : ℝ) / 2) * τ ^ (-(1 : ℝ) / 2) = 1 := by
  -- combine exponents: 1/2 + (-1)/2 = 0
  rw [← Real.rpow_add hτ]
  norm_num

/-- Swirl Reynolds number `τ^{1/2 − h} · τ^{−(1/2 + h)} = τ^{−2h}`. -/
theorem swirl_reynolds_eq {τ h : ℝ} (hτ : 0 < τ) :
    τ ^ ((1 : ℝ) / 2 - h) * τ ^ (-((1 : ℝ) / 2 + h)) = τ ^ (-2 * h) := by
  -- combine exponents: (1/2 - h) - (1/2 + h) = -2h
  rw [← Real.rpow_add hτ]
  congr 1
  ring

/-- **The swirl Reynolds number blows up** as `τ → 0⁺`, for any `h > 0`. -/
theorem swirl_reynolds_blowup {h : ℝ} (hh : 0 < h) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - h) * τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  -- on `τ > 0` the product equals `τ^(-2h)`, which blows up since `-2h < 0`
  refine (tendsto_rpow_neg_nhdsGT_zero (y := -2 * h) (by linarith)).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with τ hτ
  exact (swirl_reynolds_eq hτ).symm

/-- The swirl length shrinks to zero (for `h < 1/2`). -/
theorem swirl_length_shrinks {h : ℝ} (hh : h < 1 / 2) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - h)) (𝓝[>] 0) (𝓝 0) := by
  -- `x ↦ x^p` is continuous at `0` for `p > 0`, with value `0^p = 0`
  have hp : (0 : ℝ) < 1 / 2 - h := by linarith
  have hc : Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - h)) (𝓝 0) (𝓝 ((0 : ℝ) ^ ((1 : ℝ) / 2 - h))) :=
    (Real.continuousAt_rpow_const 0 _ (Or.inr hp.le)).tendsto
  rw [Real.zero_rpow hp.ne'] at hc
  exact tendsto_nhdsWithin_of_tendsto_nhds hc

/-- The swirl speed blows up (for `h > −1/2`). -/
theorem swirl_speed_blowup {h : ℝ} (hh : -(1 / 2) < h) :
    Tendsto (fun τ : ℝ => τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  -- negative exponent `-(1/2 + h) < 0`
  exact tendsto_rpow_neg_nhdsGT_zero (by linarith)

/-- **Vorticity `~ 1/(t_b − t)` is not integrable up to `t_b`** (Beale–Kato–Majda). -/
theorem vorticity_not_integrable {tb : ℝ} (htb : 0 < tb) :
    ¬ IntervalIntegrable (fun t : ℝ => 1 / (tb - t)) MeasureTheory.volume 0 tb := by
  intro hint
  -- `1/(tb - t) = -(t - tb)⁻¹`, so `(t - tb)⁻¹` would be integrable on `[0, tb]`
  have h2 : IntervalIntegrable (fun t : ℝ => (t - tb)⁻¹) MeasureTheory.volume 0 tb := by
    refine hint.neg.congr ?_
    intro t _
    simp only [Pi.neg_apply]
    rw [one_div, ← neg_sub, inv_neg, neg_neg]
  -- but that requires `0 = tb` or `tb ∉ [[0, tb]]`, both false
  rcases intervalIntegrable_sub_inv_iff.mp h2 with h0 | hmem
  · exact htb.ne h0
  · exact hmem Set.right_mem_uIcc

end Wyrd.PeriodicNS
