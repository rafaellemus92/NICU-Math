#!/usr/bin/env python3
"""Driver: exact Z_n (and E_n) Laurent coefficients in e^{i m phi}, polynomials in nu.
usage: run_series.py N alpha beta gamma delta out.json [--noprune]
Checks performed: div-free of every U_n mode, zero mean of advection,
exact energy identity (n+1) E_{n+1} = -2 nu Z_n (pruning keeps E_n exact for n<=N).
"""
import sys, json, time
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nsseries import series, laurent_series, check_divfree, fstr, poly_str


def main():
    N = int(sys.argv[1])
    amps = [Fr(x) for x in sys.argv[2:6]]
    out = sys.argv[6]
    prune = '--noprune' not in sys.argv
    t0 = time.time()
    print(f"N={N} amps={[str(a) for a in amps]} prune={prune}", flush=True)
    U = series(*amps, N, prune=prune)
    check_divfree(U)
    Z = laurent_series(U, N, 'curl')
    E = laurent_series(U, N, 'vel')
    # energy identity  (n+1) E_{n+1} = -2 nu Z_n
    for n in range(N):
        lhs = {m: [(n + 1) * x for x in p] for m, p in E[n + 1].items()}
        rhs = {m: [0] + [-2 * x for x in p] for m, p in Z[n].items()}
        ms = set(lhs) | set(rhs)
        for m in ms:
            a = lhs.get(m, [0] * (n + 2)); b = rhs.get(m, [0] * (n + 2))
            L = max(len(a), len(b)); a = a + [0] * (L - len(a)); b = b + [0] * (L - len(b))
            assert all(x == y for x, y in zip(a, b)), ("energy identity fails", n, m, a, b)
    print("energy identity (n+1)E_{n+1} = -2 nu Z_n : OK for n=0..%d" % (N - 1))
    res = {"N": N, "amps": [fstr(a) for a in amps], "Z": {}, "E": {},
           "modes": [len(u) for u in U], "seconds": None}
    for n in range(N + 1):
        res["Z"][n] = {m: [fstr(x) for x in Z[n][m]] for m in sorted(Z[n])}
        res["E"][n] = {m: [fstr(x) for x in E[n][m]] for m in sorted(E[n])}
        print(f"Z_{n}: harmonics {sorted(Z[n])}")
        for m in sorted(Z[n]):
            if m >= 0:
                print(f"   m={m:+d}: {poly_str(Z[n][m])}")
    res["seconds"] = time.time() - t0
    print(f"total {res['seconds']:.1f}s")
    with open(out, 'w') as f:
        json.dump(res, f, indent=1)


if __name__ == '__main__':
    main()
