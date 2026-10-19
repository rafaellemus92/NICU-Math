# Source-only mean forcing enclosure, fixed endpoint comparison

Owner Codex; branch codex/mean-source-hull. Base
f6cdc6d3eeed4c4e947eef0b56f48f1cc0b1eccd. Fixed a=c=d=1, nu=1/28,
phi=37/100, T=1/4, beta=.003. This task computes only a source norm bound from
already verified q1 nodes. It does not evolve q2, run DNS, or alter old archives.
No additional reviewer/subagent was used. New implementation/results are for
focused independent review, conditional on inherited mathematical certificates
and arithmetic/platform assumptions. No human-refereed or formal proof claim.

## Zero spatial mean and Poincare audit

Zero spatial mean is different from zero z-average. q1 and qN have only
kz=+/-1; therefore their full spatial means vanish, and so does e=q1-qN.
U has shear sin(y) and an x-harmonic vertical component, hence no spatial
zero mode. The initial perturbation sin(z)e_y also has zero mean.
For periodic divergence-free X, integral (X.grad)Y = integral div(X tensor Y)=0.
Leray preserves the spatial zero mode. Thus the unforced NS flow conserves
spatial mean; u_b and U have equal (zero) mean. Their difference minus bq1
is w, so W=w/b² is mean-zero for b!=0. At b=0 the remainder is identically zero.

The same divergence identity makes each forcing in the q2 and r equations
mean-zero. Zero initial data then implies zero spatial mean for q2,r and their
z-averages V,bar(r). A z-average can have kz=0 while its full spatial zero
mode is still absent. This justifies the mean-zero Agmon/resolvent uses for
W,e and r, and Poincare constant one in all inherited L2/H1 energy bounds:
||grad X||²>=||X||² and ||Delta X||²>=||grad X||² on the normalized2pi torus.
These also hold for z-independent mean-zero vector fields, with the horizontal
nonzero frequencies having |k|>=1. No mean removal is used to hide a constant
forcing. The quadratic mean source has exactly zero spatial mode as a divergence.

The full calculation explicitly asserts M1>=nu using exact interval nu=1/28.
The inherited fixed bound M1~2.69134 satisfies it. Thus
exp((M1-nu)(T-s))<=exp((M1-nu)T) is legitimate. A generic formula outside
this scope would require exp(max(M1-nu,0)T), or the actual time-dependent
propagator; this implementation does not claim generic parameter support.

## Exact path identity and support conventions

The pinned inherited validator defines qN=Re(e^{iz} Qtilde_lin), where
Qtilde_j=P_(kx,ky,1) Q_j is the EXACT projection of each saved complex128 node,
regarded as exact dyadic rationals, and Qtilde_lin is affine between these nodes.
Times are j/50000, j=0..12500. Raw arrays have shape12501x3x21x21, component
index0..2, kx=ix-10, ky=iy-10, kz=1. No FFT or producer interpolant is used.
This definition appears at inherited validate_residual.py lines5-18, with
project_small at333-343, node projection at464 and linear difference at483.
The saved validated.json definition records the same mathematical object.

This task imports that SAME pinned project_small function, not a replacement
rounded projection. The mode grid is checked against -10..10. Initial data
Q[0,1,10,10]=-i with exactly one nonzero coefficient is checked again. File
hash, file size, dtype, shape, manifest and inherited certificate/source hashes
are verified. The full record and additional verification identify both the
file hash and raw-array hash from the inherited certificate.

For coarse cell ell=0..249, use all51 nodes50ell..50ell+50. Choose the middle
node50ell+25 as an exactly represented disc center c. For each coefficient,
set radius=max_j abs_hi(csub(exact(Q_j),exact(c))). csub encloses subtraction
rounding; abs_hi encloses magnitude/radius; max merely selects an already
upward binary64 value. Thus every exact raw node lies in its convex disc.
Every affine segment between consecutive nodes is contained, including any
interior extreme absent at coarse endpoints. Project this raw coefficient-disc
product with inherited interval project_small. Linearity ensures containment of
exact P applied to every affine segment. This is precisely the inherited path:
P[(1-theta)Q_j+theta Q_(j+1)]=(1-theta)P Q_j+theta P Q_(j+1).
Dependencies discarded by the product hull enlarge it, never shrink it.

## Full source enclosure and error propagation

Let F=mean_z P[(q1.grad)q1] and F_N the same expression for qN. The pinned
mean-source kernel computes, for horizontal a=1,2 and component i,

    H_ai=Q_a * conjugate_reverse(Q_i),
    T_ai(k)=[H_ai(k)+conj(H_ai(-k))]/4,
    F_N=P_(kx,ky,0) i[kx T_1i+ky T_2i].

The factor1/4 comes from real +/-z harmonics. Flux and advective forms agree
on the exactly solenoidal inherited qN. Although a product of coefficient discs
also contains non-solenoidal vectors, evaluating a polynomial on that larger
set still encloses the polynomial at the actual solenoidal path. Setting the
flux derivative's spatial zero mode to zero is an exact identity, not a
numerical mean correction. P otherwise preserves supplied constant forcing.
The full convolution support is kx,ky=-20..20, shape3x41x41. No generated modes
are truncated, and the mean Parseval norm uses no extra factor1/2.

All products, sums, projection and source norms use the inherited complex-disc
arithmetic with IEEE binary64 nearest-rounding and gradual-underflow assumptions.
Source norm upper endpoints are converted by Decimal(float), preserving their
exact binary values. Accumulation uses the pinned directed40-digit interval
class and exact coarse width1/1000. If U_ell encloses the full source norm
on cell ell, then

    integral||F_N|| <= (1/1000) sum_ell U_ell =: L_N.

Averaging and P are contractions. For q1=qN+e, expansion into qN/e cross terms
and e/e gives

    integral||F-F_N|| <= DeltaF
      =T(n1 eps0+p eps1)+C_A eps1 sqrt(T delta_e).

No temporal source samples are substituted for an integral. The full source
majorant is LF=L_N+DeltaF. A reported narrow interval around its evaluation
is NOT a physical two-sided enclosure of the integral: the physical enclosure
is [0,LF_upper], recorded separately.

The exact mean equation LU V=-F, V(0)=0 has

    ||V(T)|| <= exp((M1-nu)T) LF =: Pprop LF.

For E=||grad q1(T)||²/2 and M=<-Delta U(T),V(T)>,

    |M| <= G Pprop LF,
    Z2(T) in E+[-G Pprop LF,+G Pprop LF].

G is the pinned endpoint true-Laplacian bound. This does not approximate V,
so there is no new V residual or V/base-discretization error. All qN/base
certificate errors remain accounted for in the inherited eps values/DeltaF.
The unchanged sufficient comparison is Z2_lower>beta²C_endpoint, using the
pinned analytic-tightening final output at lambda1000000. That endpoint-only
C remains conditional on its derivation and endpoint dependencies. The fixed
checkpoint LF<=.05 is reported separately; it is not substituted for the actual
coefficient comparison. No smaller b or centered observable is introduced.

## Completed result and exact comparison

All250 coarse hulls completed, covering every one of12500 fine affine cells.
The physical integral is enclosed in [0,0.011634099986769841802] (displayed
upward). The interval evaluation of its upper majorant is

    L_N in [0.01160098256918074329847347103683574687222,
            0.01160098256918074329847347103683574687256],
    DeltaF <=0.00003311741758909850330230978103381679315268,
    LF_majorant in [0.01163409998676984180177578081786956366537,
                   0.01163409998676984180177578081786956366572].

The .05 checkpoint passes. The actual unchanged comparison also passes in
this conditional computation:

    |M(T)| <=0.04188032197489055112430458451614510153884,
    Z2(T) in [0.2390354390205853038886062757535706692524,
              0.3228800752984831825812954945495797069070],
    beta² C_endpoint <=0.06229483570521460066153433755445732483802.

The lower coefficient endpoint exceeds the threshold by more than.17674060.
At beta=.003, b²Z2_lower>=2.151318951185267734997456481782136023271e-6,
while the candidate remainder upper bound is<=5.606535213469314059538090379901159235421e-7.
Their upper/lower ratio is<=.260609205. This is a bound derived from two
certificates, not a measured remainder ratio. The comparison is at T=1/4;
no all-time or whole-time-interval dominance conclusion is made. The inherited
remainder amplitude range remains |b|<=.003. No signed M was computed: its
symmetric norm bound is sufficient for a positive total coefficient enclosure.

The result depends on accepting the inherited absorption/error certificate,
analytic-tightening derivation, endpoint bound, and this new interval source
implementation. It is ready for focused independent review, not a claim of
formal verification or clinical relevance. Z2(0)=1/4 remains unchanged; no
centered/interacting-only quantity was substituted to obtain a positive result.

## Tests, timing, provenance and preserved failure

17 tests passed: seven new hull tests plus all ten inherited kernel tests.
New checks include an interior-node extreme invisible at coarse endpoints,
exact Fraction interpolation/projection containment, subnormal containment,
full hull source versus an independent exact3D advective convolution oracle,
complete time-cell coverage, grid/initial data and rejection of nonfinite nodes.
Inherited tests cover source factors/tails, zero modes, mean Parseval, operator
structure, polynomial residual, frozen exponent and inherited error budget.
Tests are implementation checks, not independent PDE observations.

Pilot coarse cells0,125,249 took .14647,.14407,.13457 seconds. The recorded
budget gate used twice the largest cell cost times250 plus10 seconds, below
85 seconds. Full run took36.624601 seconds, within its180-second watchdog.
Tests took.362798 seconds as a process; pilot including hashes took.611039s.
Raw-array and exact-accumulation verification took.167359s in the successful
run. Aggregate execution, including startup and the failed verification attempt,
was under45 seconds, within the300-second cap. No second full run was needed.

The initial additional verification script looked for the raw-array hash at
the top level of validated.json instead of under provenance, raising KeyError.
It produced no verification JSON and changed no source result. The schema lookup
was corrected; its code snapshot, empty stdout log and failure explanation are
preserved. All scientific tests and the full source run passed without retuning.

The successful postprocessor hashes the actual contiguous raw Q array again;
its SHA256 matches manifest, inherited validator and chain independently:
529b1e4c61f0a98437d09d92b1e71a1ad9a271fefafb7bbd5d507412cb4bd9d8.
The already checked Q file SHA256 is
7a8157de830a5c2358119084947299a8aeb5daf7b749f69e8506c23c47e94ccd.
It also checks every row's exact node coverage, finite upper norm and exact
Decimal(binary64) conversion. Independent Fraction summation gives
53500089114310671209/4611686018427387904000 for the sum of cell norm upper
bounds times1/1000, enclosed by the recorded interval L_N. All source, helper,
input and plan hashes are verified. Original archived math files are unchanged.

No app/web/physics tests were run for this math-only addition. No environment
packages, files containing secrets, patient data, external services, downloads,
mean-field solver, DNS, full inherited validator or additional reviewer were
used. Python3.12.14 and NumPy2.0.2 match the previously supported environment.

Review focus: hull convex containment of all fine nodes; identical inherited
projection/path; normalization and full convolution; zero-mean/Poincare audit;
input hash chain; norm accumulation; DeltaF and endpoint comparison; limits of
the inherited arithmetic model. Do not infer a sharper actual LF from the
narrow interval around its upper majorant. Source and proof are in this folder;
all outputs refuse overwrite. No further scientific stage follows automatically.
