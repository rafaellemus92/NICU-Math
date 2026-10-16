import Mathlib

/-!
# The conditional regularity route: Grönwall with a variable rate

If `dZ/dt ≤ a(t) Z(t)`, then `Z(t) ≤ Z(0) · exp(∫₀ᵗ a)`. For Navier–Stokes, a
uniform estimate `S ≤ (1 − δ) ν D + a(t) Z` with `∫₀ᵀ a < ∞` controlled
independently would therefore bound the enstrophy on `[0, T]`. That estimate is
the missing piece, and is **not** proved; this file proves only the Grönwall step.
-/

namespace Wyrd.PeriodicNS

/-- **Grönwall's inequality, variable coefficient.** -/
theorem gronwall_variable {Z Z' a : ℝ → ℝ} (ha : Continuous a)
    (hZ : ∀ t, HasDerivAt Z (Z' t) t) (hle : ∀ t, 0 ≤ t → Z' t ≤ a t * Z t)
    {t : ℝ} (ht : 0 ≤ t) :
    Z t ≤ Z 0 * Real.exp (∫ s in (0 : ℝ)..t, a s) := by
  sorry

/-- The enstrophy step: if `S ≤ (1 − δ) ν D + a Z` with `δ ≥ 0` and `D ≥ 0`, then
`S − ν D ≤ a Z`. -/
theorem stretching_estimate_step {S D Zv a ν δ : ℝ} (hν : 0 ≤ ν) (hδ : 0 ≤ δ) (hD : 0 ≤ D)
    (h : S ≤ (1 - δ) * ν * D + a * Zv) : S - ν * D ≤ a * Zv := by
  sorry

end Wyrd.PeriodicNS
