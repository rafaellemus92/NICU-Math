"""Local optimum of Z(2,phi) at N=64 (K=21) by tangent-Newton (DNS report's NSTangent),
started at the N=48 optimum 0.9703653579. Closes the N-robustness gap for C4."""
import sys, time
sys.path.insert(0, "../dns")
from ns import NSTangent
N, T, dt = 64, 2.0, 0.005
mt = NSTangent(N, 1.0 / 28.0)
phi = 0.9703653579
t0 = time.time()
for it in range(3):
    Y = mt.init_aug(phi)
    for _ in range(int(round(T / dt))):
        Y = mt.step(Y, dt)
    z0, z1, z2 = mt.zderivs(Y)
    print(f"it {it}: phi={phi:.12f} Z={z0:.12f} Z_phi={z1:+.3e} Z_phiphi={z2:.6f} ({time.time()-t0:.0f}s)", flush=True)
    if abs(z1 / z2) < 1e-11:
        break
    phi -= z1 / z2
print(f"N=64 phi*={phi:.10f}")
