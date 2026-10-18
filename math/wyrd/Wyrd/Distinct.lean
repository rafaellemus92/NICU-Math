import Wyrd.Pangram

/-!
# The ten primes in a pangram are distinct

Paper proof: every letter appears exactly once, so the letter list has no
repeats. If a prime appeared twice among the ten, its name would appear twice
in the letter list. A prime is at least 2, so its name has at least one letter,
and that letter would repeat. Contradiction.

The Lean proof follows the same three steps:

1. `nodup_letters`: the letter list has no repeats (it's a permutation of `0…25`);
2. `letters_eq`: the letter list is the names of the ten primes, joined up;
3. `nodup_of_nodup_flatMap`: if joining non-empty blocks gives no repeats,
   then the blocks' labels had no repeats either.
-/

namespace Wyrd

/-- The ten primes of a pangram, in order: `[p₁, q₁, p₂, q₂, …]`. -/
def primesOf (ps : List (Nat × Nat)) : List Nat :=
  ps.flatMap fun pq => [pq.1, pq.2]

/-- Step 1. No letter repeats: a permutation of a list without repeats has none. -/
theorem nodup_letters {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) :
    (letters ps).Nodup :=
  h.alphabet.nodup_iff.mpr List.nodup_range

/-- Step 2. The letters are the names of the ten primes, joined in order. -/
theorem letters_eq (ps : List (Nat × Nat)) : letters ps = (primesOf ps).flatMap encode := by
  simp [letters, primesOf, List.flatMap_assoc]

/-- Step 3, the heart of the proof. If each `x` becomes a non-empty block `f x`
and joining the blocks gives a list without repeats, then `l` had no repeats.
By induction on `l`: for `x :: xs`, the block `f x` shares nothing with the
blocks of `xs`. If `x` were also in `xs`, then `f x` would be one of those
blocks, so any letter of `f x` would occur twice. -/
theorem nodup_of_nodup_flatMap {α β : Type} (f : α → List β) :
    ∀ (l : List α), (∀ x ∈ l, f x ≠ []) → (l.flatMap f).Nodup → l.Nodup
  | [], _, _ => List.nodup_nil
  | x :: xs, hne, hnd => by
    rw [List.flatMap_cons, List.nodup_append] at hnd
    obtain ⟨_, hrest, hdisj⟩ := hnd
    rw [List.nodup_cons]
    refine ⟨fun hx => ?_, ?_⟩
    · -- `x ∈ xs`: take any letter `b` of `f x`; it is in both halves.
      obtain ⟨b, hb⟩ := List.exists_mem_of_ne_nil (f x) (hne x (List.mem_cons_self ..))
      exact hdisj b hb b (List.mem_flatMap.mpr ⟨x, hx, hb⟩) rfl
    · exact nodup_of_nodup_flatMap f xs
        (fun y hy => hne y (List.mem_cons_of_mem _ hy)) hrest

/-- A positive number's name has at least one letter. -/
theorem encode_ne_nil {n : Nat} (hn : 0 < n) : encode n ≠ [] := by
  intro h
  have hlen := congrArg List.length h
  rw [length_encode] at hlen
  obtain ⟨k, rfl⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  simp [digits, digitsAux] at hlen

/-- Every member of `primesOf ps` is the first or second prime of some pair. -/
theorem mem_primesOf {ps : List (Nat × Nat)} {x : Nat} (hx : x ∈ primesOf ps) :
    ∃ pq ∈ ps, x = pq.1 ∨ x = pq.2 := by
  simp only [primesOf, List.mem_flatMap, List.mem_cons, List.not_mem_nil, or_false] at hx
  exact hx

/-- **The ten primes in any pangram are pairwise distinct.** -/
theorem primes_nodup {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) :
    (primesOf ps).Nodup := by
  apply nodup_of_nodup_flatMap encode
  · intro x hx
    obtain ⟨pq, hpq, rfl | rfl⟩ := mem_primesOf hx
    · exact encode_ne_nil (by have := (h.primes pq hpq).1.1; omega)
    · exact encode_ne_nil (by have := (h.primes pq hpq).2.1; omega)
  · rw [← letters_eq]
    exact nodup_letters h

/-- And there really are ten of them. -/
theorem length_primesOf {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) :
    (primesOf ps).length = 10 := by
  have : ∀ l : List (Nat × Nat), (primesOf l).length = 2 * l.length := by
    intro l; induction l with
    | nil => rfl
    | cons _ _ ih => simp [primesOf] at ih ⊢; omega
  rw [this, h.five]

end Wyrd
