# Periodic Navier-Stokes, scaling counterexample: v_k = (sin ky, sin kz, cos kx - cos(kx+ky)).
# Checks E = 1, Z = 5k^2/4, D = 7k^4/2, S = k^3/4 for k = 1..4 with spectral derivatives (N = 48)
# and, independently, 4th-order finite differences (N = 64, 128), and the ratio
# S / (Z^0.75 D^0.2) against its predicted value, which grows like k^0.7.
# Run from this folder: python3 -I scaling_counterexample.py   (numpy only, ~7 s)
# Formerly numerics/_raw/scalreview-num/check.py.

import numpy as np
from fractions import Fraction

def spectral_deriv(f, axis, N):
    kk = np.fft.fftfreq(N, d=1.0/N)  # integer wavenumbers on [0,2pi)
    shape = [1,1,1]; shape[axis] = N
    kk = kk.reshape(shape)
    return np.real(np.fft.ifftn(1j*kk*np.fft.fftn(f)))

def fd_deriv(f, axis, h):
    # 4th-order periodic central difference, independent check
    return (-np.roll(f,-2,axis) + 8*np.roll(f,-1,axis) - 8*np.roll(f,1,axis) + np.roll(f,2,axis))/(12*h)

def quantities(k, N, deriv):
    t = 2*np.pi*np.arange(N)/N
    x, y, z = np.meshgrid(t, t, t, indexing='ij')
    u = [np.sin(k*y), np.sin(k*z), np.cos(k*x) - np.cos(k*x + k*y)]
    d = lambda f, a: deriv(f, a)
    G = [[d(u[i], j) for j in range(3)] for i in range(3)]  # G[i][j] = d_j u_i
    div = G[0][0] + G[1][1] + G[2][2]
    w = [G[2][1] - G[1][2], G[0][2] - G[2][0], G[1][0] - G[0][1]]
    Gw = [[d(w[i], j) for j in range(3)] for i in range(3)]
    avg = np.mean
    E = avg(sum(ui**2 for ui in u))/2
    Z = avg(sum(wi**2 for wi in w))/2
    D = avg(sum(Gw[i][j]**2 for i in range(3) for j in range(3)))
    S = avg(sum(w[i]*G[i][j]*w[j] for i in range(3) for j in range(3)))
    return E, Z, D, S, np.max(np.abs(div))

for k in (1, 2, 3, 4):
    N = 48
    E, Z, D, S, dv = quantities(k, N, lambda f,a: spectral_deriv(f, a, N))
    exp = (1.0, 5*k**2/4, 7*k**4/2, k**3/4)
    print(f"k={k} spectral N={N}: E={E:.12f} Z={Z:.12f} D={D:.12f} S={S:.12f} max|div|={dv:.2e}")
    print(f"      expected      : E={exp[0]:.12f} Z={exp[1]:.12f} D={exp[2]:.12f} S={exp[3]:.12f}")
    errs = [abs(a-b) for a,b in zip((E,Z,D,S), exp)]
    print("      abs errors:", ["%.1e" % e for e in errs])
    # finite differences, refined grid, independent of FFT
    for Nf in (64, 128):
        h = 2*np.pi/Nf
        Ef, Zf, Df, Sf, dvf = quantities(k, Nf, lambda f,a: fd_deriv(f, a, h))
        print(f"      FD4 N={Nf}: E={Ef:.8f} Z={Zf:.8f} D={Df:.8f} S={Sf:.8f}")
    a, b = 0.75, 0.2
    ratio = S/(Z**a * D**b)
    pred = 0.25/((5/4)**a*(7/2)**b) * k**(3-2*a-4*b)
    print(f"      S/(Z^.75 D^.2)={ratio:.12f}  predicted={pred:.12f}")

# phase-zero vs negative sign sanity: S of -v is -1/4 (sign flip), shows S is the cubic term
