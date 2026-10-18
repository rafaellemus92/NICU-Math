import json, numpy as np
from common import *
d=json.load(open('out/fullsolve_extrap.json'))['small_T_jet']; j=json.load(open('out/jet_t7.json'))
Ts=np.array([float(t) for t in d]); r=np.array([d[t]['ratio_to_leading'] for t in d])
# fit ratio-1 = a T + b T^2 + c T^3 (3 params, 4 points, least squares)
A=np.vstack([Ts,Ts**2,Ts**3]).T; coef=np.linalg.lstsq(A,r-1,rcond=None)[0]
out={'fit_c7/c6,c8/c6,c9/c6_from_dt=T/10_or_.01':coef.tolist(),'exact_c7/c6':j['c7/c6'],'exact_c8/c6':j['c8/c6']}
# dt-refinement at small T, N=24, 12 phases
nu=NU; M=12; phases=2*np.pi*np.arange(M)/M; lead=-6487/1555200
resp=Response(24,nu); res={}
for T in [.05,.1]:
    for dt in [T/10,T/40]:
        s=np.array([resp.second(integrate(resp,resp.initial(p),T,dt)) for p in phases])
        res[f'T{T}_dt{dt:.5f}']=float(harm_cos(s,2)[1]/T**6/lead)
out['dt_refinement_ratio_to_leading']=res
Ts2=np.array([.05,.1]); r2=np.array([res[f'T{T}_dt{T/40:.5f}'] for T in Ts2])
# with exact c7 known, infer c8/c6 from refined points: (r-1-c7 T)/T^2
out['inferred_c8/c6_from_refined_dt']=((r2-1-j['c7/c6']*Ts2)/Ts2**2).tolist()
print(json.dumps(out,indent=1)); json.dump(out,open('out/jet_fit.json','w'),indent=1)
