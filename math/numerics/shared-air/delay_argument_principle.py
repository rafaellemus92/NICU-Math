# Shared Air, delayed linearisation: argument-principle count of characteristic roots in
# the right half-plane (contour: imaginary axis plus a semicircle of radius 50).
# Checks: 0 roots below and 2 roots above the critical delay (g = 3: tau 1.83 vs 1.84;
# g = 1: tau 4.76 vs 4.765); g_c = (h b + sqrt(h^2 b^2 + 4 a b c d^2)) / (2 c d); the count on
# either side of g_c at tau = 0 and tau = 3; and the optimal coupling g* from H(s*) = 0.
# Run from this folder: python3 -I delay_argument_principle.py   (numpy only, ~2 s)
# Formerly numerics/_raw/fureview-num/argp.py (dead placeholder lines removed).

import numpy as np
a,b,d,c,h=1/30,1/20,1/4,1/250,3/40
def D(s,g,tau):
    E=np.exp(-s*tau)
    return (s+a)*(s+b)*(s+d)+h*g*(s+b)*E-c*g**2*(s+d)*E**2
def count_rhp(g,tau,R=50.0,n=400000):
    # contour: up the imaginary axis (shifted slightly right by eps), then RHP semicircle back
    eps=1e-9
    # counterclockwise around RHP: -iR -> +iR along axis is upward (RHP on the right -> clockwise). So go +iR -> -iR along axis, then semicircle -iR -> +iR through R.
    axis=eps+1j*np.linspace(R,-R,n)
    arc=eps+R*np.exp(1j*np.linspace(-np.pi/2,np.pi/2,n))
    path=np.concatenate([axis,arc])
    v=D(path,g,tau)
    ang=np.unwrap(np.angle(v))
    return (ang[-1]-ang[0])/(2*np.pi)
for g,taus in [(3,[0,1.0,1.83,1.84,2.0,5.0]),(1,[0,4.7,4.76,4.765,6.0])]:
    for t in taus:
        print(g,t,round(count_rhp(g,t),3))
# gc
gc=(h*b+np.sqrt(h**2*b**2+4*a*b*c*d**2))/(2*c*d); print('gc',gc)
for g in [3.85,3.87]:
    print(g,'tau0',round(count_rhp(g,0),3),'tau3',round(count_rhp(g,3),3))
# g* check
from numpy.polynomial import polynomial as Pn
# H(s)=(s+a)(s+d)^2 + h^2/(4c)(s+b)
coef=np.poly1d([1,a])*np.poly1d([1,d])**2+np.poly1d([h**2/(4*c)*1, h**2/(4*c)*b])
r=[x.real for x in coef.r if abs(x.imag)<1e-12 and -b<x.real<-a]
s=r[0]; print('s*',s,'g*',h/(2*c)*(s+b)/(s+d))
