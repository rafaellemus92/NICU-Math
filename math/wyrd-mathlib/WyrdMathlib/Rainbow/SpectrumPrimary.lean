import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The primary bow across the spectrum

Water's refractive index is about `1.331` for red light (about 663 nm at 20 °C,
694 nm at 10 °C) and `1.343` for violet (about 402–410 nm). Numerically, the
primary bow is then at 42.37° (red) and 40.65° (violet), a band about 1.7° wide.
The theorems below prove 1° brackets around those values.
-/

namespace Wyrd.Rainbow

open Real

/-- The red primary bow's angle in closed form. -/
private theorem spectrumPrimary_red_exact :
    π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) =
      4 * arcsin (√(742813 / 1771561)) - 2 * arccos (√(257187 / 1000000)) := by
  -- the incidence angle is `arccos √(257187/1000000)`
  have hi : bowIncidence 1 (1331 / 1000) = arccos (√(257187 / 1000000)) := by
    simp only [bowIncidence]; norm_num
  -- the refracted angle there is `arcsin √(742813/1771561)`
  have hr :
      refr (1331 / 1000) (arccos (√(257187 / 1000000))) = arcsin (√(742813 / 1771561)) := by
    rw [refr, sin_arccos, Real.sq_sqrt (by norm_num)]
    congr 1
    rw [div_eq_iff (by norm_num),
      show (1331 / 1000 : ℝ) = √(1771561 / 1000000) by
        rw [show (1771561 / 1000000 : ℝ) = (1331 / 1000) ^ 2 by norm_num,
          Real.sqrt_sq (by norm_num)],
      ← Real.sqrt_mul (by norm_num)]
    norm_num
  -- `π - D = 4r - 2i` for the primary bow
  rw [hi, dev, hr]
  push_cast
  ring

/-- The violet primary bow's angle in closed form. -/
private theorem spectrumPrimary_violet_exact :
    π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) =
      4 * arcsin (√(732117 / 1803649)) - 2 * arccos (√(267883 / 1000000)) := by
  -- the incidence angle is `arccos √(267883/1000000)`
  have hi : bowIncidence 1 (1343 / 1000) = arccos (√(267883 / 1000000)) := by
    simp only [bowIncidence]; norm_num
  -- the refracted angle there is `arcsin √(732117/1803649)`
  have hr :
      refr (1343 / 1000) (arccos (√(267883 / 1000000))) = arcsin (√(732117 / 1803649)) := by
    rw [refr, sin_arccos, Real.sq_sqrt (by norm_num)]
    congr 1
    rw [div_eq_iff (by norm_num),
      show (1343 / 1000 : ℝ) = √(1803649 / 1000000) by
        rw [show (1803649 / 1000000 : ℝ) = (1343 / 1000) ^ 2 by norm_num,
          Real.sqrt_sq (by norm_num)],
      ← Real.sqrt_mul (by norm_num)]
    norm_num
  -- `π - D = 4r - 2i` for the primary bow
  rw [hi, dev, hr]
  push_cast
  ring

/-- Red light (`n = 1.331`): the primary bow lies between 42° and 43°. -/
theorem primary_red :
    42 * π / 180 < π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) ∧
      π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) < 43 * π / 180 := by
  rw [spectrumPrimary_red_exact, arccos_eq_pi_div_two_sub_arcsin]
  have hpi := pi_gt_three
  -- `0.7043 < arcsin √(742813/1771561)`, via `sin x ≤ T₅(x)` at `x = 0.7043`
  have ha1 : (7043 / 10000 : ℝ) < arcsin (√(742813 / 1771561)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (7043 / 10000) ≤ 7043 / 10000 - (7043 / 10000) ^ 3 / 6 + (7043 / 10000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(742813 / 1771561) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(742813/1771561) < 0.7044`, via `T₇(x) ≤ sin x` at `x = 0.7044`
  have ha2 : arcsin (√(742813 / 1771561)) < 7044 / 10000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(742813 / 1771561) < 7044 / 10000 - (7044 / 10000) ^ 3 / 6 + (7044 / 10000) ^ 5 / 120
          - (7044 / 10000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (7044 / 10000) := taylor7_le_sin (by norm_num)
  -- `0.5318 < arcsin √(257187/1000000)`, via `sin x ≤ T₅(x)` at `x = 0.5318`
  have hb1 : (5318 / 10000 : ℝ) < arcsin (√(257187 / 1000000)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (5318 / 10000) ≤ 5318 / 10000 - (5318 / 10000) ^ 3 / 6 + (5318 / 10000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(257187 / 1000000) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(257187/1000000) < 0.5319`, via `T₇(x) ≤ sin x` at `x = 0.5319`
  have hb2 : arcsin (√(257187 / 1000000)) < 5319 / 10000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(257187 / 1000000) < 5319 / 10000 - (5319 / 10000) ^ 3 / 6 + (5319 / 10000) ^ 5 / 120
          - (5319 / 10000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (5319 / 10000) := taylor7_le_sin (by norm_num)
  -- combine with `3.141592 < π < 3.141593`
  have hp1 := pi_gt_d6
  have hp2 := pi_lt_d6
  constructor <;> linarith

/-- Violet light (`n = 1.343`): the primary bow lies between 40° and 41°. -/
theorem primary_violet :
    40 * π / 180 < π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) ∧
      π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) < 41 * π / 180 := by
  rw [spectrumPrimary_violet_exact, arccos_eq_pi_div_two_sub_arcsin]
  have hpi := pi_gt_three
  -- `0.6907 < arcsin √(732117/1803649)`, via `sin x ≤ T₅(x)` at `x = 0.6907`
  have ha1 : (6907 / 10000 : ℝ) < arcsin (√(732117 / 1803649)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (6907 / 10000) ≤ 6907 / 10000 - (6907 / 10000) ^ 3 / 6 + (6907 / 10000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(732117 / 1803649) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(732117/1803649) < 0.6908`, via `T₇(x) ≤ sin x` at `x = 0.6908`
  have ha2 : arcsin (√(732117 / 1803649)) < 6908 / 10000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(732117 / 1803649) < 6908 / 10000 - (6908 / 10000) ^ 3 / 6 + (6908 / 10000) ^ 5 / 120
          - (6908 / 10000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (6908 / 10000) := taylor7_le_sin (by norm_num)
  -- `0.544 < arcsin √(267883/1000000)`, via `sin x ≤ T₅(x)` at `x = 0.544`
  have hb1 : (5440 / 10000 : ℝ) < arcsin (√(267883 / 1000000)) := by
    rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
    calc sin (5440 / 10000) ≤ 5440 / 10000 - (5440 / 10000) ^ 3 / 6 + (5440 / 10000) ^ 5 / 120 :=
          sin_le_taylor5 (by norm_num)
      _ < √(267883 / 1000000) := by rw [Real.lt_sqrt (by norm_num)]; norm_num
  -- `arcsin √(267883/1000000) < 0.5441`, via `T₇(x) ≤ sin x` at `x = 0.5441`
  have hb2 : arcsin (√(267883 / 1000000)) < 5441 / 10000 := by
    rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
    calc √(267883 / 1000000) < 5441 / 10000 - (5441 / 10000) ^ 3 / 6 + (5441 / 10000) ^ 5 / 120
          - (5441 / 10000) ^ 7 / 5040 := by rw [Real.sqrt_lt' (by norm_num)]; norm_num
      _ ≤ sin (5441 / 10000) := taylor7_le_sin (by norm_num)
  -- combine with `3.141592 < π < 3.141593`
  have hp1 := pi_gt_d6
  have hp2 := pi_lt_d6
  constructor <;> linarith

end Wyrd.Rainbow
