"""
The two congruences that govern every positional numeration value(w) = sum d_i b^(k-i):
   (1) b^k = 0 (mod b)   for k >= 1  ->  value = last digit        (mod b)
   (2) b   = 1 (mod b-1)             ->  value = sum of digits     (mod b-1)
A prime word (value > b) therefore needs gcd(last digit, b) = 1 AND
gcd(digit sum, b-1) = 1.  For an odd base, (2) forces every prime word to have
an odd digit sum; the 26 letters sum to 351 (odd), so a perfect pangram of
prime words must then have an ODD number of words (3 or 5).
This script tabulates both effects for bases 24..31 on the English-cluster
dictionary (primality not used - pure congruence filters).
"""
import math
from collections import Counter
from core import *

def factor(n):
    f, p = [], 2
    while p * p <= n:
        while n % p == 0:
            f.append(p); n //= p
        p += 1
    if n > 1:
        f.append(n)
    return "·".join(map(str, f))

allw = english_words(prime_only=False)
print(f"{len(allw):,} pronounceable English-regime words\n")
print("base | b | b-1 | admissible final letters (gcd(d,b)=1) | digit sum must be coprime to | words passing both filters | word count parity")
for b in range(24, 32):
    finals = "".join(ch for ch in ALPHABET if math.gcd(ord(ch) - 96, b) == 1)
    ok = 0
    for w, _, _ in allw:
        d = ord(w[-1]) - 96
        s = sum(ord(ch) - 96 for ch in w)
        if math.gcd(d, b) == 1 and math.gcd(s, b - 1) == 1:
            ok += 1
    parity = "odd (3 or 5 words)" if (b - 1) % 2 == 0 else "free (3..6 words)"
    print(f"{b:4d} | {factor(b):>7s} | {factor(b-1):>7s} | {finals:26s} ({len(finals):2d}) | {b-1:3d} | {ok:7,d} ({100*ok/len(allw):4.1f}%) | {parity}")

# sanity check for the task's base 26: 26 = 1 (mod 5), so a prime word's digit sum is not divisible by 5
import os
assert BASE == 26
prime = english_words(prime_only=True)
bad = [w for w, v, _ in prime if sum(ord(c) - 96 for c in w) % 5 == 0 and v != 5]
print(f"\nbase 26 check: prime words whose digit sum is divisible by 5 (value != 5): {len(bad)}  (must be 0)")
print("the only exception is the word E itself, value 5:", [w for w, v, _ in prime if v == 5])
