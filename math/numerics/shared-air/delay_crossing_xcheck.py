# Shared Air, delayed linearisation: imaginary-axis crossing analysis (method 1 of 3).
# D(s) = (s+a)(s+b)(s+d) + h g (s+b) e^{-s tau} - c g^2 (s+d) e^{-2 s tau},
# a = 1/30, b = 1/20, d = 1/4, c = r q = 1/250 (r = 1/25, q = 1/10), h = 3/40.
# Checks: det(sI - A0 - A1 e^{-s tau}) = D(s); the tau = 0 threshold g_c; for g = 1 and g = 3,
# every root s = i w on the imaginary axis, the delays tau where it occurs and the crossing direction.
# Run from this folder: python3 -I delay_crossing_xcheck.py   (numpy only, ~10 s)
# Formerly numerics/_raw/delay-xcheck/xcheck.py.

import numpy as np
a, b, d, c, h = 1/30, 1/20, 1/4, 1/250, 3/40
r, q = 1/25, 1/10
assert abs(r*q - c) < 1e-15

def Dfun(s, g, tau):
    e = np.exp(-s*tau)
    return (s+a)*(s+b)*(s+d) + h*g*(s+b)*e - c*g**2*(s+d)*e**2

# --- check state space determinant equals D(s)
def A_mats(g):
    A0 = np.array([[-a,0,-1],[0,-b,0],[0,0,-d]], float)
    A1 = np.array([[0,r*g,0],[q*g,0,0],[h*g,0,0]], float)
    return A0, A1
for s in [0.3+0.7j, -0.2+1.1j, 0.05]:
    for g, tau in [(3,2),(1,4.7)]:
        A0, A1 = A_mats(g)
        det = np.linalg.det(s*np.eye(3) - A0 - A1*np.exp(-s*tau))
        assert abs(det - Dfun(s,g,tau)) < 1e-12, (det, Dfun(s,g,tau))
print("state-space det == D(s): OK")

# --- (0) zero delay: polynomial roots, threshold in g
def zero_delay_max_re(g):
    # (s+a)(s+b)(s+d) + h g (s+b) - c g^2 (s+d)
    p = np.poly([-a,-b,-d]) + np.concatenate([[0,0], h*g*np.array([1,b])]) - np.concatenate([[0,0], c*g*g*np.array([1,d])])
    return np.roots(p).real.max(), np.roots(p)
lo, hi = 0.1, 10.0
print("tau=0 max Re at g=3:", zero_delay_max_re(3)[0], " g=4:", zero_delay_max_re(4)[0])
for _ in range(200):
    m = 0.5*(lo+hi)
    if zero_delay_max_re(m)[0] < 0: lo = m
    else: hi = m
print("tau=0 stability threshold g* =", lo, " roots there:", zero_delay_max_re(lo)[1])
# constant term check: a b d + h g b - c g^2 d = 0
gs = np.roots([-c*d, h*b, a*b*d]); print("constant-term (s=0) roots in g:", gs)

# --- (1) imaginary-axis crossing analysis
# D(iw) = P + Q1 z - Q2 z^2, z = exp(-i w tau). For fixed w, solve the quadratic in z,
# require |z| = 1, then tau = (-arg z + 2 pi k)/w.
def zs(w, g):
    s = 1j*w
    P = (s+a)*(s+b)*(s+d); Q1 = h*g*(s+b); Q2 = c*g*g*(s+d)
    # -Q2 z^2 + Q1 z + P = 0
    return np.roots([-Q2, Q1, P])

def crossings(g, wmax=5.0, n=200001):
    ws = np.linspace(1e-6, wmax, n)
    out = []
    for branch in range(2):
        # track branches by sorting by modulus would mix; instead use function f_i(w) = |z_i|-1 for both roots sorted by modulus
        pass
    F = np.array([np.sort(np.abs(zs(w,g))) for w in ws]) - 1.0
    for k in range(2):
        f = F[:,k]
        idx = np.where(np.sign(f[:-1]) != np.sign(f[1:]))[0]
        for i in idx:
            lo_, hi_ = ws[i], ws[i+1]
            flo = f[i]
            for _ in range(100):
                m = 0.5*(lo_+hi_)
                fm = np.sort(np.abs(zs(m,g)))[k]-1
                if np.sign(fm) == np.sign(flo): lo_, flo = m, fm
                else: hi_ = m
            w = 0.5*(lo_+hi_)
            z = sorted(zs(w,g), key=abs)[k]
            th = -np.angle(z)
            taus = [(th + 2*np.pi*kk)/w for kk in range(-2,4)]
            taus = sorted(t for t in taus if t > 0)
            out.append((w, z, taus))
    return out

for g in [1.0, 3.0]:
    print(f"\n=== g = {g}: imaginary-axis crossings ===")
    cr = crossings(g)
    allt = []
    for w, z, taus in cr:
        # crossing direction: sign of Re(ds/dtau) at s = i w
        dirs = []
        for t in taus[:3]:
            s = 1j*w
            e = np.exp(-s*t)
            dDds = (3*s**2 + 2*s*(a+b+d) + (a*b+a*d+b*d)) + h*g*e - h*g*(s+b)*t*e - c*g*g*e**2 + 2*c*g*g*(s+d)*t*e**2
            dDdt = -h*g*(s+b)*s*e + 2*c*g*g*(s+d)*s*e**2
            dsdt = -dDdt/dDds
            dirs.append((round(t,5), np.sign(dsdt.real), abs(Dfun(s,g,t))))
            allt.append((t, w, np.sign(dsdt.real)))
        print(f"w = {w:.6f}, |z| = {abs(z):.12f}, taus/direction/|D|: {dirs}")
    allt.sort()
    print("smallest crossing tau:", allt[0])
