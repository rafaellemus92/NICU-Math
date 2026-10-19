"""Algebraic/adversarial tests; these do not certify the inherited PDE inputs."""
from fractions import Fraction as F
from decimal import Decimal
import random
import unittest
from mpmath import iv
from check import abel, majorant, decimal_end, stored


class Check(unittest.TestCase):
    def test_young_exact_coefficient_and_sharpness(self):
        nu=F(1,28)
        for a in (F(0),F(1,7),F(13,9)):
            for g in (F(0),F(1,5),a/(2*nu),F(9)):
                gap=nu*g*g+a*a/(4*nu)-a*g
                self.assertEqual(gap,nu*(g-a/(2*nu))**2)
                self.assertGreaterEqual(gap,0)
        # Multiplying half-energy inequality by 2 gives coefficient 1/(2nu).
        self.assertEqual(2/(4*nu),F(14))

    def test_abel_exact_prefixes_and_slack(self):
        rng=random.Random(81003)
        for _ in range(500):
            x=[F(rng.randrange(10),7) for _ in range(8)]
            w=[F(rng.randrange(20),3) for _ in range(8)]
            phi=majorant(w); s=[]; total=F(0)
            for v in x: total+=v; s.append(total)
            self.assertEqual(abel(phi,s),sum(p*v for p,v in zip(phi,x)))
            slack=[v+F(rng.randrange(50),13) for v in s]
            self.assertGreaterEqual(abel(phi,slack),sum(a*b for a,b in zip(w,x)))

    def test_cumulative_differencing_counterexample(self):
        # B are legitimate cumulative upper bounds, not actual cumulative integrals.
        x=[F(0),F(101)]; w=[F(1),F(2)]; B=[F(100),F(101)]
        wrong=w[0]*B[0]+w[1]*(B[1]-B[0])
        direct=sum(a*b for a,b in zip(w,x))
        self.assertLess(wrong,direct)
        self.assertEqual(abel(majorant(w),B),direct)
        with self.assertRaises(ValueError): abel(w,B)

    def test_inclusive_cell_weight_covers_source_time(self):
        rates=[iv.mpf('2'),iv.mpf('3')];dt=iv.mpf('0.1')
        # Source starts at the left edge: excluding its cell is definitely too small.
        exact=iv.exp((rates[0]+rates[1])*dt)
        excluded=iv.exp(rates[1]*dt)
        self.assertGreater(exact.a,excluded.b)

    def test_directed_decimal_serialization(self):
        for value in (iv.mpf(1)/3,-iv.mpf(1)/7,iv.mpf('1e-70')):
            lo=iv.mpf(decimal_end(value,False));hi=iv.mpf(decimal_end(value,True))
            self.assertLessEqual(lo.a,value.a)
            self.assertGreaterEqual(hi.b,value.b)
        self.assertLessEqual(F(Decimal(decimal_end(iv.mpf(1)/3,False))),F(1,3))
        self.assertGreaterEqual(F(Decimal(decimal_end(iv.mpf(1)/3,True))),F(1,3))

    def test_stored_upper_padding_and_lower_padding(self):
        self.assertGreater(stored('[1, 1]').a,iv.mpf(1).b)
        self.assertLess(stored('[1, 1]',False).b,iv.mpf(1).a)
        with self.assertRaises(AssertionError): stored('[1, 2]')


if __name__=='__main__': unittest.main()
