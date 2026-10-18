import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The secondary bow across the spectrum

With `n ≈ 1.331` (red, about 663–694 nm) and `1.343` (violet, about 402–410 nm),
the secondary bow is numerically at 50.37° (red) and 53.48° (violet): a band
about 3.1° wide, with the colours reversed. The theorems below prove 1° brackets.
The red bracket is the sensitive one: it holds only for `n` between about
`1.3296` and `1.3334`.
-/

namespace Wyrd.Rainbow

open Real

/-! ### Red light, `n = 1.331` -/

/-- The red secondary bow's angle in closed form: `cos² i₀ = (n² - 1)/8 = 771561/8000000`,
and `sin² r₀ = (1 - cos² i₀)/n² = 7228439/14172488`. -/
private theorem spectrumSecondary_red_exact :
    dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π =
      π + 2 * arccos (√(771561 / 8000000)) - 6 * arcsin (√(7228439 / 14172488)) := by
  -- the incidence angle is `arccos √(771561 / 8000000)`
  have hi : bowIncidence 2 (1331 / 1000) = arccos (√(771561 / 8000000)) := by
    unfold bowIncidence
    congr 2
    push_cast
    norm_num
  -- the refracted angle there is `arcsin √(7228439 / 14172488)`
  have hr : refr (1331 / 1000) (arccos (√(771561 / 8000000))) =
      arcsin (√(7228439 / 14172488)) := by
    rw [refr, sin_arccos, Real.sq_sqrt (by norm_num)]
    congr 1
    -- write `n = √(n²)` and merge the roots
    rw [div_eq_iff (by norm_num),
      show (1331 / 1000 : ℝ) = √(1771561 / 1000000) by
        rw [show (1771561 / 1000000 : ℝ) = (1331 / 1000) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)],
      ← Real.sqrt_mul (by norm_num)]
    norm_num
  -- `D - π = π + 2i - 6r` for the secondary bow
  rw [hi, dev, hr]
  push_cast
  ring

/-- `0.7949 < arcsin √(7228439/14172488)`: `sin 0.7949 ≤ T₅(0.7949) < √(7228439/14172488)`. -/
private lemma spectrumSecondary_red_a_lo : (7949 / 10000 : ℝ) < arcsin (√(7228439 / 14172488)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (7949 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (7949 / 10000 : ℝ) - (7949 / 10000 : ℝ) ^ 3 / 6 + (7949 / 10000 : ℝ) ^ 5 / 120
      < √(7228439 / 14172488) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(7228439/14172488) < 0.7959`: `√(7228439/14172488) < T₇(0.7959) ≤ sin 0.7959`. -/
private lemma spectrumSecondary_red_a_hi : arcsin (√(7228439 / 14172488)) < (7959 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (7959 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(7228439 / 14172488) < (7959 / 10000 : ℝ) - (7959 / 10000 : ℝ) ^ 3 / 6 +
      (7959 / 10000 : ℝ) ^ 5 / 120 - (7959 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- `0.3151 < arcsin √(771561/8000000)`: `sin 0.3151 ≤ T₅(0.3151) < √(771561/8000000)`. -/
private lemma spectrumSecondary_red_b_lo : (3151 / 10000 : ℝ) < arcsin (√(771561 / 8000000)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (3151 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (3151 / 10000 : ℝ) - (3151 / 10000 : ℝ) ^ 3 / 6 + (3151 / 10000 : ℝ) ^ 5 / 120
      < √(771561 / 8000000) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(771561/8000000) < 0.3165`: `√(771561/8000000) < T₇(0.3165) ≤ sin 0.3165`. -/
private lemma spectrumSecondary_red_b_hi : arcsin (√(771561 / 8000000)) < (3165 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (3165 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(771561 / 8000000) < (3165 / 10000 : ℝ) - (3165 / 10000 : ℝ) ^ 3 / 6 +
      (3165 / 10000 : ℝ) ^ 5 / 120 - (3165 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- Red light (`n = 1.331`): the secondary bow lies between 50° and 51°. -/
theorem secondary_red :
    50 * π / 180 < dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π ∧
      dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π < 51 * π / 180 := by
  -- the angle is `2π - (6a + 2b)` with `a = arcsin √(7228439/14172488)`, `b = arcsin √(771561/8000000)`
  rw [spectrumSecondary_red_exact, arccos_eq_pi_div_two_sub_arcsin]
  -- rational brackets for `a`, `b` and `π`; then `309π/180 < 6a + 2b < 310π/180` is linear
  have h1 := spectrumSecondary_red_a_lo
  have h2 := spectrumSecondary_red_a_hi
  have h3 := spectrumSecondary_red_b_lo
  have h4 := spectrumSecondary_red_b_hi
  have h5 := pi_gt_d6
  have h6 := pi_lt_d6
  constructor <;> linarith

/-! ### Violet light, `n = 1.343` -/

/-- The violet secondary bow's angle in closed form: `cos² i₀ = (n² - 1)/8 = 803649/8000000`,
and `sin² r₀ = (1 - cos² i₀)/n² = 7196351/14429192`. -/
private theorem spectrumSecondary_violet_exact :
    dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π =
      π + 2 * arccos (√(803649 / 8000000)) - 6 * arcsin (√(7196351 / 14429192)) := by
  -- the incidence angle is `arccos √(803649 / 8000000)`
  have hi : bowIncidence 2 (1343 / 1000) = arccos (√(803649 / 8000000)) := by
    unfold bowIncidence
    congr 2
    push_cast
    norm_num
  -- the refracted angle there is `arcsin √(7196351 / 14429192)`
  have hr : refr (1343 / 1000) (arccos (√(803649 / 8000000))) =
      arcsin (√(7196351 / 14429192)) := by
    rw [refr, sin_arccos, Real.sq_sqrt (by norm_num)]
    congr 1
    -- write `n = √(n²)` and merge the roots
    rw [div_eq_iff (by norm_num),
      show (1343 / 1000 : ℝ) = √(1803649 / 1000000) by
        rw [show (1803649 / 1000000 : ℝ) = (1343 / 1000) ^ 2 by norm_num, Real.sqrt_sq (by norm_num)],
      ← Real.sqrt_mul (by norm_num)]
    norm_num
  -- `D - π = π + 2i - 6r` for the secondary bow
  rw [hi, dev, hr]
  push_cast
  ring

/-- `0.7836 < arcsin √(7196351/14429192)`: `sin 0.7836 ≤ T₅(0.7836) < √(7196351/14429192)`. -/
private lemma spectrumSecondary_violet_a_lo :
    (7836 / 10000 : ℝ) < arcsin (√(7196351 / 14429192)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (7836 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (7836 / 10000 : ℝ) - (7836 / 10000 : ℝ) ^ 3 / 6 + (7836 / 10000 : ℝ) ^ 5 / 120
      < √(7196351 / 14429192) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(7196351/14429192) < 0.7846`: `√(7196351/14429192) < T₇(0.7846) ≤ sin 0.7846`. -/
private lemma spectrumSecondary_violet_a_hi :
    arcsin (√(7196351 / 14429192)) < (7846 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (7846 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(7196351 / 14429192) < (7846 / 10000 : ℝ) - (7846 / 10000 : ℝ) ^ 3 / 6 +
      (7846 / 10000 : ℝ) ^ 5 / 120 - (7846 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- `0.3218 < arcsin √(803649/8000000)`: `sin 0.3218 ≤ T₅(0.3218) < √(803649/8000000)`. -/
private lemma spectrumSecondary_violet_b_lo : (3218 / 10000 : ℝ) < arcsin (√(803649 / 8000000)) := by
  have hpi := pi_gt_d6
  rw [lt_arcsin_iff_sin_lt' ⟨by linarith, by linarith⟩]
  have h5 := sin_le_taylor5 (x := (3218 / 10000 : ℝ)) (by norm_num)
  -- the Taylor polynomial is below the root: compare squares
  have hs : (3218 / 10000 : ℝ) - (3218 / 10000 : ℝ) ^ 3 / 6 + (3218 / 10000 : ℝ) ^ 5 / 120
      < √(803649 / 8000000) := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  linarith

/-- `arcsin √(803649/8000000) < 0.3232`: `√(803649/8000000) < T₇(0.3232) ≤ sin 0.3232`. -/
private lemma spectrumSecondary_violet_b_hi : arcsin (√(803649 / 8000000)) < (3232 / 10000 : ℝ) := by
  have hpi := pi_gt_d6
  rw [arcsin_lt_iff_lt_sin' ⟨by linarith, by linarith⟩]
  have h7 := taylor7_le_sin (x := (3232 / 10000 : ℝ)) (by norm_num)
  -- the root is below the Taylor polynomial: compare squares
  have hs : √(803649 / 8000000) < (3232 / 10000 : ℝ) - (3232 / 10000 : ℝ) ^ 3 / 6 +
      (3232 / 10000 : ℝ) ^ 5 / 120 - (3232 / 10000 : ℝ) ^ 7 / 5040 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

/-- Violet light (`n = 1.343`): the secondary bow lies between 53° and 54°. -/
theorem secondary_violet :
    53 * π / 180 < dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π ∧
      dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π < 54 * π / 180 := by
  -- the angle is `2π - (6a + 2b)` with `a = arcsin √(7196351/14429192)`, `b = arcsin √(803649/8000000)`
  rw [spectrumSecondary_violet_exact, arccos_eq_pi_div_two_sub_arcsin]
  -- rational brackets for `a`, `b` and `π`; then `306π/180 < 6a + 2b < 307π/180` is linear
  have h1 := spectrumSecondary_violet_a_lo
  have h2 := spectrumSecondary_violet_a_hi
  have h3 := spectrumSecondary_violet_b_lo
  have h4 := spectrumSecondary_violet_b_hi
  have h5 := pi_gt_d6
  have h6 := pi_lt_d6
  constructor <;> linarith

end Wyrd.Rainbow
