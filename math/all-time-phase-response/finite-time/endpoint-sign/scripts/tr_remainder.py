"""Time-resolved one-sided remainder at T = 1/4 (PLAN.md sections A-F), mpmath interval arithmetic, outputs new only.
Usage:  python3 -I tr_remainder.py <finite-time dir> <chain_percell.json> <output json>
New derivation, not independently reviewed; see PLAN.md. No trajectory is read."""
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
from mpmath import iv, mpf
iv.dps = 60
t0 = time.monotonic()
FT, CPC, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if OUT.exists(): raise SystemExit(f'refusing to overwrite {OUT}')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
PINS = {  # inputs at f4fe230, as audited
    'absorption-b003/results/chain.json': '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
    'absorption-b003/results/validated.json': 'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b',
    'route-b-dissipation/results/bounds.review.json': '4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
    'route-b-tightening/results/time_refinement.final.json': '79612f1164e92243b74ef40dd668651bc850ffa81d82695d7c59f039e119e849',
    'z2-endpoint/results/endpoint.json': '37368b9c6c7781e9cc691deb4742fd56e194c4ee80bed0b6a517e2425d8ab0bc',
}
for name, h in PINS.items():
    if sha(FT / name) != h: raise SystemExit('pinned input mismatch ' + name)
J = lambda p: json.loads((FT / p).read_text())
chain, val, rb, trf, ep, hull = (J('absorption-b003/results/chain.json'), J('absorption-b003/results/validated.json'),
    J('route-b-dissipation/results/bounds.review.json'), J('route-b-tightening/results/time_refinement.final.json'),
    J('z2-endpoint/results/endpoint.json'), J('source-only-hull/results/full.json'))
cpc = json.loads(CPC.read_text())
X = iv.mpf
up = lambda x: x.b
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from mpmath import nstr
def fup(x, nd):   # decimal display rounded toward +infinity (nudged past the 50-digit conversion)
    v = mpf(x.b if hasattr(x, 'b') else x)   # point interval -> exact mpf
    return str((Decimal(nstr(v, 50, strip_zeros=False)) + Decimal('1e-40')).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_CEILING))
def fdn(x, nd):   # decimal display rounded toward -infinity
    v = mpf(x.a if hasattr(x, 'a') else x)   # point interval -> exact mpf
    return str((Decimal(nstr(v, 50, strip_zeros=False)) - Decimal('1e-40')).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_FLOOR))
n = 250; D = X(1) / 1000; nu = X(1) / 28; T = X(1) / 4; beta = X(3) / 1000
# ---------------------------------------------------------------- per-cell chain rows: verify against the committed chain
rows = cpc['log']; assert len(rows) == n
for k in range(5):
    j = 50 * k + 49
    assert tuple(float(s) for s in rows[j]) == tuple(chain['log'][k]), ('per-cell chain disagrees with committed log at cell', j)
for key, col in (('K', 10), ('N_w', 9), ('eps0', 4), ('eps1', 5), ('delta2', 6), ('epsW', 3)):
    assert cpc[key] == chain[key], ('final value differs', key)
col = lambda c: [X(r[c]) for r in rows]
m1c, m2c, e0c, e1c, dlc, S1c, sgc, Nc, Kc = col(1), col(2), col(4), col(5), col(6), col(7), col(8), col(9), col(10)
cell = lambda key: [iv.mpf(float(v)) for v in val['cells'][key]]
pc, n1c, n2c = cell('sup_absq'), cell('sup_absgradq'), cell('sup_abshessq')
C = X(chain['C_A']); S = X(chain['S1'])
G = X(ep['bounds']['base_true_laplacian_upper']['hi'])
assert G.b <= X('1.8534').a
# own analytic m1 per cell (alpha at left, E1 at right) must not exceed the chain's (same formula)
for j in range(n):
    al = iv.exp(-nu * (D * j)); e1 = (1 - iv.exp(-nu * (D * (j + 1)))) / nu
    assert iv.sqrt(al ** 2 + 4 + (1 + 2 * e1) ** 2).b <= m1c[j].b * (1 + mpf('1e-30'))
assert all(m.a > nu.b for m in m1c)
# ---------------------------------------------------------------- J2 lower bound (DERIVATION.md section 1-2, variant B)
assert [r['coarse_cell'] for r in hull['rows']] == list(range(n)) and all((r['first_node'], r['last_node']) == (50 * l, 50 * l + 50) for l, r in enumerate(hull['rows']))
Uc = [X(r['source_norm_upper_exact']) for r in hull['rows']]
eps0, eps1, delta = X(chain['eps0']), X(chain['eps1']), X(chain['delta2'])
p_max = iv.mpf(float(max(val['cells']['sup_absq']))); n1_max = iv.mpf(float(max(val['cells']['sup_absgradq'])))
dF = T * (n1_max * eps0 + p_max * eps1) + C * eps1 * iv.sqrt(T * delta)
m1s = []
for j in range(n):
    al = iv.exp(-nu * (D * j)); e1 = (1 - iv.exp(-nu * (D * (j + 1)))) / nu
    m1s.append(iv.sqrt(al ** 2 + 4 + (1 + 2 * e1) ** 2))
tail = [iv.mpf(0)] * (n + 1)
for j in range(n - 1, -1, -1): tail[j] = tail[j + 1] + (m1s[j] - nu) * D
VT = sum((iv.exp(tail[l]) * D * Uc[l] for l in range(n)), iv.mpf(0)) + iv.exp(tail[0]) * dF
free = iv.exp(-2 * nu * T) / 4
E = X([ep['bounds']['half_q1_gradient_squared']['lo'], ep['bounds']['half_q1_gradient_squared']['hi']])
J2_lo = (E.a - free.b - (G * VT).b).a; J2_hi = (E.b - free.a + (G * VT).b).b
assert f'{float(J2_lo):+.6f}' == '+0.008201', 'J2 lower bound differs from the reviewed first stage'
# ---------------------------------------------------------------- global constants (route-b-tightening) for the Lemma B cap
bg = {k: X(v['hi']) for k, v in rb['bounds'].items()}
M1g, M2g, Kg, Ng, sgg, e1g, dlg, n1g, n2g, pg = (bg[k] for k in ('M1', 'M2', 'K', 'Nw', 'sigma', 'eps1', 'delta_e', 'n1', 'n2', 'p'))
ag = 2 * M1g + 2 * beta * n1g; q = 2 * beta ** 2 * C ** 2 / nu; cg = (M2g + beta * n2g) * Ng
f0 = cg * Kg + 4 * sgg ** 2 / nu; fd = 4 * C ** 2 * e1g ** 2 / nu
def gcap(t):
    z = iv.exp(2 * ag * t)
    return iv.exp(2 * q * dlg) * (f0 / ag * (z - 1) + 2 * fd * dlg * z)
# ---------------------------------------------------------------- A. cumulative retained dissipation D_w,j (no cell differencing)
Dw = []; acc = iv.mpf(0)
for i in range(n):
    Y = iv.mpf(min(up(Kc[i] ** 2), up(gcap(D * (i + 1)))))
    a_i = 2 * m1c[i] + 2 * beta * n1c[i]; c_i = (m2c[i] + beta * n2c[i]) * Nc[i]
    acc = acc + (a_i * Y + c_i * iv.sqrt(Y) + (4 / nu) * sgc[i] ** 2) * D
    Dw.append((8 / nu) * (acc + (q * Kc[i] ** 2 + (4 / nu) * C ** 2 * e1c[i] ** 2) * dlc[i]))
Dw_global = X(trf['Dw']['hi'])
assert up(Dw[-1]) <= up(Dw_global), 'time-resolved D_w exceeds the global bound'
# ---------------------------------------------------------------- lattice constant
r = np.arange(-32, 33); k2 = (r[:, None, None] ** 2 + r[None, :, None] ** 2 + r[None, None, :] ** 2).ravel()
vals, counts = np.unique(k2[k2 > 0], return_counts=True); assert counts.sum() == 65 ** 3 - 1
def Ahat(lam):
    corr = iv.mpf(0)
    for m, cnt in zip(vals.tolist(), counts.tolist()): corr += cnt * lam / (X(m) ** 2 * (lam + X(m) ** 2))
    return C ** 2 - corr
# ---------------------------------------------------------------- propagator weights
Cm = [iv.mpf(0)]; Cq = [iv.mpf(0)]
for i in range(n):
    Cm.append(Cm[-1] + (m1c[i] - nu) * D); Cq.append(Cq[-1] + (4 * m1c[i] + 1) * D)
Ew = {(i, j): iv.exp(Cm[j + 1] - Cm[i]) for j in range(n) for i in range(j + 1)}   # exact partial sums of explicit cell bounds
Qw = {(i, j): iv.exp(Cq[j + 1] - Cq[i]) for j in range(n) for i in range(j + 1)}
Pw = [iv.exp(Cm[n] - Cm[i]) for i in range(n)]
def abel(phi_hi, B):
    """Upper bound of sum_i phi_i X_i, X_i >= 0, given cumulative bounds sum_{k<=i} X_k <= B_i and phi nonincreasing (exact mpf)."""
    m = len(phi_hi); tot = iv.mpf(phi_hi[-1]) * B[m - 1]
    for i in range(m - 1): tot = tot + (iv.mpf(phi_hi[i]) - iv.mpf(phi_hi[i + 1])) * B[i]
    return tot
def nonincreasing_majorant(w_hi):
    out = list(w_hi)
    for i in range(len(out) - 2, -1, -1): out[i] = max(out[i], out[i + 1])
    return out
# ---------------------------------------------------------------- synthetic self-checks (PLAN.md implementation check 2)
def _selfcheck():
    from fractions import Fraction as Fr
    # geometric closed form: constant rate c, sum_{i<=j} exp(c (j-i+1) D) D = D e^{cD}(e^{c(j+1)D}-1)/(e^{cD}-1)
    c = X('0.7'); pre = [iv.mpf(0)]
    for i in range(30): pre.append(pre[-1] + c * D)
    for j in (0, 7, 29):
        s = sum((iv.exp(pre[j + 1] - pre[i]) for i in range(j + 1)), iv.mpf(0)) * D
        closed = D * iv.exp(c * D) * (iv.exp(c * (j + 1) * D) - 1) / (iv.exp(c * D) - 1)
        assert s.a <= closed.b and closed.a <= s.b, ('geometric check', j)
    # summation by parts with a nonincreasing majorant against a direct sum (exact rationals)
    Xs = [Fr((7 * i * i + 3) % 11, 5) for i in range(40)]
    w = [Fr((13 * i + 5) % 17 + 1, 3) for i in range(40)]
    phi = [max(w[i:]) for i in range(40)]
    B = []; s = Fr(0)
    for x in Xs: s += x; B.append(s)
    direct = sum(wi * xi for wi, xi in zip(w, Xs))
    via = phi[-1] * B[-1] + sum((phi[i] - phi[i + 1]) * B[i] for i in range(39))
    assert via == sum(p * x for p, x in zip(phi, Xs)) and via >= direct
    # the interval implementation of the same bound encloses the exact value
    val_ = abel([mpf(p.numerator) / p.denominator for p in phi], [X(b.numerator) / b.denominator for b in B])
    assert val_.b >= mpf(via.numerator) / via.denominator - mpf('1e-50')
    assert nonincreasing_majorant([3, 1, 2, 0]) == [3, 2, 2, 0]
_selfcheck()
print('synthetic self-checks passed', flush=True)
# ---------------------------------------------------------------- C-F, generic over inputs so that the collapse check uses the same code
def evaluate(cells, E_, Q_, P_, Iinf, tend, terminal_reuse):
    K_, N_, e1_, dl_, p_, n1_, m2_ = cells
    A = [p_[i] * K_[i] + n1_[i] * N_[i] for i in range(n)]
    h = [e1_[i] + beta * K_[i] for i in range(n)]
    Nr = []
    for j in range(n):
        s1 = sum((E_(i, j) * A[i] for i in range(j + 1)), iv.mpf(0)) * D
        s2 = C * E_(0, j) * K_[j] * iv.sqrt(tend(j) * dl_[j])
        s3 = iv.sqrt(sum((E_(i, j) ** 2 * h[i] ** 2 for i in range(j + 1)), iv.mpf(0)) * D) * iv.sqrt(Iinf[j])
        Nr.append(s1 + s2 + s3)
    if terminal_reuse: Nr = [Nr[-1]] * n
    Er = []
    for j in range(n):
        t1 = sum((Q_(i, j) * m2_[i] ** 2 * Nr[i] ** 2 for i in range(j + 1)), iv.mpf(0)) * D
        u1 = iv.sqrt(sum((Q_(i, j) * A[i] ** 2 for i in range(j + 1)), iv.mpf(0)) * D)
        u2 = iv.sqrt(Q_(0, j) * C ** 2 * K_[j] ** 2 * dl_[j])
        phi = nonincreasing_majorant([up(Q_(i, j) * h[i] ** 2) for i in range(j + 1)])
        u3 = iv.sqrt(abel(phi, Iinf[:j + 1]))
        Er.append(iv.sqrt(t1 + (u1 + u2 + u3) ** 2 / nu))
    if terminal_reuse: Er = [Er[-1]] * n
    a = sum((P_(i) * (p_[i] * Er[i] + n1_[i] * Nr[i]) for i in range(n)), iv.mpf(0)) * D
    b = C * iv.mpf(max(up(P_(i) * Er[i]) for i in range(n))) * iv.sqrt(T * dl_[-1])
    c = C * iv.mpf(max(up(P_(i) * e1_[i]) for i in range(n))) * iv.sqrt(T * Dr)
    d1 = iv.sqrt(sum((P_(i) ** 2 * K_[i] ** 2 for i in range(n)), iv.mpf(0)) * D) * iv.sqrt(Iinf[-1])
    d2 = iv.sqrt(sum((P_(i) * K_[i] ** 2 for i in range(n)), iv.mpf(0)) * D) * iv.sqrt(abel(nonincreasing_majorant([up(P_(i)) for i in range(n)]), Iinf))
    Nbar = a + b + c + iv.mpf(min(up(d1), up(d2)))
    return dict(Nr=Nr[-1], Er=Er[-1], Nbar=Nbar, parts=dict(smooth=a, err_adv=b, err_grad=c, self_d1=d1, self_d2=d2))
cells_tr = (Kc, Nc, e1c, dlc, pc, n1c, m2c)
cells_gl = tuple([v] * n for v in (Kg, Ng, e1g, dlg, pg, n1g, M2g))
Eg, Qg, Pg = iv.exp((M1g - nu) * T), iv.exp((4 * M1g + 1) * T), iv.exp((M1g - nu) * T)
results = {}
for lam_s in ('100', '10000', '100000', '1000000', '10000000'):
    lam = X(lam_s); Ah = Ahat(lam); row = trf['rows'][lam_s]; Dr = X(row['Dr']['hi'])
    # collapse check: global inputs, global weights, global I_inf, terminal reuse
    Iinf_g = Ah * (lam * T * Ng ** 2 + Dw_global)
    col_ = evaluate(cells_gl, lambda i, j: Eg, lambda i, j: Qg, lambda i: Pg, [Iinf_g] * n, lambda j: T, True)
    for key in ('Nr', 'Er', 'Nbar'):
        ref = X(row[key]['hi']); rel = abs((col_[key] - ref) / ref).b
        assert rel < mpf('1e-25'), ('collapse check failed', lam_s, key, float(rel))
    # time-resolved
    cumN = []; acc = iv.mpf(0)
    for i in range(n): acc = acc + Nc[i] ** 2 * D; cumN.append(acc)
    Iinf = [Ah * (lam * cumN[j] + Dw[j]) for j in range(n)]
    tr = evaluate(cells_tr, lambda i, j: Ew[(i, j)], lambda i, j: Qw[(i, j)], lambda i: Pw[i], Iinf, lambda j: D * (j + 1), False)
    for key in ('Nr', 'Er', 'Nbar'): assert up(tr[key]) <= up(col_[key]), ('monotonicity', lam_s, key)
    Cone = G * tr['Nbar'] + S * tr['Er']; Cend = Cone + Kc[-1] ** 2 / 2
    results[lam_s] = dict(Ahat=up(Ah), Iinf_T=up(Iinf[-1]), Nr_T=up(tr['Nr']), Er_T=up(tr['Er']), Nbar=up(tr['Nbar']),
                          parts={k: up(v) for k, v in tr['parts'].items()}, C_one=up(Cone), C_end=up(Cend),
                          global_Nbar=up(col_['Nbar']), global_Er=up(col_['Er']))
    print(f'lambda {lam_s:>9s}: N_r(T) <= {fup(tr["Nr"], 4):>11s}  E_r(T) <= {fup(tr["Er"], 4):>10s}  Nbar <= {fup(tr["Nbar"], 4):>11s}'
          f'  (global {fup(col_["Nbar"], 3):>10s})   C_one <= {fup(Cone, 3):>10s}', flush=True)
best = min(results, key=lambda k: results[k]['C_one'])
Cbest = iv.mpf(results[best]['C_one']); rhs = (beta ** 2 * Cbest).b
decided = J2_lo > rhs
Hlo = (iv.mpf(J2_lo) - rhs).a
print(f'\nbest lambda {best}: C_one,TR <= {fup(Cbest, 4)}   (one-sided, all 0<|b|<=0.003)')
print(f'decision rule (D):  J2_lo >= {fdn(J2_lo, 10)}  >  beta^2 C_one,TR <= {fup(rhs, 10)} ?  ->  {"CERTIFIED (conditional): H_b(T) > 0 for every 0 < |b| <= 0.003" if decided else "NOT CERTIFIED"}')
print(f'lower bound of H_b/b^2 at |b| = 0.003: >= {fdn(Hlo, 10)}')
bstar = None
if J2_lo > 0:
    bstar = iv.sqrt(iv.mpf(J2_lo) / Cbest).a
    assert bstar < beta.a or decided
    print(f'positive sign proved (conditional) for 0 < |b| < {fdn(bstar, 9)} with C_one,TR')
out = dict(status='new derivation (PLAN.md A-F), not independently reviewed; conditional on inherited certificates',
           decision_rule='J2_lo > beta^2 C_one,TR', certified=bool(decided), J2_lo=str(J2_lo), J2_hi=str(J2_hi),
           best_lambda=best, C_one_TR=str(Cbest.b), b_star_lower=(str(bstar) if bstar is not None else None), beta2_C_one_TR=str(rhs), H_over_b2_lower_at_beta=str(Hlo),
           per_lambda={k: {kk: (str(vv) if not isinstance(vv, dict) else {a: str(b) for a, b in vv.items()}) for kk, vv in v.items()} for k, v in results.items()},
           Dw_TR_T=str(up(Dw[-1])), Dw_global=str(up(Dw_global)), inputs_sha256=PINS, chain_percell_sha256=sha(CPC),
           source_sha256=sha(__file__), plan_sha256=sha(Path(__file__).resolve().parent.parent / 'PLAN.md'),
           wall_seconds=time.monotonic() - t0)
with OUT.open('x') as f: json.dump(out, f, indent=1); f.write('\n')
print(f'D_w,TR(T) <= {fup(Dw[-1], 3)}  (global {fup(Dw_global, 3)});  wall {out["wall_seconds"]:.1f} s; wrote {OUT.name}')
