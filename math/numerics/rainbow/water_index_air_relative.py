# Rainbow: refractive index of liquid water relative to air (IAPWS R9-97 divided by the
# Edlen-type index of standard air), compared with the Quan & Fry (1995) fit, at 20 C and 10 C;
# bow angles at 400, 700 and 750 nm; the wavelength that corresponds to n = 1.331 (red) and
# n = 1.343 (violet); and the 400-700 nm colour widths.
# Run from this folder: python3 -I water_index_air_relative.py   (standard library only, <1 s)
# Formerly numerics/_raw/review2-num2.py.

from math import *
import importlib.util,sys
a=[0.244257733,9.74634476e-3,-3.73234996e-3,2.68678472e-4,1.58920570e-3,2.45934259e-3,0.900704920,-1.66626219e-2]
LUV=0.2292020; LIR=5.432937
def n_vac(lam_nm,TC=20.0,rho=None):
    T=TC+273.15
    if rho is None: rho=1000*(1-(TC+288.9414)/(508929.2*(TC+68.12963))*(TC-3.9863)**2)
    rb=rho/1000; Tb=T/273.15; lb=(lam_nm/1000)/0.589
    A=rb*(a[0]+a[1]*rb+a[2]*Tb+a[3]*lb**2*Tb+a[4]/lb**2+a[5]/(lb**2-LUV**2)+a[6]/(lb**2-LIR**2)+a[7]*rb**2)
    return sqrt((2*A+1)/(1-A))
# IAPWS official check value: T=0C, rho=1000, lam=0.589 um -> 1.33434 (approx)
print("IAPWS check (0C, rho=1000, 589nm):", round(n_vac(589,0,1000),5))
def n_air(lam_nm):  # Edlen-type dispersion of standard air
    s=1/(lam_nm/1000)**2
    return 1+1e-8*(8342.54+2406147/(130-s)+15998/(38.9-s))
def n_iapws_air(lam,TC): return n_vac(lam,TC)/n_air(lam)
def n_qf(lam,T=20.0,S=0.0):  # Quan & Fry 1995, relative to air, 400-700 nm
    return (1.31405+(1.779e-4-1.05e-6*T+1.6e-8*T*T)*S-2.02e-6*T*T+(15.868+0.01155*S-0.00423*T)/lam-4382/lam**2+1.1455e6/lam**3)
print("lambda   IAPWS/air 20C  IAPWS/air 10C  QuanFry 20C  QuanFry 10C")
for lam in [400,404.7,410,420,450,486.1,550,589.3,656.3,680,700,720,750]:
    print(f"{lam:6.1f}   {n_iapws_air(lam,20):.5f}       {n_iapws_air(lam,10):.5f}       {n_qf(lam,20):.5f}     {n_qf(lam,10):.5f}")
def refr(n,i): return asin(sin(i)/n)
def dev(k,n,i): return k*pi+2*i-2*(k+1)*refr(n,i)
def binc(k,n): return acos(sqrt((n*n-1)/(k*(k+2))))
def prim(n): return degrees(pi-dev(1,n,binc(1,n)))
def sec(n): return degrees(dev(2,n,binc(2,n))-pi)
def solve(f,t,lo,hi):
    flo=f(lo)-t
    for _ in range(200):
        m=(lo+hi)/2
        if (f(m)-t)*flo>0: lo=m; flo=f(m)-t
        else: hi=m
    return (lo+hi)/2
print()
for TC in (20,10):
    print(f"--- {TC} C (air-relative IAPWS) ---")
    for lam in (400,700,750):
        n=n_iapws_air(lam,TC); print(f"  {lam} nm: n={n:.5f} primary {prim(n):.3f}  secondary {sec(n):.3f}")
    for nt in (1.331,1.343,solve(sec,50,1.25,1.45)):
        lam=solve(lambda l:n_iapws_air(l,TC),nt,350,1000); print(f"  n={nt:.5f} <-> {lam:.0f} nm")
    nr,nv=n_iapws_air(700,TC),n_iapws_air(400,TC)
    print(f"  widths 400-700nm: primary {prim(nr)-prim(nv):.3f}, secondary {sec(nv)-sec(nr):.3f}")
