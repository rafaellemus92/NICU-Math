"""Enclose J2 = Z2(T) - exp(-2 nu T)/4 and H_b/b^2 from the recorded certificates (f4fe230), in mpmath interval
arithmetic. Variant A: recorded |M| bound. Variant B (new derivation, pending review): time-weighted propagator
||V(T)|| <= sum_l exp(int_{s_l}^T (m1-nu)) int_cell||F_N|| + exp(int_0^T (m1-nu)) DeltaF, with per-cell analytic m1."""
import sys, json
from mpmath import iv, mpf
iv.dps = 60
F = sys.argv[1]
import hashlib
PINS = {  # inputs at f4fe230 (audit repair 1: full.json sets J2_lo and was unpinned)
    'source-only-hull/results/full.json': '0d2ab266fd226091a9116b83c54621ad480f2b8306f16e9dd830a705629cfa82',
    'z2-endpoint/results/endpoint.json': '37368b9c6c7781e9cc691deb4742fd56e194c4ee80bed0b6a517e2425d8ab0bc',
    'route-b-tightening/results/time_refinement.final.json': '79612f1164e92243b74ef40dd668651bc850ffa81d82695d7c59f039e119e849',
    'absorption-b003/results/chain.json': '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
    'absorption-b003/results/validated.json': 'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b',
    'route-b-dissipation/results/bounds.review.json': '4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
}
for _name, _h in PINS.items():
    if hashlib.sha256(open(F + '/' + _name, 'rb').read()).hexdigest() != _h: raise SystemExit('pinned input mismatch ' + _name)
J = lambda p: json.load(open(F + '/' + p))
hull = J('source-only-hull/results/full.json'); ep = J('z2-endpoint/results/endpoint.json')
tr = J('route-b-tightening/results/time_refinement.final.json')['rows']['1000000']
chain = J('absorption-b003/results/chain.json'); val = J('absorption-b003/results/validated.json')
X = iv.mpf
nu, T, beta = X(1) / 28, X(1) / 4, X(3) / 1000
free = iv.exp(-2 * nu * T) / 4                                   # b^2 exp(-2 nu T)/4: free heat decay of b sin z e_y
E = X([ep['bounds']['half_q1_gradient_squared']['lo'], ep['bounds']['half_q1_gradient_squared']['hi']])
G = X(ep['bounds']['base_true_laplacian_upper']['hi'])
C_A, K, S, eps0, eps1, delta = [X(chain[k]) for k in ('C_A', 'K', 'S1', 'eps0', 'eps1', 'delta2')]
p = iv.mpf(float(max(val['cells']['sup_absq']))); n1 = iv.mpf(float(max(val['cells']['sup_absgradq'])))
dF = T * (n1 * eps0 + p * eps1) + C_A * eps1 * iv.sqrt(T * delta)
Uc = [X(r['source_norm_upper_exact']) for r in hull['rows']]; assert len(Uc) == 250
D = X(1) / 1000
# A: recorded certificate, |M| <= G exp((M1-nu)T) (L_N + DeltaF)
absM_A = X(hull['bounds']['abs_M_majorant']['hi'])
# B: per-cell analytic m1 (alpha at left endpoint, E1 at right endpoint), cumulative exponent from cell l to T
m1 = []
for j in range(250):
    al = iv.exp(-nu * (D * j)); e1 = (1 - iv.exp(-nu * (D * (j + 1)))) / nu
    m1.append(iv.sqrt(al ** 2 + 4 + (1 + 2 * e1) ** 2))           # |c|+|d| = 2, gamma1 = 1 + 2 E1(t)
tail = [iv.mpf(0)] * 251
for j in range(249, -1, -1): tail[j] = tail[j + 1] + (m1[j] - nu) * D
assert all(lo > nu for lo in [m.a for m in m1])
VT_B = sum((iv.exp(tail[l]) * D * Uc[l] for l in range(250)), iv.mpf(0)) + iv.exp(tail[0]) * dF
absM_B = G * VT_B
# B' : constant M1 (as in the hull note) but time-weighted
M1 = X(J('route-b-dissipation/results/bounds.review.json')['bounds']['M1']['hi'])
VT_Bc = sum((iv.exp((M1 - nu) * (T - D * l)) * D * Uc[l] for l in range(250)), iv.mpf(0)) + iv.exp((M1 - nu) * T) * dF
absM_Bc = G * VT_Bc
Cend = X(tr['C_endpoint']['hi']); Cone = X('1.8534') * X(tr['Nbar']['hi']) + S * X(tr['Er']['hi'])   # one-sided: drop K^2/2 >= 0
def J2(absM): return ((E.a - free.b - absM.b).a, (E.b - free.a + absM.b).b)
def show(label, absM):
    lo, hi = J2(absM)
    print(f'{label:44s} |M| <= {float(absM.b):.6f}   J2 in [{float(lo):+.6f}, {float(hi):+.6f}]   sign(J2) {"> 0 certified" if lo > 0 else "undetermined"}')
    return lo, hi
print(f'free decay exp(-2nuT)/4 in [{float(free.a):.9f}, {float(free.b):.9f}];  E - free in [{float((E.a-free.b).a):.6f}, {float((E.b-free.a).b):.6f}]')
loA, hiA = show('A  recorded certificate (hull note)', absM_A)
loC, hiC = show("B' time-weighted, constant M1", absM_Bc)
loB, hiB = show('B  time-weighted, per-cell m1(t)', absM_B)
print(f'||V(T)|| <= {float(VT_B.b):.6f} (B)  vs recorded {float((absM_A/G).b):.6f}')
b2C, b2Co = beta ** 2 * Cend, beta ** 2 * Cone
print(f'remainder at |b| = 0.003: two-sided b^2 C_endpoint <= {float(b2C.b):.6f};  one-sided (positive sign only, K^2/2 dropped) <= {float(b2Co.b):.6f}')
for label, lo, hi in (('A', loA, hiA), ('B', loB, hiB)):
    Hlo = (lo - b2Co.b).a; Hhi = (hi + b2C.b).b
    print(f'{label}: H_b/b^2 at |b|=0.003 in [{float(Hlo):+.6f}, {float(Hhi):+.6f}]   sign {"determined" if Hlo > 0 or Hhi < 0 else "undetermined"}')
    if lo > 0:
        bstar = iv.sqrt(lo / Cone.b)
        print(f'   positive sign proved only for 0 < |b| < {float(bstar.a):.6e}  (fixed target |b| <= 0.003 NOT met)')
need_C_now = (loB / beta ** 2).a                     # lower end: the requirement is C < this
print(f'required one-sided constant for the fixed range with J2_lo(B): C < {float(need_C_now):.1f}   (current {float(Cone.b):.1f}, factor {float((Cone.b / need_C_now).b):.2f})')
J2_meas = (iv.mpf('0.26658869158967474') - free).a           # uncertified numerical value, point-ish
M_meas = 0.26658869158967474 - 0.7496102395109782 ** 2 / 2
print(f'uncertified N=24 hierarchy: Z2(T) = 0.266589, J2 ~ {float(J2_meas):.6f}, M ~ {M_meas:+.6f}; inside B enclosure: {bool(loB < J2_meas < hiB)}; |M| inside B bound: {abs(M_meas) < float(absM_B.b)}')
need_exact = (J2_meas / beta ** 2).a
print(f'required one-sided constant even with an exact J2 (~{float(J2_meas):.5f}): C < {float(need_exact):.1f}  (factor {float((Cone.b / need_exact).b):.2f})')
print(f'uncertified ||V(T)|| <= ||grad V(T)|| = 0.014139 (Poincare) versus certified time-weighted bound {float(VT_B.b):.6f}')
