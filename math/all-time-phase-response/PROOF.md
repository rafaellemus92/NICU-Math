# All-time small-b response on the fixed periodic torus

**Mathematical argument, with symbolic constants.** This is not a numerical
certificate, a Lean proof, or a claim about general 3D regularity. All variables
are nondimensional. The torus is fixed as `(R/2πZ)^3`; averages use `(2π)^−3 dx`.
All fields below are real, divergence-free and mean-zero. Viscosity ν is strictly
positive; a,c,d are any fixed finite real numbers; φ ranges over the entire circle.

Write `||f||_s² = Σ_k (1+|k|²)^s |f̂(k)|²` with normalized Fourier coefficients.
Thus `F_s=||sin(z)e_y||_s=2^((s−1)/2)`. Define
`B(f,g)=P(f·∇g)` and `L_U h = h_t−νΔh+B(U,h)+B(h,U)`.
All constants below are independent of φ, t and the spatial Galerkin cutoff.

## 1. An integrable base norm, analytically

For b=0 the solution is

```
U = (a e^(−νt) sin y, 0, Re(e^(ix) W(y,t))),
W_t = ν(W_yy−W) − i a e^(−νt) sin y W,
W(y,0) = c − d e^(i(y+φ)).
```

These formulas solve the full projected equations: the horizontal component is
a decaying shear, and the vertical velocity is transported linearly by it.
Factoring `W=e^(−νt)V` gives
`V_t=νV_yy−i a e^(−νt)sin(y)V`. For every integer j≥0, differentiation in y,
integration by parts and the bounded derivatives of sin give

```
(1/2) d/dt ||V||_{H^j_y}²
  ≤ C_j |a| e^(−νt) ||V||_{H^j_y}².
```

The diffusion term is nonpositive; multiplication by sin is bounded on H^j,
so no derivative of V beyond j is required. Integration gives
`||V(t)||_{H^j_y} ≤ exp(C_j |a|/ν)||V(0)||_{H^j_y}`.
Equivalence between the one-dimensional weight `(1+k_y²)^j` and the
three-dimensional weight `(2+k_y²)^j` on k_x=±1 yields, after enlarging C_j,

```
sup_φ ||U(t,φ)||_j ≤ L_j e^(−νt),
L_j = C_j (|a| + (|c|+|d|) exp(C_j |a|/ν)).
```

In particular `M_s(t)=sup_φ ||U(t,φ)||_{s+1}` has integral at most
`L_{s+1}/ν`. This uses no sampled phases, time quadrature, or numerical tail.
The constants C_j are finite Sobolev/multiplication constants, not evaluated
numbers. Linear parabolic existence for V, or its Galerkin construction with
these estimates at every j, supplies the smooth base solution for all time.

## 2. A uniform smallness radius

For integer s≥4 choose K_s large enough for the energy inequalities

```
|<B(f,h),h>_s| ≤ K_s ||f||_{s+1} ||h||_s²,
||B(h,f)||_s ≤ K_s ||f||_{s+1} ||h||_s,
|<B(h,h),h>_s| ≤ K_s ||h||_s³.
```

The first and third use the divergence-free transport cancellation and the
commutator after s derivatives; Sobolev embedding controls first derivatives
in L∞. P is an order-zero orthogonal Fourier multiplier commuting with these
derivatives. Increasing K_s absorbs the sum of the two linear estimates.
Poincaré gives `||∇h||_s²≥||h||_s²` since k=0 is absent.
For `v=u_b−U`, `y=||v||_s` consequently obeys, in the upper-Dini sense at y=0,

```
y' ≤ (−ν+K_s M_s)y + K_s y²,        y(0)=|b|F_s.
```

Set `A(t)=K_s∫_0^t M_s`, `A∞=K_s∫_0^∞ M_s < ∞`, and
`h(t)=exp(−νt+A(t))`. Scalar comparison (or differentiating y/h) gives

```
y(t) ≤ y(0) h(t) / (1−K_s y(0)∫_0^t h(τ)dτ).
```

As `∫h≤e^A∞/ν`, the sufficient condition

```
|b| F_s ≤ ν e^(−A∞)/(2K_s)                         (1)
```

makes the denominator at least 1/2 at every time. Therefore

```
||u_b(t,φ)−U(t,φ)||_s ≤ 2 |b| F_s e^A∞ e^(−νt).   (2)
```

Local H^s existence and uniqueness can be obtained by Fourier Galerkin
approximation, these commutator estimates on a short interval, and compactness;
the same estimates for differences give uniqueness. The continuation criterion
is that a finite maximal existence time requires unbounded H^s norm.
The cutoff-independent bound (2) together with the bound on U prevents that.
Smooth initial data retain higher regularity on each finite interval by the
tame higher-order energy estimate with the bounded lower norm. This yields a
unique global smooth solution for this small-b family, uniformly in φ.
No value such as b=0.1, 0.2, 1 or 10^−80 is certified by (1) without constants.

## 3. Coefficient variations and a derivative budget

For the observable remainder use s=R≥8 in (1)–(2). Choose a single K that
dominates the energy constants at all integer levels 4,…,R, including mixed
transport estimates; write `A=K∫ M_R`. Also choose D dominating

```
||B(f,g)||_j ≤ D ||f||_{j+1} ||g||_{j+1},  4≤j≤R−1.
```

This deliberately loses a derivative in each forcing estimate. Define

```
L_U q1 = 0,                         q1(0)=sin(z)e_y,
L_U q2 = −B(q1,q1),                 q2(0)=0,
L_U q3 = −B(q1,q2)−B(q2,q1),        q3(0)=0.
```

These are **coefficients**, not derivatives: `q_j=(∂_b^j u)|_0/j!` when the
parameter derivatives are taken. Finite-time parameter differentiability is
justified by subtracting the equations at two b values and iterating difference
quotients with this derivative budget; smooth initial data permit extra levels
on each compact time interval. The uniform remainder proof below is stronger
than merely asserting finite-time differentiability and does not assume a
uniform fourth derivative at the outset.

The linear forced energy inequality and variation of constants give

```
||q1||_R     ≤ C1 e^(−νt),       C1=e^A F_R,
||q2||_{R−1} ≤ C2 e^(−νt),       C2=e^A D C1²/ν,
||q3||_{R−2} ≤ C3 e^(−νt),       C3=2e^A D C1 C2/ν.             (3)
```

Indeed a source bounded by H e^(−2νt) contributes at most
`e^A H e^(−νt)∫_0^t e^(−ντ)dτ≤e^A H e^(−νt)/ν`.
Linear Galerkin limits provide q_j at their stated regularities; no estimate
of `B(q1,q1)` in H^R from q1 in H^R has been used.

## 4. Uniform field remainder, including its decay

Fix `β=min(1,ν e^(−A)/(2KF_R))`; all following constants are uniform for
`|b|≤β`. Put `V*=2βF_R e^A` and
`Q*=βC1+β²C2+β³C3`. With `T=bq1+b²q2+b³q3`, let `e=v−T`.
Direct subtraction, using
`B(v,v)−B(T,T)=B(v,e)+B(e,T)`, gives the exact equation

```
L_U e + B(v,e)+B(e,T) = −R_T,
e(0)=0,
R_T = b⁴[B(q1,q3)+B(q2,q2)+B(q3,q1)]
    + b⁵[B(q2,q3)+B(q3,q2)] + b⁶ B(q3,q3).
```

At level `ℓ=R−3≥5`, all q_i belong to H^(ℓ+1), so

```
||R_T||_ℓ ≤ H4 |b|⁴ e^(−2νt),
H4 = D(2C1C3+C2²+2βC2C3+β²C3²).
```

In the energy estimate the first argument v transports e and is bounded by
(2); the second mixed term needs T in H^(ℓ+1), supplied by (3). Therefore

```
||e||_ℓ' ≤ [−ν+K(M_R+(V*+Q*)e^(−νt))]||e||_ℓ
            + H4 |b|⁴ e^(−2νt),
||e(t)||_ℓ ≤ C4 |b|⁴ e^(−νt),
C4 = (H4/ν) exp(A+K(V*+Q*)/ν).                         (4)
```

There is no quadratic remainder term: the already controlled exact v is in
the transport coefficient. For the requested second-order truncation,

```
||u_b−U−bq1−b²q2||_{R−3}
   ≤ (C3+βC4)|b|³ e^(−νt).                            (5)
```

One can also obtain (5) in H^(R−2) directly using the degree-three residual of
`bq1+b²q2`, q2 in H^(R−1), and the identical mixed transport estimate.
A cubic field error is generally present; parity does not remove it as a field.

## 5. Observable response and quartic remainder

Let `ω_f=curl f` and define the ordered trilinear form
`T_s(f,g,h)=< (ω_f)_i (ω_g)_j ∂_j h_i >` (sum over i,j).
This T_s is distinct from the truncated field T above. Then

```
E(u)=<u,u>/2,       Z(u)=<ω_u,ω_u>/2,       S(u)=T_s(u,u,u),
E2=<U,q2>+<q1,q1>/2,
Z2=<ω_U,ω_q2>+<ω_q1,ω_q1>/2,
S2=T_s(q2,U,U)+T_s(U,q2,U)+T_s(U,U,q2)
   +T_s(q1,q1,U)+T_s(q1,U,q1)+T_s(U,q1,q1).
```

At t=0 these are `(E2,Z2,S2)=(1/4,1/4,0)`. In particular, multiplying q2 by
2 without changing the formulas is incorrect.

Translation `Jf(x,y,z)=f(x,y,z+π)` fixes U and sends the initial perturbation
to its negative. Uniqueness gives `u_−b=Ju_b`. Recursion gives
`Jq_j=(−1)^j q_j`: q1 has z frequencies ±1, q2 has 0,±2, and q3 has ±1,±3.
Every spatially averaged observable above is J-invariant. Thus the polynomial
`O(U+bq1+b²q2+b³q3)` is **exactly even in b**, with no odd coefficients.
Its constant and quadratic coefficients are O(U) and O2.

For completeness, at ℓ≥5 there are finite constants C_B,C_T with
`|<f,g>|, |<curl f,curl g>| ≤ C_B||f||_ℓ||g||_ℓ` and
`|T_s(f,g,h)|≤C_T||f||_ℓ||g||_ℓ||h||_ℓ`; use L²,L²,L∞ for the last estimate.
Let `d0=L_R, d1=C1, d2=C2, d3=C3`, `H=Σ_{i=0}³ β^i d_i`, and
`H'=H+C4β⁴`. For E or Z take

```
C_obs,2 = (C_B/2) Σ_{0≤i,j≤3, i+j≥4} β^(i+j−4) d_i d_j
          +(C_B/2) C4(H+H').
```

For S take

```
C_obs,3 = C_T Σ_{0≤i,j,k≤3, i+j+k≥4} β^(i+j+k−4) d_i d_j d_k
          + C_T C4 (H'²+H'H+H²).
```

These finite sums also harmlessly bound the zero odd coefficients. Polynomial
expansion, (4), and telescoping the bilinear/trilinear expressions now prove

```
|E(u_b)−E(U)−b²E2|, |Z(u_b)−Z(U)−b²Z2|
    ≤ C_obs,2 |b|⁴ e^(−2νt),
|S(u_b)−S(U)−b²S2| ≤ C_obs,3 |b|⁴ e^(−3νt).          (6)
```

This uses fourth-order **field control after a cubic expansion**. Evenness
alone, or an O(b³) field bound alone, would not prove (6). All constants are
uniform in φ and time. Integrating against a phase sine/cosine transfers these
bounds with at most a factor 2 for nonzero real Fourier coefficients.
The base's linear dependence on `(1,e^(iφ))` in W makes E,Z,S contain only the
constant and first phase harmonics (S reduces to `−<U_y w_x w_y>`). This does
not truncate the phase spectrum of the b² response or of the full solution.

## Scope of the conclusion

Equations (1)–(6) are an analytic sufficient condition and response bounds,
with deliberately conservative symbolic constants. They do not estimate the
optimal admissible radius. No computed radius is certified here. The stored
simulations test finite Fourier systems over a short interval, not (1).
No assertion of convergence of a time Taylor series at a late time is needed.

## Appendix: cross-check against the parent derivation

The parent supplied an independently audited derivation after the initial local
commit. Its logistic condition, coefficient equations, derivative budget,
residual factorization and decay powers agree with sections 2–5 above. The
following explicit Fourier base bound is adopted from that derivation after
checking the shift inequality; the original proof and constants remain intact.

Put m=R+1 and `||W||_{*,m}²=Σ_n (2+n²)^m |W_n|²`. Since
`2+(n±1)²≤2(2+n²)`, each Fourier shift has norm at most `L=2^(m/2)`.
Multiplication by sin y, the difference of the shifts divided by 2i, has norm
at most L. For `V=e^(νt)W`, heat is dissipative in this norm, and hence

```
||W(t)||_{*,m} ≤ e^(−νt)
  exp((L|a|/ν)(1−e^(−νt))) sqrt(2^m c²+3^m d²),
||U(t)||_m² = [2^m a²e^(−2νt)+||W(t)||_{*,m}²]/2.
```

Thus an explicit phase-uniform majorant is

```
C_base² = [2^m a²+exp(2L|a|/ν)(2^m c²+3^m d²)]/2,
M_R(t) ≤ C_base e^(−νt),       A ≤ K C_base/ν.
```

The remaining energy/product constant K is still symbolic. This is not a
certified numerical threshold. One may use the last upper bound in every
exponential constant instead of the exact integral A.

The parent alternatively bounds the lower-order base norm by
`D0=e^A sqrt(2^(R−1)(a²+c²)+3^R d²/2)`; this follows from its energy inequality.
Our `L_R` is an independent, coarser base majorant, so there is no contradiction.
The parent's explicit observable constants sum only surviving even polynomial
terms, while ours also harmlessly bound zero odd terms. Neither requires a
numerically evaluated Sobolev constant.

The trilinear conventions differ and must not be silently interchanged.
Our ordered form is `T_s(p,h,q)=<curl p · (grad q) curl h>`.
The parent's final outer-slot-symmetric form is
`T_parent(p,q,h)=<curl p · D(q) curl h>`, with `D(q)` symmetric strain. They obey

```
T_parent(p,q,h) = [T_s(p,h,q)+T_s(h,p,q)]/2.
```

Their full symmetrizations agree, as do S(u) and the six-term S2 coefficient.
The earlier parent message placed strain in the third slot; its final version
places strain in the middle slot and correspondingly permutes its compressed
S2 formula. Our explicit ordered-slot implementation does not require a change.

Numerically, q3 is **not implemented**. The q3 and quartic field remainder in
this note are analytic statements; the measured field residual subtracts only
U+bq1+b²q2 and therefore has cubic scaling. Observable quartic scaling is checked
separately, as documented in README.md.
