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
  have h1 : ∀ y : ℝ, -sin (-y) = sin y := fun y => by rw [sin_neg]; ring
  have h2 : ∀ z : ℝ, -sin (z + π) = sin z := fun z => by rw [sin_add_pi]; ring
  have h3 : ∀ x y : ℝ, cos (-x) - cos (-x + -y + φ) = cos x - cos (x + y + -φ) := fun x y => by
    rw [cos_neg, show -x + -y + φ = -(x + y + -φ) by ring, cos_neg]
  simp only [rotShift, vphi, h1, h2, h3]

theorem mirror_fixes_vphi (φ : ℝ) : mirror (vphi φ) = vphi φ := by
  have h2 : ∀ z : ℝ, sin (-z - π) = sin z := fun z => by
    rw [show -z - π = -(z + π) by ring, sin_neg, sin_add_pi]; ring
  have h3 : ∀ x y : ℝ, -(cos (x + π) - cos (x + π + y + φ)) = cos x - cos (x + y + φ) :=
    fun x y => by
      rw [cos_add_pi, show x + π + y + φ = (x + y + φ) + π by ring, cos_add_pi]; ring
  simp only [mirror, vphi, h2, h3]

theorem quantities_even (φ : ℝ) :
    (vphi (-φ)).energy = (vphi φ).energy ∧ (vphi (-φ)).enstrophy = (vphi φ).enstrophy ∧
      (vphi (-φ)).palin = (vphi φ).palin ∧ (vphi (-φ)).stretching = (vphi φ).stretching := by
  obtain ⟨hE, hZ, hD, hS⟩ := quantities_vphi φ
  obtain ⟨hE', hZ', hD', hS'⟩ := quantities_vphi (-φ)
  exact ⟨by rw [hE, hE'], by rw [hZ, hZ'], by rw [hD, hD'], by rw [hS, hS', cos_neg]⟩

end Wyrd.PeriodicNS
