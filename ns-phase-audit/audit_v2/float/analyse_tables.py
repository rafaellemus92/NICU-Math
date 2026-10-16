"""Print |c_{n,m}| tables, noise diagnostics, and A-vs-B agreement."""
import numpy as np
d = np.load("tables_float.npz")
eps = np.finfo(float).eps
nmax = 12
def get(c, mm, n, m):
    return c[n, int(np.where(mm == m)[0][0])]
for lab in ["0", "1/28", "1/7"]:
    cA, mmA, cB, mmB, ZA = d[lab+"_cA"], d[lab+"_mmA"], d[lab+"_cB"], d[lab+"_mmB"], d[lab+"_ZA"]
    print(f"\n===== nu = {lab} =====")
    print("n  | max|Z_n(phi)| | noise(|m|>n+2,A) | max|Im c| | max|c_m - c_-m| | max_m|cA-cB|  | ratio noise/(eps*max|Z|)")
    for n in range(nmax+1):
        sc = np.abs(ZA[:, n]).max()
        zero = [abs(get(cA, mmA, n, m)) for m in mmA if abs(m) > n+2]
        nz = max(zero) if zero else float('nan')
        imc = max(abs(get(cA, mmA, n, m).imag) for m in range(-(n+2), n+3))
        sym = max(abs(get(cA, mmA, n, m) - get(cA, mmA, n, -m)) for m in range(0, n+3))
        ab = max(abs(get(cA, mmA, n, m) - get(cB, mmB, n, m)) for m in range(-(n+2), n+3))
        print(f"{n:2d} | {sc:.3e} | {nz:.2e} | {imc:.2e} | {sym:.2e} | {ab:.2e} | {max(nz,ab)/(eps*sc):.1f}")
    print("\n|c_{n,m}| (A), m = 0..7")
    print("n   " + "".join(f"{'m='+str(m):>12s}" for m in range(8)))
    for n in range(nmax+1):
        print(f"{n:2d}  " + "".join(f"{abs(get(cA, mmA, n, m)):12.3e}" for m in range(8)))
    print("signed Re c_{n,m} (A), m=0..4")
    for n in range(nmax+1):
        print(f"{n:2d}  " + "".join(f"{get(cA, mmA, n, m).real:+.15e} " for m in range(5)))
