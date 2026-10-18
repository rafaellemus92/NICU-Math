"""Referee check: run the package's variational solver (U,q1,q2) over 8 phases to T=1,
recording phase harmonics of E2,Z2,S2 at checkpoints.  Compare the cos(2 phi) enstrophy
coefficient at T=1 with the lab's independently established -2.4148e-3 and at small T with
the exact leading jet -(6487/1555200) t^6.  N=18, nu=1/28, dt=.005, a=c=d=1.
"""
import sys, json, time
import numpy as np
PKG = str(__import__('pathlib').Path(__file__).resolve().parents[2]/'all-time-phase-response')
sys.path.insert(0, PKG)
from response import Response, harmonics

def main():
    t0 = time.perf_counter()
    N, nu, dt, M = int(sys.argv[1]), 1/28, .005, 8
    checkpoints = [.5, 1.0]
    s = Response(N, nu)
    phases = 2*np.pi*np.arange(M)/M
    states = [s.initial(p) for p in phases]
    t = 0.; rows = []
    for Tc in checkpoints:
        steps = int(round((Tc - t)/dt))
        for _ in range(steps):
            states = [s.step(Y, dt) for Y in states]
        t += steps*dt
        vals = np.array([s.second(Y) for Y in states])
        h = harmonics(vals)
        lead = -6487/1555200*t**6
        rows.append({'T': t, 'Z2_cos2': h['2']['cos'][1], 'E2_cos2': h['2']['cos'][0], 'S2_cos2': h['2']['cos'][2],
                     'Z2_cos0': h['0']['cos'][1], 'Z2_cos1': h['1']['cos'][1], 'Z2_cos3': h['3']['cos'][1],
                     'leading_jet_t6': lead, 'Z2_cos2_over_jet': h['2']['cos'][1]/lead,
                     'E2_all_phases': vals[:, 0].tolist()})
    print(json.dumps({'params': dict(N=N, K=s.g.K, nu=nu, dt=dt, phases=M), 'rows': rows,
                      'wall_seconds': time.perf_counter() - t0}, indent=1))

if __name__ == '__main__':
    main()
