> Historical PR15 record from a9aaf1f, referring to source 77916bb.
> Dates, passes, pending-review language and paths below describe that session.
> Use [README.md](README.md) for current scratch-only commands and
> [the correction review](../../../docs/reconciliation/CORRECTIONS.md) for fresh checks.

# Results: the enstrophy Taylor jet of a phase family of Navier–Stokes flows

This file explains what was computed, what it shows, and what it cannot show.
Every number points to a file in this folder or to a cited source.
"Analogy" marks a comparison that is only a picture. "Open" marks a question nobody has settled.

> Imported historical narrative from source SHA
> `77916bb51ea88ea6e1b2cddd2cd6e9309993383f`; “rerun”, “pass” and source
> timings below describe that source session. Historical PR15 coverage is in IMPORT.md; current checks are in the correction review linked above.
> Lower-order results overlap the existing phase audit. The structural argument
> is a non-refereed mathematical sketch, not a newly certified theorem.

## Summary

ChatGPT's package `periodic_ns_lab_v2` studied a one-parameter family of flows and claimed one
exact result: the enstrophy first depends on cos 2φ at order t⁶, with coefficient −6487/1555200
for every viscosity. Three independent programs here confirm it, two in exact arithmetic and one
in floating point. They also give the full t⁷ term and the cos 2φ part of the t⁸ term, which the
package did not have.

Two rules explain the shape of every coefficient through t¹⁴. One comes from running time
backwards. The other says a cos(mφ) term needs at least 3m nonlinear steps, because without the
sin z part of the flow the phase is just carried along like dye. These rules predict that cos 3φ
first appears at t⁹ and cos 4φ at t¹². The computation confirms both.

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
energy E = 1 and the same enstrophy Z = 5/4 (`results/series.json`, orders 0).

**Quantities.** With ⟨·⟩ the average over the cube:

    E = ½ ⟨|u|²⟩   (energy),     Z = ½ ⟨|curl u|²⟩   (enstrophy: the mean-square vorticity).

**The jet.** "Jet" means the Taylor series in time at t = 0:

    Z(t, φ) = Σₙ Zₙ(φ) tⁿ.

Each Zₙ is computed exactly from the equation by a recurrence. Each is a polynomial in ν with
rational coefficients and a finite Fourier series in φ.

*Analogy:* this is like describing a breath only by the flow, its rate of change, the rate of
change of that, and so on, at the instant it begins. Each number is exact. But a finite list of
them, with no error bound, cannot tell you the tidal volume at end-inspiration.

**Laurent versus cosine coefficients.** The files store Laurent coefficients c[n, m](ν):

    Z(t, φ) = Σₙ Σₘ c[n, m](ν) tⁿ e^{imφ}.

The flow has an exact mirror symmetry, so Z(t, φ) = Z(t, −φ) and c[n, −m] = c[n, m]. In cosine form:

    [tⁿ] Z = c[n, 0] + Σ_{m≥1} 2 c[n, m] cos(mφ).

**So the cosine coefficient is 2c for m ≥ 1.** The package's −6487/1555200 is a cosine coefficient.
The matching Laurent coefficient is −6487/3110400.

Where to look: `results/series.json` holds every c[n, m](ν) for n ≤ 14.
`python3 show_series.py` prints them readably (saved in `results/series_summary.txt`).

## 2. ChatGPT's t⁶ claim, checked three ways

**The claim** (package `RESULTS.md` and `proof_notes.md`). Through t⁵, Z depends on φ only
through a constant and cos φ. At t⁶ the first new harmonic appears, −(6487/1555200) t⁶ cos 2φ,
and this coefficient does not depend on ν.

**Verdict: correct.** Three programs that share no code give the same answer:

| Program | Nonlinear term | Arithmetic | What it gives |
|---|---|---|---|
| `taylor_exact.py` | advective, −P[(u·∇)u] | exact rationals, ν kept as a symbol | c[6, ±2] = −6487/3110400 as a constant polynomial in ν |
| `exact_single_nu.py` | rotational, P[u × curl u] | exact complex rationals, ν a fixed number | same values at every ν tried |
| `float_check.py` | rotational, P[u × curl u] | 64-bit floating point on an FFT grid | agrees with every c[n, m] to rounding |

P is the projection that removes the gradient part of a field; it is how the pressure keeps the
flow incompressible. The two forms of the nonlinear term differ by a gradient, which P removes. So
an error would have to appear in two different formulations and two kinds of arithmetic at once.

Evidence:
- `taylor_exact.py` reproduces `results/series.json`: through n = 8 in `tests/test_jet.py`, and
  through n = 14 in the historical source-session 10.5-minute run that matched in every field except the timings
  (`results/taylor_exact_n14.log`).
- `exact_single_nu.py`: zero exact mismatches at ν = 1/28 (n ≤ 8), −2/3 (n ≤ 7) and 3 (n ≤ 5) in
  this folder (`results/exact_single_nu.log`). An earlier run at 12 further values of ν through
  n = 11 also found zero mismatches (`source-only results/earlier_runs/reconcile_compare_nodes.log`).
- `float_check.py`: worst error 6.5 × 10⁻¹³ relative to each order's largest coefficient, for
  ν = 0, 1/28 and 1/3 and all n ≤ 14 (`results/float_check.log`).
- A fourth route, the leaf decomposition below, also gives −6487/3110400 (`results/decompose.log`).

ChatGPT's own proof of ν-independence evaluated the t⁶ coefficient at 7 exact values of ν and used
the bound "degree in ν ≤ n". That argument is valid (`source-only results/earlier_runs/audit_node_parity.txt`).
Section 4 gives a second proof that needs no interpolation.

## 3. Beyond the package: all of t⁷, and the cos 2φ part of t⁸

All from `results/series.json`, printed in `results/series_summary.txt`.

**The t⁷ term, every harmonic.**

    [t⁷] Z = c[7,0] + 2c[7,1] cos φ + 2c[7,2] cos 2φ

    c[7,0]  = −(8116327869497/13975769808000) ν − (198133/6075) ν³ − (188431/1890) ν⁵ − (74/45) ν⁷
    2c[7,1] = −47271934743389/1677092376960000 + (56494201/16329600) ν² + (6011/420) ν⁴ + (769/315) ν⁶
    2c[7,2] = (207269/7257600) ν

- There is no cos 3φ or cos 4φ at t⁷.
- The cos 2φ term is exactly linear in ν. With no viscosity it vanishes.
- With no viscosity, the whole t⁷ term is −0.0281868 cos φ.
- At ν = 1/28: [t⁷]Z = −0.0222323 − 0.0237508 cos φ + 0.0010200 cos 2φ.

**The t⁸ cos 2φ coefficient.**

    2c[8,2] = 7035947189629/3354184753920000 − (7261/120960) ν²  =  0.00209766 − 0.0600281 ν²

At ν = 1/28 it is 0.0020211. There is no cos 3φ or cos 4φ at t⁸. The full c[8, 0] and c[8, 1]
are in `results/series_summary.txt`.

**One way to read the cos 2φ terms.** The cos 2φ dependence is born at t⁶ with no help from
viscosity. At t⁷ viscosity adds its first correction, with the opposite sign. Together the two
terms equal c₆ t⁶ (1 − λνt) with λ = 621807/90818 ≈ 6.85 (`results/decompose.log`). This looks
like damping at rate λν. That is an interpretation of two Taylor terms, not a decay law. The ν²
part of the t⁸ coefficient (Laurent γ = −7261/241920 ≈ −0.0300) is not what a pure exponential
e^{−λνt} would give (−0.0489).

**A sanity check.** The highest power of ν at each order comes from steps with no nonlinearity,
when the flow simply diffuses like heat. Then Z = ¾ e^{−2νt} + ½ e^{−4νt}, so the top coefficient
of c[n, 0] must be [¾(−2)ⁿ + ½(−4)ⁿ]/n!. That gives −74/45 at n = 7 and 103/126 at n = 8, and
both match (`source-only results/earlier_runs/reconcile_check_claims.log`).

## 4. Two rules that fix the shape of every coefficient

Both rules hold for every c[n, m] with n ≤ 14 (`python3 show_series.py --rules`). They are also
sharp there: every power of ν they allow actually occurs.

### 4.1 Rule A: time-reversal parity

**Statement.** c[n, m](−ν) = (−1)^{n+m} c[n, m](ν). Equivalently, c[n, m] contains only powers νᵖ
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

| Harmonic | First order | Coefficient there (cosine form) | Next order |
|---|---|---|---|
| cos 2φ | t⁶ | −6487/1555200 ≈ −4.17 × 10⁻³, no ν | linear in ν |
| cos 3φ | t⁹ | −21381938959/105921623808000 ≈ −2.02 × 10⁻⁴, no ν | linear in ν |
| cos 4φ | t¹² | ≈ −1.87 × 10⁻⁶ (exact rational in the file), no ν | linear in ν |

The rule also gives a structural proof of ChatGPT's t⁶ claim, valid for every ν without
interpolation.

**Checks term by term.** `leaf_check.py` builds the labelled jet and checks the lemma and the leaf
counts on every individual term, for n ≤ 9 (`results/leaf_check.log`). An earlier run did the same
for n ≤ 11 (`source-only results/earlier_runs/structure_leaf_check11.log`). Independently, the audit scaled
sin z by ε in a float jet. At ε = 0 the harmonics 2 to 4 vanished to 10⁻¹⁶
(`source-only results/earlier_runs/audit_selection_rule.txt`).

**Status.** The proof above is a careful sketch, checked by computation. It has not been refereed.
The audit, the exact computation and the float computation arrived at this rule independently.

## 5. What produces the t⁶ cos 2φ coefficient

From `python3 decompose.py` (`results/decompose.log`).

- **One leaf set does it all.** Exactly one 8-leaf set can contribute:
  {a−², b+, b−, c−², d+²}. It reproduces c[6, 2] = −6487/3110400 exactly. All 6 steps in it are
  nonlinear, so c[6, 2] is a purely inviscid quantity.
- **Mostly passive.** In 83.5% of it (−5419/3110400), the phase leaf d is only carried along by
  the phase-free flow. The other 16.5% (−89/259200) is back-reaction, where d's vertical velocity
  itself pushes something. The first cos 3φ and cos 4φ coefficients are 100% back-reaction.
- **Heavy cancellation.** Splitting by which pair of orders (j, 6 − j) is multiplied:
  {0, 6} gives 43%, {1, 5} gives 20%, {2, 4} gives −715%, and {3, 3} gives +751%. Individual
  products nearly cancel; for example +4.6618 × 10⁻³ against −4.6578 × 10⁻³. So no single
  interaction "explains" the coefficient. It is the small remainder of large opposing terms.
- **Viscous correction.** Of the t⁷ cos 2φ coefficient, 96.2% comes from viscosity changing the
  vortex stretching and only 3.8% from direct dissipation of the cos 2φ structure. (Vortex
  stretching is the 3D effect in which the flow stretches its own spinning tubes of fluid, which
  spins them faster and raises the enstrophy.)

## 6. What the jet cannot tell you

**No remainder bound.** The jet gives exact derivatives at t = 0. Nobody has a bound on the error
of a truncated series at a finite time. So no statement about Z at t > 0 follows rigorously from it.

**Comparison with the package's simulation.** At ν = 1/28 and φ = 0.9710730, the package's 64³
simulation gives Z(1) = 1.68959, Z(1.5) = 2.02514, Z(2) = 2.25528 and Z(4) = 1.95481 (file
`results/refine_p01_N64/diagnostics.csv` inside ChatGPT's package, not included here). The float
jet to t⁴⁰ (`python3 long_jet.py`, `results/long_jet.log`) and the earlier comparison
(`source-only results/earlier_runs/structure_growth.log`) show:

| Time | Best the jet does | Error vs simulation |
|---|---|---|
| t = 0.5 | sum through t⁴⁰ | about 10⁻¹⁰ |
| t = 1 | stop at the smallest term (t³³) | about 3 × 10⁻⁵ |
| t = 1.5 | stop at t¹⁴ | about 5 × 10⁻² |
| t = 2 | none: the sum through t¹⁴ is 5.4, through t⁴⁰ about 6 × 10⁷ | no information |
| t = 4 | none: the sum through t¹⁴ is about 3.6 × 10⁴ | no information |

**Historical finite-order growth observations (no divergence theorem)** (`results/long_jet.log`, at φ = 0.971). Two standard
tests read the coefficients aₙ of Z(t) = Σ aₙ tⁿ. The *root test* |aₙ|^(−1/n) settles near the
radius of convergence: the series converges for t below it and diverges above it. The *ratio* |aₙ/aₙ₋₁| settles near the
inverse of that radius. If the ratio grows without limit, the radius is zero and the series
diverges at every t > 0.

For every ν > 0 tried, the coefficients alternate in sign from n = 15 on. At ν = 1/10, 1/3 and 1
the ratio grows steadily over n = 20 to 40: from 1.16 to 1.48, from 1.84 to 2.51 and from 3.20 to
4.70. At ν = 1/28 the root test keeps falling, from 1.73 at n = 15 to 1.27 at n = 40. So an earlier
estimate of a convergence radius of 1.6 to 1.9, made from 15 coefficients, does not hold up. At
ν = 0 the root test stays between 1.64 and 1.86. That fits a convergent series, but it also drifts
down (1.86 at n = 15, 1.64 at n = 40), so it does not settle the question.

Why would viscosity make the series diverge? A heuristic reason comes from Rule A. A convergent series would also define the flow at negative times, and that is
Navier–Stokes run backwards: anti-diffusion. This heuristic does not establish instantaneous blow-up or divergence. At ν = 0 running
backwards is harmless, which fits the convergent-looking behaviour there. **Open:** this is
numerical evidence, not a proof.

**Why the jet cannot explain the simulated optimum.** A function C + B cos φ + A₂ cos 2φ has an
interior maximum in φ only if |B| < 4|A₂|. At t = 1 the jet through t¹⁴ gives B ≈ 0.162 and
A₂ ≈ −0.0022, so 4|A₂|/|B| ≈ 0.05 (`results/series_summary.txt`). There φ = 0 is still a strict
local maximum (d²Z/dφ² ≈ −0.152). The simulated sign change of d²Z/dφ² near T = 1.765 and the
optimum φ ≈ 0.971 at t = 2 lie beyond the jet's reach. They are finite-time effects that the jet
can neither confirm nor rule out.

## 7. Audit of the package's other numerical claims

An earlier audit read every file of `periodic_ns_lab_v2` before running it, then reran its claims
and checked them with independent code. The package's code was not modified.

| Claim | Verdict | Evidence |
|---|---|---|
| The package's 27 tests pass | **Pass** (27 passed in 12.5 s) | `audit_pytest.txt` |
| d²Z/dφ²(T, 0) changes sign between T = 1.76 and 1.77 on 24³, 32³, 48³ | **Pass**. Crossing at T ≈ 1.76454, 1.76499, 1.76499. Independent finite differences agree. Halving the time step moves it by 2 × 10⁻⁹ | `audit_crossing.txt` |
| Ranking: at t = 2, φ = 0.971 beats 0 and 2.16; at t = 4, 2.16 beats 0.971 and 0 | **Pass** on 32³; an independent solver agrees to about 10⁻¹⁵ | `audit_ranking32.log` |
| Newton finds a stationary phase φ* = 0.971073 at 24³ | **Pass**: dZ/dφ ≈ −5 × 10⁻¹⁰, d²Z/dφ² = −0.1708. Local, not a proven global optimum | `audit_opt_fd_24.log` |
| Phase reflection Z(T, φ) = Z(T, −φ) and time reversal | **Pass** (defects ≤ 4 × 10⁻¹⁵) | `audit_symmetry.txt` |
| 48³ vs 64³ field differences | **Pass**: regenerated 1.38 × 10⁻⁴ at t = 2 and 2.99 × 10⁻⁴ at t = 4, as in the package | `audit_field48_64.log` |
| Energy never increases | **Pass** in 45 trajectories, but this is automatic for this kind of truncated model; it checks the bookkeeping, not accuracy | `audit_csv_audit.txt` |
| An interior optimum needs a cos 2φ term | **Partly**: the algebra is right but it only constrains the truncated series (Section 6) | — |

Earlier evidence is retained in the pinned source, not recopied here: [source earlier_runs](https://github.com/rafaellemus92/NICU-Math/blob/77916bb51ea88ea6e1b2cddd2cd6e9309993383f/navier-stokes-jet/results/earlier_runs).

**Reproducibility gaps found.** The archive leaves out the saved flow states, so some tables need
reruns. No packaged script writes `spatial_comparison.csv` or `curvature_crossing.csv`.
`summarize_v2.py` hard-codes the test counts. The README's test command works only because the
current directory lands on Python's path.

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

## 8. Scope of this import

This family is unforced and periodic. Nothing in this folder establishes blow-up
or global smoothness. The source's September-2026 publication/announcement
claims are unverified and are not adopted in this import; consult the pinned
source for that historical text. This import makes no current publication-status
claim. No rigorous Taylor remainder or finite-time optimum is established.
Finite root/ratio sequences cannot establish convergence or divergence.

## 9. Credits

- **ChatGPT (OpenAI), `periodic_ns_lab_v2`.** It defined the φ-family and wrote the simulation
  code and sensitivity equations. It ran the phase sweep and the grid refinements, computed the
  exact jet through t⁶, and made the t⁶ claim checked here. It also wrote proof notes that state
  their limits clearly. The package is not included in this folder; Sections 2, 6 and 7 describe it.
- **This folder's code** was written by Claude agents in this project and imports nothing from the
  package. `taylor_exact.py`: the exact computation. `float_check.py`: adapted from the float
  computation's FFT jet. `exact_single_nu.py`: the reconciliation step. `ljet.py`, `decompose.py`
  and `long_jet.py`: the structure analysis. `leaf_check.py` and `show_series.py` were assembled
  from the earlier checking scripts.

## 10. Open questions

- A rigorous remainder bound, or another method (for example resummation), that reaches t ≈ 2.
- A proof that the series diverges for ν > 0, and of how fast its coefficients grow.
- Rules A and B bound the coefficients. That every allowed coefficient is actually nonzero is
  observed only through t¹⁴.
- Whether the first coefficients c[3m, m] (cos 2φ at t⁶, cos 3φ at t⁹, ...) follow a pattern.
