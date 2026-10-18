# The nonlinear absorption condition at b = 0.003, T = 0.25: an inhomogeneous remainder estimate with validated q₁

**Status: paper argument with every constant explicit; the analytic constants evaluated in validated
interval arithmetic with directed rounding; the computed quantities (the base-flow amplitude and
the linear coefficient q₁) validated a posteriori against the exact equations through residuals,
with Galerkin tails included exactly and the time discretization enclosed, in double precision
with a documented inflation. Not formalized. One phase, φ = 0.37.**
Written by Claude (session "Inviscid run convergence past max|ω|"), 18 October 2026, on the
corrected finite-time note [../NOTE.md](../NOTE.md) at commit `cd9c9f0a`, branch
`claude/absorption-b003-T025`. It answers the question that note leaves open in its section 7:
for unit amplitudes, ν = 1/28 and T = 0.25, can b = 0.003 satisfy the nonlinear absorption condition

    C_A ( |b| sup_{[0,T]} ‖∇q₁‖ + b² K(T) ) ≤ ν/2,                                    (A)

where K(T) is a certified bound of ‖∇w‖/b² for the nonlinear remainder w := v − b q₁ and the
propagator of the linear operator L_U is bounded analytically, not sampled? The target (A), the
parameters and b were fixed before any number below was computed and are not changed here; a
second, weaker sufficient condition that the argument itself uses is reported alongside, labelled.

Conventions, the family, the base flow U, the coefficient q₁, the constants m₁, m₂, m_Δ, C_A,
the inequalities (I1)–(I6) and the exponents are those of [../NOTE.md](../NOTE.md) sections 0 and
2, used without change. β₁(0.25) = 1.08×10⁻³ of that note does not cover b = 0.003; the question
is whether the finer split v = b q₁ + w does.

## 1. The equation for the remainder and the inhomogeneous estimate

v = u_b − U solves v_t − νΔv + B(U,v) + B(v,U) + B(v,v) = 0, v(0) = b f, and q₁ solves
L_U q₁ = 0, q₁(0) = f, so w = v − b q₁ solves

    L_U w = −b² B(q₁,q₁) − b B(q₁,w) − b B(w,q₁) − B(w,w),        w(0) = 0.               (1.1)

Write q₁ = q₁^N + e, where q₁^N is a computed trigonometric polynomial (Section 3) and e the
error, and let, on [0, T],

    ε₀(t) ≥ ‖e(t)‖,   ε₁(t) ≥ ‖∇e(t)‖,   δ₂(t) ≥ ∫₀ᵗ ‖Δe‖²   (certified in Section 3),
    n₁(t) ≥ sup|∇q₁^N|,  n₂(t) ≥ sup|∇²q₁^N|,  p₀(t) ≥ sup|q₁^N|,  S^N(t) ≥ ‖∇q₁^N‖,  P^N(t) ≥ ‖q₁^N‖,

all computed (Section 3). Three facts about q₁^N are used: it is divergence-free (the Leray
projection and the linear interpolation preserve this in exact arithmetic; in double precision the
divergence is at roundoff, under the caveat of Section 3), it is smooth, and its sup norms are
bounded by the ℓ¹ sums of its Fourier coefficients. Everything below is for 0 ≤ t ≤ T on an
interval where the smooth solution exists; the continuation argument is at the end of Section 2.

**Lemma W1 (L² of w).** Pair (1.1) with w. By (I1) ⟨B(U,w),w⟩ = ⟨B(q₁,w),w⟩ = ⟨B(w,w),w⟩ = 0; by
(I2) |⟨B(w,U),w⟩| ≤ m₁‖w‖²; |⟨B(q₁,q₁),w⟩| ≤ ‖(q₁·∇)q₁‖‖w‖; and, splitting q₁ = q₁^N + e,
|⟨(w·∇)q₁^N, w⟩| ≤ n₁‖w‖² while ⟨(w·∇)e, w⟩ = −⟨(w·∇)w, e⟩ (div w = 0), so
|b||⟨(w·∇)e,w⟩| ≤ |b|‖e‖_∞‖∇w‖‖w‖ ≤ |b|C_A‖Δe‖‖∇w‖‖w‖ ≤ (ν/2)‖∇w‖² + b²C_A²‖Δe‖²‖w‖²/(2ν). With
ν‖∇w‖² ≥ (ν/2)‖∇w‖² + (ν/2)‖w‖² (Poincaré):

    d/dt ‖w‖ ≤ ρ₀(t) ‖w‖ + b² σ₁(t),     ρ₀ := m₁ + |b| n₁ + b² C_A² ‖Δe‖²/(2ν) − ν/2,

where σ₁(t) ≥ ‖(q₁·∇)q₁‖(t). Hence, with R₀(t) := ∫₀ᵗ ρ₀,

    ‖w(t)‖ ≤ b² N_w(t),     N_w(t) := ∫₀ᵗ e^{R₀(t) − R₀(s)} σ₁(s) ds.                      (1.2)

ρ₀ contains ‖Δe‖², which is controlled only in time-integrated form; that is enough, because ρ₀
enters only through its integral: ∫ ρ₀ ≤ ∫ (m₁ + |b|n₁ − ν/2) + b² C_A² δ₂/(2ν). On a single cell
[s, t] of the computation the dissipation integral is bounded by the cell increment of the right-hand
side of Lemma E's third inequality plus ε₁(s)²/(2ν) (Section 3), not by the increment alone.

**The source σ₁.** (q₁·∇)q₁ = (q₁^N·∇)q₁^N + (e·∇)q₁^N + (q₁^N·∇)e + (e·∇)e, so by (I5)

    ‖(q₁·∇)q₁‖ ≤ σ₁^a(t) + C_A ‖Δe‖ ‖∇e‖,    σ₁^a := p₀ S^N + n₁ ε₀ + p₀ ε₁.              (1.3)

(The computed bound of ‖(q₁^N·∇)q₁^N‖ is p₀ S^N, i.e. sup|q₁^N| · ‖∇q₁^N‖.) The last term of
(1.3) is again only time-integrable; in (1.2) it contributes at most
e^{R₀(t)} C_A ε₁(t) (t δ₂(t))^{1/2} by Cauchy–Schwarz (using e^{R₀(t) − R₀(s)} ≤ e^{R₀(t)}, i.e.
R₀(s) ≥ 0, true since ρ₀ ≥ m₁ − ν/2 ≥ |c| + |d| − ν/2 > 0), and in Lemma W2 below its square
contributes through δ₂. So σ₁ in (1.2) means σ₁^a plus this separately bounded piece.

**Lemma W2 (H¹ of w, with the bootstrap).** Pair (1.1) with −Δw. Each term:

- ⟨B(U,w),Δw⟩ ≤ m₁‖∇w‖² by (I3); ⟨B(w,U),Δw⟩ ≤ m₁‖∇w‖² + m₂‖w‖‖∇w‖ by (I4).
- b²|⟨(q₁·∇)q₁, Δw⟩| ≤ b² σ₁ ‖Δw‖ ≤ (ν/8)‖Δw‖² + 2 b⁴ σ₁²/ν.
- b|⟨(q₁^N·∇)w, Δw⟩| ≤ |b| n₁ ‖∇w‖²: integrate by parts once; the term with the second
  derivatives of w vanishes because div q₁^N = 0, and the other is −Σ_{i,j,k}⟨(∂_j q₁^N_k)(∂_k w_i)(∂_j w_i)⟩,
  bounded pointwise by |∇q₁^N| |∇w|² (operator norm ≤ Frobenius norm).
- b|⟨(e·∇)w, Δw⟩| ≤ |b| ‖e‖_∞ ‖∇w‖ ‖Δw‖ ≤ |b| C_A ‖Δe‖ ‖∇w‖ ‖Δw‖ ≤ (ν/8)‖Δw‖² + (2 b² C_A² ‖Δe‖²/ν) ‖∇w‖².
- b|⟨(w·∇)q₁^N, Δw⟩| ≤ |b| n₁ ‖∇w‖² + |b| n₂ ‖w‖ ‖∇w‖: integrate by parts once; the two terms are
  Σ(∂_j w_k)(∂_k q₁^N_i)(∂_j w_i) and Σ w_k (∂_j∂_k q₁^N_i)(∂_j w_i), bounded pointwise by
  |∇q₁^N||∇w|² and |w||∇²q₁^N||∇w|.
- b|⟨(w·∇)e, Δw⟩| ≤ |b| ‖w‖_∞ ‖∇e‖ ‖Δw‖ ≤ |b| C_A ε₁ ‖Δw‖² ≤ (ν/8)‖Δw‖²   provided   |b| C_A ε₁(T) ≤ ν/8.   (H1)
- |⟨(w·∇)w, Δw⟩| ≤ ‖w‖_∞ ‖∇w‖ ‖Δw‖ ≤ C_A ‖∇w‖ ‖Δw‖² ≤ (ν/2)‖Δw‖²   on any interval where   C_A ‖∇w‖ ≤ ν/2.   (H2)

The dissipation ν‖Δw‖² absorbs ν/8 + ν/8 + ν/8 + ν/2 = 7ν/8 of these; the remaining (ν/8)‖Δw‖² is
at least (ν/8)‖∇w‖². With y := ‖∇w‖² and (1.2), on an interval where (H1), (H2) hold:

    y′ ≤ 2ρ₁ y + 2 (m₂ + |b| n₂) ‖w‖ √y + 4 b⁴ σ₁²/ν,     ρ₁ := 2m₁ + 2|b| n₁ + 2 b² C_A² ‖Δe‖²/ν − ν/8.

Young's inequality 2(m₂ + |b|n₂)‖w‖√y ≤ (m₂ + |b|n₂)²‖w‖² + y gives y′ ≤ (2ρ₁ + 1) y + b⁴ [ (m₂+|b|n₂)² N_w² + 4σ₁²/ν ],
and with R₁(t) := ∫₀ᵗ (2ρ₁ + 1),

    ‖∇w(t)‖ ≤ b² K(t),     K(t)² := ∫₀ᵗ e^{R₁(t) − R₁(s)} [ (m₂ + |b| n₂)² N_w² + 4 σ₁²/ν ](s) ds.      (1.4)

In (1.4) the square of (1.3) is expanded as σ₁² ≤ 2σ₁^{a2} + 2C_A²‖Δe‖²‖∇e‖² ≤ 2σ₁^{a2} + 2C_A² ε₁² ‖Δe‖²,
and the second part is integrated against the dissipation bound (per cell, with the ε₁(s)²/(2ν)
term of Section 3). K is nondecreasing (every factor is), so
sup_{[0,T]} ‖∇w‖ ≤ b² K(T).

**Closure.** Let T_max be the maximal existence time of the smooth solution u_b and T′ := min(T, T_max).
w(0) = 0, so (H2) holds at t = 0 with room. Let t* be the supremum of times t < T′ up to which
C_A‖∇w‖ ≤ ν/2 on [0, t]. If (H1) holds and

    C_A b² K(T) < ν/2,                                                                        (B)

then on [0, t*] Lemma W2 gives C_A‖∇w‖ ≤ C_A b² K(T) < ν/2, so by continuity t* = T′, and
‖∇u_b‖ ≤ ‖∇U‖ + |b| ‖∇q₁‖ + ‖∇w‖ is bounded on [0, T′). If T_max ≤ T this contradicts the
enstrophy continuation criterion (../NOTE.md Proposition 1, same references), so T_max > T and
(1.2), (1.4) hold on [0, T]. ∎

This is the inhomogeneous remainder estimate asked for: the propagator of L_U enters only through
the analytic Grönwall factors e^{R₀}, e^{R₁}, built from the certified base-flow bounds m₁, m₂
of ../NOTE.md section 2 (no numerics), and the computed q₁^N enters only through its sup norms,
its H¹ norm and the source σ₁, each with a certified error term. The absorption that the argument
itself needs is (B) together with (H1): only the self-interaction B(w,w) is absorbed by the Agmon
inequality, and w is O(b²). The note's condition (A) then follows from ‖∇v‖ ≤ |b|‖∇q₁‖ + ‖∇w‖
with sup‖∇q₁‖ ≤ S_1 := sup (S^N + ε₁) and sup‖∇w‖ ≤ b² K(T); it is stronger than what is used,
and it is the condition this note was asked to decide.

## 2. The base flow in the computation and its error

The computation uses U_N := (σ, 0, w_N) with σ = a e^{−νt} sin y exact and w_N = Re(e^{ix} W_lin(y,t)),
where W_lin is the piecewise-linear-in-time interpolant between RK4 nodes of the truncated
(|n| ≤ K_W = 20) Fourier system of W_t = ν(W_yy − W) − i a e^{−νt} sin(y) W. The true W and the
error δW := W − W_lin satisfy

    δW_t = ν(δW_yy − δW) − i a e^{−νt} sin(y) δW − r_W,    r_W := W_lin,t − ν(W_lin,yy − W_lin) + i a e^{−νt} sin(y) W_lin,

with δW(0) the representation error of the data W(y,0) = c − d e^{i(y+φ)} in double precision
(W₁(0) = −d e^{iφ} is not exactly representable; the error is of the order of the machine epsilon and
is covered by the rounding caveat of Section 3, under which the chain starts from ε_W(0) = 0). In the weighted norm ‖X‖²_{*,3} := Σ_n (2+n²)³|X_n|²
the heat part is dissipative with rate at least ν (every mode has n²+1 ≥ 1) and multiplication by
sin y has operator norm at most L₃ := 2^{3/2} (the shift bound 2+(n±1)² ≤ 2(2+n²) of PROOF.md's
appendix), so

    d/dt ‖δW‖_{*,3} ≤ (L₃ |a| e^{−νt} − ν) ‖δW‖_{*,3} + ‖r_W‖_{*,3},    ε_W(t) := the resulting integral bound.

The residual r_W is a trigonometric polynomial computed exactly on each cell as a polynomial of
degree 1 in τ = t − t_j (the product sin(y)·W_lin reaches |n| = K_W + 1 and is kept, so the Galerkin
tail is in r_W), with the factor e^{−νt} frozen at t_j and its variation over the cell,
|e^{−ντ} − 1| ≤ νh, bounded separately. Since δw = Re(e^{ix}δW) and ‖·‖_{*,3} controls the ℓ¹ sums
by Cauchy–Schwarz,

    sup|δw| ≤ S₀ ε_W,   sup|∇δw| ≤ S₁ ε_W,   sup|∇²δw| ≤ S₂ ε_W,
    S₀² = Σ_n (2+n²)⁻³,  S₁² = Σ_n (1+n²)(2+n²)⁻³,  S₂² = Σ_n (1+n²)²(2+n²)⁻³

(the Frobenius norms of ∇ and ∇² of Re(e^{ix}W_n e^{iny}) are at most (1+n²)^{1/2}|W_n| and
(1+n²)|W_n|, and Minkowski's inequality; the three lattice sums are enclosed with their tails in
absorb_chain.py). These sups of δU = (0,0,δw) are what the q₁ residual needs.

## 3. The computed q₁ and its certified error

q₁ lives on k_z = ±1, so q₁ = Re(e^{iz} Q(x,y,t)) with Q complex, C³-valued, and L_U q₁ = 0 becomes

    Q_t = ν(Δ₂ − 1)Q − P[ σ Q_x + i w Q + (Q₂ σ_y, 0, Q₁ w_x + Q₂ w_y) ],     Q(0) = (0, −i, 0),

with P the Leray projector on the mode k̃ = (k_x, k_y, 1). Q is computed on |k_x|, |k_y| ≤ K_Q = 10
by RK4 with the exact Galerkin right-hand side (products evaluated on a 64² grid, alias-free since
K_Q + K_W + 1 < 32), with U_N of Section 2, and q₁^N := Re(e^{iz} Q_lin) with Q_lin the
piecewise-linear interpolant between the nodes. The error e := q₁ − q₁^N solves L_U e = −r, e(0) = 0,
with the residual

    r = [ Q_lin,t − νΔq₁^N + P(B-terms with U_N) ]  +  P[ (δU·∇)q₁^N + (q₁^N·∇)δU ],

where the first bracket, the residual in the full equation with the computed base flow, is a
trigonometric polynomial computed exactly on each cell as a polynomial of degree 2 in τ (Galerkin
part and tail together, since the products are not truncated), again with the frozen-σ variation
bounded separately, and the second bracket is bounded by the sups of Section 2:
‖(δU·∇)q₁^N‖ ≤ sup|δw| ‖q₁^N‖, ‖(q₁^N·∇)δU‖ ≤ sup|∇δw| ‖q₁^N‖, and for the gradient
‖∇[(δU·∇)q₁^N]‖ ≤ sup|∇δw|‖q₁^N‖ + sup|δw|‖∇q₁^N‖, ‖∇[(q₁^N·∇)δU]‖ ≤ sup|∇δw|‖∇q₁^N‖ + sup|∇²δw|‖q₁^N‖.
On each cell ∫‖r‖ ≤ h‖r₀‖ + (h²/2)‖r₁‖ + (h³/3)‖r₂‖ + (frozen-σ term) for r = r₀ + τr₁ + τ²r₂, and
likewise for ∇r.

**Lemma E (the error).** Pairing L_U e = −r with e and with −Δe, using (I1)–(I6) and
⟨r, Δe⟩ = −⟨∇r, ∇e⟩:

    d/dt ‖e‖ ≤ (m₁ − ν)‖e‖ + ‖r‖,
    d/dt ‖∇e‖ ≤ (2m₁ − ν)‖∇e‖ + m₂‖e‖ + ‖∇r‖,
    ν ∫₀ᵗ ‖Δe‖² ≤ ∫₀ᵗ ( 2m₁‖∇e‖² + m₂‖e‖‖∇e‖ + ‖∇r‖‖∇e‖ ),

so ε₀, ε₁, δ₂ are the corresponding integrals of the residual bounds with the Grönwall factors
e^{∫(m₁−ν)}, e^{∫(2m₁−ν)}. The third inequality integrates ½ d/dt‖∇e‖² + ν‖Δe‖² ≤ (right-hand side)
from 0, dropping ½‖∇e(t)‖² ≥ 0 and using e(0) = 0. Over a single cell [s, t] the same identity gives
ν ∫ₛᵗ ‖Δe‖² ≤ ∫ₛᵗ (right-hand side) + ½‖∇e(s)‖² ≤ ∫ₛᵗ (…) + ½ ε₁(s)², which is the per-cell bound
absorb_chain.py uses in the exponents of Lemmas W1 and W2 and in the C_A² ε₁² ‖Δe‖² source term of
(1.4); the cumulative δ₂ is used for the Cauchy–Schwarz term of (1.3). The cell recursions
e^{rate·Δ}(previous + source) are upper sums only when the cell-maximal growth rates are
nonnegative; the script asserts this on every cell (it holds because m₁ ≥ |c| + |d| = 2). These Grönwall factors are the same kind of loss that makes ../NOTE.md's
G₁ five times the measured value; here they multiply the residual, which is of order 10⁻⁵, and
are harmless. The quantities S^N, P^N, p₀, n₁, n₂ are the node values of ‖∇Q‖, ‖Q‖, Σ|Q̂_k|,
Σ|k̃||Q̂_k|, Σ|k̃|²|Q̂_k| (each convex in τ along the linear interpolant, so the cell maximum is at a
node), and S_1 = sup(S^N + ε₁).

What is and is not validated here. The Galerkin truncation is handled exactly (the tails are in
the residuals). The time discretization is handled exactly (the residual is that of a function
defined for all t). The base-flow truncation and discretization are handled exactly through δW.
The arithmetic is IEEE double; every number written by absorb_numerics.py is multiplied by
(1 + 10⁻¹⁰) and increased by 10⁻¹⁴. The residual norms are of order 10⁻⁵ and arise by cancellation
of O(1) terms, so their relative roundoff can itself be of order 10⁻¹⁰; the margin for the integrated
residuals therefore comes from the absolute term, 10⁻¹⁴ per coarse cell against an accumulated
roundoff of order 10⁻¹⁷ to 10⁻¹⁸, while the relative term covers the O(1) quantities (sup norms,
S^N). This inflation is documented, not certified. Everything after that
(absorb_chain.py) is interval arithmetic with directed rounding in the sense of ../constants.py,
on coarse cells of width 10⁻³ with upper sums (nondecreasing factors at the right endpoint, the
decreasing factor e^{−νt} at the left endpoint).

## 4. Numbers (a = c = d = 1, ν = 1/28, φ = 0.37, T = 0.25, b = 0.003)

Commands (from this folder; the first takes about 140 s in double precision, the second 0.6 s):

    python3 absorb_numerics.py            # writes results/numerics.json, results/numerics.log
    python3 absorb_chain.py               # writes results/chain.json, prints results/chain_b0.003.log

Validated bounds at T = 0.25 (every bound rounded up, every threshold rounded down; maximal relative
enclosure width of the interval chain 5.0·10⁻³⁵, plus the documented inflation of the numerics):

| quantity | meaning | bound |
|---|---|---|
| sup_t ‖W − W_lin‖_{*,3} | base-flow error (weighted norm, Section 2) | ≤ 7.6540·10⁻⁵ |
| ε₀(T) = sup_t ‖q₁ − q₁^N‖ | q₁ error, L² | ≤ 1.5475·10⁻⁵ |
| ε₁(T) = sup_t ‖∇(q₁ − q₁^N)‖ | q₁ error, H¹ | ≤ 5.6611·10⁻⁵ |
| δ₂(T) = ∫₀ᵀ ‖Δ(q₁ − q₁^N)‖² | q₁ error, dissipation | ≤ 4.5324·10⁻⁸ |
| S₁(T) = sup_t ‖∇q₁‖ | linear term | ≤ 0.74967 |
| N_w(T) = sup_t ‖w‖/b² | Lemma W1 | ≤ 0.33625 |
| K(T) = sup_t ‖∇w‖/b² | Lemma W2 | ≤ 15.674 |

The computed sup ‖∇q₁^N‖ is 0.749610; ../results/measurements.json has 0.7496 at t = 0.25 for the
same quantity, and 0.7078875 at t = 0.05 against 0.707888 here. The time course (upper bounds at
the coarse-cell boundaries) is in results/chain_b0.003.log; the Grönwall growth of K is roughly
linear in t, from 2.92 at t = 0.05 to 15.67 at t = 0.25.

**Result (exact calculation, validated interval chain on documented double-precision inputs).**
For a = c = d = 1, ν = 1/28, φ = 0.37, T = 0.25 and b = 0.003:

    (A)  b S₁ ≤ 2.2491·10⁻³,   b² K ≤ 1.4106·10⁻⁴,   b S₁ + b² K ≤ 2.3901·10⁻³  <  4.3906·10⁻³  ≤  ν/(2 C_A)

(the three bounds are rounded up separately, so the displayed parts need not add up to the displayed sum),

so the absorption condition C_A(|b| sup_t‖∇q₁‖ + b² K(T)) ≤ ν/2 of ../NOTE.md section 7 **holds**,
with margin factor ≥ 1.837. The bootstrap this folder's argument needs is weaker and also holds:

    (B)   C_A b² K < ν/2        ⇔  1.4106·10⁻⁴ < 4.3906·10⁻³    (margin factor ≥ 31),
    (H1)  |b| C_A ε₁(T) ≤ ν/8   ⇔  6.9073·10⁻⁷ ≤ 4.4642·10⁻³.

The target was fixed before the computation (b = 0.003, T = 0.25, condition (A) as stated in
../NOTE.md section 7) and was not changed afterwards. Where the two conditions differ, both are
reported above.

Where the margin goes. The linear term b S₁ is 94 % of the left side of (A); it is essentially
the measured quantity 0.7496 of ../NOTE.md, and the certification adds only ε₁ ≈ 6·10⁻⁵ to it.
The nonlinear term b² K is 6 %: K = 15.67 against the naive ‖∇w‖/b² one would read off a
simulation (of order 1), so the propagator estimate of Lemma W2 loses about a factor 10 to 15,
from the term-by-term bounds on the source and from the Grönwall factor e^{R₁}. Neither matters
for the decision at b = 0.003. The ceiling of (A) at this phase and horizon is the linear one noted
in ../NOTE.md: with S₁ = 0.74967 and K = 0 one would have b ≤ ν/(2 C_A S₁) ≈ 5.86·10⁻³.

Information only (same scripts with `--b`, outputs kept in results/chain_b*.json and .log; the
target of this folder remains b = 0.003). "Not certified" means the validated upper bound exceeds
the threshold; it does not mean the true quantity does:

| b | b S₁ ≤ | b² K ≤ | (A) left side ≤ | (A) certified | (B) left side ≤ | (B) certified |
|---|---|---|---|---|---|---|
| 0.003 | 2.2491·10⁻³ | 1.4106·10⁻⁴ | 2.3901·10⁻³ | yes (margin 1.84) | 1.4106·10⁻⁴ | yes |
| 0.0052 | 3.8983·10⁻³ | 4.2432·10⁻⁴ | 4.3226·10⁻³ | yes (margin 1.016) | 4.2432·10⁻⁴ | yes |
| 0.0053 | 3.9733·10⁻³ | 4.4082·10⁻⁴ | 4.4141·10⁻³ | no (0.995) | 4.4082·10⁻⁴ | yes |
| 0.0055 | 4.1232·10⁻³ | 4.7477·10⁻⁴ | 4.5980·10⁻³ | no (0.955) | 4.7477·10⁻⁴ | yes |
| 0.015 | 1.1246·10⁻² | 3.5499·10⁻³ | 1.4795·10⁻² | no | 3.5499·10⁻³ | yes |
| 0.016 | 1.1995·10⁻² | 4.0412·10⁻³ | 1.6036·10⁻² | no | 4.0412·10⁻³ | yes |
| 0.017 | 1.2745·10⁻² | 4.5647·10⁻³ | 1.7309·10⁻² | no | 4.5647·10⁻³ | no |

So at this phase the certificate of (A) extends to b = 5.2·10⁻³ and not to 5.3·10⁻³, and the
bootstrap (B) to b = 1.6·10⁻² and not to 1.7·10⁻²; (B) failing at larger b means this argument
stops, not that the solution does. Neither number is a stability radius.

## 5. What is certified, and what is not

- For |b| = 0.003 at φ = 0.37 and T = 0.25: the solution u_b is smooth on [0, T] and
  ‖∇w‖ ≤ b² K(T), ‖w‖ ≤ b² N_w(T) with the constants of Section 4, under the rounding
  caveat of Section 3 (double precision with a documented inflation in the numerics; validated
  interval arithmetic in the chain).
- Condition (A), the absorption condition of ../NOTE.md section 7, is decided in Section 4 with
  its margin. Condition (B), the one this argument needs, is weaker and is reported next to it.
- Not uniform in φ: the computed q₁ is for one phase. The analytic parts (m₁, m₂, the
  propagator bounds) are φ-uniform; the q₁ norms are not, and a φ-uniform certificate would need
  either a bound on ∂_φ q₁ or a computation on a φ grid with Lipschitz control. Not done.
- Not a statement about T > 0.25, about b = 1, or about regularity in general. The loss that
  remains is the Grönwall factor e^{R₁} in K; it is affordable because w is O(b²).
- The arithmetic of the numerics is not interval arithmetic. A version with validated FFT
  products would remove the one documented margin.

## 6. Review

One targeted reviewer (a single read-only agent, no sub-agents, no network), briefed on Sections
1–5, both scripts, the parent note and ../constants.py, and asked for CONFIRMED / ISSUE / NOT
CHECKED on the derivation, the chain, the numerics, Sections 2–3 and the consistency of the
numbers. Outcome, applied in this commit:

- Confirmed: every pairing bound of Lemmas W1 and W2 (including which form of the Agmon
  inequality each use needs), the Young constants and the 7ν/8 split, (1.4), the closure, the
  replication of ../constants.py in absorb_chain.base(), the lattice-sum exponents and tails, the
  rounding directions of the decisions, the alias-free products (|k_x| ≤ 11, |k_y| ≤ 30 on 64²),
  the untruncated residual, the frozen-σ correction, the inflation of every exported quantity,
  L₃ = 2^{3/2}, Lemma E, and every number of Section 4 against the result files (the reviewer re-ran
  the chain, which reproduced the log digit for digit, and replicated the recursion in plain
  double precision: K = 15.6732247, S₁ = 0.749667, N_w = 0.336241, ε₁ = 5.66108·10⁻⁵).
- One issue, major in rigor and numerically immaterial: the chain used the per-cell increment of
  the cumulative dissipation bound δ₂ in the exponents of Lemmas W1 and W2 and in the
  C_A²ε₁²‖Δe‖² source, which drops ½‖∇e(s)‖² − ½‖∇e(t)‖² on the cell without proof of its sign.
  Fixed by adding ε₁(s)²/(2ν) to the cell bound (Section 3). K changed from 15.67322467 to
  15.67322491; no printed digit of any result file changed, and both decisions are unchanged.
- Minor items, fixed in the text: the |b| factor in the Young step of Lemma W1; R₀ ≥ 0 stated
  where the Cauchy–Schwarz term needs it; the growth rates asserted nonnegative on every cell;
  the divergence-free and "exactly representable" statements qualified by the double-precision
  caveat; the roundoff margin sentence now names the absolute term; the sum in (A) of Section 4
  written as separately rounded bounds.
- Not checked by the reviewer: the parent's C_A certification and PROOF.md's appendix text
  (the shift inequality was verified directly); the numerics were code-reviewed and hash-matched,
  not re-run.
