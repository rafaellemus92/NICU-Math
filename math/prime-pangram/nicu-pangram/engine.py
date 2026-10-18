"""
Exact counting engine.

Counts (or sums weights over) all ways to partition the 26 letters into words
of a dictionary.  Every word has a nucleus = a set B of 1 or 2 vowels and a set
C of consonants.  A partition of the alphabet is: a set partition pi of the six
vowels into blocks of size 1-2, plus, for each block B, one word with vowel set
B, such that the consonant sets are pairwise disjoint and cover all 20.

For a fixed pi the count is a disjoint-union product over the blocks, which we
evaluate at the full consonant set by inclusion-exclusion with a rank variable
z (z^k marks k consonants):

   count(pi) = sum_{S subset of consonants} (-1)^(20-|S|) [z^20] prod_B G_B(S)(z)
   G_B(S)(z) = sum_{words w with vowel set B and cons(w) subset of S} wt(w) z^|cons(w)|

G_B(S) is the zeta transform (over the 2^20 consonant subsets) of the sparse
array of word weights.  Because sizes add up to exactly 20 = |all consonants|,
'union = everything and total size 20' forces disjointness, so the rank
variable makes inclusion-exclusion count disjoint covers exactly.

Weights are either integers mod a prime (exact counts via CRT over several
primes) or float64 (first-moment estimates).  A second variable x^cost
(cost = number of non-English clusters in the word) is optional and tracked
up to a maximum degree so that counts can be broken down by cost.
"""
import itertools, time
import numpy as np
from core import *

NC = 20                     # consonants
NS = 1 << NC                # 2^20 consonant subsets
PRIMES = [2147483647, 2147483629, 2147483587, 2147483579, 2147483563]
for _p in PRIMES:
    assert is_prime_py(_p)

_popcount = None
def popcount_table():
    global _popcount
    if _popcount is None:
        t = np.zeros(NS, dtype=np.int64)
        for b in range(NC):
            t[1 << b:1 << (b + 1)] = t[:1 << b] + 1
        _popcount = t
    return _popcount


def zeta(arr, mod=None):
    """In-place subset-sum (zeta) transform over the last axis of size 2^20."""
    shape = arr.shape
    a = arr.reshape(-1, NS)
    for b in range(NC):
        v = a.reshape(a.shape[0], NS >> (b + 1), 2, 1 << b)
        if mod is None:
            v[:, :, 1, :] += v[:, :, 0, :]
        else:
            v[:, :, 1, :] += v[:, :, 0, :]
            v[:, :, 1, :] %= mod
    return arr


def vowel_partitions():
    """All partitions of the 6 vowels into blocks of size 1 or 2 (76 of them),
    as lists of 6-bit masks."""
    out = []
    def rec(remaining, blocks):
        if not remaining:
            out.append(list(blocks)); return
        v = remaining[0]
        rec(remaining[1:], blocks + [1 << v])
        for w in remaining[1:]:
            rec([u for u in remaining[1:] if u != w], blocks + [(1 << v) | (1 << w)])
    rec(list(range(6)), [])
    return out


def build_G(words, weight_fn, mod=None, max_cost=0, dtype=None):
    """
    words: iterable of (word, value, mask[, cost]).  weight_fn(word, value) -> weight.
    Returns dict: vowel-block mask -> array [cost+1, deg+1, 2^20] of zeta-transformed
    weights (deg = max consonant count among words of that block).
    """
    if dtype is None:
        dtype = np.int64 if mod is not None else np.float64
    groups = {}
    for rec in words:
        w, val, m = rec[0], rec[1], rec[2]
        cost = rec[3] if len(rec) > 3 else 0
        if cost > max_cost:
            continue
        B = vset(w)
        C = cmask(w)
        k = bin(C).count("1")
        wt = weight_fn(w, val)
        if mod is not None:
            wt = int(wt) % mod
        g = groups.setdefault(B, {})
        key = (cost, k)
        arr = g.get(key)
        if arr is None:
            arr = g[key] = np.zeros(NS, dtype=dtype)
        arr[C] += wt
        if mod is not None:
            arr[C] %= mod
    G = {}
    for B, g in groups.items():
        deg = max(k for (_, k) in g)
        A = np.zeros((max_cost + 1, deg + 1, NS), dtype=dtype)
        for (cost, k), arr in g.items():
            A[cost, k] = arr
        zeta(A, mod)
        G[B] = A
    return G


def _mul(P, Q, mod, zmax):
    """Pointwise (over S) product of 2-variable polynomials P[x][z][S], Q[x][z][S],
    truncated to x-degree P.shape[0]-1 (same for both) and z-degree zmax."""
    X = P.shape[0]
    R = np.zeros((X, min(zmax, P.shape[1] + Q.shape[1] - 2) + 1, NS), dtype=P.dtype)
    for xi in range(X):
        for xj in range(X - xi):
            for zi in range(P.shape[1]):
                if not P[xi, zi].any():
                    continue
                for zj in range(Q.shape[1]):
                    if zi + zj > zmax:
                        break
                    if mod is None:
                        R[xi + xj, zi + zj] += P[xi, zi] * Q[xj, zj]
                    else:
                        R[xi + xj, zi + zj] += (P[xi, zi] * Q[xj, zj]) % mod
                        R[xi + xj, zi + zj] %= mod
    return R


def count_partitions(G, mod=None, verbose=False):
    """
    Returns array res[cost] = sum over vowel partitions pi of count(pi) with
    x-degree cost, i.e. the number (or weighted sum) of alphabet partitions
    into dictionary words with exactly `cost` foreign clusters.
    Products over blocks are shared along a DFS over vowel partitions.
    """
    X = max(A.shape[0] for A in G.values())
    dtype = next(iter(G.values())).dtype
    sign = np.where((NC - popcount_table()) % 2 == 0, 1, -1).astype(dtype)
    total = np.zeros(X, dtype=np.float64 if mod is None else object)
    if mod is not None:
        total = np.zeros(X, dtype=np.int64)
    nmul = [0]

    def rec(remaining, P):
        # P: accumulated product over the blocks chosen so far (or None)
        if not remaining:
            # extract z^20 and apply inclusion-exclusion sign
            if P.shape[1] <= NC:
                return
            for xi in range(X):
                if mod is None:
                    total[xi] += float(np.dot(sign, P[xi, NC]))
                else:
                    s = int(np.sum((sign * P[xi, NC]) % mod) % mod)
                    total[xi] = (total[xi] + s) % mod
            return
        v = remaining[0]
        cands = [1 << v] + [(1 << v) | (1 << w) for w in remaining[1:]]
        for B in cands:
            if B not in G:
                continue
            rest = [u for u in remaining[1:] if not (B >> u & 1)]
            nmul[0] += 1
            if P is None:
                rec(rest, G[B])
            elif rest:
                rec(rest, _mul(P, G[B], mod, NC))
            else:
                # leaf: only the z^20 coefficient of P * G[B] is needed
                Q = G[B]
                for xi in range(X):
                    for xj in range(X - xi):
                        acc = None
                        for zi in range(P.shape[1]):
                            zj = NC - zi
                            if zj < 0 or zj >= Q.shape[1]:
                                continue
                            term = P[xi, zi] * Q[xj, zj]
                            if mod is not None:
                                term %= mod
                            acc = term if acc is None else acc + term
                            if mod is not None:
                                acc %= mod
                        if acc is None:
                            continue
                        if mod is None:
                            total[xi + xj] += float(np.dot(sign, acc))
                        else:
                            s = int(np.sum((sign * acc) % mod) % mod)
                            total[xi + xj] = (total[xi + xj] + s) % mod

    rec(list(range(6)), None)
    if verbose:
        print(f"    block products: {nmul[0]}")
    return total


def crt(residues, mods):
    """Combine residues (list) modulo mods (pairwise coprime) into an integer."""
    x, M = 0, 1
    for r, m in zip(residues, mods):
        t = ((r - x) * pow(M, -1, m)) % m
        x += M * t
        M *= m
    return x % M, M


def exact_count(words, max_cost=0, nprimes=3, verbose=False, weight_fn=None):
    """Exact integer count(s) of alphabet partitions into `words` (by cost)."""
    if weight_fn is None:
        weight_fn = lambda w, v: 1
    res = []
    for p in PRIMES[:nprimes]:
        t0 = time.time()
        G = build_G(words, weight_fn, mod=p, max_cost=max_cost)
        r = count_partitions(G, mod=p, verbose=verbose)
        res.append([int(x) for x in r])
        if verbose:
            print(f"    mod {p}: {res[-1]}  ({time.time()-t0:.1f}s)")
    out = []
    for c in range(max_cost + 1):
        val, M = crt([res[i][c] for i in range(nprimes)], PRIMES[:nprimes])
        out.append(val)
    return out, M


def weighted_sum(words, weight_fn, max_cost=0, verbose=False):
    """Float64 sum over partitions of the product of per-word weights."""
    G = build_G(words, weight_fn, mod=None, max_cost=max_cost)
    return count_partitions(G, mod=None, verbose=verbose)


if __name__ == "__main__":
    # Validation 1: free CC.V.CC regime without primality has the closed form
    #   N0 = 20! * [x^20] (1+x+x^2)^12 = 20! * 1221
    import math
    t0 = time.time()
    words = free_words(2, 2, 1, prime_only=False)
    print(f"free regime, all words: {len(words):,} ({time.time()-t0:.1f}s)")
    cnt, M = exact_count(words, nprimes=3, verbose=True)
    expect = math.factorial(20) * 1221
    print(f"engine N0 = {cnt[0]:,}   closed form = {expect:,}   match = {cnt[0]==expect}")
    # Validation 2: same with float weights 1.0 -> must agree to double precision
    ws = weighted_sum(words, lambda w, v: 1.0)
    print(f"float engine N0 = {ws[0]:.6e}  rel.err = {abs(ws[0]-expect)/expect:.2e}")


# ------------------------------------------------- first-moment weights ---
import math as _math
_ODD = set("acegikoqsuwy")          # letters coprime to 26 (value == last letter mod 26)


def p_naive(w, v):
    """Crude prime-number-theorem density 1/ln n (0 for n < 2)."""
    return 0.0 if v < 2 else 1.0 / _math.log(v)


def p_refined(w, v):
    """Density conditioned on the residue of n mod 26: 0 unless the last letter
    is coprime to 26, else (26/phi(26))/ln n = (13/6)/ln n (capped at 1).
    Single-letter words (n <= 26) use their exact primality."""
    if len(w) == 1:
        return 1.0 if is_prime_py(v) else 0.0
    if w[-1] not in _ODD:
        return 0.0
    return min(1.0, (13.0 / 6.0) / _math.log(v))
