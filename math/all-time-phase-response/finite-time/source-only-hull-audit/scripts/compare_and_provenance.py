# Full-precision comparison of the independent scalar bounds with the recorded endpoints, and provenance hashes
# recorded inside the outputs; preserved verbatim from the audit. Run from finite-time/.
# Usage: python3 -I compare_and_provenance.py <scalar_out.json> <fresh hull output json>
import json, hashlib, sys
from decimal import Decimal, getcontext
from pathlib import Path
getcontext().prec = 80
mine = json.load(open(sys.argv[1])); run = json.load(open(sys.argv[2]))
tr = json.load(open('route-b-tightening/results/time_refinement.final.json'))['rows']['1000000']
print('full-precision comparison (independent mpmath upper bound vs recorded upper endpoint):')
for name, rec in (('Cend', tr['C_endpoint']['hi']), ('thr', run['bounds']['threshold']['hi']), ('LF', run['bounds']['LF_majorant']['hi']),
                  ('absM', run['bounds']['abs_M_majorant']['hi']), ('Nbar', tr['Nbar']['hi']), ('Er', tr['Er']['hi']), ('Ahat', tr['A_lambda']['hi'])):
    m = Decimal(mine[name].strip('[]').split(',')[-1]) if mine[name].startswith('[') else Decimal(mine[name])
    r = Decimal(rec); print(f'  {name:5s} relative difference {float(abs(m - r) / r):.1e}   recorded >= mine - 1e-35 rel: {r >= m * (1 - Decimal("1e-35"))}')
zl = mine['Z2lo'].strip('[]').split(',')[0]; print('  Z2 lower: mine', zl[:30], ' recorded', run['bounds']['Z2']['lo'][:30])
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
print('provenance recorded inside outputs:')
ep = json.load(open('z2-endpoint/results/endpoint.json')); print('  endpoint.json source == endpoint.py:', ep['source_sha256'] == sha('z2-endpoint/endpoint.py'), '| plan:', ep['plan_sha256'] == sha('z2-endpoint/PLAN.md'))
rb = json.load(open('route-b-dissipation/results/bounds.review.json')); print('  bounds.review.json source == bounds.py:', rb['source_sha256'] == sha('route-b-dissipation/bounds.py'))
t2 = json.load(open('route-b-tightening/results/time_refinement.final.json')); print('  time_refinement.final.json source/helper/plan:', t2['source_sha256'] == sha('route-b-tightening/time_refinement.py'), t2['helper_sha256'] == sha('route-b-tightening/evaluate.py'), t2['plan_sha256'] == sha('route-b-tightening/PLAN.time-refinement.md'))
fj = json.load(open('source-only-hull/results/full.json')); print('  full.json source/plan:', fj['source_sha256'] == sha('source-only-hull/source_hull.py'), fj['plan_sha256'] == sha('source-only-hull/PLAN.md'), '| my run source:', run['source_sha256'] == fj['source_sha256'])
print('  trajectory hashes recorded in bounds.review.json equal manifest raw-array hashes:', rb['trajectory_array_hashes_in_verified_inputs'] == {k: v['sha256_array_bytes'] for k, v in json.load(open('absorption-b003/results/trajectory_manifest.json'))['files'].items()})
