# Audit of `periodic_ns_lab_v2`

Prepared by Claude, 2026-10-16. Written for the user and for ChatGPT, which wrote the package.

**Bottom line.**

* We found no mathematical error and no false numerical claim in the package.
* The central identity is confirmed exactly, with ν kept symbolic:

      [t^6 cos 2φ] Z = −6487/1555200, for every ν.

* It has a structural explanation that predicts the next orders correctly. That explanation is proved at the level of the Taylor recurrence (section 4).
* Every numerical headline was reproduced by a solver written from scratch, to about 8 decimals.
* Three printed quantities carry more digits than their methods support:
  * the 9-decimal C1 values;
  * the 9-decimal "linear crossing estimates";
  * the 5-significant-digit relative-Z entries for 48³ at T = 2.
* There is one reproducibility bug: bare `pytest -q` fails to collect.
* There are a few provenance defects.
* Nothing in the package, or in our work, gives the following:
  * a continuum (cutoff-uniform) estimate;
  * a remainder bound for the Taylor jet at t = 2 or t = 4;
  * a global optimality certificate in φ.

---

## 1. What was audited and how

**Object.** This is the uploaded package `periodic_ns_lab_v2`. All 254 `MANIFEST_SHA256.txt` entries verify. We followed the audit brief in `CLAUDE_HANDOFF.md` (items 1–9) and checked the headline claims of `RESULTS.md`.

**Notation.** We use a generalised initial field

    u_0 = (α sin y, β sin z, γ cos x − δ cos(x+y+φ))   on [0,2π]^3.

The package is the case α = β = γ = δ = 1.

* Averages ⟨·⟩ are normalised volume averages. E = ½⟨|u|²⟩, Z = ½⟨|ω|²⟩, D = ⟨|∇ω|²⟩ and S = ⟨ω·(ω·∇)u⟩.
* z_{n,m} is the coefficient of e^{imφ} in [t^n]Z. Since z_{n,−m} = z_{n,m}, the coefficient of cos mφ is 2 z_{n,m}.
* ν = 1/28 unless stated otherwise.

**Four independent lines plus a cross-check.** Each line was run by a separate agent.

| Line | What it is | Package access |
|---|---|---|
| (a) Exact series | Written from scratch. Uses Python `fractions` and numpy. Taylor recurrence with **symbolic ν**, φ carried as a Fourier label, general (α,β,γ,δ). Includes a second exact implementation with a different structure (`phase_lemma_check.py`) and a float DNS check. | Did not open any package file |
| (b) Float series | Written from scratch in numpy. FFT Taylor recurrence with complex parameters. Degree separation in ν, α, β, γ, δ by DFTs on circles, to n = 12. Double and 80-bit long double. | Did not open any package file |
| (c) DNS | Written from scratch in numpy. Pseudo-spectral Fourier–Galerkin solver with fixed-dt RK4, N = 24…96, plus tangent (first and second φ-variation) equations. | Did not open any package file |
| (d) Code audit | Read the package code. Ran the 27 tests. Re-ran all production runs sequentially. Wrote its own checks: a formal-ν exact jet, a sympy symmetry check, and generic checks of the variation equations. | Read and ran the package |
| (x) Cross-check | Compared (a)–(d) with each other and with the package outputs. Tried to refute the structural explanation. Ran new tests: P1 at finite time, the N = 64 optimum, spatial relative-Z, and high-mode t² values. | Read reports and package outputs |

**Independence rules.**

* Lines (a)–(c) never read package code or outputs. Each wrote everything itself, and none touched git or the `sgrounds` repository.
* Line (d) is the only one that executed package code.
* Consequence: a number reproduced only by (d) shows that the package is **reproducible**, not that it is **accurate**. For example, the "bitwise" reruns re-used the package's own integrator. Where a claim rests on (d) alone, the verdict table says so.

---

## 2. Claude's own repository, and how it differs

**Location.** github.com/rafaellemus92/sgrounds, branch `claude/new-session-sbrl43`, folder `experiments/wyrd-mathlib`.

The repository's default branch is an unrelated web app; the proofs live on this branch.

**Contents.** Lean 4 + Mathlib formal proofs. These are static theorems about given fields; they do not cover the NS evolution.

* **Proved (in `PeriodicNS/`).** For v = (sin y, sin z, cos x − cos(x+y)), with derivatives taken by Lean `deriv` and averages taken as genuine integrals:
  * E = 1, Z = 5/4, D = ⟨|∇ω|²⟩ = 7/2, S = 1/4.
  * The fields ±A v share E, Z, D and every Fourier magnitude, but S = ±A³/4. This is in `no_closure` and `no_spectral_closure`.
  * A Galerkin cutoff bound.
  * A variable-coefficient Gronwall lemma.
  * The quantifier logic of the Clay problem statements B and D.
* **In progress.**
  * The phase family u_φ has S = cos(φ)/4, with E, Z and D independent of φ.
  * At ν = 1/28 the initial enstrophy growth is zero at φ = π/3.
  * −v is a translate of u_π.
* **Not formalised.**
  * The NS evolution itself.
  * The enstrophy balance dZ/dt = S − νD.
  * Local existence.

  Therefore **no time-series or simulation claim is a Lean theorem**.
* **Earlier (v1) FFT re-derivations, all to 7e-16:**
  * S(0) = cos(φ)/4;
  * Z''(0) = 5/4 − (5/2)ν cos φ + 11ν²;
  * high-shell values 7/48 and 9/16;
  * new-mode values 11/24 and 19/16.

**Shared and different elements.**

| Aspect | Package | Claude repository | Relation |
|---|---|---|---|
| Equation | Unforced 3D incompressible NS. Rotational form with Leray projection. | NS not formalised. Only static functionals E, Z, D, S of given fields. | Lean covers t = 0 functionals only |
| Domain | [0,2π]³, periodic | Same | Same |
| Normalisation | `norm='forward'`, volume averages, Z = ½⟨|ω|²⟩ | Integrals divided by volume | Same values: E = 1, Z = 5/4, D = 7/2, S = cos φ/4 |
| Initial data | u_φ = (sin y, sin z, cos x − cos(x+y+φ)) | v = u_0; family u_φ in progress | v = u_0. Package test 24 checks numerically that −u_0 and u_π have identical diagnostics. The Lean work states this as a translation identity. |
| Forcing | None | None | Same |
| Viscosity | 1/28, hard-coded | 1/28 where a viscosity is used | Same. νD = 1/8, so dZ/dt(0) = cos φ/4 − 1/8 in both. This matches the package's "Initial Z′" column (0.125, 0.016103519, −0.263892558). |
| Cutoff | Cube max\|k_i\| ≤ ⌊(N−1)/3⌋ | An abstract Galerkin cutoff bound | No shared discretisation |
| D | ⟨\|∇ω\|²⟩ = 7/2 (package test 10) | 7/2 | Same. The DNS line reports ½⟨\|∇ω\|²⟩ = 1.75, which is the same quantity halved. |
| Outputs | Time series, φ-sensitivities, Taylor jets | Theorems at t = 0 | Complementary |

**Conclusion.** The two bodies of work agree on every quantity they share, which is all at t = 0. There is no code to merge, and nothing was reconciled silently.

---

## 3. Verdict table

**Kinds of evidence:**

* **X**: exact algebra or proof.
* **N-ind**: numerical, from independent code.
* **N-pkg**: numerical, from the package's own code only.
* **R**: code reading.

### 3a. `CLAUDE_HANDOFF.md` items 1–9

| # | Claim / task | Verdict | Kind | Basis |
|---|---|---|---|---|
| 1 | `ns_solver.py` is unforced 3D periodic NS with strict cubic dealiasing and ν = 1/28; normalisation, projection, reality, zero mean and shell-flux sign are all correct | **PASS** | R, N-ind | **Equation (read in full).** The right-hand side is `P_K P(u×curl u) − ν\|k\|² u` with no forcing. ν = 1/28 is hard-coded in the production paths and appears in all 84 metadata files. **Dealiasing.** The cutoff K = ⌊(N−1)/3⌋ gives 3K < N. The N = 24 nonlinearity equals the alias-free N = 64 evaluation to 2.8e-17. As a counterexample showing the strict inequality matters, K = 8 at N = 24 gives an aliasing error of 3.6e-2. **Reality and divergence.** Hermitian defect 1.6e-16 and \|k·u\| = 4.9e-18. **Shell flux.** The budget closes to 1.3e-9, and Π > 0 means forward transfer. **Independent DNS.** Validated against four exact decaying solutions (errors 1.4e-15 to 3.2e-13). |
| 2 | Run the 27 tests; independently check the velocity, tangent and second-variation equations | **PASS** (with a defect) | N-pkg, X, N-ind | **Tests.** `python -m pytest -v` passes all 27. **Defect.** Bare `pytest -q` fails collection (section 6, item B1). **What the tests cover.** Sensitivity tests 1–4 and 7 run only at 16³ and T ≤ 0.2. **Generic check.** For random independent (u, w, r), the variation right-hand sides and the dZ, d²Z formulas are exact to about 1e-15 (5-point stencils on a degree-4 polynomial). **Production times.** Richardson finite differences of the plain solver at 24³ give d²Z(1.76) = −0.0020361, d²Z(1.77) = +0.0024648 and d²Z(φ\*, T = 2) = −0.1707845, all equal to the variational values. **Independent tangent solver.** Line (c) reproduces the curvature crossing (section 5.4). |
| 3 | Reproduce the sweep and the 32³/48³/64³ runs; test the rankings at t = 2 and t = 4; compare whole Fourier fields | **PASS** for rankings; **PARTIAL** for field comparison | N-ind, N-pkg | **Rankings.** Hold at N = 24, 32, 48 and 64 with margins ≥ 0.025 (t = 2) and ≥ 0.10 (t = 4), about 10³–10⁶ times every grid or integrator difference. **Re-runs.** All 33 sweep, 3 time-refinement and 9 refinement runs reproduce bitwise with the package code. **Full-field L² column.** Reproduced only with the package code. **Relative-Z column.** Independently reproduced for every 32³ row and every T = 4 row. The 48³, T = 2 rows differ by 1–2.5% (section 5.5). **Selection effects (acknowledged in `RESULTS.md`).** 0.971073 was optimised at 24³ only, and 2.159845 = 22π/32 is a sweep grid point. |
| 4 | Local optimiser at 24³ and 32³: stationary point versus global optimum | **PASS** (local stationary maximum); global optimum **UNPROVEN** | N-ind | **Reproduced** to about 1e-8 in φ by independent tangent-Newton and golden-section searches. Z_φφ ≈ −0.170 at every N. **New results.** N = 48 gives φ\* = 0.9703653579; N = 64 gives φ\* = 0.9703643925. φ\* converges to about 0.970364. **Global optimality.** No global certificate exists, and the package does not claim one. |
| 5 | Phase-reflection symmetry; sign change of ∂²_φ Z(T,0) between T = 1.76 and 1.77 | **PASS** | X, N-ind | **Symmetry.** F[u](x) = R u(Rx+b) with R = diag(−1,−1,1) and b = (0,0,π) maps u_φ to u_{−φ}. This is checked with sympy for general amplitudes, and the cubic cutoff and RK4 commute with it exactly. **Numerical check.** Z(T,+0.5) − Z(T,−0.5) is at most 8.9e-16 over [0,2], and the fields map to within 2.8e-15. **Sign change.** Holds at N = 24–64, dt ∈ {0.01, 0.005, 0.0025} and h ∈ {0.04, 0.02, 0.01}, by both the tangent method and finite differences. The 9-decimal crossing values are **PARTIAL** (section 6, item B3). |
| 6 | Taylor recurrence; [t⁶ cos 2φ]Z = −6487/1555200 for every ν; only m ∈ {0,±1} at orders 0–5 | **PASS** | X | **Recurrence.** Re-derived independently, with the pressure fully accounted for by P. **Value.** Obtained exactly, with ν symbolic, by line (a) (two exact implementations) and by line (d)'s formal-ν code. Line (b) confirms it in long double to a relative 5e-18. **Package jets.** Equal by Fraction equality, with 0 mismatches over orders 0–6 at all 7 nodes. **Orders 0–5.** Contain only m ∈ {0,±1}, as exact polynomials in ν. **Structural reason.** Section 4. |
| 7 | Degree ≤ 6 in ν is established before the 7-node identity test; factor of 2 between Laurent and cosine coefficients | **PASS** | X, R | **Degree lemma.** `proof_notes` §4 states the induction deg_ν U_n ≤ n before the test, and the induction is correct. **Nodes.** The 7 nodes are exact Fractions. **No interpolation needed.** Symbolic-ν computation reaches the same result without any. **Factor of 2.** Laurent −6487/3110400 gives the cosine coefficient −6487/1555200. **Sharper bound.** deg_ν z_{6,2} = 0 follows from counting (section 4). |
| 8 | Does a small, explicit set of mode interactions account for the coefficient? | **PARTIAL** (answered) | X | **No.** z_{6,2} is a near-cancellation: pair {2,4} contributes +103/6912 and pair {3,3} contributes −433/27648. Six \|k\|² shells and more than a dozen wave-vector classes contribute (section 4.4). **What is explained.** The full PDE is kept, and the structural argument explains when the term appears, its monomial form and its ν-independence. It does not explain the numerical value. |
| 9 | State the additional estimate that would turn a finite-mode experiment into a continuum argument | **UNPROVEN** (none exists; the package correctly claims none) | Logic | The needed estimates are stated precisely in section 7. |

### 3b. `RESULTS.md` headline claims

| Claim | Verdict | Kind | Basis |
|---|---|---|---|
| 45 velocity trajectories (33 + 9 + 3) and 10 sensitivity integrations | **PASS** | N-pkg | Counted in the logs: 10 = 4 (24³ optimiser) + 3 (32³ optimiser) + 3 (curvature). All 45 trajectories were re-run. |
| 27 tests passed | **PASS** | N-pkg | True via `python -m pytest`. The number 27 is hard-coded in `summarize_v2.py` (item B5). |
| 21 independent Taylor checks, maximum difference 6.7e-16 | **PASS** | N-pkg | The re-run gives 21 checks with maximum difference 5.55e-16 (the archive has 6.66e-16). The literal is hard-coded. |
| Seven exact rational viscosity nodes establish the polynomial identity | **PASS** | X | See item 7. The re-run is identical apart from elapsed time. |
| All main runs: ν = 1/28, no forcing, E = 1, Z = 1.25 | **PASS** | R, N-ind | All 84 metadata files and the code agree. E(0) and Z(0) are exact. |
| Initial Z′ column: 0.125, 0.016103519, −0.263892558 | **PASS** | X, N-ind | Equals cos φ/4 − 1/8 to within 1.5e-16. |
| 64³ Z(2), Z(4) and sampled peaks, to 9 decimals | **PARTIAL** | N-ind | **Agreement.** Independent fixed-dt RK4 agrees to 1.3e-9–4.4e-9 at T = 2 and 4, and to 2e-9–7e-9 at the peaks. **Source of the gap.** The package's 64³ runs used CFL-adaptive RK4 (455/459/470 steps; dt between 0.0010 and 0.0098 on [0,2]). Over [0,4], max\|ΔZ\| reaches 1.4e-8. With the same fixed dt the two codes agree to about 1e-12. **Conclusion.** The 9th decimal is integrator-dependent. |
| Peak times 2.20, 2.55, 2.90 | **PASS** | N-ind | Same at every N ≥ 24. Refined peaks are given in section 5.1. |
| Ranking: 0.971 best at t = 2, 2.16 best at t = 4 | **PASS** | N-ind | Holds at N = 24, 32, 48 and 64. |
| All three candidates have dZ/dt < 0 at t = 4 | **PASS** | N-ind | No earlier report had tested this. A 4th-order finite difference on the DNS at N = 64 gives −0.422549, −0.464033 and −0.427863, matching the package CSV. |
| Local phase optimisation table (24³, 32³) | **PASS** | N-ind | See item 4 and section 5.3. Correctly labelled as local and not certified global. |
| Curvature at φ = 0 changes sign between 1.76 and 1.77 on 24³, 32³ and 48³ | **PASS** | N-ind | See item 5. Also holds at 64³. |
| Linear crossing estimates 1.764523827, 1.764968015, 1.764976046 | **PARTIAL** | N-ind | Correct as linear interpolants, which is how they are labelled. The true crossings are about 1.8e-5 later, so 9 decimals overstate the accuracy (item B3). |
| Spatial comparison table against 64³ | **PARTIAL** | N-ind, N-pkg | **Relative Z.** All 32³ rows and all T = 4 rows reproduce independently to 0.05% or better. The 48³, T = 2 rows differ by 1–2.5% because of time-step contamination (item B4). **Full-field L².** Reproduced with the package code only. |
| Temporal comparison table at 32³ | **PASS** | N-ind, N-pkg | **dt = 0.005 row.** Reproduced independently: 2.255288136558, to about 1e-12. **Other rows.** Reproduced with the package code. |
| Order-6 exact result: −(6487/1555200) t⁶ cos 2φ, ν-independent, only m ∈ {0,±1} at orders 0–5 | **PASS** | X | See item 6 and section 4. |
| "Local derivative identity; no remainder estimate permits t = 2 or t = 4" | **PASS** (statement accurate) | Logic | No remainder bound exists anywhere (section 7). |
| "No estimate uniform in the Fourier cutoff has been established" | **PASS** (statement accurate) | Logic | See section 7. |
| Phase symmetry Z(T,φ) = Z(T,−φ) (`proof_notes` §1) | **PASS** | X, N-ind | See item 5. Uniqueness of the smooth solution is needed, and the notes state this. |
| Galerkin ODE cannot blow up at fixed cutoff (`proof_notes` §6) | **PASS** | X | Standard energy argument. The ⟨u, N(u)⟩ = 0 checks pass (below 7e-17 in the DNS line; package test 14). |
| Package test: high-mode t² energy 7/48 and enstrophy 9/16 | **PASS** | N-ind | An independent numpy evaluation of P[−(U₀·∇)U₀] on \|k\|² > 2 gives exactly these values at three phases. |

---

## 4. The sixth-order coefficient

### 4.1 Independent exact confirmation

* **Value.** z_{6,±2} = −6487/3110400 exactly, so the cos 2φ coefficient of [t⁶]Z is **−6487/1555200 = −4.17116769547325e-3**.
  * The symbolic-ν polynomial is this constant alone: the coefficients of ν¹ through ν⁶ are exactly 0.
  * There is no sin 2φ term, because Z is even in φ.
* **Implementations that agree.**
  * Line (a) `nsseries.py`: symbolic ν, uses the phase lemma, general amplitudes.
  * Line (a) `phase_lemma_check.py`: generic Gaussian rationals, conservative nonlinearity, rational ν. Every U_n mode and every Z_n coefficient matches through n = 7.
  * Line (d) `exact_nu_poly.py`: formal ν, rotational form.
  * The package's own `exact_time_series.py`, re-run.
  * Line (b) in long double: −2.0855838477366255087e-3 against the exact −2.0855838477366255144e-3. A continued-fraction fit returns −6487/3110400.
* **Checks built into the exact line.**
  * Every mode of every U_n is divergence-free.
  * The k = 0 advection vanishes for each φ-harmonic.
  * The energy identity (n+1)E_{n+1} = −2ν Z_n holds as an identity of ν-polynomials.
* **Low orders** (unit amplitudes; z_{n,1} is half the cos φ coefficient):

| n | z_{n,0} | z_{n,1} | \|m\| ≥ 2 |
|---|---|---|---|
| 0 | 5/4 | 0 | — |
| 1 | −7/2 ν | 1/8 | — |
| 2 | 5/8 + 11/2 ν² | −5/8 ν | — |
| 3 | −145/36 ν − 19/3 ν³ | −1/24 + 17/12 ν² | — |
| 4 | −3/80 + 41/3 ν² + 35/6 ν⁴ | 1/16 ν − 49/24 ν³ | — |
| 5 | −25289/48600 ν − 2963/90 ν³ − 67/15 ν⁵ | 2869/86400 + 239/480 ν² + 43/20 ν⁴ | — |
| 6 | 8500748131/210161952000 + 145723/23328 ν² + 3767/60 ν⁴ + 131/45 ν⁶ | −908723/3110400 ν − 769/288 ν³ − 107/60 ν⁵ | z_{6,2} = −6487/3110400 |
| 7 | −8116327869497/13975769808000 ν − 198133/6075 ν³ − 188431/1890 ν⁵ − 74/45 ν⁷ | −47271934743389/3354184753920000 + 56494201/32659200 ν² + 6011/840 ν⁴ + 769/630 ν⁶ | z_{7,2} = (207269/14515200) ν |

* **Consistency with t = 0 values.** [t²]Z = 5/8 − (5/4)ν cos φ + (11/2)ν². This is Z''(0)/2, consistent with v1 and with package tests 21–22: Z''(0) = 921/784 at φ = 0 and 1061/784 at φ = π, for ν = 1/28.
* **Float agreement.** Over all n ≤ 12, all m, ν ∈ {0, 1/28, 1/7} and both float discretisations, the exact and float tables agree to at most 2.1e-15 absolute.
* **DNS agreement.** A from-scratch DNS matches the order-10 series to 7e-15 at t = 0.05 and 4e-14 at t = 0.1, at both ν = 0 and ν = 1/28.

### 4.2 Structural explanation

We kept the full PDE: no interactions were deleted. Write Z as a polynomial in the amplitudes α, β, γ, δ, with the δ factors carrying e^{±iφ}. For a monomial in [t^n]Z let:

* d = its total amplitude degree;
* e = its power of ν;
* m = its φ-harmonic.

**P1: β = 0 gives a 2D-3C linear structure.**

* **Statement.** If β = 0, then at every order:
  * every mode has k_z = 0;
  * u₂ ≡ 0;
  * u₁ = α e^{−νt} sin y exactly;
  * u₃ is a passive scalar carried by that shear.
* **Proof.**
  * At k_z = 0 the Leray symbol splits as P_2D ⊕ 1. The third component passes through untouched, and nothing leaks between u₃ and the in-plane components.
  * The in-plane shear closes on itself, because d_x(c sin y) = 0.
  * The u₃ recurrence is linear and preserves k_x.
* **Consequence for u₃.** u₃ is linear in (γ, δe^{iφ}, δe^{−iφ}), and the (k_x, m) labels stay locked to {(1,0), (1,1), (−1,0), (−1,−1)}.
* **Consequence for Z and E.** Parseval pairs (k, m₁) with (−k, m₂), and ω₃ = −∂_y u₁ has no cross terms with ω₁ and ω₂. So Z and E contain only m ∈ {−1, 0, 1}.
* **Conclusion.** With β = 0 there is no cos 2φ term at any order.

**P2: counting.**

* **Per-axis wave-vector balance.** A zero spatial mean requires the factors to balance along each axis:
  * x: g₊ − g₋ + d₊ − d₋ = 0;
  * y: a₊ − a₋ + d₊ − d₋ = 0;
  * z: b₊ = b₋;
  * and the harmonic is m = d₊ − d₋.

  Hence #α, #γ and #δ are each ≥ \|m\| and each has the parity of m, and #β is even.
* **Combining with P1.** For \|m\| ≥ 2, #β ≥ 2, so the amplitude degree is **d ≥ 3\|m\| + 2**.
* **Grading.** Each term satisfies **d + e = n + 2**. This follows from n = (d−1) + e in U_n, or equivalently from the scaling u → λu(x, λt), ν → λν.
* **Parity.** d ≡ m (mod 2), so e ≡ n − m (mod 2).
* **Consequences:**
  1. A \|m\| ≥ 2 harmonic cannot appear before **n = 3\|m\|**. At that order e = 0, so the coefficient is **ν-independent**, and it is forced to be a multiple of α^{\|m\|} β² γ^{\|m\|} δ^{\|m\|}. For m = 2 at n = 6, this is −6487/3110400 · α²β²γ²δ².
  2. At **n = 7, m = 2**, parity forces e = 1 and d = 8. So the coefficient is exactly **C ν α²β²γ²δ²: proportional to ν, and zero for Euler**.
  3. **cos 3φ cannot appear before n = 9**, and at n = 9 it is ν-independent and ∝ α³β²γ³δ³. cos 4φ cannot appear before n = 12.
  4. For Euler, z_{n,m} = 0 unless n ≡ m (mod 2).

### 4.3 What the computations showed

| Prediction | Result | Source |
|---|---|---|
| β = 0 gives no \|m\| ≥ 2 harmonic | Exact symbolic-ν runs to **n = 16** (two amplitude sets) and to n = 10 (three sets) give max\|m\| = 1. Float runs to n = 12 sit at the 9e-16 noise floor. The field-level mechanism (k_z = 0, u₂ = 0, u₁ = α(−ν)ⁿ/n! sin y, k_x locking, linearity in γ and δ) is confirmed exactly. **New finite-time DNS** (N = 24, T = 1, 2, 4): the \|m\| = 2–4 harmonics of Z and E are at most 1.9e-15. In the β = 1 control, \|Z₂\| = 1.1e-3, 2.3e-2 and 3.2e-2. | (a), (b), (x) |
| Grading d + e = n + 2 | Exact: scaling the amplitudes by λ ∈ {2, −3/5} gives λ^{n+2−e} for every n ≤ 9. Float: λ-homogeneity holds to 6e-15. | (a), (b) |
| Selection rules | Zero violations: exact univariate interpolation for n ≤ 9, float per-variable DFTs for n ≤ 12. For m = 1, β⁰ terms do occur, as P2 allows. | (a), (b) |
| n = 6, m = 2 is ν-free and equals −6487/3110400 · α²β²γ²δ² | Exact at amplitudes (2,3,5,7): −317863/3456 = 44100 × unit value. Exact at (1,2,1,3): 36 × unit value. Exact at (½, −⅔, ¾, 5/7). Float: random signed tuples deviate by at most 6e-14 relative. | (a), (b) |
| [t⁷] m = 2 is C ν with C ≠ 0 | **z_{7,2} = (207269/14515200) ν exactly**, so the cos 2φ coefficient of [t⁷]Z is (207269/7257600) ν. The ν⁰ term is zero (long double: −2.2e-21). **DNS check:** the e^{2iφ} harmonic differs between ν = 0 and ν = 1/28 by 5.016e-11 at t = 0.1. The series gives 5.015e-11 including higher orders, and 5.10e-11 from the t⁷ term alone. | (a), (b), (x) |
| First cos 3φ at n = 9 | **z_{9,3} = −21381938959/211843247616000**, ν-independent, with monomial α³β²γ³δ³. Long double agrees to 7.5e-18 relative. Next order: z_{10,3} = (22945853676929/20125108523520000) ν. | (a), (b) |
| First cos 4φ at n = 12 | z_{12,4} = −36714890439535371262123/39287653650070819209216000000, ν-independent, with monomial α⁴β²γ⁴δ⁴. \|m\| ≥ 5 is absent through n = 12. | (a), (b) |
| At finite time, the m = 2 harmonic is even in β and O(β²) | At Z(T = 1), ν = 1/28, c₂/β² = −1.1909e-3, −1.2035e-3, −1.2067e-3 and −1.2075e-3 for β = 0.4, 0.2, 0.1, 0.05. β = −0.1 gives the same value as +0.1. | (x) |

For reference, the next even order is [t⁸] cos 2φ = 7035947189629/3354184753920000 − (7261/120960) ν². Its ν⁰ part is not a single monomial, as expected.

**Status.**

| Statement | Status |
|---|---|
| P1 at the level of the Taylor recurrence, for all (α, γ, δ, ν) | **Proved** (analytic induction re-derived by the cross-check) |
| P1 at the solution level (finite T) | **Verified numerically** to 2e-15 through T = 4. A proof would follow the same lines, since the k_z = 0 subspace is invariant and the u₃ equation is linear, but we have not written it out. |
| P2: grading, selection rules, "no \|m\| harmonic before n = 3\|m\|", e = 0 and the forced monomial at n = 3\|m\| | **Proved**, given P1 |
| [t⁷] m = 2 coefficient is ∝ ν and zero for Euler | Form **proved**. Constant **computed exactly**: 207269/14515200. |
| Leading coefficient at n = 3\|m\| is nonzero | **Computed** for \|m\| = 2, 3, 4. **Unproven** for \|m\| ≥ 5. |

**Not claimed.** The structure says nothing about the size of these coefficients at finite t. As `proof_notes` §5 also says, the order-6 term alone does not explain the finite-time pitchfork at T ≈ 1.765.

### 4.4 Mode decomposition of z_{6,2} (item 8)

Every partial sum below is independent of ν on its own, not just the total.

| Unordered pair {j, 6−j} | Contribution |
|---|---|
| {0,6} | −563/622080 |
| {1,5} | −97/230400 |
| {2,4} | **+103/6912** (+0.01490) |
| {3,3} | **−433/27648** (−0.01566) |
| Total | −6487/3110400 (−0.00209) |

| \|k\|² shell | 1 | 2 | 3 | 5 | 6 | 9 |
|---|---|---|---|---|---|---|
| Contribution | +10439/6220800 | −5977/1555200 | +563/414720 | +205/20736 | −353/20736 | +3/512 |

Shells 4, 8 and ≥ 10 contribute nothing.

* **Largest wave-vector classes.** ±(2,1,±1) contributes −1159/124416 for each sign of k_z, from the (3,3) pair. ±(2,0,±1) contributes +145/31104 each, from (2,4). ±(2,2,±1) contributes +3/1024 each.
* **Where the contributions live.** Every contributing wave vector has \|k_z\| ≤ 1, which reflects the single pair of β factors. The φ-label splits that occur are (0,2), (1,1) and (2,0).
* **Order 7.** The pair split of z_{7,2} is {0,7} = 232607/43545600 ν, {1,6} = 4579/777600 ν, {2,5} = −66823/691200 ν and {3,4} = 24815/248832 ν. These sum to 207269/14515200 ν, and again two large terms nearly cancel.

**Answer to item 8.** No small set of interactions accounts for the value: the result is a near-cancellation between the {2,4} and {3,3} pairs, spread over six shells. The structural argument in section 4.2 accounts for the existence, order, monomial form and ν-independence of the coefficient, but not its magnitude.

---

## 5. Numerical reproduction: package values against ours

All "ours" values come from line (c): fixed-dt RK4 with dt = 0.005 and K = ⌊(N−1)/3⌋, unless marked otherwise.

### 5.1 64³ candidates (`RESULTS.md`)

| φ | Quantity | Package (CFL-adaptive RK4) | Ours N = 64 | Ours N = 96 |
|---|---|---|---|---|
| 0 | Z(2) | 2.229748776 | 2.2297487716 | 2.2297487715 |
| 0 | Z(4) | 1.806838777 | 1.8068387743 | 1.8068387814 |
| 0 | sampled peak | 2.240711313 @ 2.20 | 2.240711306 @ 2.20 | — |
| 0.971073032 | Z(2) | 2.255276393 | 2.2552763904 | — |
| 0.971073032 | Z(4) | 1.954808208 | 1.9548082050 | — |
| 0.971073032 | sampled peak | 2.344619472 @ 2.55 | 2.344619466 @ 2.55 | — |
| 2.159844949 | Z(2) | 2.128147203 | 2.1281472017 | — |
| 2.159844949 | Z(4) | 2.058295070 | 2.0582950664 | — |
| 2.159844949 | sampled peak | 2.339378222 @ 2.90 | 2.339378220 @ 2.90 | — |

**Trajectory and endpoint comparison at N = 64.**

| φ | max\|Z_ours − Z_pkg\| over [0,4] | dZ/dt(4), package | dZ/dt(4), ours |
|---|---|---|---|
| 0 | 1.41e-8 (t = 2.80) | −0.422549 | −0.422549 |
| 0.971 | 9.13e-9 (t = 3.05) | −0.464033 | −0.464033 |
| 2.16 | 3.24e-9 (t = 3.90) | −0.427863 | −0.427863 |

**Refined peaks (ours, N = 64).** Z = 2.24072957 at t = 2.1918; 2.34476832 at t = 2.5738; 2.33943383 at t = 2.8859.

**Grid convergence.**

* At φ = 0, N = 64 and N = 96 differ by 1e-10 in Z(2) and by 7e-9 in Z(4).
* N = 48 is within 1e-7 of N = 64 in Z(2) and within 1.3e-6 in Z(4).
* The 4-decimal peak values need N ≥ 48.

**Same-dt check (integrator explanation confirmed).**

| Case | Ours | Package |
|---|---|---|
| N = 24, dt = 0.01, φ = 0.971073032, Z(2) | 2.2553157108912 | 2.255315710891167 |
| N = 32, dt = 0.005, φ\* (32³), Z(2) | 2.255288136558 | 2.2552881365578 |

**Time convergence of our solver** (N = 24, φ = 0.971073032, Z(2)). For dt = 0.02, 0.01, 0.005 and 0.0025 we get 2.2553157832082, 2.2553157108912, 2.2553157061028 and 2.2553157057954. Successive differences shrink by factors 15.1 and 15.6, so the scheme is 4th order.

### 5.2 Rankings

| N | Z(2) order | Z(4) order |
|---|---|---|
| 24, 32, 48, 64 | 0.971 > 0 > 2.16 | 2.16 > 0.971 > 0 |

### 5.3 Local optimum of Z(2, φ)

| Grid | Package φ\* / Z(2) / Z_φφ | Audit re-run (package code) | Ours (independent) |
|---|---|---|---|
| 24³ | 0.971073031980 / 2.255315710891 / −0.170784509 | 0.9710730319801162 / 2.2553157108911694 | Newton 0.9710730446, golden 0.971073025 / 2.255315706103 / −0.170785 |
| 32³ | 0.970408763818 / 2.255288141713 / −0.170347874 | 0.9704087638177296 / 2.25528814171347 | Newton 0.9704087779, golden 0.970408758 / 2.255288136558 / −0.170348 |
| 48³ | — | — | 0.9703653579 / 2.255276553869 / −0.170339 |
| 64³ | — | — | 0.9703643925 / 2.255276433236 / −0.170339 |

* **Why φ\* differs slightly.** The differences of about 1.3e-8 to 1.4e-8 between the package's and our φ\* are time-step effects: the package optimiser uses a dt cap of 0.01, and we use dt = 0.005.
* **Why Z(2) differs.** The values differ by about 5e-9 because they were computed at different dt (see the dt = 0.005 row in section 5.6).
* **Convergence of φ\*.** The shifts are −6.6e-4 (24 → 32), −4.3e-5 (32 → 48) and −9.7e-7 (48 → 64). The continuum value is about 0.970364.
* **Shape at 24³.** Z(2, ·) is unimodal on [0.85, 1.10].

**Phase drift (supplementary).** This is not a headline of `RESULTS.md`.

| T | 33-point grid argmax (package sweep and ours) | Continuous maximiser, N = 24 | Continuous maximiser, N = 32 |
|---|---|---|---|
| 1 | 0 | 0 (φ = 0 optimal until T ≈ 1.765) | — |
| 2 | 0.9817 | 0.97107 | — |
| 2.5 | 1.4726 | 1.42380 | — |
| 3 | 1.6690 (17π/32) | 1.63745 | 1.63502 |
| 3.5 | 1.8653 | 1.85664 | — |
| 4 | 2.1598 (22π/32) | 2.12015 | 2.11816 |

### 5.4 Curvature crossing of ∂²_φ Z(T, 0)

| N | Package "linear crossing estimate" | Our linear interpolant (same two samples) | Our accurate crossing (tangent; 2nd-level Richardson FD agrees to 1e-10) |
|---|---|---|---|
| 24 | 1.764523827 | 1.7645238 | 1.764542 |
| 32 | 1.764968015 | 1.7649680 | 1.764986 |
| 48 | 1.764976046 | 1.7649760 | 1.764994 |
| 64 | — | — | 1.764994 |

**Curvature at the bracket ends, ∂²_φ Z at T = 1.76 / 1.77.**

| N | Package (dt cap 0.01) | Ours (tangent, dt = 0.005) |
|---|---|---|
| 24 | −0.0020361499 / +0.0024647953 | −0.0020361491 / +0.0024647961 |
| 32 | −0.0022321135 / +0.0022608554 | −0.0022321121 / +0.0022608568 |
| 48 | −0.0022356061 / +0.0022571299 | −0.0022356046 / +0.0022571315 |
| 64 | — | −0.0022355925 / +0.0022571443 |

* With dt ∈ {0.01, 0.005, 0.0025}, the crossings agree to 1e-6 or better.
* For T < 1.76499, φ = 0 is a local maximum of Z(T, ·); after that it is a local minimum, and a symmetric pair of maxima ±φ\*(T) branches off.

### 5.5 Spatial table: relative Z difference against 64³

| φ | T | Grid | Package | Ours (fixed dt) | Ratio |
|---|---|---|---|---|---|
| 0 | 2 | 32³ | 3.4640e-06 | 3.4629e-06 | 0.9997 |
| 0 | 2 | 48³ | 4.6168e-08 | 4.4995e-08 | **0.9746** |
| 0 | 4 | 32³ | 1.0405e-05 | 1.0405e-05 | 1.0000 |
| 0 | 4 | 48³ | 5.2210e-07 | 5.2203e-07 | 0.9999 |
| 0.971 | 2 | 32³ | 5.1927e-06 | 5.1916e-06 | 0.9998 |
| 0.971 | 2 | 48³ | 5.4675e-08 | 5.3541e-08 | **0.9793** |
| 0.971 | 4 | 32³ | 1.4048e-05 | 1.4048e-05 | 1.0000 |
| 0.971 | 4 | 48³ | 4.0555e-07 | 4.0566e-07 | 1.0003 |
| 2.160 | 2 | 32³ | 6.3863e-06 | 6.3856e-06 | 0.9999 |
| 2.160 | 2 | 48³ | 8.3129e-08 | 8.2482e-08 | **0.9922** |
| 2.160 | 4 | 32³ | 6.8017e-05 | 6.8017e-05 | 1.0000 |
| 2.160 | 4 | 48³ | 6.0727e-07 | 6.0755e-07 | 1.0005 |

The full-field L² column (for example 4.0827e-4 at φ = 0, T = 4, 48³) was reproduced to all printed digits, but only by the audit, using the package's code.

### 5.6 Temporal table at 32³ (selected phase)

| dt cap | Package Z(2) | Ours |
|---|---|---|
| 0.01 | 2.255288141713 | (audit, package code: identical) |
| 0.005 | 2.255288136558 | **2.255288136558** (independent) |
| 0.0025 | 2.255288136229 | (audit, package code: identical) |

### 5.7 Symmetry

* **The two maps.** The package, DNS and audit use R = diag(−1,−1,1) with b = (0,0,π), a proper rotation. The exact and float lines use G[u](x) = −u(−x + (π,0,0)), a parity map with det −1.
* **Both are valid.** Both maps send u_φ to u_{−φ}; this was checked analytically.
* **Mirror stabiliser.** Their composition, S[u](x) = diag(1,1,−1) u(x+π, y, −z−π), fixes u_φ. So the family has a mirror stabiliser.
* **Numerics.** At N = 24 and T = 2, Z(+0.5) − Z(−0.5) = −4.4e-16. In the tangent runs, Z_φ(T, 0) stays at or below 2e-16.

---

## 6. Errors, overclaims and bugs

**No mathematical error was found in the package, and no headline number is wrong.** The items below are bugs, overstated precision, and provenance gaps. Each comes with its smallest concrete instance.

### A. Bugs

* **B1. Test collection.**
  * **Failure.** Running `pytest -q` from the package root gives `1 error during collection: ModuleNotFoundError: No module named 'ns_solver'`, in `tests/test_sensitivity.py`.
  * **Cause.** `tests/test_sensitivity.py` and `tests/test_time_series.py` lack the `sys.path` insert that `tests/test_solver.py` has.
  * **Workaround.** Only `python -m pytest`, the command in the README, gives 27 passed.
* **B2. Ignored or hidden options.**
  * `phase_sensitivity.optimize` ignores `--dt`, because `integrate` is always called with `dt_max=.01`.
  * `integrate` hard-codes ν = 1/28 and has no `--nu` option.
  * These are harmless for the production runs but silently ignore user input.
* **B2b. Overwriting the archive.** `exact_viscosity_invariant.py` writes to the cwd-relative path `results/viscosity_identity`. Running it from the package root overwrites the archived certificate.

### B. Overstated precision (overclaims)

* **B3. Linear crossing estimates.**
  * `RESULTS.md` and `curvature_crossing.csv` print 1.764523827 (24³). The accurate crossing is 1.764542.
  * The bias is about 1.8e-5 at every grid. The values are correctly labelled as linear interpolants, but 9 decimals exceed their accuracy by about four orders of magnitude.
* **B4. Spatial relative-Z column.**
  * At φ = 0, T = 2, 48³ the package prints 4.6168e-8. A fixed-dt comparison gives 4.4995e-8.
  * The cause is that the table compares a fixed-dt 48³ run with a CFL-adaptive 64³ run, so a time-step error of about 2–3e-9 absolute contaminates the 48³, T = 2 rows (1–2.5%).
  * Printing 5 significant digits overstates what these rows measure.
* **C1 9th decimal.**
  * The 64³ sampled peak at φ = 0 is printed as 2.240711313; fixed-dt RK4 gives 2.240711306.
  * Over the whole trajectory the time-step error reaches 1.4e-8. The 9th decimal reflects the integrator, not the PDE.

### C. Provenance gaps

* **B5. Hard-coded counts.** `summarize_v2.py` hard-codes `tests_passed=27`, `independent_Taylor_coefficient_checks=21`, `exact_viscosity_identity_nodes=7` and the text "6.7e−16" instead of reading them from logs. The values happen to match the logs.
* **B6. Missing generating scripts.** No script in the package generates `results/spatial_comparison.csv` or `results/curvature_crossing.csv`. The archive also omits the `.npz` states. The audit regenerated the states and reproduced all 12 spatial rows and all 3 crossing rows.
* **B7. Garbled sentence.** `proof_notes.md` §3 contains "This nonzero coefficient is half of neither the objective nor its derivative". The factor-2 statement that follows it is correct.
* **B8. Scope and manifest.**
  * The exact identity in the package is proved for α = β = γ = δ = 1 only. Section 4 extends it to −6487/3110400 · α²β²γ²δ².
  * `execution_manifest.json` lists scipy, which no script uses.

### D. Acknowledged selection effects

These are stated in `RESULTS.md`; we confirm and quantify them.

* **0.971073 is a 24³ optimum.** It is not stationary at 32³ (dZ/dφ = −1.13e-4 there). The implied Z(2) shortfall is about 4e-8.
* **2.159845 = 22π/32 is a sweep grid point.** The 24³ T = 4 maximiser is 2.12015.
* **Rankings unaffected.** Neither effect changes a ranking.

### E. Errors in our own intermediate work, recorded for transparency

* **The brief's C5 wording.** The orchestrator's brief attributed "≈1.67 at T = 3" to a 17-point sweep. That wording is not in the package. A 17-point sweep gives π/2 = 1.5708. The package's actual 33-point sweep gives 1.669 = 17π/32, which we reproduce. The continuous optimum is 1.6375 (N = 24).
* **Float-line precision caveat.** The float line said its long-double values carry "about 18 significant digits". That is true for c_{6,0}(ν = 0) (relative 8.9e-18) and c_{9,3} (7.5e-18). It is false for:
  * c_{10,3}/ν: relative 3.1e-16, about 15.5 digits;
  * c_{12,4}: relative 4.1e-15, about 14 digits.
* **DNS-line wording.** The DNS line's "C1 reproduced" is accurate to 8 decimals, not 9.
* **Audit-line wording.** The audit's "bitwise" agreement re-ran the package integrator, so it demonstrates reproducibility, not accuracy.

### F. Not errors

* The audit's degree bound, deg_ν c_{n,m} ≤ n + 2 − 3\|m\|, is weaker than P2 because it omits the extra β². It was closed by explicit formal-ν computation.
* The package's `velocity_coefficients` counts (8, 36, 126, …) count per-component entries. The exact line's counts (8, 28, 68, …) count vector modes. The two are not comparable, and neither affects any result.

---

## 7. What remains unproven

### 7.1 A cutoff-uniform (continuum) estimate (item 9)

None exists, and the package correctly claims none. Every number in section 5 is a property of a Galerkin ODE at finite K, integrated in floating point.

To turn a statement such as "Z(2) at φ = 0.971 exceeds Z(2) at φ = 0" into a theorem about the PDE, one needs the following:

* **(i) A computable error bound.** Let u_K be the computed Galerkin trajectory and u the continuum solution. One needs a bound ε_K(t) ≥ ‖∇(u − u_K)(t)‖_{L²} on [0, T]. It must be in the enstrophy (H¹) norm, because the claims concern Z, and an L² velocity bound does not control Z.
* **(ii) The standard a-posteriori route** (in the style of Chernyshenko–Constantin–Robinson–Titi, 2007) has four parts:
  * **(a) Residual.** Measure the residual of u_K in the full equation, r_K = (I − P_K) P[(u_K·∇)u_K], along the computed trajectory.
  * **(b) Error inequality.** Use an H¹ energy inequality for e = u − u_K. Its linear growth rate depends on norms of u_K, and it has a superlinear term, because the 3D enstrophy inequality is cubic.
  * **(c) Closure.** Require that the comparison ODE for ‖∇e‖², started at 0 and driven by (a), stays finite through T. If it does, the continuum smooth solution exists on [0, T], and the bound on |Z(T) − Z_K(T)| is explicit.
  * **(d) Rigorous integration.** Add a bound on RK4 and floating-point error, for example by validated integration.
* **(iii) The decision criterion.** The rankings would become theorems if these bounds are smaller than the observed margins: at least 0.025 at t = 2 and at least 0.10 at t = 4.
* **What exists so far.**
  * The Lean repository has a Galerkin cutoff bound and a variable-coefficient Gronwall lemma. These are the kind of ingredients step (b) needs, but they are not connected to an NS evolution, which is not formalised.
  * The a-priori alternative is a bound on sup_{t ≤ T} Z_K(t) uniform in K. For this data on [0, 4] that is essentially the regularity question itself, and it is not available.

### 7.2 No remainder bound for the Taylor jet at t = 2 or t = 4

* **What is proven.** The order-6 identity, and the order-7, 9 and 12 results, are exact statements about time derivatives at t = 0.
* **What is missing.** Using the jet at finite t would need either a remainder bound |Z(t) − Σ_{n≤N} Z_n tⁿ| ≤ R_N(t), or an explicit lower bound on the radius of analyticity in t (for example a Gevrey-class estimate with constants evaluated for this data). Neither the package nor our work has one.
* **Evidence that exists, all at small t:**
  * the order-10 series matches the DNS to 1e-14 for t ≤ 0.1 and to 6e-9 at t = 0.3;
  * the order-12 series matches to 1.8e-10 at t = 0.2, ν = 1/7, which is the size of the truncation term.
* Convergence of the series was not proved.

### 7.3 Global optimality in φ

* **What exists.** The optimiser certifies a local stationary maximum (Z_φφ ≈ −0.170). The 33-point sweep looks unimodal at each T.
* **Why that is not enough.** A grid is not a global certificate.
* **What a certificate would need.** A validated Lipschitz or curvature bound on Z(T, ·) over [0, π], combined with validated values. Even that would only be a finite-K statement.

### 7.4 Continuum convergence of the numerical values

* **Evidence.** All convergence evidence is empirical:
  * N = 64 against N = 96: 1e-10 in Z(2) and 7e-9 in Z(4) (φ = 0);
  * φ\* shifts shrinking from 6.6e-4 (24 → 32) to 9.7e-7 (48 → 64);
  * crossing times agreeing to 1e-7 between N = 48 and N = 64.
* **Missing.** Without section 7.1, none of these is a bound against the PDE.

### 7.5 Smaller open points

* **Leading coefficients for \|m\| ≥ 5.** The coefficient at n = 3\|m\| is computed nonzero only for \|m\| = 2, 3, 4.
* **P1 at the solution level.** Verified numerically through T = 4; the proof has not been written out.
* **Phase lemma check.** The exact line's phase lemma was cross-checked against the generic complex implementation for three parameter sets only, though the lemma itself is proved.
* **Lean coverage.** No time-dependent statement is formalised in Lean.

---

## 8. Reproduction commands

```
W=audit_v2               # this folder of the ZIP
PKG=/path/to/periodic_ns_lab_v2   # your copy of the package (scripts that read it: run with python3 -I from outside it)
```

### (a) Exact series

Scripts are in `$W/exact`; outputs are in the same folder.

```
cd $W/exact
python3 run_series.py 12 1 1 1 1 z12_unit.json             # symbolic-nu jet to n=12, 83 s; asserts energy identity
python3 run_series.py 7 1 1 1 1 z7_unit_noprune.json --noprune
python3 tables.py z12_unit.json                            # -> tables_unit.txt
python3 phase_lemma_check.py 7 1/28 1 1 1 1                # second exact implementation
python3 test_predictions.py 10 9                           # P1, grading, monomials -> predictions.log
python3 p1_highorder.py 16 2 0 5 7                         # beta=0 to n=16 (+ beta=1/1000 control)
python3 mode_decomp.py 6 2 ; python3 mode_decomp.py 7 2    # -> mode_decomp_n6m2.log, mode_decomp_n7m2.log
python3 dns_check.py z10_unit.json 1/28 32 2e-3 8 0.3      # float DNS vs series
```

### (b) Float series

Scripts are in `$W/float`; outputs (logs and npz files) are in the same folder.

```
cd $W/float
python3 sanity.py ; python3 run_tables.py ; python3 analyse_tables.py ; python3 make_tables.py
python3 t_exact62.py ; python3 t_nu_poly.py --recompute ; python3 t_amp_degree.py --recompute
python3 t_beta0.py ; python3 t_random_monomial.py ; python3 t_loworder_ld.py ; python3 dns_check.py
```

### (c) DNS

Scripts are in `$W/dns`. The run order is in `queue1.sh`–`queue4.sh`.

```
cd $W/dns
python3 validate.py                       # exact solutions, budgets, dt convergence -> validate.out
python3 c1.py N dt [phi]                  # C1 trajectories (N = 24 32 48 64 96; dt 0.005 / 0.0025)
python3 c2.py                             # phi -> -phi symmetry
python3 c3.py N [dt] [notan]              # curvature crossing (FD + tangent); c3_interp.py for interpolation
python3 c4.py N [newton]                  # local optimum at T=2
python3 c5.py N M ; python3 c5_opt.py N T:phi0,...   # phase sweep (M=16 or 32) and continuous maximisers
python3 ns_if.py N dt {rk4|if} phis       # integrator diagnostics
```

### (d) Code audit

Scripts are in `$W/code_audit` (in the original run: audit/mine); re-run outputs were not included (42 MB).

```
cd $PKG && ../venv/bin/python -m pytest -v -p no:cacheprovider     # 27 passed
cd $PKG && ../venv/bin/pytest -q -p no:cacheprovider               # collection error (B1)
cd $PKG && python3 exact_time_series.py --order 6 --nu 1/28 --out ../rerun/exact_time_series.json
cd $W/audit/rerun && python3 ../pkg/exact_viscosity_invariant.py > viscosity_identity.log   # run outside PKG (B2b)
cd $PKG && python3 check_time_series.py --input ../rerun/exact_time_series.json --out ../rerun/independent_time_series_check.json
cd $W/code_audit && python3 -I exact_nu_poly.py 6 jet6.json
python3 -I compare_nodes.py jet6.json <archive>/results/viscosity_identity
python3 -I symmetry_sympy.py   # needs sympy ; python3 -I solver_checks.py
python3 -I variation_generic.py ; python3 -I fd_variations.py
bash rerun_all.sh                          # full sequential re-execution, about 28 min
python3 -I compare_runs.py {sweep,time,curv,refine}
```

### (x) Cross-check

Scripts and logs are in `$W/xcheck`.

```
cd $W/xcheck
python3 compare_series.py      # exact vs float vs package jets (Fraction equality)
python3 compare_dns_pkg.py     # DNS vs package diagnostics.csv, crossings, dZ/dt(4)
python3 spatial_relZ.py        # independent relative-Z column (section 5.5)
python3 p1_finite_time.py      # P1 at finite time, beta^2 scaling
python3 opt64.py               # N=64 local optimum
python3 highmode_t2.py         # 7/48 and 9/16
```

Any script that reads package files should be run with `python3 -I` from outside the package directory.
