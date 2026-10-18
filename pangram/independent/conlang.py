"""A perfect pangram whose words ARE primes: A=1..Z=26, bijective base-26
(the spreadsheet-column numeration: Z=26, AA=27, AB=28, ...). Each word's
value must be prime; every word must contain a vowel (a e i o u y); and the
words must be pronounceable by a simple rule (no run of more than three
consonants, none of more than two vowels, and the word must start and end in
a cluster that English allows). Random search over orderings and cuts."""
import random, sys

ALPHA = "abcdefghijklmnopqrstuvwxyz"
VOW = set("aeiouy")
ONSETS = set("b c d f g h j k l m n p q r s t v w x z bl br ch cl cr dr dw fl fr gl gr gw kl kn kr kw ph pl pr qu sc sch scr sh shr sk sl sm sn sp sph spl spr st str sw th thr tr tw wh wr zh".split()) | {""}
CODAS = set("b c d f g h k l m n p q r s t v w x z ch ck ct ft ld lf lk lm lp lt mp nd ng nk ns nt nx ph pt rb rd rf rk rl rm rn rp rs rt sh sk sm sp st th ts xt sm lsh mph nch ngs nks nth rch rld rst rth ght lch ltz tz ltz nz rz".split()) | {""}


def value(w):
    v = 0
    for c in w:
        v = v * 26 + (ord(c) - 96)
    return v


def is_prime(n):
    if n < 2: return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0: return n == p
    d, s = n - 1, 0
    while d % 2 == 0: d //= 2; s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):   # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True


def pronounceable(w):
    runs, i = [], 0
    while i < len(w):
        j = i
        while j < len(w) and ((w[j] in VOW) == (w[i] in VOW)): j += 1
        runs.append(w[i:j]); i = j
    if not any(r[0] in VOW for r in runs): return False
    for r in runs:
        if r[0] in VOW and len(r) > 2: return False
        if r[0] not in VOW and len(r) > 3: return False
    onset = runs[0] if runs[0][0] not in VOW else ""
    coda = runs[-1] if runs[-1][0] not in VOW else ""
    return onset in ONSETS and coda in CODAS


def search(trials, seed, nwords_choices=(5, 6, 7)):
    rnd = random.Random(seed)
    letters = list(ALPHA)
    found = []
    for t in range(trials):
        rnd.shuffle(letters)
        k = rnd.choice(nwords_choices)
        cuts = sorted(rnd.sample(range(1, 26), k - 1))
        words, prev = [], 0
        for c in cuts + [26]:
            words.append("".join(letters[prev:c])); prev = c
        if all(pronounceable(w) for w in words) and all(is_prime(value(w)) for w in words):
            found.append(words)
            if len(found) >= 8: break
    return found, t + 1


if __name__ == "__main__":
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000000
    found, used = search(trials, 2026)
    print(f"{used:,} random sentences tried; {len(found)} perfect prime pangrams found")
    for words in found:
        s = " ".join(words)
        ok = sorted("".join(words)) == list(ALPHA)
        print(f"\n  {s.upper()}   (26 distinct letters: {ok})")
        for w in words:
            print(f"     {w:8s} = {value(w):>12,}  prime")
