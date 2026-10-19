"""Mean-q2 pilot kernels only. No evolution or full-horizon certification.
Interval discs and arithmetic assumptions are inherited from the pinned validator.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import importlib.util
from decimal import Decimal, localcontext
import numpy as np

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
PIN='2d2952363b8d2f4cf6918123a94d47c7b69988ca2ec54c06179830562ecea4bc'
path=PARENT/'absorption-b003/validate_residual.py'
if hashlib.sha256(path.read_bytes()).hexdigest()!=PIN:
    raise ValueError('Validator source mismatch')
if hashlib.sha256((PARENT/'constants.py').read_bytes()).hexdigest()!='996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014':
    raise ValueError('Interval source mismatch')
spec=importlib.util.spec_from_file_location('pilot_validator',path)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
CI,Iv,TRAP=v.CI,v.Iv,v.TRAP


def put(a,sl,b):
    a.re[sl],a.im[sl],a.rad[sl]=b.re,b.im,b.rad


def grow(a,bx,by):
    nx,ny=a.shape[-2:];x=nx//2;y=ny//2
    if bx<x or by<y: raise ValueError('Cannot truncate support')
    out=v.zeros(a.shape[:-2]+(2*bx+1,2*by+1))
    put(out,(...,slice(bx-x,bx+x+1),slice(by-y,by+y+1)),a)
    return out


def grid(a):
    nx,ny=a.shape[-2:]
    return np.meshgrid(np.arange(-nx//2+1,nx//2+1,dtype=float),
                       np.arange(-ny//2+1,ny//2+1,dtype=float),indexing='ij')


def reverse_conjugate(a):
    return v.cconj(a[...,::-1,::-1])


def project(a,kz=0,remove_mean=False):
    """Leray preserves the zero-mode force. remove_mean defines an approximation only."""
    x,y=grid(a);k2=x*x+y*y+kz*kz
    dot=v.cadd(v.cadd(v.cscale(a[0],x),v.cscale(a[1],y)),v.cscale(a[2],kz))
    safe=np.where(k2==0,1,k2)
    d=v.cdiv_pos(dot,safe);out=v.zeros(a.shape)
    for j,k in enumerate((x,y,kz)):
        put(out,j,v.csub(a[j],v.cscale(d,k)))
    if kz==0:
        center=(slice(None),a.shape[1]//2,a.shape[2]//2)
        put(out,center,v.zeros((3,)) if remove_mean else a[center])
    return out


def mean_node(raw):
    a=v.exact(raw)
    return project(v.cscale(v.cadd(a,reverse_conjugate(a)),.5),remove_mean=True)


def mean_source(Q):
    """P div_xy mean(qN tensor qN), qN=Re(e^iz Q), with full convolution.
    H_ji=Q_j*conj(Q_i). Real mean tensor = (H+conj(reverse H))/4.
    Equivalence to advective form uses exact div(qN)=0; Q is projected first.
    """
    nx,ny=Q.shape[-2:]
    neg=reverse_conjugate(Q)
    H=v.zeros((2,3,2*nx-1,2*ny-1))
    for ix in range(nx):
        for iy in range(ny):
            left=Q[:2,ix,iy]
            left=CI(left.re[:,None,None,None],left.im[:,None,None,None],left.rad[:,None,None,None])
            right=CI(neg.re[None],neg.im[None],neg.rad[None])
            prod=v.cmul(left,right)
            sl=(slice(None),slice(None),slice(ix,ix+nx),slice(iy,iy+ny))
            put(H,sl,v.cadd(H[sl],prod))
    tensor=v.cscale(v.cadd(H,reverse_conjugate(H)),.25)
    x,y=grid(tensor)
    F=v.cmul_i(v.cadd(v.cscale(tensor[0],x),v.cscale(tensor[1],y)))
    # Exact derivative of a periodic flux has zero full mean, regardless of rounding radii.
    put(F,(slice(None),nx-1,ny-1),v.zeros((3,)))
    return project(F)


def shear(V,bx,by):
    """sin(y) d_x V + (V_y cos(y),0,0), on complete output support."""
    nx,ny=V.shape[-2:];mx,my=nx//2,ny//2
    x,_=grid(V);out=v.zeros((3,2*bx+1,2*by+1))
    for shift in (-1,1):
        sl=(slice(None),slice(bx-mx,bx+mx+1),slice(by-my+shift,by+my+1+shift))
        term=v.cscale(V,shift*.5*x)
        put(term,0,v.cadd(term[0],v.cscale(V[1],.5)))
        put(out,sl,v.cadd(out[sl],term))
    return out


def vertical_base(W,V,bx,by):
    """Only (0,0,V_x*w_x+V_y*w_y). There is NO w*d_z V for mean V."""
    mx,my=V.shape[1]//2,V.shape[2]//2;kw=len(W.re)//2
    out=v.zeros((3,2*bx+1,2*by+1))
    # Physical w coefficients: +x W/2, -x conjugate(W reversed)/2.
    neg=v.cconj(W[::-1])
    for sx,A in ((1,v.cscale(W,.5)),(-1,v.cscale(neg,.5))):
        for iy in range(2*kw+1):
            ky=iy-kw
            dx=v.cscale(v.cmul_i(A[iy]),sx)
            dy=v.cscale(v.cmul_i(A[iy]),ky)
            term=v.cadd(v.cmul(dx,V[0]),v.cmul(dy,V[1]))
            sl=(2,slice(bx-mx+sx,bx+mx+1+sx),slice(by-my+ky,by+my+1+ky))
            put(out,sl,v.cadd(out[sl],term))
    return out


def scale_iv(a,iv):
    m,r=v.iv_to_mr(iv)
    return v.cmul_rs(a,m,r)


def residual_polynomial(Q0,Q1,W0,W1,V0,V1,j,h_inv=50000):
    """Fine-cell polynomial with exp(-nu*t) frozen left; all input paths affine.
    V states are pilot probes, not an evolved solution. Returns full-support residual.
    """
    kq=Q0.shape[-1]//2;mx,my=V0.shape[1]//2,V0.shape[2]//2;kw=len(W0.re)//2
    bx=max(mx+1,2*kq);by=max(my+max(kw,1),2*kq)
    nu=Iv.of('1/28');h=1/Iv.of(h_inv);ee=(-nu*j/h_inv).exp()
    dQ=v.csub(Q1,Q0);dW=v.csub(W1,W0);dV=v.csub(V1,V0)
    D=v.cscale(grow(dV,bx,by),h_inv)
    Vb=grow(V0,bx,by);x,y=grid(Vb);k2=x*x+y*y
    S0=shear(V0,bx,by);S1=shear(V1,bx,by);Sd=shear(dV,bx,by)
    B0=vertical_base(W0,V0,bx,by);B1=vertical_base(W1,V1,bx,by)
    Bd=vertical_base(dW,dV,bx,by)
    F0=mean_source(Q0);F1=mean_source(Q1);Fd=mean_source(dQ)
    crossB=v.cscale(v.csub(v.csub(B1,B0),Bd),h_inv)
    crossF=v.cscale(v.csub(v.csub(F1,F0),Fd),h_inv)
    R0=v.cadd(v.cadd(D,scale_iv(v.cscale(Vb,k2),nu)),
               v.cadd(project(v.cadd(scale_iv(S0,ee),B0)),grow(F0,bx,by)))
    R1=v.cadd(scale_iv(v.cscale(D,k2),nu),
               v.cadd(project(v.cadd(scale_iv(v.cscale(Sd,h_inv),ee),crossB)),grow(crossF,bx,by)))
    R2=v.cscale(v.cadd(project(Bd),grow(Fd,bx,by)),h_inv*h_inv)
    norms=[Iv.of(v.wnorm_hi(R,1,False)) for R in (R0,R1,R2)]
    sn=max(v.wnorm_hi(S0,1,False),v.wnorm_hi(S1,1,False))
    frozen=ee*nu*h.sq()/2*Iv.of(sn)
    integral=h*norms[0]+h.sq()/2*norms[1]+h.sq()*h/3*norms[2]+frozen
    return dict(R0=R0,R1=R1,R2=R2,bx=bx,by=by,integral=integral,
                polynomial_norms=norms,frozen=frozen,F0=F0,F1=F1,Fd=Fd,
                source_L1=h*Iv.of(v.wnorm_hi(F0,1,False))
                  +h.sq()/2*Iv.of(v.wnorm_hi(crossF,1,False))
                  +h.sq()*h/3*Iv.of(v.wnorm_hi(v.cscale(Fd,h_inv*h_inv),1,False)))


def direct_frozen(Q,W,V,D,j,h_inv=50000):
    kq=Q.shape[-1]//2;mx,my=V.shape[1]//2,V.shape[2]//2;kw=len(W.re)//2
    bx=max(mx+1,2*kq);by=max(my+max(kw,1),2*kq)
    Vb=grow(V,bx,by);x,y=grid(Vb)
    ee=(-Iv.of('1/28')*j/h_inv).exp()
    return v.cadd(v.cadd(grow(D,bx,by),scale_iv(v.cscale(Vb,x*x+y*y),Iv.of('1/28'))),
      v.cadd(project(v.cadd(scale_iv(shear(V,bx,by),ee),vertical_base(W,V,bx,by))),grow(mean_source(Q),bx,by)))
