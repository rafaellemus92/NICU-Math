# Shared Air, delayed linearisation: Chebyshev pseudospectral collocation of the delay
# generator (method 2 of 3, independent of the crossing analysis).
# Checks: convergence of the rightmost eigenvalues in N, residual |D(lambda)|, and the critical
# delay tau_c (bisection on the rightmost real part) for g = 3 and g = 1 at N = 20, 40, 60.
# Run from this folder: python3 -I delay_chebyshev_xcheck.py   (numpy only, ~5 s)
# Formerly numerics/_raw/delay-xcheck/cheb.py.

import numpy as np
a, b, d, c, h = 1/30, 1/20, 1/4, 1/250, 3/40
r, q = 1/25, 1/10

def cheb(N):
    # Trefethen's cheb: nodes x_j = cos(pi j/N), j=0..N, x_0 = 1
    x = np.cos(np.pi*np.arange(N+1)/N)
    cc = np.hstack([2, np.ones(N-1), 2]) * (-1)**np.arange(N+1)
    X = np.tile(x, (N+1,1)).T
    dX = X - X.T
    Dm = np.outer(cc, 1/cc) / (dX + np.eye(N+1))
    Dm = Dm - np.diag(Dm.sum(axis=1))
    return Dm, x

def generator(g, tau, N):
    A0 = np.array([[-a,0,-1],[0,-b,0],[0,0,-d]], float)
    A1 = np.array([[0,r*g,0],[q*g,0,0],[h*g,0,0]], float)
    Dm, x = cheb(N)           # theta = tau*(x-1)/2 in [-tau, 0]; x=1 -> theta=0, x=-1 -> theta=-tau
    Dm = Dm * (2/tau)
    n = 3
    M = np.kron(Dm, np.eye(n))   # rows j=1..N: u'(theta_j)
    # row block j=0 (theta=0): u'(0) = A0 u(0) + A1 u(-tau)
    M[0:n,:] = 0
    M[0:n,0:n] = A0
    M[0:n,N*n:(N+1)*n] += A1
    return M

def rightmost(g, tau, N=40, k=4):
    ev = np.linalg.eigvals(generator(g, tau, N))
    ev = ev[np.argsort(-ev.real)]
    return ev[:k]

def Dfun(s, g, tau):
    e = np.exp(-s*tau)
    return (s+a)*(s+b)*(s+d) + h*g*(s+b)*e - c*g**2*(s+d)*e**2

print("Convergence check, g=3 tau=2, rightmost eigenvalues vs N:")
for N in [10, 20, 30, 40, 60]:
    ev = rightmost(3, 2, N, 3)
    print(N, np.round(ev, 8))
ev = rightmost(3, 2, 40, 3)
print("|D(lambda)| residual at N=40:", [abs(Dfun(l,3,2)) for l in ev])

def max_re(g, tau, N=40):
    return rightmost(g, tau, N, 1)[0].real

for g, tlo, thi in [(3, 1.0, 2.5), (1, 3.0, 6.0)]:
    # scan then bisect on max real part of generator spectrum
    ts = np.linspace(tlo, thi, 31)
    vals = [max_re(g, t) for t in ts]
    i = next(i for i in range(len(ts)-1) if vals[i] < 0 <= vals[i+1])
    lo, hi = ts[i], ts[i+1]
    for _ in range(50):
        m = 0.5*(lo+hi)
        if max_re(g, m) < 0: lo = m
        else: hi = m
    ev = rightmost(g, 0.5*(lo+hi), 40, 2)
    print(f"g={g}: tau scan max Re: {[round(v,5) for v in vals[::5]]}")
    print(f"g={g}: critical tau (pseudospectral, N=40) = {0.5*(lo+hi):.6f}, rightmost there: {np.round(ev,6)}")
    for N in [20, 60]:
        lo2, hi2 = lo-0.01, hi+0.01
        for _ in range(50):
            m = 0.5*(lo2+hi2)
            if max_re(g, m, N) < 0: lo2 = m
            else: hi2 = m
        print(f"   N={N}: critical tau = {0.5*(lo2+hi2):.6f}")

# monotonic check: stable for all tau in (0, tau_c)?
for g in [1, 3]:
    ts = np.linspace(0.01, 6 if g==1 else 2.5, 120)
    mr = np.array([max_re(g,t) for t in ts])
    first = ts[np.argmax(mr >= 0)] if (mr>=0).any() else None
    print(f"g={g}: max Re on (0,tau) grid stays negative until tau ~ {first}; max Re at tau=0.01: {mr[0]:.5f}")
