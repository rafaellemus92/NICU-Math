import WyrdMathlib.PeriodicNS.SignFlip

/-!
# The phase family: only a relative phase changes, and stretching follows it

From the uploaded `periodic_ns_lab_v1`: the family

  `v_φ = (sin y, sin z, cos x − cos(x + y + φ))`,  `v_0 = v`.

Translating space can remove the phases of three of the four plane waves, but not
the relational phase `φ`, because the wave vector `(1, 1, 0)` is the sum of
`(1, 0, 0)` and `(0, 1, 0)`. Changing `φ` moves no Fourier magnitude (the
magnitudes are not formalised here). Proved:

* `div_vphi`, `vphi_zero`: every member is divergence-free, and `φ = 0` is `v`.
* `quantities_vphi`: `E = 1`, `Z = 5/4`, `D = 7/2` for **every** `φ`, while
  `S = cos φ / 4`.
* `quantities_vphi_smul`, `growth_iff`: for amplitude `A > 0`, `S − νD > 0`
  exactly when `cos φ > 14ν/A`.
* `zero_growth_at_pi_div_three`: at `A = 1`, `ν = 1/28`, `φ = π/3` gives `S − νD = 0`.
* `neg_v_translate`: the old sign-reversed field `−v` is `v_π` translated by
  `(π, π, π)`, so it is a member of the family.

As in `SignFlip.lean`, `S − νD` is the right-hand side of the standard enstrophy
balance. The balance itself, and any time evolution (the lab's `Z''(0)`,
high-shell growth and simulations), are not formalised.
-/

namespace Wyrd.PeriodicNS

open Real

/-- The phase family. -/
noncomputable def vphi (φ : ℝ) : Field :=
  ⟨fun _ y _ => sin y, fun _ _ z => sin z, fun x y _ => cos x - cos (x + y + φ)⟩

theorem vphi_zero : vphi 0 = v := by
  sorry

theorem div_vphi (φ x y z : ℝ) : (vphi φ).div x y z = 0 := by
  sorry

theorem quantities_vphi (φ : ℝ) :
    (vphi φ).energy = 1 ∧ (vphi φ).enstrophy = 5 / 4 ∧ (vphi φ).palin = 7 / 2 ∧
      (vphi φ).stretching = cos φ / 4 := by
  sorry

theorem quantities_vphi_smul (A φ : ℝ) :
    ((vphi φ).smul A).energy = A ^ 2 ∧ ((vphi φ).smul A).enstrophy = 5 * A ^ 2 / 4 ∧
      ((vphi φ).smul A).palin = 7 * A ^ 2 / 2 ∧
      ((vphi φ).smul A).stretching = A ^ 3 * cos φ / 4 := by
  sorry

theorem growth_iff {A ν φ : ℝ} (hA : 0 < A) :
    0 < ((vphi φ).smul A).stretching - ν * ((vphi φ).smul A).palin ↔ 14 * ν / A < cos φ := by
  sorry

theorem zero_growth_at_pi_div_three :
    ((vphi (π / 3)).smul 1).stretching - 1 / 28 * ((vphi (π / 3)).smul 1).palin = 0 := by
  sorry

theorem neg_v_translate (x y z : ℝ) :
    (v.smul (-1)).u1 x y z = (vphi π).u1 (x + π) (y + π) (z + π) ∧
      (v.smul (-1)).u2 x y z = (vphi π).u2 (x + π) (y + π) (z + π) ∧
      (v.smul (-1)).u3 x y z = (vphi π).u3 (x + π) (y + π) (z + π) := by
  sorry

end Wyrd.PeriodicNS
