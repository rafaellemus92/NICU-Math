"""Print the candidate-prime data used by Wyrd/Minimal.lean.

V  = numbers below 4295 not rejected by `rejectB` (no small divisor, name has no
     repeated letter). This is every prime with a repeat-free name, plus nothing
     else, but Lean doesn't rely on that: it re-checks the data itself.
VB = the same set as a bitmask (bit n set iff n is in V).
NT = every name below 4295 packed into one number: 16 bits per n, each letter
     stored as code + 1 in 5 bits (0 marks the end). Lean proves NT matches
     `encode`.

Usage: python3 scripts/gen_candidates.py
"""
import sys, os
sys.set_int_max_str_digits(0)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from coupled_prime26_pangram import encode

A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def rejected(n):
    if n < 3:
        return True
    name = encode(n)
    return (len(set(name)) < len(name)
            or any(d < n and n % d == 0 for d in range(2, 66)))

V = [n for n in range(0, 4295) if not rejected(n)]
print(f'-- {len(V)} candidates')
print('def V : List Nat :=\n  [' + ',\n   '.join(', '.join(map(str, V[i:i+16])) for i in range(0, len(V), 16)) + ']')
print()
print(f'def VB : Nat :=\n  {sum(1 << n for n in V)}')

def packed(n):
    if n == 0:
        return 0
    return sum((A.index(ch) + 1) << (5 * i) for i, ch in enumerate(encode(n)))

print()
print(f'def NT : Nat :=\n  {sum(packed(n) << (16 * n) for n in range(4295))}')
