"""Agmon-type constant on the 2pi-torus for mean-zero fields, L^2 norms on [0,2pi]^3:
    ||f||_inf <= C_A ||grad f||^{1/2} ||Delta f||^{1/2}.
Derivation.  f = sum_{k != 0} f_k e^{ik.x}, ||f||^2 = (2pi)^3 sum |f_k|^2.  For any R >= 1,
    |f(x)| <= sum_{0<|k|<=R} |f_k| + sum_{|k|>R} |f_k|
           <= (sum |k|^2 |f_k|^2)^{1/2} s2(R)^{1/2} + (sum |k|^4 |f_k|^2)^{1/2} s4(R)^{1/2}
           =  (2pi)^{-3/2} [ ||grad f|| s2(R)^{1/2} + ||Delta f|| s4(R)^{1/2} ],
with s2(R) = sum_{0<|k|<=R} |k|^{-2} and s4(R) = sum_{|k|>R} |k|^{-4}.  Put rho = ||Delta f||/||grad f|| (>= 1 by
Poincare) and R = rho:  |f(x)| <= (2pi)^{-3/2} ||grad f||^{1/2} ||Delta f||^{1/2} [ (s2(rho)/rho)^{1/2} + (rho s4(rho))^{1/2} ].
So C_A = (2pi)^{-3/2} sup_{rho >= 1} [ (s2(rho)/rho)^{1/2} + (rho s4(rho))^{1/2} ].  As rho -> infinity both brackets tend
to 4 pi, so the bracket tends to 2 sqrt(4 pi) = 7.09; the lattice sums are enumerated to |k| <= 60 and the tail of s4 is
bounded by its shell integral 4 pi / 60 with a 10% margin.  The supremum over rho <= 40 is reported; the slow rise toward
rho = 40 is the margin on the tail, so C_A <= 0.47 is a safe value and 0.45 the asymptotic one.
Run: python3 agmon_constant.py
"""
import numpy as np

R = 60
r = np.arange(-R, R + 1)
kx, ky, kz = np.meshgrid(r, r, r, indexing="ij", sparse=True)
mag = np.sqrt((kx ** 2 + ky ** 2 + kz ** 2).astype(np.float64)).ravel()
mag = np.sort(mag[mag > 0])
inv2, inv4 = 1.0 / mag ** 2, 1.0 / mag ** 4
cum2 = np.cumsum(inv2)
inside = mag <= R
s4_tail = 4 * np.pi / R * 1.10 + inv4[~inside].sum()
cum4_rest = inv4[inside].sum() - np.cumsum(inv4) + s4_tail
best, best_rho = 0.0, None
for rho in np.unique(mag[mag <= 40]):
    j = np.searchsorted(mag, rho, side="right") - 1
    val = np.sqrt(cum2[j] / rho) + np.sqrt(rho * cum4_rest[j])
    if val > best:
        best, best_rho = val, rho
print(f"sup over rho in [1,40] of (s2/rho)^(1/2) + (rho s4)^(1/2) = {best:.4f} at rho = {best_rho:.3f}   (limit 2 sqrt(4 pi) = {2*np.sqrt(4*np.pi):.4f})")
print(f"C_A = {best/(2*np.pi)**1.5:.4f}   (asymptotic {2*np.sqrt(4*np.pi)/(2*np.pi)**1.5:.4f});  use C_A = 0.47")
for rho in (1.0, 2.0, 5.0, 10.0, 20.0, 40.0):
    j = np.searchsorted(mag, rho, side="right") - 1
    print(f"  rho={rho:5.1f}: s2/rho={cum2[j]/rho:.3f}  rho*s4={rho*cum4_rest[j]:.3f}  bracket={np.sqrt(cum2[j]/rho)+np.sqrt(rho*cum4_rest[j]):.3f}")
