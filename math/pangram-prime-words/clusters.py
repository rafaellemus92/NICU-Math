"""
Fixed orthographic English onset / coda cluster lists.

The task statement said "[paste ONSETS]" / "[paste CODAS]" but no lists were
supplied, so the lists below are the ones used by every script in this
directory.  They are *letter* clusters (not phonemes), because the numeration
is on letters.  Conventions:

  * y is a VOWEL (the vowel set is a e i o u y), so y never appears in a
    cluster ("yes" = onset "" + nucleus "ye" + coda "s").
  * "qu" is onset "q" followed by the vowel u; "squ" is onset "sq".
  * Silent-e spellings do not create codas ("curve" is NOT evidence for a
    coda "rv"), because a word must be onset + nucleus + coda with the
    nucleus in the middle.
  * Clusters with a doubled letter (ll, ss, ff, tt, zz ...) are omitted: a
    perfect pangram can never use them.
  * Every single consonant is an onset.  Single-consonant codas exclude j and
    q (no ordinary English word ends in j or q) and v (final v is non-standard:
    "rev", "spiv").  The exclusion of q matters for the structural argument in
    README.md; the exclusion of j and v does not matter for primality
    (any word ending in j or v is even).

Each cluster is given with an example word.  Change the lists here and every
number in the README changes accordingly; dictionary sizes are printed by the
scripts so a reader can see what list they are looking at.
"""

VOWELS = "aeiouy"
CONSONANTS = "bcdfghjklmnpqrstvwxz"
assert len(VOWELS) == 6 and len(CONSONANTS) == 20
assert set(VOWELS + CONSONANTS) == set("abcdefghijklmnopqrstuvwxyz")

# ---------------------------------------------------------------- onsets ---
ONSET_EXAMPLES = {
    "": "(no onset: 'at')",
    # single consonants (all 20)
    "b": "bat", "c": "cat", "d": "dog", "f": "fun", "g": "go", "h": "hat",
    "j": "jam", "k": "kit", "l": "let", "m": "map", "n": "no", "p": "pit",
    "q": "quit (q + vowel u)", "r": "run", "s": "sun", "t": "top", "v": "van",
    "w": "wet", "x": "xenon", "z": "zoo",
    # two consonants
    "bl": "blue", "br": "brown", "ch": "chip", "cl": "clap", "cr": "crab",
    "dr": "drum", "dw": "dwarf", "fl": "flat", "fr": "frog", "gh": "ghost",
    "gl": "glad", "gn": "gnome", "gr": "grab", "kn": "knee", "mn": "mnemonic",
    "ph": "photo", "pl": "plan", "pn": "pneumatic", "pr": "pram", "ps": "psalm",
    "pt": "pterodactyl", "rh": "rhyme", "sc": "scan", "sh": "ship", "sk": "skip",
    "sl": "slip", "sm": "small", "sn": "snap", "sp": "spin", "sq": "squid (sq + u)",
    "st": "stop", "sw": "swim", "th": "thin", "tr": "trap", "tw": "twin",
    "wh": "what", "wr": "write",
    # three consonants
    "chr": "chrome", "phl": "phlegm", "phr": "phrase", "sch": "school",
    "scr": "scrap", "shr": "shred", "sph": "sphere", "spl": "split",
    "spr": "spring", "str": "strap", "thr": "three", "thw": "thwart",
}

# ----------------------------------------------------------------- codas ---
CODA_EXAMPLES = {
    "": "(no coda: 'go')",
    # single consonants (17: no j, q, v)
    "b": "cab", "c": "arc/tic", "d": "bad", "f": "if", "g": "bag", "h": "oh",
    "k": "yak", "l": "pal", "m": "ham", "n": "an", "p": "cap", "r": "car",
    "s": "gas", "t": "at", "w": "cow", "x": "box", "z": "quiz",
    # two consonants
    "bs": "cabs", "bt": "debt", "ch": "rich", "ck": "back", "cs": "arcs",
    "ct": "act", "ds": "lids", "fs": "ifs", "ft": "loft", "gh": "laugh",
    "gm": "paradigm", "gn": "sign", "gs": "bags", "ks": "yaks", "lb": "bulb",
    "lc": "talc", "ld": "old", "lf": "elf", "lk": "milk", "lm": "film",
    "ln": "kiln", "lp": "help", "ls": "pals", "lt": "salt", "mb": "lamb",
    "mn": "hymn", "mp": "lamp", "ms": "hams", "nc": "zinc", "nd": "and",
    "ng": "sing", "nk": "ink", "ns": "cans", "nt": "ant", "nx": "lynx",
    "ph": "graph", "ps": "caps", "pt": "apt", "rb": "herb", "rc": "arc",
    "rd": "bird", "rf": "surf", "rg": "berg", "rk": "ark", "rl": "girl",
    "rm": "arm", "rn": "barn", "rp": "harp", "rs": "cars", "rt": "art",
    "sh": "ash", "sk": "ask", "sm": "prism", "sp": "wasp", "st": "best",
    "th": "bath", "ts": "cats", "tz": "blitz", "wd": "crowd", "wk": "hawk",
    "wl": "owl", "wn": "own", "ws": "cows", "wt": "newt", "xt": "next",
    # three consonants
    "bts": "debts", "cht": "yacht", "cks": "backs", "cts": "acts",
    "dst": "midst", "dth": "width", "fth": "fifth", "fts": "lofts",
    "ghs": "laughs", "ght": "night", "gms": "paradigms", "gns": "signs",
    "lbs": "bulbs", "lch": "belch", "lcs": "talcs", "lds": "folds",
    "lfs": "elfs/golfs", "lks": "milks", "lms": "films", "lns": "kilns",
    "lps": "helps", "lpt": "sculpt", "lsh": "welsh", "lst": "whilst",
    "lth": "health", "lts": "salts", "ltz": "waltz", "mbs": "lambs",
    "mns": "hymns", "mph": "nymph", "mps": "lamps", "mpt": "prompt",
    "nch": "bench", "ncs": "zincs", "nct": "instinct", "nds": "hands",
    "ngs": "sings", "ngst": "angst", "nks": "inks", "nst": "against",
    "nth": "month", "nts": "ants", "phs": "graphs", "pth": "depth",
    "pts": "apts", "rbs": "herbs", "rch": "arch", "rcs": "arcs", "rds": "birds",
    "rfs": "surfs", "rgs": "bergs", "rks": "arks", "rld": "world",
    "rls": "girls", "rms": "arms", "rns": "barns", "rnt": "burnt",
    "rps": "harps", "rpt": "excerpt", "rsh": "marsh", "rst": "first",
    "rth": "earth", "rts": "arts", "rtz": "quartz", 
    "tch": "match", "ths": "baths",
    "wds": "crowds", "wks": "hawks", "wls": "owls", "wns": "owns",
    "wts": "newts", "xth": "sixth", "xts": "texts",
    # four / five consonants
    "dths": "widths", "fths": "fifths", "ghts": "nights",
    "lfth": "twelfth", "lpts": "sculpts", "lths": "tilths", "mphs": "nymphs",
    "mpts": "prompts", "ncts": "instincts", "ngth": "length", "nths": "months",
    "pths": "depths", "rlds": "worlds", "rpts": "excerpts", "rths": "earths",
    "xths": "sixths", "chts": "yachts",
    "lfths": "twelfths", "ngths": "lengths",
}

ONSETS = sorted(ONSET_EXAMPLES, key=lambda s: (len(s), s))
CODAS = sorted(CODA_EXAMPLES, key=lambda s: (len(s), s))

for _c in ONSETS + CODAS:
    assert all(ch in CONSONANTS for ch in _c), _c
    assert len(set(_c)) == len(_c), _c   # no doubled letters

if __name__ == "__main__":
    print("onsets:", len(ONSETS), "(incl. empty)")
    print("codas: ", len(CODAS), "(incl. empty)")
    print("max onset len", max(map(len, ONSETS)), "max coda len", max(map(len, CODAS)))
    for L in range(6):
        print(f"  onsets of length {L}: {sum(len(c)==L for c in ONSETS):3d}   codas of length {L}: {sum(len(c)==L for c in CODAS):3d}")
