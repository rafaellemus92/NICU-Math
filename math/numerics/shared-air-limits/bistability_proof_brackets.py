# Shared Air limits: the numbers the Lean proofs in WyrdMathlib/Limits/Bistability.lean rely on.
# * f(y, g) at the intermediate-value brackets y = 1.3, 1.4 (g = 2.1) and y = 2.79, 2.792 (g = 3);
# * the g = 3 co-arousal equilibrium, its Jacobian eigenvalues and the Routh-Hurwitz quantity
#   c2 c1 - c0 (printed as p[1] p[2] - p[3]);
# * the minimum of the one-variable polynomial f2(u) of bist_f2_pos on [0, 10];
# * the minimum of the g <= 2 positivity bound Phi(g, u) on (0, 2] x [0, 20].
# Run from this folder: python3 -I bistability_proof_brackets.py   (numpy only, <1 s)
# Formerly numerics/_raw/num.py.

import numpy as np
def cap(y): return 1/(1+(y/0.8)**2)
def capD(y): return -(2*y/0.64)/(1+(y/0.8)**2)**2
def xf(y,g): return y*(1/20+0.02*y**2)/(0.1*g)
def f(y,g):
    x=xf(y,g); z=0.3*g*x*cap(y)
    return -x/30 - z + 0.04*g*y - 0.02*x**3
for g,ys in [(2.1,[1.3,1.4]),(3,[2.79,2.792])]:
    for y in ys: print(g,y,xf(y,g),f(y,g))
# root at g=3
lo,hi=2.79,2.792
for _ in range(60):
    m=(lo+hi)/2
    if f(m,3)>0: lo=m
    else: hi=m
y=lo; x=xf(y,3); g=3
J=np.array([[-1/30-0.06*x**2,0.04*g,-1],[0.1*g,-1/20-0.06*y**2,0],[0.3*g*cap(y)/4,0.3*g*x*capD(y)/4,-1/4]])
print("y",y,"x",x,"cap",cap(y),"capD",capD(y))
print(np.linalg.eigvals(J))
p=np.poly(J); print(p, p[1]*p[2]-p[3])
# f2
u=np.linspace(0,10,100001)
w=0.05+0.02*u; A=0.64+u
f2=A*w/30+0.5*u*w**3*A+0.384*w-0.016*A
print(f2.min(), u[f2.argmin()])
# check Phi positivity on g in (0,2]
G=np.linspace(0.01,2,400)[:,None]
U=np.linspace(0,20,4001)[None,:]
W=0.05+0.02*U
Phi=(1/30+0.192*G/(0.64+U)+2*U*W**2/G**2)*W-0.004*G**2
print(Phi.min())
