"""A ceiling on the radius that condition (1) of ../PROOF.md can certify, at the tested
parameters a = c = d = 1, nu = 1/28.

Condition (1) of PROOF.md section 2 reads |b| F_s <= nu exp(-K_s INT M_s) / (2 K_s), so the
largest |b| it can certify is

    r_s(K_s, I_s) = nu exp(-K_s I_s) / (2 K_s F_s),   I_s = int_0^inf M_s dt,
    M_s(t) = sup_phi ||U(t, phi)||_{s+1},   F_s = ||sin(z) e_y||_s = 2^((s-1)/2).

PROOF.md never evaluates K_s or I_s. The ceiling below uses only three facts:

  1. r_s decreases in K_s > 0 and in I_s > 0, so lower bounds on both give an upper bound on r_s.
  2. K_s must satisfy the second inequality of section 2, ||P(h.grad f)||_s <= K_s ||f||_{s+1} ||h||_s,
     for every pair (f, h); the test pair f = sin(y) e_x, h = sin(z) e_y gives
     K_s >= kappa_s = (sqrt(3)/2)^s / sqrt(2).
  3. U = (a e^(-nu t) sin y, 0, w), and the H^(s+1) norm is a sum over components and modes, so
     M_s(t) >= ||a e^(-nu t) sin(y) e_x||_{s+1} = |a| e^(-nu t) 2^(s/2), hence I_s >= |a| 2^(s/2) / nu.

So r_s <= nu exp(-kappa_s I_s^low) / (2 kappa_s F_s) whatever values the uncomputed constants
take. The script checks kappa_s, F_s and the shear norm with exact FFT norms on an 8^3 grid,
shows that the ceiling decreases with s (so s = 4 is the largest case), and checks that the
radius beta of section 4 (R >= 8) obeys the same kind of ceiling, which is smaller still.

Run from this folder:  python3 -I -B radius_ceiling.py > radius_ceiling.log
Standard library and NumPy only; under a second.
"""
import math
import platform

import numpy as np

A, NU = 1.0, 1.0 / 28.0          # a = c = d = 1 (c and d do not enter the ceiling), nu = 1/28
TESTED_B = (0.05, 0.1)           # the b values of the stored simulations
n = 8                            # 8^3 grid: exact for the degree-1 trigonometric fields used here
x = 2 * np.pi * np.arange(n) / n
X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
k1 = np.fft.fftfreq(n, d=1.0 / n)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2
KV = np.stack([KX, KY, KZ])


def coef(f):
    """Normalized Fourier coefficients of a real vector field f of shape (3, n, n, n)."""
    return np.fft.fftn(f, axes=(1, 2, 3)) / n**3


def hnorm(fh, s):
    """||f||_s^2 = sum_k (1 + |k|^2)^s |f_k|^2 with normalized coefficients."""
    return math.sqrt(float(((1 + K2)**s * (np.abs(fh)**2).sum(axis=0)).sum()))


def leray(fh):
    kd = (KV * fh).sum(axis=0)
    return fh - KV * np.where(K2 > 0, kd / np.where(K2 > 0, K2, 1), 0)


def grad(fh_comp):
    """Spectral gradient of one scalar component, returned in physical space (3, n, n, n)."""
    return np.stack([np.real(np.fft.ifftn(1j * KV[j] * fh_comp) * n**3) for j in range(3)])


zero = np.zeros_like(X)
f_shear = np.stack([np.sin(Y), zero, zero])      # f = sin(y) e_x  (the shear direction of U)
h_pert = np.stack([zero, np.sin(Z), zero])       # h = sin(z) e_y  (the b perturbation)
fh, hh = coef(f_shear), coef(h_pert)
# (h . grad) f, component i = sum_j h_j d_j f_i
adv = np.stack([sum(h_pert[j] * grad(fh[i])[j] for j in range(3)) for i in range(3)])
Bh = leray(coef(adv))

print('radius_ceiling.py: ceiling on the radius certified by PROOF.md condition (1)')
print(f'python {platform.python_version()}, numpy {np.__version__}')
print(f'parameters: a = c = d = 1, nu = 1/28; (h.grad)f is divergence-free, so P leaves it '
      f'unchanged: max |P(h.grad f) - h.grad f| = {np.max(np.abs(Bh - coef(adv))):.1e}')
print()
print(' s   kappa_s (FFT)  kappa_s (formula)  F_s (FFT)  F_s (formula)  I_s lower = 2^(s/2)/nu'
      '   log10 ceiling of r_s')
rows = []
for s in range(4, 13):
    kap_fft = hnorm(Bh, s) / (hnorm(fh, s + 1) * hnorm(hh, s))
    kap = (math.sqrt(3) / 2)**s / math.sqrt(2)
    F_fft, F = hnorm(hh, s), 2**((s - 1) / 2)
    shear_fft, shear = hnorm(fh, s + 1), 2**(s / 2)
    assert abs(kap_fft - kap) < 1e-12 * kap and abs(F_fft - F) < 1e-12 * F
    assert abs(shear_fft - shear) < 1e-12 * shear
    I_low = abs(A) * shear / NU
    log10_r = math.log10(NU / (2 * kap * F)) - kap * I_low / math.log(10)
    rows.append((s, log10_r))
    print(f'{s:2d}   {kap_fft:.10f}   {kap:.10f}      {F_fft:9.4f}  {F:9.4f}       '
          f'{I_low:12.1f}             {log10_r:9.3f}')
# the ceiling falls with s for every s >= 4: kappa_s I_s and kappa_s F_s both grow like (3/2)^(s/2)
logs = [math.log10(NU) - (1.5**(s / 2)) * (abs(A) / (math.sqrt(2) * NU)) / math.log(10)
        - math.log10(1.5**(s / 2)) for s in range(4, 200)]
assert all(b < a for a, b in zip(logs, logs[1:]))
assert all(abs(l - r) < 1e-9 for l, (_, r) in zip(logs, rows))
s, log10_r4 = rows[0]
r4 = 10**log10_r4
print()
print(f'Largest ceiling (s = 4): radius certified by (1) <= {r4:.3e}   (log10 = {log10_r4:.3f})')
print('The ceiling decreases strictly in s for 4 <= s < 200 (checked; analytically, kappa_s I_s and')
print('kappa_s F_s are both (3/2)^(s/2) times constants), so it holds for every admissible s.')
for b in TESTED_B:
    print(f'tested b = {b}: b / ceiling = {b / r4:.2e}')
k3 = (math.sqrt(3) / 2)**3 / math.sqrt(2)
print(f's = 3 (allowed by the remark in PROOF.md section 2): ceiling {NU * math.exp(-k3 * abs(A) * 2**1.5 / NU) / (2 * k3 * 2.0):.2e}')

# section 4: beta = min(1, nu e^(-A)/(2 K F_R)), A = K int M_R, K >= every K_j, 4 <= j <= R, R >= 8
print()
print('Section 4 radius beta (R >= 8, K >= kappa_4 because K dominates the level-4 constants):')
kap4 = (math.sqrt(3) / 2)**4 / math.sqrt(2)
for R in (8, 9, 10):
    log10_beta = (math.log10(NU / (2 * kap4 * 2**((R - 1) / 2)))
                  - kap4 * abs(A) * 2**(R / 2) / NU / math.log(10))
    assert log10_beta < log10_r4
    print(f'  R = {R:2d}: beta <= 10^({log10_beta:.2f}), below the s = 4 ceiling')
