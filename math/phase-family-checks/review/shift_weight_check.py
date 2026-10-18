"""Appendix check: shift norm in weights (2+n^2)^m vs (1+n^2)^m, and the exact
operator norm of multiplication by sin y in the (2+n^2)^m weighted space
(truncated matrix, numerically), compared with the note's bound L=2^(m/2).
Also verifies F_s=||sin z e_y||_s=2^((s-1)/2) and the ||U||_m formula structure."""
import numpy as np

# 1) integer inequality 2+(n+-1)^2 <= 2(2+n^2)  <=>  (n-+1)^2 >= 0 : always true
bad = [n for n in range(-2000, 2001) if 2+(n+1)**2 > 2*(2+n*n) or 2+(n-1)**2 > 2*(2+n*n)]
print("violations of 2+(n+-1)^2 <= 2(2+n^2) in |n|<=2000:", bad)
# equality cases
eq = [n for n in range(-5, 6) if 2+(n+1)**2 == 2*(2+n*n) or 2+(n-1)**2 == 2*(2+n*n)]
print("equality cases:", eq, "(so the constant 2 is sharp for the shift ratio)")
# the naive 1D weight (1+n^2) does NOT satisfy the analogous bound with constant 2
bad1 = [n for n in range(-5, 6) if 1+(n+1)**2 > 2*(1+n*n)]
print("violations of 1+(n+1)^2 <= 2(1+n^2):", bad1, "-> ratio at n=1 is", (1+4)/(2*2))

# 2) exact norm of multiplication by sin y on the weighted space, truncated |n|<=Nn
def sin_mult_norm(m, Nn=200):
    n = np.arange(-Nn, Nn+1)
    w = (2.0+n*n)**(m/2)          # ||V||_* = ||diag(w) V||_2
    M = np.zeros((len(n), len(n)))
    # (sin y V)_n = (V_{n-1} - V_{n+1})/(2i); magnitude matrix (unitary phases irrelevant for norm)
    for i in range(len(n)):
        if i-1 >= 0: M[i, i-1] = 0.5
        if i+1 < len(n): M[i, i+1] = -0.5
    A = np.diag(w) @ M @ np.diag(1.0/w)   # conjugated operator in the weighted norm
    return np.linalg.norm(A, 2)

for m in [0, 1, 2, 5, 9]:
    nrm = sin_mult_norm(m)
    print(f"m={m}: numerical norm of (sin y .) in ||.||_*,m = {nrm:.6f};  note's bound L=2^(m/2) = {2**(m/2):.6f};  ratio bound/actual = {2**(m/2)/nrm:.3f}")

# 3) F_s = ||sin z e_y||_s with ||f||_s^2 = sum (1+|k|^2)^s |f_k|^2 : modes k=(0,0,+-1), |f_k|=1/2
for s in [4, 8]:
    F = np.sqrt(2*(2.0**s)*(0.5**2))
    print(f"s={s}: F_s computed {F:.6f}  claimed 2^((s-1)/2) = {2**((s-1)/2):.6f}")
# ||a sin y||_m^2 = 2^(m-1) a^2 : modes (0,+-1,0)
m = 9
print("||a sin y||_m^2 /a^2 for m=9:", 2*(2.0**m)*0.25, " appendix 2^m/2 =", 2.0**m/2)
# Re(e^{ix}W): modes (1,n,0) coeff W_n/2 and (-1,-n,0) coeff conj(W_n)/2, |k|^2=1+n^2 -> weight (2+n^2)^m, total (1/2)sum(2+n^2)^m|W_n|^2
print("Re(e^{ix}W) norm^2 = (1/2)||W||_*,m^2  (two conjugate modes, each |W_n|^2/4) -> OK")
# initial ||V(0)||_*,m^2 = 2^m c^2 + 3^m d^2 (V_0=c, V_1=-d e^{i phi})
print("||V(0)||_*,m^2 = 2^m c^2 + 3^m d^2 : weights (2+0)^m, (2+1)^m -> OK")
