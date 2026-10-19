"""Derive chain_percell_t050.py from the regenerated, reviewed T=1/4 chain_percell.py (sha256 0af7b93e...)
by two exact textual patches, each required to apply exactly once: the horizon T=0.25 -> 0.5 in the
interval constant and in the scope assertion. The recursion and every formula are unchanged; with
500 coarse cells the cell width stays 1/1000. Display strings that still say 'T = 0.25' are cosmetic."""
import hashlib, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = HERE/'endpoint-sign'/'scripts'/'chain_percell.py'
text = src.read_text()
assert hashlib.sha256(text.encode()).hexdigest() == '0af7b93e89fdd88ce105a0e0f9d3c31148221171b8b5c2620558569b77824b8b'
for old, new in [("    T = Iv.of('0.25')\n", "    T = Iv.of('0.5')\n"),
                 ("and P['T'] == 0.25\n", "and P['T'] == 0.5\n")]:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
out = HERE/'endpoint-sign'/'scripts'/'chain_percell_t050.py'
with out.open('x') as f:
    f.write(text)
print('wrote', out, hashlib.sha256(text.encode()).hexdigest())
