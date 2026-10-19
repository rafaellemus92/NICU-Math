# Pinned-hash check of the audited commit, preserved verbatim from the audit. Run from finite-time/.
import hashlib, re
from pathlib import Path
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins = {}
for src in ('source-only-hull/source_hull.py','z2-endpoint/endpoint.py','route-b-tightening/evaluate.py','route-b-dissipation/bounds.py','mean-q2-pilot/kernels.py'):
    t = Path(src).read_text()
    for name, h in re.findall(r"'([A-Za-z0-9_./-]+\.(?:py|json|log))'\s*:\s*'([0-9a-f]{64})'", t):
        pins.setdefault(name, set()).add((h, src))
    for h in re.findall(r"PIN\s*=\s*'([0-9a-f]{64})'", t): pins.setdefault('absorption-b003/validate_residual.py', set()).add((h, src))
    for h in re.findall(r"PIN_REMAINDER\s*=\s*'([0-9a-f]{64})'", t): pins.setdefault('route-b-tightening/results/time_refinement.final.json', set()).add((h, src))
    for h in re.findall(r"constants.py'\)\.read_bytes\(\)\)\.hexdigest\(\)!='([0-9a-f]{64})'", t): pins.setdefault('constants.py', set()).add((h, src))
bad = 0
for name, s in sorted(pins.items()):
    actual = sha(name)
    for h, src in sorted(s):
        ok = actual == h
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {name:62s} pinned by {src}")
print('mismatches:', bad)
