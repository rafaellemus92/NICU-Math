"""Exact finite-Fourier algebra checks, not an evolution or PDE certificate."""
from fractions import Fraction as F
from dataclasses import dataclass
import unittest

@dataclass(frozen=True)
class C:
    r:F=F(0)
    i:F=F(0)
    def __add__(self,other):
        if not isinstance(other,C):other=C(F(other))
        return C(self.r+other.r,self.i+other.i)
    __radd__=__add__
    def __neg__(self):return C(-self.r,-self.i)
    def __sub__(self,other):return self+-other
    def __mul__(self,other):
        if not isinstance(other,C):other=C(F(other))
        return C(self.r*other.r-self.i*other.i,self.r*other.i+self.i*other.r)
    __rmul__=__mul__
    def conj(self):return C(self.r,-self.i)

I=C(F(0),F(1));ZERO=(C(),C(),C())
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(s,v):return tuple(s*x for x in v)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),C())
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def k2(k):return sum(x*x for x in k)
def inner(a,b):return sum((dot(v,tuple(x.conj() for x in b.get(k,ZERO))) for k,v in a.items()),C())
def curl(u):return {k:scale(I,cross(k,v)) for k,v in u.items()}
def adv(a,b):
    out={}
    for k,v in a.items():
        for l,w in b.items():
            m=tuple(x+y for x,y in zip(k,l))
            out[m]=add(out.get(m,ZERO),scale(I*dot(v,l),w))
    return out

def family(b,phase=(F(3,5),F(4,5))):
    # Exact phase fixture cos(phi),sin(phi); no claim it equals fixed phi=.37.
    a=c=d=F(1);cp,sp=phase
    modes={(0,1,0):(C(0,-a/2),C(),C()),
           (0,0,1):(C(),C(0,-b/2),C()),
           (1,0,0):(C(),C(),C(c/2)),
           (1,1,0):(C(),C(),C(-d*cp/2,-d*sp/2))}
    return {**modes,**{tuple(-x for x in k):tuple(x.conj() for x in v) for k,v in modes.items()}}

def diagnostics(u):
    omega=curl(u)
    Z=sum((k2(k)*dot(v,tuple(x.conj() for x in v)) for k,v in u.items()),C())*F(1,2)
    D=sum((k2(k)*dot(v,tuple(x.conj() for x in v)) for k,v in omega.items()),C())
    Q=inner(omega,adv(omega,u))
    return Z,D,Q

class Balance(unittest.TestCase):
    def test_initial_normalization_and_zero_excess(self):
        for phase in ((F(1),F(0)),(F(3,5),F(4,5))):
            U=family(F(0),phase);Z0,D0,Q0=diagnostics(U)
            for b in (F(3,1000),-F(3,1000),F(1,1000)):
                u=family(b,phase);Z,D,Q=diagnostics(u)
                self.assertTrue(all(dot(k,v)==C() for k,v in u.items()))
                self.assertEqual(Z-Z0,C(b*b/4))
                self.assertEqual(D-D0,C(b*b/2))
                self.assertEqual(Q-Q0,C())
                # Zdiff'-heat'=Qdiff-nu Ddiff+nu b²/2=0 initially.
                self.assertEqual(Q-Q0-(D-D0)*F(1,28)+C(b*b/56),C())
    def test_exact_enstrophy_balance_and_laplacian_norm(self):
        u=family(F(3,1000));Z,D,Q=diagnostics(u);nu=F(1,28)
        self.assertEqual(Q,C(F(3,20)))  # cos(phi)/4; nonzero detects reversed stretching sign.
        lap={k:scale(-k2(k),v) for k,v in u.items()}
        rhs=adv(u,u)
        pairing=-inner({k:scale(k2(k),v) for k,v in u.items()},rhs)-inner(lap,lap)*nu
        self.assertEqual(D,inner(lap,lap))
        self.assertEqual(pairing,Q-D*nu)
    def test_heat_baseline_symbolic_coefficients(self):
        # Coefficients of exp(-2nu t): Zheat=b²/4, Dheat=b²/2, Qheat=0.
        b=F(3,1000);nu=F(1,28)
        self.assertEqual(-2*nu*(b*b/4),-nu*(b*b/2))
        # Integrated heat dissipation coefficient of (1-exp(-2nu T)).
        self.assertEqual(nu*(b*b/2)/(2*nu),b*b/4)
    def test_positive_excess_does_not_fix_mechanism_signs(self):
        # S - nu R = H. These are logical scalar counterexamples, not NS realizations.
        nu=F(1,28)
        for S,weighted_R in ((F(-1),F(-2)),(F(2),F(1)),(F(1,2),F(-1,2))):
            R=weighted_R/nu
            self.assertEqual(S-nu*R,F(1))

if __name__=='__main__':unittest.main()
