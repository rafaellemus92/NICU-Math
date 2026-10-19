# Comparison of the fresh source_hull.py run with the recorded full.json, preserved verbatim from the audit.
# Usage: python3 -I compare_hull_output.py <recorded full.json> <fresh output json>
import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
TIMING = {'seconds', 'wall_seconds'}
ENV = {'python', 'numpy', 'peak_rss_kib'}
num_diff, timing, env, other = [], [], [], []
def walk(x, y, path):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y: other.append((path + '/' + k, 'missing in one')); continue
            walk(x[k], y[k], path + '/' + k)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (p, q) in enumerate(zip(x, y)): walk(p, q, f'{path}[{i}]')
    elif x != y:
        leaf = path.rsplit('/', 1)[-1]
        if leaf in TIMING: timing.append(path)
        elif leaf in ENV: env.append((path, x, y))
        else: num_diff.append((path, x, y))
walk(a, b, '')
print('rows:', len(a['rows']), len(b['rows']))
print('numerical/content differences:', len(num_diff)); [print('  ', d) for d in num_diff[:10]]
print('timing-only differences:', len(timing), '(per-cell seconds and wall)')
print('environment differences:'); [print('  ', e) for e in env]
print('structural:', other)
keys = ['source_norm_upper_exact', 'source_norm_upper_binary64', 'max_raw_hull_radius', 'max_source_disc_radius', 'first_node', 'last_node', 'coarse_cell']
same = all(all(r[k] == s[k] for k in keys) for r, s in zip(a['rows'], b['rows']))
print('all 250 rows identical in every numerical field:', same)
print('bounds identical:', a['bounds'] == b['bounds'], '| LF enclosure identical:', a['LF_physical_enclosure'] == b['LF_physical_enclosure'])
print('decisions:', b['checkpoint_LF_le_point05'], b['positive_Z2_lower_exceeds_threshold'], '| wall recorded', round(a['wall_seconds'], 2), 'this run', round(b['wall_seconds'], 2))
for k in ('LF_majorant', 'abs_M_majorant', 'Z2', 'threshold', 'remainder_upper'):
    print(f"  {k:16s} lo {b['bounds'][k]['lo'][:22]}  hi {b['bounds'][k]['hi'][:22]}")
print('max hull radius over cells:', max(r['max_raw_hull_radius'] for r in b['rows']), ' max source radius:', max(r['max_source_disc_radius'] for r in b['rows']))
