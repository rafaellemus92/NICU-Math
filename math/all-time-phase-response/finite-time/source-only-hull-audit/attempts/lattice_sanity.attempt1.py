# Flawed first lattice sanity estimate, preserved verbatim from the audit (run as python3 -I -c).
# Flaw: truncates on the cube [-R,R]^3 but adds the tail 4 pi/(R+0.5) for the region OUTSIDE A BALL;
# the region outside the cube is a strict subset, so the tail is overestimated by roughly 0.02.
import numpy as np
R=200; r=np.arange(-R,R+1,dtype=np.float64); s4=0.0; sl=0.0
for x in r:
    k2=(x*x+r[:,None]**2+r[None,:]**2); k2=k2[k2>0]; s4+=(1/k2**2).sum(); sl+=(1/(1e6+k2**2)).sum()
tail4=4*np.pi/(R+0.5); print('sum |k|^-4 ~', s4+tail4, ' C_A^2 =', 4.06707921080**2); print('A_lambda(1e6) ~', sl+tail4, ' Ahat <= 0.474521867')
