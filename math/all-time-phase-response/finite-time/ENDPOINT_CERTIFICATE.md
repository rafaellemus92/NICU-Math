# A conditional positive interaction excess at one Navier–Stokes endpoint

## Problem and statement

Consider the unforced incompressible Navier–Stokes equations

\[
 \partial_t u+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0
\]

on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), with real, mean-zero initial data

\[
 u_b(x,y,z,0)=(a\sin y,\ b\sin z,\ c\cos x-d\cos(x+y+\phi)).
\]

All variables are nondimensional. Inner products use normalized measure
\((2\pi)^{-3}dx\); thus \(\|v\|_2^2=\sum_k|\widehat v_k|^2\).
Set \(Z(v)=\frac12\|\nabla v\|_2^2=\frac12\|\operatorname{curl}v\|_2^2\)
for solenoidal periodic fields. Let \(U=u_0\) denote the solution at parameter
\(b=0\), not the initial velocity. It has the form
\(U=(a e^{-\nu t}\sin y,0,h(x,y,t))\), where
\(h_t+a e^{-\nu t}\sin y\,h_x=\nu\Delta_{xy}h\) and
\(h(x,y,0)=c\cos x-d\cos(x+y+\phi)\).

The observable is

\[
 H_b(T)=Z(u_b(T))-Z(U(T))-\frac{b^2}{4}e^{-2\nu T}.
\]

The last term is exactly the enstrophy of the isolated heat evolution
\(b e^{-\nu t}\sin z\,e_y\). It is a reference subtraction, not a claim
that this perturbation evolves independently inside the full solution.

**Conditional endpoint theorem.** Assume the analytic inequalities, validated
input enclosures, smoothness closure and arithmetic hypotheses listed in the
appendix. At
\[
 a=c=d=1,\quad \nu=1/28,\quad\phi=37/100,\quad T=1/4,
 \quad 0<|b|\le\beta=3/1000,
\]
the smooth solutions covered by the inherited closure satisfy
\[
 H_b(T)\ge 0.004804904671503\,b^2>0.
\]
This is a conditional computer-assisted estimate, not a formally verified theorem.
The sufficient scalar comparison, with safely rounded endpoints, is

\[
 J_{2,\mathrm{lo}}\ge0.008200720680466,
 \qquad \beta^2 C_{\mathrm{new}}\le0.003395816008963,
 \qquad J_{2,\mathrm{lo}}-\beta^2C_{\mathrm{new}}
       \ge0.004804904671503>0.                         \tag{1}
\]

## Response identity

Write \(B(v,w)=P[(v\cdot\nabla)w]\) for the Leray-projected nonlinearity and
\(L_Uv=\partial_tv-\nu\Delta v+B(U,v)+B(v,U)\).
The coefficients use the Taylor convention
\(q_1=\partial_bu_b|_{b=0}\), \(q_2=\tfrac12\partial_b^2u_b|_{b=0}\):

\[
 L_Uq_1=0,\ q_1(0)=\sin z\,e_y;\qquad
 L_Uq_2=-B(q_1,q_1),\ q_2(0)=0.
\]

Define \(w=u_b-U-bq_1\), \(r=w-b^2q_2\), and let a bar denote normalized
z-average. Because \(U\) is z-independent, the linearized operator preserves
z modes: \(q_1\) has modes \(\pm1\), and \(q_2\) has modes \(0,\pm2\).
Orthogonality and periodic integration by parts yield the exact identities

\[
 J_2=\tfrac12\|\nabla q_1(T)\|_2^2
       +\langle-\Delta U(T),\bar q_2(T)\rangle-e^{-2\nu T}/4,
 \qquad H_b(T)=b^2J_2+R_Z(T),
\]
\[
 R_Z=\langle-\Delta U,\bar r\rangle
        +b\langle\nabla q_1,\nabla r\rangle
        +\tfrac12\|\nabla w\|_2^2,                    \tag{2}
\]
\[
 L_U\bar r=-b\overline{B(q_1,r)+B(r,q_1)}-\overline{B(w,w)}. \tag{3}
\]
The support argument, rather than scalar evenness alone, justifies (3).
The mean pairing in \(J_2\) need not be positive. Its inherited lower bound
uses a validated norm enclosure, not an assumed favorable sign.

## Divergence-form improvement

Fix a nonzero admissible b and set \(W=w/b^2\). Split \(\bar r/b^4=X+Y\)
by linearity of \(L_U\), with zero initial data for both terms. Take
\[
 L_U X=-P\operatorname{div}\overline{W\otimes W},\qquad
 L_U Y=-b^{-3}\overline{B(q_1,r)+B(r,q_1)}.
\]
These are responses to the actual solution's forcing. The previously bounded
full r controls Y, so this split introduces no circular improvement of r.
The improved term is specifically the quadratic self-source \(B(w,w)\).
The previous derivative-based estimate was available but loose; divergence form
permits use of the smaller L2 norm in place of that gradient factor.

X is solenoidal and z-independent. Pairing its equation with X removes P;
periodicity moves the divergence onto \(\nabla X\). Jensen's inequality for
normalized z-average and the Frobenius tensor norm give
\[
 |\langle-P\operatorname{div}\overline{W\otimes W},X\rangle|
 \le\|\overline{W\otimes W}\|_2\|\nabla X\|_2
 \le\|W\|_2\|W\|_\infty\|\nabla X\|_2.
\]
There is no volume or component factor since \(|W\otimes W|_F=|W|^2\).
Transport by U is skew; stretching is bounded using
\(m_1(t)\ge\|\nabla U(t)\|_\infty\). Young's inequality gives
\[
 \tfrac12(\|X\|_2^2)'+\nu\|\nabla X\|_2^2
 \le m_1\|X\|_2^2+\nu\|\nabla X\|_2^2
       +\frac{\|W\|_2^2\|W\|_\infty^2}{4\nu}.
\]
All viscous dissipation is spent here; no Poincare damping is retained.
Since X(0)=0, Gronwall implies
\[
 \|X(T)\|_2^2\le\frac1{2\nu}\int_0^T
 e^{2\int_s^Tm_1(t)dt}\|W(s)\|_2^2\|W(s)\|_\infty^2\,ds. \tag{4}
\]
The absorption coefficients are \(1/(4\nu)=7\) before doubling and
\(1/(2\nu)=14\) after doubling. No later-cell initial energy is discarded.

On 250 cells of width \(\Delta=1/1000\), inherited envelopes give
\(\|W(s)\|_2\le N_i\) and
\(\int_0^{t_{j+1}}\|W(s)\|_\infty^2ds\le I_j\), uniformly in b.
Set
\[
 f_i=e^{2\Delta\sum_{k\ge i}m_{1,k}}N_i^2,
 \quad\psi_i=\max_{k\ge i} f_k.
\]
The positive-rate propagation includes the source cell. Summation by parts
against true cumulative integrals, then replacement by their upper bounds,
gives
\[
 d_{\rm div}^2:=\frac1{2\nu}
 [\psi_{249}I_{249}+\sum_{i<249}(\psi_i-\psi_{i+1})I_i]
 \ge\|X(T)\|_2^2.                                    \tag{5}
\]
All coefficients multiplying I are nonnegative. In particular, no difference
of cumulative upper bounds is interpreted as cell dissipation.

At the previously selected Fourier weight \(\lambda=10^6\), the evaluated
bounds are \(d_{\rm div}\le158.221110\) and \(\|Y(T)\|_2\le12.344635\).
The former self bound was 603.159427. With inherited
\(G\ge\|\Delta U(T)\|_2\), \(S\ge\|\nabla q_1(T)\|_2\),
\(\|\nabla r(T)\|_2\le |b|^3 E_r\), use the full-precision upper endpoints:
\[
 C_{\rm new}=G(\text{nonself}+\min(d_1,d_2,d_{\rm div}))+S E_r
 \le377.312890.
\]
Dropping only the positive last term in (2) proves
\(R_Z\ge-b^4C_{\rm new}\). Together with the full-precision evaluation
in (1), \(b^2\le\beta^2\) proves the statement. The rounded C alone would
not reproduce every displayed digit of (1); the stored directed endpoints do.

## Dependency and reproduction appendix

Paths below are relative to this finite-time directory. The original certificate
is pinned at [0f258a1](https://github.com/rafaellemus92/NICU-Math/tree/0f258a1add2b9e339d6c28f3599c43c4ad8241c3/math/all-time-phase-response/finite-time).

| Layer | Evidence and role |
| --- | --- |
| Analytic identities | `NOTE.md`, `route-b-dissipation/NOTE.md`, `endpoint-beta003/NOTE.md`: linearized equations, mode supports, energy estimates, (2)–(5). These arguments are inspectable mathematics, not machine-checked proofs. |
| Inherited validated computation | `absorption-b003/results/validated.json`, `chain.json` and `endpoint-sign/results/chain_percell.json`: residual/error enclosures, closure, uniform cellwise bounds. Smoothness over this interval and b-range depends on that closure/Lemma M. |
| Quadratic coefficient | `z2-endpoint/results/endpoint.json`, `source-only-hull/results/full.json`, `endpoint-sign/DERIVATION.md`: endpoint E/G, mean-source enclosure and J2 lower bound. The postprocessor inherits the reviewed J2 total. |
| Remainder bounds | `route-b-dissipation/results/bounds.review.json`, `endpoint-sign/results/tr_remainder.repaired.json`: global cap coefficients, Ahat, full-r estimates and separately named nonself components. Upstream `route-b-tightening/results/time_refinement.final.json` supplies global D_r used in err_grad; the other derivations use `route-b-tightening/NOTE.md` and endpoint-sign A–F. |
| New directed postprocessing | [Pinned check.py](https://github.com/rafaellemus92/NICU-Math/blob/0f258a1add2b9e339d6c28f3599c43c4ad8241c3/math/all-time-phase-response/finite-time/endpoint-beta003/check.py), [candidate.json](https://github.com/rafaellemus92/NICU-Math/blob/0f258a1add2b9e339d6c28f3599c43c4ad8241c3/math/all-time-phase-response/finite-time/endpoint-beta003/results/candidate.json), and `endpoint-beta003/INPUTS.json`: mpmath intervals, source/input hashes and scalar comparison. Current repaired code preserves the comparison. |
| Independent reproduction | [Audit at b03bfa4](https://github.com/rafaellemus92/NICU-Math/tree/b03bfa45ae25d3543d7ecbd3a2361f990d01120f/math/all-time-phase-response/finite-time/independent-checks/endpoint-beta003-0f258a1): different implementation using 40-digit directed Decimal intervals, recomputing the scalar chain from primitive inputs rather than stored totals. It agrees with (1). |
| Empirical implementation checks | Exact toy/mutation tests check source-cell inclusion and Abel algebra. The audit's resolved Fourier-field binary64 checks test normalization, integration-by-parts signs and skew transport; they are not certificates of arbitrary fields or independent PDE evidence. |
| Trusted assumptions | Correct inherited inequalities/closure, Fourier tails and validated bounds; stated IEEE binary64 round-to-nearest, gradual underflow/no-FMA platform model; correct Python/Decimal/mpmath arithmetic. No inherited certificate was revalidated in preparing this note. |

`time_refinement.final.json` remains an upstream arithmetic dependency: its
global D_r enters the stored err_grad bound through endpoint-sign A–F. The
current postprocessor hash-checks this file but does not parse it or read its
fields directly; it consumes err_grad from tr_remainder.repaired.json. Current
output explicitly distinguishes direct inputs from this upstream dependency. Original plans, inputs,
outputs and SHA256SUMS remain historical records tied to their source commits.

To reproduce the repaired postprocessor and focused tests, from
`endpoint-beta003/`, use an unused output destination:

```sh
python -B check.py /tmp/unused-endpoint-result.json
python -B test_check.py -v
```

The independent reviewer reported approximately six seconds total for its
bounded audit; the published scalar log records 1.4 seconds for that component.
It inspected but did not run the original mpmath script/tests, and did not
revalidate inherited certificates. Its Decimal calculation and Fourier checks
are AI audit artifacts, not human refereeing or formal verification. See
[repair/reproduction record](endpoint-beta003/AUDIT_REPAIRS.md) for exact scope,
fresh outputs and mutation evidence.

This conclusion is only at T=1/4 and the fixed phase/parameters. It implies
neither monotonic enstrophy growth nor positive interaction excess at every
intermediate time. At b=0, H_b=0. It does not extend the amplitude interval,
prove general three-dimensional regularity, establish novelty, or constitute
clinical evidence. In particular, H_b(T)>0 does not imply
Z(u_b(T))>Z(u_b(0)): comparison to a base flow plus isolated heat decay is
different from absolute enstrophy growth.

## Related work

This note uses established a posteriori validation principles with a
problem-specific perturbative remainder estimate to certify a quantified
positive enstrophy excess at a fixed time uniformly over a continuous amplitude
interval. Chernyshenko et al. [1] develop robustness/a posteriori regularity
criteria from computations; Morosi–Pizzocchero [2] develop residual/error control
for periodic, zero-mean solenoidal Sobolev solutions. Neither supplies this
signed comparison. Illustrative numerical examples in such a framework are
not automatically interval-certified.

The enstrophy-optimization literature asks different questions: Lu–Doering [3]
study instantaneous variational optimization and numerical cubic scaling;
Ayala–Protas [4] study instantaneous extrema and their evolution;
Kang–Yun–Protas [5] numerically optimize terminal enstrophy over finite times
using adjoints, obtaining local maximizers rather than universal upper bounds.
These are not certificates of this fixed-family baseline comparison. This is
a bounded context check, not an exhaustive novelty search or a priority claim.

1. S. I. Chernyshenko, P. Constantin, J. C. Robinson and E. S. Titi,
   “A posteriori regularity of the three-dimensional Navier–Stokes equations
   from numerical computations,” *J. Math. Phys.* **48** (2007), 065204.
   [Primary manuscript](https://arxiv.org/abs/math/0607181).
2. C. Morosi and L. Pizzocchero, “On approximate solutions of the incompressible
   Euler and Navier–Stokes equations,” *Nonlinear Analysis* **75** (2012),
   2209–2235. [DOI](https://doi.org/10.1016/j.na.2011.10.020);
   [primary manuscript](https://arxiv.org/abs/1104.3832).
3. L. Lu and C. R. Doering, “Limits on Enstrophy Growth for Solutions of the
   Three-dimensional Navier-Stokes Equations,” *Indiana Univ. Math. J.*
   **57**(6) (2008), 2693–2727. [DOI](https://doi.org/10.1512/iumj.2008.57.3716).
4. D. Ayala and B. Protas, “Extreme vortex states and the growth of enstrophy
   in three-dimensional incompressible flows,” *J. Fluid Mech.* **818** (2017),
   772–806. [DOI](https://doi.org/10.1017/jfm.2017.136);
   [primary manuscript](https://arxiv.org/abs/1605.05742).
5. D. Kang, D. Yun and B. Protas, “Maximum amplification of enstrophy in
   three-dimensional Navier–Stokes flows,” *J. Fluid Mech.* **893** (2020), A22.
   [DOI](https://doi.org/10.1017/jfm.2020.204);
   [primary manuscript](https://arxiv.org/abs/1909.00041).
