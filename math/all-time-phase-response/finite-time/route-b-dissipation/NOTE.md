# Route B, first stage: retained dissipation and a direct quartic observable bound

Owner: Codex, 2026-10-19. Base: `419e6c3d2e0321816849ca550ad8da5cf34ba75a`.
Status: derived paper estimate and directed interval evaluation, **independent
mathematical review pending; not formalized**. This is not a new simulation,
a novelty claim, a clinical result, or an assertion about general regularity.
The [preregistered milestone](PLAN.md) was written before evaluation.

## Scope, inputs and notation

Fix a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000, and |b|<=beta.
All norms and integrals use the parent's normalized torus convention:
||f||²=(2pi)^(-3) integral_{T³}|f|² and Z(f)=||grad f||²/2.
There are no dimensional clinical units. B(X,Y)=P[(X.grad)Y], with the
orthogonal Leray projector P. L_U X=X_t-nu Delta X+B(U,X)+B(X,U).
A bar denotes z-average. The velocity base U is independent of z.

The [completed absorption certificate](../absorption-b003/NOTE.md) supplies smoothness on [0,T] uniformly
for |b|<=beta, as justified by its NOTE §8 Lemma M, and the following terminal
upper envelopes, valid throughout [0,T] and for the whole amplitude interval:

    v=u_b-U=b q1+w,  ||w||<=b² N,  ||grad w||<=b² K,
    ||grad q1||<=S,  q1=qN+e,
    ||e||<=eps0, ||grad e||<=eps1, integral_0^T ||Delta e||²<=delta.

Here N=N_w, S=S1. qN is the exactly solenoidal approximation defined by the
Leray projections of the stored dyadic arrays, not a new numerical trajectory.
Let p,n1,n2,sN be global bounds on ||qN||_infty, ||grad qN||_infty,
||grad² qN||_infty, ||grad qN||. They are maxima of the **validated** cell
bounds, not nearest-rounded diagnostic log values. Set

    sigma=p sN+n1 eps0+p eps1,  d_e(t)=||Delta e(t)||.

Then ||(q1.grad)q1||<=sigma+C_A eps1 d_e by the archived source decomposition.
All input floats are read as their exact binary values using Decimal(float).
The printed chain upper bounds are read as exact decimal upper bounds.

For the analytic base-flow envelopes, set E1=(1-exp(-nu T))/nu,
E2=(1-exp(-2nu T))/(2nu), g1=1+2E1,
g2=1+4E1+(4/nu)(E1-E2). The parent's derivative estimates give, for all t<=T,

    M1=sqrt(5+g1²) >= ||grad U||_infty,
    M2=sqrt(5+2g1²+g2²) >= ||grad² U||_infty,
    MD=sqrt(1+(2+g2)²) >= ||Delta U||.

These deliberately use alpha<=1, rather than its smaller terminal value.
Let C=C_A. The inherited fixed input has C<=4.06707921080. We use its certified
upper endpoint everywhere. Poincare constant is one, on mean-zero fields.
All fields below have zero spatial mean, since their initial data and periodic
advective forcing have zero mean. All bounds inherit the completed certificate's
arithmetic/platform assumptions; Python Decimal and the interval implementation
are also trusted. The calculation pins the input and interval-source SHA-256s.

## 1. Retaining W2's positive dissipation

Before the Poincare substitution in the archived W2 argument, with
Y=||grad w||² and D=||Delta w||, its seven-eighths absorption gives

    (1/2)Y' + (nu/8)D²
      <= [2M1+2|b|n1+(2b² C²/nu)d_e²]Y
         +(M2+|b|n2)||w|| sqrt(Y)
         +(2b⁴/nu) ||(q1.grad)q1||².                         (W)

The coefficient nu/8 is the dissipation that was replaced by nu||grad w||²/8
in the original K estimate. We retain it here, so **no negative nu/8 appears
in the growth coefficient of (W)**. Using (x+y)²<=2x²+2y² on the source,
dividing symbolically by b⁴ for b!=0, and bounding |b| by beta gives

    H(h,d) = (2M1+2 beta n1)K² h
             +(2 beta² C²/nu)K² d
             +(M2+beta n2)N K h
             +(4/nu)(sigma² h+C² eps1² d).

Integrate from zero, use w(0)=0, and discard only the nonnegative final energy:

    integral_0^T ||Delta w||² <= b⁴ D_w,
    D_w = (8/nu) H(T,delta).                                (1)

The factors 8/nu and 4/nu have different origins: retained dissipation and the
squared-source Young estimate. Their combination legitimately produces nu^-2.
No finite difference of K², or of any cumulative upper bound, is used.
At b=0, w=0 exactly; the estimates extend without dividing by zero.

**Cell rule.** For a cell [s,t], let K_s² bound ||grad w(s)||²/b⁴, and let d_st
be an absolute bound on integral_s^t d_e². The valid bound is

    integral_s^t ||Delta w||²
       <= b⁴[(4/nu)K_s²+(8/nu)H(t-s,d_st)].                 (2)

K_s=0 only when s=0 (or another zero initial energy is actually known).
The omitted final energy cannot be recovered from a difference of two upper
bounds. Similarly, the error's own energy inequality gives

    integral_s^t d_e² <= eps1(s)²/(2nu)
       + (1/nu) integral_s^t [2M1 eps1²+M2 eps0 eps1+eps1 ||grad r_e||],

where r_e is the **full** residual, including the base-flow discrepancy. A
cumulative delta upper-bound increment alone is not a valid substitute.
The script does not reprocess error cells: delta is a valid absolute bound on
any subinterval. It reports one deliberately loose later-cell example using
h=T/250, K_s=K, d_st=delta, including its initial-energy contribution explicitly.
It does not sum such examples to manufacture (1). The single global integration
of (W), with zero initial energy, is what proves (1).

## 2. Generic linear estimates and the available q2 bounds

If L_U X=-F, X(0)=0, and L>=integral||F||, J>=integral||F||² on [0,T], the
parent's I1-I6 inequalities give

    ||X|| <= N_X := exp((M1-nu)T) L,
    ||grad X|| <= E_X := {exp((4M1+1)T)[M2² N_X² T+J/nu]}^(1/2),
    integral||Delta X||² <= D_X
       := (2/nu)[(2M1+1/2)E_X² T+(1/2)M2² N_X² T+J/(2nu)]. (3)

For clarity, the H1 step is
(1/2)y'+(nu/2)||Delta X||² <= (2M1+1/2)y+(1/2)M2²||X||²+||F||²/(2nu).
Discarding dissipation and applying Gronwall gives E_X; integrating that same
inequality, with zero initial energy, gives D_X. On later cells an initial
||grad X(s)||²/nu term must be added to this D_X formula. All growth rates
here are positive for the fixed parameters; e^{-(M1-nu)s}<=1 is legitimate.

The Taylor coefficient convention is L_U q2=-B(q1,q1), q2(0)=0: q2 is half
the second b-derivative. The original analytic Lemma 3 remains valid without
smallness of b, but its T=1/4 bounds N2<=330.47, Q2<=7631.7, D2<=5.9394e8 are
large. No new q2 approximation is needed to improve them: use

    L_sigma=T sigma+C eps1 sqrt(T delta),
    J_sigma=2[T sigma²+C² eps1² delta]

in (3), giving new N2,Q2,D2. These optional q2 estimates are reported for
comparison. **The observable estimate below uses q2's equation and Fourier
support only, not these norm bounds.**

## 3. Direct estimate of the full second-order field remainder

Define r=w-b²q2, including both its mean and oscillating parts. Exactly,

    L_U r = -b[B(q1,w)+B(w,q1)]-B(w,w),  r(0)=0.            (4)

Let z_w=||Delta w||/b² for b!=0; (1) bounds its squared time integral by D_w.
Using q1=qN+e, the five source terms have the bounds

    ||B(qN,w)||/b² <= p K,
    ||B(w,qN)||/b² <= n1 N,
    ||B(e,w)||/b² <= C K d_e,
    ||B(w,e)||/b² <= C eps1 z_w,
    ||B(w,w)||/b⁴ <= C K z_w.

These use the L2 contraction of P and the mean-zero Agmon inequality
||X||_infty<=C||Delta X||. Thus the source in (4), divided by |b|³, is bounded by

    A+C K d_e+H z_w,  A=p K+n1 N,  H=C(eps1+beta K).

Consequently Cauchy-Schwarz and (x+y+z)²<=3(x²+y²+z²) give

    L_r=A T+C K sqrt(T delta)+H sqrt(T D_w),
    J_r=3[A² T+C² K² delta+H² D_w].                         (5)

Apply (3) to the scaled equation, obtaining N_r,E_r,D_r, so
||r||<=|b|³N_r, ||grad r||<=|b|³E_r,
integral||Delta r||²<=b⁶D_r. These are bounds on the full r, not only its oscillating part.
At b=0 the fields vanish, with the same interpretation as in (1).

## 4. The extra order for the mean and the observable

Since U is z-independent, L_U and P preserve each z Fourier mode and commute
with z-averaging. q1 has only k_z=+/-1, and q2 has only 0,+/-2. Therefore the
z-means of B(q1,q2) and B(q2,q1) vanish. Substituting w=b²q2+r into just the
terms linear in w in (4) gives the exact mean equation

    L_U bar(r)=-b overline[B(q1,r)+B(r,q1)]-overline[B(w,w)]. (6)

It follows, by the same decomposition q1=qN+e, that its forcing divided by b⁴
has L1-in-time bound

    L_bar = (p E_r+n1 N_r)T
             +C E_r sqrt(T delta)
             +C eps1 sqrt(T D_r)
             +C K sqrt(T D_w).

The z-average is an L2 contraction. Equation (3)'s L2 estimate gives

    ||bar(r)|| <= b⁴ N_bar,  N_bar=exp((M1-nu)T)L_bar.       (7)

This is the needed mean cancellation. Evenness of the scalar enstrophy in b
by itself would not justify (6), nor bound the coefficients quantitatively.
We use the actual mode support. No claim about a separate phase-onset rule
is needed or made.

Let Z2=<grad U,grad q2>+(1/2)||grad q1||² and
R_Z=Z(U+bq1+w)-Z(U)-b²Z2. Direct expansion, integration by parts, and mode
orthogonality <grad q1,grad q2>=0 give the exact identity

    R_Z=<-Delta U,bar(r)>+b<grad q1,grad r>+(1/2)||grad w||².

Combining (7), the full-r estimate and the existing S,K yields

    |R_Z(t)| <= b⁴ C_B,
    C_B=MD N_bar+S E_r+(1/2)K²,  for all t<=T, |b|<=beta.  (8)

All inputs are terminal envelopes; the integrated sources up to any earlier t
are bounded by the full-horizon sources used here. The coefficients are
nonnegative and nondecreasing in beta once the old S,K,N,eps,delta envelopes
at beta are fixed, so smaller |b| are covered uniformly. Negative b is treated
by absolute values throughout; the original translation z->z+pi also supplies
its symmetry. No monotonicity of actual trajectories in b is asserted.
This proves the proposed bound on paper conditional on the previously audited
certificate; independent review of this new argument is still required.

## 5. Evaluation, provenance and first-stage verdict

`bounds.py` is small interval postprocessing using the unmodified parent's
40-digit directed interval implementation. It verifies pinned hashes before
importing that implementation or reading inputs. It uses no trajectory reads,
NumPy, solver, network or randomness. The previously downloaded and verified
LFS arrays remain in the original isolated audit checkout; their recorded raw
array hashes travel with this output. No files were downloaded again. The
completed end-to-end reproduction at e9aa28a matched all numerical fields;
its strict checker differed only in Python-version metadata after excluding
wall time. Commit 419e6c3 changed documentation only.

Commands from this folder (Python 3.12 or 3.13; standard library only):

    python3 -B bounds.py --output results/bounds.rerun.json
    python3 -B -m unittest -v test_bounds.py

Outputs refuse overwrite. `results/bounds.json` stores full interval endpoints,
upward-rounded display values, input/source hashes, decomposed losses and the
unchanged milestone. An interval lower endpoint bounds the evaluated majorant
from below; it is **not** a lower bound on the physical norm or actual error. The adjacent log is the first evaluation. It gives:

| Quantity | Certified upper bound from this derivation |
|---|---:|
| D_w, with integral ||Delta w||² <= b⁴ D_w | 86107 |
| integral ||Delta w||² at |b|=0.003 | 6.9747e-6 |
| N2, Q2, D2 from the validated q1 source | 0.63604, 21.949, 40386 |
| N_r, E_r, D_r | 68.245, 2376.2, 4.7333e8 |
| N_bar | 20265 |
| C_B | 87807 |
| |R_Z| at |b|=0.003 | 7.1123e-6 |

Every displayed entry is separately rounded upward from its own full interval;
products of displayed bounds can therefore exceed a separately displayed
product bound. Route A's previously reproduced displayed C_Z<=1.2102e14 gives
9802.62 before display rounding at this amplitude (9.81e3 to three significant
digits); the new derived bound is 7.1123e-6. The preregistered 1e-2 milestone
is met by the interval evaluation. This is an upper bound, not a measured error,
not a sharp constant, and not a comparison with patient data.

Dependency map:

    verified qN/base residual enclosures -> old eps0,eps1,delta,S,N,K
        -> retained W2 -> D_w
        -> full-r source (5) -> N_r,E_r,D_r
        -> mode cancellation (6) -> N_bar
        -> exact observable identity -> C_B
    same q1 source -> optional analytic q2 norm bounds (not used by C_B)

There is no missing numerical input for this deliberately coarse first-stage
bound. The remaining gate is independent mathematical review. Largest loss:
W2's global K² growth contribution to D_w; then C(beta K+eps1) times the
w-dissipation in J_r, and C K sqrt(T D_w) in the mean source. The latter alone
contributes about 9353 before the mean propagator. The mean term dominates
C_B. These are identifiable inequalities, not evidence that the actual
remainder is large. Cellwise sharpening and validated q2 are optional future
work, not part of this stage. No additional stage is launched here.
