import importlib.util
import unittest
import subprocess
import sys
import tempfile
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from response import Response, audit, integrate, harmonics, ROOT

class VariationTests(unittest.TestCase):
    def test_initial_and_factorial_convention(self):
        s=Response(12); Y=s.initial(.43)
        np.testing.assert_allclose(s.second(Y),[.25,.25,0],atol=2e-15)
        ns=audit.NS(12); U,f,_=Y; h=.2
        second=(ns.rhs(U+h*f)+ns.rhs(U-h*f)-2*ns.rhs(U))/(2*h*h)
        np.testing.assert_allclose(s.rhs(Y)[2],second,atol=2e-14)
        Y=integrate(s,Y,.1,.01); U,f,q=Y
        second=(ns.rhs(U+h*f+h*h*q)+ns.rhs(U-h*f+h*h*q)-2*ns.rhs(U))/(2*h*h)
        np.testing.assert_allclose(second-h*h*ns.nonlin(q),s.rhs(Y)[2],atol=2e-14)

    def test_support_divergence_parity(self):
        s=Response(12); Y=integrate(s,s.initial(.7),.2,.01); g=s.g
        for j,(v,allowed) in enumerate(zip(Y,[[0],[1],[0,2]])):
            bad=~np.isin(g.kvec[2],allowed)
            self.assertLess(np.max(abs(v[:,bad])),2e-14)
            self.assertLess(np.max(abs(g.div_h(v))),2e-14)
            np.testing.assert_allclose(v*np.cos(np.pi*g.kvec[2]),(-1)**j*v,atol=2e-14)

    def test_base_reduction(self):
        s=Response(18); phi=.37; T=.2; dt=.005
        Y=integrate(s,s.initial(phi),T,dt); g=s.g
        n=g.N; k=np.fft.fftfreq(n)*n; y=2*np.pi*np.arange(n)/n
        mask=abs(k)<=g.K; W=np.fft.fft(1-np.exp(1j*(y+phi)))
        def rhs(t,w):
            return -s.nu*(k*k+1)*w-1j*np.exp(-s.nu*t)*np.fft.fft(np.sin(y)*np.fft.ifft(w))*mask
        for m in range(round(T/dt)):
            t=m*dt; k1=rhs(t,W); k2=rhs(t+dt/2,W+dt*k1/2)
            k3=rhs(t+dt/2,W+dt*k2/2); k4=rhs(t+dt,W+dt*k3)
            W+=dt*(k1+2*k2+2*k3+k4)/6
        X,Yg,Z=np.broadcast_arrays(g.X,g.Y,g.Z)
        physical=np.stack([np.exp(-s.nu*T)*np.sin(Yg),np.zeros_like(X),
                           np.real(np.exp(1j*X)*np.fft.ifft(W)[None,:,None])+np.zeros_like(Z)])
        np.testing.assert_allclose(g.inv(Y[0]),physical,atol=3e-12)

    def test_stretching_slots(self):
        s=Response(12); Y=integrate(s,s.initial(.4),.2,.01)
        U,f,q=Y; g=s.g; rhs=s.rhs(Y)
        zprime=g.inner(g.curl_h(rhs[0]),g.curl_h(q))+g.inner(g.curl_h(U),g.curl_h(rhs[2]))+g.inner(g.curl_h(f),g.curl_h(rhs[1]))
        D2=2*g.inner(g.k2*U,g.k2*q)+g.inner(g.k2*f,g.k2*f)
        self.assertAlmostEqual(s.second(Y)[2],zprime+s.nu*D2,places=13)
        hs=np.array([-3,-2,-1,0,1,2,3])*.1
        vals=np.array([s.quantities(U+h*f+h*h*q) for h in hs])
        coeff=np.polynomial.polynomial.polyfit(hs,vals,6)
        np.testing.assert_allclose(coeff[2],s.second(Y),atol=2e-12)

    def test_phase_aliasing(self):
        for M,expected in [(6,1),(8,0),(12,0)]:
            p=2*np.pi*np.arange(M)/M
            self.assertAlmostEqual(harmonics(np.cos(4*p)[:,None])['2']['cos'][0],expected,places=13)

    def test_all_reported_phase_components_checked(self):
        from pilot import phase_error
        a={str(m):{'cos':[0.,0.,0.],'sin':[0.,0.,0.]} for m in range(4)}
        b={str(m):{'cos':[0.,0.,0.],'sin':[0.,0.,0.]} for m in range(4)}
        b['3']['sin'][2]=.125
        self.assertEqual(phase_error(a,b),.125)

    def test_recheck_does_not_overwrite_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'saved.json'; source.write_text('preserve me')
            run=subprocess.run([sys.executable,str(Path(__file__).with_name('pilot.py')),
                '--recheck-saved',str(source),'--output',str(source)],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn('output must differ',run.stderr)
            self.assertEqual(source.read_text(),'preserve me')

    def test_bad_inputs(self):
        s=Response(12)
        with self.assertRaises(ValueError): integrate(s,s.initial(0),1,0)

class ExactJetTests(unittest.TestCase):
    def test_leading_cos2_general_amplitudes(self):
        spec=importlib.util.spec_from_file_location('exact_ns',ROOT/'ns-phase-audit/audit_v2/exact/nsseries.py')
        mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        for a,b,c,d in [(F(1),F(1),F(1),F(1)),(F(1,2),F(1,3),F(2),F(1,5))]:
            U=mod.series(a,b,c,d,6,verbose=False); Z=mod.laurent_series(U,6)
            for n in range(6): self.assertFalse(any(Z[n].get(2,[])))
            self.assertEqual(2*Z[6][2][0],-F(6487,1555200)*a*a*b*b*c*c*d*d)
            self.assertFalse(any(Z[6][2][1:]))

if __name__=='__main__': unittest.main()
