import Wyrd.Pangram

/-!
# There are infinitely many primes (Euclid, c. 300 BC)

Paper proof: take any `n` and look at `n! + 1`. It is at least 2, so some prime
`p` divides it. If `p ≤ n`, then `p` also divides `n!`, so it divides
`(n! + 1) - n! = 1`, which is impossible. So `p > n`.

Core Lean has neither factorials nor "every number ≥ 2 has a prime factor", so
both are proved here first. Mathlib has them as `Nat.factorial` and
`Nat.exists_prime_and_dvd`.
-/

namespace Wyrd

/-! ## Factorials -/

/-- `fact n = 1 · 2 · … · n`. -/
def fact : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * fact n

theorem fact_pos : ∀ n, 0 < fact n
  | 0 => by decide
  | n + 1 => Nat.mul_pos (Nat.succ_pos n) (fact_pos n)

/-- Every `k` from 1 to `n` divides `n!`. Induction on `n`: `(n+1)! = (n+1) · n!`,
so `k` divides it either as the factor `n + 1` itself or through `n!`. -/
theorem dvd_fact : ∀ {k n : Nat}, 1 ≤ k → k ≤ n → k ∣ fact n
  | _, 0, hk, hkn => by omega
  | k, n + 1, hk, hkn => by
    rcases Nat.lt_or_eq_of_le hkn with hlt | heq
    · exact Nat.dvd_trans (dvd_fact hk (by omega)) (Nat.dvd_mul_left _ _)
    · rw [heq]; exact Nat.dvd_mul_right _ _

/-! ## Every number ≥ 2 has a prime factor -/

/-- Strong induction: if `m` is prime, it is its own prime factor. Otherwise it
has a divisor `d` with `1 < d < m`, and a prime factor of `d` divides `m`. -/
theorem exists_prime_dvd : ∀ m, 2 ≤ m → ∃ p, IsPrime p ∧ p ∣ m
  | m, hm => by
    by_cases hp : IsPrime m
    · exact ⟨m, hp, Nat.dvd_refl m⟩
    · -- Not prime: some divisor is neither 1 nor m.
      have : ∃ d, d ∣ m ∧ d ≠ 1 ∧ d ≠ m := by
        apply Classical.byContradiction
        intro hno
        exact hp ⟨hm, fun d hd => by
          apply Classical.byContradiction
          intro hd'
          exact hno ⟨d, hd, fun e => hd' (Or.inl e), fun e => hd' (Or.inr e)⟩⟩
      obtain ⟨d, hdm, hd1, hdm'⟩ := this
      have hdle : d ≤ m := Nat.le_of_dvd (by omega) hdm
      have hd0 : d ≠ 0 := by rintro rfl; simp at hdm; omega
      obtain ⟨p, hp, hpd⟩ := exists_prime_dvd d (by omega)
      exact ⟨p, hp, Nat.dvd_trans hpd hdm⟩
termination_by m => m
decreasing_by omega

/-! ## Euclid's theorem -/

/-- **For every `n` there is a prime bigger than `n`.** -/
theorem exists_prime_gt (n : Nat) : ∃ p, n < p ∧ IsPrime p := by
  obtain ⟨p, hp, hpd⟩ := exists_prime_dvd (fact n + 1) (by have := fact_pos n; omega)
  refine ⟨p, ?_, hp⟩
  apply Nat.lt_of_not_le
  intro hpn
  -- `p ≤ n`, so `p ∣ n!`, and so `p ∣ 1`.
  have h1 : p ∣ fact n := dvd_fact (by have := hp.1; omega) hpn
  have : p ∣ 1 := (Nat.dvd_add_right h1).mp hpd
  have := Nat.le_of_dvd (by decide) this
  have := hp.1
  omega

/-- **There are infinitely many primes**, stated as: no number bounds them all. -/
theorem primes_infinite : ¬ ∃ B, ∀ p, IsPrime p → p ≤ B := by
  rintro ⟨B, hB⟩
  obtain ⟨p, hgt, hp⟩ := exists_prime_gt B
  have := hB p hp
  omega

end Wyrd
