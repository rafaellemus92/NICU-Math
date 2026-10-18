import json, time
from common import *
nu=NU; dt=.01; M=8; phases=2*np.pi*np.arange(M)/M
cfgs=[(24,7),(24,8),(30,9)]
t0=time.time(); out={}
for N,K in cfgs:
    r=Response(N,nu,K=K)
    rec={1.0:[],8.0:[]}
    for p in phases:
        Y=r.initial(p)
        for n in range(800):
            Y=r.step(Y,dt)
            if n+1 in (100,800): rec[round((n+1)*dt)].append(r.second(Y))
    for T in rec:
        arr=np.array(rec[T])
        out[f'N{N}_K{K}_T{T}']={'cos0':harm_cos(arr,0).tolist(),'cos1':harm_cos(arr,1).tolist(),'cos2':harm_cos(arr,2).tolist(),'cos3':harm_cos(arr,3).tolist()}
    print(N,K,time.time()-t0,flush=True)
    json.dump(out,open(str(OUT)+'/K_effect_resp.json','w'),indent=1)
print(json.dumps(out,indent=1))
