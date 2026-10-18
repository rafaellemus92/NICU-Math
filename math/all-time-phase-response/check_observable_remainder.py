"""Raw E/Z/S remainders; pre-set ratio acceptance 14..18 for b=.1/.05.
No q3 computation. Finite-system scaling evidence, not a continuum certificate.
"""
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path
import numpy as np
from response import Response, audit, integrate


def main():
    start=time.perf_counter(); cpu=time.process_time()
    T=.5; nu=1/28; phi=.37; rows=[]
    for N,dt in [(18,.005),(18,.0025),(24,.005)]:
        solver=Response(N,nu); full=audit.NS(N,nu)
        Y=integrate(solver,solver.initial(phi),T,dt)
        Q0=solver.quantities(Y[0]); Q2=solver.second(Y); cases=[]
        for b in [.1,.05]:
            raw=[]; fields=[]
            for signed_b in [b,-b]:
                u=integrate(full,full.init_family(phi,b=signed_b),T,dt)
                raw.append(solver.quantities(u)-Q0-signed_b**2*Q2)
                field=u-Y[0]-signed_b*Y[1]-signed_b**2*Y[2]
                fields.append(float(np.sqrt(solver.g.inner(field,field))))
            cases.append({'abs_b':b,'raw_plus_E_Z_S':raw[0].tolist(),
                'raw_minus_E_Z_S':raw[1].tolist(),
                'raw_even_E_Z_S':(.5*(raw[0]+raw[1])).tolist(),
                'field_second_order_L2_plus_minus':fields})
        ratios=(abs(np.array(cases[0]['raw_even_E_Z_S']))/abs(np.array(cases[1]['raw_even_E_Z_S']))).tolist()
        rows.append({'N':N,'K':(N-1)//3,'dt':dt,'Q0_E_Z_S':Q0.tolist(),
                     'Q2_E_Z_S':Q2.tolist(),'cases':cases,'raw_quartic_ratios_E_Z_S':ratios})
    checks={f'N{r["N"]}_dt{r["dt"]}_{name}':bool(14<ratio<18)
            for r in rows for name,ratio in zip(['E','Z','S'],r['raw_quartic_ratios_E_Z_S'])}
    out={'status':'pass' if all(checks.values()) else 'FAIL','checks':checks,
         'definitions':{'observable_raw':'R_O(b)=O(u_b)-O(U)-b^2 O2, O=E,Z,S',
             'raw_even':'(R_O(+b)+R_O(-b))/2; plus and minus stored separately',
             'observable_ratio':'abs(raw_even(.1))/abs(raw_even(.05)), componentwise; quartic target 16',
             'field':'normalized L2 norm of u_b-U-b q1-b^2 q2; cubic target ratio 8',
             'not_tested':'No q3 solver or cubic-field-subtraction/quartic-field test'},
         'metadata':{'a':1,'c':1,'d':1,'nu':nu,'T':T,'phi':phi,'phase_count':1,
             'phase_quadrature':'none here; original response pilots used 8 and 12',
             'seed':None,'randomness':'none','units':'nondimensional; normalized 2pi torus averages',
             'python':platform.python_version(),'numpy':np.__version__,
             'git_parent':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
             'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                 [Path(__file__),Path(__file__).with_name('response.py'),Path(audit.__file__)]},
             'wall_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu},
         'runs':rows}
    output=Path('results/observable_remainder.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':out['status'],'ratios':[r['raw_quartic_ratios_E_Z_S'] for r in rows],
                      'wall_seconds':out['metadata']['wall_seconds']}))
    return 0 if all(checks.values()) else 1

if __name__=='__main__': raise SystemExit(main())
