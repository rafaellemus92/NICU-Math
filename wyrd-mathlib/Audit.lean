import WyrdMathlib
/-! Run `lake env lean Audit.lean`: only `propext`, `Classical.choice`,
`Quot.sound` should appear, never `sorryAx` or `Lean.ofReduceBool`. -/
#print axioms Wyrd.isPrime_iff
#print axioms Wyrd.setOf_prime_infinite
#print axioms Wyrd.solution_primes
#print axioms Wyrd.bertrand
