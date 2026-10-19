"""Frozen paired DNS diagnostic; empirical finite-grid evidence, not validation."""
import argparse,csv,hashlib,importlib.util,json,math,platform,resource,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOLVER=ROOT/'math/ns-phase-audit/audit_v2/dns/ns.py'
spec=importlib.util.spec_from_file_location('paired_ns',SOLVER)
nsmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(nsmod)
NU=1/28; B=.003; PHI=.37; T=.25
COLUMNS=['t','b','S_over_b2','nuR_over_b2','H_over_b2','balance_over_b2',
         'trapS_over_b2','trapNuR_over_b2','integrated_direct_expanded_error']

def tri(g,u):
    w=g.inv(g.curl_h(u))
    return sum(float(np.mean(w[i]*w[j]*g.inv(1j*g.kvec[j]*u[i]))) for i in range(3) for j in range(3))

def run(N,dt,steps,out):
    started=time.monotonic();solver=nsmod.NS(N,NU);g=solver.g
    assert N>3*g.K and N%2==0
    states=np.stack([solver.init_family(PHI,b=b) for b in (0.,B,-B)])
    stats=dict(max_divergence=0.,max_tail_enstrophy_fraction=0.,max_tri_rhs_scaled_error=0.,
               max_direct_expanded_scaled_error=0.,max_balance_scaled=0.,max_parity_scaled=0.,
               max_trapezoid_scaled_difference=0.)
    tail=(np.max(np.abs(g.kvec),axis=0)>=g.K-1)*g.mask
    def stage(y):
        nl=np.stack([solver.nonlin(u) for u in y]);rhs=nl-solver.visc*y
        q=np.array([g.inner(g.k2*u,n) for u,n in zip(y,nl)])
        d=np.array([2*g.palin(u) for u in y])
        direct=np.stack([q[1:]-q[0],NU*(d[1:]-d[0])],axis=1)
        expanded=[]
        for j in (1,2):
            v=y[j]-y[0];dn=nl[j]-nl[0]
            qe=g.inner(g.k2*v,nl[0])+g.inner(g.k2*y[0],dn)+g.inner(g.k2*v,dn)
            de=2*g.inner(g.k2*y[0],g.k2*v)+g.inner(g.k2*v,g.k2*v)
            expanded.append((qe,NU*de))
        expanded=np.array(expanded)
        stats['max_direct_expanded_scaled_error']=max(stats['max_direct_expanded_scaled_error'],float(np.max(np.abs(direct-expanded)))/B**2)
        return rhs,expanded,direct,q
    def observe(y,t,integ,integ_direct,trap,q,check_tri):
        heat_loss=B**2*(-math.expm1(-2*NU*t))/4
        heat_now=B**2*math.exp(-2*NU*t)/4
        vals=[]
        for j,b in ((1,B),(2,-B)):
            v=y[j]-y[0]
            h=g.inner(g.k2*y[0],v)+.5*g.inner(g.k2*v,v)-heat_now
            hd=g.enstrophy(y[j])-g.enstrophy(y[0])-heat_now
            s=integ[j-1,0];r=integ[j-1,1]-heat_loss
            err=max(float(np.max(np.abs(integ[j-1]-integ_direct[j-1]))),abs(h-hd))/B**2
            row=[t,b,s/B**2,r/B**2,h/B**2,(h-s+r)/B**2,
                 trap[j-1,0]/B**2,(trap[j-1,1]-heat_loss)/B**2,err]
            vals.append(row)
            stats['max_direct_expanded_scaled_error']=max(stats['max_direct_expanded_scaled_error'],err)
            stats['max_balance_scaled']=max(stats['max_balance_scaled'],abs(row[5]))
            stats['max_trapezoid_scaled_difference']=max(stats['max_trapezoid_scaled_difference'],abs(row[2]-row[6]),abs(row[3]-row[7]))
        stats['max_parity_scaled']=max(stats['max_parity_scaled'],float(np.max(np.abs(np.array(vals[0][2:5])-np.array(vals[1][2:5])))))
        for j,u in enumerate(y):
            stats['max_divergence']=max(stats['max_divergence'],float(np.max(np.abs(g.div_h(u)))))
            frac=float(np.sum(g.w*g.k2*tail*np.sum(np.abs(u)**2,axis=0)))/(2*g.enstrophy(u))
            stats['max_tail_enstrophy_fraction']=max(stats['max_tail_enstrophy_fraction'],frac)
            if check_tri:stats['max_tri_rhs_scaled_error']=max(stats['max_tri_rhs_scaled_error'],abs(tri(g,u)-q[j])/B**2)
        if not np.isfinite(y).all():raise ValueError('nonfinite state')
        if stats['max_divergence']>1e-10 or stats['max_tri_rhs_scaled_error']>1e-8:raise ValueError('normalization/divergence diagnostic failure')
        if stats['max_direct_expanded_scaled_error']>1e-8 or stats['max_parity_scaled']>1e-7:raise ValueError('difference/parity diagnostic failure')
        if stats['max_balance_scaled']>1e-5:raise ValueError('balance threshold failed')
        return vals
    # Independent analytic initial diagnostics, before interpreting any trajectory.
    rhs,e,d,q=stage(states)
    assert abs(q[0]-math.cos(PHI)/4)<1e-12
    for j in (1,2):
        assert abs(g.enstrophy(states[j])-g.enstrophy(states[0])-B**2/4)<1e-12
        assert abs(2*g.palin(states[j])-2*g.palin(states[0])-B**2/2)<1e-12
    # Exact heat-mode test of spectral operators (no time integration).
    f=solver.init_family(0.,a=0.,b=B,c=0.,d=0.)
    assert np.max(np.abs(solver.nonlin(f)))<1e-14
    assert abs(g.enstrophy(f)-B**2/4)<1e-18
    assert abs(2*g.palin(f)-B**2/2)<1e-18
    integ=np.zeros((2,2));integ_direct=integ.copy();trap=integ.copy();previous=e
    rows=observe(states,0.,integ,integ_direct,trap,q,True)
    for step in range(1,steps+1):
        k1,e1,d1,_=stage(states)
        k2,e2,d2,_=stage(states+dt*k1/2)
        k3,e3,d3,_=stage(states+dt*k2/2)
        k4,e4,d4,_=stage(states+dt*k3)
        states=states+dt*(k1+2*k2+2*k3+k4)/6
        integ+=dt*(e1+2*e2+2*e3+e4)/6
        integ_direct+=dt*(d1+2*d2+2*d3+d4)/6
        _,e,_,q=stage(states)
        trap+=dt*(previous+e)/2;previous=e
        rows.extend(observe(states,step*dt,integ,integ_direct,trap,q,step%10==0 or step==steps))
    with out.with_suffix('.csv').open('x',newline='') as f:
        writer=csv.writer(f);writer.writerow(COLUMNS);writer.writerows(rows)
    result=dict(label='numerical evidence; not a continuum certificate',N=N,K=g.K,dt=dt,steps=steps,T_run=steps*dt,
                nu=NU,phi=PHI,b_values=[B,-B],a=1,c=1,d=1,stats=stats,
                endpoints=[dict(zip(COLUMNS,row)) for row in rows[-2:]],
                elapsed_seconds=time.monotonic()-started,peak_rss_MiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
                python=platform.python_version(),numpy=np.__version__,platform=platform.platform(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                solver_sha256=hashlib.sha256(SOLVER.read_bytes()).hexdigest(),
                preregistration_sha256=hashlib.sha256((HERE/'PREREGISTRATION.md').read_bytes()).hexdigest())
    with out.with_suffix('.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--N',type=int,required=True);ap.add_argument('--dt',type=float,required=True)
    ap.add_argument('--steps',type=int,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    assert (args.N,args.dt) in ((24,.0025),(24,.00125),(32,.0025))
    assert args.steps in (10,round(T/args.dt))
    run(args.N,args.dt,args.steps,args.out)
