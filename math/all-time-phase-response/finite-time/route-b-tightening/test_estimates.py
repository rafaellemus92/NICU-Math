import unittest
from fractions import Fraction as F
from decimal import Decimal,localcontext
import evaluate as e
import time_refinement as t
I=e.I
class Checks(unittest.TestCase):
    def encloses_fraction(self,x,r):
        self.assertLessEqual(F(x.lo),r);self.assertGreaterEqual(F(x.hi),r)
    def test_exact_histogram_and_subtraction(self):
        hist=e.histogram(2)
        self.assertEqual(sum(hist.values()),124)
        self.assertEqual(hist[1],6)
        lam=100;C=F('4.06707921080')
        exact=C*C-sum((F(count*lam,n*n*(lam+n*n)) for n,count in hist.items()),F(0))
        with localcontext(e.c.TRAP): x=e.resolvent(hist,I.of(lam),I.of(str(C.numerator)+'/'+str(C.denominator)))
        self.encloses_fraction(x,exact)
    def test_zero_lambda_recovers_old_constant(self):
        with localcontext(e.c.TRAP):
            x=e.resolvent(e.histogram(2),I.of(0),I.of(4));self.assertEqual(x.hi,16)
    def test_increasing_cube_only_improves_majorant(self):
        with localcontext(e.c.TRAP):
            a=e.resolvent(e.histogram(1),I.of(100),I.of(4.1))
            b=e.resolvent(e.histogram(2),I.of(100),I.of(4.1))
        self.assertLess(b.hi,a.lo)
    def test_minkowski_improves_three_square_bound(self):
        # Independent exact Cauchy identity for integer component norm bounds.
        for a,b,c in [(2,3,5),(0,1,9),(3,3,3)]:
            self.assertEqual(3*(a*a+b*b+c*c)-(a+b+c)**2,(a-b)**2+(a-c)**2+(b-c)**2)
    def test_constant_energy_cap_integral(self):
        # K=0 fixes the min envelope identically zero, even with a positive forcing majorant.
        b={k:I.of(v['hi']) for k,v in e.old['bounds'].items()};b['nu']=I.of('1/28');b['K']=I.of(0)
        with localcontext(e.c.TRAP): iy,_,_=t.refine(b,n=4)
        self.assertEqual(iy.hi,0)
    def test_nested_right_sums_and_endpoint_cap(self):
        b={k:I.of(v['hi']) for k,v in e.old['bounds'].items()};b['nu']=I.of('1/28')
        with localcontext(e.c.TRAP):
            coarse,_,_=t.refine(b,n=8);fine,_,_=t.refine(b,n=16)
            final=t.energy_cap(b['T'],b);k2=b['K'].sq()
        self.assertLess(fine.hi,coarse.lo)
        self.assertLessEqual(final.hi,k2.hi)
    def test_exact_viscosity_reciprocal(self):
        with localcontext(e.c.TRAP): x=1/I.of('1/28')
        self.encloses_fraction(x,F(28))
    def test_source_only_sufficient_condition_exact(self):
        lower=F('0.28091')-F('1.8534')*F('1.9424')*F('0.05')
        self.assertGreater(lower,F('0.06230'))
        self.assertEqual(lower,F('0.100907792'))
if __name__=='__main__':unittest.main()
