# Independent AI review record

One read-only reviewer, task /root/analytic_review, reviewed the candidate
formulas, then the scripts and stored outputs. No recursive reviewers,
numerical runs, edits or external actions were performed by that reviewer.
This is AI mathematical/code review, not human refereeing or formal verification.

The reviewer accepted Fourier weighted Cauchy-Schwarz for mean-zero vector
fields without a factor three, finite subtraction from the inherited lattice
upper bound, the revised full-r and mean forcings, and the Minkowski bound.
The zero-initial Duhamel cap and single global retained-dissipation integration
were also accepted, with no missing initial energy or factor two found.

The first exact-code review identified a blocking arithmetic defect: the
scripts used the upper endpoint of nu as a point. This could underestimate
1/nu and exp((M1-nu)T). Initial results were preserved and superseded. Both
paths now use the exact rational interval1/28, with corrected results in
*.final.json. Endpoint provenance/scope/G checks were added. Both plan versions
and exact earlier script snapshots were retained.

Final review reported the corrections present, matching source/input/plan
hashes, and no further blocking defect in the inspected scripts or formulas.
It accepted the conservative recorded candidate bounds C_global<15128.8003,
C_endpoint<6921.6485, beta²C_endpoint<.06230, conditional on inherited
certificates. It read the eight-pass final test log but did not rerun tests.
The final documentation/commit itself was not independently reviewed.

The reviewer also accepted the conditional source-only lemma:
if integral||mean B(q1,q1)||<=.05, then
Z2(T)>=.28091-1.8534*1.9424*.05=.100907792>.06230.
It stressed that the antecedent has NOT been computed, and that a hull of all
fine nodes must cover every affine segment; source sampling is insufficient.

Remaining limitations: no dominance result, no signed coefficient computed,
no new source-only experiment, no human review/formalization of inherited PDE
estimates. Endpoint G cannot silently replace a uniform-in-time norm. The
current coefficient interval still includes zero; no sampled coefficient or
q1 energy term alone is a lower bound on |Z2|.
