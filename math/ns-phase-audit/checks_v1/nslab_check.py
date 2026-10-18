# Independent spectral check of the periodic_ns_lab_v1 exact claims (numpy FFT, not their code).
import numpy as np
N=16
k1=np.fft.fftfreq(N,1/N); KX,KY,KZ=np.meshgrid(k1,k1,k1,indexing='ij'); K=[KX,KY,KZ]
K2=KX**2+KY**2+KZ**2; K2s=np.where(K2==0,1,K2)
x=np.arange(N)*2*np.pi/N; X,Y,Zc=np.meshgrid(x,x,x,indexing='ij')
F=lambda f: np.fft.fftn(f); Fi=lambda f: np.real(np.fft.ifftn(f))
def grad(f): fh=F(f); return [Fi(1j*K[j]*fh) for j in range(3)]
def proj(v):
    vh=[F(c) for c in v]; dot=sum(K[j]*vh[j] for j in range(3))
    return [Fi(vh[i]-K[i]*dot/K2s) for i in range(3)]
def lap(v): return [Fi(-K2*F(c)) for c in v]
def B(a,b): # -P[(a.grad) b]
    gb=[grad(c) for c in b]
    return proj([-(a[0]*gb[i][0]+a[1]*gb[i][1]+a[2]*gb[i][2]) for i in range(3)])
def curl(v):
    g=[grad(c) for c in v]
    return [g[2][1]-g[1][2], g[0][2]-g[2][0], g[1][0]-g[0][1]]
def avg(f): return float(np.mean(f))
def inner(a,b): return avg(sum(a[i]*b[i] for i in range(3)))
def add(*vs): return [sum(v[i] for v in vs) for i in range(3)]
def sc(c,v): return [c*vi for vi in v]
def filt(v,mask): return [Fi(F(c)*mask) for c in v]
worst=0
for phi in (0.0,0.7,np.pi/3,2.0,np.pi):
    for nu in (1/28,0.1,0.0):
        u=[np.sin(Y),np.sin(Zc),np.cos(X)-np.cos(X+Y+phi)]
        w=curl(u)
        S=avg(sum(w[i]*sum(grad(u[i])[j]*w[j] for j in range(3)) for i in range(3)))
        f=add(B(u,u),sc(nu,lap(u)))
        g=add(B(f,u),B(u,f),sc(nu,lap(f)))
        wt,wtt=curl(f),curl(g)
        Z1=inner(w,wt); Z2=inner(wt,wt)+inner(w,wtt)
        hi=(K2>2).astype(float)
        fh=filt(f,hi); Ehi=inner(fh,fh)/2; Zhi=inner(curl(fh),curl(fh))/2
        e=[abs(S-np.cos(phi)/4), abs(Z1-(np.cos(phi)/4-3.5*nu)), abs(Z2-(1.25-2.5*nu*np.cos(phi)+11*nu**2)), abs(Ehi-7/48), abs(Zhi-9/16)]
        worst=max(worst,max(e))
print("max abs error over phi in {0,.7,pi/3,2,pi}, nu in {1/28,.1,0}:", worst)
# all-new-modes coefficients for the plus field, phi=0, nu=1/28
u=[np.sin(Y),np.sin(Zc),np.cos(X)-np.cos(X+Y)]
supp=sum((np.abs(F(c))>1e-9).astype(float) for c in u)>0
f=add(B(u,u),sc(1/28,lap(u))); fn=filt(f,(~supp).astype(float))
print("new-mode E coeff", inner(fn,fn)/2, "(claim 11/24 =",11/24,")  Z coeff", inner(curl(fn),curl(fn))/2, "(claim 19/16 =",19/16,")")
