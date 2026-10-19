"""Compare the T=1/2 bundle inputs on [0, 1/4] with the reviewed T=1/4 files, and the rerun of the
reviewed chain recursion (T=1/2 variant) with the bundle's 500-row per-cell table.
Usage: python3 -I -B compare_t025.py <bundle artifacts dir> <t025_reference dir> <rerun chain json>"""
import sys, json, hashlib
from pathlib import Path
ART, REF, RERUN = (Path(a) for a in sys.argv[1:4])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for p in (REF / 't025_chain_percell.json', REF / 't025_validated.json', RERUN,
          ART / 'endpoint-sign/results/chain_percell.json', ART / 'absorption-b003/results/validated.json', ART / 'absorption-b003/results/chain.json'):
    print(sha(p), p.name)
a, b = json.loads((REF / 't025_chain_percell.json').read_text()), json.loads((ART / 'endpoint-sign/results/chain_percell.json').read_text())
assert a['log_columns'] == b['log_columns'] and len(a['log']) == 250 and len(b['log']) == 500
print('per-cell table, cells 1..250 identical in all 11 columns:', a['log'] == b['log'][:250])
va, vb = json.loads((REF / 't025_validated.json').read_text()), json.loads((ART / 'absorption-b003/results/validated.json').read_text())
print('validated cells 1..250 identical in all 9 fields:', all(va['cells'][k] == vb['cells'][k][:250] for k in vb['cells']) and set(va['cells']) == set(vb['cells']))
print('validated conventions/approximation/initial identical:', va['conventions'] == vb['conventions'], va['approximation'] == vb['approximation'], va['initial'] == vb['initial'])
print('validated parameters that differ:', {k: (va['parameters'][k], vb['parameters'][k]) for k in vb['parameters'] if va['parameters'].get(k) != vb['parameters'][k]})
print('validator sha256 T=1/4 vs T=1/2:', va['provenance']['validator_sha256'][:16], vb['provenance']['validator_sha256'][:16])
r, c = json.loads(RERUN.read_text()), json.loads((ART / 'absorption-b003/results/chain.json').read_text())
print('rerun of reviewed recursion: 500 rows identical to bundle table:', r['log'] == b['log'])
print('rerun top-level fields identical to bundle chain.json (except the T label):', [k for k in c if k not in ('log', 'T') and c[k] != r.get(k)] == [])
print('closure at b = 0.003:', r['condition_A'], r['condition_B1'], r['condition_B2'], r['verdict'], 'lhs_A', r['lhs_A'], 'threshold', r['threshold_nu_over_2CA'])
