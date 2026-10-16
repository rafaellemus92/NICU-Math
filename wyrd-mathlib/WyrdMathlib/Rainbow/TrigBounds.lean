import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.Calculus.Deriv.MeanValue

/-!
# Taylor bounds for sin and cos, to degree 7

Mathlib stops at `x - x³/6 ≤ sin x` and `1 - x²/2 ≤ cos x`. Each bound below
follows from the previous one: if `g(0) = 0` and `g' ≥ 0` on `[0, ∞)`, then
`g ≥ 0` there. Valid for all `x ≥ 0`.
-/

namespace Wyrd.Rainbow

open Real

theorem cos_le_taylor4 {x : ℝ} (hx : 0 ≤ x) : cos x ≤ 1 - x ^ 2 / 2 + x ^ 4 / 24 := by
  sorry

theorem sin_le_taylor5 {x : ℝ} (hx : 0 ≤ x) : sin x ≤ x - x ^ 3 / 6 + x ^ 5 / 120 := by
  sorry

theorem taylor6_le_cos {x : ℝ} (hx : 0 ≤ x) : 1 - x ^ 2 / 2 + x ^ 4 / 24 - x ^ 6 / 720 ≤ cos x := by
  sorry

theorem taylor7_le_sin {x : ℝ} (hx : 0 ≤ x) :
    x - x ^ 3 / 6 + x ^ 5 / 120 - x ^ 7 / 5040 ≤ sin x := by
  sorry

end Wyrd.Rainbow
