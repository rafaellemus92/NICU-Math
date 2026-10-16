import WyrdMathlib.Rainbow.Deriv
import WyrdMathlib.Rainbow.MinLemma

/-!
# The rainbow: where the bright bow sits

For `1 < n < k + 1` (water, `n ≈ 4/3`, qualifies for every `k ≥ 1`), the
deviation `D` of the `k`-th bow has exactly one stationary point on
`[0, π/2]`, at `cos² i = (n² - 1) / (k(k+2))`, and it is the strict minimum.
-/

namespace Wyrd.Rainbow

open Real

theorem cos_bowIncidence_sq {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    cos (bowIncidence k n) ^ 2 = (n ^ 2 - 1) / (k * (k + 2)) := by
  sorry

theorem bowIncidence_mem {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    bowIncidence k n ∈ Set.Ioo 0 (π / 2) := by
  sorry

theorem deriv_dev_bowIncidence {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    deriv (dev k n) (bowIncidence k n) = 0 := by
  sorry

/-- The only stationary point of `D` on `[0, π/2]` is the bow's incidence angle. -/
theorem deriv_dev_eq_zero_iff_eq {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1)
    {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) :
    deriv (dev k n) i = 0 ↔ i = bowIncidence k n := by
  sorry

/-- **The bow is the strict minimum of the deviation.** -/
theorem dev_lt_of_ne {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1)
    {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) (hne : i ≠ bowIncidence k n) :
    dev k n (bowIncidence k n) < dev k n i := by
  sorry

theorem dev_isMinOn {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    IsMinOn (dev k n) (Set.Icc 0 (π / 2)) (bowIncidence k n) := by
  sorry

/-- Water (`n = 4/3`): the primary bow (`k = 1`) is where `cos² i = 7/27`. -/
theorem water_primary :
    cos (bowIncidence 1 (4 / 3)) ^ 2 = 7 / 27 ∧
      IsMinOn (dev 1 (4 / 3)) (Set.Icc 0 (π / 2)) (bowIncidence 1 (4 / 3)) := by
  sorry

/-- Water (`n = 4/3`): the secondary bow (`k = 2`) is where `cos² i = 7/72`. -/
theorem water_secondary :
    cos (bowIncidence 2 (4 / 3)) ^ 2 = 7 / 72 ∧
      IsMinOn (dev 2 (4 / 3)) (Set.Icc 0 (π / 2)) (bowIncidence 2 (4 / 3)) := by
  sorry

end Wyrd.Rainbow
