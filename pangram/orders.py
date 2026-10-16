"""
Named digit assignments ("transliterations") for the order experiment.
Each is a permutation of a-z; letter ORDER[i] gets digit i+1.  They are
conventions, stated explicitly so they can be criticised and changed.

alphabetical : the task's A=1..Z=26 (note: all six vowels sit on odd digits).
breath_path  : the nucleus first (vowels ordered by jaw opening, i.e. by the
               first formant: a o e u i y), then consonants in the order the
               breath meets their place of articulation on the way out:
               glottal h; velar k g c q x; postalveolar j; alveolar t d n s z l r;
               labiodental f v; bilabial p b m w.
lips_first   : the same path read from the lips inward, vowels last.
acoustic_up  : rough ascending order of the dominant spectral energy of each
               letter's usual English sound (nasals and voiced stops low, back
               vowels, liquids, front vowels, affricate, voiceless stops, then
               the sibilants and f highest).
acoustic_down: the same order descending (s = 1 ... m = 26).
"""
ORDERS = {
    "alphabetical":  "abcdefghijklmnopqrstuvwxyz",
    "breath_path":   "aoeuiy" + "hkgcqxjtdnszlrfvpbmw",
    "lips_first":    "wmbpvfrlzsndtjxqcgkh" + "yiueoa",
    "acoustic_up":   "mnwbdguovalrheiyjpkqctzxfs",
    "acoustic_down": "sfxztcqkpjyiehrlavoug" + "dbwnm",
}
for k, v in ORDERS.items():
    assert sorted(v) == list("abcdefghijklmnopqrstuvwxyz"), k
