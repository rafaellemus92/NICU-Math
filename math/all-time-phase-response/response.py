"""Coefficient variations in b; reuse the repository's strict-dealiased NS solver.
No random numbers. Fourier coefficients and all averages are volume-normalized.
"""
import importlib.util
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_ns', ROOT / 'ns-phase-audit/audit_v2/dns/ns.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class Response(audit.NS):
    """U,b*q1,b**2*q2 coefficients (q2 is half the second derivative)."""
    def initial(self, phi, a=1., c=1., d=1.):
        U = self.init_family(phi, a=a, b=0., c=c, d=d)
        f = self.init_family(0., a=0., b=1., c=0., d=0.)
        return np.stack([U, f, np.zeros_like(U)])

    def rhs(self, Y):
        g = self.g
        u = [g.inv(v) for v in Y]
        w = [g.inv(g.curl_h(v)) for v in Y]
        return np.stack([g.proj(g.fwd(sum(np.cross(u[j], w[n-j], axis=0)
                          for j in range(n+1)))) - self.visc * Y[n]
                         for n in range(3)])

    def tri(self, v, w, u):
        """T(v,w,u) = <curl(v)_i curl(w)_j partial_j u_i>."""
        g = self.g
        cv, cw = g.inv(g.curl_h(v)), g.inv(g.curl_h(w))
        return sum(float(np.mean(cv[i]*cw[j]*g.inv(1j*g.kvec[j]*u[i])))
                   for i in range(3) for j in range(3))

    def quantities(self, u):
        return np.array([self.g.energy(u), self.g.enstrophy(u), self.tri(u,u,u)])

    def second(self, Y):
        U, q1, q2 = Y
        g = self.g
        E = g.inner(U,q2) + .5*g.inner(q1,q1)
        W, w1, w2 = [g.curl_h(v) for v in Y]
        Z = g.inner(W,w2) + .5*g.inner(w1,w1)
        S = sum(self.tri(Y[i],Y[j],Y[2-i-j]) for i in range(3) for j in range(3-i))
        return np.array([E,Z,S])


def integrate(solver, state, T, dt):
    if not np.isfinite(T) or not np.isfinite(dt) or T < 0 or dt <= 0:
        raise ValueError('require finite T >= 0 and dt > 0')
    steps = int(np.ceil(T/dt))
    if steps:
        for _ in range(steps):
            state = solver.step(state,T/steps)
    if not np.isfinite(state).all():
        raise FloatingPointError('nonfinite integration')
    return state


def harmonics(values):
    """Return m=0,1,2,3 cosine/sine estimates, not infinite-series exactness."""
    p = 2*np.pi*np.arange(len(values))/len(values)
    return {str(m): {'cos': ((1 if m==0 else 2)*np.mean(values*np.cos(m*p)[:,None],axis=0)).tolist(),
                     'sin': (2*np.mean(values*np.sin(m*p)[:,None],axis=0)).tolist()}
            for m in range(4)}
