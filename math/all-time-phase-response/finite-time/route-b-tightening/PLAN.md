# Bounded analytic tightening, before numerical evaluation

Owner Codex; base 4bf68e0a6dcddc0d38b77c0123006fbea90d5f89.
Fixed original a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=.003.
No coefficient lower bound is assumed. No dominance claim follows from a smaller
remainder upper bound alone. Preserve all original results.

Investigate resolvent-weighted Fourier Cauchy-Schwarz using the already certified
L2 and integrated H2 bounds of w/b². Finite cube radius 32; prescribed positive
lambda values 100,10000,100000,1000000,10000000. Each valid choice is a separate
analytic bound; comparison is sensitivity of proved inequalities, not a fitted
physical trajectory. Reuse unchanged inherited K and Dw initially. Also examine
local-time loss and signed-pairing obstructions. Numerical budget 300 seconds
aggregate; each subprocess timeout at most 60 seconds. Only small postprocessing,
no trajectory read, DNS, downloads, full validator or external writes.

Produce complete proof, directed interval results, source hashes, test evidence,
and request one independent read-only review (no recursive reviewers). Stop at
candidate bound and explicit coefficient obstruction; no next experiment launch.
