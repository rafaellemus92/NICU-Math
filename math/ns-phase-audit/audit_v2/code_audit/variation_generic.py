import sys, numpy as np
sys.path.insert(0, '../../periodic_ns_lab_v2')
from ns_solver import PeriodicNS, fft, ifft, cross
from phase_sensitivity import variation_rhs, objective
s = PeriodicNS(16)
rng = np.random.default_rng(5)
u, w, r = (s.project(fft(rng.normal(size=(3, 16, 16, 16)))) for _ in range(3))
state = np.stack((u, w, r))
rates = variation_rhs(s, state)
# curve c(e) = u + e w + e^2 r / 2 ; c' = w, c'' = r at e=0.  rhs quadratic => exact polynomial in e
def f(e): return s.rhs(u + e*w + 0.5*e*e*r)
h = 1e-3
d1 = (f(h) - f(-h))/(2*h); d2 = (f(h) - 2*f(0) + f(-h))/h**2
sc = np.max(np.abs(rates[1])), np.max(np.abs(rates[2]))
print("generic tangent RHS rel err:", np.max(np.abs(d1 - rates[1]))/sc[0], " second-variation RHS rel err:", np.max(np.abs(d2 - rates[2]))/sc[1])
# exact quadratic-structure check without FD: N(c(e)) for e in {-1,0,1,2} fits degree-4 polynomial; use exact coefficients
# objective formulas: Z(c(e)) = Z + e <om, eta> + e^2/2 (|eta|^2 + <om,zeta>) + O(e^3)
Zf = lambda v: 0.5*np.vdot(s.curl(v), s.curl(v)).real
o = objective(s, state)
g = (Zf(u + h*w + 0.5*h*h*r) - Zf(u - h*w + 0.5*h*h*r))/(2*h)
H = (Zf(u + h*w + 0.5*h*h*r) - 2*Zf(u) + Zf(u - h*w + 0.5*h*h*r))/h**2
print("objective dZ rel err:", abs(g - o['dZ_dphi'])/abs(o['dZ_dphi']), " d2Z rel err:", abs(H - o['d2Z_dphi2'])/abs(o['d2Z_dphi2']))
# Exact (degree-4 polynomial) extraction with 5-point stencils, step 1: no truncation error
F = {e: f(float(e)) for e in (-2, -1, 0, 1, 2)}
d1 = (F[-2] - 8*F[-1] + 8*F[1] - F[2])/12; d2 = (-F[-2] + 16*F[-1] - 30*F[0] + 16*F[1] - F[2])/12
print("EXACT-stencil tangent RHS rel err:", np.max(np.abs(d1 - rates[1]))/sc[0], " second-variation RHS rel err:", np.max(np.abs(d2 - rates[2]))/sc[1])
G = {e: Zf(u + e*w + 0.5*e*e*r) for e in (-2, -1, 0, 1, 2)}
g = (G[-2] - 8*G[-1] + 8*G[1] - G[2])/12; H = (-G[-2] + 16*G[-1] - 30*G[0] + 16*G[1] - G[2])/12
print("EXACT-stencil objective dZ rel err:", abs(g - o['dZ_dphi'])/abs(o['dZ_dphi']), " d2Z rel err:", abs(H - o['d2Z_dphi2'])/abs(o['d2Z_dphi2']))
