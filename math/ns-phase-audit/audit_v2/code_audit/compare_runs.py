"""Compare reproduced trajectories with archived ones (diagnostics.csv row-by-row) and
recompute full-field grid comparisons from regenerated Fourier states."""
import csv, json, sys, glob, os
import numpy as np
ARCH = '../../periodic_ns_lab_v2/results'
NEW = '../code_audit_rerun'
def rows(p):
    with open(p) as f: return [{k: float(v) if v not in ('True', 'False') else v for k, v in r.items()} for r in csv.DictReader(f)]
def cmp_diag(a, b, keys=('energy', 'enstrophy', 'stretching', 'D')):
    ra, rb = rows(a), rows(b)
    assert len(ra) == len(rb), (a, len(ra), len(rb))
    worst = 0.0
    for x, y in zip(ra, rb):
        assert abs(x['t'] - y['t']) < 1e-12
        for k in keys:
            worst = max(worst, abs(x[k] - y[k]) / max(abs(y[k]), 1e-300))
    return worst, len(ra)
what = sys.argv[1]
if what == 'sweep':
    w = []
    for d in sorted(glob.glob(f'{NEW}/sweep/sweep_*_N24')):
        lab = os.path.basename(d)
        w.append((lab,) + cmp_diag(f'{d}/diagnostics.csv', f'{ARCH}/{lab}/diagnostics.csv'))
    print('sweep: runs compared', len(w), ' max relative diff over all rows/keys', max(x[1] for x in w))
    S = {r['label']: r for r in csv.DictReader(open(f'{NEW}/sweep/sweep_summary.csv'))}
    for T in (1, 2, 3, 4):
        best = max(S.values(), key=lambda r: float(r[f'Z_t{T}']))
        print(f'  T={T}: argmax over 33-point grid phase={float(best["phase"]):.6f}  Z={float(best[f"Z_t{T}"]):.9f}')
elif what == 'time':
    for lab in ('dt0.01', 'dt0.005', 'dt0.0025'):
        print(lab, cmp_diag(f'{NEW}/time_refinement/{lab}/diagnostics.csv', f'{ARCH}/time_refinement/{lab}/diagnostics.csv'))
    v = np.load(f'{NEW}/time_refinement/dt0.0025/state_t2.npz')['u_hat']
    for lab in ('dt0.01', 'dt0.005'):
        u = np.load(f'{NEW}/time_refinement/{lab}/state_t2.npz')['u_hat']
        print('  rel field L2 vs dt0.0025', lab, np.linalg.norm(u - v) / np.linalg.norm(v))
elif what == 'curv':
    for n in (24, 32, 48):
        p = f'{NEW}/curvature_N{n}/diagnostics.csv'
        if not os.path.exists(p): continue
        print(n, cmp_diag(p, f'{ARCH}/curvature_N{n}/diagnostics.csv', keys=('Z', 'd2Z_dphi2')))
        r = rows(p); neg = [x for x in r if x['d2Z_dphi2'] < 0 and x['t'] > 0.5]; pos = [x for x in r if x['d2Z_dphi2'] > 0 and x['t'] > 1]
        lo = max(x['t'] for x in r if x['t'] > 1 and x['d2Z_dphi2'] < 0); hi = min(x['t'] for x in r if x['t'] > lo)
        a = [x for x in r if x['t'] == lo][0]['d2Z_dphi2']; b = [x for x in r if x['t'] == hi][0]['d2Z_dphi2']
        # quadratic (3-point) root vs linear root
        t3 = [x for x in r if lo - 0.0101 < x['t'] < hi + 0.0101]
        ts = np.array([x['t'] for x in t3]); vs = np.array([x['d2Z_dphi2'] for x in t3])
        c = np.polyfit(ts, vs, 3); roots = [z.real for z in np.roots(c) if abs(z.imag) < 1e-12 and lo <= z.real <= hi]
        sign_changes = [(r[i]['t'], r[i+1]['t']) for i in range(len(r)-1) if r[i]['t'] > 0 and np.sign(r[i]['d2Z_dphi2']) != np.sign(r[i+1]['d2Z_dphi2'])]
        print(f'   sign changes (t>0): {sign_changes}; linear root {lo + (hi-lo)*(-a)/(b-a):.9f}; cubic-fit root {roots}')
elif what == 'refine':
    labs = sorted(os.path.basename(d) for d in glob.glob(f'{NEW}/refine/refine_p*'))
    for lab in labs:
        print(lab, cmp_diag(f'{NEW}/refine/{lab}/diagnostics.csv', f'{ARCH}/{lab}/diagnostics.csv'))
    def embed(a, nlo, nhi):
        freq = np.rint(np.fft.fftfreq(nlo)*nlo).astype(int); idx = freq % nhi
        out = np.zeros((3, nhi, nhi, nhi), complex)
        for c in range(3): out[c][np.ix_(idx, idx, idx)] = a[c]
        return out
    arch = {(int(r['phase_index']), r['time'], int(r['n'])): r for r in csv.DictReader(open(f'{ARCH}/spatial_comparison.csv'))}
    for j in range(3):
        for T in (2, 4):
            hi = np.load(f'{NEW}/refine/refine_p{j:02d}_N64/state_t{T}.npz')['u_hat']
            for n in (32, 48):
                lo = np.load(f'{NEW}/refine/refine_p{j:02d}_N{n}/state_t{T}.npz')['u_hat']
                e = embed(lo, n, 64)
                rel = np.linalg.norm(e - hi) / np.linalg.norm(hi)
                # also: difference restricted to the modes the coarse grid retains, and the 64^3 tail beyond them
                kmax = (n - 1)//3
                f64 = np.rint(np.fft.fftfreq(64)*64).astype(int)
                K = np.max(np.abs(np.array(np.meshgrid(f64, f64, f64, indexing='ij'))), axis=0)
                inside = K <= kmax
                rel_in = np.linalg.norm((e - hi)[:, inside]) / np.linalg.norm(hi)
                rel_tail = np.linalg.norm(hi[:, ~inside]) / np.linalg.norm(hi)
                k = np.array(np.meshgrid(f64, f64, f64, indexing='ij')); k2 = np.sum(k*k, 0)
                Z = lambda u: 0.5*np.sum(k2*np.sum(np.abs(u)**2, 0))
                relZ = abs(Z(e)/Z(hi) - 1)
                a = arch[(j, str(T), n)]
                print(f'phase{j} T={T} N{n} vs 64: relL2={rel:.4e} (archived {float(a["relative_field_L2"]):.4e})  relZ={relZ:.4e} (archived {float(a["relative_Z_difference"]):.4e})  in-band part={rel_in:.3e} 64-tail beyond K_{n}={rel_tail:.3e}')
