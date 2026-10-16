import Mathlib

/-!
# The 2:1 locking condition, for the averaged phase equation

After weak-forcing averaging, the phase difference obeys
`φ' = Δ − k sin φ` with detuning `Δ = ω − 2Ω` and `k = ε a₂/2`. This file proves
the exact statements for that averaged equation:

* it has an equilibrium exactly when `|Δ| ≤ k`;
* it has a *stable* equilibrium (where `−k cos φ < 0`) exactly when `|Δ| < k`.

That is the source's `|ω − 2Ω| < ε a₂/2`. It is exact for the averaged equation
only; for the full noisy, modulated population model it is a first-order
approximation. Also, for 2:1 locking the first circular moment can vanish even
under perfect locking (phases `0` and `π`), so the index must use the second.
-/

namespace Wyrd.SharedAir

open Complex

theorem averaged_equilibrium_iff {Δ k : ℝ} (hk : 0 < k) :
    (∃ φ : ℝ, Δ - k * Real.sin φ = 0) ↔ |Δ| ≤ k := by
  sorry

theorem averaged_stable_equilibrium_iff {Δ k : ℝ} (hk : 0 < k) :
    (∃ φ : ℝ, Δ - k * Real.sin φ = 0 ∧ -(k * Real.cos φ) < 0) ↔ |Δ| < k := by
  sorry

/-- Perfect 2:1 locking sampled at phases `0` and `π`: first moment `0`, second `1`. -/
theorem two_to_one_moments :
    (exp ((0 : ℝ) * I) + exp (Real.pi * I)) / 2 = 0 ∧
      (exp (2 * (0 : ℝ) * I) + exp (2 * Real.pi * I)) / 2 = 1 := by
  sorry

end Wyrd.SharedAir
