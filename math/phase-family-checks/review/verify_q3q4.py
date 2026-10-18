"""Referee check of PROOF.md Sections 4-5: extend the variational system to q3 and q4,
then measure (i) z-mode support and J-parity of q_j, (ii) the vanishing inner products
that make the observable polynomial even, (iii) the CUBIC-truncation field remainder
u_b-U-b q1-b^2 q2-b^3 q3 (PROOF eq. (4): should scale like b^4, ratio 16),
(iv) raw observable remainders minus the explicit b^4 coefficient (should be O(b^6), ratio 64),
(v) u_{-b} = J u_b on the full solve.  N=18, nu=1/28, T=.5, dt=.005, phi=.37 as in the package.
"""
import sys, json, time
import numpy as np
PKG = str(__import__('pathlib').Path(__file__).resolve().parents[2]/'all-time-phase-response')
sys.path.insert(0, PKG)
from response import Response, audit, integrate

NQ = 5  # fields U,q1,q2,q3,q4

class Resp4(Response):
    def initial(self, phi, a=1., c=1., d=1.):
        Y = super().initial(phi, a, c, d)
        return np.concatenate([Y, np.zeros((NQ-3,)+Y.shape[1:], dtype=Y.dtype)])
    def rhs(self, Y):
        g = self.g
        u = [g.inv(v) for v in Y]
        w = [g.inv(g.curl_h(v)) for v in Y]
        return np.stack([g.proj(g.fwd(sum(np.cross(u[j], w[n-j], axis=0) for j in range(n+1)))) - self.visc*Y[n]
                         for n in range(NQ)])
    def obs_coeff(self, Y, order):
        """b^order coefficient of (E,Z,S) of U+b q1+...; q_0=U."""
        g = self.g
        E = .5*sum(g.inner(Y[i], Y[order-i]) for i in range(order+1))
        W = [g.curl_h(v) for v in Y]
        Z = .5*sum(g.inner(W[i], W[order-i]) for i in range(order+1))
        S = sum(self.tri(Y[i], Y[j], Y[order-i-j]) for i in range(order+1) for j in range(order+1-i))
        return np.array([E, Z, S])

def J(g, vh):
    """translation z -> z+pi on half spectra: multiply by (-1)^kz"""
    return vh*np.cos(np.pi*g.kvec[2])

def main():
    t0 = time.perf_counter()
    N, nu, T, dt, phi = 18, 1/28, .5, .005, .37
    s = Resp4(N, nu); full = audit.NS(N, nu); g = s.g
    Y = integrate(s, s.initial(phi), T, dt)
    out = {'params': dict(N=N, K=g.K, nu=nu, T=T, dt=dt, phi=phi)}
    # (i) z-support and parity
    supp = {}
    for j in range(NQ):
        kz = g.kvec[2]
        amp = np.abs(Y[j]).max(axis=(0, 1, 2))  # over components & kx,ky -> per kz
        present = [int(k) for k in np.unique(kz[0]) if amp[..., ] is not None and np.abs(Y[j][:, :, :, int(k)]).max() > 1e-13]
        par = float(np.abs(J(g, Y[j]) - (-1)**j*Y[j]).max())
        supp[f'q{j}'] = {'kz_support(half spectrum, kz>=0)': present, 'J_parity_residual': par,
                         'max_abs': float(np.abs(Y[j]).max())}
    out['support_parity'] = supp
    # (ii) inner products
    ip = {'<U,q1>': g.inner(Y[0], Y[1]), '<q1,q2>': g.inner(Y[1], Y[2]), '<U,q3>': g.inner(Y[0], Y[3]),
          '<q1,q3>': g.inner(Y[1], Y[3]), '<q2,q2>/2': .5*g.inner(Y[2], Y[2]), '<U,q4>': g.inner(Y[0], Y[4]),
          '<U,q2>': g.inner(Y[0], Y[2]), '<q1,q1>/2': .5*g.inner(Y[1], Y[1])}
    out['inner_products'] = ip
    O = [s.obs_coeff(Y, k) for k in range(5)]
    out['obs_coeffs_E_Z_S_order0to4'] = [o.tolist() for o in O]
    out['second_matches_package_formula'] = float(np.abs(O[2] - s.second(Y[:3])).max())
    # full solves
    cases = {}
    for b in [.1, .05, .025]:
        rec = {}
        up = integrate(full, full.init_family(phi, b=b), T, dt)
        um = integrate(full, full.init_family(phi, b=-b), T, dt)
        rec['J_u_plus_minus_u_minus_maxabs'] = float(np.abs(J(g, up) - um).max())
        for sign, u in [('+', up), ('-', um)]:
            bb = sign == '+' and b or -b
            r2 = u - Y[0] - bb*Y[1] - bb**2*Y[2]
            r3 = r2 - bb**3*Y[3]
            r4 = r3 - bb**4*Y[4]
            rec[f'field_L2_rem_order2{sign}'] = float(np.sqrt(g.inner(r2, r2)))
            rec[f'field_L2_rem_order3{sign}'] = float(np.sqrt(g.inner(r3, r3)))
            rec[f'field_L2_rem_order4{sign}'] = float(np.sqrt(g.inner(r4, r4)))
            rec[f'field_H1like_rem_order3{sign}'] = float(np.sqrt(2*g.enstrophy(r3)))
            q = s.quantities(u)
            rec[f'raw_obs_rem{sign}'] = (q - O[0] - bb**2*O[2]).tolist()
            rec[f'obs_rem_after_b4{sign}'] = (q - O[0] - bb**2*O[2] - bb**4*O[4]).tolist()
            rec[f'obs_odd_poly_b1+b3{sign}'] = (bb*O[1] + bb**3*O[3]).tolist()
        cases[str(b)] = rec
    out['cases'] = cases
    def ratio(key, b1, b2):
        a = np.array(cases[str(b1)][key]); c = np.array(cases[str(b2)][key])
        return (np.abs(a)/np.abs(c)).tolist()
    out['ratios'] = {
        'field_order2 .1/.05 (target 8)': ratio('field_L2_rem_order2+', .1, .05),
        'field_order3 .1/.05 (target 16)': ratio('field_L2_rem_order3+', .1, .05),
        'field_order3 .05/.025 (target 16)': ratio('field_L2_rem_order3+', .05, .025),
        'field_order4 .1/.05 (target 32)': ratio('field_L2_rem_order4+', .1, .05),
        'field_order4 .05/.025 (target 32)': ratio('field_L2_rem_order4+', .05, .025),
        'fieldH1_order3 .1/.05 (target 16)': ratio('field_H1like_rem_order3+', .1, .05),
        'raw_obs .1/.05 (target 16)': ratio('raw_obs_rem+', .1, .05),
        'raw_obs .05/.025 (target 16)': ratio('raw_obs_rem+', .05, .025),
        'obs_after_b4 .1/.05 (target 64)': ratio('obs_rem_after_b4+', .1, .05),
        'obs_after_b4 .05/.025 (target 64)': ratio('obs_rem_after_b4+', .05, .025),
    }
    out['wall_seconds'] = time.perf_counter() - t0
    print(json.dumps(out, indent=1, default=float))

if __name__ == '__main__':
    main()
