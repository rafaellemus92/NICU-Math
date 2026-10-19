"""Exact synthetic checks/structural tests, not a full-horizon PDE certificate."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
import unittest
import numpy as np
import kernels as k
v=k.v

def pair(z): return F(float(z.real)),F(float(z.imag))
def add(a,b): return a[0]+b[0],a[1]+b[1]
def mul(a,b): return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def sc(a,b): return a[0]*b,a[1]*b

def advective_oracle(Q):
    modes=[];mx=Q.shape[1]//2;my=Q.shape[2]//2
    for ix in range(Q.shape[1]):
        for iy in range(Q.shape[2]):
            if not np.any(Q[:,ix,iy]): continue
            a=[sc(pair(z),F(1,2)) for z in Q[:,ix,iy]]
            wave=(ix-mx,iy-my,1)
            modes += [(wave,a),(tuple(-x for x in wave),[(r,-i) for r,i in a])]
    out={}
    for p,a in modes:
        for q,b in modes:
            mode=tuple(p[j]+q[j] for j in range(3))
            if mode[2]: continue
            dot=(F(0),F(0))
            for j in range(3): dot=add(dot,sc(a[j],q[j]))
            src=[mul((-dot[1],dot[0]),z) for z in b]
            old=out.setdefault(mode,[(F(0),F(0)) for _ in range(3)])
            out[mode]=[add(old[j],src[j]) for j in range(3)]
    for wave,a in list(out.items()):
        norm=sum(x*x for x in wave)
        if norm:
            dot=(F(0),F(0))
            for j in range(3): dot=add(dot,sc(a[j],wave[j]))
            out[wave]=[add(a[j],sc(dot,-F(wave[j],norm))) for j in range(3)]
    return out

def assert_contains(test,disc,index,z):
    dr=F(float(disc.re[index]))-z[0];di=F(float(disc.im[index]))-z[1]
    test.assertLessEqual(dr*dr+di*di,F(float(disc.rad[index]))**2)

def sample_q():
    Q=np.zeros((3,3,3),complex)
    Q[:,2,2]=[0,1,-1] # k=(1,1,1)
    Q[:,0,1]=[1,0,1] # k=(-1,0,1)
    return Q

class KernelTests(unittest.TestCase):
    def test_real_factor_flux_vs_exact_advective_convolution_and_source_tail(self):
        Q=sample_q();source=k.mean_source(v.exact(Q));oracle=advective_oracle(Q)
        for ix in range(5):
            for iy in range(5):
                target=oracle.get((ix-2,iy-2,0),[(F(0),F(0))]*3)
                for c in range(3): assert_contains(self,source,(c,ix,iy),target[c])
        self.assertNotEqual(oracle[(2,1,0)][2],(0,0))
        self.assertGreater(abs(source.im[2,4,3]),source.rad[2,4,3])

    def test_initial_sin_z_source_is_exactly_zero_target(self):
        Q=np.zeros((3,3,3),complex);Q[1,1,1]=-1j
        source=k.mean_source(v.exact(Q))
        self.assertTrue(np.all(np.hypot(source.re,source.im)<=source.rad))
        self.assertTrue(np.all(source.rad[:,2,2]==0))

    def test_leray_zero_mode_preserved_for_force_removed_for_approximation(self):
        A=np.zeros((3,3,3),complex);A[:,1,1]=[1,2,3]
        force=k.project(v.exact(A));node=k.mean_node(A)
        np.testing.assert_array_equal(force.re[:,1,1],[1,2,3])
        np.testing.assert_array_equal(node.re[:,1,1],[0,0,0])
        self.assertTrue(np.all(node.rad[:,1,1]==0))

    def test_kz0_operator_has_no_vertical_advection(self):
        W=v.exact(np.array([1j,1,.5],complex))
        A=np.zeros((3,3,3),complex);A[2,1,2]=1;A[2,1,0]=1
        out=k.vertical_base(W,k.mean_node(A),2,2)
        self.assertTrue(np.all(np.hypot(out.re,out.im)<=out.rad))

    def test_base_product_tail_is_retained(self):
        W=np.zeros(5,complex);W[4]=1
        A=np.zeros((3,3,3),complex);A[0,1,2]=.5;A[0,1,0]=.5
        out=k.vertical_base(v.exact(W),k.mean_node(A),2,3)
        assert_contains(self,out,(2,3,6),(F(0),F(1,4))) # (kx,ky)=(1,3)
        self.assertGreater(abs(out.im[2,3,6]),out.rad[2,3,6])

    def test_shear_real_factor(self):
        A=np.zeros((3,3,3),complex);A[1,2,1]=.5;A[1,0,1]=.5
        out=k.shear(k.mean_node(A),2,2)
        assert_contains(self,out,(0,3,3),(F(1,4),F(0)))

    def test_affine_cell_polynomial_matches_direct_midpoint(self):
        Q0=v.exact(sample_q());Q1=v.cscale(Q0,1.125)
        W0=v.exact(np.array([.25j,1,.5],complex));W1=v.cscale(W0,.875)
        A=np.zeros((3,3,3),complex);A[0,1,2]=.125;A[0,1,0]=.125
        V0=k.mean_node(A);V1=v.cscale(V0,1.0625)
        with localcontext(k.TRAP):
            p=k.residual_polynomial(Q0,Q1,W0,W1,V0,V1,0,h_inv=8)
            mid=lambda a,b:v.cscale(v.cadd(a,b),.5)
            direct=k.direct_frozen(mid(Q0,Q1),mid(W0,W1),mid(V0,V1),v.cscale(v.csub(V1,V0),8),0,h_inv=8)
            tau=k.Iv.of('1/16')
            poly=v.cadd(p['R0'],v.cadd(k.scale_iv(p['R1'],tau),k.scale_iv(p['R2'],tau.sq())))
        self.assertTrue(np.all(np.hypot(poly.re-direct.re,poly.im-direct.im)<=poly.rad+direct.rad))

    def test_mean_norm_has_no_single_z_harmonic_half_factor(self):
        A=np.zeros((3,3,3),complex);A[0,1,2]=.5;A[0,1,0]=.5
        upper=v.wnorm_hi(k.mean_node(A),1,False)
        self.assertGreaterEqual(F(upper)**2,F(1,2))
        self.assertLess(upper,.708)

    def test_inherited_error_budget_and_initial_data_distinction(self):
        import json
        d=json.loads((k.HERE/'results/pilot.json').read_text())
        rb=json.loads((k.PARENT/'route-b-dissipation/results/bounds.review.json').read_text())['bounds']
        e=d['inherited_error_budget_coefficients']
        exact=F(1,4)*(F(rb['n1']['hi'])*F(rb['eps0']['hi'])+F(rb['p']['hi'])*F(rb['eps1']['hi']))
        self.assertLessEqual(F(e['q1_source_smooth_allowance']['lo']),exact)
        self.assertGreaterEqual(F(e['q1_source_smooth_allowance']['hi']),exact)
        for key,S in [('base_coefficient_times_sup_gradV','0.45864'),('base_coefficient_times_sup_V','0.58868')]:
            exact=F(1,4)*F('7.5438e-5')*F(S)
            self.assertLessEqual(F(e[key]['lo']),exact)
            self.assertGreaterEqual(F(e[key]['hi']),exact)
        self.assertEqual(Decimal(e['mean_initial_error']['hi']),0)
        self.assertGreater(Decimal(e['inherited_W_initial_error']['lo']),0)

    def test_frozen_exponential_correction(self):
        with localcontext() as ctx:
            ctx.prec=80;nu=Decimal(1)/28;h=Decimal(1)/50000
            exact=h-(1-(-nu*h).exp())/nu
        with localcontext(k.TRAP):
            bound=k.Iv.of('1/28')*k.Iv.of('1/50000').sq()/2
        self.assertGreater(exact,0);self.assertLessEqual(exact,bound.hi)

if __name__=='__main__': unittest.main()
