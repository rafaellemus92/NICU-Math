import WyrdMathlib.PeriodicNS.Example

/-!
# The exact averages for the example field

Genuine integrals over `[0, 2π]³`: `E = 1`, `Z = 5/4`, `D = 7/2`, `S = 1/4`, and
`⟨|∇v|²⟩ = 5/2`.
-/

namespace Wyrd.PeriodicNS

open Real

/-- **The quantities of `v`.** -/
theorem quantities_v :
    v.energy = 1 ∧ v.enstrophy = 5 / 4 ∧ v.palin = 7 / 2 ∧ v.stretching = 1 / 4 ∧ v.gradSq = 5 / 2 := by
  sorry

end Wyrd.PeriodicNS
