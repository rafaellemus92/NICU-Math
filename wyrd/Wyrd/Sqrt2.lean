/-!
# √2 is irrational (whole-number form)

Core Lean has no real numbers, so we prove the whole-number heart of it:

> no fraction `a / b` (with `b ≠ 0`) squares to 2, i.e. `a² = 2b²` forces `b = 0`.

The sister project `../wyrd-mathlib` turns this into Mathlib's
`Irrational (√2)` about the real number.

Paper proof, by **infinite descent** (Fermat's name for it): suppose
`a² = 2b²` with `b > 0`. Then `a²` is even, so `a` is even, say `a = 2c`. Then
`4c² = 2b²`, so `b² = 2c²`: another solution, with `b < a`. Repeating forever
would give an endless decreasing sequence of positive whole numbers, which is
impossible. In Lean, "repeating forever is impossible" is just strong
induction on `a`.
-/

namespace Wyrd

/-- If `a` is odd, so is `a · a`. -/
theorem mul_self_mod_two {a : Nat} (h : a % 2 = 1) : (a * a) % 2 = 1 := by
  rw [Nat.mul_mod, h]

/-- **`a² = 2b²` only when `b = 0`.** -/
theorem eq_zero_of_mul_self_eq_two_mul : ∀ a b : Nat, a * a = 2 * (b * b) → b = 0
  | a, b, h => by
    apply Classical.byContradiction
    intro hb
    -- `a` is even: if it were odd, `a · a` would be odd, but it equals `2b²`.
    have heven : a % 2 = 0 := by
      rcases Nat.mod_two_eq_zero_or_one a with h0 | h1
      · exact h0
      · have := mul_self_mod_two h1
        omega
    obtain ⟨c, rfl⟩ : ∃ c, a = 2 * c := ⟨a / 2, by omega⟩
    -- `4c² = 2b²`, so `b² = 2c²`.
    have hbc : b * b = 2 * (c * c) := by
      have := Nat.mul_mul_mul_comm 2 c 2 c
      omega
    -- The new solution is smaller: `b < 2c`.
    have hpos : 0 < b * b := Nat.mul_pos (by omega) (by omega)
    have hlt : b < 2 * c := by
      apply Nat.lt_of_not_le
      intro hle
      have := Nat.mul_le_mul hle hle
      omega
    -- Descent: the smaller solution forces `c = 0`, so `b² = 0`, so `b = 0`.
    have hc := eq_zero_of_mul_self_eq_two_mul b c hbc
    subst hc
    omega
termination_by a => a
decreasing_by omega

/-- **No fraction squares to 2.** -/
theorem no_fraction_squares_to_two : ¬ ∃ a b : Nat, b ≠ 0 ∧ a * a = 2 * (b * b) := by
  rintro ⟨a, b, hb, h⟩
  exact hb (eq_zero_of_mul_self_eq_two_mul a b h)

end Wyrd
