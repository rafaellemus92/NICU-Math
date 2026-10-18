# Shared Air limits, "Test 4's second state": equilibria of the deterministic perceived world
# for g in {0.5, ..., 3.0}, with and without the capacity limit cap(A_m) = 1/(1 + (A_m/0.8)^2),
# and the largest real part of the Jacobian eigenvalues at each equilibrium.
# Run from this folder: python3 -I bistability_equilibria_sweep.py   (numpy only, <1 s)
# Formerly numerics/_raw/limits/bistab.py.

# Equilibria of the deterministic perceived world (U=0, noise=0, A0=0, steadiness=1).
# infant: 0 = -Ai/30 - C + 0.04 g Am - 0.02 Ai^3
# mom:    0 = -Am/20 + 0.10 g Ai - 0.02 Am^3
# sooth:  C = 0.30 g Ai cap(Am), cap = 1/(1+(Am/0.8)^2)  (or cap = 1)
import numpy as np
def cap(Am, withcap): return 1/(1+(Am/0.8)**2) if withcap else 1.0
def F(Ai, Am, g, withcap):
    C = 0.3*g*Ai*cap(Am, withcap)
    return (-Ai/30 - C + 0.04*g*Am - 0.02*Ai**3, -Am/20 + 0.1*g*Ai - 0.02*Am**3)
def jac(x, g, withcap, h=1e-7):
    # full 3x3 Jacobian in (Ai, Am, C)
    Ai, Am, C = x
    def f(v):
        Ai, Am, C = v
        return np.array([-Ai/30 - C + 0.04*g*Am - 0.02*Ai**3,
                         -Am/20 + 0.1*g*Ai - 0.02*Am**3,
                         (0.3*g*Ai*cap(Am, withcap) - C)/4])
    J = np.zeros((3,3))
    for j in range(3):
        e = np.zeros(3); e[j] = h
        J[:,j] = (f(np.array(x)+e) - f(np.array(x)-e))/(2*h)
    return J
# Reduce: from mom eq, Ai = (Am/20 + 0.02 Am^3)/(0.1 g); plug into infant eq -> scalar in Am.
def infant_res(Am, g, withcap):
    Ai = (Am/20 + 0.02*Am**3)/(0.1*g)
    return F(Ai, Am, g, withcap)[0], Ai
for withcap in (True, False):
    print("cap" if withcap else "no cap")
    for g in [0.5, 1, 1.5, 1.8, 1.9, 2.0, 2.1, 2.2, 2.5, 3.0]:
        Ams = np.linspace(1e-4, 20, 400001)
        r = np.array([infant_res(a, g, withcap)[0] for a in Ams[::50]])
        A = Ams[::50]
        roots = []
        for i in range(len(r)-1):
            if r[i]*r[i+1] < 0:
                lo, hi = A[i], A[i+1]
                for _ in range(80):
                    mid = (lo+hi)/2
                    if infant_res(lo, g, withcap)[0]*infant_res(mid, g, withcap)[0] <= 0: hi = mid
                    else: lo = mid
                Am = (lo+hi)/2; Ai = infant_res(Am, g, withcap)[1]
                C = 0.3*g*Ai*cap(Am, withcap)
                ev = np.linalg.eigvals(jac((Ai, Am, C), g, withcap))
                roots.append((round(Ai,5), round(Am,5), round(max(ev.real),5)))
        ev0 = np.linalg.eigvals(jac((0,0,0), g, withcap))
        print(f"  g={g}: origin maxRe={max(ev0.real):.5f}; nonzero eq (Ai,Am,maxRe):", roots)
