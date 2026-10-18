import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The primary rainbow sits at about 42°

For water (`n = 4/3`), the primary bow is seen at angle `π - D` from the point
opposite the sun. Exactly, that angle is `4·arcsin √(5/12) - 2·arccos √(7/27)`,
and numerically it is about 42.0°.
-/

namespace Wyrd.Rainbow

open Real

/-- The primary bow's angle in closed form. -/
theorem primary_bow_water_exact :
    π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) = 4 * arcsin (√(5 / 12)) - 2 * arccos (√(7 / 27)) := by
  -- the incidence angle of the primary bow for water is `arccos √(7/27)`
  have hi : bowIncidence 1 (4 / 3) = arccos (√(7 / 27)) := by
    simp only [bowIncidence]; norm_num
  -- the refracted angle there is `arcsin √(5/12)`
  have hr : refr (4 / 3) (arccos (√(7 / 27))) = arcsin (√(5 / 12)) := by
    rw [refr, sin_arccos, Real.sq_sqrt (by norm_num)]
    congr 1
    rw [div_eq_iff (by norm_num),
      show (4 / 3 : ℝ) = √(16 / 9) by
        rw [show (16 / 9 : ℝ) = (4 / 3) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)],
      ← Real.sqrt_mul (by norm_num)]
    norm_num
  -- `π - D = 4r - 2i` for the primary bow
  rw [hi, dev, hr]
  push_cast
  ring

/-- **The primary rainbow is between 41° and 43°.** -/
theorem primary_bow_water :
    41 * π / 180 < π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) ∧
      π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) < 43 * π / 180 := by
  rw [primary_bow_water_exact, arccos_eq_pi_div_two_sub_arcsin]
  have hpi := pi_gt_three
  -- `0.701 < arcsin √(5/12)`, since `sin 0.701 ≤ T₅(0.701) < √(5/12)`
  have ha1 : (701 / 1000 : ℝ) < arcsin (√(5 / 12)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (701 / 1000) ≤ 701 / 1000 - (701 / 1000) ^ 3 / 6 + (701 / 1000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(5 / 12) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(5/12) < 0.7025`, since `√(5/12) < T₇(0.7025) ≤ sin 0.7025`
  have ha2 : arcsin (√(5 / 12)) < 7025 / 10000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(5 / 12) < 7025 / 10000 - (7025 / 10000) ^ 3 / 6 + (7025 / 10000) ^ 5 / 120
          - (7025 / 10000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (7025 / 10000) := taylor7_le_sin (by norm_num)
  -- `0.533 < arcsin √(7/27)`, since `sin 0.533 ≤ T₅(0.533) < √(7/27)`
  have hb1 : (533 / 1000 : ℝ) < arcsin (√(7 / 27)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (533 / 1000) ≤ 533 / 1000 - (533 / 1000) ^ 3 / 6 + (533 / 1000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(7 / 27) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(7/27) < 0.535`, since `√(7/27) < T₇(0.535) ≤ sin 0.535`
  have hb2 : arcsin (√(7 / 27)) < 535 / 1000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(7 / 27) < 535 / 1000 - (535 / 1000) ^ 3 / 6 + (535 / 1000) ^ 5 / 120
          - (535 / 1000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (535 / 1000) := taylor7_le_sin (by norm_num)
  -- combine with `3.141592 < π < 3.141593`
  have hp1 := pi_gt_d6
  have hp2 := pi_lt_d6
  constructor <;> linarith

end Wyrd.Rainbow
