# Historical calculation retained for provenance; see README.md here.
# Its majorant/sample-based numbers are NOT rigorous ceilings on the true radius.
"""(a) Upper bounds on the radius certifiable by condition (1), |b| F_s <= nu e^{-A}/(2K),
using (i) the appendix's explicit C_base (A <= K C_base/nu) and (ii) the TRUE
phase-max integral int_0^inf sup_phi ||U||_{s+1} dt measured in true_base_norm.py,
with K replaced by the certified lower bounds from K_lower_bound.py (beta_max is
decreasing in K, so these are rigorous upper bounds on what (1) can ever certify).
(b) Numerical check of the scalar comparison y(t) <= y(0) h/(1 - K y(0) int h)
for y' = (-nu + K M)y + K y^2 with M(t)=C e^{-nu t}."""
import math, numpy as np
print("WARNING: historical estimates below are not certified radius bounds; see review/README.md.")
nu = 1/28
cases = [  # s, F_s, K_lb, true int M (from true_base_norm.py, Nn=128), log10(C_base/nu) appendix
    (4, 2**1.5, 0.1564, 2343.37, 71.31),
    (8, 2**3.5, 0.0762, 1.92772e6, 278.60),
]
for s, F, K, Itrue, log10_app in cases:
    # (i) appendix majorant
    log10_beta_app = math.log10(nu/(2*K*F)) - K*10**log10_app/math.log(10)
    # (ii) true integral
    log10_beta_true = math.log10(nu/(2*K*F)) - K*Itrue/math.log(10)
    print(f"s={s}: with K>={K}: appendix-majorant radius <= 10^({log10_beta_app:.3g});  "
          f"true-base-integral radius <= 10^({log10_beta_true:.1f})")
# a plausible (not certified) K of order 10 for the realistic case
for s, F, K, Itrue, _ in cases:
    for Kp in [1.0, 10.0]:
        print(f"   s={s}, if K={Kp}: true-base-integral radius <= 10^({math.log10(nu/(2*Kp*F)) - Kp*Itrue/math.log(10):.1f})")

# (b) comparison check
K = 1.0; C = 2.0; y0 = 0.05
Ainf = K*C/nu
beta = nu*math.exp(-Ainf)/(2*K)  # condition (1) threshold for y(0)
print(f"\ncomparison test: K={K}, M=C e^(-nu t) with C={C}, A_inf={Ainf:.3f}, y(0) threshold from (1) = {beta:.3e}")
for y0 in [beta, 0.5*beta, 2*beta]:
    t = 0.0; y = y0; dt = 1e-3; A = 0.0; H = 0.0; worst = -1.0
    ok = True
    while t < 400:
        def f(tt, yy): return (-nu + K*C*math.exp(-nu*tt))*yy + K*yy*yy
        k1 = f(t, y); k2 = f(t+dt/2, y+dt*k1/2); k3 = f(t+dt/2, y+dt*k2/2); k4 = f(t+dt, y+dt*k3)
        y += dt*(k1+2*k2+2*k3+k4)/6
        # exact A(t) and int h by quadrature
        t += dt
        A = K*C*(1-math.exp(-nu*t))/nu
        h = math.exp(-nu*t + A)
        H += dt*(h + math.exp(-(t-dt)*nu + K*C*(1-math.exp(-nu*(t-dt)))/nu))/2
        den = 1 - K*y0*H
        if den <= 0 or not math.isfinite(y):
            ok = False; break
        bound = y0*h/den
        worst = max(worst, y/bound)
    print(f"  y0/threshold={y0/beta:.2f}: ODE stays finite={ok}, max y/bound={worst:.6f} (<=1 means bound holds), "
          f"min denominator={1-K*y0*H:.4f}, 2 y0 e^Ainf e^(-nu t) at t=400 vs y: {2*y0*math.exp(Ainf)*math.exp(-nu*400):.3e} vs {y:.3e}")
