"""Time course of Q0=(E,Z,S)(U), Q2=(E2,Z2,S2) at phi=.37 and raw remainder ratios at T=2,4,8 (b=.1,.05,.025). N from argv."""
import sys, json, time
from common import *
N=int(sys.argv[1]); nu=NU; dt=.01; phi=.37; Ts=[.5,1,2,4,8]
r=Response(N,nu); ns=audit.NS(N,nu); t0=time.time()
Y=r.initial(phi); U={}; Q0={}; Q2={}; Ys={}
t=0.
for n in range(800):
    Y=r.step(Y,dt); t=round((n+1)*dt,10)
    if t in Ts: Q0[t]=r.quantities(Y[0]).tolist(); Q2[t]=r.second(Y).tolist(); Ys[t]=Y.copy()
out={'N':N,'K':r.g.K,'Q0':Q0,'Q2':Q2,'Z2_over_Z0':{t:Q2[t][1]/Q0[t][1] for t in Ts}}
bs=[.1,.05,.025]; raw={T:{} for T in [2,4,8]}; fld={T:{} for T in [2,4,8]}
for b in bs:
    for sgn in [1,-1]:
        u=ns.init_family(phi,b=sgn*b)
        for n in range(800):
            u=ns.step(u,dt); t=round((n+1)*dt,10)
            if t in raw:
                rr=r.quantities(u)-np.array(Q0[t])-b*b*np.array(Q2[t]); raw[t].setdefault(b,[]).append(rr.tolist())
                f=u-Ys[t][0]-sgn*b*Ys[t][1]-b*b*Ys[t][2]; fld[t].setdefault(b,[]).append(float(np.sqrt(r.g.inner(f,f))))
res={}
for T in raw:
    ev={b:.5*(np.array(raw[T][b][0])+np.array(raw[T][b][1])) for b in bs}
    res[T]={'raw_even':{b:ev[b].tolist() for b in bs},'ratio_.1/.05':(abs(ev[.1])/abs(ev[.05])).tolist(),'ratio_.05/.025':(abs(ev[.05])/abs(ev[.025])).tolist(),
            'field_L2':{b:fld[T][b] for b in bs},'field_ratio_.1/.05':fld[T][.1][0]/fld[T][.05][0],'field_ratio_.05/.025':fld[T][.05][0]/fld[T][.025][0],
            'raw_even_over_b2Q2_at_b=.1':(ev[.1]/(.01*np.array(Q2[T]))).tolist()}
out['remainders']=res; out['wall']=time.time()-t0
print(json.dumps(out,indent=1)); json.dump(out,open(str(OUT)+f'/late_time_N{N}.json','w'),indent=1)
