import json, time
from common import *
nu=NU; N=24; T=.5; dt=.01; M=12
t0=time.time()
ns=audit.NS(N,nu); resp=Response(N,nu)
phases=2*np.pi*np.arange(M)/M
out={}
# variational second-order coefficient at T=.5 (12 phases) -> compare to refined.json runs[-1]
sec=np.array([resp.second(integrate(resp,resp.initial(p),T,dt)) for p in phases])
out['variational_T0.5_cos2']=harm_cos(sec,2).tolist(); out['variational_T0.5_cos0']=harm_cos(sec,0).tolist()
out['variational_T0.5_cos1']=harm_cos(sec,1).tolist()
# full-solve central second differences at b=.025,.0125
cd={}
for b in [.025,.0125]:
    rows=[]
    for p in phases:
        U=integrate(ns,ns.init_family(p,b=0.),T,dt)
        up=integrate(ns,ns.init_family(p,b=b),T,dt); um=integrate(ns,ns.init_family(p,b=-b),T,dt)
        q=resp.quantities
        rows.append((q(up)+q(um)-2*q(U))/(2*b*b))
    rows=np.array(rows); cd[b]=rows
    out[f'central_b{b}_cos2']=harm_cos(rows,2).tolist(); out[f'central_b{b}_cos0']=harm_cos(rows,0).tolist()
    out[f'central_b{b}_cos1']=harm_cos(rows,1).tolist()
rich=(16*cd[.0125]-cd[.025])/15
out['richardson_cos2']=harm_cos(rich,2).tolist(); out['richardson_cos0']=harm_cos(rich,0).tolist(); out['richardson_cos1']=harm_cos(rich,1).tolist()
out['refined_json_runs[-1]_cos2']=[2.7902921411609993e-07,-5.285760791649367e-05,-0.0006056308722179558]
out['diff_richardson_minus_variational_cos2']=(np.array(out['richardson_cos2'])-np.array(out['variational_T0.5_cos2'])).tolist()
out['diff_richardson_minus_refinedjson_cos2']=(np.array(out['richardson_cos2'])-np.array(out['refined_json_runs[-1]_cos2'])).tolist()
out['max_abs_diff_variational_vs_richardson_allphases']=float(np.max(abs(rich-sec)))
# T=1 variational Z2 cos2 vs lab value -2.4148e-3 (N=24 and N=30)
for NN in [24,30]:
    r=Response(NN,nu)
    s1=np.array([r.second(integrate(r,r.initial(p),1.0,dt)) for p in phases])
    out[f'variational_T1_N{NN}_cos2']=harm_cos(s1,2).tolist()
    out[f'variational_T1_N{NN}_cos0']=harm_cos(s1,0).tolist()
out['lab_T1_Zcos2_over_b2']=-2.4148e-3
# small-T jet: Z2 cos2 / T^6 -> -6487/1555200 = -4.1712e-3 ?
lead=-6487/1555200
jet={}
for TT in [.05,.1,.2,.3]:
    s=np.array([resp.second(integrate(resp,resp.initial(p),TT,min(dt,TT/10))) for p in phases])
    c2=harm_cos(s,2)
    jet[TT]={'Z2cos2':float(c2[1]),'Z2cos2_over_T6':float(c2[1]/TT**6),'ratio_to_leading':float(c2[1]/TT**6/lead),'E2cos2':float(c2[0]),'S2cos2':float(c2[2])}
out['small_T_jet']=jet; out['leading_coeff']=lead
out['wall']=time.time()-t0
json.dump(out,open(str(OUT)+'/fullsolve_extrap.json','w'),indent=1)
print(json.dumps(out,indent=1))
