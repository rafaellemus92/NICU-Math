"""Evaluate the appendix's explicit base majorant C_base and the implied upper
bound on the certifiable radius beta for the lab parameters a=c=d=1, nu=1/28,
for m=R+1 with R=8 (observable theorem) and m=s+1 with s=4 (all-time theorem).
beta_max(K) = nu e^{-A}/(2 K F_R),  A <= K C_base/nu, decreasing in K, so any
lower bound K_lb on an admissible K gives an upper bound on beta.
All in logs (base 10) because the numbers overflow double."""
import math, sys
a = c = d = 1.0
nu = 1.0/28.0
K_lb = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

def log10_add(x, y):
    m = max(x, y)
    return m + math.log10(10**(x-m) + 10**(y-m))

for s in [4, 8]:
    m = s + 1
    L = 2**(m/2)
    log10_exp = (2*L*abs(a)/nu)/math.log(10)          # log10 exp(2L|a|/nu)
    log10_term2 = log10_exp + math.log10(2**m*c*c + 3**m*d*d)
    log10_Cb2 = log10_add(math.log10(2**m*a*a), log10_term2) - math.log10(2)
    log10_Cb = log10_Cb2/2
    log10_A_over_K = log10_Cb - math.log10(nu)         # A/K <= C_base/nu
    F = 2**((s-1)/2)
    # log10 beta_max = log10(nu/(2 K F)) - K*(C_base/nu)/ln10
    log10_beta = math.log10(nu/(2*K_lb*F)) - K_lb*(10**log10_A_over_K)/math.log(10)
    print(f"s={s}, m={m}: L=2^(m/2)={L:.4f}, 2L|a|/nu={2*L/nu:.2f}, "
          f"log10 exp(2L|a|/nu)={log10_exp:.2f}, log10 C_base={log10_Cb:.2f}, "
          f"log10 (A/K upper bound)={log10_A_over_K:.2f}")
    print(f"   with K >= {K_lb}: log10(beta_max) <= {log10_beta:.4g}   i.e. beta <= 10^({log10_beta:.3g})")
    # also: the exp(L|a|/nu) growth factor for ||V||, for comparison with the true one
    print(f"   appendix growth factor exp(L|a|/nu) = 10^{(L/nu)/math.log(10):.2f}")
