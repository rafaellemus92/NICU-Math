import WyrdMathlib.SharedAir.Specific

/-!
# Whose good: the equations do not choose an objective

The source: "The equations describe how two bodies move each other. Nothing in
them distinguishes care from skilled manipulation." The equations take no intent
as input, so intent cannot be read off any trajectory. What mathematics *can*
show is that "better" needs an objective, and that natural objectives disagree.

Take the zero-delay linearised perceived world (`x` infant arousal, `y` mom's
arousal, `z` soothing) after an infant disturbance `x(0) = 1`, `y(0) = 0`:

* `mom_untouched_iff`: mom's arousal stays at rest for all `t ≥ 0` **exactly**
  when `g = 0`. An objective that protects mom picks `g = 0`.
* `infant_best_moves_mom`: the coupling that maximises the recovery rate after
  the infant's disturbance (`optimal_coupling`, `g* ≈ 0.08036`) is positive, so
  it necessarily moves mom. That rate is the spectral rate of the whole
  zero-delay linearised system (its slowest decaying mode), not the source's
  Test 4 statistic.

No single coupling serves both objectives. Choosing between them, or a third
person's objective, is a decision about whose good counts. The dynamics are the
same under every choice.
-/

namespace Wyrd.Limits

open Wyrd.SharedAir

/-- A trajectory of the zero-delay linearised perceived world (`a = 1/30`,
`b = 1/20`, `d = 1/4`, `r = 1/25`, `q = 1/10`, `h = 3/40`). -/
structure LinSol (g : ℝ) (x y z : ℝ → ℝ) : Prop where
  hx : ∀ t, HasDerivAt x (-x t / 30 - z t + g / 25 * y t) t
  hy : ∀ t, HasDerivAt y (-y t / 20 + g / 10 * x t) t
  hz : ∀ t, HasDerivAt z (-z t / 4 + 3 * g / 40 * x t) t

/-- Mom stays at rest after an infant disturbance exactly when `g = 0`. -/
theorem mom_untouched_iff {g : ℝ} {x y z : ℝ → ℝ} (hs : LinSol g x y z) (hx0 : x 0 = 1)
    (hy0 : y 0 = 0) : (∀ t, 0 ≤ t → y t = 0) ↔ g = 0 := by
  constructor
  · intro hy
    have h1 : HasDerivWithinAt y (-y 0 / 20 + g / 10 * x 0) (Set.Ici 0) 0 :=
      (hs.hy 0).hasDerivWithinAt
    have h2 : HasDerivWithinAt y 0 (Set.Ici 0) 0 :=
      (hasDerivWithinAt_const (0 : ℝ) (Set.Ici (0 : ℝ)) (0 : ℝ)).congr_of_mem
        (fun t ht => hy t ht) (Set.mem_Ici.mpr le_rfl)
    have h3 := (uniqueDiffWithinAt_Ici (0 : ℝ)).eq_deriv _ h1 h2
    rw [hx0, hy0] at h3
    linarith
  · rintro rfl
    intro t _
    set φ : ℝ → ℝ := fun t => Real.exp (t / 20) * y t with hφ
    have hd : ∀ t, HasDerivAt φ 0 t := by
      intro t
      have he : HasDerivAt (fun t : ℝ => Real.exp (t / 20)) (Real.exp (t / 20) * (1 / 20)) t := by
        have := ((hasDerivAt_id t).div_const 20).exp
        simpa using this
      have := he.mul (hs.hy t)
      convert this using 1
      ring
    have hc : φ t = φ 0 :=
      is_const_of_deriv_eq_zero (fun s => (hd s).differentiableAt) (fun s => (hd s).deriv) t 0
    simp only [hφ, hy0, mul_zero] at hc
    rcases mul_eq_zero.mp hc with h | h
    · exact absurd h (Real.exp_pos _).ne'
    · exact h

/-- The infant-optimal coupling moves mom. -/
theorem infant_best_moves_mom {s₀ : ℝ} (hs₀ : s₀ ∈ Set.Ioo (-(1 / 20 : ℝ)) (-(1 / 30)))
    (hH : H (1 / 30) (1 / 20) (1 / 4) (1 / 250) (3 / 40) s₀ = 0) {x y z : ℝ → ℝ}
    (hs : LinSol (G (1 / 20) (1 / 4) (1 / 250) (3 / 40) s₀) x y z) (hx0 : x 0 = 1)
    (hy0 : y 0 = 0) : ∃ t, 0 ≤ t ∧ y t ≠ 0 := by
  have hpos := (optimal_coupling hyp_sharedAir hs₀ hH).1
  by_contra hne
  push Not at hne
  have := (mom_untouched_iff hs hx0 hy0).mp hne
  linarith

end Wyrd.Limits
