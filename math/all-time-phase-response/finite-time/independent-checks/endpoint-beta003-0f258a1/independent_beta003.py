"""Independent end-to-end reproduction of endpoint-beta003 (codex/endpoint-beta003-tightening at 0f258a1).

Written from endpoint-beta003/NOTE.md and PLAN.md and from endpoint-sign PLAN.md A-F, not from check.py or
tr_remainder.py. Interval engine: the parent's 40-digit decimal Iv class (finite-time/constants.py, directed
rounding), not mpmath. Unlike check.py, nothing is read from the parent's stored totals: J2_lo, D_w,j, I_inf,j,
N_r,j, E_r,j, the three nonself parts, d1, d2 and the new d_div are all recomputed here from the primitive
certified inputs (per-cell chain rows, validated cell sups, global Route B constants, the source hull, the
endpoint enclosure, the global D_r of route-b-tightening), then compared with results/candidate.json.

Usage: python3 -B independent_beta003.py <finite-time dir of a 0f258a1 checkout> <fresh output dir>"""
import sys, json, hashlib, importlib.util, time
from decimal import Decimal, localcontext
from pathlib import Path
from collections import Counter

FT, OUT = Path(sys.argv[1]), Path(sys.argv[2]); t0 = time.monotonic()
PINS = {  # every input read here, with the hash it must have
    'constants.py': '996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014',
    'absorption-b003/results/chain.json': '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
    'absorption-b003/results/validated.json': 'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b',
    'endpoint-sign/results/chain_percell.json': '795e3a7b5c83bee29308392fd33232864e9df41e121646cbcd9b1fca395d58bc',
    'route-b-dissipation/results/bounds.review.json': '4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
    'route-b-tightening/results/time_refinement.final.json': '79612f1164e92243b74ef40dd668651bc850ffa81d82695d7c59f039e119e849',
    'z2-endpoint/results/endpoint.json': '37368b9c6c7781e9cc691deb4742fd56e194c4ee80bed0b6a517e2425d8ab0bc',
    'source-only-hull/results/full.json': '0d2ab266fd226091a9116b83c54621ad480f2b8306f16e9dd830a705629cfa82',
    'endpoint-beta003/results/candidate.json': '3aa3c960357f6d3758d4899ae76a6ccfe1ceaa1ca122e25329395c480bd1c155',
}
for name, h in PINS.items():
    assert hashlib.sha256((FT / name).read_bytes()).hexdigest() == h, 'pinned input mismatch: ' + name
spec = importlib.util.spec_from_file_location('c', FT / 'constants.py'); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
I = c.Iv
J = lambda p: json.loads((FT / p).read_text())
chain, val, rb, trf, ep, hull = (J('absorption-b003/results/chain.json'), J('absorption-b003/results/validated.json'),
    J('route-b-dissipation/results/bounds.review.json'), J('route-b-tightening/results/time_refinement.final.json'),
    J('z2-endpoint/results/endpoint.json'), J('source-only-hull/results/full.json'))
cpc, cand = J('endpoint-sign/results/chain_percell.json'), J('endpoint-beta003/results/candidate.json')
P = lambda d: I(Decimal(d))
with localcontext(c.TRAP):
    n = 250; D = I.of('1/1000'); nu = I.of('1/28'); T = I.of('1/4'); beta = I.of('3/1000'); lam = I.of('1000000')
    assert chain['b'] == '0.003' and chain['T'] == 0.25 and chain['phi'] == 0.37 and cpc['b'] == '0.003'
    assert ep['scope'] == 'a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000'
    rows = cpc['log']; assert len(rows) == n and [Decimal(r[0]) for r in rows] == [Decimal(f'{i + 1}e-3') for i in range(n)]
    colv = lambda k: [P(r[k]) for r in rows]
    m1, m2, e1, dl, sg, N, K = colv(1), colv(2), colv(5), colv(6), colv(8), colv(9), colv(10)
    cell = lambda k: [P(Decimal(x)) for x in val['cells'][k]]
    p, n1, n2 = cell('sup_absq'), cell('sup_absgradq'), cell('sup_abshessq')
    C, S = P(chain['C_A']), P(chain['S1'])
    G = P(ep['bounds']['base_true_laplacian_upper']['hi']); assert G.hi <= Decimal('1.8534')
    # ---- J2 lower end (endpoint-sign DERIVATION.md variant B)
    m1s = [((-2 * nu * D * j).exp() + 4 + (1 + 2 * (1 - (-nu * D * (j + 1)).exp()) / nu).sq()).sqrt() for j in range(n)]
    for j in range(n): assert m1s[j].hi <= (m1[j] * I(Decimal('1.000000000000000000000000000001'))).hi and m1[j].lo > nu.hi
    U = [P(r['source_norm_upper_exact']) for r in hull['rows']]; assert [r['coarse_cell'] for r in hull['rows']] == list(range(n))
    pmax, n1max = P(Decimal(max(val['cells']['sup_absq']))), P(Decimal(max(val['cells']['sup_absgradq'])))
    eps0, eps1, delta = P(chain['eps0']), P(chain['eps1']), P(chain['delta2'])
    dF = T * (n1max * eps0 + pmax * eps1) + C * eps1 * (T * delta).sqrt()
    tail = [I.of(0)] * (n + 1)
    for j in range(n - 1, -1, -1): tail[j] = tail[j + 1] + (m1s[j] - nu) * D
    VT = sum((tail[l].exp() * D * U[l] for l in range(n)), I.of(0)) + tail[0].exp() * dF
    J2lo = (P(ep['bounds']['half_q1_gradient_squared']['lo']) - (-2 * nu * T).exp() / 4 - G * VT).lo
    # ---- A, B: cumulative D_w,j and I_inf,j from zero (Lemma B cap with the global Route B constants)
    g = {k: P(v['hi']) for k, v in rb['bounds'].items()}
    a_g = 2 * g['M1'] + 2 * beta * g['n1']; q = 2 * beta.sq() * C.sq() / nu
    f0 = (g['M2'] + beta * g['n2']) * g['Nw'] * g['K'] + 4 * g['sigma'].sq() / nu; fd = 4 * C.sq() * g['eps1'].sq() / nu
    gcap = lambda t: (2 * q * g['delta_e']).exp() * (f0 / a_g * ((2 * a_g * t).exp() - 1) + 2 * fd * g['delta_e'] * (2 * a_g * t).exp())
    Dw, acc = [], I.of(0)
    for i in range(n):
        Y = I(min(K[i].sq().hi, gcap(D * (i + 1)).hi))
        acc = acc + ((2 * m1[i] + 2 * beta * n1[i]) * Y + (m2[i] + beta * n2[i]) * N[i] * Y.sqrt() + 4 * sg[i].sq() / nu) * D
        Dw.append(8 / nu * (acc + (q * K[i].sq() + 4 * C.sq() * e1[i].sq() / nu) * dl[i]))
    R = 32; sq = [x * x for x in range(-R, R + 1)]
    hist = Counter(a + b + cc for a in sq for b in sq for cc in sq); del hist[0]; assert sum(hist.values()) == 65 ** 3 - 1
    Ah = C.sq() - sum((I.of(cnt) * lam / (I.of(m * m) * (lam + I.of(m * m))) for m, cnt in hist.items()), I.of(0))
    cumN, s_ = [], I.of(0)
    for i in range(n): s_ = s_ + N[i].sq() * D; cumN.append(s_)
    Iinf = [Ah * (lam * cumN[j] + Dw[j]) for j in range(n)]
    # ---- C, D: time-resolved N_r,j, E_r,j (inclusive cell weights, exp of cumulative sums split as a product)
    Cm, Cq = [I.of(0)], [I.of(0)]
    for i in range(n): Cm.append(Cm[-1] + (m1[i] - nu) * D); Cq.append(Cq[-1] + (4 * m1[i] + 1) * D)
    eM, eMi = [x.exp() for x in Cm], [(-x).exp() for x in Cm]
    eQ, eQi = [x.exp() for x in Cq], [(-x).exp() for x in Cq]
    Ew = lambda i, j: eM[j + 1] * eMi[i]; Qw = lambda i, j: eQ[j + 1] * eQi[i]; Pw = lambda i: eM[n] * eMi[i]
    def majorant(w):
        out = list(w)
        for i in range(len(out) - 2, -1, -1): out[i] = max(out[i], out[i + 1])
        return out
    def abel(phi, B):
        assert all(phi[i] >= phi[i + 1] for i in range(len(phi) - 1)) and phi[-1] >= 0
        tot = I(phi[-1]) * B[len(phi) - 1]
        for i in range(len(phi) - 1): tot = tot + (I(phi[i]) - I(phi[i + 1])) * B[i]
        return tot
    A = [p[i] * K[i] + n1[i] * N[i] for i in range(n)]; h = [e1[i] + beta * K[i] for i in range(n)]
    Nr, Er = [], []
    for j in range(n):
        s1 = sum((Ew(i, j) * A[i] for i in range(j + 1)), I.of(0)) * D
        s2 = C * Ew(0, j) * K[j] * (D * (j + 1) * dl[j]).sqrt()
        s3 = (sum((Ew(i, j).sq() * h[i].sq() for i in range(j + 1)), I.of(0)) * D).sqrt() * Iinf[j].sqrt()
        Nr.append(s1 + s2 + s3)
    for j in range(n):
        t1 = sum((Qw(i, j) * m2[i].sq() * Nr[i].sq() for i in range(j + 1)), I.of(0)) * D
        u1 = (sum((Qw(i, j) * A[i].sq() for i in range(j + 1)), I.of(0)) * D).sqrt()
        u2 = (Qw(0, j) * C.sq() * K[j].sq() * dl[j]).sqrt()
        u3 = abel(majorant([(Qw(i, j) * h[i].sq()).hi for i in range(j + 1)]), Iinf).sqrt()
        Er.append((t1 + (u1 + u2 + u3).sq() / nu).sqrt())
    # ---- E: nonself parts of the mean forcing (actual r, bounded above), and the old self bounds
    Dr = P(trf['rows']['1000000']['Dr']['hi'])
    smooth = sum((Pw(i) * (p[i] * Er[i] + n1[i] * Nr[i]) for i in range(n)), I.of(0)) * D
    err_adv = C * I(max((Pw(i) * Er[i]).hi for i in range(n))) * (T * dl[-1]).sqrt()
    err_grad = C * I(max((Pw(i) * e1[i]).hi for i in range(n))) * (T * Dr).sqrt()
    d1 = (sum((Pw(i).sq() * K[i].sq() for i in range(n)), I.of(0)) * D).sqrt() * Iinf[-1].sqrt()
    d2 = (sum((Pw(i) * K[i].sq() for i in range(n)), I.of(0)) * D).sqrt() * abel(majorant([Pw(i).hi for i in range(n)]), Iinf).sqrt()
    # ---- new: divergence-form self response, ||X(T)||^2 <= (1/(2nu)) int exp(2 int_s^T m1) ||W||^2 ||W||_inf^2 ds
    sfx = [I.of(0)] * (n + 1)
    for i in range(n - 1, -1, -1): sfx[i] = sfx[i + 1] + 2 * m1[i] * D          # inclusive: cells i..n-1
    f = [(sfx[i].exp() * N[i].sq()).hi for i in range(n)]
    f_monotone = all(f[i] >= f[i + 1] for i in range(n - 1))
    weighted = abel(majorant(f), Iinf)
    ddiv = (weighted / (2 * nu)).sqrt()
    nonself = smooth + err_adv + err_grad
    selfb = I(min(d1.hi, d2.hi, ddiv.hi))
    Cnew = G * (nonself + selfb) + S * Er[-1]
    Cold = G * (nonself + I(min(d1.hi, d2.hi))) + S * Er[-1]
    margin_lo = (I(J2lo) - beta.sq() * I(Cnew.hi)).lo
    passes = margin_lo > 0
    rd = lambda x: c.round_down(x, 16); ru = lambda x: c.round_up(x, 16)
    def cv(s):
        s = str(s).strip()
        return Decimal(s[1:-1].split(',')[1].strip()) if s.startswith('[') else Decimal(s)
    lines = [
        f'independent reproduction of endpoint-beta003 at 0f258a1 (decimal intervals, 40 digits, directed rounding)',
        f'J2 lower end                     >= {rd(J2lo)}   (candidate {cand["inherited_J2_lower"]["lo"][:18]})',
        f'D_w,TR(T)                        <= {ru(Dw[-1].hi)}   (candidate {cand["Dw_T"]["hi"][:18]})',
        f'I_inf(T)                         <= {ru(Iinf[-1].hi)}   (candidate {cand["Iinf_T"]["hi"][:18]})',
        f'E_r(T)                           <= {ru(Er[-1].hi)}',
        f'nonself = smooth + err_adv + err_grad <= {ru(nonself.hi)}   (candidate {cand["nonself_sum"]["hi"][:18]})',
        f'   smooth {ru(smooth.hi)}, err_adv {ru(err_adv.hi)}, err_grad {ru(err_grad.hi)}',
        f'old self bounds d1 <= {ru(d1.hi)}, d2 <= {ru(d2.hi)}   (candidate old {cand["old_self_bound"]["hi"][:18]})',
        f'weighted I_inf (Abel, suffix majorant) <= {ru(weighted.hi)}   (candidate {cand["weighted_Iinf_bound"]["hi"][:18]}); weights already monotone: {f_monotone}',
        f'new self bound d_div             <= {ru(ddiv.hi)}   (candidate {cand["self_divergence_bound"]["hi"][:18]})',
        f'old C (recomputed)               <= {ru(Cold.hi)}   (candidate old {cand["old_C_upper"]["hi"][:18]})',
        f'new C                            <= {ru(Cnew.hi)}   (candidate {cand["new_C_upper"]["hi"][:18]})',
        f'beta^2 C_new                     <= {ru((beta.sq() * I(Cnew.hi)).hi)}   (candidate {cand["beta2_C_upper"]["hi"][:18]})',
        f'H_b(1/4)/b^2 lower bound at |b| = 0.003 (hence on 0 < |b| <= 0.003): >= {rd(margin_lo)}   (candidate {cand["H_over_b2_lower_at_beta"]["lo"][:18]})',
        f'claimed 0.004804904671503 is below the recomputed lower bound: {Decimal("0.004804904671503") <= margin_lo}',
        f'target comparison J2_lo - beta^2 C_new > 0: {passes}',
        f'relative differences from the candidate (upper endpoints): ' + ', '.join(
            f'{k} {abs(float(cv(cand[kk]["hi"])) / float(v.hi) - 1):.1e}' for k, kk, v in
            (('nonself', 'nonself_sum', nonself), ('d_div', 'self_divergence_bound', ddiv), ('C_new', 'new_C_upper', Cnew))),
        f'wall {time.monotonic() - t0:.1f} s',
    ]
print('\n'.join(lines))
with (OUT / 'independent_beta003.log').open('x') as fh: fh.write('\n'.join(lines) + '\n')
