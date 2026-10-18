# Periodic Navier-Stokes, the field v = u_0 = (sin y, sin z, cos x - cos(x+y)): exact (Fraction)
# Fourier expansion of |v|^2, |omega|^2, |grad omega|^2, omega.(grad v)omega and |grad v|^2.
# Prints the constant term, the number of modes, and the mode list in the form used in the
# proof of quantities_v (WyrdMathlib/PeriodicNS/Averages.lean).
# Run from this folder: python3 -I quantities_v_modes.py   (standard library only, <1 s)
# Formerly numerics/_raw/fourier.py.

from fractions import Fraction as Fr
from collections import defaultdict
# complex numbers as (re, im) fractions
def cmul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cadd(a,b): return (a[0]+b[0], a[1]+b[1])
class T:
    def __init__(s, d=None): s.d = {k:v for k,v in (d or {}).items() if v!=(0,0)}
    def __add__(s,o):
        o = o if isinstance(o,T) else const(o)
        d=defaultdict(lambda:(Fr(0),Fr(0)))
        for k,v in s.d.items(): d[k]=cadd(d[k],v)
        for k,v in o.d.items(): d[k]=cadd(d[k],v)
        return T(d)
    __radd__=__add__
    def __neg__(s): return T({k:(-v[0],-v[1]) for k,v in s.d.items()})
    def __sub__(s,o): return s+(-(o if isinstance(o,T) else const(o)))
    def __rsub__(s,o): return const(o)-s
    def __mul__(s,o):
        o = o if isinstance(o,T) else const(o)
        d=defaultdict(lambda:(Fr(0),Fr(0)))
        for k1,v1 in s.d.items():
            for k2,v2 in o.d.items():
                k=tuple(a+b for a,b in zip(k1,k2)); d[k]=cadd(d[k],cmul(v1,v2))
        return T(d)
    __rmul__=__mul__
    def __pow__(s,n):
        r=const(1)
        for _ in range(n): r=r*s
        return r
def const(c): return T({(0,0,0):(Fr(c),Fr(0))})
def cos(k):
    m=tuple(-a for a in k); h=Fr(1,2)
    if k==m: return const(1)
    return T({k:(h,Fr(0)), m:(h,Fr(0))})
def sin(k):
    m=tuple(-a for a in k); h=Fr(1,2)
    # (e^{ik}-e^{-ik})/(2i) = -i/2 e^{ik} + i/2 e^{-ik}
    if k==m: return const(0)
    return T({k:(Fr(0),-h), m:(Fr(0),h)})
def canon(k):
    for a in k:
        if a>0: return True
        if a<0: return False
    return True
def lean(f):
    out=[]
    for k in sorted(f.d):
        if not canon(k): continue
        c=f.d[k]
        if k==(0,0,0):
            assert c[1]==0; a,b=c[0],Fr(0)
        else:
            a,b=2*c[0],-2*c[1]
        def s(x): 
            if x.denominator==1: return f"{x.numerator}" if x>=0 else f"({x.numerator})"
            return f"({x.numerator}/{x.denominator})" 
        def si(x): return f"{x}" if x>=0 else f"({x})"
        out.append(f"({s(a)}, {s(b)}, {si(k[0])}, {si(k[1])}, {si(k[2])})")
    return "[" + ", ".join(out) + "]"
X=(1,0,0);Y=(0,1,0);Z=(0,0,1);XY=(1,1,0)
sx,cx,sy,cy,sz,cz,sxy,cxy=sin(X),cos(X),sin(Y),cos(Y),sin(Z),cos(Z),sin(XY),cos(XY)
energy = sy**2 + sz**2 + (cx-cxy)**2
w1=sxy-cz; w2=sx-sxy; w3=-cy
ens = w1**2+w2**2+w3**2
palin = cxy**2 + cxy**2 + sz**2 + (cx-cxy)**2 + (-cxy)**2 + sy**2
J=[[const(0),cy,const(0)],[const(0),const(0),cz],[-sx+sxy, sxy, const(0)]]
w=[w1,w2,w3]
st = const(0)
for i in range(3):
    st = st + w[i]*(J[i][0]*w[0]+J[i][1]*w[1]+J[i][2]*w[2])
grad = cy**2 + cz**2 + (-sx+sxy)**2 + sxy**2
for name,f in [("energy",energy),("ens",ens),("palin",palin),("st",st),("grad",grad)]:
    print(name, f.d.get((0,0,0)), len([k for k in f.d if canon(k)]))
    print(lean(f))
