# Divergence-form mean self-interaction at the fixed endpoint

Owner Codex, base `6757dcb7655387a09666c7928c0099516188ee38`.
This is a small analytic postprocessor of committed bounds, not a new PDE
simulation. The candidate resolves the fixed sufficient comparison conditional
on inherited certificates. One focused independent AI review found no blocking defect; see [REVIEW.md](REVIEW.md).
No general Navier–Stokes regularity, novelty or clinical claim is made.

## Exact inequality and scope

Fix a=c=d=1, nu=1/28, phi=37/100, T=1/4 and beta=3/1000. Use the
normalized 2pi-torus norm and Z(u)=||grad u||²/2. The target is
H_b(T)=Z(u_b(T))-Z(U(T))-b²exp(-2nu T)/4. Definitions q1,q2,w,r,
L_U and z-average are those of the inherited Route B note. For every nonzero
|b|<=beta, smoothness and envelopes follow from the inherited absorption
closure and its Lemma M, not from this computation.

The exact mean equation is

    L_U bar(r) = -b overline[B(q1,r)+B(r,q1)] - overline[B(w,w)].

For each fixed b, regard the actual right side as prescribed forcing and use
linearity to split bar(r)/b⁴ into nonself and self responses. This does not
assume r is independent of its forcing: the already proved bounds on the
actual r supply the nonself estimate. The old bounds for the three named
nonself contributions, full-r gradient E_r and q1 gradient S are unchanged.

Set W=w/b². Its self response X has zero initial state and satisfies

    L_U X = -P div overline(W tensor W).

Solenoidality gives the divergence identity. The tensor is indexed so that
its divergence is (W.grad)W. Projection and z-averaging commute with derivatives.
Pairing with the z-independent solenoidal X removes P; periodic integration
by parts moves the derivative onto X. With normalized averages, Jensen and
Cauchy–Schwarz give

    ||overline(W tensor W)||_L2(x,y) <= ||W tensor W||_L2(x,y,z)
                                    <= ||W||_infty ||W||_L2.

There is no volume or component factor: the Frobenius norm of W tensor W is
|W|². Transport by U is skew in this pairing, and stretching is bounded by
m1(t)||X||², where m1 bounds ||grad U||_infty. Thus

    (1/2)(||X||²)' + nu||grad X||²
      <= m1||X||² + ||W|| ||W||_infty ||grad X||
      <= m1||X||² + nu||grad X||² + ||W||²||W||_infty²/(4nu).

The last step is the exact square inequality
nu(g-a/(2nu))²>=0. It spends all dissipation, so no negative Poincare growth
term is retained. Gronwall with X(0)=0 yields

    ||X(T)||² <= (1/(2nu)) integral_0^T
       exp(2 integral_s^T m1(t)dt) ||W(s)||² ||W(s)||_infty² ds.  (1)

No forward q2 or adjoint evolution is needed for (1).

## Certified envelope use

The pinned per-cell chain supplies N_i>=||W(s)|| for s in cell i, uniformly
for all nonzero |b|<=beta. Recompute the parent's cumulative D_w,j and
I_j>=integral_0^{t_(j+1)}||W||_infty² from its A–B formulas at the already
selected lambda=1000000. No lattice recomputation is needed: the audited
Ahat upper endpoint is read directly. Final cumulative values reproduce
the parent within 1e-45 relative discrepancy (a consistency check only).

Since every m1,i>0, an inclusive cell upper weight for (1) is
f_i=exp(2 sum_(k>=i) m1,k Delta) N_i². Let phi_i=max_(k>=i) f_k.
For the unknown true cell integrals x_i>=0 and true prefix sums S_i<=I_i,

    sum f_i x_i <= sum phi_i x_i
      = phi_last S_last + sum_(i<last)(phi_i-phi_(i+1)) S_i
      <= phi_last I_last + sum_(i<last)(phi_i-phi_(i+1)) I_i.

Every coefficient of I_i is nonnegative. No cumulative envelope is
subtracted to infer cell dissipation. Define d_div as the square root of
this last quantity divided by 2nu. The triangle inequality for the linear
split then replaces the old self contribution min(d1,d2) by
min(d1,d2,d_div). The nonself components are read separately; subtracting
two norm upper bounds would not justify their reuse.

The exact observable identity retains its positive term:

    R_Z = <-Delta U,bar(r)> + b<grad q1,grad r> + ||grad w||²/2.

Dropping only the last nonnegative term gives
R_Z>=-b⁴ C_new, C_new=G(nonself+min(d1,d2,d_div))+S E_r.
The unchanged lower J2 bound therefore gives, uniformly over 0<|b|<=beta,

    H_b(T)/b² >= J2_lo-beta² C_new.                          (2)

## Result and alternative route

Safely rounded outward values from `results/candidate.json`:

| Quantity | Upper bound (unless labeled lower) |
| --- | ---: |
| Old mean self contribution | 603.159427 |
| New divergence mean self contribution | 158.221110 |
| Unchanged nonself sum | 12.344635 |
| Old remainder constant | 1201.917538 |
| New remainder constant | 377.312890 |
| beta² C_new | 0.003395816008963 |
| J2 lower bound | >=0.008200720680466 |
| H_b(T)/b² lower bound at beta | >=0.004804904671503 |

Thus (2) is strictly positive on the entire fixed nonzero amplitude range,
conditional on the inherited certificates and acceptance of this new argument.
It does not establish monotonicity of actual trajectories, a sharp amplitude
threshold, or validity beyond beta. At b=0 the interaction excess is zero.
The interval endpoints in the output enclose evaluations of sufficient
majorants; they are not lower/upper measurements of actual norm values.

The alternative signed-mean route at the old remainder would suffice if
M > -0.024523165383133463572158893395164397387447352706526
(a conservative upper threshold). A favorable sign is not expected or needed.
The norm-only source hull file does not contain a signed pairing or an adjoint
residual, so merely relabeling that certificate as signed cannot improve it.
An analytic adjoint or coarse validated pairing could be useful, but no
impossibility claim about such alternatives is established. Since route1 meets
the fixed comparison cheaply, no adjoint/q2 construction or pilot was needed.

## Inheritance, arithmetic and reproduction

Assumed, not rerun: the absorption certificate/closure and cellwise Lemma M;
analytic base bounds; q1, endpoint G/E and source-hull certificates; Route B
mode support and remainder identities; weighted Fourier inequality and the
audited endpoint-sign A–F chain. The independent audit at
`87fa0e39ac51d8fd63b110af60e88c2f0e606109` was inspected read-only. The new
calculation does not repair or independently validate those dependencies.
Inherited IEEE binary64 assumptions, Python, mpmath interval arithmetic and
stored upper endpoint interpretation remain trusted. No new empirical data.

`INPUTS.json` pins all seven input files. Stored point endpoints are padded
outward by 1e-50 to exceed their roughly 60-digit serialization uncertainty.
Arithmetic uses mpmath intervals at 70 digits; exact nu=1/28, beta=3/1000 and
cell duration=1/1000 are formed as interval rational divisions. Directed
decimal conversion uses the exact binary endpoint ratio and Decimal rounding.
All acceptance decisions use interval endpoints, not rounded table entries.

From this directory with the already installed Python 3.12 / mpmath 1.3.0:

```sh
python -B check.py /tmp/new-unused-endpoint-result.json
python -B test_check.py -v
```

Outputs are exclusive-create. The first invocation in the separate test venv
failed importing mpmath, before computation; `results/first.log` is preserved.
The successful candidate used system Python, with no installation. Original
outputs and branches remain untouched; no LFS, arrays, DNS, validator, q2,
adjoint, paid service, push, PR, merge or deployment was used.

Six focused tests passed. Recorded wall time for the failed import, successful
postprocessor and tests totals 0.303954 seconds, below the 300-second cap;
each invocation had a 60-second hard timeout. Unrelated application, web,
NS simulation and Lean suites were not rerun. The local result is ready for
human review; publication/integration is not authorized by this stage.
