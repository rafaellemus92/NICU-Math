"""Tests of locking.py against the exact results stated in its docstring.  Run: python3 test_locking.py"""
import math, sys
from locking import *

fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (("  — " + detail) if detail else ""))
    if not ok: fails += 1

# --- Adler: lock, fixed phase, recovery rate measured from an integration ---
dw, K = 0.2, 0.5
phi_star, lam = adler_fixed_phase(dw, K), adler_recovery_rate(dw, K)
ts, ps = adler_integrate(dw, K, phi_star + 0.1, 40.0)
i1, i2 = int(2.0 / 1e-3), int(6.0 / 1e-3)
lam_meas = math.log(abs(ps[i1] - phi_star) / abs(ps[i2] - phi_star)) / (ts[i2] - ts[i1])
check("Adler lock: phi* = asin(dw/K) and the orbit converges to it", abs(ps[-1] - phi_star) < 1e-6, f"phi*={phi_star:.6f} phi(40)={ps[-1]:.9f}")
check("Adler recovery rate = sqrt(K^2-dw^2)", abs(lam_meas - lam) / lam < 0.01, f"measured {lam_meas:.5f} exact {lam:.5f}")

# --- Adler: slip period outside the lock (the brief's numbers: dw=0.377, K=0.28) ---
dw, K = 0.377, 0.28
T_slip = adler_slip_period(dw, K)
ts, ps = adler_integrate(dw, K, 0.0, 300.0, dt=2e-3)
slips = int((ps[-1] - ps[0]) // (2 * math.pi))
T_meas = (ts[-1] - ts[0]) / ((ps[-1] - ps[0]) / (2 * math.pi))
check("Adler slip period = 2pi/sqrt(dw^2-K^2)", abs(T_meas - T_slip) / T_slip < 0.02, f"measured {T_meas:.2f} s exact {T_slip:.2f} s ({slips} slips in 300 s)")
check("at threshold the slip period diverges", adler_slip_period(0.28, 0.28) == math.inf)

# --- circle map: exact 0:1 edge ---
K = 0.5
t0 = circle_tongue(0, 1, K)
check("0/1 tongue upper edge = K/2pi", abs(t0["hi"] - K / TWO_PI) < 2e-4, f"{t0['hi']:.5f} vs {K/TWO_PI:.5f}")
t1 = circle_tongue(1, 1, K)
check("1/1 tongue lower edge = 1 - K/2pi", abs(t1["lo"] - (1 - K / TWO_PI)) < 2e-4, f"{t1['lo']:.5f}")

# --- width ~ K^q ---
w2a, w2b = circle_tongue(1, 2, 0.1)["width"], circle_tongue(1, 2, 0.2)["width"]
w3a, w3b = circle_tongue(1, 3, 0.2)["width"], circle_tongue(1, 3, 0.4)["width"]
check("1/2 tongue: doubling K multiplies width by ~4", abs(w2b / w2a - 4) < 0.6, f"ratio {w2b/w2a:.2f}")
check("1/3 tongue: doubling K multiplies width by ~8", abs(w3b / w3a - 8) < 1.6, f"ratio {w3b/w3a:.2f}")
K = 0.8
w12, w13, w25, w37, w1317 = (circle_tongue(*pq, K)["width"] for pq in [(1, 2), (1, 3), (2, 5), (3, 7), (13, 17)])
check("simple ratios lock widest; mediant 2/5 wider than 3/7; 13/17 tiny", w12 > w13 > w25 > w37 and w1317 < 0.05 * w12, f"1/2 {w12:.4f} 1/3 {w13:.4f} 2/5 {w25:.4f} 3/7 {w37:.4f} 13/17 {w1317:.1e}")

# --- golden mean ---
om = circle_omega_for(GOLDEN, 0.9)
a = circle_analyze(om, 0.9, n=20000, qmax=200)
cf = continued_fraction(a["W"], 8)
check("golden orbit quasi-periodic at K=0.9, continued fraction [0;1,1,1,1,...]", (not a["locked"]) and cf[0] == 0 and all(v == 1 for v in cf[1:6]), f"W={a['W']:.6f} cf={cf}")

# --- chaos only beyond K=1 ---
below = max(circle_analyze(o, k)["lyap"] for k in (0.3, 0.7, 1.0) for o in (0.1, 0.3, GOLDEN, 0.75))
above = any(circle_analyze(o, 1.6)["lyap"] > 0.05 for o in (0.05, 0.3, 0.618, 0.9))
check("no positive Lyapunov exponent for K<=1; chaos at K=1.6", below <= 1e-3 and above, f"max below {below:.1e}")

print("ALL PASS" if not fails else f"{fails} FAILED")
sys.exit(1 if fails else 0)
