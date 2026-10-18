"""Recompute every ratio quoted in README.md from the archived JSON (read-only)."""
import json, sys
R = str(__import__('pathlib').Path(__file__).resolve().parents[2]/'all-time-phase-response/results') + '/'
obs = json.load(open(R+'observable_remainder.json'))
for run in obs['runs']:
    c1, c2 = run['cases']
    ratios = [abs(a)/abs(b) for a, b in zip(c1['raw_even_E_Z_S'], c2['raw_even_E_Z_S'])]
    fr = c1['field_second_order_L2_plus_minus'][0]/c2['field_second_order_L2_plus_minus'][0]
    print(f"N={run['N']} dt={run['dt']}: raw ratios E,Z,S = {ratios}  stored={run['raw_quartic_ratios_E_Z_S']}  field2 ratio={fr:.6f}")
    # README's second_error (normalised by b^2) ratio = max_O|raw_even/b^2| ratio
    se1 = max(abs(x)/.1**2 for x in c1['raw_even_E_Z_S']); se2 = max(abs(x)/.05**2 for x in c2['raw_even_E_Z_S'])
    print(f"   second_error ratio (README 3.999658882) = {se1/se2:.9f}; raw S mags {c1['raw_even_E_Z_S'][2]:.9e} {c2['raw_even_E_Z_S'][2]:.9e}")
for name in ['pilot.json', 'refined.json']:
    d = json.load(open(R+name))
    print(name, d['status'], d['checks'], d['errors'], 'ratio', d['second_difference_ratio'], 'field', d['field_remainder_ratio'])
    print('  cos2 harmonics E,Z,S run[-1]:', d['runs'][-1]['harmonics_E_Z_S']['2']['cos'])
    print('  pilot.py sha in json:', d['metadata']['sha256']['math/all-time-phase-response/pilot.py'][:8])
