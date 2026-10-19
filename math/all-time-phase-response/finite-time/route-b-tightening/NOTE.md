# Analytic Route B tightening: candidate for independent review

Owner Codex. Branch codex/route-b-analytic-tightening, base
4bf68e0a6dcddc0d38b77c0123006fbea90d5f89. Fixed a=c=d=1, nu=1/28,
phi=37/100, T=1/4, beta=.003. No DNS, mean-q2 evolution, full validator or
trajectory download/read was performed. This is analytic interval postprocessing.
Original archives are untouched. No dominance or new physical result is claimed.

The candidate below is conditional on the inherited absorption/Route B
certificates and, for endpoint improvements, the pending-review endpoint bound.
An independent AI reviewer examined the derivations and implementation; see
REVIEW.md for limitations and the correction it identified. AI review is not
human refereeing or formal verification.

## 1. Quantitative diagnosis, without an assumed coefficient

The existing C_B is 87806.1462 (rounded description, not a new upper endpoint).
Its components are mean pairing 85902.0117 (about 97.8%), cross term1781.2973,
and w energy122.837138. Mean forcing before propagation is dominated by
C_A K sqrt(T D_w)=9352.9868, versus1076.3137 smooth q/r coupling and only
3.4967 combined q-error terms. That self term is about89.7% of mean forcing.

D_w=86106.4507 arises from (8/nu) times energy contributions331.4276 growth,
4.93904 mixed,48.03716 source, and9.0914e-8 error advection. The K² growth
contribution is about86.2% of this sum. In the full-r squared forcing bound,
w-dissipation contributes9470.1892 of10064.2028, about94.1%.

Thus the major losses are repeatedly using global K at all times, the estimate
||w||_infty<=C_A||Delta w|| which discards the much smaller L2 norm, and
three-term square splitting. Tiny q1 validation errors are not the leading loss.
The original inherited K=15.674 and N=.33625 remain unchanged below.

There is no known positive certified lower bound on |Z2(T)|: its present
interval includes zero. Hence there is no established numerical C_B target
that by itself proves dominance. For any future certified L>0, the required
condition is C_B<L/beta². We report beta²C_B, not a comparison with uncertified
sampled coefficients or with the positive q1 energy term alone.

## 2. Lemma A: exploit L2 information in the sup-norm estimate

All norms use normalized torus Parseval and Euclidean vector magnitudes.
For any mean-zero vector field W in H2 and lambda>=0, define

    A_lambda = sum_{k in Z³, k!=0} 1/(lambda+|k|^4).

Fourier triangle inequality followed by weighted Cauchy-Schwarz proves

    ||W||_infty² <= A_lambda [lambda||W||²+||Delta W||²].       (A)

There is no factor three: apply Cauchy-Schwarz to the scalar magnitudes of
vector Fourier coefficients. No incompressibility is needed for (A), only
zero spatial mean. For the finite cube F_R={max|k_i|<=R, k!=0}, the inherited
C_A² upper-bounds sum |k|^-4, so

    A_lambda <= Ahat_lambda
      := C_A²-sum_{k in F_R} lambda/[|k|^4(lambda+|k|^4)].     (B)

The finite correction is nonnegative. Subtract its LOWER interval endpoint
from the UPPER endpoint of C_A². This is implemented by interval subtraction.
No new tail estimate is needed; unremoved positive correction outside the
cube only makes Ahat larger. Ahat's lower endpoint is not a lower bound on
the infinite lattice sum. All reported intervals enclose majorant evaluations,
not physical norm lower bounds.

For b!=0 let W=w/b². Inherited bounds give ||W||<=N, ||grad W||<=K and
integral||Delta W||²<=D_w. Integrating (A),

    integral_0^T ||W||_infty² <= I_infty
       := Ahat_lambda(lambda T N²+D_w).                      (C)

It follows that the full scaled-r forcing in Route B obeys

    ||F_r||/|b|³ <= A+C_A K d_e+h||W||_infty,
    A=pK+n1N, h=eps1+beta K, d_e=||Delta e||.

Indeed B(w,e)/b² is bounded by eps1||W||_infty and
B(w,w)/b⁴ by K||W||_infty. The other three terms retain their old bounds.
Hence valid L1 and squared L2 forcing majorants are

    L_r=A T+C_A K sqrt(T delta)+h sqrt(T I_infty),
    J_r=[A sqrt(T)+C_A K sqrt(delta)+h sqrt(I_infty)]².       (D)

The second line uses Minkowski in time, not an assumption that different
terms are uncorrelated or have a favorable sign.

Keep the inherited linear lemma unchanged:

    N_r=exp((M1-nu)T)L_r,
    E_r²=exp((4M1+1)T)[M2²N_r²T+J_r/nu],
    D_r=(2/nu)[(2M1+1/2)E_r²T+M2²N_r²T/2+J_r/(2nu)].       (E)

Mode support still gives the exact mean-remainder equation in Route B.
Its revised forcing bound is

    L_bar=(p E_r+n1 N_r)T+C_A E_r sqrt(T delta)
           +C_A eps1 sqrt(T D_r)+K sqrt(T I_infty),
    N_bar=exp((M1-nu)T)L_bar.                               (F)

Thus C_global=MDelta N_bar+S E_r+K²/2 bounds the remainder throughout[0,T].
At T only, replace MDelta by G<=1.8534, obtaining

    C_endpoint=G N_bar+S E_r+K²/2.                          (G)

The latter depends on the endpoint derivation and is not a uniform-in-time
claim. Both cover every |b|<=beta; b=0 follows directly from zero remainder.
The exact observable identity and all original Fourier cancellations remain
unchanged. Nothing permits dropping the positive K²/2 in a two-sided absolute
bound, or inferring signs from b-evenness.

## 3. Lemma B: zero-initial-energy cap improves retained dissipation

Set y=||grad w||²/b⁴, z=||Delta w||/b² and

    a=2M1+2beta n1, q=2beta² C_A²/nu,
    c=(M2+beta n2)N,
    f0=cK+4sigma²/nu, f_delta=4C_A²eps1²/nu.

The original retained W2 inequality is

    y'/2+(nu/8)z² <= a y+q d_e² y+c sqrt(y)
                     +(4/nu)(sigma²+C_A²eps1² d_e²).

Using sqrt(y)<=K and discarding only positive dissipation gives

    y' <= (2a+2q d_e²)y+2f0+2f_delta d_e², y(0)=0.

Duhamel and integral_s^t d_e²<=delta prove, since a>0 here,

    y(t)<=g(t):=exp(2q delta)
       [(f0/a)(exp(2at)-1)+2f_delta delta exp(2at)].          (H)

The smooth part is integrated exactly in time; the error forcing is bounded
by its global mass and the largest propagator. g(0)>0 reflects that upper
estimate, not a nonzero actual initial error. Therefore

    integral_0^T y <= I_y := upper integral of min(K²,g(t)).

Both functions are nondecreasing. A1000-cell right-endpoint rectangle sum
with exact interval h=T/1000 supplies the stated upper integral. Integrating
the ORIGINAL W2 inequality once from zero, using integral sqrt(y)<=sqrt(T I_y),
gives

    D_w,new=(8/nu)[a I_y+q K²delta+c sqrt(T I_y)
                     +(4/nu)(sigma²T+C_A²eps1²delta)].       (I)

No differences of cumulative upper bounds are used. No later-cell initial
energy is discarded. The pointwise K remains15.674; only its time-integrated
use is sharpened. This avoids repeating an initial-energy charge on every cell.
It is valid to insert (I) into (C), retaining all other inherited inputs.

## 4. Directed interval sensitivity and current candidate

R=32 uses274624 integer lattice points and an exact integer histogram of |k|².
The five lambdas were listed before execution. Each yields a valid upper
majorant; choosing the smallest reported bound is not a claim of global
optimality or a fitted scientific prediction.

| lambda | C_global with old D_w | C_endpoint with old D_w | C_global with (I) | C_endpoint with (I) |
|---:|---:|---:|---:|---:|
|100|44668|20042|34472|15513|
|10000|25975|11739|20234|9190|
|100000|20245|9194|16002|7310|
|1000000|17927|8165|15129|6922|
|10000000|26896|12148|25633|11588|

Table entries rounded upward to integers from final directed interval outputs.
Using lambda=1000000 and (I), selected upper bounds are:

    I_y <=31.887685 (old T K²=61.418569),
    D_w,new <=50101.780 (old86106.451),
    Ahat_lambda <=.474521868,
    I_infty <=37187.233,
    L_r <=11.581678, J_r <=536.54100,
    N_r <=22.495866, E_r <=563.96425, D_r <=26664472,
    N_bar <=3440.1771.

The mean self forcing drops from9352.9868 to an upper1511.2865;
smooth mean forcing is<=259.01004 and both q-error terms together<.8300.
The retained-dissipation growth term drops331.4276 ->172.0727; source48.0372
is unchanged. This explicitly identifies which losses were reduced.

The full, unrounded majorant endpoints yield

    C_global <=15128.800282, beta²C_global <=.136159203,
    C_endpoint <=6921.648412, beta²C_endpoint <=.062294836,
    beta^4 C_endpoint <=5.606536e-7.

The global improvement does not depend on the endpoint G refinement. The
endpoint improvement is conditional on that additional certificate. Neither
is a dominance certificate: the known lower bound on |Z2(T)| remains zero.
No numerical remainder value or measured coefficient entered the calculation.

## 5. Signed structure, obstruction, and a smaller next experiment

The known q1 energy interval supplies E>=.28091, but Z2=E+M and the certified
norm-only M enclosure allows cancellation. Thus neither E nor Z2(0)=1/4 is
a lower bound on |Z2(T)|. Translation symmetry supplies parity, not sign.
Tighter K alone is unnecessary for the present improvement, and signed
cancellations cannot be credited without a separately controlled observable.

There is now a cheaper possible route than evolving mean q2. Let

    L_F >= integral_0^T ||overline B(q1,q1)|| dt.

The exact zero-initial mean equation gives

    ||V(T)||<=P L_F, P=exp((M1-nu)T)<=1.9424,
    Z2(T)>=E_lo-G P L_F.                                   (J)

If an independently validated source-only calculation establishes L_F<=.05,
then exact conservative decimal arithmetic gives

    Z2(T)>=.28091-1.8534*1.9424*.05=.100907792 > .06230.

Together with (G), this would meet the ORIGINAL endpoint comparison at the
unchanged beta. This is a conditional sufficient lemma, NOT a result of this
task. No current output certifies L_F<=.05. Inherited generic q1 source bounds
are too coarse; the three pilot source values cannot establish the integral.

Smallest next proposed experiment (NOT RUN): on each of250 coarse time cells,
build an outward complex-disc hull of all51 existing fine-node raw Q arrays.
Project the hull at kz=+1 with interval arithmetic. Convexity and linearity
then enclose every prescribed piecewise-affine qN segment in that cell.
Evaluate the full quadratic mean-source convolution once per cell, keeping
all modes, real +/-z factors, conjugate reversal and final Leray projection.
Bound the entire cell by its enclosing Parseval norm times exact duration.
Sum these250 bounds and add the inherited source discrepancy<=3.3118e-5.
This encloses L_F, with no source-time sampling assumption.

No approximate V is evolved, so there is no V residual, V initial-error budget
or base-discretization term in (J); U is treated through its analytic propagator
and endpoint G. The q1 error and its inherited base error remain accounted for
by the existing certificate and Delta_F. A hull can overestimate severely;
failure to reach .05 must be preserved and does not imply physical failure.

This proposal needs250 source convolutions, compared with12500 residual cells
(each with several convolutions) in the mean validator. Its timing is not yet
measured. Start with a few hull cells under a short hard cap to test cost and
slack; authorize a bounded full250-cell pass separately if appropriate. Do not
launch the two-hour mean validator merely because it was previously proposed.

## 6. Arithmetic, failures, reproducibility, and budget

Use only results/sensitivity.final.json and results/time_refinement.final.json
for current candidate numbers. Earlier results and exact script snapshots are
preserved. Independent review found that taking every stored upper endpoint
as a point also took nu slightly ABOVE1/28. Reciprocal and dissipative factors
can then be underestimated. The initial runs are superseded and are NOT cited
as certified bounds; corrected scripts use the exact interval I.of('1/28').
Review-stage and final runs preserve output files separately. Endpoint JSON is
now hash-pinned and its exact scope and G<=1.8534 are checked before evaluation.

PLAN.md preserves the first preregistration hash. PLAN.time-refinement.md
preserves the expanded preregistration hash. Script snapshots preserve exact
initial/review hashes; final sources match final JSON. Original Route B,
endpoint, absorption and lattice records are never changed. Hash verification
precedes interval-helper import. Upper inputs are used only monotonically;
nu is treated as an exact parameter, not a monotone upper input.

Eight focused tests pass, including exact Fraction finite subtraction, lattice
counts, lambda-zero recovery, cube monotonicity, Minkowski identity, zero cap,
nested right sums, exact viscosity reciprocal and the conditional(J) arithmetic.
These are implementation checks, not formal proof or independent PDE evidence.
No application code changed; web/physics tests were not run for this math-only
postprocessor. No new dependencies or paid resources were used.

All numerical invocations, including superseded runs and tests, used less than
five seconds wall time in total (conservative allowance), far below300 seconds.
Final process times: about.174s sensitivity,.331s time refinement,.126s tests;
recorded separately from internal algorithm timers. Each process was limited
to60 seconds. The independent reviewer ran no computations.

Reproduction from this folder, Python3.12/NumPy already installed:

    python -B evaluate.py
    python -B time_refinement.py
    python -B -m unittest -v test_estimates.py

Output paths are exclusive-create; use a separate copied working folder with
new output destinations for reruns. Existing result files must not be removed
or overwritten just to run these commands. Review the exact local commit before
integration. No push, merge, deployment, new download or next experiment is
included in this task.
