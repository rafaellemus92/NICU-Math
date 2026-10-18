#!/usr/bin/env python3
"""Particle-physics cluster: every number used in the fact-check is computed here.
Inputs are copied from verified sources (CODATA 2022 via NIST; PDG 2026; papers named inline)."""
import numpy as np
from fractions import Fraction as Fr

# ---------- CODATA 2022 (physics.nist.gov/cuu) ----------
hbar_c_MeVfm = 197.3269804          # MeV fm (exact)
hbar_eVs     = 6.582119569e-16      # eV s (exact)
h            = 6.62607015e-34       # J s (exact)
kB           = 1.380649e-23         # J/K (exact)
N_A          = 6.02214076e23        # 1/mol (exact)
eV_kg        = 1.782661921e-36      # kg per eV/c^2 (exact)
m_p_kg       = 1.67262192595e-27
m_e_kg       = 9.1093837139e-31
u_kg         = 1.66053906892e-27
G_F          = 1.1663787e-5         # GeV^-2
alpha_inv    = 137.035999177
Ry_eV        = 13.605693122990      # hydrogen ionisation scale (Rydberg energy)
yr_s         = 365.25*86400

m_p_GeV = m_p_kg/eV_kg/1e9
u_GeV   = u_kg/eV_kg/1e9
print(f"m_p c^2 = {m_p_kg:.11e} kg / {eV_kg:.9e} kg/eV = {m_p_GeV*1e3:.6f} MeV")
print(f"u c^2   = {u_GeV*1e3:.4f} MeV")

# ---------- PDG 2026 summary tables ----------
M_H, dM_H = 125.13, 0.11            # GeV
G_H, G_H_up, G_H_dn = 3.0e-3, 1.5e-3, 0.7e-3   # GeV
M_W, dM_W = 80.3625, 0.0077
M_Z, dM_Z = 91.1879, 0.0020

print("\n=== (1) Higgs, W, Z, weak range, Navier-Stokes scale ===")
print(f"M_H/m_p = {M_H}/{m_p_GeV:.6f} = {M_H/m_p_GeV:.1f} proton masses")
for G, lab in [(G_H, 'central'), (G_H+G_H_up, 'Gamma+1sig'), (G_H-G_H_dn, 'Gamma-1sig')]:
    tau = hbar_eVs/(G*1e9); ctau_fm = hbar_c_MeVfm/(G*1e3)
    print(f"H lifetime ({lab}): hbar/Gamma = {hbar_eVs:.6e} eV s / {G*1e9:.2e} eV = {tau:.3e} s ; c*tau = {ctau_fm:.1f} fm = {ctau_fm*1e-15:.2e} m")
v = (np.sqrt(2)*G_F)**-0.5
print(f"Higgs VEV v = (sqrt2*G_F)^(-1/2) = (1.41421*{G_F:.7e})^(-1/2) = {v:.3f} GeV")
# tree-level relation M_W = g v/2 -> g; just report M_W/v
print(f"M_W/v = {M_W/v:.4f}, M_Z/v = {M_Z/v:.4f}")

rW_fm = hbar_c_MeVfm/(M_W*1e3); rZ_fm = hbar_c_MeVfm/(M_Z*1e3)
print(f"weak range W: hbar c / M_W c^2 = {hbar_c_MeVfm} MeV fm / {M_W*1e3:.1f} MeV = {rW_fm:.4e} fm = {rW_fm*1e-15:.4e} m")
print(f"weak range Z: {hbar_c_MeVfm} / {M_Z*1e3:.1f} = {rZ_fm:.4e} fm = {rZ_fm*1e-15:.4e} m")

rho_w, M_w = 993.330, 18.0153e-3     # NIST WebBook, water at 310.15 K, 0.101325 MPa; kg/mol
n_w = rho_w*N_A/M_w
a_mean = n_w**(-1/3)
r_OO = 2.80e-10                       # Skinner et al. 2013, nearest-neighbour g_OO peak 2.80(1) A
print(f"water number density at 37 C: {rho_w}*{N_A:.6e}/{M_w} = {n_w:.4e} m^-3 ; mean spacing n^(-1/3) = {a_mean*1e10:.3f} A")
print(f"ratio O-O peak / W range = {r_OO:.2e}/{rW_fm*1e-15:.4e} = {r_OO/(rW_fm*1e-15):.3e}")
print(f"ratio mean spacing / W range = {a_mean/(rW_fm*1e-15):.3e}")

# weak vs EM at chemical energies (dimensionless effective couplings)
alpha = 1/alpha_inv
for E_GeV, lab in [(m_p_GeV, 'E=m_p'), (Ry_eV*1e-9, 'E=13.6 eV')]:
    gw = G_F*E_GeV**2
    print(f"G_F*E^2 at {lab}: {G_F:.4e}*{E_GeV:.4e}^2 = {gw:.3e} ; alpha = {alpha:.5e} ; ratio = {gw/alpha:.2e}")

print("\n=== (2) Unification / proton decay ===")
tau_p = 2.4e34; t0 = 13.797e9
print(f"tau/B(p->e+pi0) > {tau_p:.1e} yr ; / age of universe {t0:.3e} yr = {tau_p/t0:.2e}")
N_nuc = 70/u_kg
print(f"nucleons in 70 kg ~ 70/{u_kg:.6e} = {N_nuc:.3e}")
print(f"upper bound on p->e+pi0 decays/yr in 70 kg (even if every nucleon were a proton): {N_nuc:.3e}/{tau_p:.1e} = {N_nuc/tau_p:.2e} per yr")
print(f"gauge bosons = dim SU(3)+dim SU(2)+dim U(1) = 8+3+1 = {8+3+1}")

print("\n=== (3) 3 x 4 ===")
for N, dN in [(2.9840, 0.0082), (2.9963, 0.0074)]:
    print(f"N_nu = {N} +- {dN}: (3 - N)/sigma = {(3-N)/dN:.2f} sigma")
types_per_gen = 4; colours = 3; gens = 3
print(f"flavour types: {types_per_gen}x{gens} = {types_per_gen*gens}")
per_gen_col = 2*colours + 2
print(f"counting colour: (2 quarks x {colours} + 2 leptons) x {gens} = {per_gen_col*gens}; with antiparticles = {2*per_gen_col*gens}")
weyl = 6+3+3+2+1   # (3,2)+(3b,1)+(3b,1)+(1,2)+(1,1)
print(f"Weyl fermions per generation 6+3+3+2+1 = {weyl}; x3 = {3*weyl}; with nu_R = {3*(weyl+1)}")
# SU(2)^2 U(1)_Y anomaly: sum of Y over left-handed doublets, convention Q = T3 + Y/2
Yq, Yl = Fr(1, 3), Fr(-1)
for Nc in [1, 2, 3, 4]:
    print(f"  Nc={Nc}: sum_doublets Y = Nc*{Yq} + {Yl} = {Nc*Yq + Yl} ; sum of Q per generation = Nc*(2/3-1/3) + (0-1) = {Nc*(Fr(2,3)-Fr(1,3)) - 1}")
for n in [1, 2, 3, 4]:
    print(f"  n={n} generations: CKM angles n(n-1)/2 = {n*(n-1)//2}, CP phases (n-1)(n-2)/2 = {(n-1)*(n-2)//2}")
nf_max = max(nf for nf in range(0, 30) if 33 - 2*nf > 0)
print(f"asymptotic freedom 33-2nf>0 -> nf <= {nf_max} -> generations <= {nf_max//2}")

print("\n=== (4) spin-1/2 ===")
sz = np.array([[1, 0], [0, -1]], dtype=complex)
def U(th):  # exp(-i th sz/2), diagonal so exact
    return np.diag(np.exp(-1j*th*np.diag(sz)/2))
def R(th):
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
print("SU(2) U(2pi) =\n", np.round(U(2*np.pi).real, 12), "\nSU(2) U(4pi) =\n", np.round(U(4*np.pi).real, 12))
print("SO(3) R(2pi) =\n", np.round(R(2*np.pi), 12))
a, da = 716.8, 3.8
print(f"Rauch 1978: alpha = {a} +- {da} deg vs 720: (720-{a})/{da} = {(720-a)/da:.2f} sigma")
T = 310.0
for m, lab in [(70.0, '70 kg human'), (m_e_kg, 'free electron')]:
    lam = h/np.sqrt(2*np.pi*m*kB*T)
    print(f"thermal de Broglie wavelength ({lab}, {T} K): h/sqrt(2 pi m k T) = {lam:.3e} m")

print("\n=== (5) dark matter in a 70-L body ===")
V_cm3 = 70*1000
for rho in [0.2, 0.3, 0.4, 0.47, 0.55, 0.6]:
    M_GeV = rho*V_cm3
    M_kg = M_GeV*1e9*eV_kg
    print(f"rho={rho} GeV/cm^3: {rho}*{V_cm3} = {M_GeV:.3e} GeV = {M_kg:.3e} kg = {M_GeV/m_p_GeV:.3e} m_p ; fraction of 70 kg = {M_kg/70:.2e}")
rho0 = 0.4
for mchi in [1.0, 40.0, 100.0]:
    print(f"  if m_chi = {mchi} GeV: N = {rho0}*{V_cm3}/{mchi} = {rho0*V_cm3/mchi:.0f} particles in the body at any instant (rho=0.4)")
vc = 233e3
print(f"time to cross 1 m at v_c = 233 km/s: {1/vc:.2e} s")
# order-of-magnitude upper bound on DM scatters in 70 kg, crude model: all mass as O-16, LZ SI limit at 40 GeV,
# coherent A^2 scaling, no form factor, no threshold, all particles at 233 km/s
sig_n = 2.2e-48; mchi = 40.0; A = 16
mN = A*u_GeV
muN = mchi*mN/(mchi+mN); mun = mchi*m_p_GeV/(mchi+m_p_GeV)
sigN = sig_n*A**2*(muN/mun)**2
NT = 70/(A*u_kg)
n_chi = rho0/mchi
rate = NT*n_chi*sigN*(vc*100)
print(f"  mu_N={muN:.3f} GeV, mu_n={mun:.4f} GeV, sigma_N = {sig_n:.1e}*{A}^2*({muN:.3f}/{mun:.4f})^2 = {sigN:.3e} cm^2")
print(f"  N_T = {NT:.3e} O-16 nuclei, n_chi = {n_chi} cm^-3, v = {vc*100:.2e} cm/s")
print(f"  rate < {rate:.2e} /s = {rate*yr_s:.2e} /yr -> < 1 scatter per {1/(rate*yr_s):.0f} yr")

print("\n=== (1b) how much of a proton's mass is Higgs-generated quark mass ===")
m_u, m_d = 2.16, 4.70   # MeV, PDG 2026 MS-bar at 2 GeV
s = 2*m_u + m_d
print(f"uud: 2*{m_u} + {m_d} = {s:.2f} MeV ; / m_p {m_p_GeV*1e3:.3f} MeV = {100*s/(m_p_GeV*1e3):.2f} %")
mu_w = 691.304e-6  # Pa s, NIST WebBook water 310.15 K
print(f"NS for water uses only rho = {rho_w} kg/m^3 and mu = {mu_w*1e6:.3f} uPa s ; kinematic nu = {mu_w/rho_w:.3e} m^2/s")
