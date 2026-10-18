import Wyrd.Distinct

/-!
# Every pangram has an even sum and never uses the prime 2

Paper proof:

1. **2 is in at most one pair.** The ten primes are distinct (`primes_nodup`).
2. **So some pair avoids 2.** There are five pairs, and at most one contains 2.
3. **So `N` is even.** Both primes in that pair are odd (2 is the only even
   prime), and odd + odd is even.
4. **So 2 is never used.** If a pair were `(2, q)`, then `q = N - 2` would be
   even, and an even prime is 2. That gives the pair `(2, 2)`, which repeats a
   prime, contradicting step 1.

Each step below is one lemma.
-/

namespace Wyrd

/-- A prime other than 2 is odd: if 2 divided it, 2 would have to be 1 or itself. -/
theorem IsPrime.odd {p : Nat} (hp : IsPrime p) (h2 : p ≠ 2) : p % 2 = 1 := by
  apply Nat.le_antisymm (by omega)
  apply Nat.pos_of_ne_zero
  intro h0
  rcases hp.2 2 (Nat.dvd_of_mod_eq_zero h0) with h | h <;> omega

/-- `primesOf` of a list `x :: xs` is `x.1 :: x.2 :: primesOf xs`. -/
theorem primesOf_cons (x : Nat × Nat) (xs : List (Nat × Nat)) :
    primesOf (x :: xs) = x.1 :: x.2 :: primesOf xs := rfl

/-- If the primes don't repeat, the two primes in each pair differ. -/
theorem pair_ne : ∀ (ps : List (Nat × Nat)), (primesOf ps).Nodup → ∀ pq ∈ ps, pq.1 ≠ pq.2
  | [], _, _, hm => absurd hm List.not_mem_nil
  | x :: xs, hnd, pq, hm => by
    rw [primesOf_cons, List.nodup_cons, List.nodup_cons] at hnd
    rcases List.mem_cons.mp hm with rfl | hm
    · exact fun heq => hnd.1 (List.mem_cons.mpr (Or.inl heq))
    · exact pair_ne xs hnd.2.2 pq hm

/-- Step 1. If the primes don't repeat and *every* pair contains 2, there is at
most one pair. Otherwise 2 would show up in the first pair and again later. -/
theorem length_le_one_of_all_two :
    ∀ (ps : List (Nat × Nat)), (primesOf ps).Nodup →
      (∀ pq ∈ ps, pq.1 = 2 ∨ pq.2 = 2) → ps.length ≤ 1
  | [], _, _ => by simp
  | [_], _, _ => by simp
  | x :: y :: ys, hnd, hall => by
    exfalso
    -- 2 occurs among the primes of `y :: ys` ...
    have hlater : 2 ∈ primesOf (y :: ys) := by
      rw [primesOf_cons]
      rcases hall y (by simp) with h | h <;> simp [h]
    -- ... and in the first pair `x`, contradicting no repeats.
    rw [primesOf_cons, List.nodup_cons, List.nodup_cons] at hnd
    rcases hall x (by simp) with h | h
    · exact hnd.1 (List.mem_cons_of_mem _ (h ▸ hlater))
    · exact hnd.2.1 (h ▸ hlater)

/-- Step 2. Some pair contains no 2. -/
theorem exists_pair_without_two {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) :
    ∃ pq ∈ ps, pq.1 ≠ 2 ∧ pq.2 ≠ 2 := by
  apply Classical.byContradiction
  intro hnone
  have hall : ∀ pq ∈ ps, pq.1 = 2 ∨ pq.2 = 2 := by
    intro pq hm
    apply Classical.byContradiction
    intro hc
    exact hnone ⟨pq, hm, fun e => hc (Or.inl e), fun e => hc (Or.inr e)⟩
  have := length_le_one_of_all_two ps (primes_nodup h) hall
  rw [h.five] at this
  omega

/-- Step 3. **Every pangram has an even sum.** -/
theorem sum_even {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) : N % 2 = 0 := by
  obtain ⟨pq, hm, h1, h2⟩ := exists_pair_without_two h
  have := (h.primes pq hm).1.odd h1
  have := (h.primes pq hm).2.odd h2
  have := h.sums pq hm
  omega

/-- Step 4. **No pangram uses the prime 2.** -/
theorem two_not_mem {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) :
    2 ∉ primesOf ps := by
  intro hmem
  obtain ⟨pq, hm, h2 | h2⟩ := mem_primesOf hmem
  all_goals
    have hs := h.sums pq hm
    have he := sum_even h
    have hne := pair_ne ps (primes_nodup h) pq hm
  · -- `pq = (2, q)`: `q` is a prime other than 2, so odd, so `N = 2 + q` is odd.
    have := (h.primes pq hm).2.odd (by omega)
    omega
  · -- `pq = (q, 2)`: the same, mirrored.
    have := (h.primes pq hm).1.odd (by omega)
    omega

end Wyrd
