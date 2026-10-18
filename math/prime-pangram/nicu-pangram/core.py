"""
Core utilities shared by all scripts.

Numeration (fixed by the task): bijective base-26, A=1 ... Z=26,
    value("ab") = 1*26 + 2 = 28.
Letters are encoded as bits 0..25 (a=0 ... z=25) in a 26-bit mask.
"""
import ctypes, itertools, os, sys
import numpy as np
from clusters import VOWELS, CONSONANTS, ONSETS, CODAS

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FULL = (1 << 26) - 1
VOWEL_MASK = sum(1 << (ord(c) - 97) for c in VOWELS)
CONS_MASK = FULL ^ VOWEL_MASK
CONS_LIST = list(CONSONANTS)                      # 20 consonants in bit order
CONS_INDEX = {c: i for i, c in enumerate(CONS_LIST)}   # consonant -> 0..19
VOWEL_INDEX = {v: i for i, v in enumerate(VOWELS)}      # vowel -> 0..5


def value(word: str) -> int:
    """Bijective base-26 value, A=1..Z=26 (the task's numeration)."""
    v = 0
    for ch in word:
        v = v * 26 + (ord(ch) - 96)
    return v


def mask(word: str) -> int:
    m = 0
    for ch in word:
        m |= 1 << (ord(ch) - 97)
    return m


def cmask(word: str) -> int:
    """20-bit consonant mask (bit i = CONS_LIST[i])."""
    m = 0
    for ch in word:
        if ch in CONS_INDEX:
            m |= 1 << CONS_INDEX[ch]
    return m


def vset(word: str) -> int:
    """6-bit vowel mask."""
    m = 0
    for ch in word:
        if ch in VOWEL_INDEX:
            m |= 1 << VOWEL_INDEX[ch]
    return m


def mask_to_str(m: int) -> str:
    return "".join(ALPHABET[i] for i in range(26) if m >> i & 1)


# ------------------------------------------------------------ primality ---
_SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime_py(n: int) -> bool:
    """Deterministic Miller-Rabin, valid for n < 3.3e24 (all values here)."""
    if n < 2:
        return False
    for p in _SMALL:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


_lib = None


def _load_lib():
    global _lib
    if _lib is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libmr.so")
        if not os.path.exists(path):
            os.system(f"gcc -O2 -shared -fPIC -o {path} {path[:-6]}mr.c")
        _lib = ctypes.CDLL(path)
        _lib.is_prime_batch.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]
        _lib.is_prime_batch.restype = None
    return _lib


def is_prime_batch(values: np.ndarray) -> np.ndarray:
    """Vectorised deterministic Miller-Rabin on a uint64 array (C helper)."""
    vals = np.ascontiguousarray(values, dtype=np.uint64)
    out = np.zeros(len(vals), dtype=np.uint8)
    if len(vals):
        _load_lib().is_prime_batch(vals.ctypes.data, len(vals), out.ctypes.data)
    return out.astype(bool)


# --------------------------------------------------------- word regimes ---
def free_clusters(max_len: int):
    """All strings of distinct consonants with length 0..max_len."""
    out = [""]
    for L in range(1, max_len + 1):
        out += ["".join(p) for p in itertools.permutations(CONS_LIST, L)]
    return out


def nuclei(max_vowels: int = 2):
    """Nuclei: one vowel, or (if max_vowels==2) any ordered pair of distinct vowels."""
    out = list(VOWELS)
    if max_vowels >= 2:
        out += ["".join(p) for p in itertools.permutations(VOWELS, 2)]
    return out


def _cluster_arrays(strings):
    """masks (26-bit), values, lengths of a list of strings as numpy arrays."""
    m = np.array([mask(s) for s in strings], dtype=np.int64)
    v = np.array([value(s) for s in strings], dtype=np.uint64)
    L = np.array([len(s) for s in strings], dtype=np.int64)
    return m, v, L


def generate_words(onsets, nucs, codas, prime_only=True, with_tags=False,
                   onset_tag=None, coda_tag=None):
    """
    Enumerate every word onset+nucleus+coda with pairwise distinct letters.
    Returns a list of (word, value, mask) (prime ones only if prime_only).
    If with_tags, each tuple also carries (onset, coda) so a caller can score
    clusters (e.g. count non-English clusters).  Vectorised with numpy.
    """
    om, ov, oL = _cluster_arrays(onsets)
    nm, nv, nL = _cluster_arrays(nucs)
    cm, cv, cL = _cluster_arrays(codas)
    pow26 = np.array([26 ** k for k in range(12)], dtype=np.uint64)
    results = []
    # stage 1: onset x nucleus
    on_pairs = []
    for i in range(len(onsets)):
        ok = (nm & om[i]) == 0
        for j in np.nonzero(ok)[0]:
            on_pairs.append((i, j))
    on_pairs = np.array(on_pairs, dtype=np.int64).reshape(-1, 2)
    pm = om[on_pairs[:, 0]] | nm[on_pairs[:, 1]]
    pv = ov[on_pairs[:, 0]] * pow26[nL[on_pairs[:, 1]]] + nv[on_pairs[:, 1]]
    # stage 2: x coda, chunked over codas
    for k in range(len(codas)):
        ok = (pm & cm[k]) == 0
        idx = np.nonzero(ok)[0]
        if len(idx) == 0:
            continue
        vals = pv[idx] * pow26[cL[k]] + cv[k]
        if prime_only:
            pr = is_prime_batch(vals)
            idx, vals = idx[pr], vals[pr]
        for t, val in zip(idx, vals):
            i, j = on_pairs[t]
            w = onsets[i] + nucs[j] + codas[k]
            if with_tags:
                results.append((w, int(val), pm[t] | cm[k], onsets[i], codas[k]))
            else:
                results.append((w, int(val), int(pm[t] | cm[k])))
    return results


def english_words(prime_only=True, max_vowels=2):
    return generate_words(ONSETS, nuclei(max_vowels), CODAS, prime_only=prime_only)


def free_words(max_onset=2, max_coda=2, max_vowels=1, prime_only=True):
    return generate_words(free_clusters(max_onset), nuclei(max_vowels),
                          free_clusters(max_coda), prime_only=prime_only)


# --------------------------------------------------------- exact cover ---
def exact_cover(words, max_solutions=1, costs=None, budget=0, full=FULL, verbose=False):
    """
    Enumerate ways to partition the letters of `full` into words.
    words: list of (word, value, mask).  costs: optional per-word integer
    cost; only covers with total cost <= budget are explored.
    Returns (solutions, nodes).  Each solution is a list of word indices.
    Algorithm X with 'uncovered letter having the fewest candidates' branching.
    """
    n = len(words)
    masks = np.array([w[2] for w in words], dtype=np.int64)
    cost = np.zeros(n, dtype=np.int64) if costs is None else np.asarray(costs, dtype=np.int64)
    by_letter = [np.nonzero(masks >> b & 1)[0] for b in range(26)]
    sols, nodes = [], [0]

    def rec(covered, chosen, left):
        nodes[0] += 1
        if covered == full:
            sols.append(list(chosen))
            return len(sols) >= max_solutions
        best_bit, best_c = -1, None
        rem = full & ~covered
        b = 0
        while rem:
            if rem & 1:
                ids = by_letter[b]
                ok = ((masks[ids] & covered) == 0) & (cost[ids] <= left)
                c = ids[ok]
                if best_c is None or len(c) < len(best_c):
                    best_bit, best_c = b, c
                    if len(c) == 0:
                        return False
            rem >>= 1
            b += 1
        for i in best_c:
            chosen.append(int(i))
            if rec(covered | int(masks[i]), chosen, left - int(cost[i])):
                return True
            chosen.pop()
        return False

    rec(0, [], budget)
    return sols, nodes[0]


def show(words, sol):
    return " ".join(words[i][0].upper() for i in sol) + "   values: " + \
        " / ".join(f"{words[i][1]:,}" for i in sol)


if __name__ == "__main__":
    assert value("ab") == 28 and value("a") == 1 and value("z") == 26
    assert value("xwozc") == 11_382_491 and value("tvyrq") == 9_543_577
    assert value("kjums") == 5_217_049 and value("lfe") == 8273
    assert value("bpi") == 1777 and value("hdang") == 3_727_159
    import random
    rnd = random.Random(1)
    test = np.array([rnd.randrange(2, 26 ** 10) for _ in range(20000)] + [2, 3, 4, 5, 25, 27, 97, 561, 1_000_003], dtype=np.uint64)
    c = is_prime_batch(test)
    assert all(bool(c[i]) == is_prime_py(int(test[i])) for i in range(len(test)))
    print("self-test ok")


# --------------------------------------------------- C exact cover driver ---
def exact_cover_c(words, max_solutions=1, costs=None, budget=0, full=FULL, tag="tmp", cap=None):
    """
    Same contract as exact_cover() but runs the bitset C program xcover
    (compiled from xcover.c).  Returns (solutions, nodes).
    """
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    exe = os.path.join(here, "xcover")
    if not os.path.exists(exe):
        subprocess.check_call(["gcc", "-O2", "-o", exe, os.path.join(here, "xcover.c")])
    path = os.path.join(here, "results", f"_xcover_{tag}.dat")
    with open(path, "w") as f:
        for i, w in enumerate(words):
            f.write(f"{w[2]} {0 if costs is None else int(costs[i])}\n")
    if cap is None:
        cap = max(sum(ch not in VOWELS for ch in w[0]) for w in words)
    out = subprocess.run([exe, path, str(max_solutions), str(budget), str(full), str(cap)],
                         capture_output=True, text=True, check=True).stdout.splitlines()
    sols = [list(map(int, line.split())) for line in out if line and not line.startswith("nodes=")]
    nodes = int(out[-1].split()[0].split("=")[1])
    os.remove(path)
    return sols, nodes
