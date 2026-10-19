# User-relayed external AI review and local response

Reviewed candidate: 375e399d79d513f4ba263be1c7ed3606d01e35a6.
Review source: the user's relay of the external NS-Speech session audit.
The actual reviewer model is unverified; the user reported a switch due to quota.
This is AI review, not a human referee report or formal verification. No reviewer
was spawned by this local follow-up. Original results and their historical
"review pending" metadata are preserved unchanged.

The relay reports conditional acceptance of the derivation and source correspondence,
seven passing tests, a byte-identical rerun, and an independent transcription matching
the intervals. Those external executions are reported, not independently witnessed
here. In the earlier focused critique, the C_A upper-endpoint provenance and zero
spatial means were additionally resolved from exact parent-source lines. The new
local follow-up checks are distinguished below.

## Findings and adjudication

1. **Absolute accuracy versus quadratic dominance: accepted.** The unchanged
   milestone is an absolute normalized enstrophy error below 0.01. The bound
   7.1123e-6 exceeds the relayed sampled b²|Z2| estimate 2.25–2.40e-6 at b=0.003.
   No dominance or certified relative accuracy follows. The sampled estimate and
   suggested ~0.0017 threshold are not rigorous or uniform certificates. Correction during the
   fixed-endpoint follow-up: the relayed Z2(0)=0 assertion was incorrect for
   the defined coefficient; Z2(0)=1/4. See ../z2-endpoint/NOTE.md.
   NOTE.md states this limitation next to the milestone.
2. **NumPy dependency: accepted.** Parent constants.py imports NumPy at line 59.
   The new postprocessor performs no NumPy computation, but importing its parent
   requires NumPy. The standard-library-only/no-NumPy wording is corrected.
3. **Explicit scope checks: accepted as defense in depth.** Unchanged SHA-256 pins
   already restrict the exact inputs. validate_scope now also checks the chain's
   b,T,phi, certificate kind/decisions and the validated input's a,c,d,nu,T,phi,
   exact rational strings, grid parameters, completion, zero q1 initial error and
   consumed cell-array lengths. These are fail-closed ValueError checks. Metadata
   floats are checked against their exact expected representations; the actual
   formulas continue to use rational nu, T and beta. The lattice log is pinned
   provenance only; CA is read from the archived certified chain, not recomputed.
4. **Tests versus mathematical proof: accepted.** Tests check implementation,
   arithmetic, input guards and preservation. The Fourier-set test is structural;
   it does not prove the PDE preserves those supports. The analytic argument
   remains in the note and is subject to the stated conditional AI review.

## Additional premise and comparison checks

w, q2, r=w-b²q2 and bar(r) have zero initial data. e=q1-qN also has zero
initial data: validate_residual.py lines 443–445 check the exact stored -i
coefficient, and the mode-wise Leray projection preserves it. This must not be
confused with the nonzero initial base-flow representation error epsW0, already
propagated in the archived certificate. Both q1 and qN have only kz=+/-1,
so e has zero full spatial mean. Solenoidality alone would not suffice.

The observable expansion also uses <grad U,grad q1>=0, from kz=0 versus +/-1,
in addition to q1/q2 orthogonality. The note now states both explicitly.
E_r bounds full r; saved oscillating-remainder diagnostics describe a different
quantity. Reported N=24 results at b=0.01/0.05 are outside |b|<=0.003 and lack
validated discretization error. No rigorous tightness ratio or true small-b
error is inferred. No changes to unrelated old-note comparisons were made.

## Local validation and boundary

Eight focused tests pass in Python 3.12; the new scope test mutates or removes
individual fixed fields and shortens consumed cell arrays. The numerical and
input-provenance trees from evaluate() match the original results exactly;
only source hash and the review-status description change. The new result is
saved separately as results/bounds.review.json, never over the original.
See results/tests-review312.log and results/bounds.review.log.

No analytic formula, pinned input, original result, parent script or trajectory
was changed. No DNS, full validator, LFS download, parameter sweep, additional
agent, push, PR or merge was performed.

Suggested next scientific target, not started: at the fixed T=1/4, certify an
interval enclosure for Z2 with a nonzero lower bound on |Z2| and compare b²|Z2|
against the remainder bound. If the current remainder envelope remains larger,
sharpen its dominant mean/self-interaction estimate before claiming dominance.
Any extension to a time interval must specify its endpoints and certify a
lower bound there (the defined coefficient does not vanish at t=0); no numerical threshold is preregistered or certified here.
