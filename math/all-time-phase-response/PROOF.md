# All-time small-b response on the fixed periodic torus

**Mathematical argument, with symbolic constants.** This is not a numerical
certificate, a Lean proof, or a claim about general 3D regularity. All variables
are nondimensional. The torus is fixed as `(R/2πZ)^3`; averages use `(2π)^−3 dx`.
All fields below are real, divergence-free and mean-zero. Viscosity ν is strictly
positive; a,c,d are any fixed finite real numbers; φ ranges over the entire circle.

Write `||f||_s² = Σ_k (1+|k|²)^s |f̂(k)|²` with normalized Fourier coefficients.
Thus `F_s=||sin(z)e_y||_s=2^((s−1)/2)`. Define
`B(f,g)=P(f·∇g)` and `L_U h = h_t−νΔh+B(U,h)+B(h,U)`.
All constants below are independent of φ and t, and no Galerkin cutoff enters
them, because they come from a priori estimates for the smooth solution. The
Sobolev constants C_j, K_s, K, D, C_B, C_T depend only on the regularity index;
L_j, A∞, A, C1–C4, β and C_obs also depend on a, c, d and ν, through factors
such as exp(C|a|/ν), e^(±A∞) and e^(±A).

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
The three inequalities are the Kato–Ponce commutator estimates [KP88] combined
with Sobolev embedding. They are stated with room to spare: they already hold
for s≥3, but section 2 keeps s≥4, and every radius figure below (and in the
cross-links) is for s≥4. At s=3 the same bound below gives a ceiling of
3.1×10^−18, still more than 10^16 below the simulated b. The first needs only
`||f||_s` (with f=h this is the third); the second genuinely needs
`||f||_{s+1}`. The test pair `f=sin(y)e_x`, `h=sin(z)e_y` in the second
inequality gives `K_s ≥ (√3/2)^s/√2`, so K_4 ≥ 0.3977 (used below; checked
with exact Fourier norms in [review/radius_ceiling.py](review/radius_ceiling.py)).
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
The a priori bound (2) together with the bound on U prevents that. (In a
Galerkin construction, measure `v_N=u_b^N−U_N` from the Galerkin base U_N,
which obeys the same base majorant because truncation is an orthogonal Fourier
multiplier.)
Smooth initial data retain higher regularity on each finite interval by the
tame higher-order energy estimate with the bounded lower norm. This yields a
unique global smooth solution for this small-b family, uniformly in φ.
No value such as b=0.1, 0.2, 1 or 10^−80 is certified by (1) without constants.

**How small the radius in (1) is.** The largest |b| that (1) certifies is
`ν e^(−K_s∫M_s)/(2K_s F_s)`. This decreases in K_s and in ∫M_s, so lower
bounds on those two give a ceiling on the radius that holds whatever values
the uncomputed constants take. At a=c=d=1, ν=1/28 (the pilot's parameters) and
s=4: K_4 ≥ 0.3977 (above), and the shear part `a e^(−νt) sin(y) e_x` of U alone
gives `∫M_4 ≥ |a|2^(s/2)/ν = 112`, so (1) certifies no |b| above 7.2×10^−22.
Larger s gives smaller ceilings, and the radius β of section 4 (R≥8) obeys a
smaller one still. The b used in the stored simulations (0.05, 0.1) are
therefore more than 10^19 times larger than any b this argument covers with
s≥4. The scale comes from exp(K∫M), which grows with |a|/ν. The computation,
with these assumptions, is [review/radius_ceiling.py](review/radius_ceiling.py)
([log](review/radius_ceiling.log)).

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

These are **coefficients**, not derivatives. Sections 3–5 never differentiate
in b: section 3 builds the q_j from these linear equations and sections 4–5
bound the remainders directly, which identifies the q_j as Taylor coefficients
of b ↦ u_b. That this map is in fact real-analytic, with
`q_j=(∂_b^j u)|_0/j!`, is the standard analytic dependence of strong solutions
on their initial data (Picard iteration for the Duhamel form in the
e^(νt)-weighted space around U); it is not used below.

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
constant and first phase harmonics. (Write the base as `(σ,0,w)` with shear
profile `σ(y,t)=a e^(−νt) sin y`; then S reduces to `−<σ_y w_x w_y>`.) This is
P1 of [AUDIT.md](../ns-phase-audit/audit_v2/AUDIT.md) §4.2 and the
passive-scalar lemma of
[enstrophy-jet/RESULTS.md](../ns-phase-audit/enstrophy-jet/RESULTS.md) §4.2,
here for E, Z and S at the solution level and for all t. It does not truncate
the phase spectrum of the b² response or of the full solution. Wavevector
counting (AUDIT.md §4.2 P2; RESULTS.md §4.2 Rule B, both stated for Z, where an
L-leaf term of [t^n]Z carries ν^(n+2−L); for the cubic S an L-leaf term of
[t^n]S carries ν^(n+3−L), E′=−2νZ puts E one order after Z with a factor ν,
and each further pair of sin z leaves adds two orders) shows that an |m|≥2
harmonic cannot enter the time-Taylor coefficients of the b² response before
t^(3|m|) in Z2, t^(3|m|−1) in S2 and t^(3|m|+1) in E2 (where it carries a
factor ν), and cannot enter the b⁴ terms before two orders later. The exact
series confirms these onsets wherever it reaches (E and Z through t^10, S
through t^9; [review/exact_b2_check.log](review/exact_b2_check.log), item 5). Whether every
harmonic actually occurs is not proved.

## Scope of the conclusion

Equations (1)–(6) are an analytic sufficient condition and response bounds,
with deliberately conservative symbolic constants. They do not estimate the
optimal admissible radius. No computed radius is certified here. The stored
simulations test finite Fourier systems over a short interval, not (1).
No assertion of convergence of a time Taylor series at a late time is needed.
The stored simulations stop at T=0.5, where νT≈0.018 and e^(−2νT)≈0.965, so
they do not test the decay rates either.

## What this is not, and where it sits

- **Not about b=1**, the family the repository audits
  ([../ns-phase-audit/](../ns-phase-audit/)), nor about the b of the stored
  simulations: section 2 puts every b this argument covers below 7.2×10^−22 at
  the tested parameters. Reaching b=1 would need a non-perturbative method, for
  example validated a-posteriori numerics along the b=1 trajectory
  ([AUDIT.md](../ns-phase-audit/audit_v2/AUDIT.md) §7.1) followed by
  small-data theory once the flow has decayed. Even that would cover one data
  family, not the general question.
- **Not about statement (B) of the Millennium problem** (global smoothness
  of unforced periodic flows, still open), nor about blow-up; see
  [enstrophy-jet/RESULTS.md](../ns-phase-audit/enstrophy-jet/RESULTS.md) §8.
- **Sections 2–4 are an instance of known results.** The b=0 base does not
  depend on z and has an out-of-plane component u_z besides its in-plane shear
  u_x (a 2D-3C flow; here u_y ≡ 0); such flows are globally smooth. Global
  existence and decay for small 3D perturbations of global decaying strong
  solutions are classical [PRST94, Ga97, If99, GIP03],
  and the b-expansion is the standard analytic dependence on the data. What is
  specific to this note is the explicit phase-uniform base majorant
  (appendix), the b² coefficients E2, Z2, S2 with their values at t=0, and the
  parity bookkeeping under J.

References:

- [PRST94] G. Ponce, R. Racke, T. C. Sideris, E. S. Titi, Comm. Math. Phys.
  159 (1994) 329–341.
- [Ga97] I. Gallagher, Internat. Math. Res. Notices 1997, no. 18, 919–935.
- [If99] D. Iftimie, Bull. Soc. Math. France 127 (1999) 473–517.
- [GIP03] I. Gallagher, D. Iftimie, F. Planchon, Ann. Inst. Fourier 53 (2003)
  1387–1424.
- [KP88] T. Kato, G. Ponce, Comm. Pure Appl. Math. 41 (1988) 891–907.
- Local existence and continuation: A. J. Majda, A. L. Bertozzi, *Vorticity
  and Incompressible Flow* (Cambridge University Press, 2002), chapter 3.

## Appendix: cross-check against the parent derivation

The parent (the session that commissioned this note, most likely the
coordinating ChatGPT session of the same workflow) supplied a derivation after
the initial local commit. The delivery called it independently audited; as far
as the delivery shows, that audit was made within the same workflow, and the
derivation is not refereed. Its logistic condition, coefficient equations,
derivative budget, residual factorization and decay powers agree with sections
2–5 above. The
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
