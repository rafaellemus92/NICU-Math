import Mathlib

/-!
# Subtracting a control correlation does not isolate direct coupling

The model proposes `Corr(infant, mom) − Corr(infant, other parent)` as "the part
the room can't explain". Counterexample with **no direct coupling at all**: a
shared input `U` plus independent noises, `X = U + e₁`, `M = U + e₂`,
`O = U + 3e₃`. The probability space is completely explicit: four independent
fair ±1 coins, 16 equally likely outcomes. Then `Corr(X, M) = 1/2` and
`Corr(X, O) = 1/√20`, so the contrast is `1/2 − 1/√20 ≈ 0.276 > 0`, from
unequal noise alone.
-/

namespace Wyrd.SharedAir

/-- One outcome: the four coins `(U, e₁, e₂, e₃)`, each `±1`. -/
def coin (b : Bool) : ℝ := if b then 1 else -1

/-- Expectation over the 16 equally likely outcomes. -/
noncomputable def E (f : ℝ → ℝ → ℝ → ℝ → ℝ) : ℝ :=
  (∑ u : Bool, ∑ e1 : Bool, ∑ e2 : Bool, ∑ e3 : Bool, f (coin u) (coin e1) (coin e2) (coin e3)) / 16

/-- The three signals: shared input plus independent noise, no direct coupling. -/
def X (u e1 _e2 _e3 : ℝ) : ℝ := u + e1
def M (u _e1 e2 _e3 : ℝ) : ℝ := u + e2
def O (u _e1 _e2 e3 : ℝ) : ℝ := u + 3 * e3

/-- The coins are independent: every joint outcome has probability `1/16 = (1/2)⁴`,
and each coin is fair with mean zero. -/
theorem coins_fair : E (fun u _ _ _ => u) = 0 ∧ E (fun _ e1 _ _ => e1) = 0 ∧
    E (fun _ _ e2 _ => e2) = 0 ∧ E (fun _ _ _ e3 => e3) = 0 := by
  -- each is a finite sum over Bool⁴ of ±1 values that cancels
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [E, coin]

theorem second_moments :
    E (fun u e1 e2 e3 => X u e1 e2 e3 ^ 2) = 2 ∧ E (fun u e1 e2 e3 => M u e1 e2 e3 ^ 2) = 2 ∧
      E (fun u e1 e2 e3 => O u e1 e2 e3 ^ 2) = 10 ∧
      E (fun u e1 e2 e3 => X u e1 e2 e3 * M u e1 e2 e3) = 1 ∧
      E (fun u e1 e2 e3 => X u e1 e2 e3 * O u e1 e2 e3) = 1 := by
  -- expand the 16-term sums explicitly and evaluate
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp [E, coin, X, M, O] <;> norm_num

/-- Correlation of two mean-zero signals. -/
noncomputable def corr (f g : ℝ → ℝ → ℝ → ℝ → ℝ) : ℝ :=
  E (fun u e1 e2 e3 => f u e1 e2 e3 * g u e1 e2 e3) /
    Real.sqrt (E (fun u e1 e2 e3 => f u e1 e2 e3 ^ 2) * E (fun u e1 e2 e3 => g u e1 e2 e3 ^ 2))

theorem corr_XM : corr X M = 1 / 2 := by
  obtain ⟨hX, hM, -, hXM, -⟩ := second_moments
  unfold corr
  rw [hX, hM, hXM]
  -- √(2·2) = 2
  have h4 : Real.sqrt (2 * 2) = 2 := Real.sqrt_mul_self (by norm_num)
  rw [h4]

theorem corr_XO : corr X O = 1 / Real.sqrt 20 := by
  obtain ⟨hX, -, hO, -, hXO⟩ := second_moments
  unfold corr
  rw [hX, hO, hXO]
  norm_num

/-- **The contrast is positive with no direct coupling.** -/
theorem contrast_pos_without_coupling : 0 < corr X M - corr X O := by
  rw [corr_XM, corr_XO, sub_pos]
  -- 1/√20 < 1/2 because 2 < √20 (as 2² = 4 < 20)
  have h2 : (2 : ℝ) < Real.sqrt 20 := by
    rw [Real.lt_sqrt (by norm_num)]; norm_num
  rw [div_lt_div_iff_of_pos_left one_pos (Real.sqrt_pos.mpr (by norm_num)) two_pos]
  exact h2

end Wyrd.SharedAir
