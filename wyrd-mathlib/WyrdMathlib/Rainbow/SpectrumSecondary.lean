import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The secondary bow across the spectrum

With `n ≈ 1.331` (red) and `1.343` (violet), the secondary bow is seen at about
50.37° (red) and 53.48° (violet): about 3.1° wide, colours reversed.
-/

namespace Wyrd.Rainbow

open Real

/-- Red light (`n = 1.331`): the secondary bow lies between 50° and 51°. -/
theorem secondary_red :
    50 * π / 180 < dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π ∧
      dev 2 (1331 / 1000) (bowIncidence 2 (1331 / 1000)) - π < 51 * π / 180 := by
  sorry

/-- Violet light (`n = 1.343`): the secondary bow lies between 53° and 54°. -/
theorem secondary_violet :
    53 * π / 180 < dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π ∧
      dev 2 (1343 / 1000) (bowIncidence 2 (1343 / 1000)) - π < 54 * π / 180 := by
  sorry

end Wyrd.Rainbow
