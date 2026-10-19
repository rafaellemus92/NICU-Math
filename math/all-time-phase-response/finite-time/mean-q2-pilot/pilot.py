"""Three-cell runtime/correctness probe only; no q2 evolution or full validator."""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,json,platform,resource,signal,time
from pathlib import Path
from decimal import Decimal,localcontext
import numpy as np
import kernels as k
v=k.v
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
PINS={
 'absorption-b003/results/trajectory_manifest.json':'8c39c91f4980ef30458c3300f6df0094709873e355546b7c54a764a0553dd847',
 'absorption-b003/results/chain.json':'0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
 'route-b-dissipation/results/bounds.review.json':'4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
}

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def pack(x):return {'lo':str(x.lo),'hi':str(x.hi)}

def probe_node(j):
    A=np.zeros((3,41,41),complex)
    if j:
        A[0,20,21]=A[0,20,19]=.005
        A[0,20,40]=A[0,20,0]=.000001
        A[2,21,20]=.002j;A[2,19,20]=-.002j
    return k.mean_node(A)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--trajectory',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError('Refusing to overwrite '+str(args.output))
    def stop(signum,frame):raise TimeoutError('180-second pilot limit reached')
    signal.signal(signal.SIGALRM,stop);signal.setitimer(signal.ITIMER_REAL,180)
    start=time.monotonic()
    for name,digest in PINS.items():
        if sha(PARENT/name)!=digest:raise ValueError('Input mismatch: '+name)
    manifest=json.loads((PARENT/'absorption-b003/results/trajectory_manifest.json').read_text())
    chain=json.loads((PARENT/'absorption-b003/results/chain.json').read_text())
    rb=json.loads((PARENT/'route-b-dissipation/results/bounds.review.json').read_text())
    arrays={}
    for name,m in manifest['files'].items():
        p=args.trajectory/name
        if p.stat().st_size!=m['bytes'] or sha(p)!=m['sha256_file']:raise ValueError('Array mismatch '+name)
        a=np.load(p,mmap_mode='r',allow_pickle=False)
        if list(a.shape)!=m['shape'] or str(a.dtype)!=m['dtype']:raise ValueError('Layout mismatch '+name)
        arrays[name]=a
    Qn,Wn=arrays['Q_nodes.npy'],arrays['W_nodes.npy']
    rows=[]
    with localcontext(k.TRAP):
        for j in (0,6250,12499):
            begin=time.monotonic()
            Q0=k.project(v.exact(Qn[j]),kz=1);Q1=k.project(v.exact(Qn[j+1]),kz=1)
            W0=v.exact(Wn[j]);W1=v.exact(Wn[j+1])
            V0=probe_node(j);V1=v.cscale(V0,.999998)
            t=time.monotonic();r=k.residual_polynomial(Q0,Q1,W0,W1,V0,V1,j)
            kernel=time.monotonic()-t
            # Independent evaluation order at the midpoint, using the same frozen exponential.
            mid=lambda a,b:v.cscale(v.cadd(a,b),.5)
            D=v.cscale(v.csub(V1,V0),50000)
            direct=k.direct_frozen(mid(Q0,Q1),mid(W0,W1),mid(V0,V1),D,j)
            tau=k.Iv.of('1/100000')
            poly=v.cadd(r['R0'],v.cadd(k.scale_iv(r['R1'],tau),k.scale_iv(r['R2'],tau.sq())))
            distance=np.hypot(poly.re-direct.re,poly.im-direct.im)
            overlaps=bool(np.all(distance<=poly.rad+direct.rad))
            if not overlaps:raise ArithmeticError('Midpoint interval evaluations disagree')
            mask=np.ones(r['R0'].shape[-2:],bool)
            mask[r['bx']-20:r['bx']+21,r['by']-20:r['by']+21]=False
            tail=v.CI(r['R0'].re[:,mask],r['R0'].im[:,mask],r['R0'].rad[:,mask])
            row={'fine_cell':j,'state_kind':'zero first-cell probe' if j==0 else 'synthetic later-cell probe, NOT actual q2',
                 'residual_kernel_seconds':kernel,'total_cell_seconds':time.monotonic()-begin,
                 'output_support':[r['bx'],r['by']],
                 'integral_residual_upper':pack(r['integral']),
                 'polynomial_coefficient_norms':[pack(x) for x in r['polynomial_norms']],
                 'frozen_shear_allowance':pack(r['frozen']),
                 'forcing_integral_upper':pack(r['source_L1']),
                 'r0_tail_norm_upper':v.wnorm_hi(tail,1,False),
                 'max_r0_disc_radius':float(np.max(r['R0'].rad)),
                 'midpoint_discs_overlap':overlaps}
            rows.append(row)
            print(f'cell {j}: residual kernel {kernel:.4f}s, total {row["total_cell_seconds"]:.4f}s, midpoint overlap {overlaps}',flush=True)
        T,nu=k.Iv.of('1/4'),k.Iv.of('1/28')
        B=rb['bounds'];get=lambda key:k.Iv.of(B[key]['hi'])
        eps0,eps1,delta,CA=get('eps0'),get('eps1'),get('delta_e'),get('CA')
        smooth=T*(get('n1')*eps0+get('p')*eps1)
        error_square=CA*eps1*(T*delta).sqrt()
        deltaF=smooth+error_square
        # Upward-rounded conversion constants from the archived chain log.
        log=PARENT/'absorption-b003/results/chain_b0.003.log'
        if '4.5864E-1, 5.8868E-1, 1.1484E+0' not in log.read_text():raise ValueError('Sup conversion record mismatch')
        epsW=k.Iv.of(chain['epsW'])
        base_grad_coeff=T*epsW*k.Iv.of('0.45864')
        base_l2_coeff=T*epsW*k.Iv.of('0.58868')
        prop=((get('M1')-nu)*T).exp()
        budgets={name:pack(value) for name,value in {
          'q1_source_smooth_allowance':smooth,'q1_source_quadratic_error_allowance':error_square,
          'q1_source_L1_allowance':deltaF,
          'base_coefficient_times_sup_gradV':base_grad_coeff,
          'base_coefficient_times_sup_V':base_l2_coeff,
          'L2_propagator_upper':prop,'q1_allowance_after_propagation':prop*deltaF,
          'mean_initial_error':k.Iv.of(0),'inherited_W_initial_error':k.Iv.of(chain['epsW0'])}.items()}
    elapsed=time.monotonic()-start
    timings=[r['residual_kernel_seconds'] for r in rows]
    result={'scope':'fixed a=c=d=1, nu=1/28, phi=37/100,T=1/4,beta=.003; pilot only',
      'base_commit':'bc305995c49f3303352e1c1a4e13a50dbf90d965',
      'no_q2_trajectory_generated':True,'not_a_full_horizon_residual_bound':True,
      'rows':rows,'inherited_error_budget_coefficients':budgets,
      'wall_seconds_including_hashes':elapsed,
      'kernel_total_seconds':sum(timings),
      'naive_full_12500_cell_seconds_range':[12500*min(timings),12500*max(timings)],
      'extrapolation_caveat':'Not a runtime guarantee; only three same-size synthetic probes, no evolved field, no streaming/cache optimization.',
      'new_251_node_storage_bytes':251*3*41*41*16,
      'new_12501_node_storage_bytes':12501*3*41*41*16,
      'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'python':platform.python_version(),'numpy':np.__version__,
      'inputs_sha256':PINS,'trajectory_file_hashes':{name:m['sha256_file'] for name,m in manifest['files'].items()},
      'source_sha256':{name:sha(HERE/name) for name in ('kernels.py','pilot.py','PLAN.md')},
      'conversion_log_sha256':sha(log),
      'verdict':'sampled kernel checks completed; full-run approval and independent review still required'}
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(f'pilot total wall {elapsed:.4f}s; residual kernels {sum(timings):.4f}s',flush=True)
    print('naive 12500-cell residual-only range (seconds):',result['naive_full_12500_cell_seconds_range'])
    signal.setitimer(signal.ITIMER_REAL,0)

if __name__=='__main__':main()
