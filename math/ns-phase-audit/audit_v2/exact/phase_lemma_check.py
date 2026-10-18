#!/usr/bin/env python3
"""Second, structurally different exact implementation (generic Gaussian
rationals, NO phase lemma, conservative form of the nonlinearity, numeric
rational nu) used to verify the main code nsseries.py.

  (u.grad)u = div(u (x) u)  ->  mode K:  i * sum_{P+Q=K} (k . c_P) c_Q
  U_{n+1} = [nu Lap U_n - P sum_j N(U_j,U_{n-j})]/(n+1)
  Z_n = 1/2 sum_j sum_{K,K'; k'=-k} omega_j(K) . omega_{n-j}(K')  ->  e^{i(m+m')phi}
  omega(K) = i k x c(K)  (computed with complex arithmetic)

Checks: (a) phase lemma: c real iff kx odd, purely imaginary iff kx even;
(b) reality: c(-K) = conj c(K); (c) Z_n identical to nsseries at this nu.
usage: phase_lemma_check.py N nu alpha beta gamma delta
"""
import sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])

Z0 = (Fr(0), Fr(0))


def gadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def gmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gscale(s, x):
    return (s * x[0], s * x[1])


I = (Fr(0), Fr(1))


def initial(a, b, g, d):
    h = Fr(1, 2)
    U = {}
    def put(K, comp, val):
        v = U.setdefault(K, [Z0, Z0, Z0])
        v[comp] = gadd(v[comp], val)
    # a sin y = a (e^{iy} - e^{-iy})/(2i)
    put((0, 1, 0, 0), 0, (Fr(0), -a * h)); put((0, -1, 0, 0), 0, (Fr(0), a * h))
    put((0, 0, 1, 0), 1, (Fr(0), -b * h)); put((0, 0, -1, 0), 1, (Fr(0), b * h))
    put((1, 0, 0, 0), 2, (g * h, Fr(0))); put((-1, 0, 0, 0), 2, (g * h, Fr(0)))
    # -d cos(x+y+phi) = -d/2 (e^{i(x+y+phi)} + e^{-i(...)})
    put((1, 1, 0, 1), 2, (-d * h, Fr(0))); put((-1, -1, 0, -1), 2, (-d * h, Fr(0)))
    return {K: v for K, v in U.items() if any(c != Z0 for c in v)}


def run(N, nu, amps):
    U = [initial(*amps)]
    for n in range(N):
        NL = {}
        for j in range(n + 1):
            A, Bd = U[j], U[n - j]
            for P, cp in A.items():
                for Q, cq in Bd.items():
                    K = tuple(p + q for p, q in zip(P, Q))
                    k = K[:3]
                    kc = gadd(gadd(gscale(k[0], cp[0]), gscale(k[1], cp[1])), gscale(k[2], cp[2]))
                    if kc == Z0:
                        continue
                    f = gmul(I, kc)
                    v = NL.setdefault(K, [Z0, Z0, Z0])
                    for c in range(3):
                        v[c] = gadd(v[c], gmul(f, cq[c]))
        new = {}
        for K in set(NL) | set(U[n]):
            k = K[:3]
            kk = sum(x * x for x in k)
            if kk == 0:
                assert all(c == Z0 for c in NL.get(K, [Z0] * 3))
                continue
            w = NL.get(K, [Z0, Z0, Z0])
            kw = gadd(gadd(gscale(k[0], w[0]), gscale(k[1], w[1])), gscale(k[2], w[2]))
            pw = [gadd(w[c], gscale(Fr(-k[c], kk), kw)) for c in range(3)]
            old = U[n].get(K, [Z0, Z0, Z0])
            v = [gscale(Fr(1, n + 1), gadd(gscale(-nu * kk, old[c]), gscale(-1, pw[c]))) for c in range(3)]
            if any(c != Z0 for c in v):
                new[K] = v
        U.append(new)
    # checks (a), (b)
    for n, Ud in enumerate(U):
        for K, v in Ud.items():
            for c in v:
                if K[0] % 2:
                    assert c[1] == 0, ("phase lemma (odd kx) fails", n, K, c)
                else:
                    assert c[0] == 0, ("phase lemma (even kx) fails", n, K, c)
            mK = tuple(-x for x in K)
            w = Ud[mK]
            for c in range(3):
                assert w[c] == (v[c][0], -v[c][1]), ("reality fails", n, K)
    # Z_n
    def curl(K, v):
        kx, ky, kz = K[:3]
        cr = [gadd(gscale(ky, v[2]), gscale(-kz, v[1])),
              gadd(gscale(kz, v[0]), gscale(-kx, v[2])),
              gadd(gscale(kx, v[1]), gscale(-ky, v[0]))]
        return [gmul(I, c) for c in cr]
    W = [{K: curl(K, v) for K, v in Ud.items()} for Ud in U]
    idx = []
    for Wd in W:
        d = {}
        for K, v in Wd.items():
            d.setdefault(K[:3], []).append((K[3], v))
        idx.append(d)
    Z = []
    for n in range(N + 1):
        tot = {}
        for j in range(n + 1):
            for K, v in W[j].items():
                mk = tuple(-x for x in K[:3])
                for m2, w in idx[n - j].get(mk, []):
                    s = Z0
                    for c in range(3):
                        s = gadd(s, gmul(v[c], w[c]))
                    m = K[3] + m2
                    tot[m] = gadd(tot.get(m, Z0), s)
        tot = {m: gscale(Fr(1, 2), s) for m, s in tot.items() if s != Z0}
        for m, s in tot.items():
            assert s[1] == 0, ("Z Laurent coefficient not real", n, m, s)
        Z.append({m: s[0] for m, s in tot.items()})
    return U, Z


def main():
    N = int(sys.argv[1]); nu = Fr(sys.argv[2]); amps = [Fr(x) for x in sys.argv[3:7]]
    U, Z = run(N, nu, amps)
    print(f"generic Gaussian-rational run: N={N} nu={nu} amps={[str(a) for a in amps]}")
    print("  phase lemma + reality condition: OK for all modes of U_0..U_%d" % N)
    from nsseries import series, laurent_series
    Um = series(*amps, N, verbose=False, prune=False)
    Zm = laurent_series(Um, N, 'curl')
    for n in range(N + 1):
        ev = {m: sum(Fr(c) * nu ** e for e, c in enumerate(p)) for m, p in Zm[n].items()}
        ev = {m: v for m, v in ev.items() if v}
        assert ev == Z[n], ("mismatch", n, ev, Z[n])
        # also check the velocity coefficients mode by mode
        for K, v in U[n].items():
            r = Um[n].get(K)
            assert r is not None, ("mode missing in main code", n, K)
            for c in range(3):
                val = sum(Fr(x) * nu ** e for e, x in enumerate(r[c]))
                exp_ = (val, Fr(0)) if K[0] % 2 else (Fr(0), val)
                assert exp_ == v[c], ("U mismatch", n, K, c)
        for K in Um[n]:
            if K not in U[n]:
                r = Um[n][K]
                assert all(sum(Fr(x) * nu ** e for e, x in enumerate(r[c])) == 0 for c in range(3)), ("extra mode", n, K)
        print(f"  n={n}: U_n (all {len(U[n])} modes) and Z_n Laurent coefficients agree exactly with nsseries.py")


if __name__ == '__main__':
    main()
