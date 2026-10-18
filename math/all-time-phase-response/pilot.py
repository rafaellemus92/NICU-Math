"""Bounded validation pilot. Any failed numerical acceptance check exits nonzero."""
import argparse
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path
import numpy as np
from response import Response, audit, integrate, harmonics


def run(N, dt, phases, T, nu):
    solver = Response(N,nu)
    vals=[]
    for p in 2*np.pi*np.arange(phases)/phases:
        Y=integrate(solver,solver.initial(p),T,dt)
        vals.append(solver.second(Y))
    return np.array(vals)


def phase_error(h1,h2):
    return max(abs(x-y) for m in h1 for part in ("cos","sin")
               for x,y in zip(h1[m][part],h2[m][part]))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--recheck-saved', nargs='+', type=Path, help='Recheck all reported phase harmonics without integration')
    p.add_argument('--output', type=Path, default=None)
    p.add_argument('--coarse-N', type=int, default=12)
    p.add_argument('--T', type=float, default=.5)
    p.add_argument('--dt', type=float, default=.01)
    p.add_argument('--nu', type=float, default=1/28)
    args=p.parse_args()
    if args.output is None:
        args.output=Path('results/recheck.json' if args.recheck_saved else 'results/pilot.json')
    if args.recheck_saved:
        if args.output.resolve() in [path.resolve() for path in args.recheck_saved]:
            p.error('output must differ from every saved input')
        records=[]
        for path in args.recheck_saved:
            data=json.loads(path.read_text())
            error=phase_error(data['runs'][2]['harmonics_E_Z_S'],data['runs'][3]['harmonics_E_Z_S'])
            records.append({'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'phase_all_m0_to_m3_cos_and_sin_error':error,'limit':data['limits']['phase'],
                'phase_check_pass':bool(error<=data['limits']['phase']),
                'original_status':data['status'],
                'full_solve_parameters_from_source':{'N':18,'K':5,'phi':.37,'dt':data['runs'][1]['dt_actual'],
                 'b_magnitudes':[.1,.05],'dt_note':'metadata supplied retrospectively from inspected source; matches run 1 step'}})
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps({'recheck_only':True,'records':records},indent=2)+'\n')
        print(json.dumps(records))
        return 0 if all(x['phase_check_pass'] for x in records) else 1
    if not (np.isfinite(args.nu) and args.nu>0 and np.isfinite(args.T) and args.T>0
            and np.isfinite(args.dt) and args.dt>0):
        p.error('nu, T, dt must be finite and positive')
    if args.coarse_N < 9: p.error('coarse-N must be >= 9')
    start=time.perf_counter(); cpu=time.process_time()
    N0=args.coarse_N; N1=N0+6
    configs=[(N0,args.dt,8),(N0,args.dt/2,8),(N1,args.dt/2,8),(N1,args.dt/2,12)]
    results=[run(N,dt,M,args.T,args.nu) for N,dt,M in configs]
    hs=[harmonics(v) for v in results]
    # Pre-registered absolute tolerances; small bounded pilot, no certification.
    errors={'time':float(np.max(abs(results[0]-results[1]))),
            'space':float(np.max(abs(results[1]-results[2]))),
            'phase':phase_error(hs[2],hs[3])}
    limits={'time':2e-7,'space':2e-4,'phase':2e-6}
    solver=Response(18,args.nu); ns=audit.NS(18,args.nu)
    Y=integrate(solver,solver.initial(.37),args.T,args.dt/2)
    U=Y[0]; second=solver.second(Y); residuals=[]
    for b in [.1,.05]:
        plus=integrate(ns,ns.init_family(.37,b=b),args.T,args.dt/2)
        minus=integrate(ns,ns.init_family(.37,b=-b),args.T,args.dt/2)
        central=(solver.quantities(plus)+solver.quantities(minus)-2*solver.quantities(U))/(2*b*b)
        residuals.append({'b':b,'central_second':central.tolist(),
                          'second_error':float(np.max(abs(central-second))),
                          'field_L2_remainder':float(np.sqrt(solver.g.inner(plus-U-b*Y[1]-b*b*Y[2],plus-U-b*Y[1]-b*b*Y[2]))),
                          'parity_error':float(np.max(abs(solver.quantities(plus)-solver.quantities(minus))))})
    ratio= residuals[0]['second_error']/residuals[1]['second_error']
    field_ratio=residuals[0]['field_L2_remainder']/residuals[1]['field_L2_remainder']
    checks={k:errors[k]<=limits[k] for k in errors}
    checks.update(second_difference_ratio=3.5<ratio<4.5,field_remainder_ratio=7<field_ratio<9,
                  parity=max(x['parity_error'] for x in residuals)<1e-12)
    files=[Path(__file__),Path(__file__).with_name('response.py'),Path(audit.__file__)]
    out={'status':'pass' if all(checks.values()) else 'FAIL','checks':checks,
         'error_definitions':{
             'second_error':'max over E,Z,S of abs((O(+b)+O(-b)-2 O(U))/(2 b^2)-O2); normalized by b^2',
             'field_L2_remainder':'norm(u_+b-U-b q1-b^2 q2), normalized spatial L2; second-order truncation only',
             'second_difference_ratio':'normalized response errors at b=.1/.05; target 4',
             'field_remainder_ratio':'second-order field truncation errors at b=.1/.05; target 8',
             'not_tested':'q3 is not implemented; no cubic-field truncation ratio 16 is measured'},
         'metadata':{'python':platform.python_version(),'numpy':np.__version__,'seed':None,
         'randomness':'none','git_base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
         'sha256':{str(f.relative_to(Path(__file__).resolve().parents[2])):hashlib.sha256(f.read_bytes()).hexdigest() for f in [f.resolve() for f in files]},
         'units':'nondimensional; torus side 2pi; normalized volume averages',
         'norms':'field: normalized L2; observable differences: componentwise max absolute',
         'a':1,'c':1,'d':1,'nu':args.nu,'T':args.T,
         'full_solve_parameters':{'N':18,'K':5,'phi':.37,'dt_actual':args.T/int(np.ceil(args.T/(args.dt/2))),'b_magnitudes':[.1,.05]},
         'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu},
         'runs':[{'N':N,'K':(N-1)//3,'dt_requested':dt,'dt_actual':args.T/int(np.ceil(args.T/dt)),
                  'phases':M,'second_E_Z_S':v.tolist(),'harmonics_E_Z_S':h}
                 for (N,dt,M),v,h in zip(configs,results,hs)],
         'errors':errors,'limits':limits,'full_solve_checks':residuals,
         'variation_second':second.tolist(),'second_difference_ratio':ratio,'field_remainder_ratio':field_ratio}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:out[k] for k in ['status','checks','errors','second_difference_ratio','field_remainder_ratio']}))
    print('wall seconds:',out['metadata']['wall_seconds'])
    return 0 if all(checks.values()) else 1

if __name__=='__main__':
    raise SystemExit(main())
