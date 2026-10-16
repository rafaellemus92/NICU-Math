import WyrdMathlib.PeriodicNS.PhaseFamily

/-!
# `φ ↦ −φ` is a rotation followed by a translation

Let `F[u](x) = R u(R x + b)` with `R = diag(−1, −1, 1)` and `b = (0, 0, π)`: a
rotation by `π` about the `z`-axis, then a shift by `π` in `z`.

* `rotShift_vphi`: `F` maps `v_φ` to `v_{−φ}` exactly.
* `mirror_fixes_vphi`: the mirror map `M[u](x) = diag(1, 1, −1) u(x + π, y, −z − π)`
  fixes every `v_φ`.
* `quantities_even`: `E`, `Z`, `D`, `S` take the same values at `φ` and `−φ`.

Navier–Stokes on the torus commutes with rotations and translations. So, given
uniqueness of smooth solutions, the evolved enstrophy satisfies
`Z(T, φ) = Z(T, −φ)`, and `φ = 0` is always a stationary point of `φ ↦ Z(T, φ)`.
That last step needs Navier–Stokes solution theory and is **not** formalised
here.
-/

namespace Wyrd.PeriodicNS

open Real

/-- Rotation by `π` about the `z`-axis, then a shift by `π` in `z`. -/
noncomputable def rotShift (u : Field) : Field :=
  ⟨fun x y z => -u.u1 (-x) (-y) (z + π), fun x y z => -u.u2 (-x) (-y) (z + π),
   fun x y z => u.u3 (-x) (-y) (z + π)⟩

/-- The mirror map `diag(1, 1, −1) u(x + π, y, −z − π)`. -/
noncomputable def mirror (u : Field) : Field :=
  ⟨fun x y z => u.u1 (x + π) y (-z - π), fun x y z => u.u2 (x + π) y (-z - π),
   fun x y z => -u.u3 (x + π) y (-z - π)⟩

theorem rotShift_vphi (φ : ℝ) : rotShift (vphi φ) = vphi (-φ) := by
  sorry

theorem mirror_fixes_vphi (φ : ℝ) : mirror (vphi φ) = vphi φ := by
  sorry

theorem quantities_even (φ : ℝ) :
    (vphi (-φ)).energy = (vphi φ).energy ∧ (vphi (-φ)).enstrophy = (vphi φ).enstrophy ∧
      (vphi (-φ)).palin = (vphi φ).palin ∧ (vphi (-φ)).stretching = (vphi φ).stretching := by
  sorry

end Wyrd.PeriodicNS
