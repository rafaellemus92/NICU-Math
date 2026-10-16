import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The primary bow across the spectrum

Water's refractive index is about `1.331` for red light and `1.343` for violet.
The primary bow is then seen at about 42.37° (red) and 40.65° (violet), so the
coloured band is about 1.7° wide.
-/

namespace Wyrd.Rainbow

open Real

/-- Red light (`n = 1.331`): the primary bow lies between 42° and 43°. -/
theorem primary_red :
    42 * π / 180 < π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) ∧
      π - dev 1 (1331 / 1000) (bowIncidence 1 (1331 / 1000)) < 43 * π / 180 := by
  sorry

/-- Violet light (`n = 1.343`): the primary bow lies between 40° and 41°. -/
theorem primary_violet :
    40 * π / 180 < π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) ∧
      π - dev 1 (1343 / 1000) (bowIncidence 1 (1343 / 1000)) < 41 * π / 180 := by
  sorry

end Wyrd.Rainbow
