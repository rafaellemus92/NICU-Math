"""Extract the pure b^2 part of the exact-jet cos(2phi) enstrophy coefficients at t^6..t^8 (a=c=d=1), compare with response.py."""
import importlib.util, json, numpy as np
from fractions import Fraction as F
from common import PKG
spec=importlib.util.spec_from_file_location('exact_ns',PKG.parent/'ns-phase-audit/audit_v2/exact/nsseries.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
nu=F(1,28)
def ev(p): return sum(F(c)*nu**i for i,c in enumerate(p)) if p else F(0)
betas=[F(1),F(2),F(3),F(4)]
vals={}
for b in betas:
    U=mod.series(F(1),b,F(1),F(1),8,verbose=False); Z=mod.laurent_series(U,8)
    vals[b]={n:2*ev(Z[n].get(2)) for n in range(6,9)}
out={}
import sympy
for n in range(6,9):
    # Z[n][2](beta) = sum_k A_k beta^(2k), k=1..4 ; exact solve
    Mx=sympy.Matrix([[b**(2*k) for k in range(1,5)] for b in betas]); rhs=sympy.Matrix([sympy.Rational(vals[b][n].numerator,vals[b][n].denominator) for b in betas])
    sol=Mx.LUsolve(rhs)
    out[f't^{n}']={'b^2':str(sol[0]),'b^4':str(sol[1]),'b^6':str(sol[2]),'b^8':str(sol[3]),'b2_float':float(sol[0]),'b1_total_float':float(sum(sol))}
c6=out['t^6']['b2_float']; out['pure_b2_c7/c6']=out['t^7']['b2_float']/c6; out['pure_b2_c8/c6']=out['t^8']['b2_float']/c6
out['response_py_inferred_c8/c6_(dt=T/40)']=[-0.3613602687077603,-0.35019966404738717]
print(json.dumps(out,indent=1)); json.dump(out,open('out/jet_b2.json','w'),indent=1)
