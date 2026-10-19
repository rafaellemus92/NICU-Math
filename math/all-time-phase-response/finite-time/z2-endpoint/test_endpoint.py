"""Implementation/structural tests, not proof of the PDE certificates."""
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
import endpoint as e

class EndpointTests(unittest.TestCase):
    def test_initial_coefficient_is_one_quarter(self):
        Q=np.zeros((3,3,3),complex);Q[1,1,1]=-1j
        self.assertEqual(e.projected_gradient_squared(Q),F(1,2))
        with localcontext(e.TRAP):
            _,energy=e.energy_with_gradient_error(F(1,2),e.Iv.of(0))
        # q2(0)=0: Z2(0) is this energy, not zero.
        self.assertLessEqual(energy.lo,Decimal('0.25'))
        self.assertGreaterEqual(energy.hi,Decimal('0.25'))
        self.assertGreater(energy.lo,0)

    def test_parallel_mode_projects_to_zero(self):
        Q=np.zeros((3,3,3),complex);Q[:,2,0]=[1+2j,-1-2j,1+2j]
        self.assertEqual(e.projected_gradient_squared(Q),0)

    def test_projection_against_independent_rational_projector(self):
        Q=np.zeros((3,3,3),complex);Q[:,2,0]=[1+2j,-.5+.25j,3-1j]
        k=[1,-1,1];q=[e.components(z) for z in Q[:,2,0]]
        dr=sum(k[j]*q[j][0] for j in range(3))
        di=sum(k[j]*q[j][1] for j in range(3))
        pq=[(q[j][0]-F(k[j],3)*dr,q[j][1]-F(k[j],3)*di) for j in range(3)]
        expected=F(3,2)*sum(r*r+i*i for r,i in pq)
        self.assertEqual(e.projected_gradient_squared(Q),expected)

    def test_base_laplacian_normalization(self):
        W=np.zeros(3,complex);W[1]=1
        self.assertEqual(e.base_vertical_laplacian_squared(W),F(1,2))
        W[1]=0;W[2]=1
        self.assertEqual(e.base_vertical_laplacian_squared(W),F(2))

    def test_error_clips_lower_norm_before_squaring(self):
        with localcontext(e.TRAP):
            _,energy=e.energy_with_gradient_error(F(0),e.Iv.of('0.1'))
        self.assertEqual(energy.lo,0)
        self.assertGreaterEqual(energy.hi,Decimal('0.005'))

    def test_absolute_intervals_do_not_round_in_outer_context(self):
        for lo,hi,wantlo,wanthi in [('-1.234567','2.345678','0','2.345678'),
                                   ('-2.345678','-1.234567','1.234567','2.345678'),
                                   ('1.234567','2.345678','1.234567','2.345678')]:
            with localcontext(e.TRAP):
                got=e.absolute_interval(e.Iv(Decimal(lo),Decimal(hi)))
            self.assertEqual(got.lo,Decimal(wantlo));self.assertEqual(got.hi,Decimal(wanthi))

    def test_weight_ratio_factor_identity(self):
        for n in range(-6,7):
            x=F(n*n)
            self.assertEqual(4*(x+2)**3-27*(x+1)**2,(x-1)**2*(4*x+5))
            self.assertLessEqual((1+x)**2/(2+x)**3,F(4,27))

    def test_recorded_endpoint_energy_from_exact_fraction(self):
        d=json.loads((e.HERE/'results/endpoint.json').read_text())
        qsq=F(d['exact_endpoint_fractions']['projected_q_gradient_squared'])
        with localcontext(e.TRAP):
            _,energy=e.energy_with_gradient_error(qsq,e.Iv.of('5.6024e-5'))
        saved=d['bounds']['half_q1_gradient_squared']
        self.assertEqual(str(energy.lo),saved['lo']);self.assertEqual(str(energy.hi),saved['hi'])
        self.assertFalse(d['fixed_target_dominance_certified'])
        self.assertFalse(d['zero_excluded'])
        self.assertEqual(Decimal(d['bounds']['abs_Z2']['lo']),0)
        for val in d['bounds'].values():
            self.assertLessEqual(Decimal(val['display_lower']),Decimal(val['lo']))
            self.assertGreaterEqual(Decimal(val['display_upper']),Decimal(val['hi']))

    def test_output_preservation_before_array_access(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'saved.json';out.write_text('keep evidence')
            run=subprocess.run([sys.executable,'-B',str(e.HERE/'endpoint.py'),
                '--trajectory',str(Path(tmp)/'absent'),'--output',str(out)],capture_output=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn(b'Refusing to overwrite',run.stderr)
            self.assertEqual(out.read_text(),'keep evidence')

if __name__=='__main__': unittest.main()
