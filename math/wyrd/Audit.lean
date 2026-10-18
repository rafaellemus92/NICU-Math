import Wyrd
/-! Run `lake env lean Audit.lean`. Each line should list only Lean's standard
axioms (`propext`, `Classical.choice`, `Quot.sound`) — never `sorryAx`
(an unfinished proof) or `Lean.ofReduceBool` (trusting compiled code). -/
#print axioms Wyrd.decode_encode
#print axioms Wyrd.encode_injective
#print axioms Wyrd.solution_names
#print axioms Wyrd.solution_isPangram
#print axioms Wyrd.lower_bound
#print axioms Wyrd.primes_nodup
#print axioms Wyrd.length_primesOf
#print axioms Wyrd.sum_even
#print axioms Wyrd.two_not_mem
#print axioms Wyrd.no_smaller_pangram
#print axioms Wyrd.smallest_pangram_sum
#print axioms Wyrd.exists_prime_gt
#print axioms Wyrd.primes_infinite
#print axioms Wyrd.no_fraction_squares_to_two
