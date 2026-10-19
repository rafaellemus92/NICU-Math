# Preregistered four-terminal grouping example

Owner Codex; base2b14eeaa3d6a432e357f9ae0b9b2c936a725f6aa; branch
codex/physiology-spatial-compliance. Written before endpoint evaluation.
Two identical shared-trunk subtrees, two terminals each. All trunk and terminal
resistances1 cmH2O*s/mL. Compare G=(1,1)|(2,2) and M=(1,2)|(1,2) mL/cmH2O.
Same graph, resistances, compliance multiset, total compliance6, initial terminal
pressures1 cmH2O, initial total excess volume6mL and energy3 cmH2O*mL.
Prescribed boundary releases from1 to0 at t=0. Synthetic, nonclinical scope.

Primary endpoint f_G(1)-f_M(1), retained fraction relative to initial6mL.
Observation times0,.25,.5,1,2,4 seconds; trajectory checks may sample0..4 more
finely to check formulas, not choose another primary time. No parameter tuning.
Preserve a null or roundoff-sized endpoint. Exact initial derivative oracle:
V=6,V'=-4/3,V''=1/3 both; V_G'''=-5/54,V_M'''=-1/9.

Controls: zero-trunk contraction gives independent equal-R compartments and
aggregate permutation invariance; simultaneous graph/parameter relabeling;
volume conservation and passive energy decay, including nonuniform pressures.
Use NumPy symmetric eigendecomposition, independent analytic closed forms and
existing SciPy expm crosscheck. No installs. Full physiology regression suite.
At most300 seconds aggregate numerical execution, process timeouts<=60 seconds.
One bounded independent code/math review, no recursive reviewers. No change to
existing two-compartment code or NS proof, no owner-branch integration, no push.
Root AGENTS.md explicitly requires docs/HANDOFF.md and docs/RESEARCH_INDEX.md
updates in addition to physiology/ and tests/physiology/.
