# A certified finite-time bound for the enstrophy error beyond the b² response

**Status: paper argument with every constant explicit; constants evaluated in validated interval
arithmetic with directed rounding (admissible radii rounded down, error constants rounded up); not
formalized.**
Written by Claude (session "Navier Stokes-Speech"), 18 October 2026, on main `2b14eeaa`.
It answers one question for the family of [../PROOF.md](../PROOF.md): for ν > 0 and a
finite interval [0, T], how large is

    R_Z(t) := Z(u_b)(t) − Z(U)(t) − b² Z2(t),

the enstrophy error after its quadratic response in b is subtracted, with constants
that can be evaluated? Section 1 extracts the constants of the existing all-time theorem
and names its largest loss. Sections 2–5 prove a finite-time bound at the enstrophy (H¹)
level, which is the level the question lives at. Section 6 evaluates the constants with a
complete numerical error budget ([constants.py](constants.py),
[results/constants.log](results/constants.log)) and compares them with measured values
([check_bounds.py](check_bounds.py)). Section 7 states what is certified, what is a ceiling, the
single estimate that keeps the bound from being usable, and the estimate that any improvement
of the radius still needs.

## 0. Conventions

Torus T³ = (ℝ/2πℤ)³, ⟨·⟩ the normalized average, ‖·‖ the normalized L² norm, all fields real,
divergence-free and mean-zero. Fourier coefficients are normalized, so ‖f‖² = Σ_k |f̂_k|²,
‖∇f‖² = Σ |k|²|f̂_k|², ‖Δf‖² = Σ |k|⁴|f̂_k|². Poincaré: ‖∇f‖ ≥ ‖f‖ and ‖Δf‖ ≥ ‖∇f‖ (|k| ≥ 1).
P is the Leray projector, B(f,g) = P[(f·∇)g]. For a z-independent field a bar denotes the
z-average (the k_z = 0 modes) and a tilde the rest: f = f̄ + f̃, orthogonal in every H^s.

Family: u₀ = (a sin y, b sin z, c cos x − d cos(x+y+φ)), ν > 0, (a, c, d) fixed reals with
(H) |c| + |d| ≥ ν. (Used once, to drop a factor e^{−Φ₁}; it holds at the tested parameters.)
Base flow (b = 0): U = (σ, 0, w), σ(y,t) = a e^{−νt} sin y, w_t + σ w_x = νΔw,
w(0) = c cos x − d cos(x+y+φ). Perturbation data f := sin z e_y, with
F₀ := ‖f‖ = 2^{−1/2}, F₁ := ‖∇f‖ = 2^{−1/2}.
Coefficients (as in PROOF.md §3, q₂ is the b² Taylor coefficient, half the second b-derivative):
L_U q₁ = 0, q₁(0) = f; L_U q₂ = −B(q₁,q₁), q₂(0) = 0, where L_U h = h_t − νΔh + B(U,h) + B(h,U).
q₁ lives on k_z = ±1, q₂ on k_z ∈ {0, ±2} (L_U preserves k_z because U is z-independent).
Z(u) = ½‖curl u‖² = ½‖∇u‖², Z2 = ⟨curl U, curl q₂⟩ + ½‖curl q₁‖².

Agmon constant: for mean-zero f, ‖f‖_∞ ≤ Σ_k |f̂_k| ≤ C_A ‖Δf‖ with
C_A² := Λ₄ := Σ_{k∈ℤ³∖0} |k|^{−4}, certified in [results/lattice_sums.log](results/lattice_sums.log).

## 1. The existing theorem's constants and its largest loss

PROOF.md §2 certifies all-time smoothness and ‖u_b − U‖_s ≤ 2|b|F_s e^{A∞} e^{−νt} for

    |b| ≤ β_s := ν e^{−A∞} / (2 K_s F_s),   A∞ = K_s ∫₀^∞ M_s dt,   M_s = sup_φ ‖U‖_{s+1},

with s ≥ 4, F_s = 2^{(s−1)/2}, K_s the H^s energy constant. Three facts fix the scale:
K₄ ≥ 0.3977 from a single test pair ([../review/radius_ceiling.py](../review/radius_ceiling.py));
the shear part alone gives ∫M₄ ≥ 2²|a|/ν = 112 at a = 1, ν = 1/28, hence the ceiling
β₄ ≤ 7.2×10⁻²² whatever the other constants are; and a numerically computed base integral
∫₀^∞ M₄ ≈ 2.7×10³ (one-dimensional solve of W; not certified and not in this repository —
the ceiling itself uses only the shear part) would give β₄ ≤ 10^{−460}.

Where the loss comes from, in decreasing order:
1. **The Sobolev level.** The H^s energy method needs ‖U‖_{s+1} with s ≥ 4, i.e. five
   derivatives of the base flow. The shear tilts the base modes to wavenumbers k_y ~ a t
   before viscosity removes them, and the H⁵ norm weights that by (1+|k|²)^{5/2}: the
   integral is 2.66×10³ at s = 4 against ∫₀^∞ sup|∇U| of order 10¹–10². For the enstrophy
   error only first and second derivatives of U are needed (Section 2), so this loss is
   avoidable for the question asked here.
2. **Exponentiating a sup-norm bound.** Every transport and stretching term is bounded by
   sup|∇U| times the norm squared and then integrated into a Grönwall exponent. The true
   linearized propagator grows far less (Section 6 measures it). This loss is intrinsic to
   energy methods with explicit constants and is the one that remains below.
3. **The all-time integral.** For a bound on [0, T] only ∫₀^T enters.

The bound below removes losses 1 and 3 and keeps loss 2.

## 2. The base flow: derivative bounds without Sobolev constants

Let X solve X_t + σ X_x − νΔX = F on the torus with smooth periodic data. The drift σ e_x is
divergence-free, so the maximum principle gives ‖X(t)‖_∞ ≤ ‖X(0)‖_∞ + ∫₀ᵗ ‖F(s)‖_∞ ds.
Differentiating the w equation (σ does not depend on x) and writing γ := |c| + |d|,
α(t) := |a| e^{−νt}, E₁(t) := (1 − e^{−νt})/ν, E₂(t) := (1 − e^{−2νt})/(2ν):

| derivative | equation | sup bound |
|---|---|---|
| w_x, w_xx | F = 0 | γ |
| w_y, w_xy | F = −σ_y w_x resp. −σ_y w_xx | γ₁(t) := \|d\| + \|a\| γ E₁(t) |
| w_yy | F = −2σ_y w_xy − σ_yy w_x | γ₂(t) := \|d\| + \|a\|γE₁ + 2\|a\|\|d\|E₁ + (2a²γ/ν)(E₁ − E₂) |
| σ_y, σ_yy | explicit | α(t) |

(Initial sups: |w_x(0)|, |w_xx(0)| ≤ |c| + |d|; |w_y(0)|, |w_xy(0)|, |w_yy(0)| ≤ |d|.)
Hence, with Frobenius norms pointwise in x,

    |∇U| ≤ m₁(t) := (α² + γ² + γ₁²)^{1/2},
    |∇²U| ≤ m₂(t) := (α² + γ² + 2γ₁² + γ₂²)^{1/2},
    ‖ΔU‖ ≤ m_Δ(t) := (a² + (γ + γ₂)²)^{1/2}.

(ΔU = (σ_yy, 0, w_xx + w_yy); in m_Δ the decreasing factor α is replaced by |a| so that m_Δ,
like m₁ and m₂ in the sense used below, is nondecreasing in t, which Section 5 relies on when it
states a uniform bound on [0, T].) These are the only properties of U used below.

Five inequalities, for smooth divergence-free mean-zero X, Y, Z (sums over repeated indices):

- (I1) ⟨(U·∇)X, X⟩ = 0 and ⟨(X·∇)Y, Y⟩ = 0.
- (I2) |⟨(X·∇)U, X⟩| ≤ m₁ ‖X‖².
- (I3) |⟨(U·∇)X, ΔX⟩| ≤ m₁ ‖∇X‖². Proof: integrate by parts once;
  ⟨(U·∇)∂_jX, ∂_jX⟩ = 0 by (I1), and the remaining term is
  −Σ_{i,j,k} ⟨(∂_jU_k)(∂_kX_i)(∂_jX_i)⟩ = −Σ_i ⟨(∇X_i)ᵀ(∇U)(∇X_i)⟩, bounded pointwise by |∇U|·|∇X|²
  (operator norm ≤ Frobenius norm).
- (I4) |⟨(X·∇)U, ΔX⟩| ≤ m₁‖∇X‖² + m₂‖X‖‖∇X‖. Proof: integrate by parts; the two terms are
  Σ_{i,j,k}(∂_jX_k)(∂_kU_i)(∂_jX_i) ≤ |∇U||∇X|² and Σ X_k (∂_j∂_kU_i)(∂_jX_i) ≤ |X||∇²U||∇X|.
- (I5) ‖(X·∇)Y‖ ≤ ‖X‖_∞‖∇Y‖ ≤ C_A‖ΔX‖‖∇Y‖, and |⟨(X·∇)Y, ΔZ⟩| ≤ C_A‖ΔX‖‖∇Y‖‖ΔZ‖.
- (I6) ‖P S‖ ≤ ‖S‖; ⟨P S, Z⟩ = ⟨S, Z⟩ and ⟨P S, ΔZ⟩ = ⟨S, ΔZ⟩ for divergence-free Z.

Exponents used throughout (all nondecreasing under (H)):
Φ₁(t) := ∫₀ᵗ (m₁ − ν), Ψ(t) := ∫₀ᵗ (2m₁ − ν/2), Θ(t) := ∫₀ᵗ (4m₁ + 1).

## 3. The perturbation v = u_b − U: L², H¹, and the certified radius

v solves v_t − νΔv + B(U,v) + B(v,U) + B(v,v) = 0, v(0) = b f.

**Lemma 1 (L²).** ½ d/dt‖v‖² + ν‖∇v‖² = −⟨(v·∇)U, v⟩ ≤ m₁‖v‖² (by (I1), (I2), (I6)); with
Poincaré, ‖v(t)‖ ≤ |b| F₀ e^{Φ₁(t)} for as long as the smooth solution exists. No smallness.

**Lemma 2 (H¹ with bootstrap).** Pairing with −Δv and using (I3)–(I6),

    ½ d/dt ‖∇v‖² + ν‖Δv‖² ≤ 2m₁‖∇v‖² + m₂‖v‖‖∇v‖ + C_A ‖∇v‖ ‖Δv‖².

On any interval where C_A‖∇v‖ ≤ ν/2, the last term is absorbed and, with ‖Δv‖ ≥ ‖∇v‖ and
z := ‖∇v‖, the upper Dini derivative satisfies z′ ≤ (2m₁ − ν/2) z + m₂‖v‖, whence

    ‖∇v(t)‖ ≤ |b| G₁(t),   G₁(t) := e^{Ψ(t)} [ F₁ + F₀ ∫₀ᵗ m₂(s) e^{Φ₁(s) − Ψ(s)} ds ],

and, integrating the inequality with (ν/2)‖Δv‖² kept,

    ∫₀ᵗ ‖Δv‖² ≤ b² D₁(t),   D₁(t) := (2/ν) [ ½F₁² + ∫₀ᵗ ( 2m₁G₁² + m₂ F₀ e^{Φ₁} G₁ ) ].

**Proposition 1 (finite-time radius).** Let T > 0 and

    β₁(T) := ν / ( 2 C_A G₁(T) ).

If |b| < β₁(T), the solution u_b is smooth on [0, T] and Lemmas 1–2 hold on [0, T].
Proof. Let [0, T_max) be the maximal interval of the smooth solution and T′ := min(T, T_max).
C_A‖∇v(0)‖ = C_A|b|F₁ < ν/2. Let t* be the supremum of times < T′ up to which
C_A‖∇v‖ ≤ ν/2; on [0, t*] Lemma 2 gives C_A‖∇v‖ ≤ C_A|b|G₁(T) < ν/2, so by continuity
t* = T′ and ‖∇v‖ ≤ |b|G₁(T) on [0, T′). If T_max ≤ T this bounds ‖∇u_b‖ up to T_max, which
the enstrophy continuation criterion for 3D Navier–Stokes forbids (Temam, *Navier–Stokes
Equations*, Ch. III, Thm 3.10 and Rem. 3.7; Constantin–Foias, *Navier–Stokes Equations*,
Ch. 10); hence T_max > T and the bounds hold on [0, T]. ∎

β₁ is a certified admissible radius for the finite interval, not a ceiling on a sufficient
condition: every |b| below it is covered. The inequality |b| < β₁(T) is strict, and the evaluated
radii of Section 6 are rounded down, so every printed radius is itself admissible.

**Lemma 3 (the linear coefficients).** q₁ obeys the same inequalities without the cubic term,
so ‖q₁‖ ≤ F₀e^{Φ₁}, ‖∇q₁‖ ≤ G₁, ∫₀ᵗ‖Δq₁‖² ≤ D₁ (the b = 1 versions). For q₂, with source
s₂ := (q₁·∇)q₁, ‖s₂‖ ≤ C_A G₁ ‖Δq₁‖ (I5):

    ‖q₂(t)‖ ≤ N₂(t) := e^{Φ₁(t)} C_A G₁(t) (t D₁(t))^{1/2},
    ‖∇q₂(t)‖² ≤ Q₂(t)² := e^{Θ(t)} [ ∫₀ᵗ m₂² N₂² + C_A² G₁(t)² D₁(t)/ν ],
    ∫₀ᵗ ‖Δq₂‖² ≤ D₂(t) := (2/ν) [ ∫₀ᵗ ( (2m₁+½) Q₂² + ½ m₂² N₂² ) + C_A² G₁² D₁ /(2ν) ].

(L²: d/dt‖q₂‖ ≤ (m₁−ν)‖q₂‖ + ‖s₂‖, Cauchy–Schwarz on ∫‖Δq₁‖, and e^{−Φ₁(s)} ≤ 1 by (H).
H¹: ½y′ + ν‖Δq₂‖² ≤ 2m₁y + m₂‖q₂‖√y + ‖s₂‖‖Δq₂‖, then m₂‖q₂‖√y ≤ ½m₂²‖q₂‖² + ½y and
‖s₂‖‖Δq₂‖ ≤ (ν/2)‖Δq₂‖² + ‖s₂‖²/(2ν), so y′ ≤ (4m₁+1)y + m₂²‖q₂‖² + ‖s₂‖²/ν.)
Both the mean and the oscillating part of q₂ obey the same bounds (orthogonal projections).

## 4. Mean and oscillating parts; the remainders

Because U is z-independent, z-averaging commutes with L_U and with P, and for the quadratic
term ((v·∇)v)‾ = (v̄·∇)v̄ + ((ṽ·∇)ṽ)‾ while ((v·∇)v)~ = (v̄·∇)ṽ + (ṽ·∇)v̄ + ((ṽ·∇)ṽ)~.
All estimates below are on [0, T] with |b| < β₁(T), so that C_A‖∇v̄‖ ≤ C_A‖∇v‖ ≤ ν/2 and
‖∇ṽ‖ ≤ ‖∇v‖ ≤ |b|G₁, ∫‖Δṽ‖² ≤ ∫‖Δv‖² ≤ b²D₁. Each of the following is the generic
estimate for X_t − νΔX + B(U,X) + B(X,U) [+ B(X,X)] = −P S, X(0) = 0:

    ‖X(t)‖ ≤ e^{Φ₁(t)} ∫₀ᵗ ‖S‖,
    ‖∇X(t)‖² ≤ e^{Θ(t)} [ ∫₀ᵗ m₂² ‖X‖² + (c_S/ν) ∫₀ᵗ ‖S‖² ],      (c_S = 1 linear, 2 with B(X,X))
    ∫₀ᵗ ‖ΔX‖² ≤ (c_D/ν) [ ∫₀ᵗ ( (2m₁+½)‖∇X‖² + ½m₂²‖X‖² ) + (c_S/(2ν)) ∫₀ᵗ ‖S‖² ],   (c_D = 2 linear, 4 with B(X,X))

the cubic case being absorbed by the bootstrap exactly as in Lemma 2.

**Lemma 4 (mean part v̄).** v̄_t − νΔv̄ + B(U,v̄) + B(v̄,U) + B(v̄,v̄) = −P[((ṽ·∇)ṽ)‾], v̄(0) = 0,
and ‖((ṽ·∇)ṽ)‾‖ ≤ C_A‖Δṽ‖‖∇ṽ‖ ≤ C_A |b| G₁ ‖Δv‖. Therefore

    ‖v̄(t)‖ ≤ b² N̄(t),  N̄ := e^{Φ₁} C_A G₁ (t D₁)^{1/2};
    ‖∇v̄(t)‖ ≤ b² V̄(t),  V̄² := e^{Θ} [ ∫₀ᵗ m₂² N̄² + 2 C_A² G₁² D₁/ν ];
    ∫₀ᵗ ‖Δv̄‖² ≤ b⁴ D̄(t),  D̄ := (4/ν) [ ∫₀ᵗ ( (2m₁+½) V̄² + ½ m₂² N̄² ) + C_A² G₁² D₁/ν ].

**Lemma 5 (oscillating remainder r̃ := ṽ − b q₁).** r̃ solves the linear equation with
S_r = (v̄·∇)ṽ + (ṽ·∇)v̄ + ((ṽ·∇)ṽ)~, r̃(0) = 0, and by (I5)
‖S_r‖ ≤ C_A [ |b|G₁‖Δv̄‖ + b²V̄‖Δv‖ + |b|G₁‖Δv‖ ]. With |b| ≤ β₁ := β₁(T):

    ‖r̃(t)‖ ≤ b² N_r(t),   N_r := e^{Φ₁} C_A t^{1/2} [ G₁ D₁^{1/2} + β₁ ( G₁ D̄^{1/2} + V̄ D₁^{1/2} ) ];
    ‖∇r̃(t)‖ ≤ b² R₁(t),   R₁² := e^{Θ} [ ∫₀ᵗ m₂² N_r² + (3C_A²/ν) S_r* ],  S_r* := G₁²D₁ + β₁²(G₁²D̄ + V̄²D₁);
    ∫₀ᵗ ‖Δr̃‖² ≤ b⁴ D_r(t),  D_r := (2/ν) [ ∫₀ᵗ ( (2m₁+½) R₁² + ½ m₂² N_r² ) + (3C_A²/(2ν)) S_r* ].

(∫‖S_r‖² ≤ 3C_A²[b²G₁²∫‖Δv̄‖² + b⁴V̄²∫‖Δv‖² + b²G₁²∫‖Δv‖²] ≤ 3C_A² b⁴ S_r*.)

**Lemma 6 (oscillating second-order remainder ẽ₂ := ṽ − b q₁ − b² q̃₂ = r̃ − b² q̃₂).**
Since q̃₂ solves the oscillating part of the q₂ equation, ẽ₂ solves the linear equation with
S_e = (v̄·∇)ṽ + (ṽ·∇)v̄ + ((ṽ·∇)ṽ)~ − b²((q₁·∇)q₁)~, and
(ṽ·∇)ṽ − b²(q₁·∇)q₁ = (r̃·∇)ṽ + (b q₁·∇)r̃. Hence
‖S_e‖ ≤ C_A [ |b|G₁‖Δv̄‖ + b²V̄‖Δv‖ + |b|G₁‖Δr̃‖ + |b|³R₁‖Δq₁‖ ], all of order b³, and

    ‖ẽ₂(t)‖ ≤ |b|³ N_e(t),  N_e := e^{Φ₁} C_A t^{1/2} [ G₁D̄^{1/2} + V̄D₁^{1/2} + G₁D_r^{1/2} + R₁D₁^{1/2} ];
    ‖∇ẽ₂(t)‖ ≤ |b|³ Ẽ(t),  Ẽ² := e^{Θ} [ ∫₀ᵗ m₂² N_e² + (4C_A²/ν) S_e* ],  S_e* := G₁²D̄ + V̄²D₁ + G₁²D_r + R₁²D₁;
    ∫₀ᵗ ‖Δẽ₂‖² ≤ b⁶ D_e(t),  D_e := (2/ν) [ ∫₀ᵗ ( (2m₁+½) Ẽ² + ½ m₂² N_e² ) + (2C_A²/ν) S_e* ].

**Lemma 7 (mean second-order remainder ē₂ := v̄ − b² q̄₂, in L²).** Subtracting the mean part
of the q₂ equation from the v̄ equation, ē₂ solves the linear equation with
S̄_e = (v̄·∇)v̄ + ((ṽ·∇)ṽ)‾ − b²((q₁·∇)q₁)‾ = (v̄·∇)v̄ + ((r̃·∇)ṽ)‾ + ((b q₁·∇)r̃)‾.
Insert r̃ = b²q̃₂ + ẽ₂ and ṽ = b q₁ + b²q̃₂ + ẽ₂. The products (q̃₂·∇)q₁ and (q₁·∇)q̃₂ have
k_z ∈ {±1, ±3} and no mean, so the b³ terms vanish and

    S̄_e = (v̄·∇)v̄ + b⁴((q̃₂·∇)q̃₂)‾ + b((ẽ₂·∇)q₁)‾ + b((q₁·∇)ẽ₂)‾ + b²((q̃₂·∇)ẽ₂)‾ + b²((ẽ₂·∇)q̃₂)‾ + ((ẽ₂·∇)ẽ₂)‾,

every term of order b⁴ or smaller. By (I5) and Cauchy–Schwarz in time,

    ‖ē₂(t)‖ ≤ b⁴ Ē(t),
    Ē := e^{Φ₁} C_A t^{1/2} [ V̄D̄^{1/2} + Q₂D₂^{1/2} + G₁D_e^{1/2} + ẼD₁^{1/2} + β₁( ẼD₂^{1/2} + Q₂D_e^{1/2} ) + β₁² ẼD_e^{1/2} ].

(The bounds ‖∇q̃₂‖ ≤ Q₂ and ∫‖Δq̃₂‖² ≤ D₂ are Lemma 3's; ∫‖Δẽ₂‖² ≤ b⁶D_e is Lemma 6's.)

## 5. The enstrophy error

Z(u_b) − Z(U) = ⟨∇U, ∇v⟩ + ½‖∇v‖² = ⟨−ΔU, v̄⟩ + ½‖∇v‖² (U has no k_z ≠ 0 modes), and
b²Z2 = ⟨−ΔU, b²q̄₂⟩ + ½b²‖∇q₁‖². Writing ‖∇v‖² = ‖∇v̄‖² + ‖∇ṽ‖² and expanding
ṽ = b q₁ + b²q̃₂ + ẽ₂, the cross term 2b³⟨∇q₁, ∇q̃₂⟩ vanishes (k_z = ±1 against ±2), so

    R_Z = ⟨−ΔU, ē₂⟩ + ½‖∇v̄‖² + ½b⁴‖∇q̃₂‖² + 2b²·½⟨∇q̃₂,∇ẽ₂⟩ + b⟨∇q₁,∇ẽ₂⟩ + ½‖∇ẽ₂‖².

This identity is exact (the six-term form is checked numerically to rounding in
check_bounds.py, including the vanishing of the cross term). With Lemmas 3–7,
for |b| < β₁(T) and 0 ≤ t ≤ T:

**Theorem.** |R_Z(t)| ≤ C_Z(t) b⁴, with

    C_Z(t) := m_Δ Ē + ½ V̄² + ½ Q₂² + G₁ Ẽ + β₁ Q₂ Ẽ + ½ β₁² Ẽ²        (all evaluated at t),

every factor an explicit function of (a, c, d, ν, t, C_A) through Sections 2–4. The same chain
gives |E(u_b) − E(U) − b²E2| ≤ (m₁-free) analogues, not written out.

Time interval: [0, T] for any T > 0. Norms: normalized L² and H¹ on T³. Parameter range:
ν > 0, (a, c, d) real with (H), |b| < β₁(T) (strict). Coefficient convention: q₂ is the Taylor
coefficient (half the second derivative), Z2 the coefficient of b² in Z, S-free.

## 6. Numbers

[constants.py](constants.py) evaluates every function of Sections 2–5 on a uniform time grid
(n = 20 000 cells) with rigorous upper Riemann sums: on each cell the decreasing factor α is
frozen at its left endpoint and every other factor (all nondecreasing) at its right endpoint,
so each computed quantity is an upper bound of its definition; the gap to the integral is a
slack, not an error. The arithmetic is validated. Every quantity is an interval with decimal
endpoints of 40 digits, computed with directed rounding (floor for lower, ceiling for upper
endpoints); square roots are verified by exact squaring; exponentials come from a Taylor
polynomial with an explicit remainder after argument halving; the cancellations E₁ − E₂ and
1 − e^{−νt} and every nested operation are enclosed automatically; and the maximal relative
width of all enclosures is printed (3×10⁻³¹ in the log). That line is the complete rounding
budget: nothing else in the evaluation is approximate. Printed radii are lower endpoints
rounded down and printed constants are upper endpoints rounded up, so the table below consists
of valid bounds as printed. The script enforces the parameter range on which the argument is
valid, ν > 0, T > 0, a, c, d real with |c| + |d| ≥ ν (hypothesis (H)), and refuses anything
else. C_A is the certified bound of results/lattice_sums.log (C_A ≤ 4.06708, cross-checked
there against an independent built-in bound; threshold ν/(2C_A) ≥ 4.39×10⁻³). At a = c = d = 1
and ν = 1/28 exactly ([results/constants.log](results/constants.log); bounds rounded in their
certified direction to three digits, measured values to two):

| T | m₁(T) | G₁(T) | **β₁(T)** | C_Z(T) | measured ‖∇v‖/\|b\| | measured \|R_Z\|/b⁴ |
|---|---|---|---|---|---|---|
| 0.1 | 2.54 | 1.47 | 2.99×10⁻³ | 4.76×10⁸ | — | — |
| 0.25 | 2.69 | 4.04 | 1.08×10⁻³ | 2.64×10¹² | 0.75 | 6.4×10⁻⁵ |
| 0.5 | 2.99 | 20.8 | 2.11×10⁻⁴ | 5.14×10¹⁹ | 0.88 | 1.0×10⁻³ |
| 1 | 3.71 | 694 | 6.33×10⁻⁶ | 6.02×10³⁸ | 1.40 | 1.0×10⁻² |

The measured columns are from [check_bounds.py](check_bounds.py) (full nonlinear solves at
b = 10⁻², N = 24, dt = 0.005, φ = 0.37, saved every 0.05;
[results/check_bounds.log](results/check_bounds.log)). Every bound of Sections 2–5 is
consistent with its measurement, i.e. exceeds it (Table A: the Section 2 derivative bounds
against certified maxima of the trigonometric polynomials of a fine one-dimensional solve,
ratios 1.02–3.4; Table B: the chain), and the six-term identity of Section 5 holds to 6×10⁻¹⁶.
Three caveats. (i) Which b the theorem covers: b = 10⁻² and 0.05 lie outside every certified
radius (and the absorption hypothesis fails along the b = 10⁻² solve, C_A‖∇v‖ ≈ 3×10⁻²);
b = 10⁻³ lies inside the radius only for T ≤ 0.25 (β₁(0.25) = 1.08×10⁻³) and outside it at
T = 0.5 (β₁ = 2.11×10⁻⁴) and T = 1 (6.33×10⁻⁶). Table B therefore compares the bounds with the
b → 0 limits of the b^k-scaled quantities, which are smooth in b, and b = 10⁻³ cannot be used
for the b⁴-scaled columns (roundoff). (ii) Measurements certify nothing: the solves are N = 24
truncations without error control, and the absorption hypothesis C_A‖∇v‖ ≤ ν/2 observed along
the b = 10⁻³ solve (5.7×10⁻³ ≤ 1.8×10⁻²) is checked only at the 21 saved sample times, not in
between. Where the theorem applies (b = 10⁻³, T ≤ 0.25) the hypothesis is certified by
Proposition 1 on all of [0, T]; where it does not (T = 0.5, 1) the observation is not a
substitute. (iii) A check that passes by factors of 10⁵–10⁴⁰ has no power to detect a
moderate error in a late constant; only the base-flow bounds and G₁ are tested tightly.
Where the chain loses, at T = 0.25 (bound/measured): G₁ 5.4, D₁ 3×10³, Q₂ 3×10⁵,
V̄ 8×10⁵, R₁ 2×10⁶, Ẽ 9×10¹⁰, Ē 1×10¹⁶, C_Z 4×10¹⁶; incrementally, D₁/G₁ ≈ 6×10²,
Q₂/D₁ ≈ 80, V̄/D₁ ≈ 2×10², R₁/V̄ ≈ 3, Ẽ/R₁ ≈ 4×10⁴, Ē/Ẽ ≈ 10⁵.

## 7. What is certified, and the obstruction

- **Certified (for |b| < β₁(T)):** smoothness on [0, T], the Lemma 1–2 bounds on v, and
  |R_Z(t)| ≤ C_Z(t) b⁴ on [0, T], every constant evaluated in validated arithmetic. β₁ is an
  admissible radius, not a ceiling: every b below it is covered. At T = 0.25 it is 1.08×10⁻³,
  more than 10¹⁸ times the ceiling 7.2×10⁻²² that the all-time condition of PROOF.md can
  certify at the same parameters (that figure is a ceiling on a sufficient condition, not a
  covered set).
- **Not usable as a number, and why.** C_Z exceeds the measured remainder by 10¹⁶ at
  T = 0.25 and 10⁴⁰ at T = 1. The loss has two distinct sources, separated in Table C of
  the check log:
  1. *The radius* is limited by the Agmon absorption of the cubic term in Lemma 2,
     C_A‖∇v‖ ≤ ν/2, which caps any radius from this argument at ν/(2C_A F₁) ≤ 6.21×10⁻³
     whatever the base flow does, and is reduced below that by the Grönwall factor
     G₁(T)/F₁ of (I3)–(I4) (5.4× at T = 0.25, 500× at T = 1 against the measured growth).
     Table C evaluates ν/(2C_A·sup‖∇q₁‖) with the measured linear coefficient, 3–6×10⁻³;
     that is the absorption threshold on q₁, not a radius: a radius needs ‖∇v‖ for the full
     perturbation, and v − bq₁ is not bounded there (see the last bullet).
  2. *The constant* is dominated not by the propagator but by the source estimates
     ‖(X·∇)Y‖ ≤ C_A‖ΔX‖‖∇Y‖ followed by Cauchy–Schwarz in time against the dissipation
     integrals D₁, D̄, D_r, D_e, each of which trades a pointwise-small transport velocity
     for ν⁻¹ times a time-integrated H² norm. The incremental losses in Section 6 (6×10² at
     the first dissipation integral, then 80, 2×10², 3, 4×10⁴ and 10⁵ through the chain)
     are all of this kind. With the measured G₁, D₁ inserted into this same majorant, C_Z
     still exceeds the measurement by 10¹¹ (Table C); that figure is a property of this
     majorant with those inputs, not a lower bound on what a different estimate could achieve.
     The source estimate is the precise obstructing estimate.
- **One improvement, and the estimate it still needs.** Certify the linear layer numerically
  instead of bounding it: compute, with validated error control along [0, T] (interval
  arithmetic, or a-posteriori control in the sense of Chernyshenko–Constantin–Robinson–Titi
  2007), the pointwise norms ‖∇q₁‖, ‖Δq₁‖, ‖q₁‖_∞, ‖∇q₂‖, ‖Δq₂‖, ‖q̃₂‖_∞ and the H¹ norm of
  the solution operator of L_U. Validated norms of q₁ alone prove nothing about the radius:
  Proposition 1 needs ‖∇v‖ for the full perturbation, and v = bq₁ + w with the nonlinear
  remainder w := v − bq₁ solving

      L_U w = −B(bq₁ + w, bq₁ + w),   w(0) = 0.

  The missing estimate is a certified bound ‖∇w(t)‖ ≤ b² K(T) on [0, T] for |b| < β, with K(T)
  obtained from a validated solution-operator bound rather than from the Grönwall majorant
  e^{Ψ} (the loss that produced G₁). Given such a K, the absorption
  C_A(|b| sup‖∇q₁‖ + b² K) ≤ ν/2 would yield a radius, necessarily below the absorption
  ceiling ν/(2C_A F₁) ≤ 6.21×10⁻³ of Lemma 2's method; without it, Table C's threshold on q₁
  is not a radius. Whether a validated bound on w can close this at one short horizon, say
  T = 0.25, is open: it is the next question, not a result. For the constant, the source
  bounds built from linear objects (s₂, and the q₁, q̃₂ factors in S̄_e) would lose their
  ν⁻¹·dissipation exchange and those built from the nonlinear pieces v̄, r̃, ẽ₂ would keep it;
  how much of the gap closes is not predicted by Table C, whose residual is specific to the
  present majorant. Moving the whole chain one derivative up does not escape this either: the
  H² estimate pairs a source S with Δ²X and needs ∇S, i.e. ‖∇X‖_∞ of the transporting field
  (one more derivative everywhere), and the ν⁻¹ exchange then multiplies ∫‖∇S‖²; whether that
  is numerically smaller is unknown. A free, small gain not applied here: for the z-independent
  fields v̄, q̄₂, ē₂ the two-dimensional lattice sum of results/lattice_sums.log allows
  C_A = 2.455 instead of 4.067 in Lemmas 4 and 7. Measured growth rates are not continuum
  certificates; everything in this bullet is a proposal, not a result.

Nothing here concerns b = 1, the all-time statement, or regularity in general.
