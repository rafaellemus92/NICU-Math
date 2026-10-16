import WyrdMathlib.PeriodicNS.Averages

/-!
# Same spectrum, opposite enstrophy change

For amplitude `A`, the fields `±A v` have the same energy `A²`, enstrophy `5A²/4`,
dissipation `7A²/2`, and the same Fourier magnitude at every wave vector. But the
cubic stretching term flips sign: `S = ±A³/4`. So the enstrophy rate `S − νD`
from the standard balance is `A³/4 − 7νA²/2` for one and `−A³/4 − 7νA²/2` for the
other: of opposite signs once `A > 14ν`. With `A = 1`, `ν = 1/28` the rates are
`1/8` and `−3/8`.

Consequence: no rule `dZ/dt = Φ(E, Z, D, ν)` can hold for all solutions. The
same inputs would need two different outputs. Neither field is claimed to blow
up; this only shows what magnitude-only descriptions lose.
-/

namespace Wyrd.PeriodicNS

open Real

/-- **The quantities of `A v`.** -/
theorem quantities_smul (A : ℝ) :
    (v.smul A).energy = A ^ 2 ∧ (v.smul A).enstrophy = 5 * A ^ 2 / 4 ∧
      (v.smul A).palin = 7 * A ^ 2 / 2 ∧ (v.smul A).stretching = A ^ 3 / 4 := by
  sorry

/-- With `A = 1`, `ν = 1/28`: enstrophy rates `1/8` for `v` and `−3/8` for `−v`. -/
theorem rates :
    (v.smul 1).stretching - 1 / 28 * (v.smul 1).palin = 1 / 8 ∧
      (v.smul (-1)).stretching - 1 / 28 * (v.smul (-1)).palin = -3 / 8 := by
  sorry

/-- **Opposite signs** whenever `A > 14ν > 0`. -/
theorem opposite_signs {A ν : ℝ} (hν : 0 < ν) (hA : 14 * ν < A) :
    0 < (v.smul A).stretching - ν * (v.smul A).palin ∧
      (v.smul (-A)).stretching - ν * (v.smul (-A)).palin < 0 := by
  sorry

/-- **Identical Fourier magnitudes at every wave vector.** -/
theorem same_spectrum (A : ℝ) (k : ℤ × ℤ × ℤ) :
    ‖coeff (v.smul (-A)).u1 k‖ = ‖coeff (v.smul A).u1 k‖ ∧
      ‖coeff (v.smul (-A)).u2 k‖ = ‖coeff (v.smul A).u2 k‖ ∧
      ‖coeff (v.smul (-A)).u3 k‖ = ‖coeff (v.smul A).u3 k‖ := by
  sorry

/-- **No closed enstrophy law in `(E, Z, D, ν)`.** -/
theorem no_closure :
    ¬ ∃ Φ : ℝ → ℝ → ℝ → ℝ → ℝ, ∀ u ∈ ({v.smul 1, v.smul (-1)} : Set Field),
      u.stretching - 1 / 28 * u.palin = Φ u.energy u.enstrophy u.palin (1 / 28) := by
  sorry

end Wyrd.PeriodicNS
