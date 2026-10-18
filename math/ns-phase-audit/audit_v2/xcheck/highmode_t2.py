"""Independent check of package test claim: the t^2 coefficient of energy/enstrophy in
|k|^2>2 modes is 7/48 and 9/16 (= 1/2 |B(U0,U0)_high|^2 terms). U1 = nu Lap U0 + B(U0,U0);
nu Lap U0 lives on |k|^2<=2, so high-mode part of U1 is P[-(U0.grad)U0] restricted."""
import numpy as np
from fractions import Fraction
N = 16
x = 2*np.pi*np.arange(N)/N
X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
k = np.fft.fftfreq(N, 1.0/N)
KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij")
K2 = KX**2+KY**2+KZ**2
def F(f): return np.fft.fftn(f)/N**3
def Fi(fh): return np.real(np.fft.ifftn(fh*N**3))
for phi in [0.0, 0.7, 2.3]:
    u = [np.sin(Y), np.sin(Z), np.cos(X)-np.cos(X+Y+phi)]
    uh = [F(c) for c in u]
    grad = lambda fh: [Fi(1j*KX*fh), Fi(1j*KY*fh), Fi(1j*KZ*fh)]
    adv = []
    for i in range(3):
        g = grad(uh[i]); adv.append(F(-(u[0]*g[0]+u[1]*g[1]+u[2]*g[2])))
    kd = KX*adv[0]+KY*adv[1]+KZ*adv[2]
    k2i = np.where(K2>0, 1.0/np.where(K2>0,K2,1), 0)
    B = [adv[0]-KX*kd*k2i, adv[1]-KY*kd*k2i, adv[2]-KZ*kd*k2i]
    hi = K2 > 2.5
    E = 0.5*sum((np.abs(b)**2*hi).sum() for b in B)
    Zs = 0.5*sum((np.abs(b)**2*K2*hi).sum() for b in B)
    print(f"phi={phi}: high-mode E_t2={E:.15f} (7/48={7/48:.15f}), Z_t2={Zs:.15f} (9/16={9/16:.15f})",
          Fraction(E).limit_denominator(1000), Fraction(Zs).limit_denominator(1000))
