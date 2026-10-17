import WyrdMathlib.SharedAir.Linearization
import WyrdMathlib.SharedAir.Specific

/-!
# Test 4's second state: the capacity limit makes the pair bistable

The revised source says the rising side of Test 4's inverted U is "a second
stable state: above a responsiveness of about 2, a large enough disturbance
flips the pair into sustained co-arousal … Remove that capacity limit and the
second state disappears." For the deterministic perceived world (`U = 0`, no
noise, baseline `0`, steadiness `1`, zero delay) this is exact:

* `no_coarousal_without_cap_general`: without the capacity limit (`cap ≡ 1`),
  any equilibrium other than rest forces `P(0, g) < 0`, so rest is already
  unstable. This holds for any positive coefficients with a cubic damping
  `κ > 0`.
* `only_rest_without_cap`: with the model's coefficients and `0 ≤ g ≤ 3` (the
  whole Test 4 sweep), rest is the only equilibrium without the cap.
* `only_rest_upto_two`: **with** the cap, rest is still the only equilibrium for
  `0 ≤ g ≤ 2`.
* `coarousal_exists_above_two`: at `g = 2.1` there is a co-arousal equilibrium
  (`Aᵢ, Aₘ > 0`). So the second state appears between 2 and 2.1, matching
  "about 2" (numerically near 2.069).
* `coarousal_stable_at_three`: at `g = 3` there is a co-arousal equilibrium that
  is linearly stable: every eigenvalue of the Jacobian `jac` has negative real
  part. Rest is also stable there (`stable_at_three`), so the pair is
  **bistable**.
* `hasDerivAt_field_line_at`: `jac` is the true derivative of the model's field
  at any point, along every direction.
* `cubic_hurwitz`: the Routh–Hurwitz test for cubics used above.

Not proved: the size of the disturbance that flips the pair (the basin
boundary), and anything about delay or noise. As the source says, this is one
mechanism that could produce the shape, not evidence that it is the one at work.
-/

namespace Wyrd.Limits

open Wyrd.SharedAir

/-- The field with the capacity limit removed (`cap ≡ 1`). -/
noncomputable def fieldNoCap (g : ℝ) (p : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (-p.1 / 30 - p.2.2 + 0.04 * g * p.2.1 - 0.02 * p.1 ^ 3,
   -p.2.1 / 20 + 0.10 * g * p.1 - 0.02 * p.2.1 ^ 3,
   (0.30 * g * p.1 - p.2.2) / 4)

/-- `cap'(y)`. -/
noncomputable def capDeriv (y : ℝ) : ℝ := -(2 * y / 0.64) / (1 + (y / 0.8) ^ 2) ^ 2

/-- The Jacobian of `field g` at `p` (order `Aᵢ, Aₘ, C`). -/
noncomputable def jac (g : ℝ) (p : ℝ × ℝ × ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  !![-1 / 30 - 0.06 * p.1 ^ 2, 0.04 * g, -1;
     0.10 * g, -1 / 20 - 0.06 * p.2.1 ^ 2, 0;
     0.30 * g * cap p.2.1 / 4, 0.30 * g * p.1 * capDeriv p.2.1 / 4, -1 / 4]

/-- `jac g p` is the derivative of `field g` at `p` along every direction `v`. -/
theorem hasDerivAt_field_line_at (g : ℝ) (p v : ℝ × ℝ × ℝ) :
    HasDerivAt (fun t : ℝ => field g (p + t • v))
      ((jac g p).mulVec ![v.1, v.2.1, v.2.2] 0, (jac g p).mulVec ![v.1, v.2.1, v.2.2] 1,
        (jac g p).mulVec ![v.1, v.2.1, v.2.2] 2) 0 := by
  obtain ⟨p1, p2, p3⟩ := p
  obtain ⟨v1, v2, v3⟩ := v
  -- rewrite the map along the line as an explicit triple of real functions of `t`
  have hfun : (fun t : ℝ => field g ((p1, p2, p3) + t • (v1, v2, v3))) = fun t =>
      (-(p1 + t * v1) / 30 - (p3 + t * v3) + 0.04 * g * (p2 + t * v2) - 0.02 * (p1 + t * v1) ^ 3,
       -(p2 + t * v2) / 20 + 0.10 * g * (p1 + t * v1) - 0.02 * (p2 + t * v2) ^ 3,
       (0.30 * g * (p1 + t * v1) * cap (p2 + t * v2) - (p3 + t * v3)) / 4) := by
    funext t; simp [field, Prod.smul_mk, smul_eq_mul]
  rw [hfun]
  have h1 : HasDerivAt (fun t : ℝ => p1 + t * v1) v1 0 := by
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const v1).const_add p1
  have h2 : HasDerivAt (fun t : ℝ => p2 + t * v2) v2 0 := by
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const v2).const_add p2
  have h3 : HasDerivAt (fun t : ℝ => p3 + t * v3) v3 0 := by
    simpa using ((hasDerivAt_id (0:ℝ)).mul_const v3).const_add p3
  -- `cap (p₂ + t v₂)` is the inverse of a never-vanishing polynomial in `t`
  have hden : HasDerivAt (fun t : ℝ => 1 + ((p2 + t * v2) / 0.8) ^ 2)
      (2 * (p2 / 0.8) * (v2 / 0.8)) 0 := by
    have := ((h2.div_const 0.8).pow 2).const_add 1
    simpa using this
  have hpos : (1 + ((p2 + 0 * v2) / 0.8) ^ 2 : ℝ) ≠ 0 := by positivity
  have hcap : HasDerivAt (fun t : ℝ => cap (p2 + t * v2)) (capDeriv p2 * v2) 0 := by
    have := hden.inv hpos
    convert this using 1
    · funext t; simp [cap, one_div]
    · simp only [capDeriv, zero_mul, add_zero]
      ring
  refine HasDerivAt.prodMk ?_ (HasDerivAt.prodMk ?_ ?_)
  · convert (((h1.neg.div_const 30).sub h3).add (h2.const_mul (0.04 * g))).sub
      ((h1.pow 3).const_mul 0.02) using 1
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, jac]
    ring
  · convert ((h2.neg.div_const 20).add (h1.const_mul (0.10 * g))).sub
      ((h2.pow 3).const_mul 0.02) using 1
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, jac]
    ring
  · convert ((((h1.const_mul (0.30 * g)).mul hcap).sub h3).div_const 4) using 1
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_three, jac]
    ring

/-- Routh–Hurwitz for cubics: `c₂, c₀ > 0` and `c₂ c₁ > c₀` put every root in the
open left half-plane. -/
theorem cubic_hurwitz {c₂ c₁ c₀ : ℝ} (h₂ : 0 < c₂) (h₀ : 0 < c₀) (h₂₁ : c₀ < c₂ * c₁)
    {s : ℂ} (hs : s ^ 3 + c₂ * s ^ 2 + c₁ * s + c₀ = 0) : s.re < 0 := by
  -- real and imaginary parts of the cubic, with `x = Re s`, `y = Im s`
  have hre := congrArg Complex.re hs
  have him := congrArg Complex.im hs
  simp [pow_succ, Complex.mul_re, Complex.mul_im] at hre him
  set x := s.re
  set y := s.im
  have hc₁ : 0 < c₁ := by
    by_contra hc
    push Not at hc
    nlinarith
  by_contra hx
  push Not at hx
  by_cases hy : y = 0
  · -- a real root: the cubic is `≥ c₀ > 0` for `x ≥ 0`
    rw [hy] at hre
    nlinarith [mul_nonneg hx (sq_nonneg x), mul_nonneg h₂.le (sq_nonneg x), mul_nonneg hc₁.le hx]
  · -- a complex root: `y² = 3x² + 2c₂x + c₁`, and then the real part is `< 0` for `x ≥ 0`
    have hy2 : y ^ 2 = 3 * x ^ 2 + 2 * c₂ * x + c₁ := by
      have : y * (3 * x ^ 2 + 2 * c₂ * x + c₁ - y ^ 2) = 0 := by linear_combination him
      rcases mul_eq_zero.mp this with h | h
      · exact absurd h hy
      · linarith
    have key : -8 * x ^ 3 - 8 * c₂ * x ^ 2 - (2 * c₁ + 2 * c₂ ^ 2) * x + (c₀ - c₂ * c₁) = 0 := by
      linear_combination hre + (3 * x + c₂) * hy2
    nlinarith [mul_nonneg hx (sq_nonneg x), mul_nonneg h₂.le (sq_nonneg x),
      mul_nonneg (by positivity : (0:ℝ) ≤ 2 * c₁ + 2 * c₂ ^ 2) hx]

/-- Without the capacity limit, an equilibrium other than rest forces `P(0, g) < 0`. -/
theorem no_coarousal_without_cap_general {a b d r q h κ g x y z : ℝ} (ha : 0 < a)
    (hb : 0 < b) (hd : 0 < d) (hh : 0 ≤ h) (hκ : 0 < κ) (hg : 0 ≤ g)
    (e₁ : -a * x - z + r * g * y - κ * x ^ 3 = 0) (e₂ : -b * y + q * g * x - κ * y ^ 3 = 0)
    (e₃ : -d * z + h * g * x = 0) (hne : (x, y) ≠ (0, 0)) :
    P a b d (r * q) h g 0 < 0 := by
  -- `d r g y = x (d a + d κ x² + h g)` and `q g x = y (b + κ y²)`
  have hA : d * r * g * y = x * (d * a + d * κ * x ^ 2 + h * g) := by
    linear_combination d * e₁ - e₃
  have hB : q * g * x = y * (b + κ * y ^ 2) := by linear_combination e₂
  have hhg : 0 ≤ h * g := mul_nonneg hh hg
  have hx : x ≠ 0 := by
    intro hx0
    rw [hx0] at hB
    have : y * (b + κ * y ^ 2) = 0 := by linarith
    rcases mul_eq_zero.mp this with h' | h'
    · exact hne (by rw [hx0, h'])
    · nlinarith [sq_nonneg y]
  have hy : y ≠ 0 := by
    intro hy0
    rw [hy0] at hA
    have : x * (d * a + d * κ * x ^ 2 + h * g) = 0 := by linarith
    rcases mul_eq_zero.mp this with h' | h'
    · exact hx h'
    · nlinarith [sq_nonneg x, mul_pos hd ha, mul_nonneg (mul_pos hd hκ).le (sq_nonneg x)]
  have hxy : x * y ≠ 0 := mul_ne_zero hx hy
  -- multiply the two relations and cancel `x y`
  have hkey : d * r * q * g ^ 2 = (d * a + d * κ * x ^ 2 + h * g) * (b + κ * y ^ 2) := by
    apply mul_right_cancel₀ hxy
    linear_combination (q * g * x) * hA + (x * (d * a + d * κ * x ^ 2 + h * g)) * hB
  have hx2 : 0 < x ^ 2 := by positivity
  have h1 : 0 < d * κ * x ^ 2 := by positivity
  have h2 : 0 ≤ κ * y ^ 2 := by positivity
  have h3 : 0 < d * a := mul_pos hd ha
  rw [P_zero]
  nlinarith [mul_pos h1 hb, mul_nonneg (by linarith : (0:ℝ) ≤ d * a + d * κ * x ^ 2 + h * g) h2]

/-- Without the cap, rest is the only equilibrium over the whole Test 4 sweep. -/
theorem only_rest_without_cap {g : ℝ} (hg₀ : 0 ≤ g) (hg : g ≤ 3) {p : ℝ × ℝ × ℝ}
    (hp : fieldNoCap g p = 0) : p = 0 := by
  obtain ⟨x, y, z⟩ := p
  simp only [fieldNoCap, Prod.ext_iff, Prod.fst_zero, Prod.snd_zero] at hp
  obtain ⟨e1, e2, e3⟩ := hp
  have hxy : (x, y) = ((0:ℝ), (0:ℝ)) := by
    by_contra hne
    have := no_coarousal_without_cap_general (a := 1 / 30) (b := 1 / 20) (d := 1 / 4)
      (r := 1 / 25) (q := 1 / 10) (h := 3 / 40) (κ := 1 / 50) (x := x) (y := y) (z := z)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) hg₀
      (by linear_combination e1) (by linear_combination e2) (by linear_combination e3) hne
    -- `P(0, g) = 1/2400 + 3g/800 - g²/1000 > 0` on `[0, 3]`
    rw [P_zero] at this
    nlinarith [mul_nonneg hg₀ (sub_nonneg.mpr hg)]
  simp only [Prod.mk.injEq] at hxy
  obtain ⟨rfl, rfl⟩ := hxy
  have hz : z = 0 := by linarith
  subst hz
  rfl

/-- The one-variable bound behind `only_rest_upto_two` (`u = y²`, value `g = 2`). -/
private lemma bist_f2_pos {u : ℝ} (hu : 0 ≤ u) :
    0 < (0.64 + u) * (1 / 20 + 0.02 * u) / 30 + 0.5 * u * (1 / 20 + 0.02 * u) ^ 3 * (0.64 + u)
      + 0.384 * (1 / 20 + 0.02 * u) - 0.016 * (0.64 + u) := by
  nlinarith [sq_nonneg (u - 2.1), mul_nonneg hu (sq_nonneg (u - 2.1)),
    mul_nonneg (mul_nonneg hu hu) (sq_nonneg (u - 2.1)), pow_nonneg hu 3, pow_nonneg hu 4,
    pow_nonneg hu 5]

private lemma bist_cap_mul (y : ℝ) : cap y * (0.64 + y ^ 2) = 0.64 := by
  unfold cap
  have h : (1 + (y / 0.8) ^ 2 : ℝ) ≠ 0 := by positivity
  rw [div_mul_eq_mul_div, one_mul, div_eq_iff h]
  ring

private lemma bist_cap_pos (y : ℝ) : 0 < cap y := by
  unfold cap; positivity

/-- With the cap, rest is still the only equilibrium for `0 ≤ g ≤ 2`. -/
theorem only_rest_upto_two {g : ℝ} (hg₀ : 0 ≤ g) (hg : g ≤ 2) {p : ℝ × ℝ × ℝ}
    (hp : field g p = 0) : p = 0 := by
  obtain ⟨x, y, z⟩ := p
  simp only [field, Prod.ext_iff, Prod.fst_zero, Prod.snd_zero] at hp
  obtain ⟨e1, e2, e3⟩ := hp
  have hc : cap y * (0.64 + y ^ 2) = 0.64 := bist_cap_mul y
  have hc0 : 0 < cap y := bist_cap_pos y
  have hz : z = 0.3 * g * x * cap y := by linear_combination -4 * e3
  have hw0 : 0 < (1 / 20 : ℝ) + 0.02 * y ^ 2 := by positivity
  have hB : 0.1 * g * x = y * (1 / 20 + 0.02 * y ^ 2) := by linear_combination e2
  have hA : 0.04 * g * y = x * (1 / 30 + 0.3 * g * cap y + 0.02 * x ^ 2) := by
    linear_combination e1 + hz
  have hy : y = 0 := by
    by_contra hy
    rcases eq_or_lt_of_le hg₀ with hg0 | hgpos
    · subst hg0
      have : y * (1 / 20 + 0.02 * y ^ 2) = 0 := by linarith
      rcases mul_eq_zero.mp this with h | h
      · exact hy h
      · linarith
    · have hx : x ≠ 0 := by
        intro hx
        rw [hx] at hB
        have : y * (1 / 20 + 0.02 * y ^ 2) = 0 := by linarith
        rcases mul_eq_zero.mp this with h | h
        · exact hy h
        · linarith
      set w := (1 / 20 : ℝ) + 0.02 * y ^ 2 with hw
      set K := (1 / 30 : ℝ) + 0.3 * g * cap y + 0.02 * x ^ 2 with hK
      -- multiply the first two equations and cancel `x y`
      have hkey : 0.004 * g ^ 2 = K * w := by
        apply mul_left_cancel₀ (mul_ne_zero hx hy)
        linear_combination (0.1 * g * x) * hA + (x * K) * hB
      set u := y ^ 2 with hu
      have hu0 : 0 ≤ u := sq_nonneg y
      set A := (0.64 : ℝ) + u with hA_def
      have hA0 : 0 < A := by positivity
      have hsq : 0.01 * g ^ 2 * x ^ 2 = u * w ^ 2 := by
        linear_combination (0.1 * g * x + y * w) * hB
      have hg2 : g ^ 2 ≤ 4 := by nlinarith only [hg₀, hg]
      have hx2 : 25 * u * w ^ 2 ≤ x ^ 2 := by
        linarith only [hsq, mul_le_mul_of_nonneg_right hg2 (sq_nonneg x)]
      have hmain : 0.004 * g ^ 2 * A = A * w / 30 + 0.192 * g * w + 0.02 * x ^ 2 * w * A := by
        linear_combination A * hkey + 0.3 * g * w * hc
      have hlow : 0.5 * u * w ^ 3 * A ≤ 0.02 * x ^ 2 * w * A := by
        linarith only [mul_le_mul_of_nonneg_right hx2 (le_of_lt (mul_pos hw0 hA0))]
      -- concavity in `g`: the `g`-terms are at least `g/2` times their value at `g = 2`
      have hq : (g / 2) * (0.384 * w - 0.016 * A) ≤ 0.192 * g * w - 0.004 * g ^ 2 * A := by
        linarith only [mul_nonneg (mul_nonneg hg₀ hA0.le) (sub_nonneg.mpr hg)]
      have hf2 : 0 < A * w / 30 + 0.5 * u * w ^ 3 * A + 0.384 * w - 0.016 * A := by
        rw [hA_def, hw]; exact bist_f2_pos hu0
      have hS : 0 < A * w / 30 + 0.5 * u * w ^ 3 * A := by
        have h1 := mul_pos hA0 hw0
        have h2 := mul_nonneg (mul_nonneg hu0 (pow_pos hw0 3).le) hA0.le
        linarith only [h1, h2]
      have h1 : 0 ≤ (1 - g / 2) * (A * w / 30 + 0.5 * u * w ^ 3 * A) :=
        mul_nonneg (by linarith only [hg]) hS.le
      have h2 : 0 < (g / 2) * (A * w / 30 + 0.5 * u * w ^ 3 * A + 0.384 * w - 0.016 * A) :=
        mul_pos (by linarith only [hgpos]) hf2
      linarith only [hmain, hlow, hq, h1, h2]
  subst hy
  have hx : x = 0 := by
    have : x * (1 / 30 + 0.3 * g * cap 0 + 0.02 * x ^ 2) = 0 := by linarith
    rcases mul_eq_zero.mp this with h | h
    · exact h
    · nlinarith [mul_nonneg hg₀ hc0.le, sq_nonneg x]
  subst hx
  have : z = 0 := by rw [hz]; ring
  subst this
  rfl

/-- Given `Aₘ = y`, the value of `Aᵢ` that makes the second equation vanish. -/
private noncomputable def bistX (g y : ℝ) : ℝ := y * (1 / 20 + 0.02 * y ^ 2) / (0.1 * g)

/-- The first component of the field along the curve where the other two vanish. -/
private noncomputable def bistF (g y : ℝ) : ℝ :=
  -bistX g y / 30 - 0.30 * g * bistX g y * cap y + 0.04 * g * y - 0.02 * bistX g y ^ 3

private lemma bist_field_eq {g : ℝ} (hg : g ≠ 0) (y : ℝ) :
    field g (bistX g y, y, 0.30 * g * bistX g y * cap y) = (bistF g y, 0, 0) := by
  simp only [field, bistF, Prod.mk.injEq]
  refine ⟨trivial, ?_, by ring⟩
  have h : 0.1 * g * bistX g y = y * (1 / 20 + 0.02 * y ^ 2) := by
    unfold bistX
    field_simp
  linear_combination h

private lemma bist_cap_cont : Continuous cap := by
  unfold cap
  exact continuous_const.div (by fun_prop) (fun y => by positivity)

private lemma bist_F_cont (g : ℝ) : Continuous (bistF g) := by
  unfold bistF bistX
  have := bist_cap_cont
  fun_prop

private lemma bistX_pos {g y : ℝ} (hg : 0 < g) (hy : 0 < y) : 0 < bistX g y := by
  unfold bistX; positivity

/-- At `g = 2.1` a co-arousal equilibrium exists. -/
theorem coarousal_exists_above_two :
    ∃ p : ℝ × ℝ × ℝ, 0 < p.1 ∧ 0 < p.2.1 ∧ field 2.1 p = 0 := by
  -- `F(1.3) < 0 < F(1.4)`
  have h0 : (0:ℝ) ∈ Set.Icc (bistF 2.1 1.3) (bistF 2.1 1.4) :=
    ⟨by norm_num [bistF, bistX, cap], by norm_num [bistF, bistX, cap]⟩
  obtain ⟨y, ⟨hy1, hy2⟩, hFy⟩ :=
    intermediate_value_Icc (by norm_num : (1.3:ℝ) ≤ 1.4) (bist_F_cont 2.1).continuousOn h0
  refine ⟨(bistX 2.1 y, y, 0.30 * 2.1 * bistX 2.1 y * cap y), ?_, ?_, ?_⟩
  · exact bistX_pos (by norm_num) (by linarith)
  · show 0 < y; linarith
  · rw [bist_field_eq (by norm_num), hFy]; rfl

/-- The characteristic polynomial of a real `3 × 3` matrix. -/
private lemma bist_det3 (M : Matrix (Fin 3) (Fin 3) ℝ) (s : ℂ) :
    (s • (1 : Matrix (Fin 3) (Fin 3) ℂ) - M.map (fun r : ℝ => (r : ℂ))).det =
      s ^ 3 + ((-(M 0 0 + M 1 1 + M 2 2) : ℝ) : ℂ) * s ^ 2 +
        ((M 0 0 * M 1 1 - M 0 1 * M 1 0 + M 0 0 * M 2 2 - M 0 2 * M 2 0 + M 1 1 * M 2 2 -
          M 1 2 * M 2 1 : ℝ) : ℂ) * s + ((-M.det : ℝ) : ℂ) := by
  rw [Matrix.det_fin_three, Matrix.det_fin_three]
  simp
  ring

/-- The Routh–Hurwitz inequalities for the Jacobian at `g = 3`, from crude bounds. -/
private lemma bist_coeffs (M : Matrix (Fin 3) (Fin 3) ℝ) {x y c : ℝ}
    (h00 : M 0 0 = -1 / 30 - 0.06 * x ^ 2) (h01 : M 0 1 = 0.12) (h02 : M 0 2 = -1)
    (h10 : M 1 0 = 0.3) (h11 : M 1 1 = -1 / 20 - 0.06 * y ^ 2) (h12 : M 1 2 = 0)
    (h20 : M 2 0 = 0.225 * c) (h21 : M 2 1 = -0.703125 * x * y * c ^ 2) (h22 : M 2 2 = -1 / 4)
    (hx1 : 1.91 ≤ x) (hx2 : x ≤ 1.92) (hy1 : 2.79 ≤ y) (hy2 : y ≤ 2.792) (hc0 : 0 ≤ c)
    (hc1 : c ≤ 0.08) :
    0 < -(M 0 0 + M 1 1 + M 2 2) ∧ 0 < -M.det ∧
      -M.det < -(M 0 0 + M 1 1 + M 2 2) * (M 0 0 * M 1 1 - M 0 1 * M 1 0 + M 0 0 * M 2 2 -
        M 0 2 * M 2 0 + M 1 1 * M 2 2 - M 1 2 * M 2 1) := by
  rw [Matrix.det_fin_three, h00, h01, h02, h10, h11, h12, h20, h21, h22]
  have hx0 : 0 ≤ x := by linarith
  have hy0 : 0 ≤ y := by linarith
  have hxx1 : 1.91 ^ 2 ≤ x ^ 2 := pow_le_pow_left₀ (by norm_num) hx1 2
  have hxx2 : x ^ 2 ≤ 1.92 ^ 2 := pow_le_pow_left₀ hx0 hx2 2
  have hyy1 : 2.79 ^ 2 ≤ y ^ 2 := pow_le_pow_left₀ (by norm_num) hy1 2
  have hyy2 : y ^ 2 ≤ 2.792 ^ 2 := pow_le_pow_left₀ hy0 hy2 2
  set A1 := (1 / 30 : ℝ) + 0.06 * x ^ 2 with hA1
  set A2 := (1 / 20 : ℝ) + 0.06 * y ^ 2 with hA2
  have hA1l : 0.25 ≤ A1 := by rw [hA1]; norm_num at hxx1 ⊢; linarith
  have hA1u : A1 ≤ 0.27 := by rw [hA1]; norm_num at hxx2 ⊢; linarith
  have hA2l : 0.5 ≤ A2 := by rw [hA2]; norm_num at hyy1 ⊢; linarith
  have hA2u : A2 ≤ 0.52 := by rw [hA2]; norm_num at hyy2 ⊢; linarith
  have hm00 : (-1 / 30 - 0.06 * x ^ 2 : ℝ) = -A1 := by rw [hA1]; ring
  have hm11 : (-1 / 20 - 0.06 * y ^ 2 : ℝ) = -A2 := by rw [hA2]; ring
  rw [hm00, hm11]
  have hc2 : c ^ 2 ≤ 0.08 ^ 2 := pow_le_pow_left₀ hc0 hc1 2
  have hxy : x * y ≤ 1.92 * 2.792 := mul_le_mul hx2 hy2 hy0 (by norm_num)
  have hxyc : x * y * c ^ 2 ≤ 1.92 * 2.792 * 0.08 ^ 2 :=
    mul_le_mul hxy hc2 (sq_nonneg c) (by norm_num)
  have hxyc0 : 0 ≤ x * y * c ^ 2 := by positivity
  have hP1 : 0.25 * 0.5 ≤ A1 * A2 := mul_le_mul hA1l hA2l (by norm_num) (by linarith)
  have hP2 : A1 * A2 ≤ 0.27 * 0.52 := mul_le_mul hA1u hA2u (by linarith) (by norm_num)
  have hA2c : 0 ≤ A2 * c := mul_nonneg (by linarith) hc0
  have hA2c' : A2 * c ≤ 0.52 * 0.08 := mul_le_mul hA2u hc1 hc0 (by norm_num)
  norm_num at hxyc hP1 hP2 hA2c'
  refine ⟨by linarith, by linarith, ?_⟩
  have hc1l : 0.27 ≤ A1 * A2 - 0.036 + A1 / 4 + 0.225 * c + A2 / 4 := by linarith
  have hc2l : 1 ≤ A1 + A2 + 1 / 4 := by linarith
  have hprod := mul_le_mul hc2l hc1l (by norm_num) (by linarith)
  linarith

/-- At `g = 3` a linearly stable co-arousal equilibrium exists. -/
theorem coarousal_stable_at_three :
    ∃ p : ℝ × ℝ × ℝ, 0 < p.1 ∧ 0 < p.2.1 ∧ field 3 p = 0 ∧
      ∀ s : ℂ, (s • (1 : Matrix (Fin 3) (Fin 3) ℂ) - (jac 3 p).map (fun r : ℝ => (r : ℂ))).det = 0 →
        s.re < 0 := by
  -- `F(2.792) < 0 < F(2.79)`
  have h0 : (0:ℝ) ∈ Set.Icc (bistF 3 2.792) (bistF 3 2.79) :=
    ⟨by norm_num [bistF, bistX, cap], by norm_num [bistF, bistX, cap]⟩
  obtain ⟨y, ⟨hy1, hy2⟩, hFy⟩ :=
    intermediate_value_Icc' (by norm_num : (2.79:ℝ) ≤ 2.792) (bist_F_cont 3).continuousOn h0
  have hxpos : 0 < bistX 3 y := bistX_pos (by norm_num) (by linarith)
  refine ⟨(bistX 3 y, y, 0.30 * 3 * bistX 3 y * cap y), hxpos, by show 0 < y; linarith,
    by rw [bist_field_eq (by norm_num), hFy]; rfl, ?_⟩
  intro s hs
  set x := bistX 3 y with hx_def
  -- bounds on the equilibrium: `x ∈ [1.91, 1.92]`, `cap y ≤ 0.08`
  have hxw : 0.3 * x = y * (1 / 20 + 0.02 * y ^ 2) := by
    rw [hx_def, show (0.3:ℝ) = 0.1 * 3 by norm_num]; unfold bistX; field_simp
  have hy0 : 0 ≤ y := by linarith
  have hyyy1 : 2.79 ^ 3 ≤ y ^ 3 := pow_le_pow_left₀ (by norm_num) hy1 3
  have hyyy2 : y ^ 3 ≤ 2.792 ^ 3 := pow_le_pow_left₀ hy0 hy2 3
  have hx1 : 1.91 ≤ x := by norm_num at hyyy1; linarith
  have hx2 : x ≤ 1.92 := by norm_num at hyyy2; linarith
  have hc := bist_cap_mul y
  have hc0 := bist_cap_pos y
  have hyy1 : 2.79 ^ 2 ≤ y ^ 2 := pow_le_pow_left₀ (by norm_num) hy1 2
  have hc1 : cap y ≤ 0.08 := by
    have := mul_le_mul_of_nonneg_left (show (8:ℝ) ≤ 0.64 + y ^ 2 by norm_num at hyy1 ⊢; linarith)
      hc0.le
    linarith
  have hd : capDeriv y = -(2 * y / 0.64) * cap y ^ 2 := by
    unfold capDeriv cap
    rw [one_div, inv_pow, ← div_eq_mul_inv]
  -- the characteristic polynomial and its Routh–Hurwitz coefficients
  rw [bist_det3] at hs
  obtain ⟨k2, k0, k21⟩ := bist_coeffs (jac 3 (x, y, 0.30 * 3 * x * cap y)) (x := x) (y := y)
    (c := cap y) (by simp [jac]) (by simp [jac]; norm_num) (by simp [jac])
    (by simp [jac]; norm_num) (by simp [jac]) (by simp [jac])
    (by simp [jac]; ring) (by simp [jac, hd]; ring) (by simp [jac])
    hx1 hx2 hy1 hy2 hc0.le hc1
  exact cubic_hurwitz k2 k0 k21 hs

end Wyrd.Limits
