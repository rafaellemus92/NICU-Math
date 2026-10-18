# Shared Air, delayed linearisation: Newton iteration from a grid of starting points
# (method 3 of 3). Prints the two rightmost characteristic roots at a few (g, tau) and the
# delay at which stability is lost for g = 3 and g = 1 (bisection on the rightmost real part).
# Run from this folder: python3 -I delay_newton_roots.py   (numpy only, ~45 s)
# Formerly numerics/_raw/delaycheck.py (an unused scipy import at the end was removed).

import numpy as np
a,b,d,c,h = 1/30,1/20,1/4,1/250,3/40
def D(s,g,tau):  return (s+a)*(s+b)*(s+d) + h*g*(s+b)*np.exp(-s*tau) - c*g*g*(s+d)*np.exp(-2*s*tau)
def dD(s,g,tau):
    return ((s+b)*(s+d)+(s+a)*(s+d)+(s+a)*(s+b) + h*g*np.exp(-s*tau)*(1 - tau*(s+b))
            - c*g*g*np.exp(-2*s*tau)*(1 - 2*tau*(s+d)))
def roots(g,tau):
    found=[]
    for x0 in np.linspace(-0.5,0.5,41):
        for y0 in np.linspace(0,3,61):
            s=complex(x0,y0)
            for _ in range(80):
                f=D(s,g,tau); fp=dD(s,g,tau)
                if fp==0: break
                s-=f/fp
                if abs(s)>50: break
            if abs(s)<50 and abs(D(s,g,tau))<1e-11 and not any(abs(s-r)<1e-7 for r in found):
                found.append(s)
    return sorted(found,key=lambda z:-z.real)
for g,tau in [(3,0),(3,1.5),(3,2.0),(1,1.5),(1,5.0)]:
    r=roots(g,tau)[:2]; print(f"g={g} tau={tau}: rightmost roots {[f'{z.real:+.4f}{z.imag:+.4f}i' for z in r]}")
# critical tau via bisection on the rightmost real part (method 1: Newton root sets)
def maxre(g,tau): return roots(g,tau)[0].real
for g in [3,1]:
    lo,hi = (1.5,2.0) if g==3 else (4.0,5.5)
    for _ in range(30):
        mid=(lo+hi)/2
        if maxre(g,mid)<0: lo=mid
        else: hi=mid
    print(f"g={g}: stability lost at tau ≈ {lo:.4f}")
