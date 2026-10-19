# Fixed-endpoint Z2 enclosure: first-stage result and missing signed estimate

Owner Codex. Base `2af8fe4b3abceee08547f0fee699d78b5ac29bf2`.
Local branch `codex/phase-z2-endpoint`. Status: new analytic derivation and
interval postprocessing, pending independent review. No new evolution was run.
The approved Route B correction was pushed separately at the exact base SHA.

## Fixed question and definition

Fix a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000. On the normalized
2pi-periodic torus, Z(f)=||grad f||²/2 and

    Z2(t)=<grad U(t),grad q2(t)> + ||grad q1(t)||²/2,
    L_U q1=0, q1(0)=sin(z)e_y,
    L_U q2=-P[(q1.grad)q1], q2(0)=0.

q2 is the b² coefficient (half the second derivative). U is the b=0 solution.
The previous conditional Route B estimate is |R_Z(T;b)|<=b^4 C_B for
|b|<=beta, where R_Z=Z(u_b)-Z(U)-b²Z2 and C_B has a certified upper endpoint.
A sufficient endpoint quadratic-dominance test is

    a rigorous lower bound L<=|Z2(T)| satisfying L>beta² C_B.        (D)

This task fixed beta before evaluation. It does not change beta to make (D)
pass, and it does not infer a relative error from sampled coefficient values.
A failure to certify (D) is not a proof that actual quadratic dominance fails.

**Correction to earlier review wording:** Z2(0)=1/4, not zero. Indeed q2(0)=0,
||grad sin(z)e_y||²=1/2, and the enstrophy prefactor is 1/2. The centered
quantity Z2(t)-Z2(0) vanishes initially, but that is not the coefficient defined
above. The earlier user-relayed review wording, repeated in Route B NOTE/REVIEW,
was incorrect on this point. Those explanatory passages are corrected in this
local branch; no analytic formula or numerical archive changes. A positive
value at t=0 alone does not establish a lower bound throughout [0,T].

## 1. Exact endpoint qN energy, with the inherited H1 error

The saved complex coefficient Q(kx,ky) at node 12500 consists of exact dyadic
rationals. The approximation is qN=Re(e^{iz} P_k Q), k=(kx,ky,1), with exact
Leray projection. Thus

    ||grad qN(T)||² = (1/2) sum_k [|k|² |Q(k)|² - |k.Q(k)|²].       (1)

This follows from |P_k Q|²=|Q|²-|k.Q|²/|k|². The factor 1/2 accounts for the
real +/-1 z harmonics. Python Fraction evaluates (1) exactly on all 21x21
stored modes, using the exact real and imaginary binary64 coefficients.
No floating projection, FFT or grid quadrature is used. The inherited full
error obeys ||grad(q1-qN)||<=eps1=5.6024e-5, so if n_N=||grad qN(T)||,

    ||grad q1(T)|| in [max(0,n_N-eps1), n_N+eps1].                 (2)

The square and factor 1/2 give an interval E for ||grad q1(T)||²/2. Interval
square roots and all non-rational operations use the unchanged parent Iv class.
The source code retains the exact rational value of (1) in its output.

## 2. Endpoint base-flow Laplacian and its error

The validated base approximation is
U_N=(exp(-nu t)sin y,0,Re(e^{ix}W_lin(y,t))). At the endpoint,

    ||Delta U_N(T)||² = exp(-2nu T)/2
                       +(1/2) sum_n (1+n²)² |W_n(T)|².          (3)

The finite W sum is exact rational arithmetic. Orthogonality of the vector
components and normalized Parseval justify both halves. The true W error is
bounded by epsW=7.5438e-5 in the weighted norm sum_n(2+n²)^3 |error_n|².
For x=n²>=0,

    4(x+2)^3-27(x+1)^2=(x-1)^2(4x+5)>=0,

hence

    ||Delta(U-U_N)(T)|| <= sqrt(2/27) epsW =: eta_g.              (4)

The 2/27 includes the real x-harmonic factor 1/2; sigma=exp(-nu t)sin y is
exact and contributes no approximation error. Set

    G = upper endpoint of [||Delta U_N(T)||+eta_g].               (5)

G is an upper bound on the true norm, not a two-sided enclosure of that norm.
An interval around its numerical evaluation does not give a physical lower bound.

## 3. The signed q2 pairing: analytic norm-only enclosure

The already derived Route B linear estimate supplies

    ||q2(T)|| <= N2 <= 0.6360349089847990303600261781051790755900.

It uses the validated q1 source and no q2 simulation; its provenance and
conditional review status are inherited. Since U is z-independent,

    M := <grad U,grad q2> = <-Delta U,bar(q2)>,
    |M| <= ||Delta U|| ||bar(q2)|| <= G N2.                       (6)

The z-average is an L2 contraction. Combining (2) and (6),

    Z2(T) in E + [-G N2, G N2].                                 (7)

This enclosure is rigorous conditional on the inherited certificates, but it
has deliberately discarded the sign and cancellation of M. A q2 norm bound
cannot restore that information by itself. No unknown q2 coefficients are
silently set to zero.

## 4. Recorded first-stage evaluation

The preregistration is PLAN.md. The saved output is results/endpoint.json;
results/endpoint.log displays outward rounding. The first successful run used
Python 3.12.14 with NumPy 2.0.2; NumPy only loads/maps existing arrays, while
endpoint finite sums are rational and remaining arithmetic is interval Decimal.

| Quantity | Outward enclosure/bound |
|---|---:|
| ||grad q1(T)||²/2 | [0.28091, 0.28100] |
| ||Delta U_N(T)|| | [1.8532, 1.8533] |
| eta_g | <= 0.000020532 |
| G | <= 1.8534 |
| M | [-1.1788, 1.1788] |
| Z2(T) | **[-0.89785, 1.4598]** |
| available lower bound on |Z2(T)| | **0** |
| beta² times the existing C_B upper endpoint | [0.79025, 0.79026] |

The fixed target (D) is **not certified**. Zero is not excluded. There is also
no positive smaller-amplitude corollary from this enclosure; beta is unchanged.
The signed pairing uncertainty dominates, while the q1 energy interval is narrow.
The sampled 0.25–0.27-scale coefficient is not used as an input or proof.
Even a future precise coefficient enclosure might fail (D) with the current
C_B; sharper coefficient data alone must not be advertised as guaranteeing
quadratic dominance. A rigorous upper bound below beta² C_B would establish
that this particular sufficient comparison cannot pass, not that the true
remainder is too large.

This is a new bound/blocker ready for review, not a completed positive coefficient
certificate. Earlier conditional Route B absolute bounds remain unchanged.

## 5. Exact missing observable and an adjoint route without full q2

Let A_U=-nu Delta+B(U,.)+B(.,U), so L_U=partial_t+A_U. On solenoidal fields,

    A_U^* psi = -nu Delta psi -P[(U.grad)psi]+P[(grad U)^T psi].

Let the mean-zero z-independent adjoint solve

    -partial_s psi+A_U(s)^* psi=0,
    psi(T)=-Delta U(T).

It follows by differentiating <psi,q2>, and using q2(0)=0, that exactly

    M = -integral_0^T <psi(s), P[(q1.grad)q1](s)> ds.             (8)

Only the z-mean source matters. For qN=Re(e^{iz}Q), its unprojected mean source is

    F_N^raw=(1/2) Re[Q_1 partial_x(conj Q)
                      +Q_2 partial_y(conj Q)-i Q_3 conj Q],
    F_N=P F_N^raw.                                               (9)

Here Q denotes the exact projected, linearly interpolated stored coefficients.
The source discrepancy from the full q1 is bounded in L1 time by

    Delta_F=T(n1 eps0+p eps1)+C_A eps1 sqrt(T delta_e),            (10)

using the same qN/e decomposition as Route B and contraction of z-average/P.
Suppose a future adjoint approximation psi_N has a validated uniform L2 error
eta_psi and sup||psi_N||<=P_psi. For an outward enclosure M_N of
-integral<psi_N,F_N>, the signed observable error is bounded by

    |M-M_N| <= eta_psi L_sigma + P_psi Delta_F,                   (11)

where L_sigma is the existing bound on integral||(q1.grad)q1||. This uses
<psi-psi_N,F>+<psi_N,F-F_N>, so no cross term is omitted.

No psi_N or residual enclosure exists in the saved inputs. For a proposed
approximation, reverse-time L2 energy gives

    eta_psi <= exp((M1-nu)T)[eta_terminal + integral||R_psi||],    (12)

with R_psi the **full** residual against U and eta_terminal the terminal-data
error against -Delta U(T). If residuals are computed against U_N, additionally
include integral[||delta U||_infty ||grad psi_N||
+||grad delta U||_infty ||psi_N||], using the existing weighted W error.
The nonzero base-flow terminal error (4), and any spectral truncation of the
terminal data, belong in eta_terminal. No zero-terminal-error assumption is
permitted. Equations (8)-(12) identify the missing signed estimate precisely;
they do not pretend an unevaluated adjoint is a certificate.

## 6. Alternative mean-q2 validation plan and cost boundary

Only bar(q2), not full kz=0,+/-2 q2, is needed. A future mean-field evolution
would solve L_U bar(q2)=-F with zero initial data, where F is the z-mean source.
Writing bar(q2)=(A,B,C), the z-independent system has horizontal transport by
sigma(y), the stretching B sigma_y in its first component, and vertical
stretching A w_x+B w_y. The 2D Leray projection is modewise on (kx,ky,0).
Its full spatial zero mode must be defined as zero, not inferred from floating
solenoidality. For a projected piecewise-linear mean approximation Q2_N:

    eps_q2 <= exp((M1-nu)T)[R_int + Delta_F + Base_int],
    Base_int=integral[||delta U||_infty||grad Q2_N||
                       +||grad delta U||_infty||Q2_N||],
    |M-<-Delta U_N(T),Q2_N(T)>|
       <= G eps_q2 + eta_g ||Q2_N(T)||.                          (13)

R_int must enclose the full residual against U_N with source F_N, including
all generated Fourier modes and all time cells. This is an L2 residual problem;
no new q2 H1 certificate is necessary for this scalar pairing. Existing epsW
bounds and Fourier-to-sup conversions supply Base_int, but the approximation,
its norms, and R_int are new inputs, not currently available.

Before any implementation/run beyond this first stage, a reviewable plan would:

- Fix a mean/adjoint cutoff, for example |kx|,|ky|<=20, without selecting it
  after the dominance result. Define coefficients as exact saved dyadics followed
  by exact Leray projection, with continuous linear time interpolation.
- Use the already verified 12501 q1/base nodes. A provisional storage plan saves
  the new field at the 251 existing coarse boundaries; residual integration still
  subdivides at all q1/base fine nodes. No old output is overwritten.
- Enclose mean source (9) by direct convolution, including its full |kx|,|ky|<=20
  support. Products of a cutoff-20 mean/adjoint field with the stored base require
  at least |kx|<=21, |ky|<=41; projection does not expand support. Include the
  terminal |ky|=21 base tail if an adjoint cutoff discards it.
- Treat the cell polynomial terms exactly/enclosed (mean q1 source is quadratic
  in local time; its contraction with an affine adjoint is cubic). Integrate with
  exact rational times. Enclose the exponential shear and its variation, not
  floating solver times. Account for q1/base discrepancies via (10)-(13).
- Use direct interval convolution or a separately proved interval FFT; ordinary
  FFT agreement is not validation. Retain explicit roundoff/underflow assumptions,
  input/source hashes, residual-tail bounds and initial/terminal discrepancies.
- Test a few synthetic modes and cells first, then report measured pilot cost
  and residual slack before authorizing a full validator. No such pilot ran here.

Planning estimates, **not measurements or an approved run**: a 41x41x3 complex128
field at 251 saved nodes needs about 20.3 MB, versus about 1.01 GB if saved at
all 12501 nodes. Direct quadratic convolution involves roughly 441² mode pairs
per fine cell before component factors, or billions of pairs over the horizon.
A rigorously enclosed direct implementation may take tens of minutes to several
hours on this environment, exceeding cheap postprocessing; evolution alone may
be much faster. The prior 604-second one-dimensional-convolution validator is
not a reliable runtime promise for this 2D source. A small reviewed pilot is
required to narrow the estimate. No additional download, paid resource, new
trajectory or validator run has been launched.

## Reproduction and validation

From this folder, with Python 3.12 and NumPy:

    python -B endpoint.py --trajectory /path/to/already-verified/trajectory \
      --output results/endpoint.rerun.json
    python -B -m unittest -v test_endpoint.py

The script verifies pinned parent/source-result hashes and exact file hashes,
sizes, shapes and dtypes of both local arrays before inspecting the endpoint.
It does not fetch LFS files. Its exact finite sums and interval propagation
are cheap postprocessing, not a new PDE integration. Results record all hashes,
the exact rational endpoint sums and outward intervals. Outputs refuse overwrite.

An initial implementation invocation tripped the Decimal Inexact guard because
Python abs(Decimal) consulted the one-digit outer context. It wrote no JSON;
the issue was corrected with exact Decimal.copy_abs and a regression test.
The failure is recorded, and the target and mathematical estimate were unchanged.
Tests verify arithmetic/projection/normalization/interval implementation; they
are not proof of the PDE estimates or a substitute for independent review.
