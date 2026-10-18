"""Measured constants of the b^2 bound, from results/long_b.json (b = 0.25 and 1, 3D DNS to t = 20)
and results/reduced_family_t20.json (b = 0, the reduced solver on the same grid).
  K_Z(t) = (A_Z(b) - A_Z(0)) / b^2,  K_S(t) = (A_S(b) - A_S(0)) / b^2   (phi-averaged shifts),
  sup_t |B2_Z| / b^2, sup_t |B3_Z| / b^2, sup_t |B2_S| / b^2, sup_t |B2_E| / b^2,
  accumulated extra stretching  int_0^20 (A_S(b) - A_S(0)) dt / b^2.
Run: python3 measured_constants.py
"""
import json, numpy as np
long = json.load(open("results/long_b.json"))
base = {round(r["t"], 3): r for r in json.load(open("results/reduced_family_t20.json"))}
for bkey, rows in long.items():
    b = float(bkey); b2 = b * b
    ts = np.array([r["t"] for r in rows])
    AZ = np.array([r["Z"]["A"] for r in rows]); AS = np.array([r["S"]["A"] for r in rows]); AE = np.array([r["E"]["A"] for r in rows])
    AZ0 = np.array([base[round(t, 3)]["Z"]["A"] for t in ts]); AS0 = np.array([base[round(t, 3)]["S"]["A"] for t in ts]); AE0 = np.array([base[round(t, 3)]["E"]["A"] for t in ts])
    B1Z = np.array([r["Z"]["B1"] for r in rows]); B1Z0 = np.array([base[round(t, 3)]["Z"]["B1"] for t in ts])
    KZ, KS, KE = (AZ - AZ0) / b2, (AS - AS0) / b2, (AE - AE0) / b2
    K1 = (B1Z - B1Z0) / b2
    sup = lambda name, j: max(((abs(r[name][j]) / b2), r["t"]) for r in rows)
    print(f"b = {b}")
    print(f"  phi-averaged shifts per b^2:  K_Z max {KZ.max():+.3f} at t={ts[KZ.argmax()]:.1f}, K_S max {KS.max():+.3f} at t={ts[KS.argmax()]:.1f}, K_E min {KE.min():+.3f} at t={ts[KE.argmin()]:.1f}")
    print(f"  shift of the first harmonic of Z per b^2: max |.| {np.abs(K1).max():.3f} at t={ts[np.abs(K1).argmax()]:.1f}")
    print(f"  accumulated extra stretching int_0^20 (S_b - S_0) dt / b^2 = {np.trapezoid(AS - AS0, ts) / b2:+.3f}   (int_0^20 S_0 dt = {np.trapezoid(AS0, ts):.3f})")
    for name, j in (("Z", "B2"), ("Z", "B3"), ("S", "B2"), ("E", "B2")):
        v, t = sup(name, j); print(f"  sup_t |{name}:{j}| / b^2 = {v:.4f} at t = {t:.1f}")
    print("  table (t, K_Z, K_S, Z:B2/b^2, Z:B3/b^2):")
    for r, kz, ks in zip(rows, KZ, KS):
        if r["t"] in (0.5, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20):
            print(f"    {r['t']:5.1f} {kz:+8.3f} {ks:+8.3f} {r['Z']['B2']/b2:+9.4f} {r['Z']['B3']/b2:+9.4f}")
if "0.25" in long and "1.0" in long:
    r25 = {r["t"]: r for r in long["0.25"]}; r1 = {r["t"]: r for r in long["1.0"]}
    print("b^2 scaling check, Z:B2 at b=1 over 16 x Z:B2 at b=1/4 (1 if the b^2 law held exactly):")
    print("   " + "  ".join(f"t={t}: {r1[t]['Z']['B2'] / (16 * r25[t]['Z']['B2']):.2f}" for t in (0.5, 1, 2, 3, 4, 6, 10) if abs(r25[t]['Z']['B2']) > 1e-12))
