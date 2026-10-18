import json, time, sys
from common import *
nu=NU; dt=.01; M=12; phases=2*np.pi*np.arange(M)/M
cfgs=[(24,7),(24,8),(30,9),(36,11)]
t0=time.time(); out={}
for N,K in cfgs:
    ns=audit.NS(N,nu,K=K); g=ns.g
    rec={1.0:[],8.0:[]}
    for p in phases:
        u=ns.init_family(p,b=1.)
        t=0.
        for n in range(800):
            u=ns.step(u,dt); t=(n+1)*dt
            if n+1 in (100,800):
                rec[round(t)] .append([g.energy(u),g.enstrophy(u)])
    for T in rec:
        arr=np.array(rec[T])
        out[f'N{N}_K{K}_T{T}']={'E_mean':float(harm_cos(arr,0)[0]),'Z_mean':float(harm_cos(arr,0)[1]),
            'E_cos1':float(harm_cos(arr,1)[0]),'Z_cos1':float(harm_cos(arr,1)[1]),
            'E_cos2':float(harm_cos(arr,2)[0]),'Z_cos2':float(harm_cos(arr,2)[1]),'Z_sin2':float(harm_sin(arr,2)[1]),
            'Z_cos3':float(harm_cos(arr,3)[1]),'Z_per_phase':arr[:,1].tolist(),'E_per_phase':arr[:,0].tolist()}
    print(N,K,time.time()-t0,flush=True)
    json.dump(out,open(str(OUT)+'/K_effect_full.json','w'),indent=1)
print(json.dumps(out,indent=1))
