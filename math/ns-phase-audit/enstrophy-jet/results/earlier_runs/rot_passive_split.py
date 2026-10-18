"""Passive/back-reaction split of c[6, 2] in rotational form (RESULTS.md section 5).

RESULTS.md section 5 splits c[6, 2] = -6487/3110400 with the advective form -P[(a.grad) b]:
83.5% passive (the phase leaf d is only carried along by the phase-free flow). This script uses the
rotational form P[a x curl b] instead, with the same rule ("d never in the velocity slot"), in
exact rational arithmetic at nu = 0 (every m = 2 term at n = 6 is nu-free).

usage: python3 rot_passive_split.py      (a few seconds; output: rot_passive_split.log)
"""
from fractions import Fraction as Fr
from collections import defaultdict

# Complex rationals as (re, im) pairs of Fractions. Fields: dict (k, m) -> [vx, vy, vz].


def cmul(a, b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cadd(a, b): return (a[0]+b[0], a[1]+b[1])
Z = (Fr(0), Fr(0))
def cs(x, a): return (x*a[0], x*a[1])
I = (Fr(0), Fr(1))


def initial(al=1, be=1, ga=1, de=1, drop_d=False):
    al, be, ga, de = map(Fr, (al, be, ga, de))
    U = defaultdict(lambda: [Z, Z, Z])
    h = Fr(1, 2)
    U[((0,1,0),0)][0] = (Fr(0), -h*al); U[((0,-1,0),0)][0] = (Fr(0), h*al)
    U[((0,0,1),0)][1] = (Fr(0), -h*be); U[((0,0,-1),0)][1] = (Fr(0), h*be)
    U[((1,0,0),0)][2] = (h*ga, Fr(0)); U[((-1,0,0),0)][2] = (h*ga, Fr(0))
    if not drop_d:
        U[((1,1,0),1)][2] = (-h*de, Fr(0)); U[((-1,-1,0),-1)][2] = (-h*de, Fr(0))
    return dict(U)


def addf(F, G, sc=Fr(1)):
    for key, v in G.items():
        w = F.setdefault(key, [Z, Z, Z])
        for c in range(3): w[c] = cadd(w[c], cs(sc, v[c]))


def curl(k, u):
    # i k x u
    cx = cadd(cs(Fr(k[1]), u[2]), cs(Fr(-k[2]), u[1]))
    cy = cadd(cs(Fr(k[2]), u[0]), cs(Fr(-k[0]), u[2]))
    cz = cadd(cs(Fr(k[0]), u[1]), cs(Fr(-k[1]), u[0]))
    return [cmul(I, cx), cmul(I, cy), cmul(I, cz)]


def zpair(Uj, Ul, mt):
    """1/2 sum_k omega_j(k,m1) . omega_l(-k,m2), m1+m2=mt; returns dict k -> value (complex)"""
    out = defaultdict(lambda: Z)
    for (k, m1), a in Uj.items():
        kk = (-k[0], -k[1], -k[2])
        b = Ul.get((kk, mt - m1))
        if b is None: continue
        wa, wb = curl(k, a), curl(kk, b)
        s = Z
        for c in range(3): s = cadd(s, cmul(wa[c], wb[c]))
        out[(k, m1)] = cadd(out[(k, m1)], cs(Fr(1, 2), s))
    return out


def Brot(A, Bf):
    """P[a x curl b]  (rotational form; sum over ordered pairs equals the advective total)"""
    out = defaultdict(lambda: [Z, Z, Z])
    for (p, m1), a in A.items():
        for (q, m2), b in Bf.items():
            k = (p[0]+q[0], p[1]+q[1], p[2]+q[2])
            if k == (0,0,0): continue
            w = curl(q, b)
            cr = [cadd(cmul(a[1], w[2]), cs(Fr(-1), cmul(a[2], w[1]))),
                  cadd(cmul(a[2], w[0]), cs(Fr(-1), cmul(a[0], w[2]))),
                  cadd(cmul(a[0], w[1]), cs(Fr(-1), cmul(a[1], w[0])))]
            v = out[(k, m1+m2)]
            for c in range(3): v[c] = cadd(v[c], cr[c])
    res = {}
    for (k, m), v in out.items():
        k2 = sum(x*x for x in k); kv = Z
        for c in range(3): kv = cadd(kv, cs(Fr(k[c]), v[c]))
        w = [cadd(v[c], cs(Fr(-k[c], k2), kv)) for c in range(3)]
        if any(x != Z for x in w): res[(k, m)] = w
    return res


def jetr(nmax, U0, N=None, swap=False):
    U = [U0]
    for n in range(nmax):
        acc = {}
        for j in range(n+1):
            if N is None: addf(acc, Brot(U[j], U[n-j]))
            elif not swap: addf(acc, Brot(N[j], U[n-j]))   # d never in velocity slot
            else: addf(acc, Brot(U[j], N[n-j]))            # d never in vorticity slot
        U.append({k: [cs(Fr(1, n+1), x) for x in v] for k, v in acc.items()})
    return U


def z62(U):
    t = Z
    for j in range(7):
        for v in zpair(U[j], U[6-j], 2).values(): t = cadd(t, v)
    return t[0]


tot = z62(jetr(6, initial()))
N = jetr(6, initial(drop_d=True))
print("rot total", tot)
p1 = z62(jetr(6, initial(), N=N)); print("rot: d never in velocity slot", p1, float(p1/tot))
