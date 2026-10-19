"""Independent transcription of route-b NOTE.md formulas (1), (3), (5), (7), (8), written from the note,
not from bounds.py. 90-digit decimal, nearest rounding: a cross-check of the formulas, not a certificate."""
import json, sys
from decimal import Decimal as D, getcontext
getcontext().prec = 90
F = sys.argv[1]
ch = json.load(open(F + '/absorption-b003/results/chain.json'))
val = json.load(open(F + '/absorption-b003/results/validated.json'))
out = json.load(open(F + '/route-b-dissipation/results/bounds.json'))['bounds']
nu, T, beta = D(1) / D(28), D(1) / D(4), D(3) / D(1000)
C = D(ch['C_A']); K = D(ch['K']); N = D(ch['N_w']); S = D(ch['S1'])
eps0, eps1, delta = D(ch['eps0']), D(ch['eps1']), D(ch['delta2'])
mx = lambda k: max(D(x) for x in val['cells'][k])
p, n1, n2, sN = mx('sup_absq'), mx('sup_absgradq'), mx('sup_abshessq'), mx('sup_gradq')
exp, sqrt = lambda x: x.exp(), lambda x: x.sqrt()
# parent section 2 at a = c = d = 1: gamma = 2, alpha <= 1, gamma1 = 1 + 2E1, gamma2 = 1 + 4E1 + (4/nu)(E1 - E2)
E1 = (1 - exp(-nu * T)) / nu; E2 = (1 - exp(-2 * nu * T)) / (2 * nu)
g1 = 1 + 2 * E1; g2 = 1 + 4 * E1 + (4 / nu) * (E1 - E2)
M1 = sqrt(1 + 4 + g1**2); M2 = sqrt(1 + 4 + 2 * g1**2 + g2**2); MD = sqrt(1 + (2 + g2)**2)
sigma = p * sN + n1 * eps0 + p * eps1
# (W) integrated from 0 with w(0) = 0, Y <= b^4 K^2, ||w|| <= b^2 N, int d_e^2 <= delta, divided by b^4
H = ((2 * M1 + 2 * beta * n1) * K**2 * T + 2 * beta**2 * C**2 * K**2 * delta / nu
     + (M2 + beta * n2) * N * K * T + (4 / nu) * (sigma**2 * T + C**2 * eps1**2 * delta))
Dw = (8 / nu) * H
def lin(L, J):  # (3)
    NX = exp((M1 - nu) * T) * L
    EX2 = exp((4 * M1 + 1) * T) * (M2**2 * NX**2 * T + J / nu)
    DX = (2 / nu) * ((2 * M1 + D('0.5')) * EX2 * T + D('0.5') * M2**2 * NX**2 * T + J / (2 * nu))
    return NX, sqrt(EX2), DX
A = p * K + n1 * N; Hh = C * (eps1 + beta * K)
Lr = A * T + C * K * sqrt(T * delta) + Hh * sqrt(T * Dw)
Jr = 3 * (A**2 * T + C**2 * K**2 * delta + Hh**2 * Dw)
Nr, Er, Dr = lin(Lr, Jr)
Lbar = (p * Er + n1 * Nr) * T + C * Er * sqrt(T * delta) + C * eps1 * sqrt(T * Dr) + C * K * sqrt(T * Dw)
Nbar = exp((M1 - nu) * T) * Lbar
CB = MD * Nbar + S * Er + K**2 / 2
mine = dict(M1=M1, M2=M2, MDelta=MD, sigma=sigma, Dw=Dw, Lr=Lr, Jr=Jr, Nr=Nr, Er=Er, Dr=Dr, Nbar=Nbar, CZ=CB, RZ_at_beta=beta**4 * CB)
ok = True
for k, x in mine.items():
    lo, hi = D(out[k]['lo']), D(out[k]['hi'])
    inside = lo - abs(lo) * D('1e-60') <= x <= hi + abs(hi) * D('1e-60')
    ok &= inside
    print(f'{k:11s} independent {float(x):.10e}  in [lo, hi] of bounds.json: {inside}   rel width {float((hi - lo) / hi):.1e}')
print('ALL INSIDE:', ok)
