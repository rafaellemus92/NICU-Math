"""Raw remainder ratios at N=18,dt=.005,T=.5,phi=.37 for b=.1,.05,.025,.0125; roundoff floor estimates."""
import json
from common import *
nu=NU; N=18; T=.5; dt=.005; phi=.37
s=Response(N,nu); ns=audit.NS(N,nu)
Y=integrate(s,s.initial(phi),T,dt); Q0=s.quantities(Y[0]); Q2=s.second(Y)
U_full=integrate(ns,ns.init_family(phi,b=0.),T,dt)
out={'Q0_from_stack':Q0.tolist(),'Q0_from_fullsolve_b0':s.quantities(U_full).tolist(),
     'Q0_diff(stack vs full b=0)':(Q0-s.quantities(U_full)).tolist(),'field_diff_stack_vs_full_b0':float(np.max(abs(Y[0]-U_full)))}
raw={}
for b in [.1,.05,.025,.0125]:
    rp=s.quantities(integrate(ns,ns.init_family(phi,b=b),T,dt))-Q0-b*b*Q2
    rm=s.quantities(integrate(ns,ns.init_family(phi,b=-b),T,dt))-Q0-b*b*Q2
    raw[b]=.5*(rp+rm); out[f'raw_even_b{b}']=raw[b].tolist(); out[f'raw_odd_b{b}']=(.5*(rp-rm)).tolist()
bl=[.1,.05,.025,.0125]
for i in range(3):
    out[f'ratio_{bl[i]}/{bl[i+1]}']=(abs(raw[bl[i]])/abs(raw[bl[i+1]])).tolist()
# quartic coefficient estimate c4 = raw/b^4
for b in bl: out[f'c4_est_b{b}']=(raw[b]/b**4).tolist()
# roundoff: 'same' solve via mathematically equivalent but differently rounded path (stacked solve at b=0 vs plain)
print(json.dumps(out,indent=1))
json.dump(out,open(str(OUT)+'/cancellation_E.json','w'),indent=1)
