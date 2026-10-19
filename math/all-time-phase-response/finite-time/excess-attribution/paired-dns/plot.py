"""Plot preserved scalar CSVs only; no evolution or overwritten artifacts."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
fig,axs=plt.subplots(3,1,figsize=(8,9),sharex=True)
terms=[('S_over_b2',r'$S_b/b^2$','Accumulated stretching excess'),
       ('nuR_over_b2',r'$\nu R_b/b^2$','Accumulated dissipation excess (subtracted)'),
       ('H_over_b2',r'$H_b/b^2$','Interaction excess: H = S − νR')]
for name,color,label in [('n24_coarse','#8294aa','N=24, dt=.0025'),('n24_fine','#e39931','N=24, dt=.00125'),('n32_coarse','#235d99','N=32, dt=.0025')]:
    with (HERE/'results'/(name+'.csv')).open() as f:rows=list(csv.DictReader(f))
    for sign,style in [(1,'-'),(-1,'--')]:
        selected=[r for r in rows if float(r['b'])*sign>0]
        for ax,(term,ylabel,title) in zip(axs,terms):
            ax.plot([float(r['t']) for r in selected],[float(r[term]) for r in selected],style,color=color,
                    linewidth=1.5,label=label+(', b=+.003' if sign>0 else ', b=−.003'))
            ax.set_ylabel(ylabel);ax.set_title(title,loc='left',fontsize=11);ax.grid(alpha=.25)
axs[0].legend(fontsize=7,ncol=2);axs[-1].set_xlabel('time (nondimensional)')
fig.suptitle('Paired DNS attribution — numerical evidence',fontsize=14)
fig.text(.5,.018,'Not a continuum certificate. a=c=d=1, ν=1/28, φ=.37; ±b curves overlap.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.96])
for ext in ['png','svg']:
    target=HERE/'figures'/('attribution_timeseries.clean.'+ext)
    if target.exists():raise FileExistsError(target)
    fig.savefig(target,dpi=160)
plt.close(fig)
