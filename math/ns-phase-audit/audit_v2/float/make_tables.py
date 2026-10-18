"""Format the Laurent tables from tables_float.npz with the numerical-zero
threshold tau = 1e-13 (see report).  c_{n,-m} = c_{n,m} (checked), so m>=0."""
import numpy as np
d = np.load("tables_float.npz")
tau = 1e-13
def get(c, mm, n, m):
    return c[n, int(np.where(mm == m)[0][0])]
gl_noise = 0.0
for lab in ["0", "1/28", "1/7"]:
    cA, mmA, cB, mmB = d[lab+"_cA"], d[lab+"_mmA"], d[lab+"_cB"], d[lab+"_mmB"]
    print(f"nu = {lab}   (N=28, M=32; '0' means |c| < tau=1e-13; last col = max |c_nm| over 5<=|m|<=16)")
    print(" n " + "".join(f"{'m='+str(m):>22s}" for m in range(5)) + f"{'|m|>=5':>10s}")
    for n in range(13):
        row = []
        for m in range(5):
            v = get(cA, mmA, n, m)
            row.append(f"{v.real:+22.13e}" if abs(v) > tau else f"{'0':>22s}")
        hi = max(abs(get(cA, mmA, n, m)) for m in mmA if abs(m) >= 5)
        print(f"{n:2d} " + "".join(row) + f"{hi:10.1e}")
        for m in mmA:
            a, b = get(cA, mmA, n, m), get(cB, mmB, n, m) if m in mmB else 0
            if abs(m) > n + 2 or abs(a) < tau:
                gl_noise = max(gl_noise, abs(a))
    print()
print("largest |c| among entries classified zero (all nu, n<=12, all m):", gl_noise)
