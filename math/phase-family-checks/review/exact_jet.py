"""Referee check: exact rational time-Taylor jet of the enstrophy's e^{2 i phi} harmonic via the
package's nsseries module, separated by powers of b (Z is even in b), evaluated at nu=1/28.
Usage: python3 exact_jet.py NMAX
"""
import sys, time, importlib.util
from fractions import Fraction as F
PKG = str(__import__('pathlib').Path(__file__).resolve().parents[2]/'ns-phase-audit/audit_v2/exact/nsseries.py')
spec = importlib.util.spec_from_file_location('nsseries', PKG); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    nu = F(1, 28)
    bs = [F(1), F(1, 2), F(1, 3), F(1, 5)]
    t0 = time.time()
    cos2 = {}
    for b in bs:
        U = mod.series(F(1), b, F(1), F(1), NMAX, verbose=False)
        Z = mod.laurent_series(U, NMAX)
        cos2[b] = []
        for n in range(NMAX+1):
            p = Z[n].get(2, [])
            val = sum(F(c)*nu**e for e, c in enumerate(p))
            cos2[b].append(2*val)  # cosine convention: a_2 = Z[2]+Z[-2] = 2 Re Z[2]
    print('series time', time.time()-t0)
    # Z cos2 coefficient of t^n = sum_k b^{2k} c_{n,k}; solve with 4 b values for k=1..4
    import numpy as np
    for n in range(NMAX+1):
        A = [[float(b**(2*k)) for k in range(1, 5)] for b in bs]
        y = [float(cos2[b][n]) for b in bs]
        c = np.linalg.solve(np.array(A), np.array(y))
        # also exact rational for the b^2 part via two smallest b if higher powers vanish
        print(f't^{n}: cos2phi coefficient by b-power [b^2,b^4,b^6,b^8] =', c.tolist(),
              ' exact at b=1:', cos2[F(1)][n], ' at b=1/2:', cos2[F(1,2)][n])

if __name__ == '__main__':
    main()
