import Wyrd.Encoding

/-!
# Five-pair prime pangrams

A *prime pangram with sum `N`* is a list of five pairs of primes `(p, q)` with
`p + q = N`, whose ten names together use each letter A–Z exactly once.

Proved here:

* `solution_isPangram` — the pairs found by `../coupled_prime26_pangram.py`
  form a pangram with `N = 4296` (checked by the Lean kernel, no trust in Python);
* `lower_bound` — every pangram has `N ≥ 1352`, for any choice of pairs.

Not yet proved: that 4296 is the *smallest* `N` (see `ROADMAP.md`).
-/

namespace Wyrd

/-! ## Primes

Core Lean has no notion of prime, so we define one and a checker for it. The
checker is only trusted because `primeB_sound` proves it correct. -/

/-- `n` is prime: at least 2, and its only divisors are 1 and itself. -/
def IsPrime (n : Nat) : Prop := 2 ≤ n ∧ ∀ m, m ∣ n → m = 1 ∨ m = n

/-- Trial division: no `m` with `2 ≤ m < n` divides `n`. Slow but simple. -/
def primeB (n : Nat) : Bool :=
  2 ≤ n && (List.range' 2 (n - 2)).all fun m => n % m != 0

theorem primeB_sound {n : Nat} (h : primeB n = true) : IsPrime n := by
  simp only [primeB, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    List.mem_range'_1, bne_iff_ne, ne_eq] at h
  obtain ⟨h2, hdiv⟩ := h
  refine ⟨h2, fun m hm => ?_⟩
  have hle : m ≤ n := Nat.le_of_dvd (by omega) hm
  have hm0 : m ≠ 0 := by rintro rfl; simp at hm; omega
  by_cases h1 : m = 1
  · exact Or.inl h1
  by_cases hn : m = n
  · exact Or.inr hn
  exact absurd (Nat.mod_eq_zero_of_dvd hm) (hdiv m (by omega))

/-! ## Pangrams -/

/-- All letter codes of all ten names, in order. -/
def letters (ps : List (Nat × Nat)) : List Nat :=
  ps.flatMap fun pq => encode pq.1 ++ encode pq.2

/-- Five prime pairs, each summing to `N`, whose names use every letter exactly
once. "Exactly once" is a permutation of `[0, 1, …, 25]`. -/
structure IsPangram (N : Nat) (ps : List (Nat × Nat)) : Prop where
  five : ps.length = 5
  sums : ∀ pq ∈ ps, pq.1 + pq.2 = N
  primes : ∀ pq ∈ ps, IsPrime pq.1 ∧ IsPrime pq.2
  alphabet : (letters ps).Perm (List.range 26)

/-! ## The certificate for N = 4296 -/

def solution : List (Nat × Nat) :=
  [(1187, 3109), (53, 4243), (349, 3947), (293, 4003), (659, 3637)]

/-- The names, as the Python script prints them. -/
theorem solution_names :
    solution.map (fun pq => (name pq.1, name pq.2)) =
      [("UKR", "TEP"), ("DB", "NMF"), ("YL", "AQV"), ("SH", "CWZ"), ("IJ", "OGX")] := by
  decide +kernel

theorem solution_isPangram : IsPangram 4296 solution where
  five := rfl
  sums := by decide
  primes := by
    have h : solution.all (fun pq => primeB pq.1 && primeB pq.2) = true := by decide +kernel
    intro pq hpq
    have := List.all_eq_true.mp h pq hpq
    simp only [Bool.and_eq_true] at this
    exact ⟨primeB_sound this.1, primeB_sound this.2⟩
  alphabet := by decide +kernel

/-- **A five-pair prime pangram exists, with sum 4296.** -/
theorem pangram_exists : ∃ ps, IsPangram 4296 ps := ⟨solution, solution_isPangram⟩

/-! ## The lower bound N ≥ 1352

Idea: if `N < 1352 = 2 · 676`, then in every pair one prime is below `676 = 26²`,
so its name has at most 2 letters, and the other is below `26³`, so at most 3.
Five pairs then hold at most 25 letters, one short of the alphabet. -/

theorem pair_short {p q N : Nat} (hs : p + q = N) (hN : N < 1352) :
    (encode p ++ encode q).length ≤ 5 := by
  rw [List.length_append]
  by_cases hp : p < 676
  · have := length_encode_le_two hp
    have := length_encode_le_three (n := q) (by omega)
    omega
  · have := length_encode_le_two (n := q) (by omega)
    have := length_encode_le_three (n := p) (by omega)
    omega

theorem length_flatMap_le_five {α : Type} (l : List α) (f : α → List Nat)
    (h : ∀ x ∈ l, (f x).length ≤ 5) : (l.flatMap f).length ≤ 5 * l.length := by
  induction l with
  | nil => simp
  | cons x xs ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_cons]
    have := h x (List.mem_cons_self ..)
    have := ih (fun y hy => h y (List.mem_cons_of_mem _ hy))
    omega

/-- **Every five-pair prime pangram has sum at least 1352.** -/
theorem lower_bound {N : Nat} {ps : List (Nat × Nat)} (h : IsPangram N ps) : 1352 ≤ N := by
  apply Nat.le_of_not_lt
  intro hN
  have hlen : (letters ps).length = 26 := by
    rw [h.alphabet.length_eq, List.length_range]
  have hle : (letters ps).length ≤ 5 * ps.length :=
    length_flatMap_le_five ps _ fun pq hpq => pair_short (h.sums pq hpq) hN
  rw [h.five] at hle
  omega

end Wyrd
