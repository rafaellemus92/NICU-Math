# The nonlinear absorption condition at b = 0.003, T = 0.25: an inhomogeneous remainder estimate with validated q₁

**Status: paper argument with every constant explicit; the analytic constants evaluated in validated
interval arithmetic with directed rounding; the approximation (the base-flow amplitude W_lin and the
exactly solenoidal coefficient q₁^N) defined precisely from a stored trajectory and validated a
posteriori against the exact equations through residuals enclosed in rigorous interval arithmetic
(Galerkin tails, time discretization, initial-data, phase, viscosity and time-node discrepancies
all inside the enclosure). Not formalized. One phase, φ = 0.37. The first version of this note
(commit c764948) rested on inflated double-precision residuals and is superseded; see Section 7.**
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

all computed (Section 3). Three facts about q₁^N are used: it is divergence-free exactly, by
definition (Section 3: its node coefficients are the exact Leray projections P Q_j, so k̃·Q̂_k = 0
for every mode and every t, linear interpolation preserving this), it is smooth, and its sup norms
are bounded by the ℓ¹ sums of its Fourier coefficients. Every cancellation below that uses
div q₁^N = 0 (Lemma W1, bullets 3 and 5 of Lemma W2) and div e = 0 (Lemma E) is therefore exact;
no divergence-defect term arises. Everything below is for 0 ≤ t ≤ T on an
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
where W_lin is the piecewise-linear-in-time interpolant, on the exact nodes t_j = j/50000
(j = 0, …, 12500), between the stored node vectors W_j ∈ C⁴³ (modes |n| ≤ 21, each stored double
taken as the exact dyadic rational it is; trajectory/W_nodes.npy, produced by RK4 on the Galerkin
system truncated at |n| ≤ 20, which is irrelevant to what follows). The true W of
W_t = ν(W_yy − W) − i a e^{−νt} sin(y) W and the error δW := W − W_lin satisfy

    δW_t = ν(δW_yy − δW) − i a e^{−νt} sin(y) δW − r_W,    r_W := W_lin,t − ν(W_lin,yy − W_lin) + i a e^{−νt} sin(y) W_lin,

with δW(0) = W(·,0) − W₀ the representation error of the data W(y,0) = c − d e^{i(y+φ)}: W₀ is
checked to equal c exactly at n = 0 and zero for n ∉ {0, 1}, and at n = 1 the stored double differs
from −d e^{iφ} = −cos φ − i sin φ (φ = 37/100 exactly) by an amount enclosed from a decimal
enclosure of cos φ, sin φ (alternating Taylor series with remainder), giving
ε_W(0) := ‖δW(0)‖_{*,3} ≤ 2.695·10⁻¹⁶, the initial value of the chain. In the weighted norm ‖X‖²_{*,3} := Σ_n (2+n²)³|X_n|²
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

with P the Leray projector on the mode k̃ = (k_x, k_y, 1).

**Definition of the approximation.** The stored trajectory (trajectory/Q_nodes.npy, produced by RK4
on the Galerkin system |k_x|, |k_y| ≤ K_Q = 10 with alias-free products on a 64² grid; how it was
produced plays no role below) gives node arrays Q_j ∈ C^{3×21×21} at the exact nodes t_j = j/50000.
Set Q̃_j := P Q_j, the exact mode-wise Leray projection of the stored doubles (a rational array,
exactly solenoidal), let Q̃_lin be the piecewise-linear interpolant between the Q̃_j, and

    q₁^N := Re(e^{iz} Q̃_lin(x, y, t)),   U_N := (a e^{−νt} sin y, 0, Re(e^{ix} W_lin)),   a = c = d = 1, ν = 1/28, φ = 37/100.

Q₀ is checked bitwise to be (0, −i, 0) at k = 0 and zero elsewhere, so Q̃₀ is the exact initial
coefficient and e(0) = 0. The error e := q₁ − q₁^N solves L_U e = −r, with the residual

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
The initial data, the phase and the viscosity enter through their exact values: ε_W(0) above,
φ = 37/100 inside cos φ, sin φ, ν = 1/28 as an interval wherever it multiplies, e^{−νt_j} enclosed
from the exact rational node times (the double-precision times and constants used by the solver
never enter). The residual enclosure (validate_residual.py) is independent of the solver: it reads
only the node arrays, evaluates every product by direct convolution in k_y (Toeplitz sums over 21
terms, no FFT), applies P inside the interval computation, and encloses each cell integral as
h‖r₀‖ + (h²/2)‖r₁‖ + (h³/3)‖r₂‖ + e^{−νt_j}(νh²/2) max_nodes ‖T_σ(Q̃)‖ (with ∫₀ʰ ντ dτ = νh²/2 for
the frozen factor, ‖P f‖ ≤ ‖f‖, and the cell maximum of a norm along the linear path at a node),
likewise for ∇r and for r_W. Its arithmetic is midpoint-radius interval arithmetic over IEEE 754
binary64 vectorised in NumPy, under the model |fl(x ∘ y) − (x ∘ y)| ≤ u|fl(x ∘ y)| + η for
∘ ∈ {+, −, ×, /} with u = 2⁻⁵³ and η = 2⁻¹⁰²² (covering the subnormal range under gradual underflow;
flush-to-zero and denormals-are-zero modes assumed off, NumPy's default),
correctly rounded sqrt, exact abs and nextafter, and the order-independent summation bound
|fl(Σxᵢ) − Σxᵢ| ≤ γ_{n−1} Σ|xᵢ| + (n−1)η, γ_k = ku/(1−ku) (Higham, Accuracy and Stability of
Numerical Algorithms, 2nd ed., Lemma 3.1 and §4.2); every radius is rounded outward with nextafter
after each operation; only elementwise ufuncs and np.sum are used (no FMA, BLAS, FFT or matmul).
The scalar cell integrals, the coarse-cell sums and the decimal enclosures (e^{−νt_j}, cos φ, sin φ)
use the decimal interval class of ../constants.py; every written number is an upper bound rounded
up. Everything after that (absorb_chain.py) is interval arithmetic with directed rounding in the
sense of ../constants.py, on coarse cells of width 10⁻³ with upper sums (nondecreasing factors at
the right endpoint, the decreasing factor e^{−νt} at the left endpoint).

## 4. Numbers (a = c = d = 1, ν = 1/28, φ = 0.37, T = 0.25, b = 0.003)

Commands (from this folder; wall times on the 4-core container used here):

    python3 absorb_numerics.py        # 135 s: trajectory/W_nodes.npy, trajectory/Q_nodes.npy (not committed), results/numerics.json (inflated comparison numbers)
    python3 validate_residual.py      # 690 s: results/validated.json, the rigorous enclosures (log: results/validated.log)
    python3 absorb_chain.py           # 0.6 s: results/chain.json, printed as results/chain_b0.003.log

Validated bounds at T = 0.25 (every bound rounded up, every threshold rounded down; maximal relative
enclosure width of the interval chain 5.0·10⁻³⁵; the inputs are the rigorous enclosures of
validate_residual.py, maximal relative radius of r₀ over all cells 7.6·10⁻¹⁰, of the nodes Q̃_j 1.1·10⁻¹⁶):

| quantity | meaning | bound |
|---|---|---|
| ε_W(0) = ‖W(·,0) − W₀‖_{*,3} | initial-data representation error | ≤ 2.695·10⁻¹⁶ |
| sup_t ‖W − W_lin‖_{*,3} | base-flow error (weighted norm, Section 2) | ≤ 7.5438·10⁻⁵ |
| ε₀(T) = sup_t ‖q₁ − q₁^N‖ | q₁ error, L² | ≤ 1.5301·10⁻⁵ |
| ε₁(T) = sup_t ‖∇(q₁ − q₁^N)‖ | q₁ error, H¹ | ≤ 5.6024·10⁻⁵ |
| δ₂(T) = ∫₀ᵀ ‖Δ(q₁ − q₁^N)‖² | q₁ error, dissipation | ≤ 4.4389·10⁻⁸ |
| S₁(T) = sup_t ‖∇q₁‖ | linear term | ≤ 0.74967 |
| N_w(T) = sup_t ‖w‖/b² | Lemma W1 | ≤ 0.33625 |
| K(T) = sup_t ‖∇w‖/b² | Lemma W2 | ≤ 15.674 |

The validated upper bound of sup ‖∇q₁^N‖ is 0.749610; ../results/measurements.json has 0.7496 at
t = 0.25 for the same quantity, and 0.7078875 at t = 0.05 against 0.707888 here. The time course
(upper bounds at the coarse-cell boundaries) is in results/chain_b0.003.log; the Grönwall growth of
K is roughly linear in t, from 2.92 at t = 0.05 to 15.67 at t = 0.25.

**Result (exact calculation: validated interval chain on validated interval enclosures).**
For a = c = d = 1, ν = 1/28, φ = 0.37, T = 0.25 and b = 0.003:

    (A)  b S₁ ≤ 2.2490·10⁻³,   b² K ≤ 1.4106·10⁻⁴,   b S₁ + b² K ≤ 2.3901·10⁻³  <  4.3906·10⁻³  ≤  ν/(2 C_A)

(the three bounds are rounded up separately, so the displayed parts need not add up to the displayed sum),
so the absorption condition C_A(|b| sup_t‖∇q₁‖ + b² K(T)) ≤ ν/2 of ../NOTE.md section 7 **holds**,
with margin factor ≥ 1.837. The bootstrap this folder's argument needs is weaker and also holds:

    (B)   C_A b² K < ν/2        ⇔  1.4106·10⁻⁴ < 4.3906·10⁻³    (margin factor ≥ 31),
    (H1)  |b| C_A ε₁(T) ≤ ν/8   ⇔  6.8356·10⁻⁷ ≤ 4.4642·10⁻³.

The target was fixed before the computation (b = 0.003, T = 0.25, condition (A) as stated in
../NOTE.md section 7) and was not changed afterwards, neither in the first version of this note nor
after the audit. Where the two conditions differ, both are reported above.

Comparison with the superseded inflated inputs (commit c764948): they gave ε_W ≤ 7.6540·10⁻⁵,
ε₀ ≤ 1.5475·10⁻⁵, ε₁ ≤ 5.6611·10⁻⁵, δ₂ ≤ 4.5324·10⁻⁸ and the same S₁, N_w, K, left side and margin
to the digits shown (b S₁ ≤ 2.2491·10⁻³ then). The validated enclosures are slightly smaller because
the frozen-factor correction is now ∫₀ʰ ντ dτ = νh²/2 rather than νh·h and no inflation is applied;
the two independent evaluations of the residual sums agree to within 1.5 % (∫‖r‖: 5.3259·10⁻⁶
validated against 5.3699·10⁻⁶ inflated; ∫‖∇r‖: 1.0785·10⁻⁵ against 1.0848·10⁻⁵; ∫‖r_W‖_{*,3}:
5.1980·10⁻⁵ against 5.2745·10⁻⁵). This agreement is a consistency check, not part of the proof.

Where the margin goes. The linear term b S₁ is 94 % of the left side of (A); it is essentially
the measured quantity 0.7496 of ../NOTE.md, and the certification adds only ε₁ ≈ 6·10⁻⁵ to it.
The nonlinear term b² K is 6 %: K = 15.67 against the naive ‖∇w‖/b² one would read off a
simulation (of order 1), so the propagator estimate of Lemma W2 loses about a factor 10 to 15,
from the term-by-term bounds on the source and from the Grönwall factor e^{R₁}. Neither matters
for the decision at b = 0.003. The ceiling of (A) at this phase and horizon is the linear one noted
in ../NOTE.md: with S₁ = 0.74967 and K = 0 one would have b ≤ ν/(2 C_A S₁) ≈ 5.86·10⁻³.

Information only (same scripts with `--b`, outputs kept in results/chain_b*.json and .log, all on
the validated inputs; the target of this folder remains b = 0.003). "Not certified" means the
validated upper bound exceeds the threshold; it does not mean the true quantity does:

| b | b S₁ ≤ | b² K ≤ | (A) left side ≤ | (A) certified | (B) left side ≤ | (B) certified |
|---|---|---|---|---|---|---|
| 0.003 | 2.2490·10⁻³ | 1.4106·10⁻⁴ | 2.3901·10⁻³ | yes (margin 1.84) | 1.4106·10⁻⁴ | yes |
| 0.0052 | 3.8983·10⁻³ | 4.2432·10⁻⁴ | 4.3226·10⁻³ | yes (margin 1.016) | 4.2432·10⁻⁴ | yes |
| 0.0053 | 3.9733·10⁻³ | 4.4082·10⁻⁴ | 4.4141·10⁻³ | no (0.995) | 4.4082·10⁻⁴ | yes |
| 0.0055 | 4.1232·10⁻³ | 4.7477·10⁻⁴ | 4.5980·10⁻³ | no (0.955) | 4.7477·10⁻⁴ | yes |
| 0.015 | 1.1245·10⁻² | 3.5499·10⁻³ | 1.4795·10⁻² | no | 3.5499·10⁻³ | yes |
| 0.016 | 1.1995·10⁻² | 4.0412·10⁻³ | 1.6036·10⁻² | no | 4.0412·10⁻³ | yes |
| 0.017 | 1.2745·10⁻² | 4.5647·10⁻³ | 1.7309·10⁻² | no | 4.5647·10⁻³ | no |

So at this phase the certificate of (A) extends to b = 5.2·10⁻³ and not to 5.3·10⁻³, and the
bootstrap (B) to b = 1.6·10⁻² and not to 1.7·10⁻²; (B) failing at larger b means this argument
stops, not that the solution does. Neither number is a stability radius.

## 5. What is certified, and what is not

- For |b| = 0.003 at φ = 0.37 and T = 0.25: the solution u_b is smooth on [0, T] and
  ‖∇w‖ ≤ b² K(T), ‖w‖ ≤ b² N_w(T) with the constants of Section 4, with every numerical quantity
  enclosed in validated interval arithmetic (Section 3). What is assumed is: IEEE 754 binary64
  round-to-nearest with gradual underflow (no flush-to-zero or denormals-are-zero mode), no FMA
  contraction and no extended precision in NumPy's elementwise ufuncs, np.sum and sqrt; a correct
  `decimal` module and float↔Decimal conversion in Python; and C_A, m₁, m₂ as certified in
  ../NOTE.md. This is the standard semantics of NumPy on x86-64 and is stated, not verified by
  the code.
- Condition (A), the absorption condition of ../NOTE.md section 7, is decided in Section 4 with
  its margin. Condition (B), the one this argument needs, is weaker and is reported next to it.
- Not uniform in φ: the computed q₁ is for one phase. The analytic parts (m₁, m₂, the
  propagator bounds) are φ-uniform; the q₁ norms are not, and a φ-uniform certificate would need
  either a bound on ∂_φ q₁ or a computation on a φ grid with Lipschitz control. Not done.
- Not a statement about T > 0.25, about b = 1, or about regularity in general. The loss that
  remains is the Grönwall factor e^{R₁} in K; it is affordable because w is O(b²).
- The stored trajectory itself (265 MB) is not committed; its SHA-256 is recorded in
  results/numerics.json and results/validated.json, and absorb_numerics.py regenerates it
  bit-for-bit on the same platform (checked three times in this session; validate_residual.py was
  run four times on it, with identical output apart from wall time and the recorded source hashes).
  A different trajectory would simply be a different approximation to validate; nothing in the
  certificate depends on how it was produced.

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

## 7. The three certification gaps of the audit and how they are closed

An independent audit of commit c764948 reproduced the chain and named three gaps in the certificate
as it then stood. Each is closed in this commit without changing b, T or φ; the target condition (A)
is unchanged.

1. **Floating-point residual evaluation.** The residual norms were double-precision numbers
   inflated by x(1 + 10⁻¹⁰) + 10⁻¹⁴, a documented margin, not an enclosure. Now
   validate_residual.py encloses every residual integral and every norm of the approximation in
   midpoint-radius interval arithmetic over IEEE binary64 with the rounding model of Section 3
   (every operation's error bounded by u|result| + η, order-independent summation bound,
   outward rounding of every radius), independently of the solver: it reads only the stored node
   arrays and evaluates the products by direct convolution. The chain (absorb_chain.py) reads
   these enclosures by default; fed the old inflated numbers it labels its verdict conditional.
   The enclosures agree with the inflated numbers to the digits shown in Section 4 (the maximal
   relative radius of r₀ is 7.6·10⁻¹⁰; the inflated and the validated sums of ∫‖r‖ differ by
   less than 1.5 %), which is a consistency check of the two independent evaluations, not part of the proof.
2. **Initial-data, phase, viscosity and time-node discrepancies.** The approximation is now defined
   from exact objects (Section 3): exact rational node times t_j = j/50000 and coarse boundaries,
   the stored doubles as exact dyadic rationals, ν = 1/28 and h = 1/50000 as intervals wherever
   they multiply, e^{−νt_j} enclosed from the exact rational t_j, φ = 37/100 exactly inside the
   enclosures of cos φ and sin φ, and the representation error of the initial datum W₁(0) = −d e^{iφ}
   enclosed and carried as ε_W(0) ≤ 2.695·10⁻¹⁶ (Section 2); Q₀ is checked bitwise to be exact.
   The solver's own floating-point times and constants never enter.
3. **Solenoidality.** The approximation's node coefficients are defined as the exact Leray
   projections Q̃_j := P Q_j (Section 3), so div q₁^N = 0 exactly for all t; P is applied inside the
   interval computation, and every norm and residual of Section 4 is that of Q̃. The cancellations of
   Lemmas W1, W2 and E that use div q₁^N = 0 and div e = 0 are therefore exact, and no
   divergence-defect term is needed.

Not changed: the derivation of Section 1, the analytic constants, the chain's structure, the phase,
the horizon and b. The result of Section 4 is now a closed certificate under the platform model
stated in Section 5, with no conditional numerical input.

**Second review.** One targeted reviewer (a single read-only agent, no sub-agents, no network),
briefed on the audit's three gaps, validate_residual.py, the chain changes and Sections 3–5 and 7,
checked the floating-point model and every interval helper line by line, cross-checked T_σ and T_w
at a node against an independent 128² FFT evaluation (agreement 7·10⁻¹⁷ and 1.4·10⁻¹⁶ on O(0.5)
fields, no energy outside the retained mode ranges), checked the cell polynomials against a direct
midpoint evaluation (1–2·10⁻¹⁶), the bilinear cross-term identity, the initial-data checks, the
exact e^{−νt_j}, the norm conventions, the solenoidality claim of Section 1 (e and every term of r
exactly solenoidal), the chain diff against c764948 (only the stated changes) and every number of
Section 4 against the result files. Verdict: no blocking or major finding; gaps (i)–(iii) closed;
what remains assumed is the platform model, the `decimal` module and the parent's C_A, m₁, m₂.
Minor items, fixed in this commit: ε_W(0) was printed rounded to nearest (2.694 → 2.695·10⁻¹⁶,
the chain and the validator now print it rounded up); the arithmetic model wrongly claimed to
cover flush-to-zero (it assumes gradual underflow, NumPy's default); the residual sums agree to
1.5 %, not 1 %; the csum docstring now derives the (1+u) factor absorbed by F (the reviewer also
checked the slack numerically for every n that occurs); the validator's stated runtime; and the
chain's provenance key for the hash of the input-producing script is now `inputs_source_sha256`.
None affects a printed digit or a decision.

## 8. The trajectory artifact, what the certificate implies, and what the enstrophy theorem still needs

### 8.1 The artifact

The approximation of Section 3 is defined by two arrays, written by absorb_numerics.py and read by
validate_residual.py. They are preserved unaltered (file mode read-only) and their identity is fixed
by the hashes below, recorded in results/trajectory_manifest.json and checked by check_artifact.py
(step 1: hashes, sizes, shapes against the manifest, results/numerics.json and results/validated.json;
step 2, `--full`: an end-to-end rerun of validate_residual.py and absorb_chain.py compared with the
committed results).

| file | bytes | shape, dtype | SHA-256 of the file | SHA-256 of the raw array bytes |
|---|---|---|---|---|
| trajectory/W_nodes.npy | 8 600 816 | (12501, 43) complex128 | 0fc8d078c09bf8c8b05e3e0a40bfbe6c019b0c873f1748a0f3bbae8d8112daa9 | 825078dc2eaf8818b6e0bcd0ca6615559a3d5bb32781507dd0c4e01bf37e22bd |
| trajectory/Q_nodes.npy | 264 621 296 | (12501, 3, 21, 21) complex128 | 7a8157de830a5c2358119084947299a8aeb5daf7b749f69e8506c23c47e94ccd | 529b1e4c61f0a98437d09d92b1e71a1ad9a271fefafb7bbd5d507412cb4bd9d8 |

Layout: W_nodes[j, i] is node j = 0..12500, mode n = i − 21; Q_nodes[j, c, ix, iy] is node j, component c,
k_x = ix − 10, k_y = iy − 10. A plain tar of the two files and the manifest
(absorption-b003-trajectory-63ddc17.tar, 273 233 920 bytes, SHA-256
6ea552edc5b0a3ca83e1e4a4a1d5ef1aa0b70f55533f43e30c19b0ac643b73de) compresses to 209 MB with xz, above
GitHub's 100 MB per-file limit, so the arrays are not in the repository: at the time of this commit they
exist only in the session's worktree (git-ignored `trajectory/`) and scratchpad, and the external
destination awaits the user's decision (Section 8.1 of the report accompanying this commit lists the
options). Until then the arrays are regenerable bit-for-bit by absorb_numerics.py on the same platform
(three regenerations in this session, hashes above each time); the certificate itself does not depend
on where they are stored.

check_artifact.py at this commit: step 1 passed; step 2 (`--full`, 11 min) passed — the fresh
validate_residual.py output is identical to results/validated.json apart from wall time, and the chain
run on it is identical to results/chain.json, verdict CERTIFIED. This is the standing check for the
next review: verify the saved arrays' hashes, then rerun the validator end to end.

### 8.2 Exactly what follows from the certified condition

For a = c = d = 1, ν = 1/28, φ = 37/100, T = 1/4 and |b| = 3/1000 — both signs, because
u_{−b}(x, y, z, t) = u_b(x, y, z + π, t) exactly (the shift z ↦ z + π flips sin z and fixes the other two
components of the data, and the equations are translation invariant), so every norm below is the same for
b = ±0.003:

1. The smooth solution u_b exists on [0, T] (closure of Section 1, through the enstrophy continuation
   criterion, as in ../NOTE.md Proposition 1).
2. sup_{[0,T]} ‖∇v‖ ≤ |b| S₁ + b² K ≤ 2.3901·10⁻³, hence C_A ‖∇v(t)‖ ≤ ν/2 for every t ∈ [0, T]. This is
   the bootstrap inequality of ../NOTE.md Lemma 2, now established on all of [0, T] at |b| = 0.003, whereas
   ../NOTE.md Proposition 1 establishes it only for |b| < β₁(0.25) = 1.08·10⁻³. Consequently the conclusions
   of Lemma 2 hold at |b| = 0.003 on [0, T] (Lemma 1 needs no smallness): ‖∇v(t)‖ ≤ |b| G₁(t) and
   ∫₀ᵗ ‖Δv‖² ≤ b² D₁(t). The certified 2.39·10⁻³ is five times below |b| G₁(0.25) = 1.21·10⁻².
3. ‖v − b q₁‖ ≤ b² N_w ≤ 3.03·10⁻⁶ and ‖∇(v − b q₁)‖ ≤ b² K ≤ 1.41·10⁻⁴ on [0, T]: the response to
   b sin z is its linear coefficient up to an O(b²) remainder with these explicit constants; since q₁
   has no z-mean, the mean part obeys v̄ = w̄, so ‖∇v̄‖ ≤ b² K as well.

What does not follow from the certificate alone: the Theorem of ../NOTE.md section 5, |R_Z(t)| ≤ C_Z(t) b⁴,
is stated under |b| < β₁(T) and its text therefore does not cover b = 0.003; nothing here changes β₁;
nothing is claimed for T > 0.25 or for other φ. For |b| < 0.003 and for the enstrophy remainder at
|b| ≤ 0.003 see the audited Route A corollary in Section 8.3 (the information table of Section 4 is not
a certificate for other b).

### 8.3 What is needed to extend the enstrophy remainder theorem to b = 0.003

Route A — the parent theorem as it stands, with the bootstrap supplied by (A). In ../NOTE.md the
hypothesis |b| < β₁(T) serves two purposes, on my reading of its Sections 3–5 (to be confirmed by that
note's owner): (1) through Proposition 1, it gives C_A‖∇v‖ ≤ ν/2 on [0, T], hence Lemma 2's G₁, D₁
bounds and the absorption of the cubic term of Lemma 4 (C_A‖∇v̄‖ ≤ C_A‖∇v‖ ≤ ν/2); (2) it is used as a
number, |b| ≤ β₁, wherever a power of b beyond the displayed one is absorbed: in N_r and S_r* (Lemma 5,
hence R₁ and D_r), in Ē (Lemma 7) and in the terms β₁ Q₂ Ẽ + ½ β₁² Ẽ² of C_Z; Lemma 6 and the identity
of Section 5 use no such bound. Purpose (1) is now certified at |b| = 0.003 by (A) and Section 1.
Purpose (2) is bookkeeping: replace β₁ by β := 3/1000 in those four places and recompute everything
downstream (R₁, D_r, N_e, Ẽ, D_e inherit the dependence through N_r and S_r*). No new analytic estimate
is needed; what is needed is one evaluation of C_Z^{(β)}(0.25) in the parent's constants.py and a check of
the reading above. The first version of this paragraph predicted "C_Z^{(β)} ≤ (β/β₁)² C_Z^{(β₁)} ≈ 7.7
C_Z^{(β₁)} at worst"; that was wrong by a factor of about six, see the audit record below: β enters the
chain to the fourth power (the dominant term of Ē is β² Ẽ D_e^{1/2} with Ẽ and D_e^{1/2} each linear in
β at leading order), and the evaluated increase is 45.9. The result reads |R_Z(t)| ≤ C_Z^{(3/1000)}(t) b⁴
on [0, 1/4] with C_Z^{(3/1000)}(1/4) ≤ 1.2102·10¹⁴; at b = 0.003 that is |R_Z| ≤ 9.80·10³ against an
enstrophy of order one, and 1.9·10¹⁸ times the measured |R_Z|/b⁴ = 6.4·10⁻⁵ of ../NOTE.md Table B. A
theorem with a constant that carries no information. The evaluation was not committed anywhere (it
modifies the parent's chain; the target and scripts of this folder are fixed).

**Route A audited (19 October 2026).** The session "Navier Stokes-Speech" audited Route A on the
parent note at cd9c9f0 and this folder at 763c275 without editing either branch; its findings, which I
checked as stated here:

- *Where |b| < β₁(T) is used.* Exactly as read above: Proposition 1 (strictness at t = 0, the continuity
  bootstrap, the continuation criterion); Section 4's preamble through Proposition 1; Lemma 3 b-free;
  Lemma 6 and the six-term identity exactly of order b³ with no bound on b; the non-strict bookkeeping
  |b| ≤ β₁ in N_r and S_r* (Lemma 5), Ē (Lemma 7) and the terms β₁Q₂Ẽ + ½β₁²Ẽ² of the Theorem. Confirmed.
- *The constant.* Their interval evaluation of the parent's chain with β = 3/1000 at T = 0.25 (n = 20000,
  rounded up): N_r ≤ 5.2262·10³ (was 2.1049·10³), Ẽ ≤ 5.8735·10⁸ (2.2538·10⁸), Ē ≤ 2.8179·10¹³
  (6.1475·10¹¹), C_Z ≤ 1.2102·10¹⁴ (2.6389·10¹²), ratio 45.9. Replicated here digit for digit in a scratch
  copy of ../constants.py with a three-line hook substituting β for β₁ (the unhooked copy reproduces
  ../results/constants.log at T = 0.25 first); the scratch copy is not committed.
- *Lemma M (uniform closure for every |b| ≤ b₀ := 3/1000).* Their statement: in this folder's chain b
  enters only through |b|n₁, b²C_A²‖Δe‖²/ν, |b|n₂, |b|C_Aε₁ and b²K, each the product of |b| or b² with
  a nonnegative b-independent quantity (q₁^N, its error bounds ε₀, ε₁, δ₂, S₁ and σ₁ do not depend on b),
  so ρ₀, ρ₁, R₀, R₁, N_w(t; b), K(t; b) and the left sides of (A), (B), (H1) are nondecreasing in |b|.
  Confirmed against absorb_chain.py: with the validated cell inputs fixed, rho0_int, Nw, rho1_int2, R0,
  Nw_tot, Kw2 and lhsA, lhsB1, lhsB2 are built from b only through exp, sums, products and square roots
  of nonnegative quantities in which b and b² carry nonnegative coefficients, so the exact recursion
  values are nondecreasing functions of |b| ≥ 0. The uniform closure then runs as follows, which is the
  precise form I accept: for 0 ≤ |b| ≤ b₀ the hypotheses of Section 1's closure at b, namely (H1)
  |b|C_Aε₁ ≤ ν/8 and (B) C_A b² K̂(T; b) < ν/2 with K̂ the exact recursion value, follow from the same
  inequalities at b₀, because K̂(T; b) ≤ K̂(T; b₀) ≤ the rounded-up printed K(T; b₀) = 15.674 and
  |b| ≤ b₀; the closure (w(0) = 0 for every b, continuity, the enstrophy criterion) therefore gives the
  smooth solution on [0, T] and ‖∇w_b‖ ≤ b² K̂(T; b) ≤ b² K(T; b₀), hence
  ‖∇v_b‖ ≤ |b| S₁ + b² K(T; b₀) ≤ b₀ S₁ + b₀² K(T; b₀) ≤ 2.3901·10⁻³ and C_A‖∇v_b‖ ≤ ν/2 on [0, T],
  for every |b| ≤ 3/1000 and both signs. Two remarks, not gaps: (i) this is monotonicity of the
  certificate's bounds, proved from the recursion, not monotonicity of the solution in b, of which
  nothing is known or used; (ii) the rounding direction matters only once, in K̂(T; b₀) ≤ K(T; b₀).
  The information table of Section 4 (K from 15.673 at b = 0.003 to 15.795 at 0.017) is consistent with
  Lemma M but is a check, not the proof. No gap found.
- *The corollary (Route A), accepted.* For a = c = d = 1, ν = 1/28, φ = 37/100, T = 1/4, every
  |b| ≤ 3/1000 and 0 ≤ t ≤ T: u_b is smooth on [0, T]; ‖∇v(t)‖ ≤ |b| G₁(t) and ∫₀ᵗ ‖Δv‖² ≤ b² D₁(t) with
  the parent's G₁, D₁ (Lemma 2, whose hypothesis is the absorption inequality above); and
  |R_Z(t)| ≤ C_Z^{(3/1000)}(t) b⁴ with C_Z^{(3/1000)} the parent's chain with β₁ replaced by 3/1000 in
  N_r, S_r*, Ē and the Theorem and everything downstream recomputed, C_Z^{(3/1000)}(1/4) ≤ 1.2102·10¹⁴
  (the parent's "Lemma 0": every constant of that chain is nondecreasing in β, so any β ≥ |b| is
  admissible). Proof as in their audit: Lemma 1 by existence; Lemma 2 from the certified absorption
  inequality; Lemma 4's absorption from ‖∇v̄‖ ≤ ‖∇v‖; Lemmas 5, 7 and the Theorem with β = 3/1000;
  Lemma M for the whole interval. Status: exact calculation on certified constants, a theorem whose
  constant is vacuous at this b (|R_Z| ≤ 9.80·10³). The audit, Lemma M and the corollary are
  Navier Stokes-Speech's work; this record is my confirmation of them.

Route B — a constant that means something, built from the certified sharp quantities. Replace the
G₁, D₁-based chain of ../NOTE.md Lemmas 4–7 by this folder's bounds. The estimates needed, in order:

1. A certified bound ∫₀ᵀ ‖Δw‖² ≤ b⁴ D_w. Lemma W2 keeps (ν/8)‖Δw‖² when integrated; the chain drops it.
   It is one more accumulator over the same cells (not added: scripts fixed), and it replaces the parent's
   D₁ and D̄ in every source term below.
2. Bounds on the second-order coefficient q₂ (source (q₁·∇)q₁, modes k_z ∈ {0, ±2}): either the parent's
   analytic Lemma 3 (N₂, Q₂, D₂ built from G₁, D₁, crude but available), or a validated computation of q₂
   exactly as q₁ is validated here (a residual-enclosed Galerkin solution plus its own validator). The
   latter is a new computation of the size of this folder's, not done.
3. The second-order remainders ẽ₂ = w̃ − b² q̃₂ and ē₂ = w̄ − b² q̄₂: linear equations driven by
   (q₁·∇)w + (w·∇)q₁ + (w·∇)w − b² [(q₁·∇)q₁ − its first-order part], of orders b³ and b⁴, bounded by
   (I5) with the certified n₁, n₂, p₀ (sup norms of q₁^N), N_w, K and D_w from item 1 — the analogues of
   Lemmas 5–7 with S₁, K, N_w, D_w in place of G₁, V̄, D₁, D̄, each with one Grönwall factor of the
   linear operator (of the size of e^{R₁} ≈ 10 here, not of the parent's compounded losses).
4. The exact enstrophy identity of ../NOTE.md section 5, R_Z = ⟨−ΔU, ē₂⟩ + ½‖∇v̄‖² + ½ b⁴ ‖∇q̃₂‖² +
   b² ⟨∇q̃₂, ∇ẽ₂⟩ + b ⟨∇q₁, ∇ẽ₂⟩ + ½‖∇ẽ₂‖², assembled with the parent's m_Δ and items 1–3, giving
   |R_Z(t)| ≤ C′_Z(t) b⁴ on [0, 0.25] at |b| = 0.003 with ‖∇v̄‖ ≤ b² K already in hand.

Neither route needs a new parameter sweep. Route A needs no simulation; Route B needs none beyond the
stored trajectory unless a validated q₂ is wanted (item 2).
