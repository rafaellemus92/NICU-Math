import json, sys
from fractions import Fraction as Fr
mine = json.load(open(sys.argv[1]))
nodes_dir = sys.argv[2]
bad = 0; checked = 0
for i in range(7):
    d = json.load(open(f"{nodes_dir}/node_{i}.json"))
    nu = Fr(d['nu'])
    for entry in d['series']:
        n = str(entry['time_power'])
        theirs = {int(m): (Fr(c['real']), Fr(c['imag'])) for m, c in entry['laurent_coefficients'].items()}
        ours = {}
        for m, poly in mine[n].items():
            v = sum((Fr(c[0]) * nu**int(dd) for dd, c in poly.items()), Fr(0))
            if v != 0: ours[int(m)] = (v, Fr(0))
        checked += 1
        if ours != theirs:
            bad += 1; print("MISMATCH", nu, n, ours, theirs)
print(f"compared {checked} (node, order) Laurent vectors; mismatches={bad}")
