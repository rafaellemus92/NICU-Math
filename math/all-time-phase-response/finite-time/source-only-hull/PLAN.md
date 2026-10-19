# Source-only hull validation, fixed before execution

Base f6cdc6d3eeed4c4e947eef0b56f48f1cc0b1eccd; Codex owner.
Same fixed a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=.003.
Sufficient checkpoint LF<=.05; also report actual upper enclosure and original
endpoint dominance comparison. No measured coefficient input or retuning.

Use exactly the inherited qN path: exact saved complex128 dyadic Q nodes,
indices kx,ky=-10..10, kz=1; exact modewise Leray projection at each node,
affine time interpolation on j/50000. For coarse cell ell, enclose all51 nodes
50ell..50ell+50 in coefficient discs centered on node50ell+25. Radius is max
of outward abs_hi(csub(exact(nodes),exact(center))). Project with the inherited
project_small helper; convexity/linearity encloses every fine affine segment.
Reuse pinned full mean-source convolution; output support -20..20 and mean
Parseval with no half factor. Sum250 widths1/1000 times enclosed source norms;
add inherited full q1 discrepancy. No new base or mean-field solve.

First exact synthetic hull/projection/convolution checks and inherited kernel
suite. Then benchmark coarse cells0,125,249. Full250-cell run only if conservative
2x measured per-cell cost plus overhead fits remaining300-second aggregate cap.
Full process watchdog180s, pilot30s, tests30s; stop incomplete on timeout.
All inputs/source hashes and scope/path metadata checked; outputs exclusive-create.
No reviewer/subagent, new download, DNS, two-hour validator, push or merge.
