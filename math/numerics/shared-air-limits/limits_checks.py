# Shared Air limits, several independent checks:
# 1. harmonic lock index of a perfect n:m lock for k = 1..5;
# 2. first-order resonant averages of sin(l theta) P(psi) along n:m orbits;
# 3. saddle-node coupling where co-arousal equilibria appear, and Routh-Hurwitz at g = 3;
# 4. the clinical values (Q10 per degree, chest warmth in bpm, warming after 12 min);
# 5. margin of the "rest only" bound for 0 < g <= 2, and f(y, 3) / RH near the g = 3 equilibrium.
# Run from this folder: python3 -I limits_checks.py   (numpy only, ~4 s)
# Formerly numerics/_raw/limits/checks.py.

import numpy as np, math, cmath
# 1. Synchrogram harmonic index under perfect n:m locking
def index(k,n,m,psi0=0.3):
    return abs(sum(cmath.exp(1j*k*(psi0+2*math.pi*m*j/n)) for j in range(n))/n)
for (n,m) in [(2,1),(3,1),(3,2),(5,3),(4,3)]:
    print(f"{n}:{m}", [round(index(k,n,m),12) for k in (1,2,3,4,5)])
# 2. first-order resonant average of sin(l*theta)*P(psi), theta=n s+a, psi=m s+b
P=lambda x: np.exp(2*(np.cos(x)-1)) - np.exp(-2)*np.i0(2) # minus its exact mean e^{-2} I0(2) = 0.3085083226 (the page's PMEAN)
s=np.linspace(0,2*np.pi,200001)[:-1]; ds=s[1]-s[0]
def avg(l,n,m,a=0.4,b=1.1): return float(np.sum(np.sin(l*(n*s+a))*P(m*s+b))*ds)
for (l,n,m) in [(1,2,1),(1,3,1),(1,3,2),(1,5,3),(1,4,3),(2,3,2),(3,5,3),(2,5,3)]:
    print("l,n,m",l,n,m, round(avg(l,n,m),10))
# 3. bistability: saddle-node threshold with cap; no-cap bound
a,b,d,r,q,h,kap=1/30,1/20,1/4,1/25,1/10,3/40,0.02
cap=lambda y:1/(1+(y/0.8)**2)
def f(y,g,withcap=True):
    x=y*(b+kap*y*y)/(q*g)
    return -a*x-(h/d)*g*x*(cap(y) if withcap else 1)+r*g*y-kap*x**3
def nroots(g):
    ys=np.linspace(1e-4,10,200001); v=f(ys,g); return int(np.sum(v[:-1]*v[1:]<0))
lo,hi=2.0,2.1
for _ in range(50):
    mid=(lo+hi)/2
    if nroots(mid)>0: hi=mid
    else: lo=mid
print("saddle-node g_sn ~", (lo+hi)/2)
# margin of no-root at g=2: max of f over y>0 (f<0 means no equilibrium)
ys=np.linspace(1e-4,10,2000001); print("g=2 max f:", f(ys,2.0).max(), "at y=", ys[f(ys,2.0).argmax()])
# RH coefficients at stable co-arousal eq g=3
g=3.0
ys=np.linspace(2.7,2.9,2000001); v=f(ys,g); i=np.where(v[:-1]*v[1:]<0)[0][0]; y=ys[i]; x=y*(b+kap*y*y)/(q*g)
capd=lambda y: -2*y/0.64/(1+y*y/0.64)**2
J=np.array([[-a-3*kap*x*x, r*g, -1],[q*g, -b-3*kap*y*y, 0],[h*g*cap(y), h*g*x*capd(y), -d]])
c2=-np.trace(J); c1=(J[0,0]*J[1,1]-J[0,1]*J[1,0])+(J[0,0]*J[2,2]-J[0,2]*J[2,0])+(J[1,1]*J[2,2]-J[1,2]*J[2,1]); c0=-np.linalg.det(J)
print("g=3 eq x,y:",x,y,"RH c2,c1,c0:",c2,c1,c0,"c2c1-c0:",c2*c1-c0, "eig:",np.linalg.eigvals(J))
print("f at 2.7, 2.9:", f(2.7,3), f(2.9,3))
# 4. values
print("Q10 per degree", 2.2**0.1, "0.35C:",2.2**0.035, 140*(2.2**0.035-1), "12 min fraction", 1-math.exp(-720/400))
print("---- margins")
def F(y,g):
    x=y*(b+kap*y*y)/(q*g); return (a+(h/d)*g*cap(y)+kap*x*x)*(b+kap*y*y)-r*q*g*g
ys=np.linspace(1e-6,20,400001)
worst=min((F(ys,g).min(),g) for g in np.linspace(0.01,2.0,400))
print("min over g in (0,2], y>0 of F:", worst)
print("F min at g=2:", F(ys,2.0).min(), ys[F(ys,2.0).argmin()])
for yy in (2.78,2.79,2.791,2.792,2.80): print("f(",yy,",3)=",f(yy,3))
def RH(y,g=3.0):
    x=y*(b+kap*y*y)/(q*g)
    J=np.array([[-a-3*kap*x*x, r*g, -1],[q*g, -b-3*kap*y*y, 0],[h*g*cap(y), h*g*x*capd(y), -d]])
    c2=-np.trace(J); c1=(J[0,0]*J[1,1]-J[0,1]*J[1,0])+(J[0,0]*J[2,2]-J[0,2]*J[2,0])+(J[1,1]*J[2,2]-J[1,2]*J[2,1]); c0=-np.linalg.det(J)
    return c2,c1,c0,c2*c1-c0
for yy in np.linspace(2.7,2.9,5): print(yy, RH(yy))
