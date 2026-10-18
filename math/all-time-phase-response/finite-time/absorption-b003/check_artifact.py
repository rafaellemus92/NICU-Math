"""check_artifact.py -- the standing check of this folder's artifact: verify the saved trajectory
arrays' hashes and, with --full, rerun the validator end to end and compare with the committed results.

Step 1 (seconds). SHA-256 of trajectory/W_nodes.npy and trajectory/Q_nodes.npy, both of the files and of
the raw array bytes, against results/trajectory_manifest.json, results/numerics.json and
results/validated.json; shapes, dtypes and sizes against the manifest. These files are the exact arrays
that define the approximation validated by validate_residual.py; any change to them, including a
regeneration on another platform, makes them a different approximation (to be re-validated, not rejected).

Step 2 (--full, about 11 minutes on 4 cores). Run validate_residual.py into a scratch file and compare its
'cells', 'initial', 'coarse_t_right', 'diagnostics' and 'provenance' (except wall time) with
results/validated.json; then run absorb_chain.py on that scratch file and compare every certified bound,
decision and verdict with results/chain.json. Neither script is modified or passed any option that changes
what it computes; nothing in this folder is written (outputs go to --scratch, default a fresh temporary
directory).

Exit status 0 iff every check passes; every mismatch is printed.
Run from this folder:  python3 -B check_artifact.py [--full] [--scratch DIR]
"""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FILES = ('W_nodes.npy', 'Q_nodes.npy')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 24), b''):
            h.update(chunk)
    return h.hexdigest()


def step1():
    ok = True
    manifest = json.loads((HERE / 'results' / 'trajectory_manifest.json').read_text())['files']
    rec_num = json.loads((HERE / 'results' / 'numerics.json').read_text())['trajectory']['sha256_of_array_bytes']
    rec_val = json.loads((HERE / 'results' / 'validated.json').read_text())['provenance']['trajectory_sha256_of_array_bytes']
    print('step 1: trajectory arrays')
    for name in FILES:
        p = HERE / 'trajectory' / name
        if not p.exists():
            print(f'  {name}: MISSING ({p})')
            ok = False
            continue
        a = np.load(p, mmap_mode='r')
        fh = sha_file(p)
        ab = hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
        m = manifest[name]
        checks = {
            'size': p.stat().st_size == m['bytes'],
            'shape': list(a.shape) == m['shape'],
            'dtype': str(a.dtype) == m['dtype'],
            'sha256 file == manifest': fh == m['sha256_file'],
            'sha256 array bytes == manifest': ab == m['sha256_array_bytes'],
            'sha256 array bytes == numerics.json': ab == rec_num[name],
            'sha256 array bytes == validated.json': ab == rec_val[name],
        }
        for k, v in checks.items():
            print(f'  {name}: {k}: {"ok" if v else "MISMATCH"}')
        print(f'  {name}: {p.stat().st_size} bytes, sha256(file) = {fh}')
        ok = ok and all(checks.values())
    return ok


def compare(a, b, path, skip=()):
    """Recursively compare two JSON values; print every difference; return True iff equal outside skip."""
    if path in skip:
        return True
    if isinstance(a, dict) and isinstance(b, dict):
        ok = True
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                print(f'  {path}/{k}: present in only one file')
                ok = False
            else:
                ok = compare(a[k], b[k], f'{path}/{k}', skip) and ok
        return ok
    if a != b:
        sa, sb = json.dumps(a), json.dumps(b)
        print(f'  {path}: {sa[:80]} != {sb[:80]}')
        return False
    return True


def step2(scratch):
    ok = True
    scratch.mkdir(parents=True, exist_ok=True)
    out_v = scratch / 'validated.json'
    print(f'step 2: validate_residual.py end to end -> {out_v}')
    r = subprocess.run([sys.executable, '-B', 'validate_residual.py', '--out', str(out_v)], cwd=HERE,
                       stdout=open(scratch / 'validated.log', 'w'), stderr=subprocess.STDOUT)
    if r.returncode != 0:
        print(f'  validate_residual.py exited with {r.returncode}; see {scratch / "validated.log"}')
        return False
    new, ref = json.loads(out_v.read_text()), json.loads((HERE / 'results' / 'validated.json').read_text())
    same = compare(new, ref, 'validated', skip=('validated/provenance/wall_seconds',))
    print(f'  validated.json: {"identical to results/validated.json apart from wall time" if same else "DIFFERS (see above)"}')
    ok = ok and same
    out_c = scratch / 'chain.json'
    print(f'step 2: absorb_chain.py on the fresh enclosures -> {out_c}')
    r = subprocess.run([sys.executable, '-B', 'absorb_chain.py', '--numerics', str(out_v), '--json', str(out_c)], cwd=HERE,
                       stdout=open(scratch / 'chain.log', 'w'), stderr=subprocess.STDOUT)
    if r.returncode != 0:
        print(f'  absorb_chain.py exited with {r.returncode}; see {scratch / "chain.log"}')
        return False
    newc, refc = json.loads(out_c.read_text()), json.loads((HERE / 'results' / 'chain.json').read_text())
    same = compare(newc, refc, 'chain', skip=('chain/numerics_file',))
    print(f'  chain.json: {"identical to results/chain.json" if same else "DIFFERS (see above)"};  verdict: {newc["verdict"]}')
    return ok and same


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--full', action='store_true')
    ap.add_argument('--scratch', type=Path, default=None)
    args = ap.parse_args()
    ok = step1()
    if args.full:
        scratch = args.scratch or Path(tempfile.mkdtemp(prefix='absorption-b003-check-'))
        ok = step2(scratch) and ok
    print('RESULT:', 'all checks passed' if ok else 'CHECK FAILED')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
