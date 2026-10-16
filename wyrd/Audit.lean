import Wyrd
/-! Run `lake env lean Audit.lean`. Each line should list only Lean's standard
axioms (`propext`, `Classical.choice`, `Quot.sound`) — never `sorryAx`
(an unfinished proof) or `Lean.ofReduceBool` (trusting compiled code). -/
#print axioms Wyrd.decode_encode
#print axioms Wyrd.encode_injective
#print axioms Wyrd.solution_names
#print axioms Wyrd.solution_isPangram
#print axioms Wyrd.lower_bound
