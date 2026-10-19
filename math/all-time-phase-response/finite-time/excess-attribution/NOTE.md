# What causes the certified endpoint enstrophy excess?

Fixed problem and norm conventions are those of
[the endpoint certificate](../ENDPOINT_CERTIFICATE.md): unforced periodic NS,
normalized volume average, initial velocity
u_b(0)=(sin y,b sin z,cos x-cos(x+y+37/100)), nu=1/28, T=1/4,
0<|b|<=.003. U is the b=0 solution. This stage derives an exact balance and
identifies a data gap; it supplies no new simulation or sign certificate for
an individual mechanism. Base 3161f059c24878c9b5ea05e6cc081e72fb53bbc5.

## Exact integrated identity

For omega=curl u, define

    Z(u)=<|omega|²>/2,
    Q(u)=<omega_i omega_j partial_j u_i>,
    D(u)=<|grad omega|²>=||Delta u||².

D has no factor 1/2. The existing solver's `Grid.palin` returns D/2.
The equality with ||Delta u||² uses periodic solenoidality/Parseval.
Curling NS gives omega_t+(u.grad)omega=(omega.grad)u+nu Delta omega.
Pair with omega: transport integrates to zero, diffusion contributes -nu D,
and stretching contributes Q. Thus Z'=Q-nu D for each smooth solution.

The isolated heat perturbation f_b=b exp(-nu t) sin z e_y has
Z_heat=b² exp(-2nu t)/4, D_heat=b² exp(-2nu t)/2 and Q_heat=0.
Consequently Z_heat'=-nu D_heat. Its initial Fourier support kz=+/-1 is
orthogonal to that of U(0), which has kz=0, giving
Z(u_b(0))-Z(U(0))=b²/4. Hence H_b(0)=0 exactly, and

    H_b'(t) = Q(u_b)-Q(U)
              -nu [D(u_b)-D(U)-b² exp(-2nu t)/2].

Define the accumulated stretching excess and (unweighted) dissipation excess

    S_b(T) = integral_0^T [Q(u_b)-Q(U)] dt,
    R_b(T) = integral_0^T [D(u_b)-D(U)-D_heat] dt.

Then the proposed identity is correct, with precisely these signs:

    H_b(T) = S_b(T)-nu R_b(T).                         (1)

The signed contribution of excess dissipation to H is -nu R, not +nu R.
R<0 means less accumulated dissipation than the base-plus-isolated-heat
reference; it does not mean the physical D(u_b) is negative. S is a difference
of stretching integrals, not the full solution's absolute stretching integral.
No monotonicity of either accumulated difference is presumed.
At t=0, Q(u_b)-Q(U)=0 and D(u_b)-D(U)=b²/2, so H_b'(0)=0 as well.
For Q, the odd-b terms vanish under the z translation by pi; the b² terms
contain a single nonzero horizontal base mode and integrate to zero. This
argument is valid for the fixed phase, not just the rational-phase test fixtures.

## What the certificate actually implies

The inherited endpoint result gives, conditionally on its existing assumptions,

    S_b(T)-nu R_b(T) >= 0.004804904671503 b² > 0.       (2)

Thus at least one of S_b>0 or R_b<0 must occur; neither is individually
established. If R_b>=0, then S_b>0. If S_b<=0, then R_b<0. Both S_b>0 and
R_b<0 can contribute, and both S_b and R_b can be positive if stretching wins.
At the scalar-balance level S=-1,nu R=-2 and S=2,nu R=1 both give H=1.
These examples demonstrate a logical non-implication, not realizable solutions
of this fixed NS family. The existing nonnegative norm/dissipation upper bounds
do not supply a signed separation of (2).

The missing term is already present at quadratic response order. With
u_b=U+bq1+b²q2+..., q2 half the second parameter derivative, orthogonality gives

    [b²]D(u_b) = ||Delta q1||² + 2<Delta U,Delta q2>.

The second term is a signed pairing with the mean q2. It is not recoverable
from ||grad q2|| or ||Delta q1||. For T(v,w,h)=<curl(v)_i curl(w)_j partial_j h_i>,
Q(u)=T(u,u,u), and its b² coefficient is the sum of the six terms obtained
by distributing degrees (2,0,0) and (1,1,0) over the three slots. These too
require q2. The cached q1 trajectory alone cannot identify even the complete
leading-order mechanism. Finite-b attribution additionally requires a remainder
bound or full u_b. No unsupported q1-only surrogate is used here.

## Existing evidence inspected read-only

| Artifact | Available information | Limitation for (1) |
| --- | --- | --- |
| `../results/measurements.json` and producer `../check_bounds.py` | N=24,K=7,dt=.005; times 0:.05:1; phi=.37; b=.001,.01,.05; norms of v,q1,q2, Z2 and R_Z | No Q history; no D(u_b), and no signed <Delta U,Delta v>. Stored ||Delta v|| is insufficient because D(u_b)-D(U)=2<Delta U,Delta v>+||Delta v||². b=.003 absent. Snapshots existed only in producer memory. |
| `../../results/pilot.json`, `refined.json`, `observable_remainder.json`, `recheck.json` | Resolution/phase and response-remainder diagnostics; some terminal stretching coefficients at T=.5 | Different endpoint/amplitudes; no time integrals at the fixed target. Initial pilot space failure remains a failure; later checks are not validation of the missing observables. |
| `math/ns-phase-audit/audit_v2/dns/c1_*`, `c3_*`, c4/c5 files | Other phase/extremum/derivative summaries and timing | Their Z2/Z4 labels in c1 mean values at t=2,4, not Taylor coefficients. No applicable joint fixed-target Q/D history recovered. |
| `../absorption-b003/trajectory/{W,Q}_nodes.npy` | Actual cached files in `/tmp/nicu-artifact-e9aa28a`, headers and sizes match manifest; local worktree contains LFS pointers | W is base-flow spectral data, Q is q1 data, not vortex-stretching Q. No q2 or nonlinear u_b trajectory. |

Cached W has shape (12501,43), complex128, 8,600,816 file bytes; Q has
shape (12501,3,21,21), complex128, 264,621,296 bytes. The manifest records
file hashes 0fc8d078... and 7a8157de... and prior validation provenance. Only
headers/sizes were inspected this stage; content hashes were not freshly
revalidated and array bodies were not loaded because the missing q2/u_b
cannot be repaired by reading them. No LFS transfers or regeneration.
`inventory.json` records inspected summary/source hashes and the evidence gap.

Therefore no empirical stretching/dissipation estimate is reported. Computing
H alone from existing Z2/R_Z would not supply an independent attribution or a
resolution check of its missing parts. Differencing cumulative upper bounds
would not fix this gap either.

## Minimal next diagnostic proposal — not executed

A later explicitly authorized diagnostic could run the existing strict-dealiased
solver only on [0,.25], with a=c=d=1,nu=1/28,phi=.37, paired U,u_(+.003),u_(-.003).
Use three fixed configurations: (N=24,dt=.0025), (24,.00125), (32,.0025).
There is no phase or amplitude sweep and no q2/adjoint solve. Stream scalar
observables instead of saving full trajectory arrays.

Measure Q using its normalized trilinear definition and D=2*Grid.palin.
Record S/b², nu R/b², H/b² and the integrated balance defect
[H-S+nu R]/b² at every output, plus divergence, high-mode tails and +/-b parity.
Integrate the scalar sources with the same RK4 stages as the velocities; also
retain a separately recomputed sampled quadrature to expose quadrature error.
Use the exact integrated heat term b²(1-exp(-2nu T))/4 for nu integral D_heat.
For cancellation checks compare direct differences with expanded differences,
including D(u_b)-D(U)=2<Delta U,Delta v>+||Delta v||². Independent trilinear Q
and the nonlinear RHS pairing should agree to roundoff on the resolved grid.

Preregister before that run: mechanism signs are unknown; a null/unresolved
outcome is acceptable. Stop without a sign attribution if a nonfinite state,
normalization/balance failure, or resource cap occurs. Require scaled balance
defect <=1e-5 and both time and space changes of S/b² and nu R/b² <=1e-4.
Claim an empirical sign only if its magnitude exceeds ten times the largest
observed refinement change, balance defect or direct-versus-expanded discrepancy.
If either term fails this separation, report unresolved, not zero. These are
operational diagnostic thresholds, not rigorous error bounds. Inspect high-mode
tails and parity as additional consistency checks; do not infer a continuum
certificate from agreement of two resolutions.

Resource evidence: the committed measurements record 12.6178s for one hierarchy
plus three full solves to T=1 at N=24,dt=.005, including diagnostics; `../../results/refined.json`
records 102.35s for a broader multi-resolution/phase task. These are historical
machine-dependent timings, not fresh benchmarks. A rough allowance for the
proposed short three-configuration, three-state task is 20–120s, with diagnostic
FFT overhead uncertain. First authorize a ten-step timing pilot (hard 30s); scale
its measured cost before any full run, require projected total<300s, and stop
if it exceeds that cap rather than silently coarsen.

At N=32, one complex128 half-spectrum velocity is
3*32*32*17*16=835,584 bytes (0.797MiB); three states are 2.39MiB. RK stages and
FFT temporaries dominate beyond this storage. Plan 256MiB working allowance,
hard 512MiB cap, scalar outputs well below 1MiB; these are conservative planning
allowances, not measured peak RSS. No need to load the 264.6MB q1 cache.
For a subsequent continuum sign certificate one would need new, signed integral
error bounds for these observables, including time interpolation, Fourier tails
and nonlinear trajectory error. Neither the old enstrophy endpoint remainder
nor a converged diagnostic substitutes for that validation. No such validator
is proposed to launch automatically; its cost remains unmeasured for this task.

## Relation to the regularity obstruction and verification

Vortex stretching competes with viscous dissipation in Z'=Q-nu D. For example,
|Q|<=||sym grad u||_infty ||omega||² gives
Z'<=2||sym grad u||_infty Z after discarding dissipation. Controlling the
coefficient over arbitrarily long times for unrestricted 3D data is a different
problem from a short-time signed difference between nearby solutions. Even a
positive S here would not establish runaway growth or a singularity. The
existing small-time closure remains assumed; this stage supplies no general
regularity theorem, all-time monotonicity or novelty claim.

Four tests use exact Fraction complex Fourier arithmetic: initial orthogonality,
D=||Delta u||² and instantaneous enstrophy balance, heat-baseline constants,
and logical scalar counterexamples. Two rational phase fixtures check algebra;
they are not simulations at phi=.37. No time step is taken. See results/tests.final.log, results/timing.json and results/timing.final.json
(first run precedes the explicit nonzero-Q assertion). Independent review and limits are recorded separately.

Recorded aggregate test execution: 0.193439 seconds, with 60-second hard timeouts.
One focused independent review found no blocking defect after the documented
repairs; see [REVIEW.md](REVIEW.md). Stop at this evidence gap and future
diagnostic proposal; no new run is authorized or launched here.
