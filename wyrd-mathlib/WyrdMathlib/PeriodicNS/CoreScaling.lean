import Mathlib

/-!
# A shrinking core with bounded energy

With `τ = T − t`, radial scale `ℓ_r ~ τ^{1/2}`, axial scale `ℓ_z ~ τ^{1/2 − h}` and
swirl speed `|u_θ| ~ τ^{−1/2 − h}`: the core volume is `ℓ_r² ℓ_z ~ τ^{3/2 − h}`, and
its kinetic energy `V u² ~ τ^{1/2 − 3h}` tends to `0` when `h < 1/6`, while the speed
blows up (when `h > −1/2`). So a bound on total energy alone does not bound local
speed. The scalings are the illustrative anisotropic ones from the slides and the
accompanying notes (there `0 < h < 0.01`). Exponent arithmetic only, not a
construction of a solution.
-/

namespace Wyrd.PeriodicNS

open Filter Topology

/-- `(τ^a)^2 = τ^(a·2)` for `τ ≥ 0` (via `rpow_mul` and `rpow_natCast`). -/
private theorem coreScaling_rpow_sq {τ : ℝ} (hτ : 0 ≤ τ) (a : ℝ) :
    (τ ^ a) ^ 2 = τ ^ (a * 2) := by
  rw [Real.rpow_mul hτ, ← Real.rpow_natCast]
  norm_num

/-- Core volume `ℓ_r² ℓ_z = τ^{3/2 − h}`. -/
theorem core_volume {τ h : ℝ} (hτ : 0 < τ) :
    (τ ^ ((1 : ℝ) / 2)) ^ 2 * τ ^ ((1 : ℝ) / 2 - h) = τ ^ ((3 : ℝ) / 2 - h) := by
  -- combine into a single power of `τ`, then compare exponents
  rw [coreScaling_rpow_sq hτ.le, ← Real.rpow_add hτ]
  congr 1
  ring

/-- Core energy `V u² = τ^{1/2 − 3h}`. -/
theorem core_energy {τ h : ℝ} (hτ : 0 < τ) :
    τ ^ ((3 : ℝ) / 2 - h) * (τ ^ (-((1 : ℝ) / 2 + h))) ^ 2 = τ ^ ((1 : ℝ) / 2 - 3 * h) := by
  -- combine into a single power of `τ`, then compare exponents
  rw [coreScaling_rpow_sq hτ.le, ← Real.rpow_add hτ]
  congr 1
  ring

/-- **The core energy vanishes** as `τ → 0⁺` when `h < 1/6`, while the swirl speed
blows up (for `h > −1/2`). -/
theorem energy_vanishes_speed_blows {h : ℝ} (h1 : h < 1 / 6) (h0 : -(1 / 2) < h) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - 3 * h)) (𝓝[>] 0) (𝓝 0) ∧
      Tendsto (fun τ : ℝ => τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  constructor
  · -- positive exponent: `τ ↦ τ^e` is continuous at `0` with value `0^e = 0`
    have he : 0 < (1 : ℝ) / 2 - 3 * h := by linarith
    apply tendsto_nhdsWithin_of_tendsto_nhds
    have hc := Real.continuousAt_rpow_const 0 ((1 : ℝ) / 2 - 3 * h) (Or.inr he.le)
    rw [ContinuousAt, Real.zero_rpow he.ne'] at hc
    exact hc
  · -- negative exponent `-(1/2 + h) < 0`: blows up at `0⁺`
    exact tendsto_rpow_neg_nhdsGT_zero (by linarith)

end Wyrd.PeriodicNS
