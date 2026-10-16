import Mathlib.NumberTheory.Real.Irrational
import Wyrd.Sqrt2

/-!
# √2 is irrational, as a statement about the real number

`Wyrd.eq_zero_of_mul_self_eq_two_mul` (core Lean, `../wyrd`) shows `a² = 2b²`
forces `b = 0`. Here that becomes Mathlib's `Irrational (√2)`: if `√2` were a
fraction `p / q` in lowest terms, then `p² = 2q²` in the integers. Taking absolute
values gives whole numbers with the same equation and `q ≠ 0`, which our
theorem rules out.
-/

namespace Wyrd

/-- **√2 is irrational**, derived from our whole-number descent proof. -/
theorem irrational_sqrt_two : Irrational (Real.sqrt 2) := by
  rintro ⟨q, hq⟩
  -- `q² = 2` as rationals.
  have h2 : ((q : ℝ)) ^ 2 = 2 := by
    rw [hq]; exact Real.sq_sqrt (by norm_num)
  have hq2 : q ^ 2 = 2 := by exact_mod_cast h2
  -- Write `q = num / den` and clear the denominator: `num² = 2 · den²`.
  have hden : (q.den : ℚ) ≠ 0 := by exact_mod_cast q.den_nz
  have hrat : (q.num : ℚ) ^ 2 = 2 * (q.den : ℚ) ^ 2 := by
    have := Rat.num_div_den q
    rw [← this, div_pow] at hq2
    field_simp at hq2
    linarith
  have hint : q.num ^ 2 = 2 * (q.den : ℤ) ^ 2 := by exact_mod_cast hrat
  -- Absolute values: whole numbers `a = |num|`, `b = den` with `a² = 2b²`.
  have hnat : q.num.natAbs * q.num.natAbs = 2 * (q.den * q.den) := by
    have := congrArg Int.natAbs hint
    simpa [sq, Int.natAbs_mul] using this
  exact q.den_nz (eq_zero_of_mul_self_eq_two_mul _ _ hnat)

/-- Agrees with Mathlib's own proof. -/
example : Irrational (Real.sqrt 2) := _root_.irrational_sqrt_two

end Wyrd
