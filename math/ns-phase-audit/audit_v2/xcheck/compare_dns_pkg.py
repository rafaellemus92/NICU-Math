"""Cross-check DNS-report trajectories (dns/c1_N*_dt*_phi*.npz, fixed-dt RK4)
against the package's archived diagnostics.csv (adaptive CFL-capped RK4), whole
trajectory, plus dZ/dt(4) sign, peak values, curvature values."""
import csv, json, glob
import numpy as np
W = ".."
P = "../../periodic_ns_lab_v2"

def pkg_diag(label):
    rows = list(csv.DictReader(open(f"{P}/results/{label}/diagnostics.csv")))
    return rows

r0 = pkg_diag("refine_p00_N64")
print("package diagnostics columns:", list(r0[0].keys()))

phis = {"p00": "0.000000", "p01": "0.971073", "p02": "2.159845"}
for N in (32, 48, 64):
    for p, ps in phis.items():
        fn = f"{W}/dns/c1_N{N}_dt0.005_phi{ps}.npz"
        try:
            d = np.load(fn)
        except FileNotFoundError:
            continue
        rows = pkg_diag(f"refine_{p}_N{N}")
        tp = np.array([float(r["t"]) for r in rows]); Zp = np.array([float(r["enstrophy"]) for r in rows]); Ep = np.array([float(r["energy"]) for r in rows])
        dZp = np.array([float(r["dzdt"]) for r in rows]) if ("dZdt" in rows[0] or "dzdt" in rows[0]) else None
        t, Z, E = d["t"], d["Z"], d["E"]
        Zi = np.interp(tp, t, Z); Ei = np.interp(tp, t, E)
        # only exact sample matches (t grid 0.005 contains 0.05 multiples)
        idx = [int(round(x / 0.005)) for x in tp]
        ok = np.allclose(t[idx], tp, atol=1e-9)
        dz = np.abs(Z[idx] - Zp); de = np.abs(E[idx] - Ep)
        # dZ/dt at t=4 from DNS by 4th-order one-sided FD on the 0.005 grid
        h = t[1] - t[0]
        dZ4 = (25 * Z[-1] - 48 * Z[-2] + 36 * Z[-3] - 16 * Z[-4] + 3 * Z[-5]) / (12 * h)
        jmax = int(np.argmax(Zp))
        print(f"N={N} {p}: samples aligned={ok}; max|Z_dns-Z_pkg| over [0,4] = {dz.max():.2e} (at t={tp[dz.argmax()]:.2f}); "
              f"max|E diff| = {de.max():.2e}; DNS dZ/dt(4) = {dZ4:+.6f}" + (f"; pkg dZdt(4) = {dZp[-1]:+.6f}" if dZp is not None else "")
              + f"; pkg sampled peak {Zp[jmax]:.9f}@{tp[jmax]:.2f} vs DNS {Z[idx][jmax]:.9f}")

# curvature crossing values: package curvature_crossing.csv vs DNS tangent
print()
cc = list(csv.DictReader(open(f"{P}/results/curvature_crossing.csv")))
for r in cc:
    print("pkg crossing", r)
for N in (24, 32, 48, 64):
    for fn in sorted(glob.glob(f"{W}/dns/c3_N{N}_dt0.005.json")):
        d = json.load(open(fn))
        s = json.dumps(d)
        print(f"DNS c3 N={N}:", s[:600])
