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
  -- the doubled delay is the square of the single delay factor
  have hE : Complex.exp (-2 * z * τ) = Complex.exp (-z * τ) ^ 2 := by
    rw [sq, ← Complex.exp_add]; ring_nf
  rw [hE]
  simp [Matrix.det_fin_three, delayMatrix]
  ring

theorem Dd_zero (a b d c h g τ : ℝ) : Dd a b d c h g τ 0 = P a b d c h g 0 := by
  unfold Dd P
  simp

/-- **Delay cannot rescue high coupling**: if `P(0, g) < 0`, there is a real
characteristic root `s > 0` for every delay `τ ≥ 0`. -/
theorem delay_unstable {a b d c h g τ : ℝ} (ha : 0 < a) (hb : 0 < b) (hd : 0 < d)
    (hc : 0 < c) (hh : 0 ≤ h) (hg : 0 ≤ g) (hτ : 0 ≤ τ) (hP : P a b d c h g 0 < 0) :
    ∃ s : ℝ, 0 < s ∧ Dd a b d c h g τ s = 0 := by
  obtain ⟨S, hS⟩ : ∃ S : ℝ, S = 1 + c * g ^ 2 := ⟨_, rfl⟩
  have hcg : 0 ≤ c * g ^ 2 := by positivity
  have hS0 : 0 < S := by linarith
  have hcont : ContinuousOn (Dd a b d c h g τ) (Set.Icc 0 S) := by
    show ContinuousOn (fun s => (s + a) * (s + b) * (s + d) + h * g * (s + b) * Real.exp (-s * τ)
      - c * g ^ 2 * (s + d) * Real.exp (-2 * s * τ)) _
    fun_prop
  -- at `s = 0` the delay factors are `1`, so `Dd(0) = P(0) < 0`
  have h0 : Dd a b d c h g τ 0 < 0 := by rw [Dd_zero]; exact hP
  -- at `s = S = 1 + c g²`: the `h`-term is `≥ 0`, the doubled-delay factor is `≤ 1`,
  -- and `(S + a)(S + b) > S · 1 ≥ c g²`
  have hSpos : 0 < Dd a b d c h g τ S := by
    unfold Dd
    have e1 : 0 < Real.exp (-S * τ) := Real.exp_pos _
    have e2 : Real.exp (-2 * S * τ) ≤ 1 := Real.exp_le_one_iff.mpr (by nlinarith)
    have k1 : 0 ≤ h * g * (S + b) * Real.exp (-S * τ) := by
      have : 0 < S + b := by linarith
      positivity
    have k2 : c * g ^ 2 * (S + d) * Real.exp (-2 * S * τ) ≤ c * g ^ 2 * (S + d) := by
      have hSd : 0 < S + d := by linarith
      have hnn : 0 ≤ c * g ^ 2 * (S + d) := by positivity
      have := mul_le_mul_of_nonneg_left e2 hnn
      linarith
    have k3 : c * g ^ 2 * (S + d) < (S + a) * (S + b) * (S + d) := by
      have : c * g ^ 2 < (S + a) * (S + b) := by nlinarith
      exact mul_lt_mul_of_pos_right this (by linarith)
    linarith
  -- intermediate value theorem on `[0, S]`
  obtain ⟨s, hs, hs0⟩ := intermediate_value_Ioo hS0.le hcont ⟨h0, hSpos⟩
  exact ⟨s, hs.1, hs0⟩

/-- The real characteristic function is the delayed determinant at real `s`, with `c = r q`. -/
theorem Dd_eq_det (a b d r q h g τ s : ℝ) :
    (Dd a b d (r * q) h g τ s : ℂ) = (delayMatrix a b d r q h g τ (s : ℂ)).det := by
  sorry

end Wyrd.SharedAir
