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
  sorry

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
  sorry

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
  sorry

/-- **An unmatched control leaks the room**: with no bond, if the control's delay
`d₃` differs from mom's `d₂` (by less than a period), the contrast at lag
`d₂ − d₁` is positive. -/
theorem room_leaks_when_unmatched {ω d₁ d₂ d₃ : ℝ} (hω : 0 < ω) (h0 : 0 < |d₂ - d₃|)
    (h1 : |d₂ - d₃| < 2 * π / ω) :
    0 < xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₂))) (d₂ - d₁) -
      xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₃))) (d₂ - d₁) := by
  sorry

/-- The contrast vanishes at every lag exactly when the delays match modulo the
period. -/
theorem room_cancels_iff {ω : ℝ} (hω : 0 < ω) (d₁ d₂ d₃ : ℝ) :
    (∀ h : ℝ,
      xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₂))) h -
        xcov ω (fun t => 1 * sin (ω * (t - d₁))) (fun t => 1 * sin (ω * (t - d₃))) h = 0) ↔
      ∃ k : ℤ, ω * (d₂ - d₃) = 2 * π * k := by
  sorry

end Wyrd.Limits
