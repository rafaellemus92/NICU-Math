import WyrdMathlib
/-! Run `lake env lean Audit.lean`: only `propext`, `Classical.choice`,
`Quot.sound` should appear, never `sorryAx` or `Lean.ofReduceBool`. -/
#print axioms Wyrd.isPrime_iff
#print axioms Wyrd.setOf_prime_infinite
#print axioms Wyrd.solution_primes
#print axioms Wyrd.bertrand
#print axioms Wyrd.irrational_sqrt_two
#print axioms Wyrd.Rainbow.snell
#print axioms Wyrd.Rainbow.taylor7_le_sin
#print axioms Wyrd.Rainbow.hasDerivAt_dev
#print axioms Wyrd.Rainbow.deriv_dev_eq_zero_iff_eq
#print axioms Wyrd.Rainbow.dev_lt_of_ne
#print axioms Wyrd.Rainbow.dev_isMinOn
#print axioms Wyrd.Rainbow.water_primary
#print axioms Wyrd.Rainbow.water_secondary
#print axioms Wyrd.Rainbow.primary_bow_water
#print axioms Wyrd.Rainbow.secondary_bow_water
#print axioms Wyrd.Rainbow.alexander_dark_band
