import json, numpy as np
d=json.load(open('out/fullsolve_extrap.json'))
out={}
for m in ['cos0','cos1','cos2']:
    A=np.array(d[f'central_b0.0125_{m}']); B=np.array(d[f'central_b0.025_{m}']); V=np.array(d[f'variational_T0.5_{m}'])
    R=(4*A-B)/3
    out[m]={'richardson_4/3':R.tolist(),'variational_dt.01':V.tolist(),'diff':(R-V).tolist(),'rel_diff':((R-V)/V).tolist(),
            'b2_error_ratio (B-V)/(A-V)':((B-V)/(A-V)).tolist()}
ref=np.array(d['refined_json_runs[-1]_cos2']); R2=np.array(out['cos2']['richardson_4/3'])
out['cos2_richardson_minus_refined_json_dt.005']=(R2-ref).tolist(); out['cos2_rel']=((R2-ref)/ref).tolist()
print(json.dumps(out,indent=1)); json.dump(out,open('out/richardson_fix.json','w'),indent=1)
