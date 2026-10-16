import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import WyrdMathlib.Rainbow.Defs

/-!
# The rainbow: derivative of the deviation

`D'(i) = 2 - 2(k+1) · cos i / √(n² - sin² i)`, and its sign is decided by
comparing `cos² i` with `(n² - 1) / (k(k+2))`.
-/

namespace Wyrd.Rainbow

open Real

/-- Since `n > 1`, the radicand `n² - sin² i` is positive for every `i`. -/
private lemma deriv_aux_radicand_pos {n : ℝ} (hn : 1 < n) (i : ℝ) : 0 < n ^ 2 - sin i ^ 2 := by
  nlinarith [sin_sq_le_one i]

/-- The refraction angle changes at rate `r'(i) = cos i / √(n² - sin² i)`. -/
theorem hasDerivAt_refr {n : ℝ} (hn : 1 < n) (i : ℝ) :
    HasDerivAt (refr n) (cos i / √(n ^ 2 - sin i ^ 2)) i := by
  have hn0 : 0 < n := by linarith
  -- `|sin i / n| ≤ 1 / n < 1`, so `arcsin` is differentiable at `sin i / n`
  have hs1 : sin i / n < 1 := by
    rw [div_lt_iff₀ hn0]; nlinarith [sin_le_one i]
  have hs2 : -1 < sin i / n := by
    rw [lt_div_iff₀ hn0]; nlinarith [neg_one_le_sin i]
  -- chain rule: `arcsin ∘ (sin · / n)`
  have h := (hasDerivAt_arcsin hs2.ne' hs1.ne).comp i ((hasDerivAt_sin i).div_const n)
  -- algebra: `√(n² - sin² i) = n · √(1 - (sin i / n)²)`
  have key : n * √(1 - (sin i / n) ^ 2) = √(n ^ 2 - sin i ^ 2) := by
    have : n ^ 2 - sin i ^ 2 = n ^ 2 * (1 - (sin i / n) ^ 2) := by field_simp
    rw [this, Real.sqrt_mul (sq_nonneg n), Real.sqrt_sq hn0.le]
  have hpos : 0 < √(1 - (sin i / n) ^ 2) := by
    apply Real.sqrt_pos.2
    nlinarith
  -- so `1/√(1 - (s/n)²) · (c/n) = c / √(n² - s²)`
  convert h using 1
  · rfl
  · rw [← key]
    field_simp

/-- **The derivative of the deviation**: `D'(i) = 2 - 2(k+1) · cos i / √(n² - sin² i)`. -/
theorem hasDerivAt_dev {n : ℝ} (hn : 1 < n) (k : ℕ) (i : ℝ) :
    HasDerivAt (dev k n) (2 - 2 * (k + 1) * (cos i / √(n ^ 2 - sin i ^ 2))) i := by
  -- `D(i) = kπ + 2i - 2(k+1) r(i)`, differentiate term by term
  have h := (((hasDerivAt_id i).const_mul 2).const_add ((k : ℝ) * π)).sub
    ((hasDerivAt_refr hn i).const_mul (2 * ((k : ℝ) + 1)))
  convert h using 1
  · ext x; simp [dev]
  · ring

/-- The deviation is continuous (it is differentiable everywhere). -/
theorem continuous_dev {n : ℝ} (hn : 1 < n) (k : ℕ) : Continuous (dev k n) := by
  -- differentiable everywhere, hence continuous
  exact continuous_iff_continuousAt.2 fun i => (hasDerivAt_dev hn k i).continuousAt

/-- `D'(i) = 2 (q - (k+1) cos i) / q`, where `q = √(n² - sin² i) > 0`. -/
private lemma deriv_aux_formula {n : ℝ} (hn : 1 < n) (k : ℕ) (i : ℝ) :
    deriv (dev k n) i =
      2 * (√(n ^ 2 - sin i ^ 2) - (k + 1) * cos i) / √(n ^ 2 - sin i ^ 2) := by
  have hq : 0 < √(n ^ 2 - sin i ^ 2) := Real.sqrt_pos.2 (deriv_aux_radicand_pos hn i)
  rw [(hasDerivAt_dev hn k i).deriv]
  field_simp

/-- Squaring both (nonnegative) sides: `q < (k+1) c ↔ (n² - 1)/(k(k+2)) < c²`,
using `q² = n² - sin² i = n² - 1 + c²`. -/
private lemma deriv_aux_lt_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ}
    (hi : 0 ≤ cos i) :
    √(n ^ 2 - sin i ^ 2) < (k + 1) * cos i ↔ (n ^ 2 - 1) / (k * (k + 2)) < cos i ^ 2 := by
  have hk1 : (1 : ℝ) ≤ k := by exact_mod_cast hk
  have hkk : (0 : ℝ) < k * (k + 2) := by positivity
  have hq0 := Real.sqrt_nonneg (n ^ 2 - sin i ^ 2)
  have hKc : 0 ≤ ((k : ℝ) + 1) * cos i := mul_nonneg (by positivity) hi
  have hsq : √(n ^ 2 - sin i ^ 2) ^ 2 = n ^ 2 - sin i ^ 2 :=
    Real.sq_sqrt (deriv_aux_radicand_pos hn i).le
  have hsc := sin_sq_add_cos_sq i
  rw [div_lt_iff₀ hkk, ← pow_lt_pow_iff_left₀ hq0 hKc two_ne_zero, hsq]
  constructor <;> intro h <;> nlinarith

/-- The mirror image: `(k+1) c < q ↔ c² < (n² - 1)/(k(k+2))`. -/
private lemma deriv_aux_gt_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ}
    (hi : 0 ≤ cos i) :
    (k + 1) * cos i < √(n ^ 2 - sin i ^ 2) ↔ cos i ^ 2 < (n ^ 2 - 1) / (k * (k + 2)) := by
  have hk1 : (1 : ℝ) ≤ k := by exact_mod_cast hk
  have hkk : (0 : ℝ) < k * (k + 2) := by positivity
  have hq0 := Real.sqrt_nonneg (n ^ 2 - sin i ^ 2)
  have hKc : 0 ≤ ((k : ℝ) + 1) * cos i := mul_nonneg (by positivity) hi
  have hsq : √(n ^ 2 - sin i ^ 2) ^ 2 = n ^ 2 - sin i ^ 2 :=
    Real.sq_sqrt (deriv_aux_radicand_pos hn i).le
  have hsc := sin_sq_add_cos_sq i
  rw [lt_div_iff₀ hkk, ← pow_lt_pow_iff_left₀ hKc hq0 two_ne_zero, hsq]
  constructor <;> intro h <;> nlinarith

/-- `D` is falling exactly where `cos² i` exceeds `(n² - 1)/(k(k+2))`. -/
theorem deriv_dev_neg_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    deriv (dev k n) i < 0 ↔ (n ^ 2 - 1) / (k * (k + 2)) < cos i ^ 2 := by
  have hq : 0 < √(n ^ 2 - sin i ^ 2) := Real.sqrt_pos.2 (deriv_aux_radicand_pos hn i)
  -- `D' < 0 ↔ q < (k+1) c`, then square
  rw [deriv_aux_formula hn k i, div_lt_iff₀ hq, zero_mul, ← deriv_aux_lt_iff hn hk hi]
  constructor <;> intro h <;> linarith

/-- `D` is rising exactly where `cos² i` is below `(n² - 1)/(k(k+2))`. -/
theorem deriv_dev_pos_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    0 < deriv (dev k n) i ↔ cos i ^ 2 < (n ^ 2 - 1) / (k * (k + 2)) := by
  have hq : 0 < √(n ^ 2 - sin i ^ 2) := Real.sqrt_pos.2 (deriv_aux_radicand_pos hn i)
  -- `0 < D' ↔ (k+1) c < q`, then square
  rw [deriv_aux_formula hn k i, lt_div_iff₀ hq, zero_mul, ← deriv_aux_gt_iff hn hk hi]
  constructor <;> intro h <;> linarith

/-- `D` is stationary exactly where `cos² i = (n² - 1)/(k(k+2))`. -/
theorem deriv_dev_eq_zero_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    deriv (dev k n) i = 0 ↔ cos i ^ 2 = (n ^ 2 - 1) / (k * (k + 2)) := by
  -- trichotomy on both sides, ruling out the strict cases with the two lemmas above
  constructor
  · intro h
    rcases lt_trichotomy (cos i ^ 2) ((n ^ 2 - 1) / (k * (k + 2))) with h1 | h1 | h1
    · exact absurd h ((deriv_dev_pos_iff hn hk hi).2 h1).ne'
    · exact h1
    · exact absurd h ((deriv_dev_neg_iff hn hk hi).2 h1).ne
  · intro h
    rcases lt_trichotomy (deriv (dev k n) i) 0 with h1 | h1 | h1
    · exact absurd h ((deriv_dev_neg_iff hn hk hi).1 h1).ne'
    · exact h1
    · exact absurd h ((deriv_dev_pos_iff hn hk hi).1 h1).ne

end Wyrd.Rainbow
