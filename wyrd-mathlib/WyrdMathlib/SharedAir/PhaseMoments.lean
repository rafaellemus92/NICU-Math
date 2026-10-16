import Mathlib

/-!
# Same synchrony, different future: phase moments do not close

For `m` identical phase oscillators with mean-field coupling, in the frame
rotating at the common frequency, `θⱼ' = K · Im(Z₁ e^{−iθⱼ}) = K r sin(ψ − θⱼ)`,
where `Z₁ = r e^{iψ} = (1/m) Σ e^{iθⱼ}`. Then exactly

  `Z₁' = (K/2) (Z₁ − conj(Z₁) Z₂)`,  `Z₂ = (1/m) Σ e^{2iθⱼ}`.

So `Z₁`'s future depends on `Z₂`. Two four-cell configurations with the same
`Z₁ = 1/2` (same synchrony `R = 1/2`) have `Z₁' = K/4` and `Z₁' = 0`. Repeating
each six times gives 24 cells, the model's pacemaker count.
-/

namespace Wyrd.SharedAir

open Complex

/-- First phase moment. -/
noncomputable def Z1 {m : ℕ} (θ : Fin m → ℝ) : ℂ := (∑ j, exp (θ j * I)) / m

/-- Second phase moment. -/
noncomputable def Z2 {m : ℕ} (θ : Fin m → ℝ) : ℂ := (∑ j, exp (2 * θ j * I)) / m

/-- Mean-field velocity in the rotating frame. -/
noncomputable def vel (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) (j : Fin m) : ℝ :=
  K * (Z1 θ * exp (-(θ j * I))).im

/-- It is the Kuramoto form `K r sin(ψ − θⱼ)` when `Z₁ = r e^{iψ}`. -/
theorem vel_eq_sin (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) (j : Fin m) {r ψ : ℝ}
    (hZ : Z1 θ = r * exp (ψ * I)) : vel K θ j = K * r * Real.sin (ψ - θ j) := by
  sorry

/-- The rate of change of `Z₁` implied by the velocities. -/
noncomputable def Z1dot (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) : ℂ :=
  (∑ j, I * vel K θ j * exp (θ j * I)) / m

/-- `Z1dot` really is the time derivative of `Z₁` along a trajectory. -/
theorem hasDerivAt_Z1 {m : ℕ} {θ : ℝ → Fin m → ℝ} {θ' : Fin m → ℝ} {t : ℝ}
    (h : ∀ j, HasDerivAt (fun s => θ s j) (θ' j) t) :
    HasDerivAt (fun s => Z1 (θ s)) ((∑ j, I * θ' j * exp (θ t j * I)) / m) t := by
  sorry

/-- **The moment identity**: `Z₁' = (K/2)(Z₁ − conj(Z₁) Z₂)`. -/
theorem Z1dot_eq (K : ℝ) {m : ℕ} (θ : Fin m → ℝ) :
    Z1dot K θ = K / 2 * (Z1 θ - starRingEnd ℂ (Z1 θ) * Z2 θ) := by
  sorry

/-- Configuration A: phases `0, 0, π/2, −π/2`. -/
noncomputable def confA : Fin 4 → ℝ := ![0, 0, Real.pi / 2, -(Real.pi / 2)]

/-- Configuration B: phases `0, 0, 0, π`. -/
noncomputable def confB : Fin 4 → ℝ := ![0, 0, 0, Real.pi]

theorem moments_A : Z1 confA = 1 / 2 ∧ Z2 confA = 0 := by
  sorry

theorem moments_B : Z1 confB = 1 / 2 ∧ Z2 confB = 1 := by
  sorry

/-- **Counterexample to closure**: the same first moment (so the same synchrony
`R = 1/2`) but different rates of change, `K/4` versus `0`. -/
theorem same_synchrony_different_future (K : ℝ) :
    Z1 confA = Z1 confB ∧ Z1dot K confA = K / 4 ∧ Z1dot K confB = 0 := by
  sorry

/-- The 24-cell versions (each four-cell pattern repeated six times). -/
noncomputable def confA24 (j : Fin 24) : ℝ := confA ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩

noncomputable def confB24 (j : Fin 24) : ℝ := confB ⟨j.val % 4, Nat.mod_lt _ (by norm_num)⟩

theorem same_synchrony_different_future_24 (K : ℝ) :
    Z1 confA24 = 1 / 2 ∧ Z1 confB24 = 1 / 2 ∧ Z1dot K confA24 = K / 4 ∧ Z1dot K confB24 = 0 := by
  sorry

end Wyrd.SharedAir
