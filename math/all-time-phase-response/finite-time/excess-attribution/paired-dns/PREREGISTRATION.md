# Frozen paired diagnostic

Written before numerical execution, base4e86fa995243c3a428a253ee3333eb42251cd85f.
No change to certificate repairs0f83002654040c88e4bc652c4589550696cae3bf.
Fixed a=c=d=1,nu=1/28,phi=37/100,T=1/4,b=+/-3/1000, normalized2pi torus.
Binary64 represents these parameters; numerical evidence only. Production NS
solver unchanged: cube K=floor((N-1)/3),N>3K, normalized rFFT, weighted kz planes.
Frozen diagnostic.py is hashed in FREEZE.json before any numerical run.

Unknown signs of S and nuR; null/failed checks preserved. No retuning.
Configurations: N24/dt.0025, N24/dt.00125, N32/dt.0025; U and both b signs
are advanced together with classical RK4. All reachT=.25 except the ten-step
resource pilot (N32/dt.0025), whose shorter horizon supplies no endpoint claim.
No q2/adjoint evolution, validation, LFS or parameter sweep.

Q is accumulated by the nonlinear RHS pairing with -Delta u at RK4 stages.
At initial state/every10 steps/final state independently compare the physical
trilinear vorticity stretching expression. N>3K makes its volume average
alias-free on retained fields. D=2*palin. Expand Q and D differences in v=u_b-U
and independently compare direct subtraction at every RK stage. Accumulate
both integrals; exact integrated heat subtraction is b²(1-exp(-2nu t))/4.
H is computed independently from fields and isolated heat enstrophy. Record
all scaled contributions, balance, parity, divergence, high-mode enstrophy
fraction (max component wavenumber>=K-1), and every-step trapezoid quadrature.
The latter is independent of stage accumulation, has O(dt²) error and its
observed disagreement enters the conservative empirical-sign error scale.

Fixed principal acceptance: max over saved times |H-S+nuR|/b²<=1e-5;
endpoint time and space changes for each S/b² and nuR/b²<=1e-4, for each b sign.
Empirical sign only if magnitude>10times max(refinement change,balance defect,
direct-expanded discrepancy,observed stage-versus-trapezoid difference).
The extra quadrature term strengthens, not relaxes, the previously specified
sign rule. Secondary checks: absolute spectral divergence<=1e-10,
trilinear/RHS difference divided by b²<=1e-8, direct-expanded discrepancy
scaled by b²<=1e-8, scaled +/- parity<=1e-7. High-mode tails are reported;
space convergence remains required. Initial analytic Q(U)=cos(phi)/4,
Z difference=b²/4,D difference=b²/2 and pure-heat normalization are checked.

Pilot: exactly ten steps at N32 with all diagnostics, process hard timeout30s.
Enforce512MiB address-space cap (stricter than RSS), BLAS/OMP one thread.
Measure process wall time and peak RSS. Conservative projection:
pilot wall + 1.5*(pilot wall/10)*400 full-run steps +15s reporting/check allowance.
All400 steps charged at N32 cost. Proceed only if this is<300s and RSS<512MiB.
Runner enforces shared300s aggregate budget, per-run timeout<=remaining budget,
address-space cap on each solver; scalar output directory total<1MiB.
Stop on nonfinite states, diagnostic/normalization/balance failure, resource
limit, refinement failure, or inadequate sign separation (unresolved, not zero).
No new full run after such failure; preserve all outputs. No threshold changes.

If accepted, produce raw CSV, summary/convergence JSON and simple time-series
figures labeled numerical evidence, with S,nuR,H and the sign H=S-nuR clear.
One focused independent review permitted; local commit only, no publication.
