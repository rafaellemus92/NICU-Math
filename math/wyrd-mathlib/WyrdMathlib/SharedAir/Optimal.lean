import WyrdMathlib.SharedAir.Dominant

/-!
# A unique finite optimal coupling, and the exact stability range

Everything here is about the **zero-delay** linearisation (`U = 0`, `A₀ = 0`,
steadiness `1`, `τ = 0`). Recovery speed is its **spectral rate**
`ρ(g) = −max Re(eigenvalues)`. That is not the source's Test 4 statistic (time
back to within 10 bpm), and nothing here proves an optimum for the nonlinear,
noisy or delayed model. With `s*`
the root of `H` in `(-b, -a)` and `g* = G(s*)`:

1. for every `g ≥ 0` some eigenvalue has real part `≥ s*`, so `ρ(g) ≤ −s*`;
2. for every `g ≥ 0` with `g ≠ g*`, some eigenvalue has real part `> s*`;
3. at `g = g*` every eigenvalue has real part `≤ s*`.

So `g*` is the **unique** maximiser of `ρ`, and it is finite and positive.
Stronger coupling eventually destabilises: at zero delay, the equilibrium is
stable (all real parts negative) exactly when `g < g_c`.

**Delay changes the stability range.** Only the instability for `g > g_c`
survives every delay (`Delay.lean` proves it whenever `P(0, g) < 0`;
`Specific.lean` turns that into `g > g_c` for the Shared Air coefficients). Below `g_c`, delay can destabilise.
Numerically (two independent root searches, not a Lean proof), with the Shared
Air coefficients: at `g = 3` stability is lost at `τ ≈ 1.84 s`, and at `g = 1` at
`τ ≈ 4.76 s`. So the zero-delay range must not be transferred to `τ > 0`.
-/

namespace Wyrd.SharedAir

/-- `P(·, g)` is continuous (it is a polynomial). -/
private theorem Optimal_P_cont (a b d c h g : ℝ) : Continuous (P a b d c h g) := by
  show Continuous (fun s => (s + a) * (s + b) * (s + d) + h * g * (s + b) - c * g ^ 2 * (s + d))
  fun_prop

/-- For `g ≥ 0`, if `P(t, g) ≤ 0` then `P(·, g)` has a real root `≥ t`
(IVT on `[t, S]` with an explicit `S` where `P(S, g) ≥ 0`). -/
private theorem Optimal_root_ge {a b d c h g t : ℝ} (hp : Hyp a b d c h) (hg : 0 ≤ g)
    (ht : P a b d c h g t ≤ 0) : ∃ s, t ≤ s ∧ P a b d c h g s = 0 := by
  have ha := hp.a_pos
  have hab := hp.a_lt_b
  have hbd := hp.b_lt_d
  have hc := hp.c_pos
  have hh := hp.h_pos
  have hm0 : 0 ≤ max t 0 := le_max_right _ _
  have hmt : t ≤ max t 0 := le_max_left _ _
  have hcg : 0 ≤ c * g ^ 2 := by positivity
  set S := max t 0 + c * g ^ 2 + 1 with hS
  have hS1 : 1 ≤ S := by linarith
  have htS : t ≤ S := by linarith
  have hPS : 0 ≤ P a b d c h g S := by
    unfold P
    -- `(S + a)(S + b) ≥ S² ≥ S > c g²`
    have h1 : c * g ^ 2 < (S + a) * (S + b) := by nlinarith
    have h2 : 0 < S + d := by linarith
    have h3 : 0 ≤ h * g * (S + b) := by
      have : 0 ≤ S + b := by linarith
      positivity
    nlinarith [mul_pos h2 (sub_pos.mpr h1)]
  obtain ⟨s, hs, hPs⟩ :=
    intermediate_value_Icc htS (Optimal_P_cont a b d c h g).continuousOn ⟨ht, hPS⟩
  exact ⟨s, hs.1, hPs⟩

/-- **Unique finite optimal coupling** (zero-delay spectral rate). -/
theorem optimal_coupling {a b d c h : ℝ} (hp : Hyp a b d c h) {s₀ : ℝ}
    (hs₀ : s₀ ∈ Set.Ioo (-b) (-a)) (hH : H a b d c h s₀ = 0) :
    0 < G b d c h s₀ ∧
      (∀ g, 0 ≤ g → ∃ s : ℝ, s₀ ≤ s ∧ P a b d c h g s = 0) ∧
      (∀ g, 0 ≤ g → g ≠ G b d c h s₀ → ∃ s : ℝ, s₀ < s ∧ P a b d c h g s = 0) ∧
      (∀ z : ℂ, Pc a b d c h (G b d c h s₀) z = 0 → z.re ≤ s₀) := by
  obtain ⟨hs1, hs2⟩ := hs₀
  have hc := hp.c_pos
  have hh := hp.h_pos
  have hbd := hp.b_lt_d
  have hsb : 0 < s₀ + b := by linarith
  have hsd : 0 < s₀ + d := by linarith
  -- since `H(s₀) = 0`, the completed square gives `P(s₀, g) = -c (s₀ + d) (g - G s₀)²`
  have key : ∀ g, P a b d c h g s₀ = -(c * (s₀ + d) * (g - G b d c h s₀) ^ 2) := by
    intro g
    rw [complete_square hc.ne' hsd.ne', hH]
    ring
  have hG : 0 < G b d c h s₀ := by unfold G; positivity
  have hcd : 0 < c * (s₀ + d) := mul_pos hc hsd
  refine ⟨hG, ?_, ?_, ?_⟩
  · intro g hg
    refine Optimal_root_ge hp hg ?_
    rw [key]
    have := mul_nonneg hcd.le (sq_nonneg (g - G b d c h s₀))
    linarith
  · intro g hg hne
    have hsq : 0 < (g - G b d c h s₀) ^ 2 :=
      lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 (sub_ne_zero.mpr hne)))
    have hlt : P a b d c h g s₀ < 0 := by
      rw [key]
      have := mul_pos hcd hsq
      linarith
    obtain ⟨s, hs, hPs⟩ := Optimal_root_ge hp hg hlt.le
    -- the root is not `s₀` itself because `P(s₀, g) < 0`
    refine ⟨s, lt_of_le_of_ne hs ?_, hPs⟩
    rintro rfl
    linarith
  · -- at `g = G s₀`, `s₀ > -b` is a real root, hence dominant
    exact re_le_of_root hp hG hs1 (by rw [key]; ring)

/-- The critical coupling: the positive root of `P(0, g) = a b d + h b g − c d g²`. -/
noncomputable def gc (a b d c h : ℝ) : ℝ :=
  (h * b + Real.sqrt (h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2)) / (2 * c * d)

theorem P_zero (a b d c h g : ℝ) : P a b d c h g 0 = a * b * d + h * b * g - c * d * g ^ 2 := by
  unfold P
  ring

/-- At `g = g_c` there is a zero eigenvalue. -/
theorem P_gc {a b d c h : ℝ} (hp : Hyp a b d c h) : P a b d c h (gc a b d c h) 0 = 0 := by
  have ha := hp.a_pos
  have hab := hp.a_lt_b
  have hbd := hp.b_lt_d
  have hc := hp.c_pos
  have hh := hp.h_pos
  have hb : 0 < b := by linarith
  have hd : 0 < d := by linarith
  have hD : 0 ≤ h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2 := by positivity
  have hr2 := Real.sq_sqrt hD
  rw [P_zero]
  unfold gc
  generalize Real.sqrt (h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2) = r at hr2 ⊢
  field_simp
  linear_combination (-1 : ℝ) * hr2

/-- For `g ≥ 0`: `P(0, g) > 0` exactly when `g < g_c`. -/
theorem P_zero_pos_iff {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 ≤ g) :
    0 < P a b d c h g 0 ↔ g < gc a b d c h := by
  have ha := hp.a_pos
  have hab := hp.a_lt_b
  have hbd := hp.b_lt_d
  have hc := hp.c_pos
  have hh := hp.h_pos
  have hb : 0 < b := by linarith
  have hd : 0 < d := by linarith
  have h0 := P_gc hp
  rw [P_zero] at h0 ⊢
  have hD : 0 ≤ h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2 := by positivity
  -- `√D > h b` since `D > (h b)²`
  have hrgt : h * b < Real.sqrt (h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2) := by
    rw [Real.lt_sqrt (by positivity)]
    have : 0 < 4 * a * b * c * d ^ 2 := by positivity
    nlinarith
  have e : 2 * c * d * gc a b d c h = h * b + Real.sqrt (h ^ 2 * b ^ 2 + 4 * a * b * c * d ^ 2) := by
    unfold gc
    field_simp
  generalize gc a b d c h = x at h0 e ⊢
  -- factor `P(0, g) = (g - g_c)(h b - c d (g + g_c))` using `P(0, g_c) = 0`
  have hfac : a * b * d + h * b * g - c * d * g ^ 2 = (g - x) * (h * b - c * d * (g + x)) := by
    linear_combination h0
  -- the second factor is negative: `2(h b - c d (g + g_c)) = h b - √D - 2 c d g < 0`
  have hneg : h * b - c * d * (g + x) < 0 := by
    have : 0 ≤ c * d * g := by positivity
    nlinarith
  rw [hfac]
  constructor
  · intro hpos
    by_contra hge
    have hge := not_lt.mp hge
    have := mul_nonpos_of_nonneg_of_nonpos (sub_nonneg.mpr hge) hneg.le
    linarith
  · intro hlt
    exact mul_pos_of_neg_of_neg (sub_neg.mpr hlt) hneg

/-- **Exact stability range, zero delay**: for `g ≥ 0`, every eigenvalue of the
zero-delay linearisation has negative real part if and only if `g < g_c`. -/
theorem stable_iff {a b d c h g : ℝ} (hp : Hyp a b d c h) (hg : 0 ≤ g) :
    (∀ z : ℂ, Pc a b d c h g z = 0 → z.re < 0) ↔ g < gc a b d c h := by
  have ha := hp.a_pos
  have hab := hp.a_lt_b
  have hbd := hp.b_lt_d
  constructor
  · intro hst
    by_contra hge
    have hP0 : P a b d c h g 0 ≤ 0 :=
      not_lt.mp fun hpos => hge ((P_zero_pos_iff hp hg).mp hpos)
    -- a real root `s ≥ 0` is an eigenvalue with nonnegative real part
    obtain ⟨s, hs, hPs⟩ := Optimal_root_ge hp hg hP0
    have := hst (s : ℂ) (by rw [Pc_ofReal, hPs]; simp)
    simp at this
    linarith
  · intro hlt z hz
    rcases hg.lt_or_eq with hg' | hg'
    · -- `g > 0`: `P(-b) < 0 < P(0)` gives a real root in `(-b, 0)`, which dominates
      have hpos : 0 < P a b d c h g 0 := (P_zero_pos_iff hp hg).mpr hlt
      have hneg := P_neg_b hp hg'
      obtain ⟨s, hs, hPs⟩ := intermediate_value_Icc (show -b ≤ 0 by linarith)
        (Optimal_P_cont a b d c h g).continuousOn ⟨hneg.le, hpos.le⟩
      have hs1 : -b < s := lt_of_le_of_ne hs.1 (by rintro rfl; linarith)
      have hs2 : s < 0 := lt_of_le_of_ne hs.2 (by rintro rfl; linarith)
      exact lt_of_le_of_lt (re_le_of_root hp hg' hs1 hPs z hz) hs2
    · -- `g = 0`: `Pc z = (z + a)(z + b)(z + d)`
      subst hg'
      unfold Pc at hz
      simp only [Complex.ofReal_zero, mul_zero, zero_mul, add_zero, sub_zero,
        ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, mul_eq_zero] at hz
      rcases hz with (h1 | h1) | h1
      · have := congrArg Complex.re h1
        simp at this
        linarith
      · have := congrArg Complex.re h1
        simp at this
        linarith
      · have := congrArg Complex.re h1
        simp at this
        linarith

end Wyrd.SharedAir
