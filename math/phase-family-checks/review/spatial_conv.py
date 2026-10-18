"""Spectral convergence chain of second_E_Z_S at T=.5, dt=.005, 8 phases: N=12,18,24 (from stored JSON) extended by N=30,36 (K=9,11)."""
import json
from common import *
nu=NU; T=.5; dt=.005; M=8; phases=2*np.pi*np.arange(M)/M
pil=json.load(open(str(PKG/'results/pilot.json'))); ref=json.load(open(str(PKG/'results/refined.json')))
stored={12:np.array(pil['runs'][1]['second_E_Z_S']),18:np.array(ref['runs'][1]['second_E_Z_S']),24:np.array(ref['runs'][2]['second_E_Z_S'])}
res=dict(stored)
for N in [30,36]:
    r=Response(N,nu); res[N]=np.array([r.second(integrate(r,r.initial(p),T,dt)) for p in phases]); print(N,flush=True)
Ns=sorted(res); out={}
for a,b in zip(Ns[:-1],Ns[1:]):
    d=abs(res[a]-res[b]); out[f'maxdiff_N{a}_N{b}']={'all':float(d.max()),'E':float(d[:,0].max()),'Z':float(d[:,1].max()),'S':float(d[:,2].max())}
for N in [30,36]: out[f'cos2_N{N}']=harm_cos(res[N],2).tolist(); out[f'cos0_N{N}']=harm_cos(res[N],0).tolist()
print(json.dumps(out,indent=1)); json.dump(out,open(str(OUT)+'/spatial_conv.json','w'),indent=1)
