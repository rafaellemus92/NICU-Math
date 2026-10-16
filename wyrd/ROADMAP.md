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

- ✅ Connect to Mathlib: `IsPrime ↔ Nat.Prime` (`../wyrd-mathlib`, `isPrime_iff`).
- ✅ Infinitely many primes (`primes_infinite`), in core Lean with our own
  factorial and prime-factor lemmas.
- ⬜ Prove Bertrand's postulate ourselves. Right now `bertrand` borrows
  Mathlib's proof through the bridge.
- ✅ √2 is irrational: infinite descent in core Lean (`no_fraction_squares_to_two`),
  lifted to the real number in `../wyrd-mathlib` (`irrational_sqrt_two`).
- ✅ The rainbow (`../wyrd-mathlib/WyrdMathlib/Rainbow/`): the k-th bow at
  `cos² i = (n² − 1)/(k(k+2))` is the unique strict minimum of the deviation;
  for water the bows sit at 41–43° and 50–52°, with Alexander's dark band
  between them.
- ✅ Rainbow colours (`Colours.lean`, `Spectrum*.lean`, `VisibleBand.lean`): the
  primary bow shrinks and the secondary grows with `n`, so red is outside the
  primary and inside the secondary; real-water brackets for red and violet; the
  dark band holds for every colour from red up.
- ⬜ Rainbow width to 0.1°: tighter arcsin brackets would prove the ~1.7° and
  ~3.1° band widths, not just more than 1° and 2°.
- ⬜ Goldbach for even `N` up to some bound. It is a finite check, so this
  is doable. The full conjecture is open and won't be settled here, but
  formalising *exactly* what is known is honest work.
