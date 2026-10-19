"""Independent exact endpoint check: project each mode in rationals first, then sum (different route from endpoint.py)."""
import sys, json
from fractions import Fraction as Fr
import numpy as np
traj, ep_json = sys.argv[1], sys.argv[2]
Q = np.load(traj + '/Q_nodes.npy', mmap_mode='r')[12500]
W = np.load(traj + '/W_nodes.npy', mmap_mode='r')[12500]
tot = Fr(0)
maxdiv = Fr(0)
for ix in range(21):
    for iy in range(21):
        k = (ix - 10, iy - 10, 1)
        k2 = sum(x * x for x in k)
        qr = [Fr(float(Q[c, ix, iy].real)) for c in range(3)]
        qi = [Fr(float(Q[c, ix, iy].imag)) for c in range(3)]
        dr = sum(k[c] * qr[c] for c in range(3)); di = sum(k[c] * qi[c] for c in range(3))
        pr = [qr[c] - k[c] * dr / k2 for c in range(3)]; pi = [qi[c] - k[c] * di / k2 for c in range(3)]
        assert sum(k[c] * pr[c] for c in range(3)) == 0 and sum(k[c] * pi[c] for c in range(3)) == 0   # exactly solenoidal
        tot += k2 * sum(pr[c] ** 2 + pi[c] ** 2 for c in range(3))
gradsq = tot / 2                        # ||grad Re(e^{iz} P Q)||^2 = (1/2) sum |k|^2 |PQ|^2
wsq = Fr(0)
for i in range(43):
    n = i - 21
    wsq += (1 + n * n) ** 2 * (Fr(float(W[i].real)) ** 2 + Fr(float(W[i].imag)) ** 2)
wsq /= 2
ep = json.load(open(ep_json))
print('grad qN(T)^2 exact equals endpoint.json fraction:', str(gradsq) == ep['exact_endpoint_fractions']['projected_q_gradient_squared'])
print('base vertical Laplacian^2 equals endpoint.json fraction:', str(wsq) == ep['exact_endpoint_fractions']['base_vertical_laplacian_squared'])
print('||grad qN(T)|| ~', float(gradsq) ** 0.5, '  ||Delta w_N(T)||^2 ~', float(wsq))
json.dump({'gradsq': [gradsq.numerator, gradsq.denominator], 'wsq': [wsq.numerator, wsq.denominator]}, open(sys.argv[3], 'w'))
