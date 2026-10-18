import Mathlib.NumberTheory.Bertrand
import Mathlib.Order.Bounds.Basic
import Wyrd.Euclid

/-!
# Bridge: our primes are Mathlib's primes

`Wyrd.IsPrime` (defined in core Lean, in `../wyrd`) says exactly what
Mathlib's `Nat.prime_def` says. So the two are interchangeable, and results
can move in both directions:

* **ours → Mathlib**: our proof of Euclid's theorem gives Mathlib's notion of
  "the set of primes is infinite";
* **Mathlib → ours**: Mathlib's Bertrand's postulate becomes a statement about
  our `IsPrime`, and the pangram's primes are `Nat.Prime`.
-/

namespace Wyrd

/-- **Our definition of prime is Mathlib's.** -/
theorem isPrime_iff (n : ℕ) : IsPrime n ↔ n.Prime := Nat.prime_def.symm

/-! ## Ours → Mathlib -/

/-- Our Euclid proof, restated with Mathlib's `Set.Infinite`: a set of natural
numbers with no upper bound is infinite. -/
theorem setOf_isPrime_infinite : {p | IsPrime p}.Infinite := by
  apply Set.infinite_of_not_bddAbove
  rintro ⟨B, hB⟩
  exact primes_infinite ⟨B, fun p hp => hB hp⟩

/-- The same, for Mathlib's own primes, proved by our core-Lean Euclid. -/
theorem setOf_prime_infinite : {p : ℕ | p.Prime}.Infinite := by
  simpa only [isPrime_iff] using setOf_isPrime_infinite

/-- The ten pangram primes are primes in Mathlib's sense too. -/
theorem solution_primes : ∀ pq ∈ solution, pq.1.Prime ∧ pq.2.Prime := by
  intro pq h
  obtain ⟨h1, h2⟩ := solution_isPangram.primes pq h
  exact ⟨(isPrime_iff _).mp h1, (isPrime_iff _).mp h2⟩

/-! ## Mathlib → ours -/

/-- **Bertrand's postulate**, for our `IsPrime`: for `n ≥ 1` there is a prime
`p` with `n < p ≤ 2n`. The hard work is Mathlib's (`Nat.bertrand`); the bridge
makes it ours. -/
theorem bertrand {n : ℕ} (hn : n ≠ 0) : ∃ p, IsPrime p ∧ n < p ∧ p ≤ 2 * n := by
  obtain ⟨p, hp, h1, h2⟩ := Nat.bertrand n hn
  exact ⟨p, (isPrime_iff p).mpr hp, h1, h2⟩

end Wyrd
