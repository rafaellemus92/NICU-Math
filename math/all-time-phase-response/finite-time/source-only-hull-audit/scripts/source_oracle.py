"""Independent, non-rigorous oracle: advective form 1/2 Re[Q_a d_a conj(Q_i) - i Q_3 conj(Q_i)] by FFT on a 64^2 grid,
then Leray on (kx,ky,0) and Parseval norm. Different formula and arithmetic from the flux-form interval kernel."""
import sys, json
import numpy as np
traj, hull_json = sys.argv[1], sys.argv[2]
Q = np.load(traj + '/Q_nodes.npy', mmap_mode='r')
rows = json.load(open(hull_json))['rows']
U = np.array([float(r['source_norm_upper_exact']) for r in rows])
N = 64
kk = np.fft.fftfreq(N, 1.0 / N)
KX, KY = np.meshgrid(kk, kk, indexing='ij')
ks = np.arange(-10, 11)
KXs, KYs = np.meshgrid(ks, ks, indexing='ij')
K2s = KXs ** 2 + KYs ** 2 + 1.0
def project_q(B):                       # B: (m,3,21,21) raw -> exact-in-float Leray on (kx,ky,1)
    dot = KXs * B[:, 0] + KYs * B[:, 1] + B[:, 2]
    return B - np.stack([KXs, KYs, np.ones_like(KXs)])[None] * (dot / K2s)[:, None]
idx = np.array([k % N for k in range(-10, 11)])
def to_grid(C):                         # (m,3,21,21) small coefficients -> (m,3,N,N) full-grid coefficients
    G = np.zeros(C.shape[:2] + (N, N), complex)
    G[:, :, idx[:, None], idx[None, :]] = C
    return G
def source_norms(P):                    # P: projected coefficients (m,3,21,21)
    G = to_grid(P)
    q = np.fft.ifft2(G, axes=(-2, -1), norm='forward')
    qx = np.fft.ifft2(1j * KX * G, axes=(-2, -1), norm='forward')
    qy = np.fft.ifft2(1j * KY * G, axes=(-2, -1), norm='forward')
    f = 0.5 * np.real(q[:, 0:1] * np.conj(qx) + q[:, 1:2] * np.conj(qy) - 1j * q[:, 2:3] * np.conj(q))   # (m,3,N,N)
    Fh = np.fft.fft2(f, axes=(-2, -1), norm='forward')
    k2 = KX ** 2 + KY ** 2
    dot = KX * Fh[:, 0] + KY * Fh[:, 1]
    with np.errstate(invalid='ignore', divide='ignore'):
        corr = np.where(k2 > 0, dot / np.where(k2 > 0, k2, 1), 0)
    Fh[:, 0] -= KX * corr; Fh[:, 1] -= KY * corr
    zero_mode = np.abs(Fh[:, :, 0, 0]).max(axis=1)
    # support check: no energy beyond |kx|,|ky| <= 20
    outside = (np.abs(KX) > 20) | (np.abs(KY) > 20)
    leak = np.sqrt((np.abs(Fh[:, :, outside]) ** 2).sum(axis=(1, 2)))
    return np.sqrt((np.abs(Fh) ** 2).sum(axis=(1, 2, 3))), zero_mode, leak
node = np.empty(12501); mid = np.empty(12500); zm = 0.0; lk = 0.0
B = 250
prev_last = None
for s in range(0, 12501, B):
    e = min(s + B, 12501)
    P = project_q(np.asarray(Q[s:e]))
    n, z, l = source_norms(P); node[s:e] = n; zm = max(zm, z.max()); lk = max(lk, l.max())
    allP = P if prev_last is None else np.concatenate([prev_last[None], P])
    M = 0.5 * (allP[1:] + allP[:-1])            # midpoints of fine cells (affine path)
    m0 = s - (0 if prev_last is None else 1)
    if len(M):
        mn, z2, l2 = source_norms(M); mid[m0:m0 + len(M)] = mn
    prev_last = P[-1]
cell_of_node_max = np.array([node[50 * l:50 * l + 51].max() for l in range(250)])
cell_of_mid_max = np.array([mid[50 * l:50 * l + 50].max() for l in range(250)])
worst = np.maximum(cell_of_node_max, cell_of_mid_max)
print('max over cells of (oracle sup / hull bound):', float((worst / U).max()), ' min:', float((worst / U).min()))
print('any oracle value above its hull bound:', bool((worst > U).any()))
print('max |zero mode| of oracle source:', zm, '  max energy outside |k|<=20:', lk)
trap = (node[:-1] + node[1:]).sum() / 2 / 50000
print('trapezoid estimate of integral ||F_N||  (non-rigorous):', trap)
print('hull rigorous L_N:', U.sum() / 1000, '  ratio hull/estimate:', U.sum() / 1000 / trap)
print('||F_N|| at t=0, 0.125, 0.25:', node[0], node[6250], node[12500])
