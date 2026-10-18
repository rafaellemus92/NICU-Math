"""Independent check of the archive's b^2 response at T=0.5: (O(u_b)-O(U))/b^2 extrapolated b->0, 12 phases, vs their variational E2,Z2,S2."""
import numpy as np, json, sys; sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent)); from ns3d import NS
nu = 1/28; T = 0.5; M = 12; phis = np.arange(M)*2*np.pi/M
ns = NS(24, nu, 0.01)
base = np.array([ns.run(1, 0.0, 1, 1, p, [T])[T] for p in phis])
resp = {}
for b in (0.025, 0.0125):
    resp[b] = (np.array([ns.run(1, b, 1, 1, p, [T])[T] for p in phis]) - base)/b**2
r1, r2 = resp[0.025], resp[0.0125]
g2 = r2 - (r1 - r2)*(0.0125**2)/(0.025**2 - 0.0125**2)   # Richardson in b^2
print("b->0 extrapolated (O(u_b)-O(U))/b^2 per phase, columns E Z S:")
for v in g2: print("  ", [f"{x:.6e}" for x in v])
h = np.fft.rfft(g2, axis=0)/M
print("cos2 coefficients (E,Z,S):", [f"{x:.5e}" for x in 2*h[2].real])
print("cos1 coefficients (E,Z,S):", [f"{x:.5e}" for x in 2*h[1].real], " mean:", [f"{x:.5e}" for x in h[0].real])
print("max |r(0.025)-r(0.0125)| (b^4 size):", np.abs(r1-r2).max(axis=0))
json.dump({'phases': phis.tolist(), 'g2_E_Z_S': g2.tolist(), 'cos2': (2*h[2].real).tolist()}, open(__import__('pathlib').Path(__file__).resolve().parent / 'check_T05.json', 'w'), indent=1)
