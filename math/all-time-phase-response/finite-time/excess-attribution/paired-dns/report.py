"""Reproduce acceptance and figures from frozen scalar outputs; no evolution."""
import csv,json,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;R=HERE/'results';started=time.monotonic()
names=['n24_coarse','n24_fine','n32_coarse'];runs={n:json.loads((R/(n+'.json')).read_text()) for n in names}
terms=['S_over_b2','nuR_over_b2'];checks=[];table=[]
for sign in range(2):
    for term in terms:
        temporal=abs(runs['n24_coarse']['endpoints'][sign][term]-runs['n24_fine']['endpoints'][sign][term])
        spatial=abs(runs['n24_coarse']['endpoints'][sign][term]-runs['n32_coarse']['endpoints'][sign][term])
        checks.append(dict(b=runs['n32_coarse']['endpoints'][sign]['b'],term=term,time_change=temporal,space_change=spatial,passes=max(temporal,spatial)<=1e-4))
    for name in names:table.append(dict(configuration=name,**runs[name]['endpoints'][sign]))
maxima={k:max(r['stats'][k] for r in runs.values()) for k in runs[names[0]]['stats']}
refinement=max(max(c['time_change'],c['space_change']) for c in checks)
error_scale=max(refinement,maxima['max_balance_scaled'],maxima['max_direct_expanded_scaled_error'],maxima['max_trapezoid_scaled_difference'])
signs=[]
for row in runs['n32_coarse']['endpoints']:
    for term in terms:signs.append(dict(b=row['b'],term=term,value=row[term],error_scale=error_scale,separated=abs(row[term])>10*error_scale,sign='positive' if row[term]>0 else 'negative' if row[term]<0 else 'zero'))
accepted=all(c['passes'] for c in checks) and all(s['separated'] for s in signs) and maxima['max_balance_scaled']<=1e-5
summary=dict(status='accepted numerical evidence; not a continuum certificate' if accepted else 'unresolved; stop',
 accepted=accepted,refinement=checks,diagnostic_maxima=maxima,conservative_empirical_error_scale=error_scale,
 empirical_signs=signs,endpoint_table=table,process_wall_seconds=sum(json.loads(p.read_text())['wall_seconds'] for p in R.glob('*.process.json')),
 peak_rss_MiB=max(json.loads((R/(n+'.json')).read_text())['peak_rss_MiB'] for n in ['pilot']+names),
 quadrature_note='every-step trapezoid versus RK4 stage difference included in sign error scale; not a rigorous quadrature error enclosure')
with (R/'convergence.csv').open('x',newline='') as f:w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
with (R/'summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps(summary,indent=2))
if not accepted:raise SystemExit('acceptance failed; no sign figures')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
figdir=HERE/'figures';figdir.mkdir(exist_ok=True)
fig,axs=plt.subplots(3,1,figsize=(8,9),sharex=True)
labels=[('S_over_b2',r'$S_b/b^2$ — accumulated stretching excess'),('nuR_over_b2',r'$\nu R_b/b^2$ — accumulated dissipation excess'),('H_over_b2',r'$H_b/b^2=S_b/b^2-\nu R_b/b^2$')]
for name,color in zip(names,['#8294aa','#e39931','#235d99']):
    with (R/(name+'.csv')).open() as f:rows=list(csv.DictReader(f))
    for sign,style in [(1,'-'),(-1,'--')]:
        selected=[r for r in rows if float(r['b'])*sign>0]
        label=f"N={runs[name]['N']}, dt={runs[name]['dt']}, b={'+' if sign>0 else '-'}0.003"
        for ax,(term,title) in zip(axs,labels):
            ax.plot([float(r['t']) for r in selected],[float(r[term]) for r in selected],style,color=color,label=label,linewidth=1.4)
            ax.set_ylabel(title);ax.grid(alpha=.25)
axs[0].legend(fontsize=7,ncol=2);axs[-1].set_xlabel('time (nondimensional)')
fig.suptitle('Paired DNS attribution — numerical evidence, not a continuum certificate')
fig.text(.5,.012,'a=c=d=1, ν=1/28, φ=0.37. Positive νR is subtracted from S; ±b curves overlap.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.035,1,.96])
for ext in ['png','svg']:
    target=figdir/('attribution_timeseries.'+ext)
    if target.exists():raise FileExistsError(target)
    fig.savefig(target,dpi=160)
plt.close(fig)
summary_bytes=sum(p.stat().st_size for p in R.iterdir() if p.is_file())
assert summary_bytes<1024**2,'scalar output limit'
with (R/'report_timing.json').open('x') as f:json.dump({'seconds':time.monotonic()-started,'scalar_bytes_before_this_record':summary_bytes},f,indent=2)
