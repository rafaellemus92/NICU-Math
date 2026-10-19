"""Independent re-evaluation of the final scalar inequalities with mpmath interval arithmetic (outward rounding),
from primitive inputs only: chain.json strings, validated.json cell maxima, exact endpoint fractions, reproduced hull rows."""
import sys, json
import numpy as np
from mpmath import iv, mpf
iv.dps = 60
F, hull_json, fracs = sys.argv[1], sys.argv[2], sys.argv[3]
chain = json.load(open(F + '/absorption-b003/results/chain.json'))
val = json.load(open(F + '/absorption-b003/results/validated.json'))
ex = json.load(open(fracs)); rows = json.load(open(hull_json))['rows']
X = lambda s: iv.mpf(s)                         # encloses the decimal string
up = lambda x: x.b; lo = lambda x: x.a
P = lambda v: iv.mpf([v, v])                    # point interval at an mpf
nu, T, beta = X(1) / 28, X(1) / 4, X(3) / 1000
C, K, N, S, eps0, eps1, delta, epsW = [X(chain[k]) for k in ('C_A', 'K', 'N_w', 'S1', 'eps0', 'eps1', 'delta2', 'epsW')]
mx = lambda k: X(repr(max(val['cells'][k])))   # binary float written exactly enough; iv.mpf rounds outward
p, n1, n2, sN = [mx(k) for k in ('sup_absq', 'sup_absgradq', 'sup_abshessq', 'sup_gradq')]
# analytic base-flow envelopes (alpha <= 1, gamma = |c|+|d| = 2)
E1 = (1 - iv.exp(-nu * T)) / nu; E2 = (1 - iv.exp(-2 * nu * T)) / (2 * nu)
g1 = 1 + 2 * E1; g2 = 1 + 4 * E1 + (4 / nu) * (E1 - E2)
M1 = iv.sqrt(5 + g1 ** 2); M2 = iv.sqrt(5 + 2 * g1 ** 2 + g2 ** 2)
assert lo(M1) > up(nu)
sigma = p * sN + n1 * eps0 + p * eps1
# closure assumptions at beta (certificate)
assert up(C * (beta * S + beta ** 2 * K)) < lo(nu / 2) and up(beta * C * eps1) < lo(nu / 8)
# Lemma B: zero-initial-energy cap, 1000-cell right sum of min(K^2, g)
a = 2 * M1 + 2 * beta * n1; q = 2 * beta ** 2 * C ** 2 / nu; c = (M2 + beta * n2) * N
f0 = c * K + 4 * sigma ** 2 / nu; fd = 4 * C ** 2 * eps1 ** 2 / nu
h = T / 1000; Iy_hi = mpf(0)
for j in range(1, 1001):
    t = h * j; z = iv.exp(2 * a * t)
    g = iv.exp(2 * q * delta) * (f0 / a * (z - 1) + 2 * fd * delta * z)
    Iy_hi += min(up(K ** 2), up(g))
Iy = P(Iy_hi) * P(up(h))                        # upper sum (product rounded outward below)
Iy = iv.mpf([0, up(Iy)])
Dw = (8 / nu) * (a * Iy + q * K ** 2 * delta + c * iv.sqrt(T * Iy) + (4 / nu) * (sigma ** 2 * T + C ** 2 * eps1 ** 2 * delta))
# Lemma A: resolvent lattice constant, cube R = 32, lambda = 1e6
lam = X(10) ** 6
r = np.arange(-32, 33); n2grid = (r[:, None, None] ** 2 + r[None, :, None] ** 2 + r[None, None, :] ** 2).ravel()
vals, counts = np.unique(n2grid[n2grid > 0], return_counts=True)
corr = iv.mpf(0)
for m, cnt in zip(vals.tolist(), counts.tolist()):
    corr += cnt * lam / (X(m) ** 2 * (lam + X(m) ** 2))
assert sum(counts) == 65 ** 3 - 1
Ahat = C ** 2 - corr
Iinf = Ahat * (lam * T * N ** 2 + Dw)
A = p * K + n1 * N; hh = eps1 + beta * K
Lr = A * T + C * K * iv.sqrt(T * delta) + hh * iv.sqrt(T * Iinf)
Jr = (A * iv.sqrt(T) + C * K * iv.sqrt(delta) + hh * iv.sqrt(Iinf)) ** 2
Nr = iv.exp((M1 - nu) * T) * Lr
Er = iv.sqrt(iv.exp((4 * M1 + 1) * T) * (M2 ** 2 * Nr ** 2 * T + Jr / nu))
Dr = (2 / nu) * ((2 * M1 + X(1) / 2) * Er ** 2 * T + M2 ** 2 * Nr ** 2 * T / 2 + Jr / (2 * nu))
Lbar = (p * Er + n1 * Nr) * T + C * Er * iv.sqrt(T * delta) + C * eps1 * iv.sqrt(T * Dr) + K * iv.sqrt(T * Iinf)
Pprop = iv.exp((M1 - nu) * T)
Nbar = Pprop * Lbar
# endpoint G from exact fractions
wsq = X(ex['wsq'][0]) / X(ex['wsq'][1]); gsq = X(ex['gradsq'][0]) / X(ex['gradsq'][1])
G_mine = up(iv.sqrt(iv.exp(-nu * T) ** 2 / 2 + wsq) + iv.sqrt(X(2) / 27) * epsW)
for label, Gv in (('G = 1.8534 (as used)', X('1.8534')), ('G = own exact upper', P(G_mine))):
    Cend = Gv * Nbar + S * Er + K ** 2 / 2
    print(f'{label:24s} C_endpoint <= {float(up(Cend)):.10f}   beta^2 C_endpoint <= {float(up(beta**2*Cend)):.12f}')
Cend = X('1.8534') * Nbar + S * Er + K ** 2 / 2; thr = beta ** 2 * Cend
# source-only comparison
LN = iv.mpf(0)
for rrow in rows: LN += X(rrow['source_norm_upper_exact'])
LN = LN / 1000
dF = T * (n1 * eps0 + p * eps1) + C * eps1 * iv.sqrt(T * delta)
LF = LN + dF
nN = iv.sqrt(gsq); Elo = (iv.mpf([max(mpf(0), lo(nN - eps1))] * 2)) ** 2 / 2; Ehi = (nN + eps1) ** 2 / 2
G = P(G_mine) if False else X('1.8534')
absM = P(up(iv.mpf(ex and 0) + 0)) if False else None
Grec = X(json.load(open(F + '/z2-endpoint/results/endpoint.json'))['bounds']['base_true_laplacian_upper']['hi'])
absM = Grec * Pprop * LF
Z2lo = lo(Elo) - up(absM); Z2hi = up(Ehi) + up(absM)
print(f'M1 <= {float(up(M1)):.8f}  M2 <= {float(up(M2)):.8f}  sigma <= {float(up(sigma)):.8f}  Pprop <= {float(up(Pprop)):.8f}')
print(f'I_y <= {float(up(Iy)):.8f}  D_w,new <= {float(up(Dw)):.6f}  Ahat <= {float(up(Ahat)):.9f}  I_inf <= {float(up(Iinf)):.6f}')
print(f'L_r <= {float(up(Lr)):.8f}  J_r <= {float(up(Jr)):.6f}  N_r <= {float(up(Nr)):.7f}  E_r <= {float(up(Er)):.6f}  D_r <= {float(up(Dr)):.1f}  N_bar <= {float(up(Nbar)):.5f}')
print(f'L_N <= {float(up(LN)):.15f}  DeltaF <= {float(up(dF)):.12e}  LF <= {float(up(LF)):.15f}')
print(f'E in [{float(lo(Elo)):.10f}, {float(up(Ehi)):.10f}]  G(recorded) = {float(up(Grec)):.12f}  own G <= {float(G_mine):.12f}')
print(f'|M| <= {float(up(absM)):.14f}   Z2(T) in [{float(Z2lo):.14f}, {float(Z2hi):.14f}]')
print(f'threshold beta^2 C_endpoint <= {float(up(thr)):.14f}')
print('Z2 lower > threshold:', Z2lo > up(thr), '  margin:', float(Z2lo - up(thr)), '  ratio threshold/Z2lo:', float(up(thr) / Z2lo))
print('LF <= 0.05:', up(LF) <= mpf('0.05'))
# exact-for-every-b statement: b^4 C <= b^2 beta^2 C < b^2 Z2lo for 0 < |b| <= beta
print('strict for all 0<|b|<=beta  <=>  Z2lo > beta^2 C  (b-independent Z2):', Z2lo > up(thr))
json.dump({k: str(up(v)) for k, v in dict(Cend=Cend, thr=thr, LF=LF, absM=absM, Dw=Dw, Ahat=Ahat, Nbar=Nbar, Er=Er).items()} | {'Z2lo': str(Z2lo)}, open(sys.argv[4], 'w'), indent=1)
