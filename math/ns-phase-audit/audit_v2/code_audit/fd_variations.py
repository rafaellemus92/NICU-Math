import sys, time, numpy as np
sys.path.insert(0, '../../periodic_ns_lab_v2')
from ns_solver import PeriodicNS
from phase_sensitivity import integrate
n = 24; s = PeriodicNS(n, 1/28)
def Zpath(phase, times, dt=0.01):
    u = s.initial(phase=phase); t = 0.0; out = {}
    for T in times:
        while t < T - 1e-12:
            adv, diff = s.dt_limits(u); step = min(dt, adv, diff, T - t)
            assert step == min(dt, T - t), "CFL limit active"
            u = s.step(u, step); t += step
        out[T] = s.diagnostics(u)['enstrophy']
    return out
t0 = time.time()
# (a) phi=0 curvature at T=1.76, 1.77 (Z even in phi -> d2Z ~ 2(Z(h)-Z(0))/h^2, also full centered)
T = [1.76, 1.77, 2.0]
z0 = Zpath(0.0, T)
for h in (2e-2, 1e-2):
    zp = Zpath(h, T); zm = Zpath(-h, T)
    print(f"h={h}: " + "  ".join(f"T={t}: FD d2Z={(zp[t]-2*z0[t]+zm[t])/h**2:+.7f} (even check {abs(zp[t]-zm[t]):.1e})" for t in T))
rows, _, _ = integrate(n, 0.0, 2.0, .01, .01)
d = {round(r['t'], 6): r for r in rows}
print("variational d2Z at phi=0:", {t: round(d[t]['d2Z_dphi2'], 7) for t in T})
# (b) phi*=0.9710730319801146 at T=2: dZ and d2Z
p = 0.9710730319801146
zc = Zpath(p, [2.0])[2.0]
for h in (2e-2, 1e-2, 5e-3):
    zp = Zpath(p+h, [2.0])[2.0]; zm = Zpath(p-h, [2.0])[2.0]
    print(f"phi*={p}, h={h}: FD dZ={(zp-zm)/(2*h):+.3e}  FD d2Z={(zp-2*zc+zm)/h**2:+.7f}")
r = integrate(n, p, 2.0)[0][-1]
print("variational at phi*:", r)
print("wall", time.time()-t0)
