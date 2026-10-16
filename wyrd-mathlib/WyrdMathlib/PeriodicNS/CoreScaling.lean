import Mathlib

/-!
# A shrinking core with bounded energy

With `τ = T − t`, radial scale `ℓ_r ~ τ^{1/2}`, axial scale `ℓ_z ~ τ^{1/2 − h}` and
swirl speed `|u_θ| ~ τ^{−1/2 − h}`: the core volume is `ℓ_r² ℓ_z ~ τ^{3/2 − h}`, and
its kinetic energy `V u² ~ τ^{1/2 − 3h}` tends to `0` when `h < 1/6` while the speed
blows up. So a bound on total energy alone does not bound local speed.
Exponent arithmetic only, not a construction of a solution.
-/

namespace Wyrd.PeriodicNS

open Filter Topology

/-- Core volume `ℓ_r² ℓ_z = τ^{3/2 − h}`. -/
theorem core_volume {τ h : ℝ} (hτ : 0 < τ) :
    (τ ^ ((1 : ℝ) / 2)) ^ 2 * τ ^ ((1 : ℝ) / 2 - h) = τ ^ ((3 : ℝ) / 2 - h) := by
  sorry

/-- Core energy `V u² = τ^{1/2 − 3h}`. -/
theorem core_energy {τ h : ℝ} (hτ : 0 < τ) :
    τ ^ ((3 : ℝ) / 2 - h) * (τ ^ (-((1 : ℝ) / 2 + h))) ^ 2 = τ ^ ((1 : ℝ) / 2 - 3 * h) := by
  sorry

/-- **The core energy vanishes** as `τ → 0⁺` when `h < 1/6`, while the swirl speed
blows up (for `h > −1/2`). -/
theorem energy_vanishes_speed_blows {h : ℝ} (h1 : h < 1 / 6) (h0 : -(1 / 2) < h) :
    Tendsto (fun τ : ℝ => τ ^ ((1 : ℝ) / 2 - 3 * h)) (𝓝[>] 0) (𝓝 0) ∧
      Tendsto (fun τ : ℝ => τ ^ (-((1 : ℝ) / 2 + h))) (𝓝[>] 0) atTop := by
  sorry

end Wyrd.PeriodicNS
