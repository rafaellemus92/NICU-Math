# wyrd-mathlib: our proofs, connected to Mathlib

A sister project to [`../wyrd`](../wyrd). It depends on both
[Mathlib](https://github.com/leanprover-community/mathlib4) (`v4.35.0`, the
same Lean version as `wyrd`) and on `wyrd` itself. `wyrd` stays core-Lean
only, so it builds without the 7 GB Mathlib download.

## What's here

| Theorem | Statement |
|---|---|
| `isPrime_iff` | Our `IsPrime` is exactly Mathlib's `Nat.Prime` |
| `setOf_prime_infinite` | Mathlib's "the primes form an infinite set", proved by **our** Euclid |
| `solution_primes` | The ten pangram primes are `Nat.Prime` |
| `bertrand` | Bertrand's postulate (a prime between `n` and `2n`) for our `IsPrime`, from Mathlib's `Nat.bertrand` |

Once the bridge exists, anything Mathlib knows about primes applies to our
results, and the reverse.

## Running it

```sh
cd experiments/wyrd-mathlib
lake exe cache get          # download Mathlib's prebuilt files (~3 min, ~7 GB)
lake build
lake env lean Audit.lean    # axioms used: no sorry, no native_decide
```

Skipping `cache get` means building Mathlib from source, which takes hours.
