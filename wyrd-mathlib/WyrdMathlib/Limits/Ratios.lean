import Mathlib

/-!
# Ratios other than n:1

The Shared Air model's locking index looks for 2:1 and 3:1. Prenatal recordings
(van Leeuwen and colleagues) found brief 3:2, 5:3 and 4:3 epochs. Two exact facts
about what a harmonic index and the model's forcing can and cannot see.

**1. A harmonic index counts bands, not ratios.** Under perfect `n:m` locking
(`n` infant beats per `m` maternal cycles, `gcd(n, m) = 1`), mom's phase at
successive infant beats steps by `2π m/n`. Over one full locking cycle, the
`k`-th harmonic index `|⟨exp(i k ψⱼ)⟩|` is `1` if `n ∣ k` and `0` otherwise
(`lockIndex_eq_one`, `lockIndex_eq_zero`). So:

* no harmonic index can tell 3:2 from 3:1 (`three_two_looks_like_three_one`);
* 5:3 and 4:3 are invisible to the 2nd and 3rd harmonics (`five_three_hidden`,
  `four_three_hidden`);
* a perfect 2:1 lock has first-harmonic index 0 (`two_one_needs_second_harmonic`).

The ratio itself has to come from the beat rates, not from the index.

**2. First-order forcing through `sin θ` only produces n:1 tongues.** In the
model each maternal beat pushes each infant cell by `−ε P(ψ) sin θ`. To first
order in `ε`, locking near `n:m` is decided by the average of the forcing along
the unperturbed `n:m` orbit `θ = n s + a`, `ψ = m s + b`. For **every**
continuous `2π`-periodic `P`, forcing through the `l`-th harmonic `sin(l θ)`
averages to zero unless `m ∣ l n` (`resonant_average_vanishes`). With the
model's `sin θ` (`l = 1`) and coprime `n, m > 1`, the average vanishes
(`model_forcing_misses_n_m`), while an n:1 average generally does not
(`n_one_average`). A first-order 3:2 tongue needs the second harmonic of the
infant phase in the coupling, and 5:3 the third
(`second_harmonic_reaches_three_two`, `third_harmonic_reaches_five_three`).
Otherwise n:m locking is a higher-order effect in `ε`.

These are statements about the equations and an idealised, noise-free lock, not
about any recording.
-/

namespace Wyrd.Limits

open Complex Real

/-- The `k`-th harmonic locking index over one full `n:m` cycle. Mom's phase at the
`j`-th infant beat is `ψ₀ + 2π m j / n`. -/
noncomputable def lockIndex (k n m : ℕ) (ψ₀ : ℝ) : ℝ :=
  ‖(∑ j ∈ Finset.range n,
      Complex.exp ((((k : ℝ) * (ψ₀ + 2 * π * (m : ℝ) * (j : ℝ) / (n : ℝ)) : ℝ) : ℂ) * I)) /
    (n : ℂ)‖

/-- If the number of bands divides the harmonic, the index is `1`. -/
theorem lockIndex_eq_one {k n m : ℕ} (hn : 0 < n) (h : n ∣ k) (ψ₀ : ℝ) :
    lockIndex k n m ψ₀ = 1 := by
  sorry

/-- Otherwise (for coprime `n, m`) the index is exactly `0`. -/
theorem lockIndex_eq_zero {k n m : ℕ} (hn : 0 < n) (hcop : Nat.Coprime n m) (h : ¬ n ∣ k)
    (ψ₀ : ℝ) : lockIndex k n m ψ₀ = 0 := by
  sorry

/-- Every harmonic index reads a 3:2 lock exactly as it reads a 3:1 lock. -/
theorem three_two_looks_like_three_one (k : ℕ) (ψ₀ : ℝ) :
    lockIndex k 3 2 ψ₀ = lockIndex k 3 1 ψ₀ := by
  sorry

/-- A perfect 5:3 lock is invisible to the 2nd and 3rd harmonics; the 5th sees it. -/
theorem five_three_hidden (ψ₀ : ℝ) :
    lockIndex 2 5 3 ψ₀ = 0 ∧ lockIndex 3 5 3 ψ₀ = 0 ∧ lockIndex 5 5 3 ψ₀ = 1 := by
  sorry

/-- A perfect 4:3 lock is invisible to the 2nd and 3rd harmonics; the 4th sees it. -/
theorem four_three_hidden (ψ₀ : ℝ) :
    lockIndex 2 4 3 ψ₀ = 0 ∧ lockIndex 3 4 3 ψ₀ = 0 ∧ lockIndex 4 4 3 ψ₀ = 1 := by
  sorry

/-- A perfect 2:1 lock has first-harmonic index `0` and second-harmonic index `1`. -/
theorem two_one_needs_second_harmonic (ψ₀ : ℝ) :
    lockIndex 1 2 1 ψ₀ = 0 ∧ lockIndex 2 2 1 ψ₀ = 1 := by
  sorry

/-- **First-order averages vanish off resonance**: for every continuous
`2π`-periodic `P`, forcing through `sin(l θ)` along the `n:m` orbit averages to
zero unless `m ∣ l n`. -/
theorem resonant_average_vanishes {P : ℝ → ℝ} (hP : Continuous P)
    (hper : Function.Periodic P (2 * π)) {l n m : ℕ} (hm : 0 < m) (h : ¬ m ∣ l * n)
    (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (l * (n * s + a)) * P (m * s + b) = 0 := by
  sorry

/-- The model's own forcing `P(ψ) = exp(2(cos ψ − 1)) − c` (any centring constant
`c`) through `sin θ` has zero first-order average along every `n:m` orbit with
coprime `n, m` and `m > 1`. -/
theorem model_forcing_misses_n_m {n m : ℕ} (hm : 1 < m) (hcop : Nat.Coprime n m)
    (c a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π,
      Real.sin (n * s + a) * (Real.exp (2 * (Real.cos (m * s + b) - 1)) - c) = 0 := by
  sorry

/-- An n:1 orbit picks up the `n`-th harmonic of `P`: here `P = cos(n ·)`. -/
theorem n_one_average {n : ℕ} (hn : 0 < n) (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (n * s + a) * Real.cos (n * (s + b)) =
      π * Real.sin (a - n * b) := by
  sorry

/-- Coupling through `sin 2θ` reaches 3:2 at first order (with `P = cos 3ψ`). -/
theorem second_harmonic_reaches_three_two (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (2 * (3 * s + a)) * Real.cos (3 * (2 * s + b)) =
      π * Real.sin (2 * a - 3 * b) := by
  sorry

/-- Coupling through `sin 3θ` reaches 5:3 at first order (with `P = cos 5ψ`). -/
theorem third_harmonic_reaches_five_three (a b : ℝ) :
    ∫ s in (0 : ℝ)..2 * π, Real.sin (3 * (5 * s + a)) * Real.cos (5 * (3 * s + b)) =
      π * Real.sin (3 * a - 5 * b) := by
  sorry

end Wyrd.Limits
