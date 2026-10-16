"""Sanity checks: Z(0)=5/4, E(0)=1, dZ/dt(0)=cos(phi)/4-7nu/2, energy identity
(n+1)E_{n+1} = -2 nu Z_n, rotational vs advective form, mask on/off, grid N vs larger N, timing."""
import time, numpy as np
from nsseries import Grid, series
nmax=12
g=Grid(28)
for phi,nu in [(0.0,0.0),(0.7,1/28),(2.1,1/7)]:
    p=np.exp(1j*phi); q=np.exp(-1j*phi)
    t=time.time(); r=series(1,1,1,p,q,nu,nmax,g,diag=True); dt=time.time()-t
    Z,E=r['Z'],r['E']
    print(f"phi={phi} nu={nu:.5f} time={dt:.2f}s")
    print("  Z0-5/4 =",Z[0]-1.25," E0-1 =",E[0]-1)
    print("  Z1 - (cos phi/4 - 7nu/2) =",Z[1]-(np.cos(phi)/4-3.5*nu))
    ident=[(n+1)*E[n+1]+2*nu*Z[n] for n in range(nmax)]
    print("  max |(n+1)E_{n+1}+2nu Z_n| =",max(abs(x) for x in ident))
    print("  max rel content outside support before mask:",max(r['outside']))
    print("  max |Im Z_n| =",np.abs(Z.imag).max())
    ra=series(1,1,1,p,q,nu,nmax,g,form='adv')
    print("  max |Z_rot-Z_adv| per order:",np.abs(Z-ra['Z']).max(), " rel:",np.max(np.abs(Z-ra['Z'])/np.abs(Z)))
    rn=series(1,1,1,p,q,nu,nmax,g,mask=False)
    print("  max rel |mask - nomask|:",np.max(np.abs(Z-rn['Z'])/np.abs(Z)))
    g2=Grid(40)
    r2=series(1,1,1,p,q,nu,nmax,g2)
    print("  max rel |N28 - N40|:",np.max(np.abs(Z-r2['Z'])/np.abs(Z)))
    print("  Z_n:",' '.join(f"{z.real:.6e}" for z in Z))
