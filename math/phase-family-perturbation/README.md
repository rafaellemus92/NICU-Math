# phase-family-perturbation: the reduced family, the b² structure, and what an explicit bound costs

**Checked numerically**, with one analytic argument (section 1) that was
reviewed independently and is reproduced here; it is not a Lean theorem.
Nothing here is a regularity result, and nothing here is clinical.

The family is the periodic initial velocity

    u₀ = (a sin y, b sin z, c cos x − d cos(x + y + φ)),   ν ≥ 0,

with E = ½⟨|u|²⟩, Z = ½⟨|ω|²⟩, D = ⟨|∇ω|²⟩, S = ⟨ω_i ω_j ∂_j u_i⟩ as volume
averages over the 2π-cube, so that Z′ = S − νD. With a = b = c = d = 1 it is the
phase family of [section 2.6 of the math index](../README.md#26-periodic-navierstokes-periodicns)
and of the [ns-phase-audit](../ns-phase-audit/).

| File | What it does | Needs |
|---|---|---|
| [`reduced_family.py`](reduced_family.py) | b = 0: integrates the one-dimensional equation for the x-mode of w; checks the inviscid closed form for Z and the absence of higher φ-harmonics with viscosity | numpy |
| [`full_family_dns.py`](full_family_dns.py) | b ≠ 0: 3D pseudo-spectral Navier–Stokes (2/3 dealiasing, Leray projection, Lawson RK4); prints the φ-harmonics of E, Z, D, S over time for several b | numpy |
| [`perturbation_growth.py`](perturbation_growth.py) | Measured growth of u_b − u₀ in L² and H¹, to set beside the Grönwall factors | numpy |
| [`reduced_family_t20.py`](reduced_family_t20.py) | b = 0 on the long run's time grid, eight phases, to t = 20 | numpy |
| [`measured_constants.py`](measured_constants.py) | The measured constants of the b² bound from the long run and the b = 0 baseline | numpy |
| [`crosscheck_variational.py`](crosscheck_variational.py) | The finite-b harmonics at T = 0.5 against the archive's direct integration of the variational equations (section 6) | standard library |
| [`exact_nu_poly_amp.py`](exact_nu_poly_amp.py) | The audit's exact rational Taylor jet ([`../ns-phase-audit/audit_v2/code_audit/exact_nu_poly.py`](../ns-phase-audit/audit_v2/code_audit/exact_nu_poly.py)) with the four amplitudes as command-line rationals | standard library |
| [`base_flow_norms.py`](base_flow_norms.py) | Sup norms of the b = 0 flow over time and the integrals that an explicit perturbation bound needs | numpy |
| [`agmon_constant.py`](agmon_constant.py) | The constant in ‖f‖_∞ ≤ C_A ‖∇f‖^{1/2} ‖Δf‖^{1/2} on the torus, from lattice sums | numpy |
| [`results/`](results/) | Every output quoted below | — |

## 1. The reduced family (b = 0): exactly two phase harmonics, for all time

**Claim.** For b = 0 and any ν ≥ 0 the solution is smooth for all time and

    E(t, φ) = A_E(t) + B_E(t) cos φ,   Z(t, φ) = A_Z(t) + B_Z(t) cos φ,   S(t, φ) = A_S(t) + B_S(t) cos φ,

with no higher harmonic and no sine term, for the full evolution and not only
through the Taylor orders computed in the audit (its statement P1). For ν = 0,

    Z(t, φ) = (a² + c² + 2d²)/4 + (acd/4) t cos φ + (a²(c² + d²)/8) t².

**Why.** Nothing depends on z, so u = (U(y,t), 0, w(x,y,t)) and the pressure
does not depend on z. The horizontal shear decouples: U_t = ν U_yy, so
U = a e^{−νt} sin y. The vertical velocity then solves the linear
advection–diffusion equation w_t + U w_x = νΔw with x-independent coefficients,
so its single x-mode is preserved: w = Re[ŵ(y,t) e^{ix}] with
ŵ_t + iUŵ = ν(ŵ_yy − ŵ). Linearity gives ŵ = c·g − d·e^{iφ}·h for two solutions
g, h that do not depend on φ, so every quadratic average is a quadratic form in
(1, e^{iφ}) and contains only the constant and the first harmonic. The point
reflection (x, y) → (−x, −y) maps the φ member to the −φ member and leaves the
averages fixed, so the sine part vanishes. The stretching reduces to
S = −⟨U′ w_x w_y⟩, also quadratic in w, so it has the same structure; its
initial value is acd cos φ/4, the same cos φ/4 the full family has at t = 0. For
ν = 0 the characteristics give w(x, y, t) = w₀(x − at sin y, y), and the averages
of w_x², w_y² and U′² give the formula above term by term.

**Checked** (`results/reduced_family.out.txt`): the inviscid formula to 4e-15 at
t = 0.5, 1, 2 with a = c = d = 1, and to 4e-16 with (a, c, d) = (0.7, 1.3, 0.4);
with ν = 1/28 the cos 2φ, cos 3φ, cos 4φ and all sine coefficients of E, Z and S
are below 2e-15 at t = 0.5 and t = 2; B_E is O(ν), with B_E/ν → about −1/4 at t = 1.

Two remarks. With ν = 0 the enstrophy grows like t² forever and nothing blows
up; the family is harmless because the shear stretches w's gradients linearly
in time and nothing feeds back. And the restriction is the whole point: the
b sin z mode is what makes w's x-frequency decay into other modes.

## 2. Restoring b sin z: the b² structure

**Symmetry.** Replacing b by −b is the translation z → z + π of the initial
data, so by uniqueness u_{−b}(x, y, z, t) = u_b(x, y, z + π, t), and every
spatial average is an even function of b. Linear terms in b vanish, and the
higher harmonics, which vanish at b = 0 by section 1, are O(b²) as long as the
solution depends smoothly on b.

**Which monomial.** Counting wavevectors in the Taylor jet: a cos 2φ term needs
two d-modes with the same sign of φ, wavevector (2, 2, 0), cancelled by at least
two c-modes in x and two a-modes in y, and b-modes in pairs, at least one pair
since there is no cos 2φ at b = 0. The lowest amplitude degree is 8, which is
the ν-free part of the t⁶ coefficient (the audit's grading: amplitude degree
plus power of ν equals order plus 2). So the leading second harmonic is a single
monomial, and likewise the leading third harmonic at t⁹ with three d, three c,
three a and two b:

    [cos 2φ] Z = −(6487/1555200) a²b²c²d² t⁶ + (207269/7257600) ν a²b²c²d² t⁷ + O(t⁸),
    [cos 3φ] Z = −(21381938959/105921623808000) a³b²c³d³ t⁹ + O(t¹⁰).

**Checked exactly** (`results/jet9_unit.json`, `results/jet9_generic.json`):
the jet with amplitudes (a, b, c, d) = (1/2, 1/3, 2, 1/5) reproduces the unit
coefficients times (abcd)² at t⁶ (ν⁰), t⁷ (ν¹), t⁸ (ν²) and t⁹ (ν³), and times
a³b²c³d³ for the t⁹ cos 3φ term, as exact rationals. From t⁸ on the ν-free
coefficients are polynomials of degree 10 and contain b⁴: the ratio at t⁸ is
0.01210 against (abcd)² = 0.00444. So the b² law is exact at leading order and
acquires b⁴ corrections at order t⁸, which is what the simulations see.

**Checked by simulation** (`results/full_family_dns.log`, N = 24, ν = 1/28,
eight phases, a = c = d = 1; the dealiasing cutoff is the strict one,
K = (N − 1)/3 = 7, so that 3K < N and the cubic product in S is averaged
exactly on the grid; an earlier version of these runs used K = N/3 = 8, which
lets the boundary shell alias, and changed the numbers below in the seventh
digit). The cos 2φ coefficient of Z:

| t | b = 1 | b = 1/2 | b = 1/4 | b = 0 | ratio 1 : 1/2 | prediction for b = 1 |
|---|---|---|---|---|---|---|
| 0.1 | −4.050e-9 | −1.013e-9 | −2.534e-10 | 1e-16 | 4.00 | −4.069e-9 |
| 0.5 | −5.146e-5 | −1.312e-5 | −3.298e-6 | 3e-16 | 3.92 | −5.721e-5 |
| 1.0 | −2.213e-3 | −5.908e-4 | −1.501e-4 | 6e-16 | 3.75 | −3.151e-3 |

The prediction is the t⁶ and t⁷ terms alone; at t = 0.1 it is within 0.5%, and
the departure at later times is the higher orders, not b⁴, since the ratios for
1/2 : 1/4 stay at 3.98 and 3.93. The cos 2φ coefficient of S is larger and
earlier, −2.42e-7 at t = 0.1 for b = 1 against the leading-order value
6·(−6487/1555200)·t⁵ = −2.50e-7 (and −2.43e-7 with the ν t⁶ term), with the
same ratio 4.00 between b = 1 and b = 1/2. The cos 3φ coefficient of Z at
t = 1 is −7.3e-5, −2.2e-5, −5.7e-6 for b = 1, 1/2, 1/4. At b = 0 every higher
harmonic is at rounding, so the three-dimensional code reproduces section 1;
its b = 0 values of Z and S agree with the one-dimensional solver to 1e-8.

## 3. The perturbative bound: what is true, and what its constants are

### 3.1 The statement, with the quantifiers improved for ν > 0

The reviewed argument gives: for fixed ν > 0 and any finite T there is
b₀(T) > 0 such that for |b| < b₀(T) the solution is smooth through T and the
higher phase harmonics of E, Z, S are bounded by C_T b² on [0, T], with the
worry that C_T may grow and b₀(T) shrink as T grows.

For this base flow that worry does not arise. The b = 0 solution decays:
‖∇u₀(t)‖_∞ rises from 2.45 to 4.10 near t = 2.4 and is 6e-7 by t = 400
(`results/base_flow_norms_a1.out.txt`), and its time integral converges,

    I₁ = ∫₀^∞ ‖∇u₀‖_∞ dt = 44.2 (φ = 0), 47.0 (φ = π/2), 45.5 (φ = π),

as does ∫₀^∞ ‖∇²u₀‖_∞ dt = 93.3. A global strong solution whose gradient is
integrable in time is stable under small perturbations for all time: this is
the global stability theorem for strong solutions of three-dimensional
Navier–Stokes (Ponce, Racke, Sideris and Titi, Comm. Math. Phys. 1994;
Gallagher, Iftimie and Planchon, 2003, in the scale-invariant setting), whose
proof is the Grönwall argument of 3.2. So for ν > 0 there is a single b₀ > 0
and a single C such that for |b| < b₀ the solution is smooth for all t ≥ 0 and
every harmonic of order two and higher is bounded by C b² for all t ≥ 0.

For ν = 0 the worry is exactly right: ‖∇u₀‖_∞ grows like at (the inviscid
w_y), ∫₀ᵀ ‖∇u₀‖_∞ grows like T², the constants grow like exp(T²), and no
uniform b₀ comes out of this argument.

### 3.2 The explicit version

All norms are L² on [0, 2π)³, fields are mean-zero and divergence-free, so
‖f‖ ≤ ‖∇f‖ ≤ ‖Δf‖ (Poincaré, since |k| ≥ 1) and ‖f‖_∞ ≤ C_A ‖∇f‖^{1/2}‖Δf‖^{1/2}
with C_A ≤ 0.47 (`agmon_constant.py`: lattice sums enumerated to |k| ≤ 60, tail
bounded by its shell integral with a 10% margin; the asymptotic value is 0.45).
Let v = u_b − u₀, which satisfies

    v_t + (u₀·∇)v + (v·∇)u₀ + (v·∇)v + ∇q = νΔv,   v(0) = b sin z e_y,

with ‖v(0)‖² = ‖∇v(0)‖² = b² (2π)³/2.

*Energy.* ½ d/dt‖v‖² + ν‖∇v‖² = −⟨(v·∇)u₀, v⟩ ≤ ‖∇u₀‖_∞ ‖v‖², so for every b
and every t ≥ 0,

    ‖v(t)‖ ≤ ‖v(0)‖ exp(∫₀ᵗ ‖∇u₀‖_∞) ≤ |b| · 11.1 · e^{I₁(t)}.

No smallness is needed here; e^{I₁} is 10^{19.2} at a = c = d = 1.

*Enstrophy.* Take the inner product with −Δv. Integrating the two linear terms
by parts once (the transport part drops by skew-symmetry) gives
|⟨(u₀·∇)v, Δv⟩| ≤ ‖∇u₀‖_∞‖∇v‖² and
|⟨(v·∇)u₀, Δv⟩| ≤ (‖∇u₀‖_∞ + ‖∇²u₀‖_∞)‖∇v‖²; the nonlinear term is bounded by
‖v‖_∞‖∇v‖‖Δv‖ ≤ C_A‖∇v‖^{3/2}‖Δv‖^{3/2}, and the pressure term vanishes. With
y = ‖∇v‖², G(t) = 2‖∇u₀‖_∞ + ‖∇²u₀‖_∞ and Young's inequality on the nonlinear
term (exponents 4/3 and 4, half the dissipation absorbed),

    y′ ≤ (2G(t) − ν) y + β y³,   β = 27 C_A⁴ / (16 ν³).

The Bernoulli comparison with Φ(t) = exp ∫₀ᵗ (2G − ν) gives

    y(t) ≤ y₀ Φ(t) / √(1 − 2β y₀² J(t)),   J(t) = ∫₀ᵗ Φ²,

for as long as the root is real, and the solution is global if 2β y₀² J(∞) < 1,
that is

    |b| < b₀ := ( (2π)⁶ β J(∞) / 2 )^{−1/4}.

Since G → 0 exponentially, Φ eventually decays like e^{−νt} and J(∞) is finite.

*Harmonics.* Write v = v^o + v^e for the parts odd and even under z → z + π.
The symmetry makes v^o odd in b and v^e even in b, and v^e(0) = 0 because sin z
is odd. Then Z_b − Z₀ = ⟨ω₀, ω_{v^e}⟩ + ½‖ω_v‖², because ω₀ has only the z-mode 0
and is orthogonal to odd fields. The second term is ≤ ½ y(t). The even part
solves the linearized equation with the quadratic source P[(v^o·∇)v^o + (v^e·∇)v^e]
and zero initial data, so ‖∇v^e‖ is O(b²) by one more Grönwall estimate with the
same G and the dissipation integral of y; its constants are of the same size as
those above. The same decomposition handles E and, with one more derivative, S.

### 3.3 The constants, evaluated

`base_flow_norms.py` integrates the reduced equation to t = 400 and evaluates
the exponents; `results/base_flow_norms_a*.out.txt` has the full tables. With
ν = 1/28, φ = 0:

| a = c = d | max ‖∇u₀‖_∞ | I₁ | ∫‖∇²u₀‖_∞ | ∫(2G − ν) | log₁₀ max_t Φ | log₁₀ J(∞) | b₀ |
|---|---|---|---|---|---|---|---|
| 1 | 4.10 at t = 2.4 | 44.2 | 93.3 | 349 | 155 (at t ≈ 140) | 312 | 10⁻⁸⁰ |
| 0.3 | 0.82 at t = 3.2 | 14.5 | 23.1 | 90 | 43 | 88 | 10⁻²⁴ |
| 0.1 | 0.25 at t = 0 | 5.0 | 6.2 | 18 | 12.5 | 27 | 2.5·10⁻⁹ |

(β = 1777 at ν = 1/28, and the other two phases change the exponents by under 6%.)
The time dependence of the factor Φ at a = c = d = 1: log₁₀ Φ is 8.6 at t = 1,
22 at t = 2, 71 at t = 5, 99 at t = 10, 121 at t = 20, 145 at t = 50, 155 at
t = 100, after which it decays.

### 3.4 Against what the flow does

`perturbation_growth.py` integrates u_b and u₀ side by side (φ = 0, N = 24,
ν = 1/28, a = c = d = 1) and reports ‖v‖²/‖v(0)‖² and ‖∇v‖²/‖∇v(0)‖²
(`results/growth_b0.1.log`, `results/growth_b1.0.log`):

| | energy ratio | enstrophy ratio | the bound's factor at the same time |
|---|---|---|---|
| b = 0.1, t = 2 | 5.8 | 29 | Φ(2) = 10²² |
| b = 0.1, t = 4.5 (enstrophy peak) | 49 | 426 | Φ(4.5) ≈ 10⁶⁵ |
| b = 0.1, t = 10 (energy peak) | 56 | 144 | e^{2I₁(10)} = 10²¹, Φ(10) = 10⁹⁹ |
| b = 0.1, t = 20 | 26 | 40 | |
| b = 1, t = 2.5 (peak) | 4.1 | 15 | |
| b = 1, t = 20 | 0.26 | 0.31 | |

So the linearized evolution around u₀ does amplify a small perturbation,
by a factor of about 20 in amplitude (426 in enstrophy) over the first five
time units, through the shear and the growing gradients of w, and then
everything decays. The Grönwall factor at the same moment is 10⁶⁵. At b = 1
the perturbation is nonlinear from the start, grows less in relative terms,
and is below its initial size by t = 10. The run to t = 20 with eight phases
(`results/long_b.log`), set against the b = 0 flow on the same time grid
(`reduced_family_t20.py`, `results/reduced_family_t20.out.txt`), gives the
measured constants of the bound (`measured_constants.py`,
`results/measured_constants.out.txt`). Per b², with the time of the maximum:

| | b = 1/4 | b = 1 |
|---|---|---|
| sup_t \|cos 2φ coefficient of Z\| / b² | 0.55 (t = 6) | 0.11 (t = 3) |
| sup_t \|cos 3φ coefficient of Z\| / b² | 0.17 (t = 4.5) | 0.009 (t = 5.5) |
| sup_t \|cos 2φ coefficient of S\| / b² | 0.48 (t = 4) | 0.14 (t = 2.5) |
| sup_t (φ-mean of S_b − S₀) / b² | 2.0 (t = 3.5) | 0.9 (t = 2.5) |
| sup_t (φ-mean of Z_b − Z₀) / b² | 2.0 (t = 8) | 0.9 (t = 2.5) |
| ∫₀²⁰ (φ-mean of S_b − S₀) dt / b² | 15.0 | 4.2 |

For comparison, ∫₀²⁰ S₀ dt = 2.62 and the first harmonic of Z₀ peaks at 0.25.
Three things follow. The constant of the harmonic bound is of order one, not
small: at b = 1/4 the second harmonic of Z reaches 0.55 b² = 0.034, a sixth of
the first harmonic, by t = 6. The b² law holds at b = 1 only to about t = 1;
after that the second harmonic saturates, at 0.11 instead of the 0.55 the
quadratic law would give (the ratio of the b = 1 value to sixteen times the
b = 1/4 value is 0.98 at t = 0.5, 0.92 at t = 1, 0.76 at t = 2, 0.51 at t = 3,
0.20 at t = 4). And the restored mode does sustain stretching for a while:
at b = 1/4 the φ-averaged stretching at t = 8 is three times the base flow's,
and the accumulated extra stretching over [0, 20] is 0.94, a third of the base
flow's 2.62; at b = 1 it is 4.2, more than the base flow's own. The reported observables decrease by t ≈ 15 in these sampled runs;
this does not exclude earlier transient growth or certify continuum decay. One more observation that belongs to the
reduced family itself: the cos φ coefficient of Z changes sign near t = 3.4
at b = 0, so the member that gains enstrophy fastest at first (cos φ = 1) has
the least by t = 4; the restored mode does not cause this.

### 3.5 What this says about the next step

The canonical all-time note gives an unrefereed paper argument applying known
large-solution stability, with symbolic constants. The sampled sufficient
smallness estimates here are conservative and uncertified; there is no basis
for saying that a theorem is “wrong by eighty orders.” A ceiling on a
sufficient-condition threshold is an upper bound, not a usable sufficient
radius or a stability boundary. Finite-b simulations do not determine any of
these quantities. A rigorously enclosed linearized propagator is a possible
future approach to sharper estimates; the measured amplification is not such
an enclosure and does not establish that this approach reaches b = 1.

## 6. Cross-check with the all-time phase response note

A separate package, "all-time phase response" (Codex, 18 October; branch
`codex/all-time-phase-response`, folder `math/all-time-phase-response/`),
presents an unrefereed paper argument for the small-b statement with symbolic constants and, instead of
finite-b simulations, integrates the variational equations for the first and
second coefficients q₁, q₂ directly and reports the φ-harmonics of the b²
coefficients (E₂, Z₂, S₂) at T = 0.5, N = 24, twelve phases. Its nine tests
and its remainder check (raw quartic ratios 15.9986 to 15.9993, i.e. the
error after subtracting the b² term scales as b⁴) reproduce on this machine.
Two things in its README about this folder were right and are fixed here:
the "10⁻⁸⁰ is safe" wording (now "evaluated, not certified", above) and the
dealiasing cutoff (section 2).

`crosscheck_variational.py` sets its coefficients against this folder's
finite-b harmonics (O_b − O₀)/b² at the same T, from `results/long_b.json`
and the b = 0 baseline. Ratio of this folder's value to the archive's:

| harmonic | E, b = 1/4 | Z, b = 1/4 | S, b = 1/4 | E, b = 1 | Z, b = 1 | S, b = 1 |
|---|---|---|---|---|---|---|
| m = 0 (φ-mean) | 1.000 | 1.000 | 1.001 | 1.000 | 1.002 | 1.018 |
| m = 1 (cos φ) | 0.998 | 0.997 | 0.995 | 0.970 | 0.956 | 0.926 |
| m = 2 (cos 2φ) | 0.999 | 0.998 | 0.998 | 0.979 | 0.974 | 0.965 |
| m = 3 (cos 3φ) | 0.997 | 0.997 | 0.996 | 0.957 | 0.948 | 0.937 |

The finite-b quotient (O_b − O₀)/b² and the variational coefficient agree
within about 0.5% in this stored comparison at b = 1/4. Moving from b = 1/4
to b = 1 multiplies b² by 16, so roughly sixteenfold growth of the quotient's
deviation is consistent with an O(b²) normalized error (an O(b⁴) raw remainder).
This is empirical finite-grid scaling, not a theorem prediction at b = 1,
which lies outside the theorem's justified smallness regime. Likewise the
separate ratios near 16 obtained by halving b in raw remainders test quartic
local behavior of a smooth discrete map, not an all-time or continuum bound. The values in
`results/crosscheck_variational.out.txt` are the ones in this table.

## Running

The commands below are historical reproduction recipes, not a request for a
new campaign. Some scripts write fixed paths internally. First copy this whole
folder into a fresh scratch directory; all redirected and internally written
outputs then stay outside the repository. Keep the original archive unchanged.
Python 3 with numpy; the exact jet and cross-check use the standard library.

```sh
phase_scratch=$(mktemp -d /tmp/nicu-phase-rerun.XXXXXX)
cp -R math/phase-family-perturbation "$phase_scratch/study"  # from repository root
cd "$phase_scratch/study"
python3 reduced_family.py > results/reduced_family.out.txt          # 1 min
python3 full_family_dns.py 24 0.03571428571428571 1.0 0.002 1.0 0.5 0.25 0.0 > results/full_family_dns.log   # 5 min
SAVE=0.5 OUT=results/long_b.json python3 full_family_dns.py 24 0.03571428571428571 20.0 0.005 0.25 1.0 > results/long_b.log
python3 perturbation_growth.py 0.1 20 0.005 > results/growth_b0.1.log          # also 1.0; 2 min each
python3 reduced_family_t20.py > results/reduced_family_t20.out.txt            # 1 min
python3 measured_constants.py > results/measured_constants.out.txt
python3 crosscheck_variational.py > results/crosscheck_variational.out.txt   # reads results/atpr_refined.json
python3 exact_nu_poly_amp.py 9 results/jet9_unit.json                       # 3 min
python3 exact_nu_poly_amp.py 9 results/jet9_generic.json a=1/2 b=1/3 c=2 d=1/5
python3 base_flow_norms.py 1 > results/base_flow_norms_a1.out.txt           # 30 s; also 0.3 and 0.1
python3 agmon_constant.py > results/agmon_constant.out.txt
```

The saved outputs were produced with Python 3.11.17 and numpy 2.4.6.

## What is not claimed

- Section 1 is an analytic argument checked numerically, not a Lean theorem.
- Section 3 proves nothing about b = 1. Its chain of inequalities is standard,
  but the constants in 3.3 are evaluated, not certified: the sup norms are
  sampled from a numerical solution, the Agmon constant is a numerically
  summed lattice sum with a margin, and no truncation or tail error is
  enclosed. So "|b| < 10⁻⁸⁰" is what the evaluated chain gives, not a
  certified radius; a certification requires rigorous enclosures; no ordering of the unknown true radius follows from these sampled estimates. The
  finite-grid simulations remain resolved on the computed interval at b = 1;
  that is neither a continuum certificate nor a statement about a radius.
- Harmonics in the initial phase φ are one-parameter information. Bounding
  them does not bound fine spatial scales, and nothing here bears on the
  regularity problem.

## Reconciliation scope note

The finite-b runs are empirical finite-grid observations, outside the tiny
smallness interval of the symbolic all-time theorem. The theorem applies known
large-solution stability; novelty is not established. A decaying exponential
upper envelope permits transient growth of the trajectory. Evenness in b
does not independently prove the separate 3|m| phase-onset rule. See the
canonical [all-time package](../all-time-phase-response/README.md) and its
checked radius-ceiling script. Neither an upper ceiling nor the evaluated
1e−80 in this study is a certified usable radius or stability boundary.
