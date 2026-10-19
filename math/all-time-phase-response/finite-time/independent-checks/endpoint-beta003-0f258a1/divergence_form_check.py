"""Focused check of the normalization and signs in endpoint-beta003 NOTE.md's divergence-form step, on random
band-limited fields of the normalized 2pi-torus (|k|_inf <= 3, grid 24^3 resolves every product exactly; only
binary64 roundoff remains). W: divergence-free on T^3. X: divergence-free and z-independent. Checks:
 (i)   <P overline((W.grad)W), X> = <(W.grad)W, X>         (Leray and z-average drop against such X)
 (ii)  <(W.grad)W, X> = -<W (x) W, grad X>                  (periodic integration by parts, sign)
 (iii) |<W (x) W, grad X>| <= ||overline(W (x) W)|| ||grad X|| <= ||W (x) W|| ||grad X|| <= max|W| ||W|| ||grad X||
 (iv)  <(U.grad)X, X> = 0 for divergence-free U             (transport is skew)
Usage: python3 -I -B divergence_form_check.py"""
import numpy as np
rng = np.random.default_rng(20261019); n = 24; K = 3
k1 = np.fft.fftfreq(n, 1.0 / n); KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing='ij'); KK = np.stack([KX, KY, KZ])
avg = lambda f: f.mean()                                   # normalized average over T^3
ip = lambda A, B: avg(np.sum(A * B, axis=tuple(range(A.ndim - 3))))
nrm = lambda A: np.sqrt(ip(A, A))
def field(zfree=False):
    band = (np.abs(KX) <= K) & (np.abs(KY) <= K) & (np.abs(KZ) <= (0 if zfree else K)) & ((KX != 0) | (KY != 0) | (KZ != 0))
    Fh = (rng.normal(size=(3, n, n, n)) + 1j * rng.normal(size=(3, n, n, n))) * band
    k2 = np.where(band, (KK ** 2).sum(0), 1.0)
    Fh = Fh - KK * (np.sum(KK * Fh, 0) / k2)                # Leray projection: divergence-free
    f = np.real(np.fft.ifftn(Fh, axes=(1, 2, 3)))
    return f
def grad(f):                                               # grad[j][i] = d_j f_i
    fh = np.fft.fftn(f, axes=(-3, -2, -1))
    return np.stack([np.real(np.fft.ifftn(1j * KK[j] * fh, axes=(-3, -2, -1))) for j in range(3)])
def leray(f):
    fh = np.fft.fftn(f, axes=(1, 2, 3)); k2 = np.where((KK ** 2).sum(0) > 0, (KK ** 2).sum(0), 1.0)
    return np.real(np.fft.ifftn(fh - KK * (np.sum(KK * fh, 0) / k2), axes=(1, 2, 3)))
zmean = lambda f: np.broadcast_to(f.mean(axis=-1, keepdims=True), f.shape)
worst = dict(i=0.0, ii=0.0, iv=0.0); ratios = []
for trial in range(40):
    W, X, U = field(), field(zfree=True), field()
    gW, gX = grad(W), grad(X)
    adv = np.einsum('jxyz,jixyz->ixyz', W, gW)             # (W.grad)W
    WW = np.einsum('ixyz,jxyz->ijxyz', W, W)               # (W (x) W)_ij = W_i W_j, Frobenius norm |W|^2
    gXt = np.transpose(gX, (1, 0, 2, 3, 4))                # gXt[i][j] = d_j X_i
    lhs = ip(leray(zmean(adv)), X); direct = ip(adv, X); ibp = -ip(WW, gXt)
    scale = abs(direct) + 1e-300
    worst['i'] = max(worst['i'], abs(lhs - direct) / scale); worst['ii'] = max(worst['ii'], abs(direct - ibp) / scale)
    worst['iv'] = max(worst['iv'], abs(ip(np.einsum('jxyz,jixyz->ixyz', U, gX), X)) / (nrm(U) * nrm(gX) * nrm(X)))
    WWbar = zmean(WW)
    chain = [abs(ibp), nrm(WWbar) * nrm(gXt), nrm(WW) * nrm(gXt), np.sqrt((W ** 2).sum(0)).max() * nrm(W) * nrm(gXt)]
    assert all(chain[k] <= chain[k + 1] * (1 + 1e-12) for k in range(3)), chain
    ratios.append(chain[0] / chain[3])
print(f'(i) Leray and z-average drop: max rel. diff {worst["i"]:.1e}; (ii) integration by parts sign: max rel. diff {worst["ii"]:.1e}; '
      f'(iv) transport skew: max normalized |<(U.grad)X, X>| {worst["iv"]:.1e}')
print(f'(iii) the chain |<WW, grad X>| <= ||mean WW|| ||grad X|| <= ||WW|| ||grad X|| <= max|W| ||W|| ||grad X|| held in 40/40 trials; '
      f'tightness of the last bound: {min(ratios):.3f}..{max(ratios):.3f}')
assert max(worst.values()) < 1e-10
