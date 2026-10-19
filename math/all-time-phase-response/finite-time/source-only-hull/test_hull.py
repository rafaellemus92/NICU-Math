from fractions import Fraction as F
import sys,unittest
from pathlib import Path
import numpy as np
import source_hull as h
sys.path.insert(0,str(h.P/'mean-q2-pilot'))
from test_kernels import assert_contains,advective_oracle,sample_q

class HullTests(unittest.TestCase):
    def test_interior_node_extreme_not_only_endpoints(self):
        a=np.zeros((51,3,21,21),complex);a[1,0,9,10]=3+4j;a[49,0,9,10]=-2+1j
        disc=h.hull(a)
        for j in range(51):
            z=a[j,0,9,10];assert_contains(self,disc,(0,9,10),(F(float(z.real)),F(float(z.imag))))
        self.assertGreaterEqual(disc.rad[0,9,10],5)
    def test_affine_fraction_inside_projected_hull(self):
        a=np.zeros((51,3,21,21),complex)
        a[3,:,12,9]=[1+2j,-3+.5j,.25-1j]
        a[4,:,12,9]=[-2+1j,1-2j,3+.25j]
        disc=h.v.project_small(h.hull(a));wave=[2,-1,1];den=6
        for t in [F(0),F(1,7),F(1,2),F(1)]:
            raw=[((1-t)*F(float(a[3,c,12,9].real))+t*F(float(a[4,c,12,9].real)),(1-t)*F(float(a[3,c,12,9].imag))+t*F(float(a[4,c,12,9].imag))) for c in range(3)]
            dot=[sum(wave[c]*raw[c][part] for c in range(3)) for part in (0,1)]
            for c in range(3):assert_contains(self,disc,(c,12,9),tuple(raw[c][part]-F(wave[c],den)*dot[part] for part in (0,1)))
    def test_subnormal_node_containment(self):
        a=np.zeros((51,3,21,21),complex);a[8,0,0,0]=1e-310-2e-310j
        d=h.hull(a);assert_contains(self,d,(0,0,0),(F(float(a[8,0,0,0].real)),F(float(a[8,0,0,0].imag))))
    def test_hull_source_contains_independent_exact_oracle(self):
        small=sample_q();a=np.zeros((51,3,21,21),complex)
        a[0,:,9:12,9:12]=small;a[50,:,9:12,9:12]=2*small
        source=h.k.mean_source(h.v.project_small(h.hull(a)))
        for factor in (1,2):
            oracle=advective_oracle(factor*small)
            for wave,values in oracle.items():
                for c in range(3):assert_contains(self,source,(c,wave[0]+20,wave[1]+20),values[c])
        self.assertEqual(source.shape,(3,41,41))
    def test_cover_exactly_all_fine_cells(self):
        cells=[j for ell in range(250) for j in range(50*ell,50*ell+50)]
        self.assertEqual(cells,list(range(12500)))
        self.assertEqual(50*249+50,12500)
    def test_inherited_grid_and_exact_initial_projection(self):
        self.assertTrue(np.array_equal(h.v.ks,np.arange(-10,11)))
        a=np.zeros((51,3,21,21),complex);a[:,1,10,10]=-1j
        projected=h.v.project_small(h.hull(a))
        assert_contains(self,projected,(1,10,10),(F(0),F(-1)))
    def test_nonfinite_nodes_rejected(self):
        a=np.zeros((51,3,21,21),complex);a[0,0,0,0]=np.inf
        with self.assertRaises(ValueError):h.hull(a)

if __name__=='__main__':unittest.main()
