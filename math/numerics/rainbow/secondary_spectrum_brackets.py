# Rainbow, secondary bow colours: checks, in exact rational arithmetic, that the brackets used in
# Lean for a = arcsin sqrt(sin^2 r) and b = arcsin sqrt(cos^2 i) (k = 2, n = 1.331 and 1.343) are
# certified by T5 (lower) and T7 (upper), and prints the margins (radians) of
# d1 pi/180 < 6a + 2b < d2 pi/180, i.e. secondary bow = 360 - (6a + 2b) degrees in (360-d2, 360-d1).
# Run from this folder: python3 -I secondary_spectrum_brackets.py   (standard library only, <1 s)
# Formerly numerics/_raw/colours-ss-brackets.py.

from fractions import Fraction as Fr
import math
def T5(x): return x - x**3/6 + x**5/120
def T7(x): return T5(x) - x**7/5040
def check(name, ysq, lo, hi, scale=10000):
    lo=Fr(lo,scale); hi=Fr(hi,scale)
    ok_lo = T5(lo) > 0 and T5(lo)**2 < ysq
    ok_hi = T7(hi)**2 > ysq
    print(name, float(lo), math.asin(math.sqrt(ysq)), float(hi), ok_lo, ok_hi)
    return lo, hi
for (nm, a2, b2, d1, d2, al, ah, bl, bh) in [
  ("red", Fr(7228439,14172488), Fr(771561,8000000), 309, 310, 7949, 7959, 3151, 3165),
  ("violet", Fr(7196351,14429192), Fr(803649,8000000), 306, 307, 7836, 7846, 3218, 3232)]:
    alo, ahi = check(nm+" a", a2, al, ah)
    blo, bhi = check(nm+" b", b2, bl, bh)
    pl = Fr(3141592,1000000); ph = Fr(3141593,1000000)
    # need d1*pi/180 < 6a+2b  (lower: 6alo+2blo > d1*ph/180) and 6ahi+2bhi < d2*pl/180
    print(" lower", float(6*alo+2*blo - d1*ph/180), "upper", float(d2*pl/180 - 6*ahi - 2*bhi))
