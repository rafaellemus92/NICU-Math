"""Independent recomputation of EVERY row of results/chain_percell.json (audit repair 3).

Recomputes the absorption chain recursion of absorption-b003 (NOTE.md sections 1-3, the update rules of
absorb_chain.py) in mpmath interval arithmetic, from the same validated cell inputs, and compares all 250 rows
and all 11 fields with the per-cell file, which was produced with the parent's 40-digit decimal intervals.
For each field the per-cell upper endpoint must be >= the lower end of this enclosure of the same exact value,
and the two must agree to 1e-30 relative.
Usage:  python3 -I verify_percell.py <finite-time dir> <chain_percell.json> <output json>   (new output only)
"""
import sys, json, hashlib, time
from pathlib import Path
from mpmath import iv, mpf
iv.dps = 60
t0 = time.monotonic()
FT, CPC, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if OUT.exists(): raise SystemExit(f'refusing to overwrite {OUT}')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
VAL = FT / 'absorption-b003/results/validated.json'; CH = FT / 'absorption-b003/results/chain.json'
assert sha(VAL) == 'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b'
assert sha(CH) == '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117'
data, chain, cpc = json.loads(VAL.read_text()), json.loads(CH.read_text()), json.loads(CPC.read_text())
cells = data['cells']; n = data['parameters']['ncoarse']; assert n == 250 and len(cpc['log']) == n
X = iv.mpf
a = c = d = X(1); nu = X(1) / 28; T = X(1) / 4; b = X(3) / 1000; Delta = T / n
CA = X(chain['C_A']); L3 = iv.sqrt(X(8))
def lattice_1d(pn, pd, N0=4000, te=None):
    s = iv.mpf(0)
    for k in range(-N0, N0 + 1):
        s += X(1 + k * k) ** pn / X(2 + k * k) ** pd
    return s + 2 / ((te - 1) * X(N0) ** (te - 1))
S0, S1, S2 = iv.sqrt(lattice_1d(0, 3, te=6)), iv.sqrt(lattice_1d(1, 3, te=4)), iv.sqrt(lattice_1d(2, 3, te=2))
g = c + d; E_nu = iv.exp(-nu * Delta)
cellv = lambda key, j: iv.mpf(float(cells[key][j]))                 # exact binary64 value
el = iv.mpf(1); epsW = iv.mpf(float(data['initial']['epsW0']))
eps0 = eps1 = delta2 = Nw = Kw2 = R0 = iv.mpf(0)
fields = ['t', 'm1', 'm2', 'epsW', 'eps0', 'eps1', 'delta2', 'S1', 'sigma1', 'N_w', 'K']
maxrel = {f: mpf(0) for f in fields}; bad = []
for j in range(n):
    tr = Delta * (j + 1)
    el_prev = el
    er = el * E_nu; al = a * el; e1r = (1 - er) / nu; e2r = (1 - er ** 2) / (2 * nu)
    g1 = d + a * g * e1r; g2 = d + a * g * e1r + 2 * a * d * e1r + (2 * a ** 2 * g / nu) * (e1r - e2r)
    m1 = iv.sqrt(al ** 2 + g ** 2 + g1 ** 2); m2 = iv.sqrt(al ** 2 + g ** 2 + 2 * g1 ** 2 + g2 ** 2); el = er
    rhoW = L3 * a * el_prev - nu
    epsW = iv.exp(rhoW * Delta) * (epsW + cellv('int_rW', j))
    sdw0, sdw1, sdw2 = S0 * epsW, S1 * epsW, S2 * epsW
    q_sup, gq_sup = cellv('sup_q', j), cellv('sup_gradq', j)
    absq, absgq, abshq = cellv('sup_absq', j), cellv('sup_absgradq', j), cellv('sup_abshessq', j)
    int_r = cellv('int_r', j) + Delta * (sdw0 * q_sup + sdw1 * q_sup)
    int_gr = cellv('int_gradr', j) + Delta * (sdw1 * q_sup + sdw0 * gq_sup + sdw1 * gq_sup + sdw2 * q_sup)
    eps1_prev = eps1
    eps0 = iv.exp((m1 - nu) * Delta) * (eps0 + int_r)
    eps1 = iv.exp((2 * m1 - nu) * Delta) * (eps1 + m2 * eps0 * Delta + int_gr)
    d2_inc = (2 * m1 * eps1 ** 2 * Delta + m2 * eps0 * eps1 * Delta + eps1 * int_gr) / nu
    delta2 = delta2 + d2_inc
    d2_cell = d2_inc + eps1_prev ** 2 / (2 * nu)
    S1cell = gq_sup + eps1
    sigma1 = absq * gq_sup + absgq * eps0 + absq * eps1
    rho0_int = (m1 + b * absgq - nu / 2) * Delta + b ** 2 * CA ** 2 * d2_cell / (2 * nu)
    R0 = R0 + rho0_int
    Nw = iv.exp(rho0_int) * (Nw + sigma1 * Delta)
    rho1_int2 = (2 * (2 * m1 + 2 * b * absgq - nu / 8) + 1) * Delta + 4 * b ** 2 * CA ** 2 * d2_cell / nu
    Nw_tot = Nw + iv.exp(R0) * CA * eps1 * iv.sqrt(tr * delta2)
    Kw2 = iv.exp(rho1_int2) * (Kw2 + Delta * ((m2 + b * abshq) ** 2 * Nw_tot ** 2 + 8 * sigma1 ** 2 / nu)
                               + 8 * CA ** 2 * eps1 ** 2 * d2_cell / nu)
    mine = dict(zip(fields, (tr, m1, m2, epsW, eps0, eps1, delta2, S1cell, sigma1, Nw_tot, iv.sqrt(Kw2))))
    for f, s in zip(fields, cpc['log'][j]):
        hi = iv.mpf(s); m = mine[f]
        ok_lower = hi.b >= m.a                       # the per-cell upper bound is not below this enclosure
        rel = mpf(((abs(hi - m.b)) / m.b).b) if m.b > 0 else mpf(abs(hi).b)   # plain mpf
        maxrel[f] = max(maxrel[f], rel)
        if not (ok_lower and rel < mpf('1e-30')): bad.append((j, f, s[:30], str(m.b)[:30]))
all_ok = not bad
out = dict(all_250_rows_verified=all_ok, rows=n, fields=fields, tolerance_relative='1e-30',
           max_relative_difference={f: f'{float(v):.3e}' for f, v in maxrel.items()}, mismatches=bad[:20],
           chain_percell_sha256=sha(CPC), chain_percell_py_sha256=sha(Path(__file__).resolve().parent / 'chain_percell.py'),
           inputs_sha256={'absorption-b003/results/validated.json': sha(VAL), 'absorption-b003/results/chain.json': sha(CH)},
           source_sha256=sha(__file__), method='independent mpmath recomputation of the absorb_chain.py recursion',
           wall_seconds=time.monotonic() - t0)
with OUT.open('x') as fh: json.dump(out, fh, indent=1); fh.write('\n')
print(f'all {n} rows x {len(fields)} fields verified: {all_ok}   max relative differences: {out["max_relative_difference"]}')
print(f'wall {out["wall_seconds"]:.1f} s; wrote {OUT.name}')
