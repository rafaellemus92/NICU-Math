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

/-- The engine of the chain: if `g(0) = 0` and `g' ≥ 0` on `[0, ∞)`, then `g ≥ 0`
on `[0, ∞)`. -/
private theorem trig_aux_nonneg {g g' : ℝ → ℝ} (hg : ∀ x, HasDerivAt g (g' x) x)
    (h0 : g 0 = 0) (hd : ∀ x, 0 ≤ x → 0 ≤ g' x) {x : ℝ} (hx : 0 ≤ x) : 0 ≤ g x := by
  -- `g` is monotone on `[0, ∞)`, since its derivative is nonnegative on `(0, ∞)`
  have hmono : MonotoneOn g (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0)
    · exact fun y _ => (hg y).continuousAt.continuousWithinAt
    · exact fun y _ => (hg y).differentiableAt.differentiableWithinAt
    · intro y hy
      rw [interior_Ici] at hy
      rw [(hg y).deriv]
      exact hd y (Set.mem_Ioi.mp hy).le
  -- hence `0 = g 0 ≤ g x`
  simpa [h0] using hmono Set.self_mem_Ici hx hx

/-- `cos x ≤ 1 - x²/2 + x⁴/24`: the derivative of the gap is
`-x + x³/6 + sin x ≥ 0`, by Mathlib's `x - x³/6 ≤ sin x`. -/
theorem cos_le_taylor4 {x : ℝ} (hx : 0 ≤ x) : cos x ≤ 1 - x ^ 2 / 2 + x ^ 4 / 24 := by
  have key := trig_aux_nonneg (g := fun x => 1 - x ^ 2 / 2 + x ^ 4 / 24 - cos x)
    (g' := fun x => -x + x ^ 3 / 6 + sin x) ?_ (by simp) ?_ hx
  -- the gap is nonnegative, which is the claim
  · linarith
  -- derivative of the gap
  · intro y
    have h := (((hasDerivAt_const y (1 : ℝ)).sub ((hasDerivAt_pow 2 y).div_const 2)).add
      ((hasDerivAt_pow 4 y).div_const 24)).sub (Real.hasDerivAt_cos y)
    convert h using 1
    norm_num; ring
  -- the derivative is nonnegative by `sin_ge_sub_cube`
  · intro y hy
    have := Real.sin_ge_sub_cube hy
    linarith

/-- `sin x ≤ x - x³/6 + x⁵/120`: the derivative of the gap is
`1 - x²/2 + x⁴/24 - cos x ≥ 0`, by `cos_le_taylor4`. -/
theorem sin_le_taylor5 {x : ℝ} (hx : 0 ≤ x) : sin x ≤ x - x ^ 3 / 6 + x ^ 5 / 120 := by
  have key := trig_aux_nonneg (g := fun x => x - x ^ 3 / 6 + x ^ 5 / 120 - sin x)
    (g' := fun x => 1 - x ^ 2 / 2 + x ^ 4 / 24 - cos x) ?_ (by simp) ?_ hx
  -- the gap is nonnegative, which is the claim
  · linarith
  -- derivative of the gap
  · intro y
    have h := (((hasDerivAt_id' y).sub ((hasDerivAt_pow 3 y).div_const 6)).add
      ((hasDerivAt_pow 5 y).div_const 120)).sub (Real.hasDerivAt_sin y)
    convert h using 1
    norm_num; ring
  -- the derivative is nonnegative by the previous step
  · intro y hy
    have := cos_le_taylor4 hy
    linarith

/-- `1 - x²/2 + x⁴/24 - x⁶/720 ≤ cos x`: the derivative of the gap is
`-sin x + x - x³/6 + x⁵/120 ≥ 0`, by `sin_le_taylor5`. -/
theorem taylor6_le_cos {x : ℝ} (hx : 0 ≤ x) : 1 - x ^ 2 / 2 + x ^ 4 / 24 - x ^ 6 / 720 ≤ cos x := by
  have key := trig_aux_nonneg (g := fun x => cos x - (1 - x ^ 2 / 2 + x ^ 4 / 24 - x ^ 6 / 720))
    (g' := fun x => -sin x + x - x ^ 3 / 6 + x ^ 5 / 120) ?_ (by simp) ?_ hx
  -- the gap is nonnegative, which is the claim
  · linarith
  -- derivative of the gap
  · intro y
    have h := (Real.hasDerivAt_cos y).sub ((((hasDerivAt_const y (1 : ℝ)).sub
      ((hasDerivAt_pow 2 y).div_const 2)).add ((hasDerivAt_pow 4 y).div_const 24)).sub
      ((hasDerivAt_pow 6 y).div_const 720))
    convert h using 1
    norm_num; ring
  -- the derivative is nonnegative by the previous step
  · intro y hy
    have := sin_le_taylor5 hy
    linarith

/-- `x - x³/6 + x⁵/120 - x⁷/5040 ≤ sin x`: the derivative of the gap is
`cos x - (1 - x²/2 + x⁴/24 - x⁶/720) ≥ 0`, by `taylor6_le_cos`. -/
theorem taylor7_le_sin {x : ℝ} (hx : 0 ≤ x) :
    x - x ^ 3 / 6 + x ^ 5 / 120 - x ^ 7 / 5040 ≤ sin x := by
  have key := trig_aux_nonneg (g := fun x => sin x - (x - x ^ 3 / 6 + x ^ 5 / 120 - x ^ 7 / 5040))
    (g' := fun x => cos x - (1 - x ^ 2 / 2 + x ^ 4 / 24 - x ^ 6 / 720)) ?_ (by simp) ?_ hx
  -- the gap is nonnegative, which is the claim
  · linarith
  -- derivative of the gap
  · intro y
    have h := (Real.hasDerivAt_sin y).sub ((((hasDerivAt_id' y).sub
      ((hasDerivAt_pow 3 y).div_const 6)).add ((hasDerivAt_pow 5 y).div_const 120)).sub
      ((hasDerivAt_pow 7 y).div_const 5040))
    convert h using 1
    norm_num; ring
  -- the derivative is nonnegative by the previous step
  · intro y hy
    have := taylor6_le_cos hy
    linarith

end Wyrd.Rainbow
