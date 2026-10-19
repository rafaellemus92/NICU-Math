"""Validated source-only hull; same inherited projected affine qN, no evolution."""
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,platform,signal,time,resource
from decimal import Decimal,localcontext
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;P=HERE.parent
PINS={
'mean-q2-pilot/kernels.py':'9bc9eea62f5fc2930859f00c514cd80bfcaf138fc543b89a33975a8ccb2d3b86',
'absorption-b003/validate_residual.py':'2d2952363b8d2f4cf6918123a94d47c7b69988ca2ec54c06179830562ecea4bc',
'constants.py':'996f39f171601a73bdbd87c61e82482f7a91508ab19d78584215da1475479014',
'absorption-b003/results/trajectory_manifest.json':'8c39c91f4980ef30458c3300f6df0094709873e355546b7c54a764a0553dd847',
'absorption-b003/results/validated.json':'e404cb94b25a63989540e1cde2d6cc7630d6caa0f934125dbee4890fc7db2a5b',
'absorption-b003/results/chain.json':'0cd069e1fdd83e66a9a65bf24b5be95f477b64d255290b4ced07aa3e7f5fe117',
'route-b-dissipation/results/bounds.review.json':'4ca49f7ffa12fafa45ca83d36d551b34afd02de9671963b275e1f602237f7e65',
'z2-endpoint/results/endpoint.json':'37368b9c6c7781e9cc691deb4742fd56e194c4ee80bed0b6a517e2425d8ab0bc',
}
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for n,h in PINS.items():
    if sha(P/n)!=h:raise ValueError('Pinned input mismatch '+n)
spec=importlib.util.spec_from_file_location('hull_kernels',P/'mean-q2-pilot/kernels.py');k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)
v,I=k.v,k.Iv

def hull(nodes):
    if nodes.ndim!=4 or nodes.shape[1:]!=(3,21,21) or not np.isfinite(nodes).all():raise ValueError('Invalid node block')
    center=v.exact(nodes[len(nodes)//2])
    dif=v.csub(v.exact(nodes),center)
    rad=np.max(v.abs_hi(dif),axis=0) # comparison/selection of already upward values is exact
    return v.CI(center.re,center.im,rad)

def cell(Q,ell):
    start=time.monotonic();first=50*ell;last=first+50
    nodes=Q[first:last+1]
    if len(nodes)!=51:raise ValueError('Incomplete coarse cell')
    raw=hull(nodes)
    projected=v.project_small(raw) # EXACT same map and support as inherited validator
    source=k.mean_source(projected)
    assert source.shape==(3,41,41)
    norm=v.wnorm_hi(source,1,False)
    return {'coarse_cell':ell,'first_node':first,'last_node':last,'seconds':time.monotonic()-start,
            'source_norm_upper_binary64':norm,'source_norm_upper_exact':str(Decimal(norm)),
            'max_raw_hull_radius':float(np.max(raw.rad)),'max_source_disc_radius':float(np.max(source.rad))}

def pack(x):return {'lo':str(x.lo),'hi':str(x.hi)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trajectory',type=Path,required=True);ap.add_argument('--mode',choices=['pilot','full'],required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    def stop(s,f):raise TimeoutError('Execution cap reached')
    signal.signal(signal.SIGALRM,stop);signal.alarm(30 if args.mode=='pilot' else 180)
    start=time.monotonic()
    val=json.loads((P/'absorption-b003/results/validated.json').read_text());chain=json.loads((P/'absorption-b003/results/chain.json').read_text())
    par=val['parameters']
    for key,value in {'nu_exact':'1/28','phi_exact':'37/100','h_exact':'1/50000','NSTEP':12500,'COARSE':50,'KQ':10,'T':.25,'a':1.,'c':1.,'d':1.}.items():assert par[key]==value,(key,par.get(key))
    assert val['provenance']['complete'] and val['provenance']['cells_validated']==12500
    assert chain['verdict']=='CERTIFIED' and chain['b']=='0.003'
    manifest=json.loads((P/'absorption-b003/results/trajectory_manifest.json').read_text());m=manifest['files']['Q_nodes.npy'];file=args.trajectory/'Q_nodes.npy'
    assert file.stat().st_size==m['bytes'] and sha(file)==m['sha256_file']
    Q=np.load(file,mmap_mode='r',allow_pickle=False)
    assert list(Q.shape)==m['shape']==[12501,3,21,21] and str(Q.dtype)==m['dtype']=='complex128'
    assert Q[0,1,10,10]==-1j and np.count_nonzero(Q[0])==1
    assert np.array_equal(v.ks,np.arange(-10,11,dtype=float))
    rows=[];complete=False;failure=None
    try:
        for ell in ((0,125,249) if args.mode=='pilot' else range(250)):
            rows.append(cell(Q,ell))
            if args.mode=='pilot' or (ell+1)%25==0:print('cell',ell,'seconds',rows[-1]['seconds'],'norm upper',rows[-1]['source_norm_upper_exact'],flush=True)
        complete=True
    except TimeoutError as ex:failure=str(ex)
    result={'mode':args.mode,'completed_requested_cells':complete,'failure':failure,'rows':rows,
      'inputs_sha256':PINS,'Q_file_sha256':m['sha256_file'],'source_sha256':sha(Path(__file__)),'plan_sha256':sha(HERE/'PLAN.md'),
      'python':platform.python_version(),'numpy':np.__version__,'base_commit':'f6cdc6d3eeed4c4e947eef0b56f48f1cc0b1eccd',
      'path':'exact P_(kx,ky,1) of exact saved dyadics, affine at j/50000; coarse hull includes all51 fine nodes',
      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if args.mode=='full' and complete:
        assert [r['coarse_cell'] for r in rows]==list(range(250))
        rb=json.loads((P/'route-b-dissipation/results/bounds.review.json').read_text());ep=json.loads((P/'z2-endpoint/results/endpoint.json').read_text())
        # Conservative rounded candidate bound proved in the separately pinned analytic output below.
        cf=P/'route-b-tightening/results/time_refinement.final.json'
        expected=PIN_REMAINDER
        assert sha(cf)==expected
        candidate=json.loads(cf.read_text())['rows']['1000000']
        with localcontext(k.TRAP):
            b={key:I.of(value['hi']) for key,value in rb['bounds'].items()}
            nu=I.of('1/28');T=I.of('1/4');beta=I.of('3/1000')
            assert b['M1'].lo>=nu.hi # required by unweighted global propagator formula
            source=I.of('1/1000')*sum((I.of(r['source_norm_upper_exact']) for r in rows),I.of(0))
            deltaF=T*(b['n1']*b['eps0']+b['p']*b['eps1'])+b['CA']*b['eps1']*(T*b['delta_e']).sqrt()
            LF=source+deltaF;prop=((b['M1']-nu)*T).exp()
            G=I.of(ep['bounds']['base_true_laplacian_upper']['hi'])
            E=I(Decimal(ep['bounds']['half_q1_gradient_squared']['lo']),Decimal(ep['bounds']['half_q1_gradient_squared']['hi']))
            boundM=G*prop*LF
            Z=E+I(boundM.hi.copy_negate(),boundM.hi)
            CB=I.of(candidate['C_endpoint']['hi']);threshold=beta.sq()*CB
            result['bounds']={name:pack(x) for name,x in dict(source_majorant=source,DeltaF=deltaF,LF_majorant=LF,propagator=prop,abs_M_majorant=boundM,Z2=Z,threshold=threshold,remainder_upper=beta.sq().sq()*CB).items()}
            result['LF_physical_enclosure']={'lo':'0','hi':str(LF.hi)}
            result['checkpoint_LF_le_point05']=LF.hi<=Decimal('.05')
            result['positive_Z2_lower_exceeds_threshold']=Z.lo>threshold.hi
            result['remainder_input_sha256']=expected
            result['status']='complete conditional interval result; focused independent review required'
    result['wall_seconds']=time.monotonic()-start
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('wall',result['wall_seconds'],'complete',complete,flush=True)
    if 'bounds' in result:print(json.dumps({key:result[key] for key in ['bounds','checkpoint_LF_le_point05','positive_Z2_lower_exceeds_threshold']},indent=2))
    signal.alarm(0)

PIN_REMAINDER='79612f1164e92243b74ef40dd668651bc850ffa81d82695d7c59f039e119e849'
if __name__=='__main__':main()
