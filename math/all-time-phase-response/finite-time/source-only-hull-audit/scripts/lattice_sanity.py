# Corrected lattice sanity estimate (non-rigorous), preserved verbatim from the audit (run as python3 -I -c):
# ball truncation |k| <= R with the matching tail. The printed "literature value" string is a value recalled
# by the auditor and hard-coded; the computation itself is what confirms it.
import numpy as np
for R in (150, 300):
    r = np.arange(-R, R+1, dtype=np.float64); s4 = 0.0; sl = 0.0; R2 = R*R
    for x in r:
        k2 = x*x + r[:,None]**2 + r[None,:]**2
        m = (k2 > 0) & (k2 <= R2)
        k2 = k2[m]; s4 += (1/k2**2).sum(); sl += (1/(1e6 + k2**2)).sum()
    tail4 = 4*np.pi/R                                   # integral of 4 pi r^2 r^-4 over r > R
    taill = 4*np.pi*np.sum(1/(1e6/np.linspace(R, 40*R, 400001)**2 + np.linspace(R, 40*R, 400001)**2))*(39*R/400000) + 4*np.pi/(40*R)
    print(f'ball R={R}: sum |k|^-4 ~ {s4+tail4:.6f}   A_lambda(1e6) ~ {sl+taill:.6f}')
print('C_A^2 (certified upper) = 16.541133   literature value of the cubic-lattice sum: 16.532316 (Epstein zeta, s=2)')
