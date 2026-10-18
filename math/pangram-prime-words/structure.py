"""
Structural explanation of result (1): the English lists cannot work for a
reason that has nothing to do with WHICH numbers are prime.  Every number
here is computed from clusters.py.

Fact 1 (arithmetic).  26^k = 0 (mod 26) for k >= 1, so value(w) = (index of
the last letter) mod 26.  A prime > 26 is coprime to 26, so every prime word
of >= 2 letters ends in one of  a c e g i k o q s u w y.  (The only prime
1-letter word with a vowel is E = 5, which also ends in that set.)
Hence a NON-EMPTY coda of a prime word ends in c, g, k, q, s or w ("odd coda").

Fact 2 (packing).  A perfect pangram has 3..6 words (each word has 1-2 of the
6 vowels); each word has one onset and one coda.  So the 20 consonants must be
covered exactly by <= 6 letter-disjoint English onsets plus <= 6 letter-disjoint
odd English codas.  This is a pure exact-cover question on the cluster lists;
we decide it by a subset DP over the 2^20 consonant subsets:
    dp[a][S] = minimum number of codas needed to cover S exactly with
               a onsets and some odd codas (inf if impossible).
If dp[a][ALL] > 6 for every a <= 6, no solution exists under the lists,
whatever the primes do.  The same DP, run with one extra cluster added, tells
which single additions make the packing feasible (used in task b).
"""
import sys
import numpy as np
from core import *

NSC = 1 << 20
INF = 99
ODD = set("acegikoqsuwy")


def packing_dp(onsets, codas, max_words=6):
    """Return dp[a][S] (a = 0..max_words) as described above."""
    dp = np.full((max_words + 1, NSC), INF, dtype=np.int8)
    dp[0][0] = 0
    S = np.arange(NSC, dtype=np.int64)
    items = [(cmask(o), "on") for o in onsets if o] + \
            [(cmask(c), "co") for c in codas if c and c[-1] in ODD]
    for m, kind in items:
        idx = S[(S & m) == 0]
        tgt = idx | m
        new = dp.copy()
        if kind == "on":
            for a in range(max_words):
                cand = dp[a][idx]
                new[a + 1][tgt] = np.minimum(new[a + 1][tgt], cand)
        else:
            for a in range(max_words + 1):
                cand = dp[a][idx] + 1
                new[a][tgt] = np.minimum(new[a][tgt], cand)
        dp = new
    return dp


def report(onsets, codas, label):
    dp = packing_dp(onsets, codas)
    pc = np.zeros(NSC, dtype=np.int64)
    for b in range(20):
        pc[1 << b:1 << (b + 1)] = pc[:1 << b] + 1
    feasible = (dp <= 6).any(axis=0)            # some a <= 6 with <= 6 codas
    full_ok = bool(feasible[NSC - 1])
    best = int(pc[feasible].max())
    mand = cmask("jqvxz")
    withm = feasible & ((S_ALL & mand) == mand)
    bestm = int(pc[withm].max()) if withm.any() else -1
    print(f"{label}: all 20 consonants coverable by <=6 onsets + <=6 odd codas: {full_ok}; "
          f"max coverable consonants: {best} (with j,q,v,x,z all placed: {bestm})")
    return full_ok, best, bestm


S_ALL = np.arange(NSC, dtype=np.int64)

if __name__ == "__main__":
    odd_codas = [c for c in CODAS if c and c[-1] in ODD]
    print(f"non-empty codas: {len(CODAS)-1}; odd codas (end in c,g,k,q,s,w): {len(odd_codas)}")
    print("  ", " ".join(odd_codas))
    for L in "jqvxz":
        print(f"  {L}: in onsets {[o for o in ONSETS if L in o]}, in odd codas {[c for c in odd_codas if L in c]}")
    print()
    report(ONSETS, CODAS, "English lists")
    # how much does the packing bound explain of the relaxations?  (task b)
    print()
    for L in (1, 2, 3):
        report(sorted(set(ONSETS) | set(free_clusters(L))), CODAS, f"English + any onset of <= {L} consonants")
        report(ONSETS, sorted(set(CODAS) | set(free_clusters(L))), f"English + any coda of <= {L} consonants")


def packing_min_foreign(onsets, codas, english_onsets, english_codas, max_words=6):
    """
    Lower bound for the number of NON-English clusters any solution must use:
    dp[a][c][S] = minimum number of non-English items among a letter-disjoint
    onsets and c odd codas covering the consonant set S exactly (INF if
    impossible), a, c <= max_words.  Returns min over a, c of dp[a][c][ALL].
    """
    dp = np.full((max_words + 1, max_words + 1, NSC), INF, dtype=np.int8)
    dp[0][0][0] = 0
    S = np.arange(NSC, dtype=np.int64)
    eo, ec = set(english_onsets), set(english_codas)
    items = [(cmask(o), "on", o not in eo) for o in onsets if o] + \
            [(cmask(c), "co", c not in ec) for c in codas if c and c[-1] in ODD]
    for m, kind, foreign in items:
        idx = S[(S & m) == 0]
        tgt = idx | m
        new = dp.copy()
        add = 1 if foreign else 0
        if kind == "on":
            for a in range(max_words):
                for c in range(max_words + 1):
                    new[a + 1][c][tgt] = np.minimum(new[a + 1][c][tgt], dp[a][c][idx] + add)
        else:
            for a in range(max_words + 1):
                for c in range(max_words):
                    new[a][c + 1][tgt] = np.minimum(new[a][c + 1][tgt], dp[a][c][idx] + add)
        dp = new
    return int(dp[:, :, NSC - 1].min())
