# oscillation: phase locking, from two rhythms to the triads of a turbulent field

**Checked numerically.** Nothing in this folder is proved in Lean, and nothing
in it is clinical advice. It holds the lock-map mathematics behind the
neonatal coupled-oscillator brief as runnable code with exact tests, and one
bridge from that mathematics to the periodic Navier–Stokes phase experiments
of the Helical Lab ([`../inputs/`](../inputs/)).

| File | What it does | Needs |
|---|---|---|
| [`locking.py`](locking.py) | The Adler equation and the sine circle map: lock condition, fixed phase, recovery rate, slip period, winding number, Lyapunov exponent, Arnold tongue edges, continued fractions | standard library |
| [`test_locking.py`](test_locking.py) | 11 checks of `locking.py` against the exact results in its docstring | standard library |
| [`triads.py`](triads.py) | Vortex stretching as a sum over Fourier triads, and the coherence of its terms, on the Helical Lab ensemble | numpy, the ZIP in `../inputs/` |
| [`test_triads.py`](test_triads.py) | Exact check of `triads.py` on the phase family u_φ of section 2.6 of the main index (E = 1, Z = 5/4, D = 7/2, S = cos φ/4) | numpy |
| [`results/triad_coherence.json`](results/triad_coherence.json) | Output of `triads.py` on the 63 cases of part 1 of 4 | — |

## 1. Two rhythms: the Adler equation

For two rhythms with natural frequencies ω₁, ω₂ and relative phase φ, the
simplest model of coupling is

    dφ/dt = Δω − K sin φ,      Δω = ω₁ − ω₂ (rad/s),  K = coupling (rad/s).

Exact facts, each a test in `test_locking.py`:

- **Lock** iff |Δω| < K, at the fixed phase φ* = asin(Δω/K).
- **Recovery.** A small disturbance of the lock decays at rate λ = √(K² − Δω²).
- **Slips.** Outside the lock the phase slips once every T = 2π/√(Δω² − K²).
  Just below threshold the slips are rare and each one is a single anomalous
  cycle, which is why cycle-to-cycle variability rises *before* locking is
  reached. At threshold T is infinite.

The neonatal example of the brief (`python3 locking.py`): caregiver breathing
at 12/min, infant at 51.6/min, 4:1 target, so Δω = (4·12 − 51.6)/60 · 2π =
−0.377 rad/s.

| K (rad/s) | Outcome |
|---|---|
| 0.28 | not locked; a phase slip every 24.9 s |
| 0.65 | locked at φ* = −0.62 rad; disturbances decay at 0.53 /s (time constant 1.9 s) |

These are properties of the equation. Whether a caregiver–infant pair is an
Adler pair, and what K is, are measurements nobody in this repository has made.

## 2. One rhythm pushed by another: the circle map and Arnold tongues

When one rhythm is kicked once per cycle of another, the phase at successive
kicks obeys the sine circle map

    θ_{n+1} = θ_n + Ω − (K/2π) sin 2πθ_n,

Ω the bare frequency ratio, K the kick strength. The winding number
W = lim θ_n/n is the observed ratio. Mode locking W = p/q happens on intervals
of Ω, the Arnold tongues, and `circle_tongue(p, q, K)` finds their edges by
bisection on the monotone function W(Ω) from both sides (for K ≤ 1).

Exact facts, each a test:

- The 0:1 tongue is exactly |Ω| ≤ K/2π (a fixed point exists iff
  |2πΩ/K| ≤ 1); likewise 1:1 around Ω = 1. Measured edges at K = 0.5:
  0.07958 and 0.92042 against K/2π = 0.07958.
- The width of the p/q tongue scales like K^q for small K. Doubling K
  multiplies the 1/2 width by 4.1 (exact limit 4) and the 1/3 width by 9.1
  (exact limit 8). At K = 0.8 the widths are 1/2: 0.0485, 1/3: 0.0164,
  2/5: 0.0036, 3/7: 0.0011; the 13/17 tongue is reported as 0 because the
  detector (orbit returns within 1e-7 after a 2000-step transient) cannot
  confirm a q = 17 lock there. Simple ratios lock widest; a large prime
  denominator barely locks.
- The golden mean W = (√5 − 1)/2 has continued fraction [0; 1, 1, 1, …] and is
  the last quasi-periodic orbit to survive as K → 1 (checked at K = 0.9: not
  locked, continued fraction of the measured W is [0, 1, 1, 1, 1, 1, 1, 1]).
- For K ≤ 1 the map is invertible and has no positive Lyapunov exponent;
  above K = 1 chaos appears (checked at K = 1.6).

**Relation to the Shared Air theorems** ([`../README.md`](../README.md#24-shared-air-sharedair),
sections 2.4 and 2.5). `two_to_one_moments` and
`averaged_stable_equilibrium_iff` are first-order 2:1 locking, the q = 1, 2
cases of the picture above. The model's own limit "ratios other than n:1"
([`../inputs/Shared_Air_Model_v2_revised.md`](../inputs/Shared_Air_Model_v2_revised.md))
is where the tongues take over: at the same coupling a 3:2 tongue is narrower
than 2:1 or 3:1 by a factor of order K, and the harmonic lock index cannot
tell 3:2 from 3:1 at all (`three_two_looks_like_three_one` in `Limits/Ratios.lean`).
The circle map is what the index would need to measure instead.

## 3. Many rhythms with no clock: the triads of vortex stretching

For a periodic velocity field u(x) = Σ_k û(k) e^{ik·x} with vorticity
ω̂(k) = ik × û(k), the enstrophy balance Z′ = S − νD has the stretching term

    S = ⟨ω_i ω_j ∂_j u_i⟩ = Σ_{k+p+q=0} (ω̂(k) · ip)(ω̂(q) · û(p)).

Every term c(k, p) is a complex number; the field is real so the terms pair
into conjugates and the sum is real. Writing c = |c| e^{iφ},

    S = Σ |c| cos φ,       R = |S| / Σ |c|  ∈ [0, 1].

R is the order parameter of the triad phases in the Kuramoto sense: 1 when
every term pulls the same way, 0 when they cancel completely. The simplest
case is the phase family of section 2.6 of the main index,
u_φ = (sin y, sin z, cos x − cos(x + y + φ)), where S = cos φ/4 with E, Z, D
fixed. `test_triads.py` recovers E = 1, Z = 5/4, D = 7/2 and S = cos φ/4 from
the sampled field to 2e-15, and finds Σ|c| = 3/4 for every φ, so on this
family R = |cos φ|/3: even its most coherent member (φ = 0) has R = 1/3,
because some of its triad terms oppose each other at every phase. R = 1 is
the algebraic ceiling, not a value real fields approach. The Helical Lab's
phase-only ensembles are the many-triad
case: each case keeps every Fourier magnitude (hence E, Z, D, H) and draws the
phases at random, so at t = 0 the triad phases are as incoherent as the
construction allows, and whatever the dynamics do to R by t = 0.5 is the
question `triads.py` measures. The lab's own channels (`features.csv`:
S split by helicity sign and low/high band) are sums over classes of triads;
R is the same sum with absolute values in the denominator, so it says how much
cancellation sits inside the total S, something the classed sums cannot.

`triads.py` reconstructs the full spectrum from the saved rfft snapshots,
recomputes E, Z, D and S exactly, checks them against the ensemble's own
`diagnostics.csv` / `checks.json` / `result.json` where part 1 contains them,
and reports R at t = 0 and t = T with correlations against S and ΔZ.

### Results on part 1 of 4 (63 cases with snapshots, N = 24, ν = 1/28, T = 0.5)

Checked against the ensemble's own files on the 23 cases that have them in
this part: E, Z, D and S agree at both times to 2.5e-14 at worst, and ΔZ
agrees with `result.json` to 1.3e-15. Every case has E = 1 at t = 0.

| | t = 0 | t = 0.5 |
|---|---|---|
| R, mean (min … max) | 0.038 (0.002 … 0.131) | 0.114 (0.077 … 0.156) |
| S, mean | −0.025 | +0.999 |
| cases with S > 0 | 26 of 63 | 63 of 63 |
| Σ\|c\|, mean | 2.68 | 9.28 |

- At t = 0 the random phases do what they should: S is small and as often
  negative as positive, and R is a few percent, meaning the triad terms
  cancel almost completely.
- By t = 0.5 every case has S > 0 and R has tripled; 62 of 63 cases have
  R(0.5) > R(0). The dynamics push the triad phases toward positive
  stretching whichever sign they started with. That is the familiar tendency
  of three-dimensional flow to produce enstrophy, seen here as a statement
  about phases rather than magnitudes. But R stays near 0.11: nine tenths of
  the triad magnitude still cancels, where the phase family's most coherent
  member reaches 1/3.
- Σ|c| triples because energy moves to larger wavenumbers, where the triad
  terms are larger. R is the part of the growth of S that this does not
  explain.
- Correlations across the 63 cases with ΔZ = Z(0.5) − Z(0): S(0) +0.89,
  R(0.5) +0.80, R(0) −0.39; and R(0) with R(0.5) −0.35. The first is the
  baseline the lab's forecast test already uses (initial stretching). The
  second is not a forecast, since it uses the final state. R(0) is
  sign-blind, so its negative correlations say only that the cases with the
  largest |S(0)| were mostly the negative ones; R(0) adds nothing to S(0) as
  a predictor, which is consistent with the lab's negative result.
- By profile: `flat` (30 cases) R 0.043 → 0.100, S −0.044 → +1.43,
  ΔZ +0.013; `kminus2` (33 cases) R 0.034 → 0.126, S −0.007 → +0.61,
  ΔZ +0.057. The flat spectrum stretches more but also dissipates more
  (νD), so it gains less enstrophy.

Run time: 414 s for 126 field evaluations with 4 workers, about 13 s per
field. The run that produced the JSON was the second. The first treated the
snapshots as raw `rfftn` output instead of coefficients, and truncated the
wavenumber 7 to 6 because `fftfreq(24)·24` gives 6.999999999999999; both
errors were caught by the comparison with `diagnostics.csv`, which is why the
script keeps that comparison.

### What this is and is not

- The triad sum is an **identity at one instant** on given data. It is not a
  model of the dynamics. Periodic Navier–Stokes has no linear dispersion
  relation, so the triad phases have no natural frequencies and nothing
  "locks"; the Kuramoto analogy is to the order parameter as a measure of
  cancellation, not to the Kuramoto equations.
- R is one number per field. The lab's exact obstruction
  ([`../inputs/helical_lab_phase_organization_prediction_and_exact_obstruction.pdf`](https://github.com/rafaellemus92/NICU-Math/blob/0c3fe5d167059856ed78ec343ed99bf31114e7a1/math/inputs/helical_lab_phase_organization_prediction_and_exact_obstruction.pdf))
  shows that no finite set of such t = 0 numbers can determine the enstrophy
  curve, and the lab's forecast test found no held-out gain from its six
  channels. Nothing here overturns either result.
- Nothing here bears on regularity. N = 24 and T = 0.5 is a short time on a
  coarse grid.
- The uploaded `Oscillators.d.ts` is the TypeScript declaration of Three.js's
  shader oscillator nodes (sine, square, triangle, sawtooth of a time node)
  and has nothing to do with any of this; it is not included.

## Running

From this folder. Python 3 (tests run on 3.11.17); `triads.py` needs numpy.

```sh
python3 test_locking.py          # 11 checks, prints ALL PASS; 1.7 s
python3 locking.py               # the neonatal example; instant
python3 test_triads.py           # the phase family to 2e-15; 2 s

# The ensemble ZIP is other people's code: extract it into its own new folder
# and run with -I so nothing is imported from it.
mkdir -p /tmp/helical && unzip -q ../inputs/helical_lab_quartic_phase_experiment_part1of4.zip -d /tmp/helical
python3 -I triads.py /tmp/helical/helical_lab/results/phase3/ensemble results/triad_coherence.json 4   # 4 workers, about 7 min
```

The saved JSON was produced with Python 3.11.17 and numpy 2.4.6.

The additional uploaded PDFs/ensemble ZIP on the source branch were not copied
into this consolidation; their licensing was not established. The optional ZIP
command above requires that original source artifact and is not a smoke test.
The scripts and previously saved numerical results are retained.
