"""P1 at FINITE time (solution level, not Taylor): with beta=0 the phi-harmonics
|m|>=2 of Z(T,phi) and E(T,phi) must vanish for every T.  Uses the DNS report's
independent solver (dns/ns.py), N=24, dt=0.01, M=8 equispaced phases.
Also: field-level checks (kz content, u2, u1 = alpha e^{-nu t} sin y), and the
finite-time beta-scaling of the m=2 harmonic (P1+P2 predict O(beta^2) as beta->0)."""
import sys, time
import numpy as np
sys.path.insert(0, "../dns")
from ns import NS

N, dt = 24, 0.01
M = 8
phis = 2 * np.pi * np.arange(M) / M + 0.137
T_out = [1.0, 2.0, 4.0]

def harmonics(vals):
    # vals[j] at phis[j]; Laurent coefficient c_m = (1/M) sum_j vals_j e^{-i m phi_j}
    return {m: np.mean(vals * np.exp(-1j * m * phis)) for m in range(0, M // 2 + 1)}

def run(nu, a, b, c, d, check_fields=False):
    s = NS(N, nu=nu)
    g = s.g
    out = {T: ([], []) for T in T_out}
    fieldchk = 0.0
    for phi in phis:
        uh = s.init_family(phi, a, b, c, d)
        t = 0.0; nstep = 0
        for T in T_out:
            while nstep * dt < T - 1e-12:
                uh = s.step(uh, dt); nstep += 1
            out[T][0].append(g.enstrophy(uh)); out[T][1].append(g.energy(uh))
            if check_fields:
                u = g.inv(uh)
                kz_content = np.abs(uh[..., 1:]).max()           # any kz != 0 coefficient
                u2 = np.abs(u[1]).max()
                X, Y, Z = np.broadcast_arrays(g.X, g.Y, g.Z)
                u1_err = np.abs(u[0] - a * np.exp(-nu * T) * np.sin(Y)).max()
                fieldchk = max(fieldchk, kz_content, u2, u1_err)
    res = {}
    for T in T_out:
        Zs, Es = np.array(out[T][0]), np.array(out[T][1])
        res[T] = (harmonics(Zs), harmonics(Es))
    return res, fieldchk

t0 = time.time()
for (nu, amps, lab) in [(1 / 28, (1.3, 0.0, 0.7, 1.1), "beta=0, generic amps, nu=1/28"),
                        (0.0, (1.0, 0.0, 1.0, 1.0), "beta=0, unit amps, Euler"),
                        (1 / 28, (1.0, 1.0, 1.0, 1.0), "CONTROL beta=1, unit amps, nu=1/28")]:
    res, fc = run(nu, *amps, check_fields=(amps[1] == 0.0))
    print(f"== {lab}  (field checks max defect: {fc:.1e})" if amps[1] == 0.0 else f"== {lab}")
    for T in T_out:
        hz, he = res[T]
        print(f"  T={T}: |Z_m| m=0..4: " + " ".join(f"{abs(hz[m]):.2e}" for m in range(5))
              + "   |E_m| m=2..4: " + " ".join(f"{abs(he[m]):.2e}" for m in range(2, 5)))
    if lab.startswith("beta=0, unit amps, Euler"):
        # analytic: Z(t) = 1 + (t/4) cos phi + t^2/4 for beta=0 Euler unit amps (float report)
        for T in T_out:
            hz, _ = res[T]
            print(f"   analytic check T={T}: c0={hz[0].real:.12f} vs {1+T*T/4:.12f};  2c1={2*hz[1].real:.12f} vs {T/4:.12f}")
print("time", time.time() - t0, flush=True)

# finite-time beta scaling of m=2 harmonic at T=1 (unit other amps, nu=1/28)
print("== finite-time m=2 harmonic of Z(T=1) vs beta (P1+P2 => O(beta^2), and even in beta?)")
for b in [0.4, 0.2, 0.1, 0.05, -0.1]:
    res, _ = run(1 / 28, 1.0, b, 1.0, 1.0)
    c2 = res[1.0][0][2]
    print(f"  beta={b:+.2f}: c2={c2.real:+.6e} (Im {c2.imag:+.1e});  c2/beta^2={c2.real/b**2:+.6e}")
print("time", time.time() - t0)
