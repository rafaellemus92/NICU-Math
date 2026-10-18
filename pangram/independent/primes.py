"""Is there a perfect pangram (each of A–Z exactly once) made only of words that
name prime numbers in some language?  Exact cover over 26 letters.

Word list: prime-number names in Latin-script languages, kept only if the word
has no repeated letter.  Tags: 'd' = a diacritic was stripped (pět→pet),
'h' = hyphenated compound (dix-sept), 'c' = constructed language (Esperanto,
Klingon), 'r' = romanization of a non-Latin script (Hindi, Persian, Hebrew…).
Untagged = natural language, native Latin spelling, single word.
"""
import itertools, sys

WORDS = [
    # word, language, number, tags
    ("two", "English", 2, ""), ("five", "English", 5, ""),
    ("dos", "Spanish", 2, ""), ("tres", "Spanish", 3, ""), ("once", "Spanish", 11, ""),
    ("deux", "French", 2, ""), ("trois", "French", 3, ""), ("cinq", "French", 5, ""), ("sept", "French", 7, ""), ("onze", "French", 11, ""),
    ("dix-sept", "French", 17, "h"), ("dix-neuf", "French", 19, "h"),
    ("zwei", "German", 2, ""), ("drei", "German", 3, ""), ("elf", "German", 11, ""),
    ("due", "Italian", 2, ""), ("tre", "Italian", 3, ""), ("cinque", "Italian", 5, ""),
    ("duo", "Latin", 2, ""), ("undecim", "Latin", 11, ""),
    ("drie", "Dutch", 3, ""), ("vijf", "Dutch", 5, ""),
    ("tva", "Swedish", 2, "d"), ("fem", "Swedish", 5, ""), ("sju", "Swedish", 7, ""), ("elva", "Swedish", 11, ""),
    ("to", "Danish", 2, ""), ("syv", "Danish", 7, ""),
    ("vyf", "Afrikaans", 5, ""), ("sewe", "Afrikaans", 7, ""),
    ("tveir", "Icelandic", 2, ""), ("sjo", "Icelandic", 7, "d"),
    ("kolme", "Finnish", 3, ""),
    ("kolm", "Estonian", 3, ""),
    ("tris", "Latvian", 3, "d"),
    ("du", "Lithuanian", 2, ""), ("trys", "Lithuanian", 3, ""), ("penki", "Lithuanian", 5, ""), ("septyni", "Lithuanian", 7, ""), ("trylika", "Lithuanian", 13, ""),
    ("dwa", "Polish", 2, ""), ("trzy", "Polish", 3, ""), ("piec", "Polish", 5, "d"),
    ("dva", "Czech", 2, ""), ("tri", "Czech", 3, "d"), ("pet", "Czech", 5, "d"), ("sedm", "Czech", 7, ""), ("sedmnact", "Czech", 17, "d"),
    ("harom", "Hungarian", 3, "d"), ("het", "Hungarian", 7, "d"),
    ("doi", "Romanian", 2, ""), ("trei", "Romanian", 3, ""),
    ("dy", "Albanian", 2, ""), ("pese", "Albanian", 5, "d"),
    ("dyo", "Greek", 2, "r"), ("tria", "Greek", 3, "r"), ("epta", "Greek", 7, "r"),
    ("uc", "Turkish", 3, "d"), ("bes", "Turkish", 5, "d"), ("yedi", "Turkish", 7, ""), ("onbir", "Turkish", 11, ""),
    ("uch", "Uzbek", 3, ""), ("besh", "Uzbek", 5, ""),
    ("do", "Persian", 2, "r"), ("se", "Persian", 3, "r"), ("panj", "Persian", 5, "r"), ("haft", "Persian", 7, "r"), ("sizdah", "Persian", 13, "r"), ("nuzdah", "Persian", 19, "r"),
    ("panch", "Hindi", 5, "r"), ("sat", "Hindi", 7, "r"), ("terah", "Hindi", 13, "r"),
    ("dvi", "Sanskrit", 2, "r"),
    ("shtayim", "Hebrew", 2, "r"), ("sheva", "Hebrew", 7, "r"),
    ("er", "Mandarin", 2, "r"), ("san", "Mandarin", 3, "r"), ("wu", "Mandarin", 5, "r"), ("qi", "Mandarin", 7, "r"),
    ("ni", "Japanese", 2, "r"), ("go", "Japanese", 5, "r"), ("jusan", "Japanese", 13, "r"),
    ("sam", "Korean", 3, "r"), ("chil", "Korean", 7, "r"),
    ("song", "Thai", 2, "r"), ("ha", "Thai", 5, "r"), ("chet", "Thai", 7, "r"),
    ("pram", "Khmer", 5, "r"),
    ("hai", "Vietnamese", 2, "d"), ("ba", "Vietnamese", 3, ""), ("nam", "Vietnamese", 5, "d"), ("bay", "Vietnamese", 7, "d"),
    ("dua", "Indonesian", 2, ""), ("tiga", "Indonesian", 3, ""), ("lima", "Indonesian", 5, ""),
    ("pito", "Tagalog", 7, ""),
    ("tano", "Swahili", 5, ""),
    ("hlanu", "Zulu", 5, ""),
    ("arun", "Yoruba", 5, "d"),
    ("biyu", "Hausa", 2, ""), ("biyar", "Hausa", 5, ""),
    ("shan", "Somali", 5, ""),
    ("amist", "Amharic", 5, "r"), ("sebat", "Amharic", 7, "r"),
    ("hing", "Armenian", 5, "r"),
    ("gurav", "Mongolian", 3, "r"), ("tav", "Mongolian", 5, "r"),
    ("ezhu", "Tamil", 7, "r"),
    ("rua", "Maori", 2, ""), ("toru", "Maori", 3, ""), ("rima", "Maori", 5, ""), ("whitu", "Maori", 7, ""),
    ("fitu", "Samoan", 7, ""), ("vitu", "Fijian", 7, ""),
    ("elua", "Hawaiian", 2, ""), ("ekolu", "Hawaiian", 3, ""), ("ehiku", "Hawaiian", 7, ""),
    ("iskay", "Quechua", 2, ""), ("kimsa", "Quechua", 3, ""), ("pichqa", "Quechua", 5, ""), ("qanchis", "Quechua", 7, ""),
    ("ome", "Nahuatl", 2, ""), ("yei", "Nahuatl", 3, ""),
    ("bi", "Basque", 2, ""), ("hiru", "Basque", 3, ""), ("bost", "Basque", 5, ""),
    ("dau", "Welsh", 2, ""), ("saith", "Welsh", 7, ""),
    ("cuig", "Irish", 5, "d"), ("seacht", "Irish", 7, ""),
    ("dha", "Scottish Gaelic", 2, "d"), ("coig", "Scottish Gaelic", 5, "d"), ("seachd", "Scottish Gaelic", 7, ""),
    ("dew", "Cornish", 2, ""), ("try", "Cornish", 3, ""), ("seyth", "Cornish", 7, ""),
    ("daou", "Breton", 2, ""), ("seizh", "Breton", 7, ""),
    ("ob", "Hmong", 2, ""), ("peb", "Hmong", 3, ""), ("tsib", "Hmong", 5, ""), ("xya", "Hmong", 7, ""),
    ("sixty-one", "English", 61, "h"),
    # constructed languages
    ("kvin", "Esperanto", 5, "c"), ("sep", "Esperanto", 7, "c"), ("kin", "Ido", 5, "c"),
    ("wej", "Klingon", 3, "c"), ("vagh", "Klingon", 5, "c"), ("soch", "Klingon", 7, "c"),
]

ALPHA = "abcdefghijklmnopqrstuvwxyz"
FULL = (1 << 26) - 1


def letters_of(w):
    return "".join(c for c in w if c.isalpha())


def mask(w):
    m = 0
    for c in letters_of(w):
        b = 1 << (ord(c) - 97)
        if m & b:
            return None          # repeated letter: unusable
        m |= b
    return m


def solve(words, want_best=False):
    """Exact cover by DFS on the least-covered letter.  Returns (solutions, best_partial)."""
    items = [(w, mask(w)) for w in words]
    items = [(w, m) for w, m in items if m]
    by_letter = {i: [it for it in items if it[1] >> i & 1] for i in range(26)}
    sols, best = [], (0, [])

    def rec(cov, chosen):
        nonlocal best
        if cov == FULL:
            sols.append(list(chosen)); return
        # choose the uncovered letter with the fewest compatible words
        cand_letter, cands = None, None
        for i in range(26):
            if cov >> i & 1: continue
            c = [it for it in by_letter[i] if not it[1] & cov]
            if cands is None or len(c) < len(cands):
                cand_letter, cands = i, c
            if not c: break
        if not cands:
            if want_best:
                n = bin(cov).count("1")
                if n > best[0]: best = (n, list(chosen))
                # also allow skipping this letter to keep looking for a larger partial cover
                return
            return
        for w, m in cands:
            chosen.append(w); rec(cov | m, chosen); chosen.pop()
            if sols and not want_best: return

    rec(0, [])
    return sols, best


def best_partial(words):
    """Largest number of letters coverable by disjoint words (set packing), by DFS over letters in order with skips."""
    items = [(w, m) for w, m in ((w, mask(w)) for w in words) if m]
    best = (0, [])

    def rec(i, cov, chosen):
        nonlocal best
        n = bin(cov).count("1")
        if n > best[0]: best = (n, list(chosen))
        if i == 26: return
        # upper bound: remaining letters
        if n + (26 - i) <= best[0]: return
        if cov >> i & 1:
            rec(i + 1, cov, chosen); return
        for w, m in items:
            if m >> i & 1 and not m & cov:
                chosen.append(w); rec(i + 1, cov | m, chosen); chosen.pop()
        rec(i + 1, cov, chosen)   # leave letter i uncovered

    rec(0, 0, [])
    return best


def run(label, allowed_tags):
    words = [w for w, lang, n, t in WORDS if all(ch in allowed_tags for ch in t)]
    usable = [w for w in words if mask(w)]
    sols, _ = solve(usable)
    print(f"\n== {label}: {len(usable)} usable words ==")
    if sols:
        for s in sols[:5]:
            print("  PERFECT PANGRAM:", " ".join(s), "->", sorted("".join(letters_of(w) for w in s)) == list(ALPHA))
    else:
        n, chosen = best_partial(usable)
        cov = "".join(letters_of(w) for w in chosen)
        missing = [c for c in ALPHA if c not in cov]
        print(f"  no perfect pangram. best disjoint cover: {n}/26 letters")
        print("  words:", " ".join(chosen))
        print("  missing:", " ".join(missing))
    return bool(sols)


if __name__ == "__main__":
    info = {w: (lang, n, t) for w, lang, n, t in WORDS}
    bad = [w for w in info if not mask(w)]
    print("words with repeated letters (dropped):", " ".join(bad) or "none")
    for i, a in enumerate(ALPHA):
        ws = [w for w in info if mask(w) and (mask(w) >> i & 1)]
        if len(ws) <= 4: print(f"  letter {a}: only {len(ws)} words -> {ws}")
    run("strict: natural languages, native Latin spelling, one word", "")
    run("+ romanizations", "r")
    run("+ romanizations + stripped diacritics", "rd")
    run("+ hyphenated compounds too", "rdh")
    run("+ constructed languages too", "rdhc")
