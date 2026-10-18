"""Crossing of Z_phiphi(T,0) from tangent data: accurate (cubic, 0.005 grid) vs linear
interpolation on coarser grids (0.01: between 1.76 and 1.77) to diagnose interpolation bias."""
import numpy as np, sys
D = './'
for N in [int(a) for a in sys.argv[1:]]:
    d = np.load(D + f'c3_tan_N{N}_dt0.005.npz')
    t, Z2 = d['t'], d['Z2']
    def at(T): return Z2[int(round(T / 0.005))]
    a, b = at(1.76), at(1.77)
    lin01 = 1.76 + 0.01 * (-a) / (b - a)
    a5, b5 = at(1.76), at(1.765)
    lin005 = 1.76 + 0.005 * (-a5) / (b5 - a5) if np.sign(a5) != np.sign(b5) else float('nan')
    # high-accuracy: 6-point Lagrange on 0.005 grid around the root, solved by bisection
    i0 = int(round(1.7525 / 0.005)); tt = t[i0:i0 + 6]; yy = Z2[i0:i0 + 6]
    P = np.polyfit(tt - 1.765, yy, 5)
    lo, hi = 1.76, 1.77
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if np.sign(np.polyval(P, mid - 1.765)) == np.sign(np.polyval(P, lo - 1.765)): lo = mid
        else: hi = mid
    print(f'N={N}: Z_pp(1.76)={a:+.10e} Z_pp(1.77)={b:+.10e} | linear(0.01 grid)={lin01:.7f} '
          f'linear(0.005 grid)={lin005:.7f} quintic(0.005 grid)={0.5*(lo+hi):.7f}')
