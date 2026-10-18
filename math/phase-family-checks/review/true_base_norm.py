"""Solve the exact 1D base equation V_t = nu V_yy - i a e^{-nu t} sin(y) V,
V(0)=c - d e^{i(y+phi)} (Fourier in y, RK4), for a=c=d=1, nu=1/28, several phi.
Report: (i) true sup_t ||V(t)||_{*,m}/||V(0)||_{*,m} vs appendix exp(L|a|/nu);
(ii) true integral int_0^T ||U(t)||_m dt (phase max) vs appendix C_base/nu, for
m=5 (s=4) and m=9 (R=8). Also a mode-count convergence check (Nn=96 vs 128).
This quantifies the slack in the appendix's explicit majorant; it is NOT part of
the proof and does not certify anything."""
import numpy as np, math, sys, time
a = c = d = 1.0
nu = 1.0/28.0
T = float(sys.argv[1]) if len(sys.argv) > 1 else 800.0
phis = np.linspace(0, 2*np.pi, 8, endpoint=False)
ms = [5, 9]

def run(Nn, dt):
    n = np.arange(-Nn, Nn+1)
    V = np.zeros((len(n), len(phis)), dtype=complex)
    V[n == 0, :] = c
    V[n == 1, :] = -d*np.exp(1j*phis)
    W0 = {m: np.sqrt(np.sum((2.0+n*n)[:, None]**m*abs(V)**2, axis=0)) for m in ms}
    diff = -nu*(n*n)[:, None]
    def sinmul(X):  # (sin y X)_n = (X_{n-1}-X_{n+1})/(2i)
        out = np.zeros_like(X)
        out[1:] += X[:-1]
        out[:-1] -= X[1:]
        return out/(2j)
    def rhs(t, X):
        return diff*X - 1j*a*math.exp(-nu*t)*sinmul(X)
    steps = int(round(T/dt)); t = 0.0
    rec_t = [0.0]
    rec_norm = {m: [np.sqrt(np.sum((2.0+n*n)[:, None]**m*abs(V)**2, axis=0))] for m in ms}
    every = max(1, int(round(0.25/dt)))
    for k in range(1, steps+1):
        k1 = rhs(t, V); k2 = rhs(t+dt/2, V+dt*k1/2); k3 = rhs(t+dt/2, V+dt*k2/2); k4 = rhs(t+dt, V+dt*k3)
        V = V + dt*(k1+2*k2+2*k3+k4)/6; t += dt
        if k % every == 0:
            rec_t.append(t)
            for m in ms:
                rec_norm[m].append(np.sqrt(np.sum((2.0+n*n)[:, None]**m*abs(V)**2, axis=0)))
    rec_t = np.array(rec_t)
    out = {}
    for m in ms:
        Vn = np.array(rec_norm[m])                      # (nt, nphi)
        Un = np.sqrt((2.0**m*a*a*np.exp(-2*nu*rec_t)[:, None] + np.exp(-2*nu*rec_t)[:, None]*Vn**2)/2)
        integral = np.trapezoid(Un, rec_t, axis=0)      # per phase
        tail = Un[-1]/nu                                  # crude tail bound (decays like e^{-nu t})
        out[m] = dict(growth=(Vn/W0[m][None, :]).max(axis=0), integral=integral, tail=tail,
                      U0=Un[0], supU=Un.max(axis=0), tmax=rec_t[Un.argmax(axis=0)])
    # spectral tail check: energy in the top 10% of modes relative to total, max over time is not recorded; report final
    return out, V, n

t0 = time.time()
res96, V96, n96 = run(96, 0.004)
print(f"Nn=96 done in {time.time()-t0:.1f}s")
t0 = time.time()
res128, V128, n128 = run(128, 0.0025)
print(f"Nn=128 done in {time.time()-t0:.1f}s")
for m in ms:
    L = 2**(m/2)
    print(f"\n=== m={m} ===")
    for lab, r in [("Nn=96", res96[m]), ("Nn=128", res128[m])]:
        print(f"[{lab}] phase-max sup_t ||V||_*/||V(0)||_* = {r['growth'].max():.6g}  (appendix bound exp(L|a|/nu) = 10^{(L/nu)/math.log(10):.1f})")
        print(f"[{lab}] ||U(0)||_m = {r['U0'][0]:.6g};  phase-max sup_t ||U(t)||_m = {r['supU'].max():.6g} at t~{r['tmax'][r['supU'].argmax()]:.2f}")
        print(f"[{lab}] phase-max int_0^T ||U||_m dt = {r['integral'].max():.6g} (+ tail <= {r['tail'].max():.3g}); per-phase: {np.array2string(r['integral'], precision=4)}")
    # appendix C_base/nu
    log10_exp = (2*L/nu)/math.log(10)
    log10_Cb = 0.5*(log10_exp + math.log10(2**m*c*c+3**m*d*d) - math.log10(2))  # a^2 term negligible
    print(f"appendix C_base/nu = 10^{log10_Cb - math.log10(nu):.2f}; so true (A/K)=int M is smaller by a factor 10^{log10_Cb - math.log10(nu) - math.log10(res128[m]['integral'].max()):.1f}")
