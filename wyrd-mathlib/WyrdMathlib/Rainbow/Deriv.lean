import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import WyrdMathlib.Rainbow.Defs

/-!
# The rainbow: derivative of the deviation

`D'(i) = 2 - 2(k+1) · cos i / √(n² - sin² i)`, and its sign is decided by
comparing `cos² i` with `(n² - 1) / (k(k+2))`.
-/

namespace Wyrd.Rainbow

open Real

theorem hasDerivAt_refr {n : ℝ} (hn : 1 < n) (i : ℝ) :
    HasDerivAt (refr n) (cos i / √(n ^ 2 - sin i ^ 2)) i := by
  sorry

theorem hasDerivAt_dev {n : ℝ} (hn : 1 < n) (k : ℕ) (i : ℝ) :
    HasDerivAt (dev k n) (2 - 2 * (k + 1) * (cos i / √(n ^ 2 - sin i ^ 2))) i := by
  sorry

theorem continuous_dev {n : ℝ} (hn : 1 < n) (k : ℕ) : Continuous (dev k n) := by
  sorry

theorem deriv_dev_neg_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    deriv (dev k n) i < 0 ↔ (n ^ 2 - 1) / (k * (k + 2)) < cos i ^ 2 := by
  sorry

theorem deriv_dev_pos_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    0 < deriv (dev k n) i ↔ cos i ^ 2 < (n ^ 2 - 1) / (k * (k + 2)) := by
  sorry

theorem deriv_dev_eq_zero_iff {n : ℝ} (hn : 1 < n) {k : ℕ} (hk : 1 ≤ k) {i : ℝ} (hi : 0 ≤ cos i) :
    deriv (dev k n) i = 0 ↔ cos i ^ 2 = (n ^ 2 - 1) / (k * (k + 2)) := by
  sorry

end Wyrd.Rainbow
