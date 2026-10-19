"""Route B: fixed-input interval postprocessing; no solver or trajectory reads.
See NOTE.md for the derivation. Output is exclusive-create; archives are immutable.
"""
import sys
sys.dont_write_bytecode = True
import argparse
from decimal import Decimal, localcontext
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PINNED = {
    'constants.py': '996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014',
    'results/lattice_sums.log': '2b06979104bdd3d478d5e5d933f524341e3e6d64c2e7b1fc5249ad77171a009e',
    'absorption-b003/results/validated.json': 'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b',
    'absorption-b003/results/chain.json': '0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
}
BASE = '419e6c3d2e0321816849ca550ad8da5cf34ba75a'

def verify_inputs(parent=PARENT):
    for name, digest in PINNED.items():
        if hashlib.sha256((parent / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Pinned input mismatch: ' + name)

verify_inputs()  # Verify the interval implementation before importing it.
spec = importlib.util.spec_from_file_location('route_b_constants', PARENT / 'constants.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
Iv, TRAP = c.Iv, c.TRAP


def linear_bounds(M1, M2, nu, T, source_l1, source_l2_squared):
    """Zero initial data: L2, H1, integrated H2; source norms already integrated."""
    N = ((M1 - nu) * T).exp() * source_l1
    E2 = ((4 * M1 + 1) * T).exp() * (M2.sq() * N.sq() * T + source_l2_squared / nu)
    D = (2 / nu) * ((2 * M1 + Iv.of('1/2')) * E2 * T
                   + M2.sq() * N.sq() * T / 2 + source_l2_squared / (2 * nu))
    return N, E2.sqrt(), D


def dissipation_terms(nu, beta, CA, M1, M2, n1, n2, K, Nw, sigma, eps1,
                      duration, error_dissipation):
    """RHS of the retained W2 energy inequality, divided by b^4."""
    return {
        'growth': (2 * M1 + 2 * beta * n1) * K.sq() * duration,
        'error_advection': 2 * beta.sq() * CA.sq() * K.sq() * error_dissipation / nu,
        'mixed_energy': (M2 + beta * n2) * Nw * K * duration,
        'forcing': 4 * (sigma.sq() * duration + CA.sq() * eps1.sq() * error_dissipation) / nu,
    }


def dissipation_bound(nu, terms, initial_scaled_energy):
    """Absolute interval bound: initial_scaled_energy >= ||grad w(s)||^2 / b^4.
    Never subtract upper bounds. At s=0 this input is exactly zero.
    error_dissipation inside terms must bound the SAME interval absolutely.
    """
    return (8 / nu) * (initial_scaled_energy / 2 + sum(terms.values(), Iv.of(0)))


def evaluate():
    verify_inputs()
    val = json.loads((PARENT / 'absorption-b003/results/validated.json').read_text())
    old = json.loads((PARENT / 'absorption-b003/results/chain.json').read_text())
    assert val['provenance']['complete'] and old['verdict'] == 'CERTIFIED'
    with localcontext(TRAP):
        T, nu, beta = Iv.of('1/4'), Iv.of('1/28'), Iv.of('3/1000')
        CA = Iv.of(old['C_A'])
        K, Nw, S1, eps0, eps1, delta = [Iv.of(old[k]) for k in
                                     ('K', 'N_w', 'S1', 'eps0', 'eps1', 'delta2')]
        assert (CA * (beta * S1 + beta.sq() * K)).hi < (nu / 2).lo
        assert (beta * CA * eps1).hi < (nu / 8).lo
        # Global analytic sup bounds: alpha <= 1, increasing gamma derivatives at T.
        er = (-nu * T).exp()
        e1, e2 = (1 - er) / nu, (1 - er.sq()) / (2 * nu)
        g1 = 1 + 2 * e1
        g2 = 1 + 4 * e1 + (4 / nu) * (e1 - e2)
        M1 = (5 + g1.sq()).sqrt()
        M2 = (5 + 2 * g1.sq() + g2.sq()).sqrt()
        MD = (1 + (2 + g2).sq()).sqrt()
        # JSON floats are exact binary upper endpoints, not rounded display strings.
        def maximum(key):
            return Iv.of(max(Decimal(x) for x in val['cells'][key]))
        p, n1, n2, sn = [maximum(k) for k in
                         ('sup_absq', 'sup_absgradq', 'sup_abshessq', 'sup_gradq')]
        sigma = p * sn + n1 * eps0 + p * eps1
        terms = dissipation_terms(nu, beta, CA, M1, M2, n1, n2, K, Nw, sigma, eps1, T, delta)
        Dw = dissipation_bound(nu, terms, Iv.of(0))
        # Example valid arbitrary later coarse-cell bound. Global delta is also a
        # valid absolute error-dissipation bound on a subinterval, but is loose.
        cell_terms = dissipation_terms(nu, beta, CA, M1, M2, n1, n2, K, Nw, sigma,
                                      eps1, T / 250, delta)
        Dw_cell = dissipation_bound(nu, cell_terms, K.sq())
        # q2 bounds are informative only; observable proof uses its support, not norms.
        Lsigma = T * sigma + CA * eps1 * (T * delta).sqrt()
        Jsigma = 2 * (T * sigma.sq() + CA.sq() * eps1.sq() * delta)
        N2, Q2, D2 = linear_bounds(M1, M2, nu, T, Lsigma, Jsigma)
        # r=w-b^2 q2, whose full forcing scales as |b|^3.
        A = p * K + n1 * Nw
        H = CA * (eps1 + beta * K)
        Lr = A * T + CA * K * (T * delta).sqrt() + H * (T * Dw).sqrt()
        Jr_parts = {'smooth_q': 3 * A.sq() * T,
                    'q_error': 3 * CA.sq() * K.sq() * delta,
                    'w_dissipation': 3 * H.sq() * Dw}
        Jr = sum(Jr_parts.values(), Iv.of(0))
        Nr, Er, Dr = linear_bounds(M1, M2, nu, T, Lr, Jr)
        # Mean forcing: cubic q1-q2 terms have zero z mean.
        mean_parts = {'smooth_q': (p * Er + n1 * Nr) * T,
                      'q_error_advection': CA * Er * (T * delta).sqrt(),
                      'q_error_gradient': CA * eps1 * (T * Dr).sqrt(),
                      'w_self_interaction': CA * K * (T * Dw).sqrt()}
        Nbar = ((M1 - nu) * T).exp() * sum(mean_parts.values(), Iv.of(0))
        CZ_parts = {'mean_field': MD * Nbar, 'cross_field': S1 * Er, 'w_energy': K.sq() / 2}
        CZ = sum(CZ_parts.values(), Iv.of(0))
        RZ = beta.sq().sq() * CZ
        # Route A displayed rounded bound, independently reproduced previously.
        route_a = Iv.of('1.2102e14') * beta.sq().sq()
        vals = dict(T=T, nu=nu, beta=beta, CA=CA, M1=M1, M2=M2, MDelta=MD,
                    p=p, n1=n1, n2=n2, sigma=sigma, S1=S1, K=K, Nw=Nw,
                    eps0=eps0, eps1=eps1, delta_e=delta,
                    Dw=Dw, physical_Dw=beta.sq().sq()*Dw,
                    arbitrary_cell_Dw=Dw_cell, initial_energy_cell_term=4*K.sq()/nu,
                    N2=N2, Q2=Q2, D2=D2, Lr=Lr, Jr=Jr, Nr=Nr, Er=Er, Dr=Dr,
                    Nbar=Nbar, CZ=CZ, RZ_at_beta=RZ, route_a_RZ_at_beta=route_a)
        def pack(x):
            return {'lo': str(x.lo), 'hi': str(x.hi), 'upper_5sig': str(c.round_up(x.hi))}
        return {
            'status': 'derived interval bound; independent mathematical review pending',
            'base_commit': BASE, 'scope': 'a=c=d=1, nu=1/28, phi=37/100, T=1/4, |b|<=3/1000',
            'milestone': {'threshold': '0.01', 'strict_upper_bound_below_threshold': RZ.hi < Decimal('0.01')},
            'inputs_sha256': PINNED, 'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'trajectory_array_hashes_in_verified_inputs': old['trajectory_sha256'],
            'bounds': {k: pack(v) for k, v in vals.items()},
            'Dw_energy_terms': {k: pack(v) for k, v in terms.items()},
            'Jr_terms': {k: pack(v) for k, v in Jr_parts.items()},
            'mean_source_terms': {k: pack(v) for k, v in mean_parts.items()},
            'CZ_terms': {k: pack(v) for k, v in CZ_parts.items()},
        }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise FileExistsError('Refusing to overwrite output: ' + str(args.output))
    result = evaluate()
    with args.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    for k in ('Dw', 'physical_Dw', 'N2', 'Q2', 'D2', 'Nr', 'Er', 'Dr', 'Nbar', 'CZ', 'RZ_at_beta', 'route_a_RZ_at_beta'):
        print(k + ' <= ' + result['bounds'][k]['upper_5sig'])
    print('Fixed milestone below 0.01:', result['milestone']['strict_upper_bound_below_threshold'])
    print(result['status'])

if __name__ == '__main__':
    main()
