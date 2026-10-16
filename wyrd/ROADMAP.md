# Roadmap

Goals in rough order of difficulty. ✅ = proved, ⬜ = open.

## The pangram

- ✅ The coupled encoding is reversible (`decode_encode`).
- ✅ The 4296 solution is correct (`solution_isPangram`).
- ✅ Every pangram has `N ≥ 1352` (`lower_bound`).
- ⬜ **The ten primes in any pangram are distinct.** This follows from
  "every letter exactly once" plus injectivity. It's a good first exercise,
  using `List.Nodup` and `List.Perm.nodup_iff`.
- ⬜ **Every pangram has `N` even, and never uses the prime 2.** Hint: 2 is
  the only even prime, and it can appear in at most one pair. What parity do
  the other four pairs force on `N`? Work it out on paper first.
- ⬜ **4296 is the smallest `N`.** The Python script checks this by
  exhaustive search. To prove it in Lean, write the search as a Lean function,
  prove it *sound* (if it says "no pangram at N", there is none), then have
  the kernel run it on every even `N` from 1352 to 4294. Making it fast
  enough for `decide +kernel` is the real challenge. `native_decide` would be
  quick but trusts the compiler, so it doesn't count here.
- ⬜ **Plain base-26 has no pangram up to 18,250.** Same method as above.

## Beyond

- ⬜ Add Mathlib, then re-prove `IsPrime` equivalent to Mathlib's `Nat.Prime`.
- ⬜ Classic theorems as practice: infinitely many primes, √2 irrational,
  Bertrand's postulate (Mathlib already has these, so try them without it
  first).
- ⬜ Goldbach for even `N` up to some bound. It is a finite check, so this
  is doable. The full conjecture is open and won't be settled here, but
  formalising *exactly* what is known is honest work.
