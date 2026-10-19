"""Implementation checks, not a proof of the PDE estimates.
The Fourier-set test checks structural support arithmetic only.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import bounds as b

class BoundsTests(unittest.TestCase):
    def test_retained_w2_against_exact_rationals(self):
        nu,beta,C,M1,M2,n1,n2,K,N,sigma,eps,T,delta=map(F,
          ['1/28','3/1000','4','3','4','2','5','16','1/3','4/3','1/10000','1/4','1/10000000'])
        expected=8/nu*((2*M1+2*beta*n1)*K*K*T+2*beta*beta*C*C*K*K*delta/nu
                      +(M2+beta*n2)*N*K*T+4*(sigma*sigma*T+C*C*eps*eps*delta)/nu)
        with localcontext(b.TRAP):
            args=[b.Iv.of(str(x)) for x in (nu,beta,C,M1,M2,n1,n2,K,N,sigma,eps,T,delta)]
            actual=b.dissipation_bound(args[0],b.dissipation_terms(*args),b.Iv.of(0))
        self.assertLessEqual(F(actual.lo),expected)
        self.assertGreaterEqual(F(actual.hi),expected)

    def test_cell_initial_energy_without_forcing(self):
        # Y(t)=1-t, D²=4/nu saturates .5Y'+nu D²/8=0 on [0,1].
        # Omitting initial energy would incorrectly give zero dissipation.
        with localcontext(b.TRAP):
            nu=b.Iv.of('1/28');zero=b.Iv.of(0)
            cell=b.dissipation_bound(nu,{'rhs':zero},b.Iv.of(1))
            global_zero=b.dissipation_bound(nu,{'rhs':zero},zero)
        self.assertLessEqual(F(cell.lo),F(112))
        self.assertGreaterEqual(F(cell.hi),F(112))
        self.assertEqual(global_zero.hi,0)
        self.assertGreater(cell.lo,0)

    def test_linear_enclosures_against_80_digit_reference(self):
        for ts in ['0.001','0.1','0.25']:
            with localcontext() as ctx:
                ctx.prec=80
                M1,M2,nu,T,L,J=map(Decimal,['3','4','0.125',ts,'0.75','2'])
                N=((M1-nu)*T).exp()*L
                E2=((4*M1+1)*T).exp()*(M2*M2*N*N*T+J/nu)
                D=2/nu*((2*M1+Decimal('.5'))*E2*T+M2*M2*N*N*T/2+J/(2*nu))
                ref=[N,E2.sqrt(),D]
            with localcontext(b.TRAP):
                out=b.linear_bounds(*map(b.Iv.of,['3','4','0.125',ts,'0.75','2']))
            for iv,x in zip(out,ref):
                self.assertLessEqual(iv.lo,x)
                self.assertGreaterEqual(iv.hi,x)

    def test_fourier_cubic_cancellations_and_normalization(self):
        q1={-1,1};q2={x+y for x in q1 for y in q1}
        self.assertEqual(q2,{-2,0,2})
        mixed={x+y for x in q1 for y in q2}
        self.assertEqual(mixed,{-3,-1,1,3})
        self.assertNotIn(0,mixed)
        self.assertFalse(q1 & q2)
        # Normalized Parseval for sin(z); enstrophy has a further factor 1/2.
        self.assertEqual(2*F(1,2)**2,F(1,2))
        self.assertEqual(F(1,2)*2*F(1,2)**2,F(1,4))

    def test_tampered_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for name in b.PINNED:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(b.PARENT/name,p)
            b.verify_inputs(root)
            p=root/'absorption-b003/results/validated.json'
            p.write_bytes(p.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'Pinned input mismatch'):
                b.verify_inputs(root)

    def test_scope_mutations_fail_closed(self):
        import copy
        import json
        val=json.loads((b.PARENT/'absorption-b003/results/validated.json').read_text())
        old=json.loads((b.PARENT/'absorption-b003/results/chain.json').read_text())
        b.validate_scope(val,old)
        cases=[('parameters',key) for key in val['parameters']
               if key != 'source_sha256']
        cases += [('chain',key) for key in ('b','T','phi','verdict','numerics_kind',
                   'condition_A','condition_B1','condition_B2')]
        cases += [('provenance','complete'),('provenance','cells_validated'),('initial','eps0_0')]
        for section,key in cases:
            for missing in (False,True):
                with self.subTest(section=section,key=key,missing=missing):
                    v,o=copy.deepcopy(val),copy.deepcopy(old)
                    target=o if section=='chain' else v[section]
                    if missing: del target[key]
                    else: target[key]=None
                    with self.assertRaisesRegex(ValueError,'Certificate scope mismatch'):
                        b.validate_scope(v,o)
        for key in ('sup_absq','sup_absgradq','sup_abshessq','sup_gradq'):
            with self.subTest(short_array=key):
                v=copy.deepcopy(val);v['cells'][key].pop()
                with self.assertRaisesRegex(ValueError,'Certificate scope mismatch'):
                    b.validate_scope(v,old)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'existing.json';original=b'preserve prior evidence\n';p.write_bytes(original)
            run=subprocess.run([sys.executable,'-B',str(b.HERE/'bounds.py'),'--output',str(p)],
                               stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            self.assertNotEqual(run.returncode,0)
            self.assertIn(b'Refusing to overwrite',run.stderr)
            self.assertEqual(p.read_bytes(),original)

    def test_reproduction_and_all_display_rounding(self):
        import json
        saved=json.loads((b.HERE/'results/bounds.json').read_text());fresh=b.evaluate()
        for key in ('source_sha256', 'status'):
            saved.pop(key); fresh.pop(key)
        self.assertEqual(saved,fresh)  # All numerical/provenance inputs unchanged.
        for section in ['bounds','Dw_energy_terms','Jr_terms','mean_source_terms','CZ_terms']:
            for item in fresh[section].values():
                self.assertLessEqual(Decimal(item['lo']),Decimal(item['hi']))
                self.assertGreaterEqual(Decimal(item['upper_5sig']),Decimal(item['hi']))

if __name__=='__main__': unittest.main()
