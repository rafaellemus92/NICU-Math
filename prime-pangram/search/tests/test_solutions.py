#!/usr/bin/env python3
"""Self-contained checks for the Prime-26 pangram project (no third-party dependencies).

Run:  python3 tests/test_solutions.py            (fast checks only, ~1 s)
      python3 tests/test_solutions.py --slow     (also re-derives the DP validation counts, ~1-2 min)

Prime-26: a prime is named by its base-26 digits, A=0 ... Z=25 (no leading A, since numerals have no leading zero).
"""
import sys, itertools

B = 26

def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0: return False
        i += 2
    return True

def val(w):
    v = 0
    for ch in w: v = v * B + (ord(ch) - 65)
    return v

def letters(n):
    s = []
    while n: s.append(n % B); n //= B
    return s[::-1]

def is_pangram(words):
    s = ''.join(words)
    return len(s) == 26 and sorted(s) == [chr(c) for c in range(65, 91)]

def lettersum(words):
    return sum(ord(c) - 65 for w in words for c in w)

failures = 0
def check(cond, msg):
    global failures
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond: failures += 1

# 1. The original 5-vs-5 equation pangram (found by Gemini/ChatGPT, verified here)
L = "YR BQL CWH DNF GAX".split(); R = "KV MT OP ESJ IUZ".split()
check(all(isprime(val(w)) for w in L + R), "original pangram: all ten values prime")
check(sum(map(val, L)) == sum(map(val, R)) == 10125, "original pangram: both sides sum to 10125")
check(is_pangram(L + R), "original pangram: every letter exactly once")
check(lettersum(L) % 25 == 0 and lettersum(R) % 25 == 0, "mod-25 theorem (each side's letter-sum = 0 mod 25: 150 and 175)")
check(10125 % 25 == 0, "each side is a multiple of 25 (10125 = 25*405)")

# 2. The three (and only three) equal-difference five-pair pangrams
sols = {204: [("YSH","ZAD"),("MWF","NEB"),("JUP","KCL"),("GX","OT"),("IV","QR")],
        258: [("KQR","LAP"),("BUF","CED"),("MWJ","NGH"),("IV","ST"),("OZ","YX")],
        534: [("UGL","VAZ"),("CB","WP"),("ED","YR"),("NQF","OKT"),("HSJ","IMX")]}
for D, pairs in sols.items():
    check(all(isprime(val(p)) and isprime(val(q)) and val(q) - val(p) == D for p, q in pairs), f"D={D}: ten primes, all five differences equal {D}")
    check(is_pangram([w for pq in pairs for w in pq]), f"D={D}: perfect pangram")
    s = sum(ord(c) - 65 for p, q in pairs for c in p)
    check(s % 25 == (10 * D) % 25, f"D={D}: letter-sum of smaller words = 10*D (mod 25)  [{s} = {s%25} mod 25]")

# 3. Near-miss example for the (impossible) equal-sum puzzle: four pairs, 20 letters, N = 10146
near = [("F","PAB"),("N","OZT"),("EHX","KSJ"),("GWL","IDV")]
check(all(isprime(val(p)) and isprime(val(q)) and val(p) + val(q) == 10146 for p, q in near), "equal-sum near miss: four pairs summing to 10146")
rest = set(chr(c) for c in range(65, 91)) - set(''.join(w for pq in near for w in pq))
check(rest == set("CMQRUY"), "equal-sum near miss leaves exactly C M Q R U Y")
# no pair of distinct-letter prime words over exactly those six letters sums to 10146
found = False
for k in range(1, 6):
    for A in itertools.permutations(sorted(rest), k):
        if A[0] == 'A': continue
        rem = rest - set(A)
        for Bw in itertools.permutations(sorted(rem), len(rem)):
            if val(''.join(A)) + val(''.join(Bw)) == 10146 and isprime(val(''.join(A))) and isprime(val(''.join(Bw))): found = True
check(not found, "...and no fifth pair over those letters sums to 10146")

# 4. (slow) re-derive the DP validation counts with an independent Python enumerator
def count_partitions(letterset, j, K):
    """number of ways to split the letter set into exactly j prime words of <=K letters each"""
    letterset = sorted(letterset)
    def rec(avail, words):
        if not avail: return 1 if words == j else 0
        if words >= j: return 0
        c = avail[0]; others = avail[1:]; total = 0
        for k in range(1, K + 1):
            if k - 1 > len(others): break
            for combo in itertools.combinations(others, k - 1):
                rem = [x for x in others if x not in combo]
                for perm in itertools.permutations(combo + (c,)):
                    if perm[0] == 0: continue
                    v = 0
                    for d in perm: v = v * B + d
                    if isprime(v): total += rec(rem, words + 1)
        return total
    return rec(letterset, 0)

if "--slow" in sys.argv:
    expected = [("ABCDEFGHIJKLMN", 6, 3, 13373), ("ABCDEFGHIJKLMN", 5, 3, 8728), ("ABCDEFGHIJKLM", 5, 3, 6397),
                ("ABCDEFGHIJKL", 5, 3, 3210), ("ABCDEFGHIJKL", 4, 3, 1263),
                ("ABCDEFGHIJKL", 5, 4, 27152), ("ABCDEFGHIJKL", 4, 4, 73155), ("ABCDEFGHIJKL", 3, 4, 30128),
                ("ABCDEFGHIJK", 4, 5, 20150), ("ABCDEFGHIJK", 3, 5, 48840)]
    for ls, j, K, want in expected:
        got = count_partitions([ord(c) - 65 for c in ls], j, K)
        check(got == want, f"partition count [{ls}] into {j} words (K<={K}) = {got} (DP and C brute force gave {want})")

print("\n%d failure(s)" % failures)
sys.exit(1 if failures else 0)
