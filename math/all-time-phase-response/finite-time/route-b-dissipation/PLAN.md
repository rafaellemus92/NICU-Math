# Route B first-stage preregistration

Owner: Codex. Base: 419e6c3d2e0321816849ca550ad8da5cf34ba75a.
Written before the first Route B evaluation, 2026-10-19.

Fixed scope: a=c=d=1, nu=1/28, phi=37/100, T=1/4, every |b|<=3/1000.
Research target: establish a certified upper bound for the normalized enstrophy
remainder |Z(u_b)-Z(U)-b^2 Z2| strictly below 1/100 at b=3/1000,
T=1/4. This target will not change after evaluation. Failure is retained.

First retain W2's nu/8 dissipation before its Poincare substitution. Distinguish
zero-initial-data global accumulation from a per-cell bound carrying initial
H1 energy. Use conservative terminal certified envelopes, not differences of
upper bounds or nearest-rounded diagnostic log entries.

Then assess the b-independent coefficient q2 and the field r=w-b^2 q2.
Its equation has source b[B(q1,w)+B(w,q1)]+B(w,w). Test a direct estimate
using q1=q1^N+e, the existing sharp S1,K,Nw, and the new dissipation bound.
The z-mean cubic terms involving q1 and q2 vanish by their Fourier supports;
use this to bound the mean of r at order b^4 and the observable, if justified.
No claimed sharp q2 numerical approximation and no new simulations.

Inputs: archived validated.json and chain.json from the independently reproduced
certificate; parent constants.py interval arithmetic and certified lattice bound.
All new code/results stay here. No archive mutation, new downloads, DNS, parameter
sweeps, or integration. A second independent review remains pending.
