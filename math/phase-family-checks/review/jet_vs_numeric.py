"""Compare the variational solver's Z2 cos(2phi) harmonic (phaseT1.out, N=18) with the exact
rational jet through t^8 (b^2 part, nu=1/28) from jet8.out / exact_jet.py."""
import json
from fractions import Fraction as F
nu = F(1, 28)
# exact b^2 cos(2phi) coefficients of t^6, t^7, t^8 (from exact_jet.py output, rational)
c6 = F(-6487, 1555200)
c7 = F(207269, 203212800)
c8 = F(23726951921639, 11739646638720000) - F(4751930032987135, 10**19)  # b=1 value minus b^4 part (float est.)
# better: solve exactly from b=1 and b=1/2 values at t^8: Z(1)=A+B, Z(1/2)=A/4+B/16 (b^6,b^8 vanish numerically)
z1 = F(23726951921639, 11739646638720000); zh = F(78172013854799, 187834346219520000)
B8 = (z1 - 4*zh)*F(16, 12)  # from A+B=z1, A/4+B/16=zh -> 4A+B=16zh -> 3B = z1*4 - 16zh ... solve properly below
# A + B = z1 ; A + B/4 = 4 zh  => (3/4) B = z1 - 4 zh => B = 4/3 (z1 - 4 zh); A = z1 - B
B8 = F(4, 3)*(z1 - 4*zh); A8 = z1 - B8
print('t^8 cos2phi: b^2 coeff =', A8, float(A8), ' b^4 coeff =', B8, float(B8))
d = json.load(open(str(__import__('pathlib').Path(__file__).resolve().parent/'out/phaseT1.out')))
for r in d['rows']:
    t = r['T']
    jet6 = float(c6)*t**6; jet8 = jet6 + float(c7)*t**7 + float(A8)*t**8
    num = r['Z2_cos2']
    print(f"T={t:.2f}: numeric Z2cos2={num:.6e}  jet(t^6)={jet6:.6e}  jet(t^6..t^8)={jet8:.6e}  "
          f"rel.diff to t^8 jet={(num-jet8)/abs(jet8):.3e}  (num-jet8)/t^9={(num-jet8)/t**9:.4e}")
