import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The secondary rainbow sits at about 51°

For water (`n = 4/3`), the secondary bow is seen at angle `D - π` from the point
opposite the sun. Exactly, that angle is `π + 2·arccos √(7/72) - 6·arcsin √(65/128)`,
and numerically it is about 51.0°.
-/

namespace Wyrd.Rainbow

open Real

theorem secondary_bow_water_exact :
    dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π = π + 2 * arccos (√(7 / 72)) - 6 * arcsin (√(65 / 128)) := by
  sorry

/-- **The secondary rainbow is between 50° and 52°.** -/
theorem secondary_bow_water :
    50 * π / 180 < dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π ∧
      dev 2 (4 / 3) (bowIncidence 2 (4 / 3)) - π < 52 * π / 180 := by
  sorry

end Wyrd.Rainbow
