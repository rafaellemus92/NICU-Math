"""Independent re-derivation of the T = 1/2 adjoint certificate's final comparison (bundle ff29c90e).

Written from PROOF.md (t050-adjoint) and DERIVATION.md (t050-tightening), not from certify.py,
bounds.py or evaluate.py. Arithmetic: exact Fractions for the analytic adjoint constants and for the
cumulative N^2 sum; the parent's 40-digit directed-rounding decimal Iv class (constants.py at cd9c9f0,
sha256 996f39f1...) for everything else. mpmath is not used. Reads only bundle result files.

Usage: python3 -I -B independent_t050.py <bundle finite-time dir> <dir holding constants.py> <fresh output json>
"""
import sys, json, hashlib, importlib.util, time
from fractions import Fraction as Fr
from decimal import Decimal, localcontext
from collections import Counter
from pathlib import Path

t0 = time.monotonic()
FT, CONSTDIR, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
if OUT.exists():
    raise FileExistsError(OUT)
ART = FT / 'extension-t050/resource-amendment/artifacts'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(CONSTDIR / 'constants.py') == '996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014'
spec = importlib.util.spec_from_file_location('c', CONSTDIR / 'constants.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
I = c.Iv
report = {}
say = print

# ------------------------------------------------------------------ 0. input pins (all three manifests)
say('== 0. input hashes')
pins_ok, missing = [], []
for manifest, base in (('t050-tightening/INPUTS.json', ART), ('t050-self-gradient/INPUTS.json', FT), ('t050-adjoint/INPUTS.json', FT)):
    for name, h in json.loads((FT / manifest).read_text()).items():
        p = base / name
        if not p.exists():
            missing.append(f'{manifest}: {name}')
            continue
        assert sha(p) == h, ('hash mismatch', manifest, name)
        pins_ok.append(f'{manifest}: {name}')
for m in missing:
    say('   pinned but absent from bundle:', m)
say(f'   {len(pins_ok)} pinned files present and matching')
report['pins_matching'] = pins_ok; report['pins_absent'] = missing

J = lambda p: json.loads((ART / p).read_text())
chain, val, cpc = J('absorption-b003/results/chain.json'), J('absorption-b003/results/validated.json'), J('endpoint-sign/results/chain_percell.json')
ep, hull, trr = J('z2-endpoint/results/endpoint.json'), J('source-only-hull/results/full.json'), J('endpoint-sign/results/tr_remainder.repaired.json')
rb = J('route-b-dissipation/results/bounds.review.json')['bounds']
cert = json.loads((FT / 't050-adjoint/results/certificate-v1.json').read_text())
sg = json.loads((FT / 't050-self-gradient/results/candidate-v1.json').read_text())
tv2 = json.loads((FT / 't050-tightening/results/candidate-v2.json').read_text())

# ------------------------------------------------------------------ 1. analytic adjoint constants (exact)
say('== 1. adjoint strain constants, exact rationals')
def exp_upper(x, N=14):                       # sum_{k<=N} x^k/k! + geometric bound of the tail, 0 <= x < N+2
    s, term = Fr(0), Fr(1)
    for k in range(N + 1):
        s += term; term = term * x / (k + 1)
    return s + term / (1 - x / (N + 2))
def exp_lower(x, N=14):
    s, term = Fr(0), Fr(1)
    for k in range(N + 1):
        s += term; term = term * x / (k + 1)
    return s
eh = exp_upper(Fr(1, 2)); assert exp_lower(Fr(1, 2)) < eh < Fr(5, 3)
E = Fr(5, 3); assert E ** 3 < 5            # e^{3/2} < (5/3)^3 = 125/27 < 5
# polynomial majorants M_j <= e^t p_j(t); p as coefficient lists in t
p = {0: [2], 1: [1, 2], 2: [1, 4, 2], 3: [1, 8, 9, 2]}
binom = lambda n, k: Fr(1) if k in (0, n) else binom(n - 1, k - 1) + binom(n - 1, k)
deriv = lambda q: [k * q[k] for k in range(1, len(q))] or [0]
def padd(a, b):
    n = max(len(a), len(b)); return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]
def norm(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0: a.pop()
    return a
for j in range(4):                            # (e^t p_j)' = e^t (p_j + p_j') must equal e^t sum_l binom(j,l) p_l
    rhs = [0]
    for l in range(j):
        rhs = padd(rhs, [binom(j, l) * x for x in p[l]])
    assert norm(deriv(p[j])) == norm(rhs), ('majorant ODE', j)
init = {0: 2, 1: 1, 2: 1, 3: 1}               # W(y,0)=1-e^{i(y+phi)}: |W_0|=|W_1|=1 -> sum|n|^j|W_n|
assert all(p[j][0] >= init[j] for j in range(4))
ev = lambda q, t: sum(Fr(a) * t ** k for k, a in enumerate(q))
def consts(Eh):
    M = [Eh * ev(p[j], Fr(1, 2)) for j in range(4)]           # sup over [0,1/2] (increasing majorants)
    B00, B10 = M[0] + M[2], M[1] + M[3]                      # V(0)=W(T)-W_yy(T): sum(1+n^2)|W|, sum|n|(1+n^2)|W|
    B0 = Eh * B00                                            # B0' <= B0
    B1 = Eh * (B10 + Fr(1, 2) * B00)                         # B1' <= B1 + B0
    F = M[0] * B1 + M[1] * B0                                # ||w_x v_y||_W + ||w_y v_x||_W
    L = Eh ** 3 * (1 + F / 3) - F / 3                        # L' <= 3L + F, L(0) <= e^{-nu T} <= 1
    return M, B00, B10, B0, B1, F, L, L + B0 + B1
M, B00, B10, B0, B1, F, L, strain = consts(E)
assert M == [Fr(10, 3), Fr(10, 3), Fr(35, 6), Fr(25, 2)] and (B00, B10) == (Fr(55, 6), Fr(95, 6))
assert (B0, B1, F) == (Fr(275, 18), Fr(1225, 36), Fr(8875, 54))
assert L <= 5 + 4 * F / 3 == Fr(18155, 81)
strain_cert = Fr(18155, 81) + B0 + B1
assert strain_cert == Fr(88595, 324) < 274
# Biot-Savart factor and support used in L' <= 3L + F (|kx| <= 2 on h, kx in {0,+-2})
assert max(Fr(abs(kx * ky), kx * kx + ky * ky) for kx in range(-2, 3) for ky in range(-60, 61) if kx or ky) == Fr(1, 2)
tight = consts(eh)[-1]
say(f'   e^(1/2) < {float(eh):.15f} < 5/3; M = 10/3, 10/3, 35/6, 25/2; B0 = 275/18, B1 = 1225/36; F = 8875/54')
say(f'   strain <= 18155/81 + 275/18 + 1225/36 = 88595/324 = {float(strain_cert):.12f} < 274   (with the exact e^(1/2) bound: {float(tight):.6f})')
report['strain'] = dict(certificate=str(strain_cert), selected='274', exact_exp_variant=float(tight))

# ------------------------------------------------------------------ 2. cumulative ||W_b||^2 (exact)
say('== 2. integral of N_w^2 over 500 cells, exact')
rows = cpc['log']; n = 500
assert len(rows) == n and all(Fr(r[0]) == Fr(i + 1, 1000) for i, r in enumerate(rows)) and cpc['log_columns'][9] == 'N_w'
N2 = sum(Fr(r[9]) ** 2 for r in rows) / 1000
assert N2 == Fr(cert['bounds']['recomputed_exact_N_squared']['exact'])
assert N2 <= Fr(cert['bounds']['cumulative_N_squared']['exact']) and N2 <= Fr(sg['bounds']['cumulative_N_squared']['hi'])
self_obs = 274 * Fr(cert['bounds']['cumulative_N_squared']['exact'])
assert self_obs == Fr(cert['bounds']['self_observable_upper']['exact'])
say(f'   sum dt N_i^2 = {float(N2):.18f} (equals the certificate fraction); 274 * stored upper = {float(self_obs):.13f}')
report['N2_exact'] = str(N2)

with localcontext(c.TRAP):
    P_ = lambda d: I(Decimal(d))
    D, nu, T, beta = I.of('1/1000'), I.of('1/28'), I.of('1/2'), I.of('3/1000')
    col = lambda k: [P_(r[k]) for r in rows]
    m1, m2, e0, e1, dl, sgm, N, K = (col(k) for k in (1, 2, 4, 5, 6, 8, 9, 10))
    cell = lambda k: [P_(Decimal(x)) for x in val['cells'][k]]
    pq, n1, n2 = cell('sup_absq'), cell('sup_absgradq'), cell('sup_abshessq')
    CA = P_(chain['C_A']); S1 = P_(chain['S1'])
    G_in = P_(ep['bounds']['base_true_laplacian_upper']['hi'])
    hi = lambda x: x.hi

    # -------------------------------------------------------------- 3. endpoint quantities from exact fractions
    say('== 3. endpoint energy E and base Laplacian G from the stored exact fractions')
    gq2 = Fr(ep['exact_endpoint_fractions']['projected_q_gradient_squared'])
    lw2 = Fr(ep['exact_endpoint_fractions']['base_vertical_laplacian_squared'])
    gq = I(Decimal(gq2.numerator)) / I(Decimal(gq2.denominator))
    gq = gq.sqrt()
    E_lo_mine = ((gq - e1[-1]).sq() / 2).lo                  # ||grad q1|| >= ||grad qN|| - eps1(T)
    E_hi_mine = ((gq + e1[-1]).sq() / 2).hi
    epsW_T = P_(rows[-1][3])
    lw = (I(Decimal(lw2.numerator)) / I(Decimal(lw2.denominator)) + (-2 * nu * T).exp() / 2).sqrt()   # ||Delta U_N(T)||, sigma exact
    G_mine = lw + (I.of(2) / 27).sqrt() * epsW_T             # ||Delta(w-w_N)|| <= sqrt(2/27) ||.||_{*,3}, max at n=1
    E_in = ep['bounds']['half_q1_gradient_squared']
    say(f'   E_lo mine {E_lo_mine:.40}  stored {E_in["lo"]}')
    say(f'   E_hi mine {E_hi_mine:.40}  stored {E_in["hi"]}')
    say(f'   G    mine {G_mine.hi:.40}  stored {G_in.hi}')
    assert E_lo_mine >= c.LO.subtract(Decimal(E_in['lo']), Decimal('1e-38')) and G_mine.hi <= c.HI.add(G_in.hi, Decimal('1e-38'))
    # reconciliation: the committed pipeline uses chain.json's 5-significant-digit upper roundings of eps1(T), epsW(T)
    eps1_r, epsW_r = P_(chain['eps1']), P_(chain['epsW'])
    assert eps1_r.lo >= e1[-1].hi and epsW_r.lo >= epsW_T.hi
    E_lo_conv = ((gq - eps1_r).sq() / 2).lo
    E_hi_conv = ((gq + eps1_r).sq() / 2).hi
    G_conv = lw + (I.of(2) / 27).sqrt() * epsW_r
    say(f'   committed convention (eps1 = {chain["eps1"]}, epsW = {chain["epsW"]}):')
    say(f'   E_lo conv {E_lo_conv:.40}  E_hi conv {E_hi_conv:.40}  G conv {G_conv.hi:.40}')

    # -------------------------------------------------------------- 4. leading coefficient J2 (tightening section 2)
    say('== 4. J2 lower end with structural strain mu = m1/sqrt(3)')
    s3 = I.of(3).sqrt()
    mu = [m / s3 for m in m1]
    assert all((m - nu).lo >= 0 for m in mu)
    # P_i = exp(sum_{k>=i}(mu_k-nu)dt) as a product of per-cell factors (their code: one exp of the sum)
    fac = [((m - nu) * D).exp() for m in mu]
    Pw = [None] * n; acc = I.of(1)
    for i in range(n - 1, -1, -1):
        acc = acc * fac[i]; Pw[i] = acc
    assert [r['coarse_cell'] for r in hull['rows']] == list(range(n))
    U = [P_(r['source_norm_upper_exact']) for r in hull['rows']]
    Vs = sum((Pw[i] * U[i] for i in range(n)), I.of(0)) * D
    Vm = sum((Pw[i] * (n1[i] * e0[i] + pq[i] * e1[i]) for i in range(n)), I.of(0)) * D
    Ve = CA * (sum(((Pw[i] * e1[i]).sq() for i in range(n)), I.of(0)) * D * dl[-1]).sqrt()
    V = Vs + Vm + Ve
    free = (-2 * nu * T).exp() / 4
    J2lo = (P_(E_in['lo']) - free - G_in * V).lo
    J2lo_own_EG = (I(E_lo_mine) - free - G_mine * V).lo
    say(f'   V <= {V.hi:.25}  (source {Vs.hi:.12}, smooth error {Vm.hi:.6E}, dissipation error {Ve.hi:.6E})')
    say(f'   J2 >= {J2lo:.40}   committed {cert["bounds"]["J2_lower"]["lo"]}')
    say(f'   J2 >= {J2lo_own_EG:.40}   (with own E, G from the fractions)')

    # -------------------------------------------------------------- 5. inherited cumulative D_w and I_inf, own lattice Ahat
    say('== 5. inherited cumulative dissipation D_w and I_inf (lambda = 10^6), own resolvent constant')
    g = {k: P_(v['hi']) for k, v in rb.items()}
    a_g = 2 * g['M1'] + 2 * beta * g['n1']; q = 2 * beta.sq() * CA.sq() / nu
    f0 = (g['M2'] + beta * g['n2']) * g['Nw'] * g['K'] + 4 * g['sigma'].sq() / nu; fd = 4 * CA.sq() * g['eps1'].sq() / nu
    def gcap(t):
        z = (2 * a_g * t).exp()
        return (2 * q * g['delta_e']).exp() * (f0 / a_g * (z - 1) + 2 * fd * g['delta_e'] * z)
    R = 32; sq_ = [x * x for x in range(-R, R + 1)]
    hist = Counter(a + b + cc for a in sq_ for b in sq_ for cc in sq_); del hist[0]
    lam = I.of(1000000)
    Ahat = CA.sq() - sum((I.of(cnt) * lam / (I.of(s * s) * (lam + I.of(s * s))) for s, cnt in hist.items()), I.of(0))
    Dw, ii, acc, accN = [], [], I.of(0), I.of(0)
    cap_active = [i for i in range(n) if gcap(D * (i + 1)).hi < K[i].sq().hi]
    say(f'   cells where the global Lemma B cap (bounds.review.json) is below K_i^2: {len(cap_active)} of {n}')
    report['cap_active_cells'] = cap_active
    for i in range(n):
        Y = I(min(K[i].sq().hi, gcap(D * (i + 1)).hi))
        acc = acc + ((2 * m1[i] + 2 * beta * n1[i]) * Y + (m2[i] + beta * n2[i]) * N[i] * Y.sqrt() + 4 * sgm[i].sq() / nu) * D
        Dw.append(8 / nu * (acc + (q * K[i].sq() + 4 * CA.sq() * e1[i].sq() / nu) * dl[i]))
        accN = accN + N[i].sq() * D
        ii.append(Ahat * (lam * accN + Dw[-1]))
    strip = lambda s: Decimal(s.strip('[]').split(',')[1])
    rel = lambda a, b: abs(float(a) / float(b) - 1)
    say(f'   Ahat {Ahat.hi:.30}  stored {strip(trr["per_lambda"]["1000000"]["Ahat"]):.30}')
    say(f'   D_w(T) {Dw[-1].hi:.25}  stored {strip(trr["Dw_TR_T"]):.25}  rel {rel(Dw[-1].hi, strip(trr["Dw_TR_T"])):.1e}')
    say(f'   I_inf(T) {ii[-1].hi:.25}  stored {strip(trr["per_lambda"]["1000000"]["Iinf_T"]):.25}  rel {rel(ii[-1].hi, strip(trr["per_lambda"]["1000000"]["Iinf_T"])):.1e}')

    # -------------------------------------------------------------- 6. remainder R = r/b^3: Nr, Er, Jr, Dr (tightening section 3)
    say('== 6. remainder envelopes Nr, Er, Dr and the mean nonself observable')
    Cm, Cq, Cd = [I.of(0)], [I.of(0)], [I.of(0)]
    for i in range(n):
        Cm.append(Cm[-1] + (mu[i] - nu) * D); Cq.append(Cq[-1] + (4 * m1[i] + 1) * D); Cd.append(Cd[-1] + 2 * mu[i] * D)
    eM, eMi = [x.exp() for x in Cm], [(-x).exp() for x in Cm]
    eQ, eQi = [x.exp() for x in Cq], [(-x).exp() for x in Cq]
    eD, eDi = [x.exp() for x in Cd], [(-x).exp() for x in Cd]
    Ew = lambda i, j: eM[j + 1] * eMi[i]
    Qw = lambda i, j: eQ[j + 1] * eQi[i]
    Dweight = [eD[n] * eDi[i] for i in range(n)]
    for i in (0, 250, 499):                                    # product route and split-exp route enclose the same number
        assert Pw[i].lo <= Ew(i, n - 1).hi and Ew(i, n - 1).lo <= Pw[i].hi
    def majorant(w):
        out = list(w)
        for k in range(len(out) - 2, -1, -1): out[k] = max(out[k], out[k + 1])
        return out
    def abel(phi, B):                                          # sum phi_i x_i, prefix sums of x <= B_i, phi nonincreasing >= 0
        assert all(x >= 0 for x in phi)
        tot = I(phi[-1]) * B[len(phi) - 1]
        for k in range(len(phi) - 1): tot = tot + (I(phi[k]) - I(phi[k + 1])) * B[k]
        return tot
    A = [pq[i] * K[i] + n1[i] * N[i] for i in range(n)]
    h = [e1[i] + beta * K[i] for i in range(n)]
    Nr, Er, Dr, Jr = [], [], [], []; dacc = I.of(0)
    for j in range(n):
        tj = D * (j + 1); rng = range(j + 1)
        s1 = sum((Ew(i, j) * A[i] for i in rng), I.of(0)) * D
        s2 = CA * Ew(0, j) * K[j] * (tj * dl[j]).sqrt()
        s3 = (sum((Ew(i, j).sq() * h[i].sq() for i in rng), I.of(0)) * D * ii[j]).sqrt()
        Nr.append(s1 + s2 + s3)
        t1 = sum((Qw(i, j) * m2[i].sq() * Nr[i].sq() for i in rng), I.of(0)) * D
        u1 = (sum((Qw(i, j) * A[i].sq() for i in rng), I.of(0)) * D).sqrt()
        u2 = (Qw(0, j) * CA.sq() * K[j].sq() * dl[j]).sqrt()
        u3 = abel(majorant([hi(Qw(i, j) * h[i].sq()) for i in rng]), ii).sqrt()
        Er.append((t1 + (u1 + u2 + u3).sq() / nu).sqrt())
        jr = ((sum((A[i].sq() for i in rng), I.of(0)) * D).sqrt()
              + CA * abel(majorant([hi(K[i].sq()) for i in rng]), dl).sqrt()
              + abel(majorant([hi(h[i].sq()) for i in rng]), ii).sqrt()).sq()
        Jr.append(jr)
        dacc = dacc + D * ((2 * m1[j] + I.of('0.5')) * Er[j].sq() + m2[j].sq() * Nr[j].sq() / 2)
        Dr.append(2 / nu * (dacc + jr / (2 * nu)))
    smooth = sum((Pw[i] * (pq[i] * Er[i] + n1[i] * Nr[i]) for i in range(n)), I.of(0)) * D
    adv = CA * (sum(((Pw[i] * Er[i]).sq() for i in range(n)), I.of(0)) * D * dl[-1]).sqrt()
    grad_cs = CA * (sum(((Pw[i] * e1[i]).sq() for i in range(n)), I.of(0)) * D * Dr[-1]).sqrt()
    grad_ab = CA * (T * abel(majorant([hi((Pw[i] * e1[i]).sq()) for i in range(n)]), Dr)).sqrt()
    direct = smooth + adv + I(min(grad_cs.hi, grad_ab.hi))
    cross_s = 2 * (sum((Dweight[i] * pq[i].sq() * Nr[i].sq() for i in range(n)), I.of(0)) * D / (2 * nu)).sqrt()
    cross_e = 2 * CA * (abel(majorant([hi(Dweight[i] * Nr[i].sq()) for i in range(n)]), dl) / (2 * nu)).sqrt()
    cross = cross_s + cross_e
    nonself = min(direct.hi, cross.hi)
    tb = tv2['bounds']
    for name, mine, key in (('Nr(T)', Nr[-1], 'Nr_T'), ('Er(T)', Er[-1], 'Er_T'), ('Dr(T)', Dr[-1], 'Dr_T'), ('direct', direct, 'direct_nonself'),
                            ('cross', cross, 'cross_nonself')):
        say(f'   {name:7s} {mine.hi:.30}  committed {Decimal(tb[key]["hi"]):.30}  rel {rel(mine.hi, Decimal(tb[key]["hi"])):.1e}')
    say(f'   selected nonself = {"cross" if cross.hi < direct.hi else "direct"} {nonself:.30}')
    tolf = Decimal('1.000000000000000000000000000001')
    pc_ok = all(Nr[i].hi <= c.HI.multiply(Decimal(tv2['percell'][i]['Nr']['hi']), tolf) and
                Er[i].hi <= c.HI.multiply(Decimal(tv2['percell'][i]['Er']['hi']), tolf) for i in range(n))
    say(f'   all 500 per-cell Nr, Er within 1e-30 relative of the committed table: {pc_ok}')

    # -------------------------------------------------------------- 7. final comparison
    say('== 7. final comparison H_b(1/2)/b^2 >= J2_lo - beta^2 (274 int N^2 + G nonself + gradient)')
    qL_in = P_(sg['bounds']['qN_laplacian_norm']['hi'])       # ||Delta qN(T)||: read from the 529 MB array, not in the bundle
    qL_val = n2[-1] / I.of(2).sqrt()                          # validated-only: ||Delta q|| <= (1/sqrt2) sum|k|^2|Qhat|
    grad_in = qL_in * Nr[-1] + e1[-1] * Er[-1]
    grad_val = qL_val * Nr[-1] + e1[-1] * Er[-1]
    grad_conv = qL_in * Nr[-1] + eps1_r * Er[-1]              # committed convention: rounded-up eps1 in the error pairing
    selfC = I(Decimal(N2.numerator)) / I(Decimal(N2.denominator)) * 274
    J2lo_conv_EG = (I(E_lo_conv) - free - G_conv * V).lo
    ivd = lambda x: dict(lo=str(x.lo), hi=str(x.hi))
    out = {}
    for label, Gx, J2x, gradx in (('as certified (inherited G, E, ||Delta qN||)', G_in, J2lo, grad_in),
                                  ('own E, G from fractions', G_mine, J2lo_own_EG, grad_in),
                                  ('validated-only gradient (no array read for ||Delta qN||)', G_in, J2lo, grad_val),
                                  ('committed rounding convention (eps1, epsW rounded up to 5 digits)', G_conv, J2lo_conv_EG, grad_conv)):
        GN = Gx * I(nonself)
        C = selfC + GN + gradx
        b2C = beta.sq() * C
        margin = (I(J2x) - b2C).lo
        out[label] = dict(C_upper=str(C.hi), beta2C_upper=str(b2C.hi), J2_lower=str(J2x), H_over_b2_lower=str(margin),
                          parts=dict(self_274_intN2=ivd(selfC), G_used=ivd(Gx), G_times_nonself=ivd(GN), gradient=ivd(gradx), C=ivd(C), beta2_C=ivd(b2C)))
        say(f'   [{label}]')
        say(f'      self {selfC.hi:.30}  G*nonself {GN.hi:.30}  gradient {gradx.hi:.30}')
        say(f'      C <= {C.hi:.30}   beta^2 C <= {b2C.hi:.30}')
        say(f'      H/b^2 >= {margin:.30}   positive: {margin > 0}')
    say(f'   committed: C <= {cert["bounds"]["C_upper"]["hi"][:32]}, H/b^2 >= {cert["bounds"]["H_over_b2_lower"]["lo"][:32]}')
    conv = out['committed rounding convention (eps1, epsW rounded up to 5 digits)']
    d_conv = c.HI.subtract(Decimal(conv['H_over_b2_lower']), Decimal(cert['bounds']['H_over_b2_lower']['lo']))
    d_main = c.HI.subtract(Decimal(out['as certified (inherited G, E, ||Delta qN||)']['H_over_b2_lower']), Decimal(cert['bounds']['H_over_b2_lower']['lo']))
    d_grad = c.HI.subtract(grad_conv.hi, grad_in.hi)
    say(f'   reconciliation: H/b^2 (committed convention) - committed = {d_conv:.3E};  H/b^2 (full-precision eps1) - committed = {d_main:.6E}')
    say(f'   the latter equals beta^2 * (eps1 rounding) * Er(T) = 9e-6 * {d_grad:.6E}; E and G enter through the stored endpoint values in both')
    report['reconciliation'] = dict(H_conv_minus_committed=str(d_conv), H_fullprec_minus_committed=str(d_main),
                                    gradient_conv_minus_fullprec=str(d_grad), eps1_rounded=chain['eps1'], eps1_fullprec=str(e1[-1].hi),
                                    epsW_rounded=chain['epsW'], epsW_fullprec=str(epsW_T.hi))
    say(f'   gradient: inherited ||Delta qN(T)|| {qL_in.hi:.20} -> {grad_in.hi:.20} (committed {sg["bounds"]["gradient_new"]["hi"][:22]});'
        f' validated-only {qL_val.hi:.20} -> {grad_val.hi:.20}')

    # -------------------------------------------------------------- 8. sensitivity of the margin to inherited inputs (directed)
    # Hypothetical one-at-a-time sensitivity: how far one input would have to rise, every other input held fixed, before the
    # final comparison stops being positive. NOT an error allowance: each enclosure must still be a valid upper bound.
    say('== 8. hypothetical sensitivity, one input at a time with all others fixed (not an error allowance;'
        ' the rigorous claim needs every enclosure to be a valid bound)')
    C0 = selfC + G_in * I(nonself) + grad_in
    marg = I(J2lo) - beta.sq() * C0
    tol = {
        'source hull U_i (relative increase)': marg / (G_in * Vs),
        'G (relative increase)': marg / (G_in * (V + beta.sq() * I(nonself))),
        'E lower end (absolute decrease)': marg,
        '||Delta qN(T)|| (absolute increase)': marg / (beta.sq() * Nr[-1]),
        'all N_w (relative increase of int N^2)': marg / (beta.sq() * selfC),
        'nonself (relative increase)': marg / (beta.sq() * G_in * I(nonself)),
        'strain constant 274 (absolute increase)': marg / (beta.sq() * I(Decimal(N2.numerator)) / I(Decimal(N2.denominator))),
    }
    for k, v in tol.items():
        say(f'   {k:40s} comparison stays positive for an adverse change up to {v.lo:.6E}')
    report['sensitivity_one_at_a_time_lower'] = {k: str(v.lo) for k, v in tol.items()}
    # unrounded (full 40-digit directed) intermediates, scalar and per cell
    report['intermediates'] = dict(
        E_stored=dict(lo=E_in['lo'], hi=E_in['hi']), E_own_fullprec=dict(lo=str(E_lo_mine), hi=str(E_hi_mine)),
        E_own_conv=dict(lo=str(E_lo_conv), hi=str(E_hi_conv)), G_stored=str(G_in.hi), G_own_fullprec=ivd(G_mine), G_own_conv=ivd(G_conv),
        free=ivd(free), V_source=ivd(Vs), V_smooth_error=ivd(Vm), V_dissipation_error=ivd(Ve), V=ivd(V),
        J2_lower_stored_EG=str(J2lo), J2_lower_own_fullprec_EG=str(J2lo_own_EG), J2_lower_own_conv_EG=str(J2lo_conv_EG),
        Ahat=ivd(Ahat), Dw_T=ivd(Dw[-1]), Iinf_T=ivd(ii[-1]), Nr_T=ivd(Nr[-1]), Er_T=ivd(Er[-1]), Jr_T=ivd(Jr[-1]), Dr_T=ivd(Dr[-1]),
        direct_smooth=ivd(smooth), direct_error_advection=ivd(adv), derivative_error_cs=ivd(grad_cs), derivative_error_abel=ivd(grad_ab),
        direct=ivd(direct), cross_smooth=ivd(cross_s), cross_error=ivd(cross_e), cross=ivd(cross), nonself_selected=str(nonself),
        qN_laplacian_inherited=str(qL_in.hi), qN_laplacian_validated_only=ivd(qL_val), int_N2_exact=str(N2), self_274_intN2=ivd(selfC),
        eps1_T_fullprec=str(e1[-1].hi), eps1_T_rounded=chain['eps1'], epsW_T_fullprec=str(epsW_T.hi), epsW_T_rounded=chain['epsW'],
        C_A=str(CA.hi), beta2=ivd(beta.sq()))
    report['percell'] = [dict(i=i, t=rows[i][0], mu=ivd(mu[i]), P=ivd(Pw[i]), U=str(U[i].hi), Dweight=ivd(Dweight[i]), Dw=ivd(Dw[i]),
                              Iinf=ivd(ii[i]), Nr=ivd(Nr[i]), Er=ivd(Er[i]), Jr=ivd(Jr[i]), Dr=ivd(Dr[i])) for i in range(n)]
    report.update(J2_lower=str(J2lo), J2_lower_own_EG=str(J2lo_own_EG), V_upper=str(V.hi), E_lower_own=str(E_lo_mine), G_upper_own=str(G_mine.hi),
                  Ahat_upper=str(Ahat.hi), Dw_T_upper=str(Dw[-1].hi), Iinf_T_upper=str(ii[-1].hi), Nr_T=str(Nr[-1].hi), Er_T=str(Er[-1].hi),
                  Dr_T=str(Dr[-1].hi), direct=str(direct.hi), cross=str(cross.hi), nonself=str(nonself), percell_within_1e30=pc_ok,
                  gradient_inherited=str(grad_in.hi), gradient_validated_only=str(grad_val.hi), comparisons=out)

report['wall_seconds'] = time.monotonic() - t0
report['checker_sha256'] = sha(Path(__file__).resolve())
with OUT.open('x') as f:
    json.dump(report, f, indent=1); f.write('\n')
say(f'wall {report["wall_seconds"]:.1f} s; wrote {OUT}')
