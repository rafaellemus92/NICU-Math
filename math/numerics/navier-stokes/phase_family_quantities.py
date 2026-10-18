# Periodic Navier-Stokes, phase family u_phi: E, Z, D = <|grad omega|^2> and S on a 24^3 grid,
# with the derivatives written out by hand (no FFT), for phi in {0, 0.7, pi/3, 2}.
# Columns: phi, E, Z, D, S, cos(phi)/4.
# Run from this folder: python3 -I phase_family_quantities.py   (numpy only, <1 s)
# Formerly numerics/_raw/limreview-num/pf.py.

import numpy as np
N=24
g=np.arange(N)*2*np.pi/N
X,Y,Z=np.meshgrid(g,g,g,indexing='ij')
for phi in [0.0,0.7,np.pi/3,2.0]:
    P=X+Y+phi
    # vorticity
    w1=np.sin(P)-np.cos(Z); w2=np.sin(X)-np.sin(P); w3=-np.cos(Y)
    # grad u: u1=sin y, u2=sin z, u3=cos x - cos P
    du=[[0*X,np.cos(Y),0*X],[0*X,0*X,np.cos(Z)],[-np.sin(X)+np.sin(P),np.sin(P),0*X]]
    w=[w1,w2,w3]
    S=np.mean(sum(w[i]*du[i][j]*w[j] for i in range(3) for j in range(3)))
    # grad w
    dw=[[np.cos(P),np.cos(P),np.sin(Z)],[np.cos(X)-np.cos(P),-np.cos(P),0*X],[0*X,np.sin(Y),0*X]]
    D=np.mean(sum(dw[i][j]**2 for i in range(3) for j in range(3)))
    E=np.mean(np.sin(Y)**2+np.sin(Z)**2+(np.cos(X)-np.cos(P))**2)/2
    Zs=np.mean(w1**2+w2**2+w3**2)/2
    print(phi,E,Zs,D,S,np.cos(phi)/4)
