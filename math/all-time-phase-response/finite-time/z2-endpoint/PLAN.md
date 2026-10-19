# Fixed-endpoint coefficient investigation: preregistration

Owner Codex. Base 2af8fe4b3abceee08547f0fee699d78b5ac29bf2.
Branch codex/phase-z2-endpoint. Written before endpoint evaluation.

Fixed a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000.
Enclose Z2(T)=<grad U,grad q2>+||grad q1||²/2 and test whether a
rigorous lower bound on |Z2(T)| exceeds beta² C_B. This is a fixed-endpoint
coefficient comparison, not a relative-error guarantee on [0,T]. Do not change
beta after the result to declare success. Preserve negative/inconclusive results.

First-stage method: reuse already verified local Q/W arrays, read only their
endpoint for exact-rational finite Fourier sums, and combine with the archived
q1 H1 and base W weighted-error bounds. Bound the q2 pairing symmetrically
using the already derived analytic N2 bound. Record the resulting interval and
whether it excludes zero; a wide rigorous interval is not a positive lower bound.

No new q2 evolution, DNS, parameter sweep, full validator, download or extra
agent. If the existing envelopes are insufficient, derive the exact signed
observable/adjoint dependency and a concrete residual/arithmetic validation plan
and cost estimate before requesting a larger computation. Stop at the documented
bound/blocker for independent review. Inputs and historical outputs stay immutable.
