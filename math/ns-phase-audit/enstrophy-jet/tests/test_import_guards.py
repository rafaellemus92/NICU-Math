"""Import-specific failure controls and stored overlap, not high-order regeneration."""
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
from test_jet import ROOT, SERIES, trim
from fractions import Fraction
import float_check as fc

ROOT = Path(ROOT)


def test_stored_overlap_through_12():
    old = json.loads((ROOT.parent / 'audit_v2/exact/z12_unit.json').read_text())
    assert old['amps'] == ['1'] * 4
    for old_key, new_key in [('Z', 'orders'), ('E', 'energy_orders')]:
        for n in range(13):
            a, b = old[old_key][str(n)], SERIES[new_key][str(n)]
            for m in set(a) | set(b):
                assert trim(map(Fraction, a.get(m, []))) == trim(map(Fraction, b.get(m, []))), (old_key, n, m)


@pytest.mark.parametrize('script,args', [
    ('exact_single_nu.py', ['1/28', '0']),
    ('float_check.py', ['--nmax', '0', '--grid', '8', '--phases', '8', '--nu', '1/28']),
])
def test_cli_rejects_corrupted_reference(tmp_path, script, args):
    ref = json.loads(json.dumps(SERIES))
    path = tmp_path / 'series.json'
    path.write_text(json.dumps(ref))
    command = [sys.executable, str(ROOT / script), *args, '--series', str(path)]
    good = subprocess.run(command, capture_output=True, text=True)
    assert good.returncode == 0, good.stdout + good.stderr
    ref['orders']['0']['0'] = ['1250001/1000000']  # 1e-6 perturbation
    path.write_text(json.dumps(ref))
    bad = subprocess.run(command, capture_output=True, text=True)
    assert bad.returncode == 1, bad.stdout + bad.stderr
    diagnostic = '1 mismatches' if script == 'exact_single_nu.py' else 'tolerance 1.0e-10: FAIL'
    assert diagnostic in bad.stdout, bad.stdout + bad.stderr
    assert 'Traceback' not in bad.stderr


def test_float_nonfinite_and_tolerance_boundary():
    ex = np.array([1.0, 0.0])
    assert fc.scaled_error(ex + [0, fc.TOLERANCE / 2], ex) < fc.TOLERANCE
    assert fc.scaled_error(ex + [0, 2 * fc.TOLERANCE], ex) > fc.TOLERANCE
    for x in [float('nan'), float('inf')]:
        assert fc.scaled_error(np.array([x, 0]), ex) == float('inf')


@pytest.mark.parametrize('script,args', [
    ('exact_single_nu.py', ['1/28', '1']),
    ('float_check.py', ['--nmax', '1', '--grid', '8', '--phases', '8']),
])
def test_cli_rejects_missing_order(tmp_path, script, args):
    ref = json.loads(json.dumps(SERIES))
    del ref['orders']['1']
    path = tmp_path / 'incomplete.json'
    path.write_text(json.dumps(ref))
    run = subprocess.run([sys.executable, str(ROOT / script), *args, '--series', str(path)], capture_output=True, text=True)
    expected_code = 1 if script == 'exact_single_nu.py' else 2
    diagnostic = 'missing order' if script == 'exact_single_nu.py' else 'series must contain every requested order'
    assert run.returncode == expected_code, run.stdout + run.stderr
    assert diagnostic in run.stdout + run.stderr
    assert 'Traceback' not in run.stderr
