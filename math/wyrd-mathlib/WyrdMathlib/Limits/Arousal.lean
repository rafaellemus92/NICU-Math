import Mathlib

/-!
# "Arousal is one number": what that rules out

In the model, one hidden variable `A` sets both autonomic branches:

* vagal (parasympathetic) tone `V = V₀ (1 − 0.8 A)(1 − RSA · insp)`;
* sympathetic drive `S = 0.1 + 0.5 A⁺`.

So the two branches cannot move independently.

* `no_coactivation`: whenever sympathetic drive is above its resting value,
  vagal tone is strictly below its resting value (at the same breathing phase).
  States with both branches up at once cannot be represented: for example
  pain under sedation, or the sympathetic–vagal co-activation seen in real
  physiology.
* `symp_determines_state`, `vagal_determined_by_symp`: above rest, the
  sympathetic level fixes `A`, and with it the vagal tone. Two physiologically
  different infants with the same sympathetic drive are the same infant to the
  model.

This is the formal content of the source's limit "Arousal is one number". Which
extra dimensions matter (pain, sedation, cortisol, illness) is a clinical
question, not a mathematical one.
-/

namespace Wyrd.Limits

/-- Vagal tone. -/
noncomputable def vagal (V₀ rsa insp A : ℝ) : ℝ := V₀ * (1 - 0.8 * A) * (1 - rsa * insp)

/-- Sympathetic drive. -/
noncomputable def symp (A : ℝ) : ℝ := 0.1 + 0.5 * max A 0

private lemma symp_pos_of_gt {A : ℝ} (h : symp 0 < symp A) : 0 < A := by
  unfold symp at h
  by_contra hA'
  have hA : A ≤ 0 := not_lt.mp hA'
  rw [max_eq_right hA, max_self] at h
  exact lt_irrefl _ h

theorem no_coactivation {V₀ rsa insp A : ℝ} (hV : 0 < V₀) (hr : rsa * insp < 1)
    (hS : symp 0 < symp A) : vagal V₀ rsa insp A < vagal V₀ rsa insp 0 := by
  have hA := symp_pos_of_gt hS
  have hk : 0 < 1 - rsa * insp := by linarith
  have := mul_pos (mul_pos hV hA) hk
  unfold vagal
  nlinarith

theorem symp_determines_state {A₁ A₂ : ℝ} (h : symp A₁ = symp A₂) (h0 : symp 0 < symp A₁) :
    A₁ = A₂ := by
  have hA₁ := symp_pos_of_gt h0
  have hA₂ : 0 < A₂ := symp_pos_of_gt (h ▸ h0)
  unfold symp at h
  rw [max_eq_left hA₁.le, max_eq_left hA₂.le] at h
  linarith

theorem vagal_determined_by_symp {V₀ rsa insp A₁ A₂ : ℝ} (h : symp A₁ = symp A₂)
    (h0 : symp 0 < symp A₁) : vagal V₀ rsa insp A₁ = vagal V₀ rsa insp A₂ := by
  rw [symp_determines_state h h0]

end Wyrd.Limits
