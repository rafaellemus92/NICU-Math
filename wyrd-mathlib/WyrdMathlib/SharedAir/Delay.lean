import WyrdMathlib.SharedAir.Basic

/-!
# With delay: high coupling is unstable for every delay

Keeping the delay `τ` on the coupled terms, the characteristic equation is

  `D(s) = (s + a)(s + b)(s + d) + h g (s + b) e^{-sτ} − c g² (s + d) e^{-2sτ} = 0`.

At `s = 0` the delay factors are `1`, so `D(0) = P(0, g)`. If that is negative,
`D` must cross zero at some real `s > 0`, whatever the delay: an exponentially
growing mode.
-/

namespace Wyrd.SharedAir

/-- The delayed characteristic function on the real axis. -/
noncomputable def Dd (a b d c h g τ s : ℝ) : ℝ :=
  (s + a) * (s + b) * (s + d) + h * g * (s + b) * Real.exp (-s * τ)
    - c * g ^ 2 * (s + d) * Real.exp (-2 * s * τ)

/-- The delayed characteristic matrix `z·I − (A with each coupling delayed)`. -/
noncomputable def delayMatrix (a b d r q h g τ : ℝ) (z : ℂ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![z + a, -(r * g) * Complex.exp (-z * τ), 1;
     -(q * g) * Complex.exp (-z * τ), z + b, 0;
     -(h * g) * Complex.exp (-z * τ), 0, z + d]

/-- Its determinant is the delayed characteristic function. -/
theorem det_delayMatrix (a b d r q h g τ : ℝ) (z : ℂ) :
    (delayMatrix a b d r q h g τ z).det =
      (z + a) * (z + b) * (z + d) + h * g * (z + b) * Complex.exp (-z * τ)
        - r * q * g ^ 2 * (z + d) * Complex.exp (-2 * z * τ) := by
  sorry

theorem Dd_zero (a b d c h g τ : ℝ) : Dd a b d c h g τ 0 = P a b d c h g 0 := by
  sorry

/-- **Delay cannot rescue high coupling**: if `P(0, g) < 0`, there is a real
characteristic root `s > 0` for every delay `τ ≥ 0`. -/
theorem delay_unstable {a b d c h g τ : ℝ} (ha : 0 < a) (hb : 0 < b) (hd : 0 < d)
    (hc : 0 < c) (hh : 0 ≤ h) (hg : 0 ≤ g) (hτ : 0 ≤ τ) (hP : P a b d c h g 0 < 0) :
    ∃ s : ℝ, 0 < s ∧ Dd a b d c h g τ s = 0 := by
  sorry

end Wyrd.SharedAir
