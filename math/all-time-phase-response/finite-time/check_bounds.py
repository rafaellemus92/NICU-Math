"""check_bounds.py -- measure the quantities that NOTE.md bounds and compare them with the bounds.

Family u0 = (a sin y, b sin z, c cos x - d cos(x+y+phi)), a=c=d=1, nu=1/28, phi=0.37.
For b in {1e-3, 1e-2, 0.05}: full nonlinear solves u_b with the repository solver
(../../ns-phase-audit/audit_v2/dns/ns.py, N=24, K=7, RK4 dt=0.005) and the b-Taylor hierarchy
Y=[U, q1, q2] (../response.py; q2 = b^2 coefficient), both with the same RK4 map.
Measured: ||grad v||/|b|, ||grad vbar||/b^2, ||grad rtil||/b^2, ||grad e2til||/|b|^3, ||e2bar||/b^4,
R_Z/b^4, int ||Lap v||^2 / b^2, the exact six-term identity of NOTE.md section 5 (including the
vanishing cross term 2 b^3 <grad q1, grad q2tilde>), and the base-flow derivative sups against the
section 2 bounds; the sups come from a fine 1-D spectral solve (|n| <= 40 modes, RK4 dt = 1e-3, a
truncated solve, not a certified one) whose maxima over y are certified maxima of the resulting
trigonometric polynomials (Taylor + Bernstein bound).
Then the bounds of constants.py at T = 0.25, 0.5, 1 are printed next to the measurements
(bound/measured = the loss of that estimate), and the conditional scenario of NOTE.md section 7
(G1, D1 replaced by their measured values) is evaluated and labelled as not certified.

These are consistency checks (every bound must exceed its measurement), not certificates;
b = 1e-2 and 0.05 lie outside every certified radius, and b^4-scaled quantities at b = 1e-3 sit
at double-precision roundoff. No archived file is modified; results go to results/.

Run from this folder:  python3 -B check_bounds.py > results/check_bounds.log   (about 15 s)
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import platform
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESP_PATH = HERE.parent / 'response.py'
CONST_PATH = HERE / 'constants.py'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


response = load_module('response', RESP_PATH)   # response.py loads ns.py by path
audit = response.audit
constants = load_module('constants', CONST_PATH)

N, NU, PHI, A, C, D = 24, 1.0 / 28.0, 0.37, 1.0, 1.0, 1.0
DT, T, OUT_EVERY = 0.005, 1.0, 0.05
BS = [1e-3, 1e-2, 0.05]
K1, DT1, M1 = 40, 1e-3, 16384
NSTEPS = int(round(T / DT)); PER_OUT = int(round(OUT_EVERY / DT)); NOUT = NSTEPS // PER_OUT
TIMES = DT * PER_OUT * np.arange(NOUT + 1)
CHECK_T = [0.25, 0.5, 1.0]
tic = time.time()

ns = audit.NS(N, NU)
rs = response.Response(N, NU)
g = ns.g
W_, K2 = g.w, g.k2


def advance(solver, state, nsteps, dt, per_out):
    snaps = [state.copy()]
    for n in range(1, nsteps + 1):
        state = solver.step(state, dt)
        if n % per_out == 0:
            if not np.isfinite(state).all():
                raise FloatingPointError('nonfinite state')
            snaps.append(state.copy())
    return snaps


def nrm(f, p=0):
    return float(np.sqrt((W_ * K2 ** p * (np.abs(f) ** 2).sum(axis=0)).sum()))


def ip(f, h, p=0):
    return float((W_ * K2 ** p * (f.conj() * h).real.sum(axis=0)).sum())


def mean_part(f):
    m = np.zeros_like(f)
    m[..., 0] = f[..., 0]
    return m


maxabs = lambda f: float(np.abs(f).max()) if f.size else 0.0

# hierarchy
Y0 = rs.initial(PHI, A, C, D)
assert maxabs(Y0[0] - ns.init_family(PHI, A, 0.0, C, D)) < 1e-14
assert maxabs(Y0[1] - ns.init_family(0.0, 0.0, 1.0, 0.0, 0.0)) < 1e-14 and maxabs(Y0[2]) == 0.0
Ys = advance(rs, Y0, NSTEPS, DT, PER_OUT)
hier = {k: [] for k in ['grad_q1', 'lap_q1', 'grad_q2', 'grad_q2_tilde', 'grad_q2_bar', 'Z_U', 'Z2',
                        'q1_kz0_max', 'q2_offplane_max']}
for j in range(NOUT + 1):
    U, q1, q2 = Ys[j]
    q2bar = mean_part(q2)
    hier['grad_q1'].append(nrm(q1, 1)); hier['lap_q1'].append(nrm(q1, 2))
    hier['grad_q2'].append(nrm(q2, 1)); hier['grad_q2_tilde'].append(nrm(q2 - q2bar, 1)); hier['grad_q2_bar'].append(nrm(q2bar, 1))
    hier['Z_U'].append(g.enstrophy(U)); hier['Z2'].append(float(rs.second(Ys[j])[1]))
    hier['q1_kz0_max'].append(maxabs(q1[..., 0])); hier['q2_offplane_max'].append(maxabs(np.delete(q2, [0, 2], axis=-1)))
lapq1 = np.array(hier['lap_q1']) ** 2
hier['int_lap_q1_sq'] = np.concatenate([[0.0], np.cumsum(0.5 * (lapq1[1:] + lapq1[:-1]) * np.diff(TIMES))]).tolist()

# full solves
per_b = {}
for b in BS:
    us = advance(ns, ns.init_family(PHI, A, b, C, D), NSTEPS, DT, PER_OUT)
    s = {k: [] for k in ['norm_v', 'grad_v', 'lap_v', 'grad_vbar', 'grad_rtil', 'grad_e2til', 'norm_e2bar', 'R_Z',
                         'decomp_residual', 'six_term_residual', 'cross_term']}
    for j in range(NOUT + 1):
        U, q1, q2 = Ys[j]; ub = us[j]
        v = ub - U; vbar = mean_part(v); vtil = v - vbar
        q2bar = mean_part(q2); q2til = q2 - q2bar
        rtil = vtil - b * q1; e2til = rtil - b * b * q2til; e2bar = vbar - b * b * q2bar
        RZ = g.enstrophy(ub) - g.enstrophy(U) - b * b * hier['Z2'][j]
        s['norm_v'].append(nrm(v)); s['grad_v'].append(nrm(v, 1)); s['lap_v'].append(nrm(v, 2))
        s['grad_vbar'].append(nrm(vbar, 1)); s['grad_rtil'].append(nrm(rtil, 1))
        s['grad_e2til'].append(nrm(e2til, 1)); s['norm_e2bar'].append(nrm(e2bar))
        s['R_Z'].append(RZ)
        s['decomp_residual'].append(RZ - (ip(U, e2bar, 1) + 0.5 * (nrm(v, 1) ** 2 - b * b * nrm(q1, 1) ** 2)))
        # the six-term expansion of NOTE.md section 5 (cross term 2 b^3 <grad q1, grad q2til> omitted, must vanish)
        six = (ip(U, e2bar, 1) + 0.5 * nrm(vbar, 1) ** 2 + 0.5 * b ** 4 * nrm(q2til, 1) ** 2
               + b * b * ip(q2til, e2til, 1) + b * ip(q1, e2til, 1) + 0.5 * nrm(e2til, 1) ** 2)
        s['six_term_residual'].append(RZ - six)
        s['cross_term'].append(2 * b ** 3 * ip(q1, q2til, 1))
    lap2 = np.array(s['lap_v']) ** 2
    s['int_lap_v_sq'] = np.concatenate([[0.0], np.cumsum(0.5 * (lap2[1:] + lap2[:-1]) * np.diff(TIMES))]).tolist()
    s['b'] = b
    per_b[f'{b:g}'] = s
    del us

# base flow from the fine 1-D model, with certified maxima of the trigonometric polynomials
n1 = np.arange(-K1, K1 + 1)


def rhs1(tt, wv):
    sh = np.zeros_like(wv); sh[1:] += wv[:-1]; sh[:-1] -= wv[1:]
    return -(A * np.exp(-NU * tt) / 2) * sh - NU * (n1 ** 2 + 1) * wv


def sup_cert(coef, M, deg):
    """Certified max_y |p(y)|: |p(y)| <= |p(y_j)| + h|p'(y_j)| + (h^2/2)||p''||, h = pi/M, Bernstein ||p''|| <= deg^2 ||p||."""
    Cc = np.zeros(M, complex); Cc[n1 % M] = coef
    Cd = np.zeros(M, complex); Cd[n1 % M] = 1j * n1 * coef
    vals, dvals = np.fft.ifft(Cc) * M, np.fft.ifft(Cd) * M
    h = np.pi / M
    return float((np.abs(vals) + h * np.abs(dvals)).max() / (1.0 - h * h * deg * deg / 2.0))


w = np.zeros(2 * K1 + 1, complex); w[K1] = C; w[K1 + 1] = -D * np.exp(1j * PHI)
per1 = int(round(OUT_EVERY / DT1))
w_snaps = [w.copy()]
for step in range(1, per1 * NOUT + 1):
    tt = (step - 1) * DT1
    k1 = rhs1(tt, w); k2 = rhs1(tt + DT1 / 2, w + DT1 / 2 * k1)
    k3 = rhs1(tt + DT1 / 2, w + DT1 / 2 * k2); k4 = rhs1(tt + DT1, w + DT1 * k3)
    w = w + DT1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    if step % per1 == 0:
        w_snaps.append(w.copy())
base = {k: [] for k in ['sup_gradU', 'sup_hessU', 'lapU_L2']}
for j in range(NOUT + 1):
    wv = w_snaps[j]; sig = A * np.exp(-NU * TIMES[j])
    cW, cWy, cWyy = sup_cert(wv, M1, K1), sup_cert(1j * n1 * wv, M1, K1), sup_cert(-(n1 ** 2) * wv, M1, K1)
    base['sup_gradU'].append(float(np.sqrt(sig ** 2 + cW ** 2 + cWy ** 2)))
    base['sup_hessU'].append(float(np.sqrt(sig ** 2 + cW ** 2 + 2 * cWy ** 2 + cWyy ** 2)))
    base['lapU_L2'].append(float(np.sqrt(sig ** 2 / 2 + 0.5 * np.sum((1 + n1 ** 2) ** 2 * np.abs(wv) ** 2))))
wall = time.time() - tic

# bounds
CA = constants.read_certified_CA(HERE / 'results' / 'lattice_sums.log')
CA_src = 'results/lattice_sums.log'
if CA is None:
    CA = float(np.sqrt(constants.certified_lambda4()[2])); CA_src = 'built-in certified bound (R = 60)'
idx = {t: int(round(t / OUT_EVERY)) for t in CHECK_T}
L = []
P = L.append
P('check_bounds.py -- ' + time.strftime('%Y-%m-%d %H:%M:%S') + f'; python {platform.python_version()}, numpy {np.__version__}')
P(f'N={N} K={g.K} nu={NU:.6f} phi={PHI} a=c=d=1 dt={DT} T={T}; b in {BS}; C_A = {CA:.6f} ({CA_src}); wall {wall:.0f} s')
P(f'consistency: max|q1| on k_z=0 plane {max(hier["q1_kz0_max"]):.1e}; max|q2| off k_z in {{0,2}} {max(hier["q2_offplane_max"]):.1e}; '
  + '; '.join(f'b={k}: max|identity residual| {max(abs(x) for x in s["decomp_residual"]):.1e}, '
              f'six-term {max(abs(x) for x in s["six_term_residual"]):.1e}, cross term {max(abs(x) for x in s["cross_term"]):.1e}'
              for k, s in per_b.items()))
P('note: b = 1e-2 and 0.05 lie outside every certified radius beta1(T) and the absorption hypothesis C_A||grad v|| <= nu/2 fails along those'
  ' solves; Table B compares the bounds with the b -> 0 limits of the b^k-scaled quantities (smooth in b), not with certified cases.')
P('')
P('Table A: section 2 base-flow bounds against certified sups of the fine 1-D solve (bound / measured >= 1 required)')
P(f'{"t":>5} {"m1 bound":>10} {"sup|gradU|":>11} {"ratio":>7} {"m2 bound":>10} {"sup|hessU|":>11} {"ratio":>7} {"mDelta":>10} {"||LapU||":>10} {"ratio":>7}')
ok = True
rows = {}
for t in CHECK_T:
    r = constants.chain(A, C, D, NU, CA, t, 20000)
    rows[t] = r
    j = idx[t]
    vals = [(r['m1(T)'], base['sup_gradU'][j]), (r['m2(T)'], base['sup_hessU'][j]), (r['mDelta(T)'], base['lapU_L2'][j])]
    ok &= all(bd >= me for bd, me in vals)
    P(f'{t:5.2f} ' + ' '.join(f'{bd:10.4f} {me:11.4f} {bd / me:7.3f}' for bd, me in vals))
P('')
P('Table B: chain bounds against measurements (b = 1e-2 for b^2..b^4-scaled quantities; ratio = bound / measured = loss of the estimate)')
P(f'{"t":>5} {"quantity":>22} {"bound":>12} {"measured":>12} {"ratio":>10}')
s2 = per_b['0.01']
b2 = s2['b']
for t in CHECK_T:
    r = rows[t]; j = idx[t]
    items = [('G1 vs |grad v|/b', r['G1'], s2['grad_v'][j] / b2),
             ('D1 vs int|Lap v|^2/b^2', r['D1'], s2['int_lap_v_sq'][j] / b2 ** 2),
             ('Q2 vs |grad q2|', r['Q2'], hier['grad_q2'][j]),
             ('Vbar vs |grad vbar|/b^2', r['Vbar'], s2['grad_vbar'][j] / b2 ** 2),
             ('R1 vs |grad rtil|/b^2', r['R1'], s2['grad_rtil'][j] / b2 ** 2),
             ('Etilde vs |grad e2til|/b^3', r['Etilde'], s2['grad_e2til'][j] / abs(b2) ** 3),
             ('Ebar vs |e2bar|/b^4', r['Ebar'], s2['norm_e2bar'][j] / b2 ** 4),
             ('C_Z vs |R_Z|/b^4', r['C_Z'], abs(s2['R_Z'][j]) / b2 ** 4)]
    for name, bd, me in items:
        ok &= bd >= me
        P(f'{t:5.2f} {name:>22} {bd:12.4e} {me:12.4e} {bd / me if me > 0 else float("inf"):10.3e}')
P('')
s3 = per_b['0.001']
P(f'bootstrap hypothesis C_A ||grad v|| <= nu/2 = {NU / 2:.4e} along the b = 1e-3 solve: max C_A||grad v|| = {CA * max(s3["grad_v"]):.4e} '
  f'(holds: {CA * max(s3["grad_v"]) <= NU / 2}); certified radii beta1(T): ' + ', '.join(f'T={t}: {rows[t]["beta1"]:.2e}' for t in CHECK_T))
P(f'all bounds dominate their measurements: {ok}')
P('')
P('Table C (NOT certified): the chain with G1 and D1 replaced by the measured sup_t ||grad q1|| and int ||Lap q1||^2 over [0,T]')
P('         i.e. the conditional scenario of NOTE.md section 7 if a validated propagator bound were available')
P(f'{"T":>5} {"G1 meas":>10} {"D1 meas":>10} {"beta1 cond":>12} {"Vbar cond":>12} {"Etilde cond":>12} {"Ebar cond":>12} {"C_Z cond":>12} {"|R_Z|/b^4 meas":>15}')
for t in CHECK_T:
    j = idx[t]
    G1m = max(hier['grad_q1'][: j + 1]) * 1.001
    D1m = hier['int_lap_q1_sq'][j] * 1.001
    r = constants.chain(A, C, D, NU, CA, t, 20000, G1_override=G1m, D1_override=D1m)
    P(f'{t:5.2f} {G1m:10.4f} {D1m:10.4f} {r["beta1"]:12.3e} {r["Vbar"]:12.3e} {r["Etilde"]:12.3e} {r["Ebar"]:12.3e} {r["C_Z"]:12.3e} {abs(s2["R_Z"][j]) / b2 ** 4:15.3e}')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
(HERE / 'results' / 'measurements.json').write_text(json.dumps({
    'parameters': dict(N=N, K=g.K, nu=NU, phi=PHI, a=A, c=C, d=D, dt=DT, T=T, out_every=OUT_EVERY, bs=BS, C_A=CA,
                       sources={'response.py': sha(RESP_PATH), 'ns.py': sha(audit.__file__), 'constants.py': sha(CONST_PATH)},
                       numpy=np.__version__, python=platform.python_version(), wall_seconds=wall),
    'times': TIMES.tolist(), 'hierarchy': hier, 'per_b': per_b, 'base_1d': base,
    'bounds': {str(t): {k: v for k, v in rows[t].items() if k != 'series'} for t in CHECK_T}}, indent=1) + '\n')
print('\n'.join(L))
