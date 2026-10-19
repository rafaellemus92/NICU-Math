"""Algebraic/adversarial tests; these do not certify the inherited PDE inputs."""
from fractions import Fraction as F
from decimal import Decimal
import random
import unittest
from mpmath import iv
from check import abel, majorant, decimal_end, stored, inclusive_tail_weights


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

    def test_exact_toy_source_growth_and_source_cell_mutation(self):
        # Exact equation: x'=log(2)*(x+1), x(0)=0, t in [0,2].
        # Thus x(2)=3. Each unit cell has source mass log(2).
        # Represent integrated growth in units of log(2), so exp is exactly 2**r.
        # 2/3 < log(2) < 3/4: midpoint/trapezoid bounds on integral_1^2 1/t.
        rates=[F(1),F(1)]; dt=F(1)
        exp2=lambda exponent: F(2)**exponent.numerator if exponent.denominator==1 else None
        exact=F(3); source_lo=F(2,3); source_hi=F(3,4)
        def assert_covers(weights):
            # Even the lower bound on the proposed upper majorant exceeds x(2).
            self.assertGreaterEqual(sum(weights)*source_lo,exact)
        weights=inclusive_tail_weights(rates,dt,exp2)
        assert_covers(weights)
        # Mutation: store weight BEFORE adding the source cell's growth.
        tail=F(0); excluded=[None]*2
        for i in range(1,-1,-1):
            excluded[i]=exp2(tail)
            tail+=rates[i]*dt
        self.assertLess(sum(excluded)*source_hi,exact)
        with self.assertRaises(AssertionError): assert_covers(excluded)

    def test_weight_domain(self):
        for rates,dt in (([],F(1)),([F(-1)],F(1)),([F(1)],F(0))):
            with self.assertRaises(ValueError): inclusive_tail_weights(rates,dt)

    def test_interval_rate_guard(self):
        # mpmath returns None for an undecidable whole-interval comparison.
        self.assertIs(iv.mpf([-1,1]) < 0, None)
        for rate in (iv.mpf([-2,-1]),iv.mpf([-1,1])):
            with self.assertRaises(ValueError): inclusive_tail_weights([rate],iv.mpf(1))
        for rate in (iv.mpf(0),iv.mpf([0,1]),iv.mpf([1,2])):
            weight=inclusive_tail_weights([rate],iv.mpf(1))[0]
            self.assertGreaterEqual(weight.a,iv.mpf(1))
        self.assertEqual(inclusive_tail_weights([iv.mpf(0)],iv.mpf(1))[0],iv.mpf(1))
        for dt in (iv.mpf([-1,1]),iv.mpf(0),iv.mpf([-2,-1])):
            with self.assertRaises(ValueError): inclusive_tail_weights([iv.mpf(1)],dt)

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
