# Periodic Navier-Stokes, phase family: evaluates each mode list printed by
# phase_family_modes.py at 5 random points (x, y, z, phi) and compares it with the closed-form
# integrand; prints True when they agree to 1e-12.
# Run from this folder: python3 -I phase_family_modes_check.py   (numpy only, <1 s)
# Formerly numerics/_raw/check.py (now locates phase_family_modes.py next to itself).

import numpy as np, re, os
_here = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_here, 'phase_family_modes.py'), encoding='utf-8').read().split("for n,f in")[0])
rng=np.random.default_rng(1)
def ev(s,phi):
    s=s.replace("cos φ","cos(phi)").replace("sin φ","sin(phi)").replace("φ","phi").replace("cos","np.cos").replace("sin","np.sin")
    return eval(s,{"np":np,"phi":phi})
def parse(lst):
    # split top-level tuples
    out=[];depth=0;cur=""
    for ch in lst[1:-1]:
        if ch=='(':
            depth+=1
            if depth==1: cur=""; continue
        if ch==')':
            depth-=1
            if depth==0: out.append(cur); continue
        if depth>=1: cur+=ch
    res=[]
    for t in out:
        parts=[];d=0;c=""
        for ch in t:
            if ch=='(' : d+=1
            if ch==')' : d-=1
            if ch==',' and d==0: parts.append(c.strip()); c=""; continue
            c+=ch
        parts.append(c.strip()); res.append(parts)
    return res
def tp(L,x,y,z,phi):
    s=0
    for a,b,p,q,r in L:
        t=int(p)*x+int(q)*y+int(r)*z
        s+=ev(a,phi)*np.cos(t)+ev(b,phi)*np.sin(t)
    return s
for name,f in [("energy",energy),("enst",enst),("palin",palin),("stretch",stretch)]:
    L=parse(modes(f))
    for _ in range(5):
        x,y,z,phi=rng.uniform(-4,4,4)
        sx,cx,sy,cy,sz,cz=np.sin(x),np.cos(x),np.sin(y),np.cos(y),np.sin(z),np.cos(z)
        a=np.sin(x+y+phi);A=np.cos(x+y+phi)
        val={"energy":sy**2+sz**2+(cx-A)**2,
             "enst":(a-cz)**2+(sx-a)**2+cy**2,
             "palin":3*A**2+sz**2+(cx-A)**2+sy**2,
             "stretch":cy*(sx-a)*(a-3*cz)}[name]
        print(name, abs(val-tp(L,x,y,z,phi))<1e-12)
