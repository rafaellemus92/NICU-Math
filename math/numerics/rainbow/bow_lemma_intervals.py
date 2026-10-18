# Rainbow: (1) the exact rationals cos^2 i = (n^2-1)/(k(k+2)) and sin^2 r = (1 - cos^2 i)/n^2 that
# appear in the Lean statements for n = 1.331, 1.343; (2) the bow-angle intervals implied by the
# four-decimal arcsin brackets proved in Lean, with their margins to the stated degree ranges;
# (3) which other light paths (0 and 3..7 internal reflections) reach the 43..50 deg dark band.
# Run from this folder: python3 -I bow_lemma_intervals.py   (standard library only, <1 s)
# Formerly numerics/_raw/review2-num3.py.

from math import *
from fractions import Fraction as Fr
def refr(n,i): return asin(sin(i)/n)
def dev(k,n,i): return k*pi+2*i-2*(k+1)*refr(n,i)
def binc(k,n): return acos(sqrt((n*n-1)/(k*(k+2))))
# closed-form constants
for n,k in [(Fr(1331,1000),1),(Fr(1343,1000),1),(Fr(1331,1000),2),(Fr(1343,1000),2)]:
    q=(n*n-1)/(k*(k+2)); s2=(1-q)/(n*n)
    print(f"n={n}, k={k}: cos^2 i = {q}, sin^2 r = {s2}")
# brackets implied by the proved lemmas: (a_lo,a_hi) for arcsin sqrt(sin^2 r), (b_lo,b_hi) for arcsin sqrt(q)
P=(3.141592,3.141593)
def deg(x): return x*180/pi
cases={
 "primary red":   ((0.7043,0.7044),(0.5318,0.5319),1, 42,43),
 "primary violet":((0.6907,0.6908),(0.5440,0.5441),1, 40,41),
 "secondary red": ((0.7949,0.7959),(0.3151,0.3165),2, 50,51),
 "secondary violet":((0.7836,0.7846),(0.3218,0.3232),2,53,54),
}
for name,((alo,ahi),(blo,bhi),k,L,U) in cases.items():
    if k==1:  # pi - D = 4a - 2(pi/2 - b) = 4a + 2b - pi
        lo=4*alo+2*blo-P[1]; hi=4*ahi+2*bhi-P[0]
    else:     # D - pi = 2pi - 6a - 2b
        lo=2*P[0]-6*ahi-2*bhi; hi=2*P[1]-6*alo-2*blo
    # the linarith target is in units of pi: L*pi/180 < angle < U*pi/180 ; check conservatively
    okL = lo > L*P[1]/180; okU = hi < U*P[0]/180
    print(f"{name}: proved-lemma interval [{deg(lo):.3f}, {deg(hi):.3f}] deg  (stated ({L},{U}))  margins lo={deg(lo)-L:.3f} hi={U-deg(hi):.3f} conservative-ok={okL and okU}")
# true arcsin values
for n,k in [(1.331,1),(1.343,1),(1.331,2),(1.343,2)]:
    i=binc(k,n); r=refr(n,i)
    print(f"  n={n} k={k}: a=r={r:.6f} b=pi/2-i={pi/2-i:.6f}")
# What could be provably stated for widths from the lemmas
print("width primary from lemma intervals: [%.3f, %.3f]"%( (4*0.7043+2*0.5318-4*0.6908-2*0.5441)*180/pi, (4*0.7044+2*0.5319-4*0.6907-2*0.5440)*180/pi))
print("width secondary from lemma intervals: [%.3f, %.3f]"%( ((6*0.7949+2*0.3151)-(6*0.7846+2*0.3232))*180/pi, ((6*0.7959+2*0.3165)-(6*0.7836+2*0.3218))*180/pi))
# Other light reaching 43..50 deg from antisolar point
n=1.331
print("\nexternal reflection: D_ext = pi - 2i, angle from antisolar = 2i -> covers [0,180] incl. 43..50")
for k in range(0,8):
    if k==0:
        Ds=[2*i-2*refr(n,i) for i in [j*pi/2/2000 for j in range(2001)]]
    else:
        Ds=[dev(k,n,i) for i in [j*pi/2/2000 for j in range(2001)]]
    angs=[abs(pi-((D)%(2*pi))) for D in Ds]
    lo,hi=min(angs),max(angs)
    inband=any(43*pi/180<x<50*pi/180 for x in angs)
    extra=""
    if k>=1 and n<k+1:
        i0=binc(k,n); D0=dev(k,n,i0); extra=f" caustic at {degrees(abs(pi-(D0%(2*pi)))):.2f} deg"
    print(f"k={k}: antisolar angles span [{degrees(lo):.2f},{degrees(hi):.2f}] deg, enters 43-50 band: {inband}{extra}")
