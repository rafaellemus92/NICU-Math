"""Independent checks of response.py: rhs convolution (orders 1,2), tri(), second(), stacked RK4 = exact Taylor coefficients of the discrete map."""
import json
from common import *
nu=NU
out={}
# 1. rhs convolution: compare Response.rhs(Y)[n] with b-Taylor coefficients of NS.rhs(U+b q1+b^2 q2) via exact polynomial fit (NS.rhs is quadratic in u -> degree 4 in b)
s=Response(12,nu); ns=audit.NS(12,nu)
Y=integrate(s,s.initial(.61),.15,.01); U,q1,q2=Y
bs=np.array([-.3,-.2,-.1,0,.1,.2,.3])
vals=np.array([ns.rhs(U+b*q1+b*b*q2) for b in bs])      # shape (7,3,N,N,N/2+1)
V=np.vander(bs,7,increasing=True)
coef=np.linalg.solve(V,vals.reshape(7,-1)).reshape(7,*vals.shape[1:])
R=s.rhs(Y)
out['rhs_order0_err']=float(np.max(abs(coef[0]-R[0])))
out['rhs_order1_err']=float(np.max(abs(coef[1]-R[1])))
out['rhs_order2_err']=float(np.max(abs(coef[2]-R[2])))
out['rhs_scale']=float(np.max(abs(R)))
# 2. independent S(u) in physical space with own derivative, vs tri(u,u,u)
g=s.g
u=integrate(ns,ns.init_family(.61,b=1.),.15,.01)
def S_indep(uh):
    up=g.inv(uh); wh=g.curl_h(uh); w=g.inv(wh)
    tot=0.
    for i in range(3):
        for j in range(3):
            dju_i=g.inv(1j*g.kvec[j]*uh[i])
            tot+=np.mean(w[i]*w[j]*dju_i)
    return float(tot)
def S_indep2(uh):
    # <omega . curl P[u x omega]> = dZ/dt + nu<|grad omega|^2>  (uses projected nonlinear term)
    wh=g.curl_h(uh); nl=ns.nonlin(uh)
    return g.inner(wh,g.curl_h(nl))
out['S_tri']=s.tri(u,u,u); out['S_indep_physical']=S_indep(u); out['S_from_enstrophy_budget']=S_indep2(u)
# also ordering convention: tri(v,w,u) = <curl v_i curl w_j d_j u_i>; check against PROOF T_s(f,g,h)=<(w_f)_i (w_g)_j d_j h_i>
# 3. second(): E2,Z2,S2 as exact b^2 coefficient of O(U+b q1+b^2 q2) via polynomial fit degree 6
qs=np.array([s.quantities(U+b*q1+b*b*q2) for b in bs])
c=np.linalg.solve(V,qs)
out['second_vs_poly_b2']=(c[2]-s.second(Y)).tolist(); out['second']=s.second(Y).tolist()
out['poly_b1_coeff(should be 0 only if J-odd; E1=<U,q1>)']=c[1].tolist()
# 4. stacked RK4 == exact Taylor coefficients of discrete RK4 map: compare Y after integration with polynomial fit of full solves in b (degree high), small b
T=.2; dt=.01
Yt=integrate(s,s.initial(.61),T,dt)
bs2=np.array([-.04,-.03,-.02,-.01,0,.01,.02,.03,.04])
sols=np.array([integrate(ns,ns.init_family(.61,b=b),T,dt) for b in bs2])
V2=np.vander(bs2,9,increasing=True)
cf=np.linalg.solve(V2,sols.reshape(9,-1)).reshape(9,*sols.shape[1:])
out['discrete_map_taylor_q1_err']=float(np.max(abs(cf[1]-Yt[1]))); out['discrete_map_taylor_q2_err']=float(np.max(abs(cf[2]-Yt[2])))
out['discrete_map_taylor_q1_scale']=float(np.max(abs(Yt[1]))); out['q2_scale']=float(np.max(abs(Yt[2])))
out['discrete_map_q3_scale']=float(np.max(abs(cf[3]))); out['discrete_map_q4_scale']=float(np.max(abs(cf[4])))
# 5. z-mode support of q3 from the fit (expected +-1,+-3)
kz=g.kvec[2]
for n,allowed in [(1,[1]),(2,[0,2]),(3,[1,3]),(4,[0,2,4])]:
    bad=~np.isin(kz,allowed)
    out[f'fit_order{n}_leak_outside_zmodes_{allowed}']=float(np.max(abs(cf[n][:,bad])))
# 6. check tri() ordering explicitly: tri(v,w,u) uses curl v_i curl w_j d_j u_i
v=Yt[0]; w=Yt[1]; uu=Yt[2]
cv=g.inv(g.curl_h(v)); cw=g.inv(g.curl_h(w))
ref=sum(np.mean(cv[i]*cw[j]*g.inv(1j*g.kvec[j]*uu[i])) for i in range(3) for j in range(3))
out['tri_order_check']=float(s.tri(v,w,uu)-ref)
out['tri_not_symmetric_example']=[s.tri(v,w,uu),s.tri(w,v,uu),s.tri(uu,w,v)]
# 7. six-slot sum enumerates (i,j,2-i-j) over i in 0..2, j in 0..2-i: list them
out['slots']=[(i,j,2-i-j) for i in range(3) for j in range(3-i)]
print(json.dumps(out,indent=1))
json.dump(out,open(str(OUT)+'/formula_checks.json','w'),indent=1)
