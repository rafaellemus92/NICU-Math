"""Small directed-interval postprocessor; no solver, trajectory loads or network."""
import hashlib
import json
from pathlib import Path
import sys
import time
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from mpmath import iv

HERE = Path(__file__).resolve().parent
iv.dps = 70
X = iv.mpf

# Hash-checked historical dependency; no field enters this arithmetic.
PROVENANCE_ONLY = {"route-b-tightening/results/time_refinement.final.json"}


def inclusive_tail_weights(rates, dt, exp=iv.exp):
    """Inclusive source-cell factors exp(sum_{k>=i} rate_k*dt).

    Nonnegative cell growth bounds cover every source time in its cell.
    Generic arithmetic permits exact toy tests of this production function.
    """
    if not rates or dt <= 0 or any(rate < 0 for rate in rates):
        raise ValueError('nonempty nonnegative rates and positive duration required')
    tail = rates[0]*0
    weights = [None]*len(rates)
    for i in range(len(rates)-1, -1, -1):
        tail += rates[i]*dt
        weights[i] = exp(tail)
    return weights


def majorant(values):
    out = list(values)
    for i in range(len(out)-2, -1, -1):
        out[i] = max(out[i], out[i+1])
    return out


def abel(phi, cumulative):
    if len(phi) != len(cumulative) or not phi:
        raise ValueError('nonempty equal length sequences required')
    if any(phi[i] < phi[i+1] for i in range(len(phi)-1)):
        raise ValueError('weights must be nonincreasing')
    return phi[-1]*cumulative[-1] + sum(
        ((phi[i]-phi[i+1])*cumulative[i] for i in range(len(phi)-1)), phi[0]*0)


def decimal_end(value, upper):
    """Convert an exact binary interval endpoint to a directed decimal string."""
    sign, man, exponent, _ = value._mpi_[1 if upper else 0]
    numerator = (-1 if sign else 1)*man
    denominator = 1
    if exponent >= 0:
        numerator <<= exponent
    else:
        denominator <<= -exponent
    with localcontext() as ctx:
        ctx.prec = 50
        ctx.rounding = ROUND_CEILING if upper else ROUND_FLOOR
        return str(Decimal(numerator)/Decimal(denominator))


def bounds(value):
    return {'lo': decimal_end(value, False), 'hi': decimal_end(value, True)}


def stored(text, upper=True):
    # Parent prints point intervals. Pad beyond its ~60-digit serialization.
    lo, hi = text.strip('[]').split(',')
    assert lo.strip() == hi.strip()
    return X(hi.strip()) + (X('1e-50') if upper else -X('1e-50'))


def compute():
    ft = HERE.parent
    pins = json.loads((HERE/'INPUTS.json').read_text())
    data = {}
    for name, expected in pins.items():
        raw = (ft/name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('pinned input mismatch: '+name)
        if name not in PROVENANCE_ONLY:
            data[name] = json.loads(raw)
    parent = data['endpoint-sign/results/tr_remainder.repaired.json']
    chain = data['absorption-b003/results/chain.json']
    val = data['absorption-b003/results/validated.json']
    rows = data['endpoint-sign/results/chain_percell.json']['log']
    rb = data['route-b-dissipation/results/bounds.review.json']['bounds']
    ep = data['z2-endpoint/results/endpoint.json']
    assert chain['b']=='0.003' and chain['T']==.25 and chain['phi']==.37
    assert all(chain[k] for k in ('condition_A','condition_B1','condition_B2'))
    assert ep['scope']=='a=c=d=1, nu=1/28, phi=37/100, T=1/4, beta=3/1000'
    assert parent['best_lambda']=='1000000' and len(rows)==250
    assert [X(r[0]) for r in rows]==[X(i+1)/1000 for i in range(250)]
    nu=X(1)/28; dt=X(1)/1000; beta=X(3)/1000; T=X(1)/4
    C=X(chain['C_A']); S=X(chain['S1']); G=X(ep['bounds']['base_true_laplacian_upper']['hi'])
    assert G.b<=X('1.8534').a
    m1,m2,e1,delta,sigma,N,K = ([X(r[c]) for r in rows] for c in (1,2,5,6,8,9,10))
    n1=[X(float(v)) for v in val['cells']['sup_absgradq']]
    n2=[X(float(v)) for v in val['cells']['sup_abshessq']]
    bg={k:X(v['hi']) for k,v in rb.items()}
    ag=2*bg['M1']+2*beta*bg['n1']; q=2*beta**2*C**2/nu
    cg=(bg['M2']+beta*bg['n2'])*bg['Nw']
    f0=cg*bg['K']+4*bg['sigma']**2/nu
    fd=4*C**2*bg['eps1']**2/nu
    def gcap(t):
        z=iv.exp(2*ag*t)
        return iv.exp(2*q*bg['delta_e'])*(f0/ag*(z-1)+2*fd*bg['delta_e']*z)
    dw=[]; acc=X(0)
    for i in range(250):
        Y=min((K[i]**2).b,gcap(dt*(i+1)).b)
        a=2*m1[i]+2*beta*n1[i]; c=(m2[i]+beta*n2[i])*N[i]
        acc += (a*Y+c*iv.sqrt(Y)+4/nu*sigma[i]**2)*dt
        dw.append(8/nu*(acc+(q*K[i]**2+4/nu*C**2*e1[i]**2)*delta[i]))
    row=parent['per_lambda']['1000000']; ah=stored(row['Ahat'])
    cumulative=[]; acc=X(0)
    for i in range(250):
        acc += N[i]**2*dt
        cumulative.append(ah*(1000000*acc+dw[i]))
    # Recomputed formulas must reproduce the audited endpoints (not new certificates).
    for new, old in ((dw[-1],parent['Dw_TR_T']),(cumulative[-1],row['Iinf_T'])):
        ratio=abs(new/stored(old)-1)
        assert ratio.b<X('1e-45').a, 'parent cumulative reproduction failed'
    propagation = inclusive_tail_weights([2*m for m in m1], dt)
    weights = [(propagation[i]*N[i]**2).b for i in range(250)]
    phi=majorant(weights)
    weighted=abel(phi,cumulative)
    ddiv=iv.sqrt(weighted/(2*nu))
    parts=row['parts']
    nonself=sum((stored(parts[k]) for k in ('smooth','err_adv','err_grad')),X(0))
    self_upper=min(stored(parts['self_d1']).b,stored(parts['self_d2']).b,ddiv.b)
    cnew=G*(nonself+self_upper)+S*stored(row['Er_T'])
    cold=stored(parent['C_one_TR']); jlo=stored(parent['J2_lo'],False)
    margin=jlo-beta**2*cnew.b
    # Alternative route's sufficient signed M threshold, with conservative upper RHS.
    E=X(ep['bounds']['half_q1_gradient_squared']['lo'])
    free=iv.exp(-2*nu*T)/4
    mthreshold=beta**2*cold-(E-free)
    return dict(status='candidate conditional bound; focused independent review pending',
        scope=ep['scope'], inherited_J2_lower=bounds(jlo), old_C_upper=bounds(cold),
        nonself_sum=bounds(nonself), self_divergence_bound=bounds(ddiv),
        old_self_bound=bounds(stored(parts['self_d1'])),
        new_C_upper=bounds(cnew), beta2_C_upper=bounds(beta**2*cnew.b),
        H_over_b2_lower_at_beta=bounds(margin),
        target_comparison_passes=bool(margin.a>0), improves=bool(cnew.b<cold.a),
        current_J2_requires_C_below=bounds(jlo/beta**2),
        alternative_requires_M_greater_than=bounds(mthreshold),
        Dw_T=bounds(dw[-1]), Iinf_T=bounds(cumulative[-1]),
        weighted_Iinf_bound=bounds(weighted), inputs_sha256=pins,
        input_roles={name: ("provenance-only; hash checked, not parsed or used in arithmetic"
                            if name in PROVENANCE_ONLY else "arithmetic input") for name in pins},
        new_source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                           for name in ('check.py','PLAN.md','INPUTS.json')})


if __name__=='__main__':
    out=Path(sys.argv[1])
    if out.exists(): raise SystemExit('refusing to overwrite '+str(out))
    start=time.monotonic(); result=compute(); result['wall_seconds']=time.monotonic()-start
    with out.open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps(result,indent=2))
