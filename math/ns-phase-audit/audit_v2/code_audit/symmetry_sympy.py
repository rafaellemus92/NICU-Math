import sympy as sp
x, y, z, phi, t = sp.symbols('x y z phi t', real=True)
a, b, c, d = sp.symbols('alpha beta gamma delta', real=True)
X = sp.Matrix([x, y, z])
R = sp.diag(-1, -1, 1); bvec = sp.Matrix([0, 0, sp.pi])
def u0(p, X=X, amps=(1, 1, 1, 1)):
    al, be, ga, de = amps
    return sp.Matrix([al*sp.sin(X[1]), be*sp.sin(X[2]), ga*sp.cos(X[0]) - de*sp.cos(X[0]+X[1]+p)])
for amps in [(1, 1, 1, 1), (a, b, c, d)]:
    Y = R*X + bvec
    Fu = R*u0(phi, Y, amps)
    diff = sp.simplify(sp.expand_trig(Fu - u0(-phi, X, amps)))
    print("amps", amps, " F[u_phi] - u_{-phi} =", list(diff))
# curl equivariance and Z invariance for a generic field: curl(R u(R x + b)) = det(R) R (curl u)(R x + b)
f = [sp.Function(f'f{i}')(x, y, z) for i in range(3)]
def curl(V):
    return sp.Matrix([sp.diff(V[2], y)-sp.diff(V[1], z), sp.diff(V[0], z)-sp.diff(V[2], x), sp.diff(V[1], x)-sp.diff(V[0], y)])
U = sp.Matrix(f)
V = R*U.subs({x: -x, y: -y, z: z+sp.pi}, simultaneous=True)
lhs = curl(V)
rhs = (R*curl(U)).subs({x: -x, y: -y, z: z+sp.pi}, simultaneous=True)*R.det()
print("curl equivariance residual:", list(sp.simplify(lhs-rhs)), " det R =", R.det(), " R orthogonal:", R*R.T == sp.eye(3))
# advection equivariance: ((v.grad)v)(x) = R ((u.grad)u)(Rx+b)
def adv(V):
    return sp.Matrix([sum(V[j]*sp.diff(V[i], s) for j, s in enumerate((x, y, z))) for i in range(3)])
lhs = adv(V); rhs = R*adv(U).subs({x: -x, y: -y, z: z+sp.pi}, simultaneous=True)
print("advection equivariance residual:", list(sp.simplify(lhs-rhs)))
def div(V): return sum(sp.diff(V[i], s) for i, s in enumerate((x, y, z)))
print("divergence equivariance residual:", sp.simplify(div(V) - div(U).subs({x: -x, y: -y, z: z+sp.pi}, simultaneous=True)))
lap = lambda V: sp.Matrix([sum(sp.diff(V[i], s, 2) for s in (x, y, z)) for i in range(3)])
print("Laplacian equivariance residual:", list(sp.simplify(lap(V) - R*lap(U).subs({x: -x, y: -y, z: z+sp.pi}, simultaneous=True))))
# Fourier picture: mode k -> R k ; cubic cutoff max|k_i| and |k|^2 preserved; P(Rk) R = R P(k)
k = sp.Matrix(sp.symbols('k1 k2 k3', integer=True))
P = lambda kk: sp.eye(3) - kk*kk.T/(kk.T*kk)[0]
print("Leray commutation residual:", sp.simplify(P(R*k)*R - R*P(k)))
# dZ/dt(0) formula check: S = <omega . grad u . omega>, D = <|grad omega|^2>
u = u0(phi); w = curl(u)
avg = lambda e: sp.simplify(sp.integrate(sp.expand(sp.expand_trig(e)), (x, 0, 2*sp.pi), (y, 0, 2*sp.pi), (z, 0, 2*sp.pi))/(2*sp.pi)**3)
E = avg((u.T*u)[0]/2); Z = avg((w.T*w)[0]/2)
print("E =", E, " Z =", Z)
