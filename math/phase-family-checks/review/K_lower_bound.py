"""Certified-from-below value of the energy constant K_s: any K_s satisfying the
three inequalities of PROOF.md section 2 must exceed the ratios computed here on
concrete trigonometric polynomials (exact products: N>3K dealiasing in ns.py).
Uses the package's reused solver (read before use) imported by path.
Ratios computed:  r3 = |<B(h,h),h>_s| / ||h||_s^3,
                  r2 = ||B(h,f)||_s / (||f||_{s+1} ||h||_s)   (truncated -> lower bound),
                  r1 = |<B(f,h),h>_s| / (||f||_{s+1} ||h||_s^2).
B(f,g)=P(f.grad g) = -P(f x curl g) + P grad(...) = -(rotational-form nonlinearity with u=f, omega=curl g)."""
import importlib.util, sys, numpy as np
nspath = sys.argv[1]
spec = importlib.util.spec_from_file_location('audit_ns', nspath)
audit = importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)

rng = np.random.default_rng(12345)
N = 24
ns = audit.NS(N, 1.0)
g = ns.g

def B(f, h):
    """P(f . grad h) in half-spectrum, from rotational form: f x curl h = -(f.grad)h + grad(f.h)-(h.grad)f ... use direct form instead."""
    fphys = g.inv(f)
    grad_h = [g.inv(1j*g.kvec[j]*h) for j in range(3)]   # (3 comps) per direction j
    adv = np.stack([sum(fphys[j]*grad_h[j][i] for j in range(3)) for i in range(3)])
    return g.proj(g.fwd(adv))

def snorm2(f, s):
    return float((g.w*(1+g.k2)**s*(abs(f)**2).sum(axis=0)).sum())
def sinner(f, h, s):
    return float((g.w*(1+g.k2)**s*(f.conj()*h).real.sum(axis=0)).sum())

def randfield():
    u = rng.standard_normal((3, N, N, N))
    return g.proj(g.fwd(u))

# sanity: B(h,h) == -nonlin(h) (rotational form) on the retained modes
h = randfield()
print("max|B(h,h) + nonlin(h)| =", float(abs(B(h, h)+ns.nonlin(h)).max()), "(should be ~1e-16 rel)")
# sanity: transport cancellation <B(f,h),h>_0 = 0 for div-free f
f = randfield()
print("<B(f,h),h>_0 / (||f|| ||h||^2) =", sinner(B(f, h), h, 0)/np.sqrt(snorm2(f, 0))/snorm2(h, 0), "(should be ~0)")

for s in [4, 8]:
    best = dict(r1=0, r2=0, r3=0)
    for trial in range(60):
        f = randfield(); h = randfield()
        # also try low-mode fields (where the ratios tend to be larger relative to the (1+k^2)^s weight)
        if trial % 2:
            lowmask = (abs(g.kvec) <= 2).all(axis=0)
            f = f*lowmask; h = h*lowmask
        nf1 = np.sqrt(snorm2(f, s+1)); nh = np.sqrt(snorm2(h, s))
        r3 = abs(sinner(B(h, h), h, s))/nh**3
        r2 = np.sqrt(snorm2(B(h, f), s))/(nf1*nh)
        r1 = abs(sinner(B(f, h), h, s))/(nf1*nh*nh)
        best = {k: max(best[k], v) for k, v in zip(['r1', 'r2', 'r3'], [r1, r2, r3])}
    # specific structured fields: the family itself and Taylor-Green-like
    U0 = ns.init_family(0.37, a=1, b=1, c=1, d=1)
    for hh, ff in [(U0, U0), (randfield(), U0), (U0, randfield())]:
        nf1 = np.sqrt(snorm2(ff, s+1)); nh = np.sqrt(snorm2(hh, s))
        best['r3'] = max(best['r3'], abs(sinner(B(hh, hh), hh, s))/nh**3)
        best['r2'] = max(best['r2'], np.sqrt(snorm2(B(hh, ff), s))/(nf1*nh))
        best['r1'] = max(best['r1'], abs(sinner(B(ff, hh), hh, s))/(nf1*nh*nh))
    print(f"s={s}: K_s must be >= max(r1,r2,r3) = {max(best.values()):.4f}   (r1={best['r1']:.4f}, r2={best['r2']:.4f}, r3={best['r3']:.4f})")
