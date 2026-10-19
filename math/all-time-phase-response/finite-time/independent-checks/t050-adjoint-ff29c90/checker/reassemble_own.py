"""Own reassembly of the four-part delivery (the supplied script is not executed).
Checks each part's size and SHA-256 against README-reassembly.txt, that each part ZIP holds exactly
one member and passes CRC checks, each chunk's size and SHA-256, then the concatenation's size and
SHA-256 and the restored ZIP's CRCs. Writes the restored ZIP exclusively.
Usage: python3 -I -B reassemble_own.py <delivery dir> <fresh output zip>"""
import hashlib, io, sys, zipfile
from pathlib import Path

D, OUT = Path(sys.argv[1]), Path(sys.argv[2])
# transcribed from README-reassembly.txt (and identical to the supplied script's table)
PARTS = [('nicu-audit-part-01-of-04.zip', 7500122, '93c393153a33c49f9df4ffc741dd62f29381596bd30f4a56b8a8a320bc87a4b1',
          'chunk-01.bin', 7500000, 'c9c5a4f37068ededce96be277a4c4b06cf76c5de1c0742cf48f73c97c0542f9c'),
         ('nicu-audit-part-02-of-04.zip', 7500122, '85bdf1837b57b0c29e8f8e7aafb430277fba680df02ed63e58c6beb769db5eae',
          'chunk-02.bin', 7500000, '5b8b983e61f56b9bf70843a57e4ecb8c4073f9329f840377f40d843404d2bc97'),
         ('nicu-audit-part-03-of-04.zip', 7500122, 'e015680752e4964b45f38a81c0d88845d469dff4f43accb2ceed0703b3eb92f8',
          'chunk-03.bin', 7500000, '67528c935a8b4e481c65bab369b9474187d85d76a3147fadb7940e0aba7089f6'),
         ('nicu-audit-part-04-of-04.zip', 4469048, 'def2fda8794312e0840d137fad5956395cb1246c937464679262464a8ad0760b',
          'chunk-04.bin', 4468926, '02ce6f9fd4d075de0dcd47c05df4e4ef9fb06d6bde7a7ed092702b826e6c7a2e')]
EXP_BYTES, EXP_SHA = 26968926, '687256807635a173aa3b7d9d42d562417fd842d25bf78ef01f98db186a3c8f37'
if OUT.exists():
    raise SystemExit(f'refusing to overwrite {OUT}')
chunks = []
for name, nb, sh, member, cb, csh in PARTS:
    raw = (D / name).read_bytes()
    assert len(raw) == nb and hashlib.sha256(raw).hexdigest() == sh, ('part', name)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        assert [i.filename for i in infos] == [member] and z.testzip() is None, ('wrapper', name)
        chunk = z.read(member)
    assert len(chunk) == cb and hashlib.sha256(chunk).hexdigest() == csh, ('chunk', name)
    print(f'ok  {name}  part {sh[:16]}  chunk {csh[:16]}  {cb} bytes')
    chunks.append(chunk)
combined = b''.join(chunks)
assert len(combined) == EXP_BYTES and hashlib.sha256(combined).hexdigest() == EXP_SHA, 'combined identity'
with zipfile.ZipFile(io.BytesIO(combined)) as z:
    assert z.testzip() is None, 'combined CRC'
    names = z.namelist()
    bad = [n for n in names if n.startswith('/') or '..' in Path(n).parts or '\\' in n]
    assert not bad, ('unsafe member paths', bad)
    links = [i.filename for i in z.infolist() if (i.external_attr >> 16) & 0o170000 == 0o120000]
    assert not links, ('symlink members', links)
with OUT.open('xb') as f:
    f.write(combined)
print(f'restored {OUT}  {len(combined)} bytes  sha256 {EXP_SHA}  members {len(names)}  CRC ok, no unsafe paths or symlinks')
