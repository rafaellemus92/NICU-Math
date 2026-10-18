# Periodic Navier-Stokes, phase family u_phi: exact (Fraction) Fourier expansion in (x, y, z, phi)
# of |u|^2, |omega|^2, |grad omega|^2 and omega.(grad u)omega. Prints the constant term and the
# mode list (a, b, kx, ky, kz) meaning a cos(k.x) + b sin(k.x), in the form used in the proof of
# quantities_vphi (WyrdMathlib/PeriodicNS/PhaseFamily.lean).
# Run from this folder: python3 -I phase_family_modes.py   (standard library only, <1 s)
# Formerly numerics/_raw/modes.py. phase_family_modes_check.py evaluates its output.

from fractions import Fraction as Fr
from collections import defaultdict
# trig poly: dict (kx,ky,kz,kphi) -> complex as (Fr re, Fr im)
def add(a,b):
    r=defaultdict(lambda:(Fr(0),Fr(0)))
    for d in (a,b):
        for k,v in d.items():
            o=r[k]; r[k]=(o[0]+v[0],o[1]+v[1])
    return {k:v for k,v in r.items() if v!=(0,0)}
def scal(c,a):
    return {k:(c*v[0],c*v[1]) for k,v in a.items()}
def sub(a,b): return add(a,scal(Fr(-1),b))
def mul(a,b):
    r=defaultdict(lambda:(Fr(0),Fr(0)))
    for k1,v1 in a.items():
        for k2,v2 in b.items():
            k=tuple(x+y for x,y in zip(k1,k2))
            re=v1[0]*v2[0]-v1[1]*v2[1]; im=v1[0]*v2[1]+v1[1]*v2[0]
            o=r[k]; r[k]=(o[0]+re,o[1]+im)
    return {k:v for k,v in r.items() if v!=(0,0)}
def cos(k):
    k=tuple(k); m=tuple(-x for x in k)
    if k==m: return {k:(Fr(1),Fr(0))}
    return {k:(Fr(1,2),Fr(0)), m:(Fr(1,2),Fr(0))}
def sin(k):
    # sin t = (e^{it}-e^{-it})/(2i) = -i/2 e^{it} + i/2 e^{-it}
    k=tuple(k); m=tuple(-x for x in k)
    if k==m: return {}
    return {k:(Fr(0),Fr(-1,2)), m:(Fr(0),Fr(1,2))}
def const(c): return {(0,0,0,0):(Fr(c),Fr(0))} if c!=0 else {}
X=(1,0,0,0);Y=(0,1,0,0);Z=(0,0,1,0);W=(1,1,0,1)
def fmt(c):
    c=Fr(c)
    if c.denominator==1: return str(c.numerator)
    return f"{c.numerator}/{c.denominator}"
def trigexpr(k4, kind):
    # returns list of (coef, string) for cos(k4 phi) or sin(k4 phi)
    if kind=='c':
        if k4==0: return "1"
        a=abs(k4)
        return "cos φ" if a==1 else f"cos ({a} * φ)"
    else:
        if k4==0: return None
        a=abs(k4); s = "sin φ" if a==1 else f"sin ({a} * φ)"
        return s if k4>0 else "-"+s  # sign handled outside
def lin(terms):
    # terms: list of (Fr coef, str or None)
    parts=[]
    for c,s in terms:
        if c==0 or s is None: continue
        neg = False
        if s.startswith('-'): s=s[1:]; c=-c
        if s=="1": parts.append(fmt(c) if True else "")
        else:
            if c==1: parts.append(s)
            elif c==-1: parts.append("-"+s)
            else: parts.append(f"{fmt(c)} * {s}")
    if not parts: return "0"
    e=parts[0]
    for p in parts[1:]:
        if p.startswith('-'): e+=" - "+p[1:]
        else: e+=" + "+p
    return e
def modes(f):
    groups=defaultdict(list)
    for k,v in f.items():
        K=k[:3]
        if K==(0,0,0): groups[K].append((k[3],v)); continue
        nz=[x for x in K if x!=0][0]
        if nz>0: groups[K].append((k[3],v))
    out=[]
    for K in sorted(groups, key=lambda K:(K!=(0,0,0),K)):
        ca=[];cb=[]
        for k4,(al,be) in groups[K]:
            if K==(0,0,0):
                ca.append((al,trigexpr(k4,'c'))); ca.append((-be,trigexpr(k4,'s')))
            else:
                ca.append((2*al,trigexpr(k4,'c'))); ca.append((-2*be,trigexpr(k4,'s')))
                cb.append((-2*al,trigexpr(k4,'s'))); cb.append((-2*be,trigexpr(k4,'c')))
        a=lin(ca); b=lin(cb) if K!=(0,0,0) else "0"
        if a=="0" and b=="0": continue
        out.append(f"({a}, {b}, {K[0]}, {K[1]}, {K[2]})")
    return "[" + ", ".join(out) + "]"
sx,cx=sin(X),cos(X); sy,cy=sin(Y),cos(Y); sz,cz=sin(Z),cos(Z); a,A=sin(W),cos(W)
sq=lambda t: mul(t,t)
energy = add(add(sq(sy),sq(sz)), sq(sub(cx,A)))
w1=sub(a,cz); w2=sub(sx,a); w3=scal(Fr(-1),cy)
enst = add(add(sq(w1),sq(w2)),sq(w3))
palin = add(add(add(add(sq(A),sq(A)),sq(sz)), add(sq(sub(cx,A)),sq(A))), sq(sy))
stretch = mul(mul(cy, sub(sx,a)), sub(a, scal(Fr(3),cz)))
for n,f in [("energy",energy),("enst",enst),("palin",palin),("stretch",stretch)]:
    print(n, f.get((0,0,0,0)), modes(f)); print()
