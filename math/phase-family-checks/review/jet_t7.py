import importlib.util, json, time, numpy as np
from fractions import Fraction as F
from common import PKG
spec=importlib.util.spec_from_file_location('exact_ns',PKG.parent/'ns-phase-audit/audit_v2/exact/nsseries.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
t0=time.time(); U=mod.series(F(1),F(1),F(1),F(1),8,verbose=False); Z=mod.laurent_series(U,8); print('series time',time.time()-t0)
nu=F(1,28)
def ev(p): return float(sum(F(c)*nu**i for i,c in enumerate(p)))
out={}
for n in range(5,9):
    row=Z[n].get(2)
    out[f'Z_t^{n}_cos2_coeff_poly_in_nu']=[str(x) for x in row] if row else None
    out[f'Z_t^{n}_cos2_at_nu=1/28']=2*ev(row) if row else 0.0   # factor 2: cosine convention (laurent coeff of e^{2i phi} -> real cos amplitude)
c6=out['Z_t^6_cos2_at_nu=1/28']; c7=out['Z_t^7_cos2_at_nu=1/28']; c8=out['Z_t^8_cos2_at_nu=1/28']
out['c7/c6']=c7/c6; out['c8/c6']=c8/c6
# compare with response.py small-T data: ratio_to_leading(T) = 1 + (c7/c6) T + (c8/c6) T^2 + ...
d=json.load(open('out/fullsolve_extrap.json'))['small_T_jet']
for T,v in d.items():
    T=float(T); pred=1+c7/c6*T+c8/c6*T*T
    out[f'T={T}']={'measured_ratio':v['ratio_to_leading'],'pred_1+c7T+c8T2':pred,'pred_1+c7T':1+c7/c6*T}
print(json.dumps(out,indent=1)); json.dump(out,open('out/jet_t7.json','w'),indent=1)
