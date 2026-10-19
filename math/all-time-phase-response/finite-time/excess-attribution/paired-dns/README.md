# Paired DNS mechanism attribution

Numerical evidence at **b = ±0.003 only**: excess stretching is positive and
exceeds positive excess dissipation. This supports enhanced stretching rather
than dissipation suppression for these runs. It does not certify either sign
throughout the continuum interval 0 < |b| ≤ 0.003.

Owner: Codex. Local branch `codex/enstrophy-excess-attribution`; source base
`4e86fa995243c3a428a253ee3333eb42251cd85f`. The implementation and preregistration
were frozen in [FREEZE.json](FREEZE.json) before the pilot. Original solver,
prior attribution note, and archived certificate outputs are unchanged.

## Definitions and method

On the periodic three-torus, use normalized spatial averages, Z=||curl u||²/2,
Q=<omega_i omega_j partial_j u_i>, and D=||grad curl u||²=||Delta u||².
For the documented fixed family, a=c=d=1, nu=1/28, phi=0.37, T=0.25:

- H=Z(u_b)-Z(U)-b² exp(-2 nu t)/4.
- S=integral(Q_b-Q_U).
- R=integral(D_b-D_U-b² exp(-2 nu t)/2).
- Exact balance: H=S-nu R, with H(0)=H′(0)=0.

Three fields U,u_+,u_- evolve together with the inherited pseudospectral RK4
solver. Strict cube dealiasing uses K=floor((N-1)/3), N>3K; half-spectrum
Parseval weights are retained. Accumulation uses RK4 stage weights and exact
heat-loss subtraction. Expanded differences reduce cancellation. Their direct
comparison is an algebraic check sharing nonlinear RHS values; a separately
computed physical trilinear diagnostic checks Q at initialization, every ten
steps, and the endpoint. Every-step trapezoid accumulation supplies a distinct
quadrature comparison. Initial analytic checks include Q(U)=cos(phi)/4,
Z(u_b)-Z(U)=b²/4, D(u_b)-D(U)=b²/2 and the isolated heat mode.

## Endpoints and acceptance

Values below use N=32, dt=0.0025. All quantities are nondimensional.

| b | S/b² | nu R/b² | H/b² |
| --- | ---: | ---: | ---: |
| +0.003 | 0.021470340460231926 | 0.00045698606806878134 | 0.021013354331102657 |
| -0.003 | 0.021470340460176474 | 0.00045698606806715860 | 0.021013354331018990 |

Full runs used (N,dt)=(24,0.0025),(24,0.00125),(32,0.0025).
Maximum temporal/spatial changes in S/b² were 3.325e-13/4.434e-13;
in nu R/b², 2.806e-13/1.062e-13, below the preregistered 1e-4 threshold.
The maximum scaled balance residual was 1.394e-10 (threshold 1e-5).
Direct/expanded discrepancy was 6.134e-11, independent trilinear/RHS discrepancy
3.084e-11, parity discrepancy 1.301e-13, spectral divergence 1.607e-17,
and high-mode enstrophy fraction 4.263e-13.

The largest measured error indicator was the stage/trapezoid difference,
9.974e-8. Both signed contributions exceed ten times this scale. This is an
empirical comparison, not a rigorous error enclosure; tiny refinement changes
are not a continuum accuracy certificate. No monotonicity, general regularity,
novelty, clinical claim, or sign at untested amplitudes follows. The separate
conditional endpoint certificate concerns H, not the individual mechanisms.

## Evidence and resource record

- [Clean figure, PNG](figures/attribution_timeseries.clean.png) and
  [SVG](figures/attribution_timeseries.clean.svg); original plots also retained.
- [Convergence CSV](results/convergence.csv), [summary JSON](results/summary.json).
- Raw time histories: [N24 coarse](results/n24_coarse.csv),
  [N24 fine](results/n24_fine.csv), [N32 coarse](results/n32_coarse.csv).
- Matching JSON files retain parameters, platform, source/solver/preregistration
  hashes and diagnostics. Process JSON/logs preserve commands, exit codes and limits.

Python 3.12.14, NumPy 2.3.5; Linux 6.18.55 x86_64, glibc 2.41, single-thread
BLAS/OpenMP. The ten-step pilot took 0.872 s, 55.281 MiB RSS, and projected
68.182 s total. Full runs took 3.489, 6.272, and 7.740 s. Total solver-process
time including pilot was 18.373 s; peak RSS 57.734 MiB. Solver subprocesses had
hard timeouts (pilot 30 s, aggregate budget 300 s with report allowance) and
512 MiB address-space limits. Reporting took 1.882 s; clean plotting 1.715 s
under a 15 s timeout. Initial plot cache warnings were nonfatal; clean plots
use a writable temporary Matplotlib cache. No numerical execution failed.

Reproduction uses the recorded Python environment and `execute.py pilot`, then
`execute.py full`, then `report.py`, then `plot.py`. These tools deliberately
refuse to overwrite outputs. Use a separate repository copy with a fresh empty
`paired-dns/results` and `paired-dns/figures`, keeping the original archive
intact. Numerical reruns require their own authorization/resource gate. Source
freeze verification and stored-output inspection do not require a DNS rerun.

See [REVIEW.md](REVIEW.md) for the bounded independent AI review and validation.
