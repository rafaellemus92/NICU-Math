import WyrdMathlib.Rainbow.Deriv
import WyrdMathlib.Rainbow.MinLemma

/-!
# The rainbow: where the bright bow sits

For `1 < n < k + 1` (water, `n ≈ 4/3`, qualifies for every `k ≥ 1`), the
deviation `D` of the `k`-th bow has exactly one stationary point on
`[0, π/2]`, at `cos² i = (n² - 1) / (k(k+2))`, and it is the strict minimum.
-/

namespace Wyrd.Rainbow

open Real

/-- `q = (n² - 1)/(k(k+2))` lies strictly between `0` and `1`:
`0 < n² - 1 < (k+1)² - 1 = k(k+2)`. -/
private lemma bow_aux_q_mem {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    0 < (n ^ 2 - 1) / (k * (k + 2)) ∧ (n ^ 2 - 1) / (k * (k + 2)) < 1 := by
  have hk1 : (1 : ℝ) ≤ k := by exact_mod_cast hk
  have hkk : (0 : ℝ) < k * (k + 2) := by positivity
  constructor
  · exact div_pos (by nlinarith) hkk
  · rw [div_lt_one hkk]; nlinarith

/-- Hence `0 < √q < 1`, so `√q` is a valid cosine of an angle in `(0, π/2)`. -/
private lemma bow_aux_sqrt_mem {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    0 < √((n ^ 2 - 1) / (k * (k + 2))) ∧ √((n ^ 2 - 1) / (k * (k + 2))) < 1 := by
  obtain ⟨h0, h1⟩ := bow_aux_q_mem hn hk hnk
  exact ⟨Real.sqrt_pos.2 h0, (Real.sqrt_lt' one_pos).2 (by simpa using h1)⟩

/-- `cos i₀ = √q`, where `i₀ = arccos √q` is the bow's incidence angle. -/
private lemma bow_aux_cos {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    cos (bowIncidence k n) = √((n ^ 2 - 1) / (k * (k + 2))) := by
  obtain ⟨h0, h1⟩ := bow_aux_sqrt_mem hn hk hnk
  rw [bowIncidence, cos_arccos (by linarith) h1.le]

/-- On `[0, π/2]` the cosine is nonnegative. -/
private lemma bow_aux_cos_nonneg {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) : 0 ≤ cos i :=
  cos_nonneg_of_neg_pi_div_two_le_of_le (by linarith [pi_pos, hi.1]) hi.2

/-- At the bow's incidence angle, `cos² i = (n² - 1)/(k(k+2))`. -/
theorem cos_bowIncidence_sq {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    cos (bowIncidence k n) ^ 2 = (n ^ 2 - 1) / (k * (k + 2)) := by
  -- `cos (arccos √q) = √q`, and `(√q)² = q` since `q ≥ 0`
  rw [bow_aux_cos hn hk hnk, Real.sq_sqrt (bow_aux_q_mem hn hk hnk).1.le]

/-- The bow's incidence angle is a genuine angle of entry, strictly between `0` and `π/2`. -/
theorem bowIncidence_mem {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    bowIncidence k n ∈ Set.Ioo 0 (π / 2) := by
  -- `arccos x ∈ (0, π/2)` exactly when `0 < x < 1`
  obtain ⟨h0, h1⟩ := bow_aux_sqrt_mem hn hk hnk
  exact ⟨arccos_pos.2 h1, arccos_lt_pi_div_two.2 h0⟩

/-- The deviation is stationary at the bow. -/
theorem deriv_dev_bowIncidence {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    deriv (dev k n) (bowIncidence k n) = 0 := by
  -- `cos i₀ = √q ≥ 0` and `cos² i₀ = q`: exactly the stationarity condition
  have hc : 0 ≤ cos (bowIncidence k n) := by
    rw [bow_aux_cos hn hk hnk]; exact Real.sqrt_nonneg _
  exact (deriv_dev_eq_zero_iff hn hk hc).2 (cos_bowIncidence_sq hn hk hnk)

/-- The only stationary point of `D` on `[0, π/2]` is the bow's incidence angle. -/
theorem deriv_dev_eq_zero_iff_eq {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1)
    {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) :
    deriv (dev k n) i = 0 ↔ i = bowIncidence k n := by
  have hc := bow_aux_cos_nonneg hi
  constructor
  · intro h
    -- stationary means `cos² i = q`; with `cos i ≥ 0` this is `cos i = √q`
    have hsq := (deriv_dev_eq_zero_iff hn hk hc).1 h
    have hcos : cos i = √((n ^ 2 - 1) / (k * (k + 2))) := by
      rw [← hsq, Real.sqrt_sq hc]
    -- and `arccos` undoes `cos` on `[0, π]`
    rw [bowIncidence, ← hcos, arccos_cos hi.1 (by linarith [pi_pos, hi.2])]
  · rintro rfl
    exact deriv_dev_bowIncidence hn hk hnk

/-- Left of the bow, `D` falls: for `i ∈ (0, i₀)`, `cos i > cos i₀ = √q ≥ 0`, so `cos² i > q`. -/
private lemma bow_aux_deriv_neg {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    ∀ x ∈ Set.Ioo 0 (bowIncidence k n), deriv (dev k n) x < 0 := by
  intro x hx
  have hmem := bowIncidence_mem hn hk hnk
  have hc0 : 0 ≤ cos (bowIncidence k n) := by
    rw [bow_aux_cos hn hk hnk]; exact Real.sqrt_nonneg _
  -- cosine is strictly decreasing on `[0, π]`
  have hlt : cos (bowIncidence k n) < cos x :=
    cos_lt_cos_of_nonneg_of_le_pi hx.1.le (by linarith [pi_pos, hmem.2]) hx.2
  have hcx : 0 ≤ cos x := hc0.trans hlt.le
  rw [deriv_dev_neg_iff hn hk hcx, ← cos_bowIncidence_sq hn hk hnk]
  exact pow_lt_pow_left₀ hlt hc0 two_ne_zero

/-- Right of the bow, `D` rises: for `i ∈ (i₀, π/2)`, `0 ≤ cos i < cos i₀ = √q`, so `cos² i < q`. -/
private lemma bow_aux_deriv_pos {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    ∀ x ∈ Set.Ioo (bowIncidence k n) (π / 2), 0 < deriv (dev k n) x := by
  intro x hx
  have hmem := bowIncidence_mem hn hk hnk
  have hcx : 0 ≤ cos x := bow_aux_cos_nonneg ⟨(hmem.1.trans hx.1).le, hx.2.le⟩
  -- cosine is strictly decreasing on `[0, π]`
  have hlt : cos x < cos (bowIncidence k n) :=
    cos_lt_cos_of_nonneg_of_le_pi hmem.1.le (by linarith [pi_pos, hx.2]) hx.1
  rw [deriv_dev_pos_iff hn hk hcx, ← cos_bowIncidence_sq hn hk hnk]
  exact pow_lt_pow_left₀ hlt hcx two_ne_zero

/-- **The bow is the strict minimum of the deviation.** -/
theorem dev_lt_of_ne {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1)
    {i : ℝ} (hi : i ∈ Set.Icc 0 (π / 2)) (hne : i ≠ bowIncidence k n) :
    dev k n (bowIncidence k n) < dev k n i := by
  -- falling on `(0, i₀)`, rising on `(i₀, π/2)`: the calculus lemma does the rest
  have hmem := bowIncidence_mem hn hk hnk
  exact lt_of_deriv_sign hmem.1.le hmem.2.le (continuous_dev hn k).continuousOn
    (bow_aux_deriv_neg hn hk hnk) (bow_aux_deriv_pos hn hk hnk) i hi hne

/-- The bow minimises the deviation over all incidence angles `[0, π/2]`. -/
theorem dev_isMinOn {n : ℝ} {k : ℕ} (hn : 1 < n) (hk : 1 ≤ k) (hnk : n < k + 1) :
    IsMinOn (dev k n) (Set.Icc 0 (π / 2)) (bowIncidence k n) := by
  -- same sign pattern, non-strict conclusion
  have hmem := bowIncidence_mem hn hk hnk
  exact isMinOn_of_deriv_sign hmem.1.le hmem.2.le (continuous_dev hn k).continuousOn
    (bow_aux_deriv_neg hn hk hnk) (bow_aux_deriv_pos hn hk hnk)

/-- Water (`n = 4/3`): the primary bow (`k = 1`) is where `cos² i = 7/27`. -/
theorem water_primary :
    cos (bowIncidence 1 (4 / 3)) ^ 2 = 7 / 27 ∧
      IsMinOn (dev 1 (4 / 3)) (Set.Icc 0 (π / 2)) (bowIncidence 1 (4 / 3)) := by
  -- `1 < 4/3 < 1 + 1`
  have hn : (1 : ℝ) < 4 / 3 := by norm_num
  have hnk : (4 / 3 : ℝ) < ((1 : ℕ) : ℝ) + 1 := by norm_num
  refine ⟨?_, dev_isMinOn hn le_rfl hnk⟩
  -- `q = (16/9 - 1) / (1 · 3) = 7/27`
  rw [cos_bowIncidence_sq hn le_rfl hnk]
  norm_num

/-- Water (`n = 4/3`): the secondary bow (`k = 2`) is where `cos² i = 7/72`. -/
theorem water_secondary :
    cos (bowIncidence 2 (4 / 3)) ^ 2 = 7 / 72 ∧
      IsMinOn (dev 2 (4 / 3)) (Set.Icc 0 (π / 2)) (bowIncidence 2 (4 / 3)) := by
  -- `1 < 4/3 < 2 + 1`
  have hn : (1 : ℝ) < 4 / 3 := by norm_num
  have hk : 1 ≤ 2 := by norm_num
  have hnk : (4 / 3 : ℝ) < ((2 : ℕ) : ℝ) + 1 := by norm_num
  refine ⟨?_, dev_isMinOn hn hk hnk⟩
  -- `q = (16/9 - 1) / (2 · 4) = 7/72`
  rw [cos_bowIncidence_sq hn hk hnk]
  norm_num

end Wyrd.Rainbow
