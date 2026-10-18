#!/usr/bin/env python3
"""P1 at high order: beta=0, harmonics of Z_n for n<=N (exact, symbolic nu)."""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from nsseries import series, laurent_series
N = int(sys.argv[1]); amps = [Fr(x) for x in sys.argv[2:6]]
t0 = time.time()
U = series(*amps, N, verbose=False)
Z = laurent_series(U, N, 'curl')
print(f"amps={[str(a) for a in amps]} N={N}: max|m| per order:", [max(abs(m) for m in z) if z else None for z in Z],
      f"modes in U_n: {[len(u) for u in U]}  ({time.time()-t0:.1f}s)")
