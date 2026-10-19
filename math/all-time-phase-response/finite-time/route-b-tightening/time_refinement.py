"""Zero-initial-energy upper envelope integration; not numerical PDE evolution."""
import sys
sys.dont_write_bytecode=True
import json,time,signal
from decimal import localcontext
from pathlib import Path
import evaluate as e
I=e.I
HERE=Path(__file__).resolve().parent

def energy_cap(t,b):
    a=2*b['M1']+2*b['beta']*b['n1']
    q=2*b['beta'].sq()*b['CA'].sq()/b['nu']
    c=(b['M2']+b['beta']*b['n2'])*b['Nw']
    f0=c*b['K']+4*b['sigma'].sq()/b['nu']
    fd=4*b['CA'].sq()*b['eps1'].sq()/b['nu']
    z=(2*a*t).exp()
    g=(2*q*b['delta_e']).exp()*(f0/a*(z-1)+2*fd*b['delta_e']*z)
    # This interval encloses min of two explicit majorants, not physical y.
    k2=b['K'].sq()
    return I(min(k2.lo,g.lo),min(k2.hi,g.hi))

def refine(b,n=1000):
    T,nu,C,K,N,sigma,delta=[b[k] for k in ('T','nu','CA','K','Nw','sigma','delta_e')]
    h=T/n
    iy=h*sum((energy_cap(h*j,b) for j in range(1,n+1)),I.of(0))
    a=2*b['M1']+2*b['beta']*b['n1']
    q=2*b['beta'].sq()*C.sq()/nu
    c=(b['M2']+b['beta']*b['n2'])*N
    parts=dict(growth=a*iy,error=q*K.sq()*delta,mixed=c*(T*iy).sqrt(),forcing=4/nu*(sigma.sq()*T+C.sq()*b['eps1'].sq()*delta))
    dw=8/nu*sum(parts.values(),I.of(0))
    return iy,dw,parts

def main():
    start=time.monotonic();signal.alarm(60)
    with localcontext(e.c.TRAP):
        b={k:I.of(v['hi']) for k,v in e.old['bounds'].items()}
        b['nu']=I.of('1/28')
        iy,dw,parts=refine(b)
        # Override in-memory input to evaluator only; inherited files stay unchanged.
        e.old['bounds']['Dw']['hi']=str(dw.hi)
        hist=e.histogram(32)
        rows={str(l):e.evaluate(hist,l) for l in (100,10000,100000,1000000,10000000)}
        pack=lambda v:{'lo':str(v.lo),'hi':str(v.hi)}
        data={'status':'candidate awaiting independent exact-code review; no dominance certificate','inputs_sha256':e.PINS,'source_sha256':e.sha(Path(__file__)),'helper_sha256':e.sha(HERE/'evaluate.py'),'plan_sha256':e.sha(HERE/'PLAN.time-refinement.md'),'I_y':pack(iy),'old_T_K_squared':pack(b['T']*b['K'].sq()),'Dw':pack(dw),'energy_terms':{k:pack(v) for k,v in parts.items()},'rows':rows,'integration_cells':1000,'wall_seconds':time.monotonic()-start}
    with (HERE/'results/time_refinement.final.json').open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    print('Iy',iy.hi,'Dw',dw.hi)
    for l,r in rows.items(): print(l,'Cglobal',r['C_global']['hi'],'Cendpoint',r['C_endpoint']['hi'],'threshold',r['threshold_endpoint']['hi'])
    print('seconds',data['wall_seconds'])
if __name__=='__main__':main()
