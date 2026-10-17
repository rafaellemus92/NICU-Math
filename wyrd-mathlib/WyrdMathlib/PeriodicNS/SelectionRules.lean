import Mathlib

/-!
# Selection rules for phase harmonics in the enstrophy Taylor series

From the audit of `periodic_ns_lab_v2`. Take initial data
`u₀ = (α sin y, β sin z, γ cos x − δ cos(x + y + φ))` on the `2π`-periodic cube.
Each term of `[tⁿ] Z` is `νᵉ` times a product of initial Fourier factors. Each
factor is one of:

* `α±`, wave vector `±(0,1,0)`;
* `β±`, wave vector `±(0,0,1)`;
* `γ±`, wave vector `±(1,0,0)`;
* `δ±`, wave vector `±(1,1,0)`, carrying `e^{±iφ}`.

A spatial average keeps only terms whose wave vectors sum to zero
(`Counts.Balanced`). The term's phase harmonic is `m = #δ₊ − #δ₋`.

This file proves the **arithmetic** that follows:

* `deg_ge_of_beta`: a balanced term with at least one `β` factor has amplitude
  degree `d ≥ 3|m| + 2`;
* `deg_parity`: `d ≡ m (mod 2)`;
* `not_before`: with the grading `d + e = n + 2`, a harmonic carried by such a
  term cannot appear before order `n = 3|m|`;
* `at_first_order`: at `n = 3|m|` (`|m| ≥ 2`), necessarily `e = 0`
  (viscosity-independent). The term is then exactly `α^|m| β² γ^|m| δ^|m|`, with
  no opposite-sign pairs;
* `order_seven_m_two`: for `|m| = 2` at order 7, `e = 1` and `d = 8`. So (given P1 and
  the recurrence structure, see below) the `cos 2φ` coefficient of `[t⁷] Z` is a
  constant times `ν` and vanishes for Euler;
* `euler_parity`: for `ν = 0` (`e = 0`), only `n ≡ m (mod 2)` survives.

**Not formalised here** (proved on paper in the audit report, and checked by
exact rational computation with symbolic `ν` up to order 16):

* that `[tⁿ] Z` has this monomial structure with `d + e = n + 2`, which follows
  from the Taylor recurrence;
* the 2D-3C fact (P1): with `β = 0`, `u₃` evolves linearly and only `|m| ≤ 1`
  occurs, so every `|m| ≥ 2` term contains a `β` factor.

That the leading coefficient is actually nonzero was computed exactly for
`|m| = 2, 3, 4`. For `|m| = 2` it is `−6487/3110400` per Laurent coefficient,
that is `−6487/1555200` for `cos 2φ`.
-/

namespace Wyrd.PeriodicNS

/-- Counts of signed initial factors in one term. -/
structure Counts where
  ap : ℕ
  am : ℕ
  bp : ℕ
  bm : ℕ
  gp : ℕ
  gm : ℕ
  dp : ℕ
  dm : ℕ

namespace Counts

/-- Amplitude degree. -/
def deg (c : Counts) : ℕ := c.ap + c.am + c.bp + c.bm + c.gp + c.gm + c.dp + c.dm

/-- Phase harmonic `m`. -/
def harm (c : Counts) : ℤ := (c.dp : ℤ) - c.dm

/-- Zero total wave vector (x, y and z balance). -/
def Balanced (c : Counts) : Prop :=
  (c.gp : ℤ) - c.gm + c.dp - c.dm = 0 ∧ (c.ap : ℤ) - c.am + c.dp - c.dm = 0 ∧ c.bp = c.bm

end Counts

theorem deg_ge_of_beta {c : Counts} (h : c.Balanced) (hb : 0 < c.bp + c.bm) :
    3 * c.harm.natAbs + 2 ≤ c.deg := by
  obtain ⟨h1, h2, h3⟩ := h
  simp only [Counts.harm, Counts.deg] at *
  omega

theorem deg_parity {c : Counts} (h : c.Balanced) : ((c.deg : ℤ) - c.harm) % 2 = 0 := by
  obtain ⟨h1, h2, h3⟩ := h
  simp only [Counts.harm, Counts.deg] at *
  omega

theorem not_before {c : Counts} {n e : ℕ} (h : c.Balanced) (hb : 0 < c.bp + c.bm)
    (hg : c.deg + e = n + 2) : 3 * c.harm.natAbs ≤ n := by
  have := deg_ge_of_beta h hb
  omega

theorem at_first_order {c : Counts} {n e : ℕ} (h : c.Balanced) (hb : 0 < c.bp + c.bm)
    (hg : c.deg + e = n + 2) (hn : n = 3 * c.harm.natAbs) :
    e = 0 ∧ c.bp = 1 ∧ c.bm = 1 ∧ c.ap + c.am = c.harm.natAbs ∧
      c.gp + c.gm = c.harm.natAbs ∧ c.dp + c.dm = c.harm.natAbs := by
  have h0 := deg_ge_of_beta h hb
  obtain ⟨h1, h2, h3⟩ := h
  simp only [Counts.harm, Counts.deg] at *
  omega

theorem order_seven_m_two {c : Counts} {e : ℕ} (h : c.Balanced) (hb : 0 < c.bp + c.bm)
    (hm : c.harm.natAbs = 2) (hg : c.deg + e = 7 + 2) : e = 1 ∧ c.deg = 8 := by
  have h0 := deg_ge_of_beta h hb
  have hp := deg_parity h
  obtain ⟨h1, h2, h3⟩ := h
  simp only [Counts.harm, Counts.deg] at *
  omega

theorem euler_parity {c : Counts} {n : ℕ} (h : c.Balanced) (hg : c.deg + 0 = n + 2) :
    ((n : ℤ) - c.harm) % 2 = 0 := by
  have hp := deg_parity h
  omega

end Wyrd.PeriodicNS
