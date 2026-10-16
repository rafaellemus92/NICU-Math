#!/usr/bin/env python3
"""Independent exact Taylor jet with viscosity kept as a FORMAL polynomial variable.

Written from scratch for the audit (does not import the package).
Rotational form: u_t = P(u x curl u) - nu |k|^2 u   (pressure + |u|^2/2 removed by P).
Taylor: U_n = (1/n) [ -nu|k|^2 U_{n-1} + P sum_{j=0}^{n-1} U_j x curl U_{n-1-j} ].
(The symmetric sum equals -P sum (U_j.grad)U_{n-1-j}.)
Keys: (k1,k2,k3,m) where m is the exponent of exp(i*phi).
Values: 3-vector of polynomials in nu; poly = dict power -> (re, im) Fractions.
[t^n] Z = 1/2 sum_j <curl U_j, curl U_{n-j}>, returned as {m: poly in nu}.
"""
from fractions import Fraction as Fr
import sys, time, json

ZERO = (Fr(0), Fr(0))

def cmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])

def padd_into(dst, src, scale=None):
    # dst += scale*src, scale complex or None
    for d, c in src.items():
        if scale is not None:
            c = cmul(c, scale)
        if d in dst:
            o = dst[d]; s = (o[0]+c[0], o[1]+c[1])
            if s[0] == 0 and s[1] == 0: del dst[d]
            else: dst[d] = s
        elif c[0] != 0 or c[1] != 0:
            dst[d] = c

def pmul(p, q):
    out = {}
    for d1, a in p.items():
        for d2, b in q.items():
            c = cmul(a, b); d = d1+d2
            if d in out:
                o = out[d]; out[d] = (o[0]+c[0], o[1]+c[1])
            else:
                out[d] = c
    return {d: c for d, c in out.items() if c[0] != 0 or c[1] != 0}

def pscale(p, s):
    return {d: cmul(c, s) for d, c in p.items() if not (c[0] == 0 and c[1] == 0)}

def vec_clean(v):
    return all(len(p) == 0 for p in v)

def initial_field():
    # u = (sin y, sin z, cos x - cos(x+y+phi)); sin(a) = (e^{ia}-e^{-ia})/(2i) ; cos(a)=(e^{ia}+e^{-ia})/2
    F = {}
    def put(key, comp, c):
        F.setdefault(key, [{}, {}, {}])
        padd_into(F[key][comp], {0: c})
    half = Fr(1, 2)
    put((0,1,0,0), 0, (Fr(0), -half)); put((0,-1,0,0), 0, (Fr(0), half))   # sin y
    put((0,0,1,0), 1, (Fr(0), -half)); put((0,0,-1,0), 1, (Fr(0), half))   # sin z
    put((1,0,0,0), 2, (half, Fr(0)));  put((-1,0,0,0), 2, (half, Fr(0)))    # cos x
    put((1,1,0,1), 2, (-half, Fr(0))); put((-1,-1,0,-1), 2, (-half, Fr(0))) # -cos(x+y+phi)
    return F

def curl(F):
    out = {}
    I = (Fr(0), Fr(1))
    for key, (a, b, c) in F.items():
        k1, k2, k3 = key[:3]
        # i k x u
        w0 = {}; padd_into(w0, c, (Fr(0), Fr(k2))); padd_into(w0, b, (Fr(0), Fr(-k3)))
        w1 = {}; padd_into(w1, a, (Fr(0), Fr(k3))); padd_into(w1, c, (Fr(0), Fr(-k1)))
        w2 = {}; padd_into(w2, b, (Fr(0), Fr(k1))); padd_into(w2, a, (Fr(0), Fr(-k2)))
        if w0 or w1 or w2:
            out[key] = [w0, w1, w2]
    return out

def cross_conv(A, B, acc):
    # acc += A x B (pointwise product in physical space -> convolution of Fourier keys)
    for ka, (a0, a1, a2) in A.items():
        for kb, (b0, b1, b2) in B.items():
            key = (ka[0]+kb[0], ka[1]+kb[1], ka[2]+kb[2], ka[3]+kb[3])
            if key[:3] == (0, 0, 0):
                continue  # mean mode is removed by P anyway (it is a gradient-free constant; P sets mean 0)
            tgt = acc.setdefault(key, [{}, {}, {}])
            if a1 and b2: padd_into(tgt[0], pmul(a1, b2))
            if a2 and b1: padd_into(tgt[0], pmul(a2, b1), (Fr(-1), Fr(0)))
            if a2 and b0: padd_into(tgt[1], pmul(a2, b0))
            if a0 and b2: padd_into(tgt[1], pmul(a0, b2), (Fr(-1), Fr(0)))
            if a0 and b1: padd_into(tgt[2], pmul(a0, b1))
            if a1 and b0: padd_into(tgt[2], pmul(a1, b0), (Fr(-1), Fr(0)))

def leray(acc):
    out = {}
    for key, v in acc.items():
        k = key[:3]; k2 = k[0]*k[0]+k[1]*k[1]+k[2]*k[2]
        if k2 == 0: continue
        dot = {}
        for i in range(3):
            if k[i]: padd_into(dot, v[i], (Fr(k[i]), Fr(0)))
        w = [dict(v[i]) for i in range(3)]
        if dot:
            for i in range(3):
                if k[i]: padd_into(w[i], dot, (Fr(-k[i], k2), Fr(0)))
        if any(w):
            out[key] = w
    return out

def jet(order):
    U = [initial_field()]; W = [curl(U[0])]; Z = []
    t0 = time.time()
    for n in range(order+1):
        if n:
            acc = {}
            for j in range(n):
                cross_conv(U[j], W[n-1-j], acc)
            new = leray(acc)
            # viscous: -nu |k|^2 U_{n-1}
            for key, v in U[n-1].items():
                k2 = sum(x*x for x in key[:3])
                tgt = new.setdefault(key, [{}, {}, {}])
                for i in range(3):
                    shifted = {d+1: c for d, c in v[i].items()}
                    padd_into(tgt[i], shifted, (Fr(-k2), Fr(0)))
            inv = (Fr(1, n), Fr(0))
            Un = {}
            for key, v in new.items():
                w = [pscale(p, inv) for p in v]
                if any(w): Un[key] = w
            U.append(Un); W.append(curl(Un))
        # [t^n] Z = 1/2 sum_j <W_j, W_{n-j}> ; mean of product -> pair keys with opposite spatial k
        z = {}
        for j in range(n+1):
            A = W[j]; B = W[n-j]
            byk = {}
            for kb, vb in B.items():
                byk.setdefault(kb[:3], []).append((kb[3], vb))
            for ka, va in A.items():
                for mb, vb in byk.get((-ka[0], -ka[1], -ka[2]), []):
                    M = ka[3]+mb
                    tgt = z.setdefault(M, {})
                    for i in range(3):
                        if va[i] and vb[i]:
                            padd_into(tgt, pmul(va[i], vb[i]), (Fr(1, 2), Fr(0)))
        z = {m: p for m, p in z.items() if p}
        Z.append(z)
        maxdeg = max((max(v[i].keys()) for v in U[n].values() for i in range(3) if v[i]), default=0)
        print(f"order {n}: keys={len(U[n])}, max nu-degree in U_n={maxdeg}, elapsed={time.time()-t0:.1f}s", flush=True)
    return U, Z

def fmt(p):
    terms = []
    for d in sorted(p):
        re, im = p[d]
        assert im == 0, ("imaginary Z coefficient", d, p[d])
        terms.append(f"({re})*nu^{d}")
    return " + ".join(terms) if terms else "0"

if __name__ == "__main__":
    order = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    U, Z = jet(order)
    out = {}
    for n, z in enumerate(Z):
        print(f"[t^{n}] Z, Laurent coefficients in exp(i m phi), as polynomials in nu:")
        for m in sorted(z):
            print(f"   m={m:+d}: {fmt(z[m])}")
        out[n] = {m: {d: [str(c[0]), str(c[1])] for d, c in z[m].items()} for m in z}
    json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "nu_poly_jet.json", "w"), indent=1)
