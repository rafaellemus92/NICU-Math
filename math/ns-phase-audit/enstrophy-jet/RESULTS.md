# Results: the enstrophy Taylor jet of a phase family of Navier–Stokes flows

This file explains what was computed, what it shows, and what it cannot show.
Every number points to a file in this folder, a file elsewhere in this repository, or a cited
source. "AUDIT.md" means the lab-v2 audit, [`../audit_v2/AUDIT.md`](../audit_v2/AUDIT.md).
"Analogy" marks a comparison that is only a picture. "Open" marks a question nobody has settled.

## Summary

ChatGPT's package `periodic_ns_lab_v2` (in this repository as
[`../../inputs/periodic_ns_lab_v2_audit.zip`](../../inputs/periodic_ns_lab_v2_audit.zip)) studied
a one-parameter family of flows and claimed one exact result: the enstrophy first depends on
cos 2φ at order t⁶, with coefficient −6487/1555200 (cosine form) for every viscosity. Three
independent programs here confirm it, two in exact arithmetic and one in floating point. They also
give the full t⁷ term and the cos 2φ part of the t⁸ term, which the package did not have.

This folder was made in a separate session and shares no code with the lab-v2 audit next to it,
[`../audit_v2/AUDIT.md`](../audit_v2/AUDIT.md). Its exact series agrees with that audit's,
entry for entry, through t¹² and extends it to t¹⁴ (Section 1).

Two rules explain the shape of every coefficient through t¹⁴. One comes from running time
backwards. The other says a cos(mφ) term needs at least 3m nonlinear steps, because without the
sin z part of the flow the phase is just carried along like dye. These rules predict that cos 3φ
first appears at t⁹ and cos 4φ at t¹². The computation confirms both. The counting step is
checked in Lean; its two inputs are proved on paper only (Section 4.2).

The series is exact at t = 0 but does not reach far. Against the package's simulation it is good
to about 3 × 10⁻⁵ at t = 1, off by about 5 × 10⁻² at t = 1.5, and useless at t = 2 and t = 4. So
it cannot explain the simulation's finite-time phase optimum. None of this bears on the open
question of whether unforced Navier–Stokes flows stay smooth forever.

---

## 1. The family and the conventions

**Equation.** Incompressible Navier–Stokes on the periodic cube [0, 2π]³, with no external force:

    u_t + (u·∇)u = −∇p + ν Δu,    div u = 0.

ν is the viscosity. The package's simulations use ν = 1/28.

**Initial data (the φ-family).**

    u(x, 0) = (sin y,  sin z,  cos x − cos(x + y + φ)).

Changing φ only slides one Fourier mode in phase. Every member therefore starts with the same
energy E = 1 and the same enstrophy Z = 5/4 (`results/series.json`, orders 0). This is also a
Lean theorem, `quantities_vphi` in
[`PhaseFamily.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/PhaseFamily.lean), and is checked
numerically by
[`phase_family_quantities.py`](../../numerics/navier-stokes/phase_family_quantities.py).

**Quantities.** With ⟨·⟩ the average over the cube:

    E = ½ ⟨|u|²⟩   (energy),     Z = ½ ⟨|curl u|²⟩   (enstrophy: the mean-square vorticity).

**The jet.** "Jet" means the Taylor series in time at t = 0:

    Z(t, φ) = Σₙ Zₙ(φ) tⁿ.

Each Zₙ is computed exactly from the equation by a recurrence. Each is a polynomial in ν with
rational coefficients and a finite Fourier series in φ.

*Analogy:* this is like describing a breath only by the flow, its rate of change, the rate of
change of that, and so on, at the instant it begins. Each number is exact. But a finite list of
them, with no error bound, cannot tell you the tidal volume at end-inspiration.

**Laurent versus cosine coefficients.** The files store Laurent coefficients c\[n, m\](ν):

    Z(t, φ) = Σₙ Σₘ c[n, m](ν) tⁿ e^{imφ}.

The flow has an exact symmetry, so Z(t, φ) = Z(t, −φ) and c[n, −m] = c[n, m]. (At t = 0 this is
in Lean: a rotation plus a shift maps u₀^φ to u₀^{−φ}, a mirror fixes u₀^φ, and E, Z, D, S are
even in φ; `rotShift_vphi`, `mirror_fixes_vphi` and `quantities_even` in
[`PhaseSymmetry.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/PhaseSymmetry.lean). That
Z(t, ·) stays even for t > 0 also needs uniqueness of the solution, which is not in Lean; see
[AUDIT.md](../audit_v2/AUDIT.md) §5.7.) In cosine form:

    [tⁿ] Z = c[n, 0] + Σ_{m≥1} 2 c[n, m] cos(mφ).

**So the cosine coefficient is 2c for m ≥ 1.** The package's −6487/1555200 is a cosine coefficient.
The matching Laurent coefficient is −6487/3110400. Below, every quoted coefficient says which form
it is in.

Where to look: `results/series.json` holds every Laurent c\[n, m\](ν) for n ≤ 14.
`python3 show_series.py --orders n …` prints any orders readably (t⁶–t⁸ by default);
`results/series_summary.txt` holds the `--all` output (t⁶–t⁸ plus the rule checks and partial sums).

**Same object as the lab-v2 audit.** c[n, m] is the z_{n,m} of [AUDIT.md](../audit_v2/AUDIT.md)
§1, at unit amplitudes, with the same Laurent convention and normalization and with ν kept
symbolic in both. That audit's exact
series ([`../audit_v2/exact/z12_unit.json`](../audit_v2/exact/z12_unit.json), printed in
[`tables_unit.txt`](../audit_v2/exact/tables_unit.txt); AUDIT.md §4.1 and §4.3) agrees with
`results/series.json` entry for entry through n = 12: 61 Z and 53 E harmonic polynomials, equal as
Fractions (`python3 compare_audit_v2.py`, `results/compare_audit_v2.log`). This folder extends the
series to n = 14. The first two orders also match the t = 0 identities re-derived in
[`nslab_v1_exact_identities.py`](../../numerics/navier-stokes/nslab_v1_exact_identities.py):
Z′(0) = cos φ/4 − 7ν/2 and Z″(0) = 5/4 − (5/2)ν cos φ + 11ν².

## 2. ChatGPT's t⁶ claim, checked three ways

**The claim** (package `RESULTS.md` and `proof_notes.md`, inside
[`../../inputs/periodic_ns_lab_v2_audit.zip`](../../inputs/periodic_ns_lab_v2_audit.zip)). Through
t⁵, Z depends on φ only through a constant and cos φ. At t⁶ the first new harmonic appears,
−(6487/1555200) t⁶ cos 2φ, and this coefficient does not depend on ν.

**Verdict: correct.** Three programs that share no code give the same answer:

| Program | Nonlinear term | Arithmetic | What it gives |
|---|---|---|---|
| `taylor_exact.py` | advective, −P[(u·∇)u] | exact rationals, ν kept as a symbol | Laurent c[6, ±2] = −6487/3110400 as a constant polynomial in ν |
| `exact_single_nu.py` | rotational, P[u × curl u] | exact complex rationals, ν a fixed number | same values at every ν tried |
| `float_check.py` | rotational, P[u × curl u] | 64-bit floating point on an FFT grid | agrees with every c[n, m] to rounding |

P is the projection that removes the gradient part of a field; it is how the pressure keeps the
flow incompressible. The two forms of the nonlinear term differ by a gradient, which P removes. So
an error would have to appear in two different formulations and two kinds of arithmetic at once.

Evidence:
- `taylor_exact.py` reproduces `results/series.json`: through n = 8 in `tests/test_jet.py`, and
  through n = 14 in a fresh 10.5-minute run that matched in every field except the timings
  (`results/taylor_exact_n14.log`).
- `exact_single_nu.py`: zero exact mismatches at ν = 1/28 (n ≤ 8), −2/3 (n ≤ 7) and 3 (n ≤ 5) in
  this folder (`results/exact_single_nu.log`). An earlier run at 12 further values of ν through
  n = 11 also found zero mismatches (`results/earlier_runs/reconcile_compare_nodes.log`).
- `float_check.py`: worst error 6.5 × 10⁻¹³ relative to each order's largest coefficient, for
  ν = 0, 1/28 and 1/3 and all n ≤ 14 (`results/float_check.log`).
- A fourth route, the leaf decomposition below, also gives Laurent −6487/3110400
  (`results/decompose.log`).
- The lab-v2 audit reached the same value with its own exact and float codes
  ([AUDIT.md](../audit_v2/AUDIT.md) §4.1).

ChatGPT's own proof of ν-independence evaluated the t⁶ coefficient at 7 exact values of ν and used
the bound "degree in ν ≤ n". That argument is valid (`results/earlier_runs/audit_node_parity.txt`).
Section 4 gives a second proof that needs no interpolation.

## 3. Beyond the package: all of t⁷, and the cos 2φ part of t⁸

All from `results/series.json`, printed in `results/series_summary.txt`.

**The t⁷ term, every harmonic.**

    [t⁷] Z = c[7,0] + 2c[7,1] cos φ + 2c[7,2] cos 2φ

    c[7,0]  = −(8116327869497/13975769808000) ν − (198133/6075) ν³ − (188431/1890) ν⁵ − (74/45) ν⁷
    2c[7,1] = −47271934743389/1677092376960000 + (56494201/16329600) ν² + (6011/420) ν⁴ + (769/315) ν⁶
    2c[7,2] = (207269/7257600) ν

The 2c lines are cosine coefficients; c[7,0] is the same in both forms. AUDIT.md §4.1 and §4.3
print the Laurent halves, for example z_{7,2} = (207269/14515200) ν.

- There is no cos 3φ or cos 4φ at t⁷.
- The cos 2φ term is exactly linear in ν. With no viscosity it vanishes.
- With no viscosity, the whole t⁷ term is −0.0281868 cos φ.
- At ν = 1/28: [t⁷]Z = −0.0222323 − 0.0237508 cos φ + 0.0010200 cos 2φ.

**The t⁸ cos 2φ coefficient** (cosine form; the Laurent c[8,2] is half).

    2c[8,2] = 7035947189629/3354184753920000 − (7261/120960) ν²  =  0.00209766 − 0.0600281 ν²

At ν = 1/28 it is 0.0020211. There is no cos 3φ or cos 4φ at t⁸. The full c[8, 0] and c[8, 1]
are in `results/series_summary.txt`.

**One way to read the cos 2φ terms.** The cos 2φ dependence is born at t⁶ with no help from
viscosity. At t⁷ viscosity adds its first correction, with the opposite sign. Together the two
terms equal c₆ t⁶ (1 − λνt) with λ = 621807/90818 ≈ 6.85 (`results/decompose.log`). This looks
like damping at rate λν. That is an interpretation of two Taylor terms, not a decay law. The ν²
part of the t⁸ coefficient (Laurent γ = −7261/241920 ≈ −0.0300) is not what a pure exponential
e^{−λνt} would give (−0.0489, also Laurent).

**A sanity check.** The highest power of ν at each order comes from steps with no nonlinearity,
when the flow simply diffuses like heat. Then Z = ¾ e^{−2νt} + ½ e^{−4νt}, so the top coefficient
of c[n, 0] must be [¾(−2)ⁿ + ½(−4)ⁿ]/n!. That gives −74/45 at n = 7 and 103/126 at n = 8, and
both match (`results/earlier_runs/reconcile_check_claims.log`).

## 4. Two rules that fix the shape of every coefficient

Both rules hold for every c[n, m] with n ≤ 14 (`python3 show_series.py --rules`). They are also
sharp there: every power of ν they allow actually occurs. They are the same selection rules as
P1 and P2 of [AUDIT.md](../audit_v2/AUDIT.md) §4.2, reached separately; that audit found zero
violations, exactly for n ≤ 9 and in floating point for n ≤ 12 (§4.3).

### 4.1 Rule A: time-reversal parity

**Statement.** c\[n, m\](−ν) = (−1)^{n+m} c\[n, m\](ν). Equivalently, c[n, m] contains only powers νᵖ
with p of the same parity as n + m.

**Proof.** Write u = Σ Uₙ tⁿ. The recurrence is

    (n+1) U_{n+1} = ν ΔUₙ + Σⱼ B(Uⱼ, U_{n−j}),     B(a, b) = −P[(a·∇)b],     U₀ = u(·, 0).

1. Set Vₙ = (−1)^{n+1} Uₙ. B is bilinear and (−1)^{j+1}(−1)^{n−j+1} = (−1)ⁿ, so the Vₙ satisfy
   the same recurrence with ν replaced by −ν, starting from V₀ = −U₀. This is the series form of
   the fact that v(x, t) = −u(x, −t) solves Navier–Stokes with viscosity −ν.
2. Z is quadratic, so [tⁿ]Z picks up (−1)ⁿ: zₙ(−ν; −u₀) = (−1)ⁿ zₙ(ν; u₀).
3. A direct check gives −u₀^φ(x) = u₀^{φ+π}(x + (π, π, π)). Shifting x does not change Z.
4. So zₙ(−ν, φ + π) = (−1)ⁿ zₙ(ν, φ). Comparing e^{imφ} coefficients gives the statement.

This is pure algebra on the recurrence. It does not need the backward-in-time problem to make sense.

**Relation to the lab-v2 audit and to Lean.** AUDIT.md §4.2 gets the same parity another way:
from `deg_parity` in
[`SelectionRules.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/SelectionRules.lean) plus the
grading d + e = n + 2, which AUDIT.md proves on paper only. The proof above does not use the
grading, so the parity rule has two independent paper proofs. Only step 3 at φ = 0 is in Lean:
`neg_v_translate` in
[`PhaseFamily.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/PhaseFamily.lean) states
−u₀^0(x) = u₀^π(x + (π, π, π)). Step 3 for general φ and the sign flip of steps 1–2 are not in
Lean.

**Consequences.** c[6, 1], c[7, 0] and c[8, 1] vanish at ν = 0. At ν = 0, even orders carry only
even harmonics and odd orders only odd harmonics.

### 4.2 Rule B: harmonic m needs at least 3m nonlinear steps (m ≥ 2)

**Bookkeeping.** Split the initial velocity into its 8 Fourier pieces ("leaves"):

| Leaf | Field | Wavevector | Phase charge |
|---|---|---|---|
| a± | sin y in u_x | (0, ±1, 0) | 0 |
| b± | sin z in u_y | (0, 0, ±1) | 0 |
| c± | cos x in u_z | (±1, 0, 0) | 0 |
| d± | −cos(x+y+φ) in u_z | ±(1, 1, 0) | ±1 |

Every term of Uₙ is a tree built from copies of these leaves. A term with L leaves uses L − 1
nonlinear steps and n − L + 1 viscous steps, so it carries ν^{n−L+1}. A term of [tⁿ]Z pairs two
trees, so it has L leaves in total and carries ν^{n+2−L}. The cube average keeps only terms whose
wavevectors add to zero. The harmonic is m = (number of d+) − (number of d−).

**Counting.** For m > 0 there must be at least m leaves d+. Their x-components must be cancelled,
which needs at least m leaves c−. Their y-components need at least m leaves a−. That is 3m leaves.
Counting alone would allow cos 2φ already at t⁴, from {d+², c−², a−²}.

**The lemma: without sin z, the phase is a passive scalar.** Each term is a product of leaf
amplitudes, so the terms with no b leaf are exactly the series of the flow with the sin z part
removed. That flow keeps the form u = (U(y, t), 0, w(x, y, t)) and solves Navier–Stokes
exactly with zero pressure. U just diffuses: U = e^{−νt} sin y. The phase lives only in w, which
obeys

    w_t + U(y, t) ∂ₓw = ν Δw.

This is linear in w, and its coefficient does not depend on x, so each x-wavenumber of w evolves
on its own. w starts with x-wavenumbers ±1 only. The +1 part carries phase charge 0 or +1, the −1
part carries 0 or −1. Z pairs a +1 part with a −1 part, so its harmonic is −1, 0 or +1. Hence
terms with no b leaf have |m| ≤ 1.

*Analogy:* dye stirred by a shear flow. The dye is carried and spread, but it cannot stir itself,
so it cannot multiply with itself.

**Conclusion.** For |m| ≥ 2 a term needs b leaves. Their z-components must cancel, so it needs at
least two (one b+ and one b−). So L ≥ 3m + 2, which means at least 3m nonlinear steps. Because the
ν-power n + 2 − L cannot be negative:

- c[n, m] = 0 for n < 3m, and deg_ν c[n, m] ≤ n − 3m;
- c[3m, m] does not depend on ν;
- with Rule A: c[3m+1, m] = α_m ν exactly, and c[3m+2, m] = β_m + γ_m ν².

For m = 1 the same counting gives deg_ν c[n, 1] ≤ n − 1.

**What this predicts, and what the computation shows** (`results/series_summary.txt`):

| Harmonic | First order | Coefficient there, cosine form 2c (no ν) | Laurent c = AUDIT.md's z | Next order |
|---|---|---|---|---|
| cos 2φ | t⁶ | −6487/1555200 ≈ −4.17 × 10⁻³ | −6487/3110400 | linear in ν |
| cos 3φ | t⁹ | −21381938959/105921623808000 ≈ −2.02 × 10⁻⁴ | −21381938959/211843247616000 | linear in ν |
| cos 4φ | t¹² | −36714890439535371262123/19643826825035409604608000000 ≈ −1.87 × 10⁻⁶ | half of that (`results/series.json`) | linear in ν |

The cos 4φ value is printed in `results/series_summary.txt`. At t¹³ it is followed by Laurent
c[13, 4] = (40167973655510969803646113/3575176482156444548038656000000) ν, proportional to ν as
Rules A and B require (`results/decompose.log`).

The rule also gives a structural proof of ChatGPT's t⁶ claim, valid for every ν without
interpolation.

**Checks term by term.** `leaf_check.py` builds the labelled jet and checks the lemma and the leaf
counts on every individual term, for n ≤ 9 (`results/leaf_check.log`). An earlier run did the same
for n ≤ 11 (`results/earlier_runs/structure_leaf_check11.log`). Independently, this folder's own
earlier float audit scaled sin z by ε in a float jet. At ε = 0 the harmonics 2 to 4 vanished to
10⁻¹⁶ (`results/earlier_runs/audit_selection_rule.txt`). That earlier audit, the exact computation
and the float computation arrived at this rule independently.

**Status.**
- *The counting step is checked in Lean*, in
  [`SelectionRules.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/SelectionRules.lean):
  `deg_ge_of_beta`, `deg_parity`, `not_before`, `at_first_order`, `order_seven_m_two` and
  `euler_parity`. The file has no `sorry`, and [`Audit.lean`](../../wyrd-mathlib/Audit.lean)
  prints the axioms of all six (Lean was not rebuilt for this write-up). Those theorems take two
  things as hypotheses: the grading (here, L leaves carry ν^{n+2−L}; AUDIT.md writes d + e = n + 2)
  and the fact that every |m| ≥ 2 term has a b leaf (in AUDIT.md's terms, a factor of β, the
  amplitude of sin z).
- *Both hypotheses have only paper proofs, not refereed and not in Lean.* The passive-scalar lemma
  above is P1 of [AUDIT.md](../audit_v2/AUDIT.md) §4.2, which proves it on paper by the same
  argument.
- *Both are backed by exact computation.* With β = 0, AUDIT.md finds max |m| = 1 at every order
  through n = 16 ([`../audit_v2/exact/p1_highorder.py`](../audit_v2/exact/p1_highorder.py)) and
  checks P1 at finite time in a DNS
  ([`../audit_v2/xcheck/p1_finite_time.log`](../audit_v2/xcheck/p1_finite_time.log)). Here, every
  c[n, m] through n = 14 obeys both rules, and both are sharp.

## 5. What produces the t⁶ cos 2φ coefficient

From `python3 decompose.py` (`results/decompose.log`).

All values in this section are Laurent coefficients (the cos 2φ coefficient is twice each).

- **Only one leaf multiset is allowed.** By Rule B, exactly one 8-leaf multiset can contribute:
  {a−², b+, b−, c−², d+²}. It is the forced monomial α²β²γ²δ² of the Lean theorem
  `at_first_order` (Section 4.2), where α, β, γ, δ are AUDIT.md's amplitudes of sin y, sin z,
  cos x and cos(x + y + φ). It reproduces c[6, 2] = −6487/3110400 exactly. All 6 steps in it
  are nonlinear, so c[6, 2] is a purely inviscid quantity. This explains when the term appears,
  its monomial form and why it is ν-free. It does not explain its size.
- **Mostly passive, in this bookkeeping.** In 83.5% of it (−5419/3110400), the phase leaf d is
  only carried along by the phase-free flow. The other 16.5% (−89/259200) is back-reaction, where
  d's vertical velocity itself pushes something. The first cos 3φ and cos 4φ coefficients are 100%
  back-reaction. This split uses the advective form −P[(a·∇)b] and depends on that choice: written
  in rotational form, the same rule gives the same total but a passive share of only −23/28800,
  38.3% (`results/earlier_runs/rot_passive_split.log`). So the split describes the bookkeeping,
  not the flow.
- **Heavy cancellation.** Splitting by which pair of orders (j, 6 − j) is multiplied:
  {0, 6} = −563/622080 (43%), {1, 5} = −97/230400 (20%), {2, 4} = +103/6912 (−715%) and
  {3, 3} = −433/27648 (+751%). By wave vector, the largest pieces are the classes ±(2, 0, ±1),
  +145/31104 each (from {2, 4}), and ±(2, 1, ±1), −1159/124416 each (from {3, 3}). The value is
  spread over 6 |k|² shells and 22 ±k classes
  ([`../audit_v2/exact/mode_decomp_n6m2.log`](../audit_v2/exact/mode_decomp_n6m2.log)). So no
  small set of interactions "explains" the coefficient. It is the small remainder of large
  opposing terms. [AUDIT.md](../audit_v2/AUDIT.md) §4.4 reaches the same pair fractions with its
  own code and adds the shell split; `mode_decomp_n7m2.log` there does the same for t⁷.
- **Viscous correction.** Of the t⁷ cos 2φ coefficient, 96.2% comes from viscosity changing the
  vortex stretching and only 3.8% from direct dissipation of the cos 2φ structure. (Vortex
  stretching is the 3D effect in which the flow stretches its own spinning tubes of fluid, which
  spins them faster and raises the enstrophy.)

## 6. What the jet cannot tell you

**No remainder bound.** The jet gives exact derivatives at t = 0. Nobody has a bound on the error
of a truncated series at a finite time. So no statement about Z at t > 0 follows rigorously from it.
[AUDIT.md](../audit_v2/AUDIT.md) §7.2 says the same.

**Comparison with the package's simulation.** At ν = 1/28 and φ = 0.9710730, the package's 64³
simulation gives Z(1) = 1.68959, Z(1.5) = 2.02514, Z(2) = 2.25528 and Z(4) = 1.95481 (column
`enstrophy` of `periodic_ns_lab_v2/results/refine_p01_N64/diagnostics.csv` in
[`../../inputs/periodic_ns_lab_v2_audit.zip`](../../inputs/periodic_ns_lab_v2_audit.zip)). The float
jet to t⁴⁰ (`python3 long_jet.py`, `results/long_jet.log`) and the earlier comparison
(`results/earlier_runs/structure_growth.log`) show:

| Time | Best the jet does | Error vs simulation |
|---|---|---|
| t = 0.5 | sum through t⁴⁰ | about 10⁻¹⁰ |
| t = 1 | stop at the smallest term (t³³) | about 3 × 10⁻⁵ |
| t = 1.5 | stop at t¹⁴ | about 5 × 10⁻² |
| t = 2 | none: the sum through t¹⁴ is 5.4, through t⁴⁰ about 6 × 10⁷ | no information |
| t = 4 | none: the sum through t¹⁴ is about 3.6 × 10⁴ | no information |

**The series looks divergent for ν > 0** (`results/long_jet.log`, at φ = 0.971). Two standard
tests read the coefficients aₙ of Z(t) = Σ aₙ tⁿ. The *root test* |aₙ|^(−1/n) settles near the
radius of convergence: the series converges for t below it and diverges above it. The *ratio*
|aₙ/aₙ₋₁| settles near the inverse of that radius. If the ratio grows without limit, the radius is zero and the series
diverges at every t > 0.

For every ν > 0 tried, the coefficients alternate in sign from n = 15 on. At ν = 1/10, 1/3 and 1
the ratio grows steadily over n = 20 to 40: from 1.16 to 1.48, from 1.84 to 2.51 and from 3.20 to
4.70. At ν = 1/28 the root test keeps falling, from 1.73 at n = 15 to 1.27 at n = 40. So an earlier
estimate of a convergence radius of 1.6 to 1.9, made from 15 coefficients, does not hold up. At
ν = 0 the root test stays between 1.64 and 1.86. That fits a convergent series, but it also drifts
down (1.86 at n = 15, 1.64 at n = 40), so it does not settle the question. AUDIT.md §7.2 notes
that convergence was not proved; this is numerical evidence on that point, not a proof either way.

Why would viscosity make the series diverge? A heuristic reason comes from Rule A. A convergent
series would also define the flow at negative times, and that is Navier–Stokes run backwards:
anti-diffusion, which should blow up at once. At ν = 0 running backwards is harmless, which fits
the convergent-looking behaviour there. **Open:** this is numerical evidence, not a proof.

**Why the jet cannot explain the simulated optimum.** A function C + B cos φ + A₂ cos 2φ has an
interior maximum in φ only if |B| < 4|A₂|. At t = 1 the jet through t¹⁴ gives the cosine
amplitudes B ≈ 0.162 and A₂ ≈ −0.0022, so 4|A₂|/|B| ≈ 0.05 (`results/series_summary.txt`). The
lab-v2 audit's DNS agrees: at T = 1 it gives the Laurent harmonics |Z₁| = 8.12 × 10⁻² and
|Z₂| = 1.11 × 10⁻³, that is cosine amplitudes 0.162 and 0.0022
([`../audit_v2/xcheck/p1_finite_time.log`](../audit_v2/xcheck/p1_finite_time.log), β = 1 control).

At t = 1, φ = 0 is still a strict local maximum. The audit's tangent DNS gives
d²Z/dφ²(1, 0) = −0.15289 ([`../audit_v2/dns/c3_48.log`](../audit_v2/dns/c3_48.log); the same at
64³ in `c3_64.log`). The jet summed through t¹⁴ gives −0.15239, but its partial sums still move by
about 10⁻³ at that order (−0.15379 through t¹³), so it matches the DNS only to that accuracy.

The simulated sign change of d²Z/dφ²(T, 0) near T ≈ 1.764994 (AUDIT.md §5.4) and the t = 2
optimum φ* ≈ 0.9704 lie beyond the jet's reach. (φ* = 0.971073 on 24³, converging to 0.970364 at
64³; AUDIT.md §5.3.) They are finite-time effects that the jet can neither confirm nor rule out.

## 7. This folder's own audit of the package's other numerical claims

This section is this session's own earlier audit (16 October 2026; evidence in
`results/earlier_runs/`). It is not line (d) of the lab-v2 audit, although it covers the same
ground as [AUDIT.md](../audit_v2/AUDIT.md) §3. It read every file of `periodic_ns_lab_v2` before
running it, then reran its claims and checked them with independent code. The package's code was
not modified. Where AUDIT.md checked a row more finely, the row says so.

| Claim | Verdict | Evidence |
|---|---|---|
| The package's 27 tests pass | **Pass** (27 passed in 12.5 s) | `audit_pytest.txt` |
| d²Z/dφ²(T, 0) changes sign between T = 1.76 and 1.77 on 24³, 32³, 48³ | **Pass**. Crossing at T ≈ 1.76454, 1.76499, 1.76499. Independent finite differences agree. Halving the time step moves it by 2 × 10⁻⁹. These match AUDIT.md's 1.764542, 1.764986, 1.764994 (§5.4). The package's printed 1.764523827, 1.764968015, 1.764976046 are linear interpolants between T = 1.76 and 1.77 (so labelled in its `curvature_crossing.csv`); they run about 1.8 × 10⁻⁵ early, so their 9 decimals overstate the accuracy (AUDIT.md item B3) | `audit_crossing.txt` |
| Ranking: at t = 2, φ = 0.971 beats 0 and 2.16; at t = 4, 2.16 beats 0.971 and 0 | **Pass** on 32³; an independent solver agrees to about 10⁻¹⁵ | `audit_ranking32.log` |
| Newton finds a stationary phase φ* = 0.971073 at 24³ | **Pass** at 24³: dZ/dφ ≈ −5 × 10⁻¹⁰, d²Z/dφ² = −0.1708. Local, not a proven global optimum. φ* depends on the grid: 0.970409 at 32³ and 0.970364 at 64³ (AUDIT.md §5.3). 0.971073 is not stationary at 32³ (dZ/dφ ≈ −1.13 × 10⁻⁴), and the Z(2) shortfall there is about 4 × 10⁻⁸ (AUDIT.md §6 D) | `audit_opt_fd_24.log` |
| Phase reflection Z(T, φ) = Z(T, −φ) and time reversal | **Pass** (defects ≤ 4 × 10⁻¹⁵) | `audit_symmetry.txt` |
| 48³ vs 64³ field differences | **Pass for the full-field L² column**: regenerated 1.38 × 10⁻⁴ at t = 2 and 2.99 × 10⁻⁴ at t = 4, as in the package. This used the package's own code, so it shows reproducibility, not independent accuracy (a fixed-dt rerun at dt = 0.005 gives the same digits, 1.382058 × 10⁻⁴ and 2.993808 × 10⁻⁴, so the L² column is time-step independent; `fixed_dt_L2.log`). The log's relative-Z values are not a check: the run mixes 200 fixed steps at 48³ with 240 adaptive steps at 64³, so 5.4675 × 10⁻⁸ at t = 2 carries the time-step mismatch of AUDIT.md item B4. At fixed dt it is 5.3541 × 10⁻⁸ (AUDIT.md §5.5) | `audit_field48_64.log` |
| Energy never increases | **Pass** in 45 trajectories, but this is automatic for this kind of truncated model; it checks the bookkeeping, not accuracy | `audit_csv_audit.txt` |
| An interior optimum needs a cos 2φ term | **Partly**: the algebra is right but it only constrains the truncated series (Section 6) | — |

All evidence files are in `results/earlier_runs/`.

**Reproducibility gaps found.** The archive leaves out the saved flow states, so some tables need
reruns. No packaged script writes `spatial_comparison.csv` or `curvature_crossing.csv`.
`summarize_v2.py` hard-codes the test counts. The README's test command works only because the
current directory lands on Python's path. (These are items B6, B5 and B1 of AUDIT.md §6. That list
also has items this audit did not find: B2, options that are ignored or hard-coded; B2b, a script
that can overwrite the archived certificate; B7, a garbled sentence in `proof_notes.md`; and B8,
scope and manifest.)

**What kind of statement each claim is.**
- *Exact algebra:* the initial values, both symmetries, the recurrence, the coefficients through
  t⁶ (and here through t¹⁴), the ν-independence of the t⁶ cos 2φ term, the selection rules.
- *Numerical evidence for a truncated (Galerkin) model only:* the curvature sign change, the
  ranking, the optimum, and the grid and time-step comparisons. No error bound links these to the
  true equations.
- *Interpretation:* "the preferred phase changes with observation time", the bifurcation picture,
  and any use of the jet at t ≥ 1.5.

The package states its own limits accurately: no remainder bound, no continuum error bound, and
no claim about regularity or blow-up.

## 8. Context: the Navier–Stokes Millennium Problem in 2026

The Clay problem (Fefferman's official statement) asks whether smooth, finite-energy initial data
for 3D incompressible Navier–Stokes always give solutions that stay smooth for all time. Solvers
may prove one of four statements. Two say smoothness always holds with no external force: (A) on
all of space and (B) on the periodic cube. Two say it can fail, and these allow a smooth external
force: (C) on all of space and (D) on the periodic cube.

On 8 September 2026 OpenAI posted a paper, *Finite time blowup for Navier–Stokes*, with a proof
formalized in the Lean proof checker, of finite-time blow-up for 3D Navier–Stokes driven by a
smooth external force. The paper says this establishes statement (C), and, as its Corollary 10.6,
the periodic statement (D). Scientific American (21 September 2026) describes the official
statement as one that "offers an option called 'C'", in which solutions may use an external force.

On 11 September the Clay Institute said it "shares in the excitement ... as we contemplate the
announcement that the Navier-Stokes problem has apparently been settled", and that its prize
process "is deliberately unhurried". Its Navier–Stokes problem page still lists the problem as
"Active" (re-checked 18 October 2026). This agrees with the project's fact check,
[`../../reports/physics-biology-factcheck.md`](../../reports/physics-biology-factcheck.md) §2.1.
Scientific American reports that the unforced question remains open. It quotes Luis Silvestre:
"The Clay problem is settled, but the main problem for the Navier-Stokes equations is not."

**The logic, in Lean.** A failure of (B) would give (D), but (D), which allows a force, does not
refute (B): `not_B_implies_D` and `D_and_B_consistent` in
[`Quantifiers.lean`](../../wyrd-mathlib/WyrdMathlib/PeriodicNS/Quantifiers.lean). These are
statements about the quantifiers only, not about Navier–Stokes solutions. So a forced blow-up
leaves the unforced periodic question open.

This family is unforced and periodic: the setting of statement (B). **Nothing in this folder bears
on blow-up or global smoothness.** The jet is a statement at t = 0, and the simulations are
finite-dimensional models. Whether unforced flows like these stay smooth forever is **open**. For
a blow-up computation elsewhere in this repository, see [`../../hou-luo-1d/`](../../hou-luo-1d/):
a 1D toy model, not 3D Navier–Stokes. The PeriodicNS context paragraph of
[`../../wyrd-mathlib/README.md`](../../wyrd-mathlib/README.md) covers the same status.

Sources (re-checked 18 October 2026):
- C. L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, Clay Mathematics
  Institute official problem description (2000):
  https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf
- OpenAI, *Finite time blowup for Navier–Stokes* (PDF dated 8 September 2026; Theorem 1.1 and
  Corollary 10.6): https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf ;
  Lean formalization: https://github.com/openai/NavierStokesAndEuler
- Quanta Magazine, 8 September 2026:
  https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/
- Clay Mathematics Institute, announcement of 11 September 2026:
  https://www.claymath.org/news/navier-stokes-announcement/
- Clay Mathematics Institute, Navier–Stokes problem page (status "Active"):
  https://www.claymath.org/millennium/navier-stokes-equation/
- J. Howlett, Scientific American, 21 September 2026:
  https://www.scientificamerican.com/article/did-openai-solve-the-wrong-navier-stokes-problem/

## 9. Credits

- **ChatGPT (OpenAI), `periodic_ns_lab_v2`.** It defined the φ-family and wrote the simulation
  code and sensitivity equations. It ran the phase sweep and the grid refinements, computed the
  exact jet through t⁶, and made the t⁶ claim checked here. It also wrote proof notes that state
  their limits clearly. The package is stored at
  [`../../inputs/periodic_ns_lab_v2_audit.zip`](../../inputs/periodic_ns_lab_v2_audit.zip);
  Sections 2, 6 and 7 describe it.
- **The lab-v2 audit** ([`../audit_v2/`](../audit_v2/), separate Claude agents with their own
  code) supplied the comparison series and the β = 0 checks (Sections 1 and 4), the shell and
  wave-vector splits (Section 5), and the tangent-DNS curvature, the converged φ*, the accurate
  crossings and the fixed-dt relative-Z values (Sections 6 and 7).
- **This folder's code** was written by Claude agents in this project and imports nothing from the
  package. `taylor_exact.py`: the exact computation. `float_check.py`: adapted from the float
  computation's FFT jet. `exact_single_nu.py`: the reconciliation step. `ljet.py`, `decompose.py`
  and `long_jet.py`: the structure analysis. `leaf_check.py` and `show_series.py` were assembled
  from the earlier checking scripts. `compare_audit_v2.py` was added when this folder was moved
  next to `../audit_v2/`.

## 10. Open questions

- A rigorous remainder bound, or another method (for example resummation), that reaches t ≈ 2
  (also open in AUDIT.md §7.2).
- A proof that the series diverges for ν > 0, and of how fast its coefficients grow.
- Rules A and B bound the coefficients. That every allowed coefficient is actually nonzero is
  observed only through t¹⁴. In particular the first cos 5φ coefficient (t¹⁵) has not been
  computed; AUDIT.md §7.5 lists the same gap for |m| ≥ 5.
- Proofs of the grading and of the passive-scalar lemma (P1) in Lean (Section 4.2).
- Whether the first coefficients c[3m, m] (cos 2φ at t⁶, cos 3φ at t⁹, ...) follow a pattern.
