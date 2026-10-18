import math
NA=6.02214076e23; c=299792458.0; hbar_eVs=6.582119569e-16; hbarc=197.3269804
mp=0.93827208816
print("=== particles ===")
print("mH/mp",125.13/mp, 125.20/mp)
for G in (3.0e6,2.3e6,4.5e6): print("tau",hbar_eVs/G, "ctau fm", hbarc/(G/1e6))
GF=1.1663787e-5; print("v",(math.sqrt(2)*GF)**-0.5)
print("rW",hbarc/80362.5*1e-15,"rW(80369.2)",hbarc/80369.2*1e-15,"rZ",hbarc/91187.9*1e-15, hbarc/91188.0*1e-15)
n=993.33*NA/0.0180153; print("n",n,"spacing A",n**(-1/3)*1e10)
rW=hbarc/80362.5*1e-15; rZ=hbarc/91187.9*1e-15
print(2.80e-10/rW, 3.111e-10/rW, 2.80e-10/rZ, 3.111e-10/rZ)
print("nu water",691.3e-6/993.33)
print("=== GUT ===")
print(2.4e34/13.797e9, 70/1.66054e-27, 70/1.66054e-27/2.4e34)
print("p fraction protons in body ~", )
print("sigma",(3-2.9840)/0.0082,(3-2.9963)/0.0074)
print("=== weak coupling ===")
E=13.605693122994e-9 # GeV
print("GF E^2",GF*E**2, "alpha",1/137.035999177, "ratio",GF*E**2*137.035999177)
print("GF mp^2",GF*mp**2, GF*mp**2*137.036)
h=6.62607015e-34;k=1.380649e-23; me=9.1093837015e-31
for m in (70,me): print("lambda",h/math.sqrt(2*math.pi*m*k*310))
import numpy as np
sz=np.array([[1,0],[0,-1]])
def U(t): return np.diag(np.exp(-1j*t*np.diag(sz)/2))
print(np.round(U(2*np.pi),10),np.round(U(4*np.pi),10))
print((720-716.8)/3.8)
print("=== DM ===")
GeVkg=1.782661921e-27
for rho in (0.2,0.3,0.4,0.47,0.55,0.6):
    M=rho*7e4; print(rho,M,"GeV",M*GeVkg,"kg",M/mp,"mp")
print("frac",0.4*7e4*GeVkg/70)
for m in (100,40,1): print(m,0.4*7e4/m)
print("cross",1/233e3)
mO=15.9949146*0.93149410372; mchi=40
muN=mO*mchi/(mO+mchi); mun=0.93957*mchi/(0.93957+mchi); mup=mp*mchi/(mp+mchi)
print("muN",muN,"mun",mun,"mup",mup)
sN=2.2e-48*16**2*(muN/mun)**2; print("sigmaN",sN)
NT=70e3/15.9949146*NA; print("NT",NT)
nchi=0.4/40; v=233e5
rate=nchi*v*sN*NT; print("rate/s",rate,"/yr",rate*365.25*86400,"yrs per",1/(rate*365.25*86400))
# also realistic average speed ~ maxwellian mean speed ~ sqrt(8/(3pi))*v0*... skip
print("Planck Om_c h^2/ ... 26.4%, 84.4%")
print(0.1200/(0.1200+0.02237))
