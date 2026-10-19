# Forward mean-q2: bounded correctness and runtime pilot

Owner Codex; local branch codex/phase-mean-q2-pilot, base
bc305995c49f3303352e1c1a4e13a50dbf90d965. Status: implementation/structural
pilot, independent review pending. This is not a full coefficient certificate.
No new q2 evolution or full-horizon trajectory was generated.

## Scope and choice

Keep a=c=d=1, nu=1/28, phi=37/100, T=1/4 and beta=.003. The original target
is total Z2(T)=<grad U,grad q2>+||grad q1||²/2 and the sufficient comparison
lower(|Z2|)>beta² C_B. Neither it nor beta is changed to manufacture success.
The prior norm-only enclosure includes zero and remains the current result.

Choose forward mean-q2 rather than the adjoint: it has exactly zero initial
data and its source/error budget is explicit. An adjoint would require a
nonzero terminal-data approximation error and another backward operator.
Only V=bar(q2) is needed, because U is z-independent:

    L_U V=-F, F=bar(P[(q1.grad)q1]), V(0)=0,
    M(T)=<-Delta U(T),V(T)>.

For V independent of z, U=(sigma(y),0,w(x,y)), the P-free base operator is

    sigma partial_x V + (V_y sigma_y, 0, V_x w_x+V_y w_y).

There is **no w partial_z V**. The old kz=1 validator's i*w*Q term must not
be carried into this mean operator. Diffusion and the modewise 2D Leray
projection are applied separately. This difference is explicitly tested.

Z2(0)=1/4. Centered D2=Z2(T)-1/4 and excess-over-free-decay
I2=Z2(T)-exp(-2nu T)/4 remain separately labeled diagnostic proposals; neither
is calculated or treated as a replacement success criterion in this pilot.
Total quadratic dominance, if later established, may largely reflect initial
added enstrophy and is not by itself a demonstration of generated interactions.

## Exact approximation and source conventions

Reuse the already verified Q/W files. Q_j is projected exactly on
(kx,ky,1); qN=Re(e^{iz}Q) is real and solenoidal. The pilot imports the pinned
validator's complex-disc arithmetic helpers, with their binary64 rounding and
underflow assumptions; it never invokes that validator's main/run function.
All new convolutions are direct interval operations, not ordinary FFTs.

For horizontal direction a=1,2 and component i=1,2,3 define the Fourier
convolution H_ai=Q_a * conjugate-reverse(Q_i). The mean real tensor is

    T_ai(k)=[H_ai(k)+conj(H_ai(-k))]/4,
    F_N(k)=P_(kx,ky,0) [i kx T_1i(k)+i ky T_2i(k)].

The 1/4 is from the two factors in Re(e^{iz}Q). The two opposite z harmonics
are included through the conjugate-reversed tensor. The z-derivative of the
mean flux is zero. Flux and advective forms are equivalent because qN is
exactly solenoidal. The test oracle independently constructs all +/-z modes
and sums the 3D advective expression with exact rational complex arithmetic;
it does not reuse this flux identity in its computation.

The full source support is |kx|,|ky|<=20 for Q cutoff 10. Its full spatial zero
mode is exactly zero as a periodic divergence, and the kernel sets that
analytically known coefficient to zero. Forcing Leray projection otherwise
**preserves** a supplied zero mode. A separate approximation-node operation
Hermitian-symmetrizes the mean field, projects it, and defines its zero mode as
zero. These operations are intentionally distinct: a constant residual cannot
be hidden merely by calling a projector.

For the chosen mean cutoff 20 and W support |ky|<=21, complete base products
require |kx|<=21, |ky|<=41. Residual arrays cover all 43x83 modes in all three
components, including modes outside the approximate 41x41 state. Mean-field
Parseval norms use sum|Vhat|², with **no extra 1/2**. The q1 positive-z
representation still uses its inherited real-harmonic normalization.

## Affine cell residual and frozen exponential

On a fine interval of exact width h=1/50000, write Q=Q0+tau DQ,
W=W0+tau DW, V=V0+tau DV. Let S(V) denote the shear operator, B(W,V) the
vertical base coupling, and F(Q) the quadratic mean source. At left time tj,
e_j=exp(-nu tj), the frozen residual is

    R(tau)=DV+nu K²(V0+tau DV)
           +P[e_j S(V0+tau DV)+B(W0+tau DW,V0+tau DV)]
           +F(Q0+tau DQ)=R0+tau R1+tau² R2.

In code differences dQ=Q1-Q0, dW=W1-W0, dV=V1-V0 are used. The bilinear
cross coefficient is [B(W1,V1)-B(W0,V0)-B(dW,dV)]/h. The quadratic-source
cross coefficient is [F(Q1)-F(Q0)-F(dQ)]/h, with quadratic coefficient
F(dQ)/h². These identities handle both cross terms without dropping either.
Every multiplication/projection is enclosed, including cancellation in these
expressions. A midpoint test compares this polynomial with a separately
ordered direct evaluation; disc overlap is a consistency check, not a proof.

The residual integral is enclosed by

    h||R0||+(h²/2)||R1||+(h³/3)||R2||
      +e_j nu h²/2 * max(||S(V0)||,||S(V1)||).

The last term uses |exp(-nu tau)-1|<=nu tau and convexity of the norm of the
linear S(V) path. Norms of the **quadratic source** F(Q(t)) are NOT assumed
maximal at endpoints: its integral is bounded by its three polynomial
coefficients too. Exact rational times and interval exp/nu are used.

A future coarse-saved V trajectory can use this same fine-cell decomposition:
restrict the exact coarse affine path to each fine interval with rational
fractions of 1/50. That interpolation is not implemented as a global producer
in this pilot. The supplied V nodes here are probes only.

## Tests and execution boundary

The preregistered sampled indices are 0,6250,12499. Each uses its actual saved
Q/W endpoint pair. V0,V1 are zero in the initial-cell probe; later probes use
specified synthetic real, solenoidal mean fields (including an edge mode),
not states from a q2 solve. The later residuals cannot be summed or extrapolated
into a physical error bound for a trajectory starting at zero.

Ten tests pass, covering:

- exact-rational advective versus interval-flux convolution, real factors and
  a nonzero source tail;
- the initial sin(z)e_y source (zero exact target);
- preserving a force zero mode versus removing an approximation's mean;
- absence of vertical advection for a mean field;
- a base-product tail beyond the state cutoff, with exact coefficient i/4;
- shear factors, mean Parseval normalization and affine time-polynomial identity;
- the frozen-exponential correction against a separate 80-digit expression;
- inherited q1/base error-budget coefficients against exact rational arithmetic,
  and zero mean-q2 initial error versus nonzero W representation error.

These are arithmetic/structural implementation tests, not a PDE proof, full
validator or independent mathematical review. The interval helpers inherit the
previous arithmetic assumptions; this task does not verify hardware semantics.
A first test invocation failed because /usr/bin/time was absent; its log is
retained. A Python monotonic timer/subprocess timeout replaced that invocation.
No numerical test failed or estimate was retuned.

Budget: benchmark driver hard timeout 180 seconds; each test subprocess hard
timeout 60 seconds. Actual measured elapsed time was 2.3589 seconds for the
three-cell driver including file hashes, 0.148330 seconds for initial tests,
and 0.164147 seconds for final tests: under three seconds total, far below the
300-second numerical-execution cap. The source records the chosen cells and
synthetic states; no full-horizon arrays or runs exist in this folder.

## Measured runtime, storage and uncertainty

| Fine-cell index | Residual kernel seconds | Total probe seconds, including midpoint check |
|---|---:|---:|
| 0 | 0.5360 | 0.7200 |
| 6250 | 0.5479 | 0.7269 |
| 12499 | 0.5433 | 0.7258 |

The three residual kernels total 1.6272 seconds. Naive scaling to 12500 fine
cells is about 112–115 minutes **for the residual kernel only**, not a timing
guarantee. It excludes producing a mean trajectory and any full-run I/O or
additional review checks. Only three equal-size probes were timed; CPU load,
allocation behavior and a streaming implementation can change full-run cost.
Caching adjacent source endpoints might reduce cost, but that optimization
was not implemented or benchmarked. Do not replace the measured extrapolation
with an unsupported faster promise. A planning allowance of roughly 1–3 hours
for validation would need review before execution.

Peak process RSS was 34832 KiB (about 34 MiB) in this pilot; it is not a bound
for a full run. Stored mean nodes at 251 coarse boundaries require 20,252,688
bytes of coefficient payload (~20.3 MB). Saving all 12501 fine nodes instead
would require 1,008,680,688 bytes (~1.01 GB), which is unnecessary for the
proposed coarse-affine certificate. Both figures exclude file headers and logs.
Existing 273 MB arrays can remain read-only memory maps; a full scan can make
many more pages resident than these three probes. Full-run memory must be
checked separately; no new LFS transfer is needed for this plan.

## Residual budget and what the pilot does not establish

Full-horizon source discrepancy, inherited from the validated q1 certificate:

    Delta_F <= T(n1 eps0+p eps1)+C_A eps1 sqrt(T delta_e).

The recorded directed intervals give the convenient upward-rounded bound
Delta_F<=3.3118e-5; the complete endpoint is retained in pilot.json.
The smooth-q/error terms contribute almost all of it; the quadratic error
allowance is about 2.4003e-8. These are allowances, not lower bounds on actual
error and not proof of an irreducible accuracy floor.

Let Nv>=sup||V_N|| and Ng>=sup||grad V_N|| for a future real, projected mean
approximation. The archived weighted base error and outward conversion
constants S0<=.45864, S1<=.58868 give

    Base_int <= (8.6497210800e-6) Ng + (1.11022104600e-5) Nv.

The initial mean coefficient is exactly zero; any proposed producer must check
that explicitly. The base W initial representation error is nonzero and already
included in epsW; it must not be reset to zero. For the fixed global envelope,
exp((M1-nu)T)<=1.942366815339482226068806088954903901125. Therefore

    eps_V <= exp((M1-nu)T)[initial_error+R_int+Delta_F+Base_int].

The inherited q1 allowance alone, after this propagation, is <=6.4327e-5.
R_int and Nv,Ng for an **actual** full-horizon approximation remain unknown.
Later synthetic probe residual integrals (about 9.17e-7 and 1.86e-6 per fine
cell) are not accuracy forecasts. Their modes outside the state cutoff are
retained; their large physical mismatch is unsurprising because no q2 equation
was evolved. Arithmetic disc radii in their R0 coefficients are about 2e-13,
well below the synthetic mismatch; this observation does not certify future
roundoff or approximation error over the horizon.

For a future signed endpoint evaluation m_N=<-Delta U_N(T),V_N(T)>, use

    |M-m_N| <= G eps_V + eta_g ||V_N(T)||,
    Z2(T) in E + m_N + [-error,+error].

Here E is the existing endpoint interval for ||grad q1||²/2; G bounds the true
||Delta U(T)|| and eta_g bounds ||Delta(U-U_N)(T)||. The new endpoint derivation
provides G<=1.8534 and eta_g<=2.0532e-5, subject to its independent review;
the previously certified analytic MD is an available looser substitute for G.
The exact scalar Fourier pairing needs outward arithmetic and all retained
modes, not an ordinary rounded dot product. A planned desired interval width
must include E's width as well as these errors. If their budget is too large,
the result is an inconclusive enclosure, not permission to change beta.

Known bottlenecks: direct two-dimensional quadratic-source convolution dominates
runtime; the full-trajectory residual and its tail/interpolation components are
still the unknown accuracy bottleneck. Norm-only enclosures cannot determine
the sign of M. Neither the pilot nor a future coefficient sign certificate
alone establishes the original dominance target with current beta² C_B≈.79026.

## Concrete next full-run plan — NOT EXECUTED / requires separate review

1. Review kernels.py, the exact-mode tests and this residual/error derivation.
   Keep cutoff M=20, fine times j/50000, coarse save interval 50, and the original
   fixed physical parameters; do not tune them after the dominance outcome.
2. Implement only the forced linear mean equation with V(0)=0. A provisional
   producer uses RK4 with dt=1/50000 and ordinary FFTs on a 64x64 working grid.
   Its forcing/base are interpolated from the existing arrays, with no new base
   or q1 solve. At this cutoff, base-product support reaches ky=41: on grid 64
   wrapped modes start at |ky|=23, outside the retained |ky|<=20. The mean source
   reaches 20. Regardless of producer accuracy, residual validation is the proof.
   Save 251 nodes (~20.3 MB) to a new local artifact, preserve exact hashes, and
   define its real/divergence-free/zero-mean approximation by the projections above.
3. Verify initial zero coefficients and real/projection conventions. Restrict each
   coarse affine interval to the existing fine cells using exact rational fractions.
   Run the complete-support residual kernel on all 12500 cells and accumulate
   directed interval upper bounds. Obtain Nv,Ng by convex endpoint norm bounds
   on the coarse affine path. Include every tail and the exponential correction.
4. Add Delta_F and Base_int to R_int and propagate the L2 error with initial
   discrepancy explicitly accounted for. Compute m_N by a validated Fourier
   pairing, then form the endpoint interval using E, G and eta_g. Archive the
   input/source hashes, arithmetic assumptions, cells completed, timings and all
   decomposed error contributions. Never replace an incomplete run by a certificate.
5. Apply the unchanged total-Z2/beta=.003 comparison. Preserve failure or an
   interval containing zero. If centered/free-decay quantities are displayed,
   label them separately as diagnostics, not substituted successes. Stop and
   request independent review before publication or any further refinement.

The producer and full validator are not implemented/run by this pilot. This plan
is intentionally gated: the measured cost exceeds the current five-minute
permission. No new computation follows automatically from this note.
