"""Independent implementation of endpoint-sign PLAN.md A-F (and DERIVATION.md variant B for J2), written from the
plan's formulas, not from tr_remainder.py. Interval engine: the parent's 40-digit decimal Iv class (constants.py),
not mpmath. Reads only committed result files of cedb77cc. Writes only tr_series_lambda1e6.json, exclusive create, into the given output directory.
Usage: python3 -B independent_tr.py <finite-time dir> <fresh output dir>"""
import sys, json, hashlib, importlib.util, time
from decimal import Decimal, localcontext
from pathlib import Path

FT = Path(sys.argv[1]); t0 = time.monotonic()
assert hashlib.sha256((FT / 'constants.py').read_bytes()).hexdigest().startswith('996f39f171601a73')
spec = importlib.util.spec_from_file_location('c', FT / 'constants.py'); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
I = c.Iv
J = lambda p: json.loads((FT / p).read_text())
chain, val, rb, trf, ep, hull = (J('absorption-b003/results/chain.json'), J('absorption-b003/results/validated.json'),
    J('route-b-dissipation/results/bounds.review.json'), J('route-b-tightening/results/time_refinement.final.json'),
    J('z2-endpoint/results/endpoint.json'), J('source-only-hull/results/full.json'))
cpc = J('endpoint-sign/results/chain_percell.json'); tro = J('endpoint-sign/results/tr_remainder.json')
up = lambda x: x.hi
P = lambda d: I(Decimal(d))                      # exact decimal string or float -> point interval
with localcontext(c.TRAP):
    n = 250; D = I.of('1/1000'); nu = I.of('1/28'); T = I.of('1/4'); beta = I.of('3/1000')
    rows = cpc['log']; assert len(rows) == n and cpc['b'] == '0.003'
    colv = lambda k: [P(r[k]) for r in rows]
    m1, m2, e0, e1, dl, sg, N, K = colv(1), colv(2), colv(4), colv(5), colv(6), colv(8), colv(9), colv(10)
    cell = lambda k: [P(Decimal(x)) for x in val['cells'][k]]
    p, n1, n2 = cell('sup_absq'), cell('sup_absgradq'), cell('sup_abshessq')
    C, S = P(chain['C_A']), P(chain['S1'])
    G = P(ep['bounds']['base_true_laplacian_upper']['hi'])
    # ---- J2 lower end (DERIVATION.md section 1-2, variant B), own transcription
    m1s = [((-2 * nu * D * j).exp() + 4 + (1 + 2 * (1 - (-nu * D * (j + 1)).exp()) / nu).sq()).sqrt() for j in range(n)]
    for j in range(n): assert m1s[j].hi <= (m1[j] * I(Decimal('1.000000000000000000000000000001'))).hi and m1[j].lo > nu.hi
    U = [P(r['source_norm_upper_exact']) for r in hull['rows']]
    assert [r['coarse_cell'] for r in hull['rows']] == list(range(n))
    pmax, n1max = P(Decimal(max(val['cells']['sup_absq']))), P(Decimal(max(val['cells']['sup_absgradq'])))
    eps0, eps1, delta = P(chain['eps0']), P(chain['eps1']), P(chain['delta2'])
    dF = T * (n1max * eps0 + pmax * eps1) + C * eps1 * (T * delta).sqrt()
    tail = [I.of(0)] * (n + 1)
    for j in range(n - 1, -1, -1): tail[j] = tail[j + 1] + (m1s[j] - nu) * D
    VT = sum((tail[l].exp() * D * U[l] for l in range(n)), I.of(0)) + tail[0].exp() * dF
    Eq = ep['bounds']['half_q1_gradient_squared']
    J2lo = (P(Eq['lo']) - (-2 * nu * T).exp() / 4 - G * VT).lo
    # ---- Lemma B cap with the global constants (route-b-tightening section 3)
    g = {k: P(v['hi']) for k, v in rb['bounds'].items()}
    a_g = 2 * g['M1'] + 2 * beta * g['n1']; q = 2 * beta.sq() * C.sq() / nu
    f0 = (g['M2'] + beta * g['n2']) * g['Nw'] * g['K'] + 4 * g['sigma'].sq() / nu; fd = 4 * C.sq() * g['eps1'].sq() / nu
    def gcap(t):
        z = (2 * a_g * t).exp()
        return (2 * q * g['delta_e']).exp() * (f0 / a_g * (z - 1) + 2 * fd * g['delta_e'] * z)
    # ---- A. cumulative retained dissipation from 0: D_w,j >= int_0^{t_{j+1}} ||Delta w||^2 / b^4
    Dw, acc = [], I.of(0)
    for i in range(n):
        Y = I(min(K[i].sq().hi, gcap(D * (i + 1)).hi))
        acc = acc + ((2 * m1[i] + 2 * beta * n1[i]) * Y + (m2[i] + beta * n2[i]) * N[i] * Y.sqrt() + 4 * sg[i].sq() / nu) * D
        Dw.append(8 / nu * (acc + (q * K[i].sq() + 4 * C.sq() * e1[i].sq() / nu) * dl[i]))
    # ---- weights: exp of cumulative sums, split as exp(Cm[j+1]) * exp(-Cm[i]) (an enclosure of exp(sum_{k=i..j}))
    Cm, Cq = [I.of(0)], [I.of(0)]
    for i in range(n): Cm.append(Cm[-1] + (m1[i] - nu) * D); Cq.append(Cq[-1] + (4 * m1[i] + 1) * D)
    eM, eMi = [x.exp() for x in Cm], [(-x).exp() for x in Cm]
    eQ, eQi = [x.exp() for x in Cq], [(-x).exp() for x in Cq]
    Ew = lambda i, j: eM[j + 1] * eMi[i]
    Qw = lambda i, j: eQ[j + 1] * eQi[i]
    Pw = lambda i: eM[n] * eMi[i]
    # lattice constant (route-b-tightening (B)), own histogram
    from collections import Counter
    R = 32
    sq = [x * x for x in range(-R, R + 1)]
    hist = Counter(a + b + cc for a in sq for b in sq for cc in sq); del hist[0]
    assert sum(hist.values()) == 65 ** 3 - 1
    def Ahat(lam):
        return C.sq() - sum((I.of(cnt) * lam / (I.of(m * m) * (lam + I.of(m * m))) for m, cnt in hist.items()), I.of(0))
    def majorant(w):                     # smallest nonincreasing majorant of a list of Decimals
        out = list(w)
        for i in range(len(out) - 2, -1, -1): out[i] = max(out[i], out[i + 1])
        return out
    def abel(phi, B):                    # upper bound of sum phi_i X_i given sum_{k<=i} X_k <= B_i, phi nonincreasing >= 0
        tot = I(phi[-1]) * B[len(phi) - 1]
        for i in range(len(phi) - 1): tot = tot + (I(phi[i]) - I(phi[i + 1])) * B[i]
        return tot
    def chainCF(K_, N_, e1_, dl_, p_, n1_, m2_, Ew_, Qw_, Pw_, Iinf, tend, Dr, keep_j=False, reuse=False):
        A = [p_[i] * K_[i] + n1_[i] * N_[i] for i in range(n)]
        h = [e1_[i] + beta * K_[i] for i in range(n)]
        Nr, Er = [], []
        for j in range(n):
            s1 = sum((Ew_(i, j) * A[i] for i in range(j + 1)), I.of(0)) * D
            s2 = C * Ew_(0, j) * K_[j] * (tend(j) * dl_[j]).sqrt()
            s3 = (sum((Ew_(i, j).sq() * h[i].sq() for i in range(j + 1)), I.of(0)) * D).sqrt() * Iinf[j].sqrt()
            Nr.append(s1 + s2 + s3)
        if reuse: Nr = [Nr[-1]] * n
        for j in range(n):
            t1 = sum((Qw_(i, j) * m2_[i].sq() * Nr[i].sq() for i in range(j + 1)), I.of(0)) * D
            u1 = (sum((Qw_(i, j) * A[i].sq() for i in range(j + 1)), I.of(0)) * D).sqrt()
            u2 = (Qw_(0, j) * C.sq() * K_[j].sq() * dl_[j]).sqrt()
            u3 = abel(majorant([(Qw_(i, j) * h[i].sq()).hi for i in range(j + 1)]), Iinf).sqrt()
            Er.append((t1 + (u1 + u2 + u3).sq() / nu).sqrt())
        if reuse: Er = [Er[-1]] * n
        a = sum((Pw_(i) * (p_[i] * Er[i] + n1_[i] * Nr[i]) for i in range(n)), I.of(0)) * D
        b = C * I(max((Pw_(i) * Er[i]).hi for i in range(n))) * (T * dl_[-1]).sqrt()
        cc = C * I(max((Pw_(i) * e1_[i]).hi for i in range(n))) * (T * Dr).sqrt()
        d1 = (sum((Pw_(i).sq() * K_[i].sq() for i in range(n)), I.of(0)) * D).sqrt() * Iinf[-1].sqrt()
        d2 = (sum((Pw_(i) * K_[i].sq() for i in range(n)), I.of(0)) * D).sqrt() * abel(majorant([Pw_(i).hi for i in range(n)]), Iinf).sqrt()
        Nbar = a + b + cc + I(min(d1.hi, d2.hi))
        return dict(Nr=Nr if keep_j else Nr[-1], Er=Er if keep_j else Er[-1], Nbar=Nbar, d1=d1, d2=d2)
    out = {}
    for lam_s in ('100', '10000', '100000', '1000000', '10000000'):
        lam = I.of(lam_s); Ah = Ahat(lam); row = trf['rows'][lam_s]; Dr = P(row['Dr']['hi'])
        # global collapse with my code: must reproduce route-b-tightening's reviewed N_r, E_r, N_bar
        Eg = ((g['M1'] - nu) * T).exp(); Qg = ((4 * g['M1'] + 1) * T).exp()
        Ig = Ah * (lam * T * g['Nw'].sq() + P(trf['Dw']['hi']))
        glob = tuple([v] * n for v in (g['K'], g['Nw'], g['eps1'], g['delta_e'], g['p'], g['n1'], g['M2']))
        # terminal reuse: the global lemma uses sup bounds; emulate by evaluating at T with constant inputs
        gl = chainCF(*glob, lambda i, j: Eg, lambda i, j: Qg, lambda i: Eg, [Ig] * n, lambda j: T, Dr, reuse=True)
        # (with constant weights and inputs the per-j N_r, E_r grow with j; N_bar here uses the per-j values,
        #  so it is <= the terminal-reuse value; compare N_r(T), E_r(T) exactly and N_bar only as an upper check)
        cumN, s = [], I.of(0)
        for i in range(n): s = s + N[i].sq() * D; cumN.append(s)
        Iinf = [Ah * (lam * cumN[j] + Dw[j]) for j in range(n)]
        tr = chainCF(K, N, e1, dl, p, n1, m2, Ew, Qw, Pw, Iinf, lambda j: D * (j + 1), Dr, keep_j=(lam_s == '1000000'))
        Er_T = tr['Er'][-1] if isinstance(tr['Er'], list) else tr['Er']
        Cone = G * tr['Nbar'] + S * Er_T
        out[lam_s] = dict(tr=tr, Cone=Cone, gl=gl, row=row, Er_T=Er_T)
    best = min(out, key=lambda k: out[k]['Cone'].hi)
    rhs = (beta.sq() * out[best]['Cone']).hi
    print(f'independent J2_lo = {float(J2lo):.13f}   (committed {tro["J2_lo"][:15]})')
    
    def cv(x):
        x = str(x).strip()
        if x.startswith('['): x = x[1:-1].split(',')[1]
        return Decimal(x.strip())
    rel = lambda a, b: abs(float(cv(a)) / float(cv(b)) - 1)
    for k, v in out.items():
        r = v['row']; tr = v['tr']; c_ = tro['per_lambda'][k]
        Nr_T = tr['Nr'][-1] if isinstance(tr['Nr'], list) else tr['Nr']
        print(f'lambda {k:>8s}: global collapse N_r(T) rel.diff {rel(v["gl"]["Nr"].hi, r["Nr"]["hi"]):.1e}, E_r(T) {rel(v["gl"]["Er"].hi, r["Er"]["hi"]):.1e}'
              f' Nbar {rel(v["gl"]["Nbar"].hi, r["Nbar"]["hi"]):.1e} | TR: N_r {float(Nr_T.hi):.6f} vs {float(cv(c_["Nr_T"])):.6f}, E_r {float(v["Er_T"].hi):.6f} vs {float(cv(c_["Er_T"])):.6f},'
              f' Nbar {float(tr["Nbar"].hi):.6f} vs {float(cv(c_["Nbar"])):.6f}, C_one {float(v["Cone"].hi):.6f} vs {float(cv(c_["C_one"])):.6f}')
    print(f'independent D_w,TR(T) <= {float(Dw[-1].hi):.9f}   (committed {float(cv(tro["Dw_TR_T"])):.9f}; global {float(trf["Dw"]["hi"]):.6f})')
    Cb = out[best]['Cone']
    rhs_iv = beta.sq() * I(Cb.hi)
    Hlo = (I(J2lo) - I(rhs_iv.hi)).lo                       # lower bound of H_b/b^2 at |b| = beta
    bstar = (I(J2lo) / I(Cb.hi)).sqrt().lo                  # lower endpoint: positive sign for 0 < |b| < bstar
    rd = lambda x, k: c.round_down(x, k); ru = lambda x, k: c.round_up(x, k)
    print(f'best lambda {best}: C_one,TR <= {ru(Cb.hi, 14)}')
    print(f'(D): J2_lo >= {rd(J2lo, 14)}  vs  beta^2 C_one,TR <= {ru(rhs_iv.hi, 14)}  ->  {"HOLDS" if J2lo > rhs_iv.hi else "FAILS"}')
    print(f'lower bound of H_b/b^2 at |b| = 0.003: >= {rd(Hlo, 14)}')
    print(f'smaller-amplitude conclusion: J2_lo > 0: {J2lo > 0}; b* >= {rd(bstar, 14)} < beta: {bstar < beta.lo}; '
          f'committed b*_lower = {cv(tro["b_star_lower"]) if tro["b_star_lower"] else None}')
    # 3. a deliberately wrong weight (source cell excluded) passes both of the script's checks
    Ew_bad = lambda i, j: eM[j + 1] * eMi[i + 1]
    lam = I.of('1000000'); Ah = Ahat(lam); Dr = P(trf['rows']['1000000']['Dr']['hi'])
    cumN, s_ = [], I.of(0)
    for i in range(n): s_ = s_ + N[i].sq() * D; cumN.append(s_)
    Iinf = [Ah * (lam * cumN[j] + Dw[j]) for j in range(n)]
    bad = chainCF(K, N, e1, dl, p, n1, m2, Ew_bad, Qw, Pw, Iinf, lambda j: D * (j + 1), Dr)
    gl6 = out['1000000']['gl']
    print(f'wrong-weight variant: N_r(T) {float(bad["Nr"].hi):.6f} (correct {float(out["1000000"]["tr"]["Nr"][-1].hi):.6f}); '
          f'collapse with constant weights is unaffected by the index shift; monotonicity TR <= global still passes: '
          f'{bad["Nr"].hi <= gl6["Nr"].hi and bad["Nbar"].hi <= gl6["Nbar"].hi}')
    tr6 = out['1000000']['tr']
    json.dump(dict(t=[float((D * (j + 1)).hi) for j in range(n)], Er=[float(x.hi) for x in tr6['Er']], Nr=[float(x.hi) for x in tr6['Nr']],
                   K=[float(x.hi) for x in K], Dw=[float(x.hi) for x in Dw]),
              open(Path(sys.argv[2]) / 'tr_series_lambda1e6.json', 'x'))
    print(f'wall {time.monotonic() - t0:.1f} s')
