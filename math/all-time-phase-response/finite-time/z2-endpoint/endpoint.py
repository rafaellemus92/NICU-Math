"""Fixed endpoint Z2 enclosure from verified arrays and existing norm bounds.
No time evolution. Outputs are exclusive-create. See NOTE.md for scope/limits.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
BASE = '2af8fe4b3abceee08547f0fee699d78b5ac29bf2'
PINS = {
 'constants.py': '996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014',
 'absorption-b003/results/chain.json': '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
 'absorption-b003/results/trajectory_manifest.json': '8c39c91f4980ef30458c3300f6df0094709873e355546b7c54a764a0553dd847',
 'route-b-dissipation/results/bounds.review.json': '4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
}

def sha_file(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def check_pins():
    for name, expected in PINS.items():
        if sha_file(PARENT / name) != expected:
            raise ValueError('Pinned input mismatch: ' + name)

check_pins()
spec = importlib.util.spec_from_file_location('endpoint_constants', PARENT / 'constants.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
Iv, TRAP = c.Iv, c.TRAP


def components(z):
    return Fraction(float(z.real)), Fraction(float(z.imag))


def projected_gradient_squared(Q):
    """Exact normalized ||grad Re(e^iz P Q)||²; k=(kx,ky,1).
    |k|²|P Q|²=|k|²|Q|²-|k.Q|², so no floating projection is used.
    """
    nx, ny = Q.shape[1:]
    if Q.shape[0] != 3 or nx % 2 != 1 or ny % 2 != 1:
        raise ValueError('Expected three components on an odd centered grid')
    total = Fraction(0)
    for ix in range(nx):
        for iy in range(ny):
            k = (ix-nx//2, iy-ny//2, 1)
            q = [components(Q[j,ix,iy]) for j in range(3)]
            dot_re = sum(k[j]*q[j][0] for j in range(3))
            dot_im = sum(k[j]*q[j][1] for j in range(3))
            energy = sum(r*r+i*i for r,i in q)
            term = sum(x*x for x in k)*energy-dot_re*dot_re-dot_im*dot_im
            if term < 0:
                raise ArithmeticError('Negative exact projected energy')
            total += term
    return total / 2


def base_vertical_laplacian_squared(W):
    """Exact ||Delta Re(e^ix W(y))||², with centered odd support."""
    if len(W) % 2 != 1:
        raise ValueError('Expected odd centered W support')
    total = Fraction(0)
    for j,z in enumerate(W):
        n = j-len(W)//2
        r,i = components(z)
        total += (1+n*n)**2*(r*r+i*i)
    return total / 2


def fraction_interval(x):
    return Iv.of(x.numerator)/Iv.of(x.denominator)


def energy_with_gradient_error(norm_squared, eps):
    n = fraction_interval(norm_squared).sqrt()
    true_norm = Iv(max(Decimal(0),(n-eps).lo),(n+eps).hi)
    return n, true_norm.sq()/2


def absolute_interval(x):
    lo = Decimal(0) if x.lo <= 0 <= x.hi else min(x.lo.copy_abs(),x.hi.copy_abs())
    return Iv(lo,max(x.lo.copy_abs(),x.hi.copy_abs()))


def evaluate(trajectory):
    check_pins()
    manifest = json.loads((PARENT/'absorption-b003/results/trajectory_manifest.json').read_text())
    chain = json.loads((PARENT/'absorption-b003/results/chain.json').read_text())
    rb = json.loads((PARENT/'route-b-dissipation/results/bounds.review.json').read_text())
    if (chain['b'],chain['T'],chain['phi']) != ('0.003',0.25,0.37):
        raise ValueError('Certificate scope mismatch')
    arrays = {}
    for name,m in manifest['files'].items():
        path = trajectory/name
        if path.stat().st_size != m['bytes'] or sha_file(path) != m['sha256_file']:
            raise ValueError('Trajectory identity mismatch: ' + name)
        a = np.load(path,mmap_mode='r',allow_pickle=False)
        if list(a.shape) != m['shape'] or str(a.dtype) != m['dtype']:
            raise ValueError('Trajectory layout mismatch: ' + name)
        arrays[name] = a
    # Only endpoint arithmetic; all time-integration/error estimates are inherited.
    Qsq = projected_gradient_squared(arrays['Q_nodes.npy'][-1])
    Wsq = base_vertical_laplacian_squared(arrays['W_nodes.npy'][-1])
    with localcontext(TRAP):
        T,nu,beta = Iv.of('1/4'),Iv.of('1/28'),Iv.of('3/1000')
        eps1,epsW = Iv.of(chain['eps1']),Iv.of(chain['epsW'])
        qnorm,E1 = energy_with_gradient_error(Qsq,eps1)
        UNlap = (((-nu*T).exp()).sq()/2+fraction_interval(Wsq)).sqrt()
        # 4(x+2)^3-27(x+1)^2=(x-1)^2(4x+5)>=0 for x=n².
        # Real single-x-harmonic Parseval contributes 1/2, hence factor sqrt(2/27).
        base_lap_error = Iv.of('2/27').sqrt()*epsW
        U_lap_upper = Iv.of((UNlap+base_lap_error).hi)
        N2_upper = Iv.of(rb['bounds']['N2']['hi'])
        pairing_radius = U_lap_upper*N2_upper
        pairing = Iv(pairing_radius.hi.copy_negate(),pairing_radius.hi)
        Z2 = E1+pairing
        abs_Z2 = absolute_interval(Z2)
        CB_upper = Iv.of(rb['bounds']['CZ']['hi'])
        comparison = beta.sq()*CB_upper
        def pack(x):
            return {'lo':str(x.lo),'hi':str(x.hi),
                    'display_lower':str(c.round_down(x.lo)),
                    'display_upper':str(c.round_up(x.hi))}
        return {
          'status':'rigorous enclosure conditional on inherited certificates; new derivation needs review',
          'base_commit':BASE,'scope':'a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000',
          'source_sha256':sha_file(Path(__file__)),
          'plan_sha256':sha_file(HERE/'PLAN.md'),'inputs_sha256':PINS,
          'trajectory_files':manifest['files'],
          'exact_endpoint_fractions':{'projected_q_gradient_squared':str(Qsq),
                                      'base_vertical_laplacian_squared':str(Wsq)},
          'bounds':{k:pack(v) for k,v in {
            'qN_gradient_norm':qnorm,'half_q1_gradient_squared':E1,
            'base_approx_laplacian_norm':UNlap,'base_laplacian_error':base_lap_error,
            'base_true_laplacian_upper':U_lap_upper,'N2_upper':N2_upper,
            'signed_q2_pairing':pairing,'Z2':Z2,'abs_Z2':abs_Z2,
            'beta_squared_CB':comparison}.items()},
          'fixed_target_dominance_certified':abs_Z2.lo>comparison.hi,
          'zero_excluded':not (Z2.lo<=0<=Z2.hi),
          'interpretation':'Failure to certify dominance is not a claim that physical dominance fails.',
        }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--trajectory',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():
        raise FileExistsError('Refusing to overwrite output: '+str(args.output))
    result=evaluate(args.trajectory)
    with args.output.open('x') as f:
        json.dump(result,f,indent=2);f.write('\n')
    for key,b in result['bounds'].items():
        print(key+': ['+b['display_lower']+', '+b['display_upper']+']')
    print('Fixed target dominance certified:',result['fixed_target_dominance_certified'])
    print('Zero excluded from Z2:',result['zero_excluded'])

if __name__=='__main__': main()
