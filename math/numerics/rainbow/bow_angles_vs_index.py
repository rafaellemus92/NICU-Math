# Rainbow: Descartes bow angles as a function of the refractive index n (primary, k = 1;
# secondary, k = 2): values at n = 4/3, 1.331, 1.343 and nearby, the colour widths, slopes,
# and the index at which each bow crosses 40..43 deg / 50..54 deg.
# Caveat: the IAPWS table and the wavelength lines at the end use the index relative to
# VACUUM. The bow needs the index relative to air; water_index_air_relative.py does that and
# supersedes the wavelengths printed here. The bow angles themselves depend only on n.
# Run from this folder: python3 -I bow_angles_vs_index.py   (standard library only, <1 s)
# Formerly numerics/_raw/review2-num.py.

from math import *
# IAPWS R9-97 refractive index of water
a=[0.244257733,9.74634476e-3,-3.73234996e-3,2.68678472e-4,1.58920570e-3,2.45934259e-3,0.900704920,-1.66626219e-2]
LUV=0.2292020; LIR=5.432937
def n_water(lam_nm,TC=20.0,rho=None):
    T=TC+273.15
    if rho is None:
        # approximate density of liquid water (kg/m3)
        rho=1000*(1-(TC+288.9414)/(508929.2*(TC+68.12963))*(TC-3.9863)**2)
    rb=rho/1000; Tb=T/273.15; lb=(lam_nm/1000)/0.589
    rhs=rb*(a[0]+a[1]*rb+a[2]*Tb+a[3]*lb**2*Tb+a[4]/lb**2+a[5]/(lb**2-LUV**2)+a[6]/(lb**2-LIR**2)+a[7]*rb**2)
    return sqrt((2*rhs+1)/(1-rhs))
print("IAPWS n(lambda), 20C and 10C:")
for lam in [380,400,404.7,410,420,434,450,486.1,500,550,589.3,600,656.3,680,700,720,750,780]:
    print(f"  {lam:6.1f} nm  20C n={n_water(lam,20):.5f}   10C n={n_water(lam,10):.5f}")
def refr(n,i): return asin(sin(i)/n)
def dev(k,n,i): return k*pi+2*i-2*(k+1)*refr(n,i)
def binc(k,n): return acos(sqrt((n*n-1)/(k*(k+2))))
def prim(n): return degrees(pi-dev(1,n,binc(1,n)))
def sec(n): return degrees(dev(2,n,binc(2,n))-pi)
print()
for n in [1.331,1.343,4/3,1.3307,1.3439,1.3311,1.3435]:
    print(f"n={n:.5f}: primary {prim(n):.4f} deg, secondary {sec(n):.4f} deg")
print("widths (1.331..1.343): primary %.4f, secondary %.4f"%(prim(1.331)-prim(1.343), sec(1.343)-sec(1.331)))
print("widths (1.3307..1.3439, ~700..400nm 20C): primary %.4f, secondary %.4f"%(prim(1.3307)-prim(1.3439), sec(1.3439)-sec(1.3307)))
# slopes
h=1e-6
print("dprim/dn per 0.001: %.4f deg; dsec/dn per 0.001: %.4f deg"%((prim(1.337+h)-prim(1.337-h))/(2*h)*1e-3,(sec(1.337+h)-sec(1.337-h))/(2*h)*1e-3))
# thresholds
def solve(f,target,lo,hi):
    for _ in range(200):
        m=(lo+hi)/2
        if (f(m)-target)*(f(lo)-target)>0: lo=m
        else: hi=m
    return (lo+hi)/2
print("primary=43 at n=%.5f ; primary=42 at n=%.5f ; primary=41 at n=%.5f; primary=40 at n=%.5f"%tuple(solve(prim,t,1.2,1.45) for t in (43,42,41,40)))
print("secondary=50 at n=%.5f ; 51 at n=%.5f ; 53 at n=%.5f ; 54 at n=%.5f"%tuple(solve(sec,t,1.25,1.45) for t in (50,51,53,54)))
# wavelength at thresholds
def lam_of_n(nt,TC=20): return solve(lambda l: n_water(l,TC),nt,300,1200)
for nt in [1.331,1.343,solve(sec,50,1.25,1.45),solve(prim,43,1.2,1.45)]:
    print(f"  n={nt:.5f} <-> lambda {lam_of_n(nt,20):.1f} nm at 20C, {lam_of_n(nt,10):.1f} nm at 10C")
