import WyrdMathlib.Rainbow.Defs
import WyrdMathlib.Rainbow.TrigBounds
import Mathlib.Analysis.Real.Pi.Bounds

/-!
# The primary rainbow sits at about 42°

For water (`n = 4/3`), the primary bow is seen at angle `π - D` from the point
opposite the sun. Exactly, that angle is `4·arcsin √(5/12) - 2·arccos √(7/27)`,
and numerically it is about 42.0°.
-/

namespace Wyrd.Rainbow

open Real

theorem primary_bow_water_exact :
    π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) = 4 * arcsin (√(5 / 12)) - 2 * arccos (√(7 / 27)) := by
  sorry

/-- **The primary rainbow is between 41° and 43°.** -/
theorem primary_bow_water :
    41 * π / 180 < π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) ∧
      π - dev 1 (4 / 3) (bowIncidence 1 (4 / 3)) < 43 * π / 180 := by
  sorry

end Wyrd.Rainbow
