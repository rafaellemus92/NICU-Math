"""Independent exact accumulation and raw-array provenance checks; no source rerun."""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,json,time
from fractions import Fraction as F
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
import source_hull as h

def main():
    start=time.monotonic();ap=argparse.ArgumentParser();ap.add_argument('--trajectory',type=Path,required=True);args=ap.parse_args()
    r=json.loads((h.HERE/'results/full.json').read_text())
    assert r['completed_requested_cells'] and r['mode']=='full' and len(r['rows'])==250
    assert r['source_sha256']==h.sha(h.HERE/'source_hull.py') and r['plan_sha256']==h.sha(h.HERE/'PLAN.md')
    for name,digest in r['inputs_sha256'].items():assert h.sha(h.P/name)==digest
    assert h.sha(h.P/'route-b-tightening/results/time_refinement.final.json')==r['remainder_input_sha256']==h.PIN_REMAINDER
    array=np.load(args.trajectory/'Q_nodes.npy',mmap_mode='r',allow_pickle=False)
    assert array.flags.c_contiguous
    digest=hashlib.sha256(memoryview(array).cast('B')).hexdigest()
    val=json.loads((h.P/'absorption-b003/results/validated.json').read_text())
    manifest=json.loads((h.P/'absorption-b003/results/trajectory_manifest.json').read_text())
    chain=json.loads((h.P/'absorption-b003/results/chain.json').read_text())
    assert digest==val['provenance']['trajectory_sha256_of_array_bytes']['Q_nodes.npy']==manifest['files']['Q_nodes.npy']['sha256_array_bytes']==chain['trajectory_sha256']['Q_nodes.npy']
    total=F(0)
    for ell,row in enumerate(r['rows']):
        assert (row['coarse_cell'],row['first_node'],row['last_node'])==(ell,50*ell,50*ell+50)
        assert np.isfinite(row['source_norm_upper_binary64']) and row['source_norm_upper_binary64']>=0
        assert Decimal(row['source_norm_upper_binary64'])==Decimal(row['source_norm_upper_exact'])
        total+=F(row['source_norm_upper_exact'])/1000
    s=r['bounds']['source_majorant'];assert F(s['lo'])<=total<=F(s['hi'])
    b=r['bounds'];LF=F(b['LF_majorant']['hi']);assert LF<=F('.05')
    assert F(b['Z2']['lo'])>F(b['threshold']['hi'])
    with localcontext(h.k.TRAP):
        I=h.I;beta=I.of('3/1000');lo=I.of(b['Z2']['lo']);rem=I.of(b['remainder_upper']['hi'])
        gap=lo-I.of(b['threshold']['hi']);signal=beta.sq()*lo;ratio=rem/signal
    out={'raw_Q_sha256':digest,'matches_manifest_validator_chain':True,'source_inputs_and_plan_hashes_match':True,
      'all_12500_fine_cells_covered':True,'exact_fraction_sum_within_recorded_interval':True,
      'source_sum_exact_fraction':str(total),'Z2_lower_minus_threshold':h.pack(gap),'b_squared_Z2_lower':h.pack(signal),
      'remainder_upper_divided_by_quadratic_lower':h.pack(ratio),'source_sha256':h.sha(Path(__file__)),
      'full_result_sha256':h.sha(h.HERE/'results/full.json'),'wall_seconds':time.monotonic()-start}
    with (h.HERE/'results/verification.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
