# Rainbow, primary bow colours: finds, in exact rational arithmetic, the four-decimal brackets
# for a = arcsin sqrt(sin^2 r) and b = arcsin sqrt(cos^2 i) that the Taylor bounds T5 (lower) and
# T7 (upper) can certify, for red (n = 1.331) and violet (n = 1.343), and the margins (radians)
# of (180 + lo) pi/180 < 4a + 2b < (180 + hi) pi/180 with pi bracketed by 3.141592 .. 3.141593.
# Run from this folder: python3 -I primary_spectrum_brackets.py   (standard library only, <1 s)
# Formerly numerics/_raw/sp_check.py.

from fractions import Fraction as Fr
import math
def T5(x): return x - x**3/6 + x**5/120
def T7(x): return T5(x) - x**7/5040
pilo=Fr(3141592,10**6); pihi=Fr(3141593,10**6)
for name,ya2,yb2,lo_deg,hi_deg in [("red",Fr(742813,1771561),Fr(257187,10**6),42,43),("violet",Fr(732117,1803649),Fr(267883,10**6),40,41)]:
    a=math.asin(math.sqrt(ya2)); b=math.asin(math.sqrt(yb2))
    print(name,a,b)
    def lo(y2,v):
        # largest x = k/10000 with T5(x)^2 < y2
        k=int(v*10000)
        while not (T5(Fr(k,10000))**2 < y2 and T5(Fr(k,10000))>0): k-=1
        return Fr(k,10000)
    def hi(y2,v):
        k=int(v*10000)+1
        while not (T7(Fr(k,10000))**2 > y2): k+=1
        return Fr(k,10000)
    a1,a2,b1,b2=lo(ya2,a),hi(ya2,a),lo(yb2,b),hi(yb2,b)
    print(a1,a2,b1,b2)
    # need (180+lo_deg)*pi/180 < 4a+2b < (180+hi_deg)*pi/180
    L=4*a1+2*b1; U=4*a2+2*b2
    print(float(L - (180+lo_deg)*pihi/180), float((180+hi_deg)*pilo/180 - U))
