import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The secondary rainbow sits at about 51°

For water (`n = 4/3`), the secondary bow is seen at angle `D - π` from the point
opposite the sun. Exactly, that angle is `π + 2·arccos √(7/72) - 6·arcsin √(65/128)`,
and numerically it is about 51.0°.
-/

namespace Wyrd.Rainbow

open Real

/-- For water, the secondary bow's incidence angle is `arccos √(7/72)`, since
`((4/3)² - 1) / (2·(2+2)) = 7/72`. -/
private lemma secondary_bowIncidence : bowIncidence 2 (4 / 3) = arccos (√(7 / 72)) := by
  unfold bowIncidence
  congr 2
  push_cast
  norm_num

/-- At that incidence, the refraction angle is `arcsin √(65/128)`:
`sin (arccos √(7/72)) = √(65/72)`, and `√(65/72) / (4/3) = √(65/128)`. -/
private lemma secondary_refr : refr (4 / 3) (arccos (√(7 / 72))) = arcsin (√(65 / 128)) := by
  unfold refr
  rw [sin_arccos, sq_sqrt (by norm_num)]
  congr 1
  -- write `65/72 = (65/128)·(4/3)²` and pull the square out of the root
  rw [show (1 - 7 / 72 : ℝ) = (65 / 128) * (4 / 3) ^ 2 by norm_num,
    Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
  field_simp

/-- The secondary bow's angle in closed form. -/
theorem secondary_bow_water_exact :
    dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π = π + 2 * arccos (√(7 / 72)) - 6 * arcsin (√(65 / 128)) := by
  -- substitute the incidence and refraction angles; `D - π = π + 2i - 6r`
  rw [secondary_bowIncidence, dev, secondary_refr]
  push_cast
  ring

/-- `0.7928 < arcsin √(65/128)`: `sin 0.7928 ≤ T₅(0.7928) < √(65/128)`. -/
private lemma secondary_a_lo : (7928 / 10000 : ℝ) < arcsin (√(65 / 128)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (7928 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (7928 / 10000 : ℝ) - (7928 / 10000 : ℝ) ^ 3 / 6 + (7928 / 10000 : ℝ) ^ 5 / 120
      < √(65 / 128) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(65/128) < 0.7936`: `√(65/128) < T₇(0.7936) ≤ sin 0.7936`. -/
private lemma secondary_a_hi : arcsin (√(65 / 128)) < (7936 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (7936 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(65 / 128) < (7936 / 10000 : ℝ) - (7936 / 10000 : ℝ) ^ 3 / 6 +
      (7936 / 10000 : ℝ) ^ 5 / 120 - (7936 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- `0.3166 < arcsin √(7/72)`: `sin 0.3166 ≤ T₅(0.3166) < √(7/72)`. -/
private lemma secondary_b_lo : (3166 / 10000 : ℝ) < arcsin (√(7 / 72)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (3166 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (3166 / 10000 : ℝ) - (3166 / 10000 : ℝ) ^ 3 / 6 + (3166 / 10000 : ℝ) ^ 5 / 120
      < √(7 / 72) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(7/72) < 0.3175`: `√(7/72) < T₇(0.3175) ≤ sin 0.3175`. -/
private lemma secondary_b_hi : arcsin (√(7 / 72)) < (3175 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (3175 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(7 / 72) < (3175 / 10000 : ℝ) - (3175 / 10000 : ℝ) ^ 3 / 6 +
      (3175 / 10000 : ℝ) ^ 5 / 120 - (3175 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- **The secondary rainbow is between 50° and 52°.** -/
theorem secondary_bow_water :
    50 * π / 180 < dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π ∧
      dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π < 52 * π / 180 := by
  -- the angle is `2π - (6a + 2b)` with `a = arcsin √(65/128)`, `b = arcsin √(7/72)`
  rw [secondary_bow_water_exact, arccos_eq_pi_div_two_sub_arcsin]
  -- rational brackets for `a`, `b` and `π`; then `308π/180 < 6a + 2b < 310π/180` is linear
  have h1 := secondary_a_lo
  have h2 := secondary_a_hi
  have h3 := secondary_b_lo
  have h4 := secondary_b_hi
  have h5 := pi_gt_d6
  have h6 := pi_lt_d6
  constructor <;> linarith

end Wyrd.Rainbow
