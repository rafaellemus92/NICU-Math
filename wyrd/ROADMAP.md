# Roadmap

Goals in rough order of difficulty. ✅ = proved, ⬜ = open.

## The pangram

- ✅ The coupled encoding is reversible (`decode_encode`).
- ✅ The 4296 solution is correct (`solution_isPangram`).
- ✅ Every pangram has `N ≥ 1352` (`lower_bound`).
- ✅ The ten primes in any pangram are distinct (`primes_nodup`).
- ✅ Every pangram has `N` even and never uses the prime 2 (`sum_even`, `two_not_mem`).
- ✅ 4296 is the smallest `N` (`smallest_pangram_sum`). A kernel-run search over
  all 1,472 remaining even sums, proved complete. No `native_decide`.
- ⬜ **Plain base-26 has no pangram up to 18,250.** Same method as the
  minimality proof, with the plain encoding swapped in. Expect a longer kernel
  run: about 8,450 sums, with larger primes.
- ⬜ **Speed up the minimality check.** Letter sets as bitmasks would make
  the kernel search much faster, but the proofs would need lemmas about bits.

## Beyond

- ⬜ Add Mathlib, then re-prove `IsPrime` equivalent to Mathlib's `Nat.Prime`.
- ⬜ Classic theorems as practice: infinitely many primes, √2 irrational,
  Bertrand's postulate (Mathlib already has these, so try them without it
  first).
- ⬜ Goldbach for even `N` up to some bound. It is a finite check, so this
  is doable. The full conjecture is open and won't be settled here, but
  formalising *exactly* what is known is honest work.
