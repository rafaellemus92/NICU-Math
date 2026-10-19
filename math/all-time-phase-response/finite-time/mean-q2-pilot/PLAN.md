# Forward mean-q2 correctness/runtime pilot, fixed before execution

Base bc305995c49f3303352e1c1a4e13a50dbf90d965; owner Codex.
Fixed a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=.003. Existing total-Z2
endpoint comparison remains the target. No centered/excess diagnostic can
substitute for it. No full-horizon coefficient enclosure is promised here.

Choose forward mean-q2: zero initial data, LU V=-mean B(q1,q1).
Use direct interval convolution of validated qN coefficients for the mean
quadratic forcing, and explicit sparse-base coupling for the mean linear
operator. Ordinary FFTs are not validation. Do not reuse the kz=1 base operator
unchanged: its i*w*Q advection is absent for kz=0.

Test exact rational simple modes, real +/-z factor, Leray zero-mode handling,
mean projection, full support/tails, affine-node polynomial residual identities,
frozen exponential and inherited q1/base/initial-error budgets.

Benchmark only fine cells j=0,6250,12499, with known/synthetic mean-field nodes
(zero at the initial cell, synthetic divergence-free states later). These are
kernel probes, NOT a q2 trajectory and NOT actual residuals of an approximation
starting at zero on the full horizon. No new trajectory is generated.
Mean cutoff M=20, q1 cutoff 10, base |ky|<=21. Include full product support.

Numerical execution budget: <=300 seconds aggregate wall time. Benchmark driver
has a 180-second hard timeout; test run a 60-second timeout. Report measured
usage and reserve remaining budget for necessary focused fixes only. No broad
campaign or full validator. Existing local arrays are read-only and identity
checked; no download, upload, paid resource, subagent, PR, push or merge.

Stop after tests, sampled timings, storage estimate, bottleneck/error budget and
a concrete full-run plan. Full-run authorization is a separate decision.
