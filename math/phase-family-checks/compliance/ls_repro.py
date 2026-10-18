"""Reproduce the PR #17 compliance table with the repository generator.
Usage: python3 math/phase-family-checks/compliance/ls_repro.py <repository root>
Midpoint-volume OLS (interval-average V = V[k] + Q[k] dt/2) vs left-edge V; seed 42 and a 40-seed ensemble."""
import sys, numpy as np
sys.path.insert(0, sys.argv[1])
from navier_stokes.ventilator_ingest import generate_synthetic_waveform, segment_breaths
def ols(c, rate, mid):
    V = c.volume + (c.flow/rate/2 if mid else 0.0)
    X = np.column_stack([np.ones_like(V), V, c.flow]); b = np.linalg.lstsq(X, c.pressure, rcond=None)[0]
    return 1.0/b[1], 1e3*b[2]
def lamQ(noise, rate, seed):
    out = []
    for c0 in segment_breaths(generate_synthetic_waveform(n_breaths=50, sample_rate=rate, compliance=1.0, noise_level=0.0, seed=seed)):
        V = c0.volume + c0.flow/rate/2
        X = np.column_stack([np.ones_like(V), V]); Qp = c0.flow - X @ np.linalg.lstsq(X, c0.flow, rcond=None)[0]
        sQ = noise*np.abs(c0.flow).max(); out.append(Qp.var()/(Qp.var()+sQ**2))
    return np.mean(out)
settings = [(0.0, 100.0), (0.05, 100.0), (0.05, 1000.0), (0.10, 100.0)]
print("seed 42, 50 breaths, midpoint-volume fit (the table's convention?) and left-edge fit:")
print(f"{'noise':>5} {'Hz':>5} | {'range':>6} | {'C mid':>14} {'R mid':>12} | {'C left':>14} {'R left':>12} | {'80*lamQ':>7}")
for noise, rate in settings:
    cyc = segment_breaths(generate_synthetic_waveform(n_breaths=50, sample_rate=rate, compliance=1.0, noise_level=noise, seed=42))
    fm = np.array([ols(c, rate, True) for c in cyc]); fl = np.array([ols(c, rate, False) for c in cyc])
    rg = np.mean([(c.volume.max()-c.volume.min())/(c.pressure.max()-c.pressure.min()) for c in cyc])
    print(f"{noise:5.2f} {rate:5.0f} | {rg:6.3f} | {fm[:,0].mean():7.4f}±{fm[:,0].std():.3f} {fm[:,1].mean():6.2f}±{fm[:,1].std():4.2f} | "
          f"{fl[:,0].mean():7.4f}±{fl[:,0].std():.3f} {fl[:,1].mean():6.2f}±{fl[:,1].std():4.2f} | {80*lamQ(noise, rate, 42):7.2f}  (n={len(cyc)})")
print("\n40-seed ensemble, midpoint-volume fit:")
for noise, rate in settings:
    Cs, Rs = [], []
    for seed in range(40):
        for c in segment_breaths(generate_synthetic_waveform(n_breaths=50, sample_rate=rate, compliance=1.0, noise_level=noise, seed=seed)):
            C, R = ols(c, rate, True); Cs.append(C); Rs.append(R)
    Cs, Rs = np.array(Cs), np.array(Rs)
    print(f"{noise:5.2f} {rate:5.0f} | C={Cs.mean():.4f}±{Cs.std():.3f} (se {Cs.std()/np.sqrt(len(Cs)):.4f})  R={Rs.mean():.2f}±{Rs.std():.2f} (se {Rs.std()/np.sqrt(len(Rs)):.2f})  "
          f"bias R={Rs.mean()-80:+.2f}  80*lamQ={80*lamQ(noise, rate, 0):.2f}")
