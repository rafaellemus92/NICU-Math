import Mathlib

/-!
# Direction of influence: what a lag can and cannot say

Test 2 subtracts the infant–control correlation from the infant–mom correlation
at each lag, and reads a peak at positive lag as "the infant changed first". The
source says this direction "follows from assumptions about contagion and
soothing". Here is that point made exact, for an oscillating component of the
signals (frequency `ω`) and the cross-covariance over one period:

  `c(h) = ⟨X(t) Y(t + h)⟩`,  `X` = infant, `Y` = mom.

Covariance and correlation differ only by a positive factor, so they have the
same sign and the same peak.

* `xcov_sin`: for `X = α sin(ω(t − d₁))`, `Y = β sin(ω(t − d₂))`,
  `c(h) = (α β / 2) cos(ω (h + d₁ − d₂))`.
* `mirroring_keeps_lag`: mom leads by `d` and the infant **mirrors** her
  (same sign). The peak in the window `(−π/ω, π/ω]` is at `h = −d`: correctly
  "mom first".
* `calming_reverses_lag`: mom leads by the same `d`, but her influence
  **calms** the infant (opposite sign). The peak moves to `h = π/ω − d > 0`:
  it reads "infant first". The leader is the same; only the assumed sign of the
  response changed.
* `room_leaks_when_unmatched`: no bond at all; infant, mom and a control adult
  all follow the room with delays `d₁, d₂, d₃`. If the control's delay differs
  from mom's, the contrast is positive at some lag. A timing mismatch alone makes
  a bond-free "signal".
* `room_cancels_iff`: the contrast vanishes at every lag exactly when the
  delays match modulo the period.

So a lag fixes direction only together with an assumed sign and shape of each
pathway. That is a mathematical limit, not a shortage of data.
-/

namespace Wyrd.Limits

open Real

/-- Cross-covariance over one period `2π/ω`. A positive lag `h` with a peak means
`X` changed first. -/
noncomputable def xcov (ω : ℝ) (X Y : ℝ → ℝ) (h : ℝ) : ℝ :=
  ω / (2 * π) * ∫ t in (0 : ℝ)..2 * π / ω, X t * Y (t + h)

theorem xcov_sin {ω : ℝ} (hω : 0 < ω) (α β d₁ d₂ h : ℝ) :
    xcov ω (fun t => α * sin (ω * (t - d₁))) (fun t => β * sin (ω * (t - d₂))) h =
      α * β / 2 * cos (ω * (h + d₁ - d₂)) := by
  have hω0 : ω ≠ 0 := hω.ne'
  set c := ω * (h + d₁ - d₂) with hc
  set e := -(ω * (d₁ + d₂ - h)) with he
  let F : ℝ → ℝ := fun t => α * β / 2 * (t * cos c - sin (2 * ω * t + e) / (2 * ω))
  have hderiv : ∀ t ∈ Set.uIcc (0 : ℝ) (2 * π / ω),
      HasDerivAt F (α * sin (ω * (t - d₁)) * (β * sin (ω * (t + h - d₂)))) t := by
    intro t _
    have h1 : HasDerivAt (fun t : ℝ => 2 * ω * t + e) (2 * ω) t := by
      simpa using ((hasDerivAt_id t).const_mul (2 * ω)).add_const e
    have h2 : HasDerivAt F
        (α * β / 2 * (1 * cos c - cos (2 * ω * t + e) * (2 * ω) / (2 * ω))) t :=
      (((hasDerivAt_id t).mul_const (cos c)).sub
        (h1.sin.div_const (2 * ω))).const_mul (α * β / 2)
    refine h2.congr_deriv ?_
    have hu : c = ω * (t + h - d₂) - ω * (t - d₁) := by rw [hc]; ring
    have hv : 2 * ω * t + e = ω * (t - d₁) + ω * (t + h - d₂) := by rw [he]; ring
    rw [hu, hv, cos_sub, cos_add]
    field_simp
    ring
  have hint : IntervalIntegrable
      (fun t => α * sin (ω * (t - d₁)) * (β * sin (ω * (t + h - d₂)))) MeasureTheory.volume
      0 (2 * π / ω) := by
    apply Continuous.intervalIntegrable
    fun_prop
  unfold xcov
  simp only
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint]
  have hper : sin (2 * ω * (2 * π / ω) + e) = sin e := by
    have : 2 * ω * (2 * π / ω) + e = e + 2 * π + 2 * π := by field_simp; ring
    rw [this, sin_add_two_pi, sin_add_two_pi]
  simp only [F, hper]
  field_simp
  ring_nf

/-- **Mirroring**: mom `sin(ω t)` leads by `d`; infant `κ sin(ω(t − d))`, `κ > 0`.
The unique peak in `(−π/ω, π/ω]` is at `−d`: "mom first", correctly. -/
theorem mirroring_keeps_lag {ω κ d : ℝ} (hω : 0 < ω) (hκ : 0 < κ) (hd : 0 < d)
    (hdπ : d < π / ω) :
    (∀ h ∈ Set.Ioc (-(π / ω)) (π / ω),
      xcov ω (fun t => κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h ≤
        xcov ω (fun t => κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) (-d)) ∧
    (∀ h ∈ Set.Ioc (-(π / ω)) (π / ω),
      xcov ω (fun t => κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h =
        xcov ω (fun t => κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) (-d) →
      h = -d) := by
  have key : ∀ h, xcov ω (fun t => κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h
      = κ / 2 * cos (ω * (h + d)) := by
    intro h
    rw [xcov_sin hω, sub_zero, mul_one]
  have e1 : ω * (π / ω) = π := by field_simp
  have hk : (κ / 2) ≠ 0 := by positivity
  refine ⟨fun h _ => ?_, fun h hh heq => ?_⟩
  · rw [key, key, neg_add_cancel, mul_zero, cos_zero, mul_one]
    exact mul_le_of_le_one_right (by positivity) (cos_le_one _)
  · obtain ⟨hl, hr⟩ := hh
    rw [key, key, neg_add_cancel, mul_zero, cos_zero, mul_one] at heq
    have hc1 : cos (ω * (h + d)) = 1 := mul_left_cancel₀ hk (by rw [heq, mul_one])
    have a1 : -π < ω * h := by
      have := mul_lt_mul_of_pos_left hl hω; rwa [mul_neg, e1] at this
    have a2 : ω * h ≤ π := by
      have := mul_le_mul_of_nonneg_left hr hω.le; rwa [e1] at this
    have a3 : 0 < ω * d := mul_pos hω hd
    have a4 : ω * d < π := by
      have := mul_lt_mul_of_pos_left hdπ hω; rwa [e1] at this
    have hz := (cos_eq_one_iff_of_lt_of_lt (by rw [mul_add]; linarith [pi_pos])
      (by rw [mul_add]; linarith [pi_pos])).1 hc1
    rcases mul_eq_zero.1 hz with h0 | h0
    · exact absurd h0 hω.ne'
    · linarith

/-- **Calming**: mom `sin(ω t)` still leads by `d`, but the infant responds with
the opposite sign, `−κ sin(ω(t − d))`. The unique peak in `(−π/ω, π/ω]` is at
`π/ω − d > 0`: it reads "infant first". -/
theorem calming_reverses_lag {ω κ d : ℝ} (hω : 0 < ω) (hκ : 0 < κ) (hd : 0 < d)
    (hdπ : d < π / ω) :
    0 < π / ω - d ∧
    (∀ h ∈ Set.Ioc (-(π / ω)) (π / ω),
      xcov ω (fun t => -κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h ≤
        xcov ω (fun t => -κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0)))
          (π / ω - d)) ∧
    (∀ h ∈ Set.Ioc (-(π / ω)) (π / ω),
      xcov ω (fun t => -κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h =
        xcov ω (fun t => -κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0)))
          (π / ω - d) →
      h = π / ω - d) := by
  have key : ∀ h, xcov ω (fun t => -κ * sin (ω * (t - d))) (fun t => 1 * sin (ω * (t - 0))) h
      = -κ / 2 * cos (ω * (h + d)) := by
    intro h
    rw [xcov_sin hω, sub_zero, mul_one]
  have e1 : ω * (π / ω) = π := by field_simp
  have hk : (-κ / 2) ≠ 0 := by
    have : 0 < κ / 2 := by positivity
    rw [neg_div]; exact neg_ne_zero.2 this.ne'
  refine ⟨sub_pos.2 hdπ, fun h _ => ?_, fun h hh heq => ?_⟩
  · rw [key, key, sub_add_cancel, e1, cos_pi]
    nlinarith [neg_one_le_cos (ω * (h + d))]
  · obtain ⟨hl, hr⟩ := hh
    rw [key, key, sub_add_cancel, e1, cos_pi] at heq
    have hc1 : cos (ω * (h + d)) = -1 := mul_left_cancel₀ hk heq
    have hc2 : cos (ω * (h + d) - π) = 1 := by rw [cos_sub_pi, hc1, neg_neg]
    have a1 : -π < ω * h := by
      have := mul_lt_mul_of_pos_left hl hω; rwa [mul_neg, e1] at this
    have a2 : ω * h ≤ π := by
      have := mul_le_mul_of_nonneg_left hr hω.le; rwa [e1] at this
    have a3 : 0 < ω * d := mul_pos hω hd
    have a4 : ω * d < π := by
      have := mul_lt_mul_of_pos_left hdπ hω; rwa [e1] at this
    have hz := (cos_eq_one_iff_of_lt_of_lt (by rw [mul_add]; linarith [pi_pos])
      (by rw [mul_add]; linarith [pi_pos])).1 hc2
    apply mul_left_cancel₀ hω.ne'
    rw [mul_sub, e1]
    rw [mul_add] at hz
    linarith

/-- **An unmatched control leaks the room**: with no bond, if the control's delay
`d₃` differs from mom's `d₂` (by less than a period), the contrast at lag
`d₂ − d₁` is positive. -/
theorem room_leaks_when_unmatched {ω d₁ d₂ d₃ : ℝ} (hω : 0 < ω) (h0 : 0 < |d₂ - d₃|)
    (h1 : |d₂ - d₃| < 2 * π / ω) :
    0 < xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₂))) (d₂ - d₁) -
      xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₃))) (d₂ - d₁) := by
  rw [xcov_sin hω, xcov_sin hω, show d₂ - d₁ + d₁ - d₂ = 0 by ring,
    show d₂ - d₁ + d₁ - d₃ = d₂ - d₃ by ring, mul_zero, cos_zero]
  have hb : |ω * (d₂ - d₃)| < 2 * π := by
    rw [abs_mul, abs_of_pos hω]
    have := mul_lt_mul_of_pos_left h1 hω
    rwa [show ω * (2 * π / ω) = 2 * π by field_simp] at this
  obtain ⟨b1, b2⟩ := abs_lt.1 hb
  have hlt : cos (ω * (d₂ - d₃)) < 1 := by
    refine lt_of_le_of_ne (cos_le_one _) (fun hc => ?_)
    have hz := (cos_eq_one_iff_of_lt_of_lt b1 b2).1 hc
    rcases mul_eq_zero.1 hz with h | h
    · exact hω.ne' h
    · rw [h, abs_zero] at h0; exact lt_irrefl _ h0
  linarith

/-- The contrast vanishes at every lag exactly when the delays match modulo the
period. -/
theorem room_cancels_iff {ω : ℝ} (hω : 0 < ω) (d₁ d₂ d₃ : ℝ) :
    (∀ h : ℝ,
      xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₂))) h -
        xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₃))) h = 0) ↔
      ∃ k : ℤ, ω * (d₂ - d₃) = 2 * π * k := by
  constructor
  · intro H
    have := H (d₂ - d₁)
    rw [xcov_sin hω, xcov_sin hω, show d₂ - d₁ + d₁ - d₂ = 0 by ring,
      show d₂ - d₁ + d₁ - d₃ = d₂ - d₃ by ring, mul_zero, cos_zero] at this
    have hc : cos (ω * (d₂ - d₃)) = 1 := by linarith
    obtain ⟨n, hn⟩ := (cos_eq_one_iff _).1 hc
    exact ⟨n, by rw [← hn]; ring⟩
  · rintro ⟨k, hk⟩ h
    rw [xcov_sin hω, xcov_sin hω]
    have : ω * (h + d₁ - d₃) = ω * (h + d₁ - d₂) + k * (2 * π) := by
      linear_combination hk
    rw [this, cos_add_int_mul_two_pi]
    ring

end Wyrd.Limits
