#!/usr/bin/env python3
"""Fact-check computations: glucose quark/mass ladder, respiration loop,
in-body weak decays, solar neutrinos. Every input is labelled with its source."""
import math

# ---------- constants (sources in comments) ----------
NA   = 6.02214076e23          # exact SI
c    = 299792458.0            # exact SI
eV   = 1.602176634e-19        # exact SI
MeV  = 1e6*eV
yr   = 365.25*86400           # Julian year, s
uMeV = 931.49410372           # CODATA 2022 (physics.nist.gov Value?muc2mev)
mp   = 938.27208943           # CODATA 2022 proton, MeV
mn   = 939.56542194           # CODATA 2022 neutron, MeV
me   = 0.51099895069          # CODATA 2022 electron, MeV
mu_q = 2.16                   # PDG 2024/2025 m_u, MS-bar 2 GeV, +-0.07
md_q = 4.70                   # PDG 2024/2025 m_d, MS-bar 2 GeV, +-0.07
# NIST atomic weights & isotopic compositions (AME2020 masses), in u, neutral atoms
mH1, mC12, mO16 = 1.00782503223, 12.0, 15.99491461957

print("="*70); print("(1) GLUCOSE C6H12O6 from 12C, 1H, 16O")
nC, nH, nO = 6, 12, 6
Z = nC*6 + nH*1 + nO*8
N = nC*6 + nH*0 + nO*8
e = Z
up   = 2*Z + 1*N
down = 1*Z + 2*N
print(f"protons {Z}, neutrons {N}, electrons {e}, nucleons {Z+N}")
print(f"valence up = 2*{Z}+{N} = {up}; valence down = {Z}+2*{N} = {down}; total {up+down} = 3*{Z+N}")

M_u = nC*mC12 + nH*mH1 + nO*mO16          # monoisotopic molecular mass (atomic masses, ignores ~eV chemical bonds)
M_MeV = M_u*uMeV
print(f"molecule mass = 6*12 + 12*{mH1} + 6*{mO16} = {M_u:.8f} u = {M_MeV:.3f} MeV = {M_MeV/1e3:.4f} GeV")

q_mass = up*mu_q + down*md_q
q_lo = up*(mu_q-0.07) + down*(md_q-0.07); q_hi = up*(mu_q+0.07) + down*(md_q+0.07)
e_mass = e*me
nuc_mass = Z*mp + N*mn
free_sum = nuc_mass + e_mass
defect = free_sum - M_MeV
print(f"valence quark rest mass = {up}*{mu_q} + {down}*{md_q} = {q_mass:.2f} MeV  -> {q_mass/M_MeV*100:.3f}% (range {q_lo/M_MeV*100:.3f}-{q_hi/M_MeV*100:.3f}%)")
print(f"electron mass = {e}*{me} = {e_mass:.3f} MeV -> {e_mass/M_MeV*100:.4f}%")
print(f"free nucleons = {Z}*{mp} + {N}*{mn} = {nuc_mass:.3f} MeV -> {nuc_mass/M_MeV*100:.3f}%")
print(f"nucleons minus valence quark masses (QCD dynamics) = {nuc_mass-q_mass:.2f} MeV -> {(nuc_mass-q_mass)/M_MeV*100:.3f}%")
print(f"free p+n+e sum = {free_sum:.3f} MeV; minus molecule = binding (nuclear+atomic) {defect:.3f} MeV -> {defect/M_MeV*100:.4f}%")

# nuclear binding of 12C and 16O from atomic masses (H-1 atoms carry the electrons)
mn_u = mn/uMeV
B_C12 = (6*mH1 + 6*mn_u - mC12)*uMeV
B_O16 = (8*mH1 + 8*mn_u - mO16)*uMeV
print(f"m_n = {mn_u:.10f} u; B(12C) = {B_C12:.3f} MeV ({B_C12/12:.4f}/nucleon); B(16O) = {B_O16:.3f} MeV ({B_O16/16:.4f}/nucleon)")
B_nuc = 6*B_C12 + 6*B_O16
print(f"nuclear binding in molecule = 6*B(12C)+6*B(16O) = {B_nuc:.3f} MeV -> {B_nuc/M_MeV*100:.4f}% of molecule mass; remainder (atomic e- binding etc.) {defect-B_nuc:.4f} MeV")

# per-nucleon valence fraction
fp = (2*mu_q+md_q)/mp; fn = (mu_q+2*md_q)/mn
print(f"proton valence quark fraction = {2*mu_q+md_q:.2f}/{mp:.3f} = {fp*100:.3f}%; neutron {mu_q+2*md_q:.2f}/{mn:.3f} = {fn*100:.3f}%")

# chemical energy
for label, E_kJ in [("dcH solid, NIST -2805.0", 2805.0), ("dG'0 -2870 (Tran & Unden 1998 via BioNumbers)", 2870.0)]:
    E_mol = E_kJ*1e3
    m_mol = M_u*1e-3   # kg per mole of monoisotopic glucose
    frac = E_mol/(m_mol*c**2)
    e_molec = E_mol/NA/eV
    print(f"{label}: per molecule {e_molec:.2f} eV; E/(m c^2) = {E_mol:.4g} / ({m_mol:.6f}*c^2={m_mol*c**2:.4e}) = {frac:.3e}")
# with average molar mass 180.156 (NIST WebBook)
print(f"  using 180.156 g/mol: 2.805e6/(0.180156*c^2) = {2.805e6/(0.180156*c**2):.3e}")
# body-scale: mass lost per day to metabolism at 2000 kcal/day
E_day = 2000*4184.0
print(f"2000 kcal/day = {E_day/1e6:.3f} MJ -> dm = E/c^2 = {E_day/c**2:.3e} kg = {E_day/c**2*1e12:.1f} ng/day")

print("="*70); print("(2) RESPIRATORY QUOTIENT")
for name, co2, o2 in [("glucose C6H12O6+6O2->6CO2+6H2O",6,6),("palmitate C16H32O2+23O2->16CO2+16H2O",16,23),("albumin C72H112N18O22S+77O2->63CO2+... (OpenAnesthesia)",63,77)]:
    print(f"{name}: RQ = {co2}/{o2} = {co2/o2:.4f}; O2 not returned as CO2 = {(1-co2/o2)*100:.1f}%")
# metabolic water per gram substrate
MW_glc, MW_h2o = 180.156, 18.015
MW_palm = 16*12.011 + 32*1.008 + 2*15.999
print(f"metabolic water: glucose 6*{MW_h2o}/{MW_glc} = {6*MW_h2o/MW_glc:.3f} g/g; palmitate 16*{MW_h2o}/{MW_palm:.2f} = {16*MW_h2o/MW_palm:.3f} g/g")
# respiratory water loss check (Buck 1981 saturation vapor pressure)
def esat_kPa(T): return 0.61121*math.exp((18.678 - T/234.5)*(T/(257.14+T)))
def vap_density(T, RH):  # g/m^3
    return esat_kPa(T)*1e3*RH*18.015/(8.314462618*(T+273.15))
rho_out37 = vap_density(37,1.0); rho_out34 = vap_density(34,1.0); rho_in = vap_density(20,0.5)
VE = 0.5*12*1440/1000  # m^3/day : 500 mL tidal x 12/min (assumption)
print(f"sat vapour density 37C = {rho_out37:.1f} g/m3, 34C = {rho_out34:.1f} g/m3; inspired 20C/50%RH = {rho_in:.1f} g/m3")
print(f"VE = 0.5 L x 12/min x 1440 = {VE:.2f} m3/day -> water loss {VE*(rho_out37-rho_in):.0f} g/day (37C sat) / {VE*(rho_out34-rho_in):.0f} g/day (34C sat)")
print(f"dead space 2 mL/kg x 70 kg = {2*70} mL; 150/500 tidal = {150/500*100:.0f}%")

print("="*70); print("(3) WEAK DECAYS IN A 70 kg BODY (ICRP 23 Reference Man: K 140 g, C 16000 g)")
K_g, C_g = 140.0, 16000.0
ab_K40, T_K40, MK = 0.000117, 1.248e9*yr, 39.0983
lam_K40 = math.log(2)/T_K40
N_K40 = K_g*ab_K40/MK*NA
A_K40 = lam_K40*N_K40
print(f"K-40 atoms = 140*{ab_K40}/{MK}*NA = {N_K40:.4e} ({N_K40/NA*39.964*1e3:.2f} mg); lambda={lam_K40:.4e}/s; A = {A_K40:.0f} Bq; specific {A_K40/K_g:.2f} Bq/gK")
r14, T_C14, MC = 1.176e-12, 5700*yr, 12.011
lam_C14 = math.log(2)/T_C14
sa_C = r14*NA/MC*lam_C14
A_C14 = sa_C*C_g
print(f"C-14 specific activity = 1.176e-12*NA/12.011*ln2/(5700 y) = {sa_C:.4f} Bq/gC; x16000 g = {A_C14:.0f} Bq; with 0.226 Bq/g: {0.226*C_g:.0f} Bq")
for Cg in (12600, 16000):
    print(f"   carbon {Cg} g -> {sa_C*Cg:.0f} Bq")
bm, ec = 0.8928, 0.1072
anti = A_K40*bm + A_C14
nu   = A_K40*ec
print(f"antineutrinos: {A_K40:.0f}*{bm} + {A_C14:.0f} = {anti:.0f}/s = {anti*86400:.3e}/day")
print(f"neutrinos (K-40 EC): {A_K40:.0f}*{ec} = {nu:.0f}/s = {nu*86400:.3e}/day")
print(f"total = {(anti+nu):.0f}/s = {(anti+nu)*86400:.3e}/day ; HPS 5000 Bq K-40 variant total = {(5000+A_C14)*86400:.3e}/day")
print(f"K-40 beta-minus decays/day = {A_K40*bm*86400:.3e}; K-40 1461 keV gammas ~ EC branch {A_K40*ec:.0f}/s")

# C-14 in DNA
bp_hap = 3.055e9   # T2T-CHM13 haploid ~3.055 Gbp
bp_dip = 2*bp_hap
for Cbp in (19.0, 20.0):
    C_atoms = bp_dip*Cbp
    n14 = C_atoms*r14
    dec_yr = n14*lam_C14*yr
    print(f"C per bp {Cbp}: C atoms/diploid nucleus {C_atoms:.3e}; 14C atoms {n14:.3f}; decays/nucleus/yr {dec_yr:.3e}")
Cbp = 19.5
dec_cell_yr = bp_dip*Cbp*r14*lam_C14*yr
for ncell, lab in [(3e12,"nucleated, Sender 2016"),(3.0e13,"all cells incl. RBC, Sender 2016"),(3.72e13,"Bianconi 2013 all cells")]:
    per_day = dec_cell_yr*ncell/365.25
    life = dec_cell_yr*ncell*80
    print(f"{lab}: {ncell:.2e} cells -> {per_day:.3e} DNA 14C decays/day, {per_day/86400:.2f}/s, 80-yr total {life:.2e}")
print(f"per stem cell: {dec_cell_yr:.2e} 14C decays/yr vs ~40 SNVs/yr (Blokzijl 2016) -> ratio {dec_cell_yr/40:.1e}")

print("="*70); print("(4) SOLAR NEUTRINOS")
B16 = {"pp":5.98e10,"pep":1.44e8,"hep":7.98e3,"7Be":4.93e9,"8B":5.46e6,"13N":2.78e8,"15O":2.05e8,"17F":5.29e6}
tot = sum(B16.values())
print(f"B16-GS98 total flux = {tot:.4e} cm^-2 s^-1; pp share {B16['pp']/tot*100:.1f}%")
Lsun = 3.828e26; AU = 1.495978707e11
nu_rate = 2*Lsun/(26.1*MeV)   # ~26.1 MeV to photons per 2 neutrinos (26.73 Q minus ~0.6 avg nu)
print(f"cross-check: 2*L/(26.1 MeV) = {nu_rate:.3e} nu/s; flux at 1 AU = {nu_rate/(4*math.pi*AU**2)/1e4:.3e} cm^-2 s^-1")
for A_m2 in (0.5, 1.0):
    print(f"area {A_m2} m^2: {tot*A_m2*1e4:.2e} /s through body; per day {tot*A_m2*1e4*86400:.2e}")
# electrons in body (ICRP 23 elements)
elem = {"O":(43000,8,15.999),"C":(16000,6,12.011),"H":(7000,1,1.008),"N":(1800,7,14.007),"Ca":(1000,20,40.078),"P":(780,15,30.974),
        "S":(140,16,32.06),"K":(140,19,39.098),"Na":(100,11,22.990),"Cl":(95,17,35.45),"Mg":(19,12,24.305)}
ne = sum(g/A*Zz*NA for g,Zz,A in elem.values()); mass = sum(g for g,_,_ in elem.values())
print(f"electrons in listed elements ({mass/1000:.2f} kg): {ne:.3e}; Z/A = {ne/NA/mass:.4f}; scaled to 70 kg {ne*70000/mass:.3e}")
ne70 = ne*70000/mass
s_e, s_mu = 11.6e-46, 3.3e-46   # Bahcall, Kamionkowski, Sirlin 1995 Table VIII, pp
for lab, s in [("all nu_e", s_e), ("all nu_mu/tau", s_mu)]:
    R = B16["pp"]*s*ne70
    print(f"pp nu-e scattering, {lab}: {B16['pp']:.2e}*{s:.2e}*{ne70:.3e} = {R:.3e}/s = {R*86400:.3f}/day = {R*yr:.1f}/yr = {R*yr*80:.0f}/80yr")
# Borexino scaling
ne_PC_100t = 1e8*66/120.19*NA
print(f"Borexino PC (C9H12) electrons per 100 t = {ne_PC_100t:.4e}")
for lab, rate in [("pp 134 cpd/100t",134),("pp+7Be+pep 134+48.3+2.43",134+48.3+2.43)]:
    per_body = rate*ne70/ne_PC_100t
    print(f"{lab}: x ({ne70:.3e}/{ne_PC_100t:.3e}) = {per_body:.4f}/day in 70 kg; {per_body*365.25:.0f}/yr; {per_body*365.25*80:.0f}/80 yr")
# per-neutrino interaction probability crossing 20 cm of water-like tissue
n_e_cm3 = 1.0*10/18.015*NA   # water 1 g/cm3, 10 e- per molecule
for L in (20, 30):
    print(f"P(interact) per pp nu over {L} cm: {n_e_cm3:.3e}*1.16e-45*{L} = {n_e_cm3*1.16e-45*L:.1e}")
# comparison with KCL worksheet
print(f"KCL worksheet: 1e35 nu/s -> 3.44e11 m^-2 s^-1 vs B16 {tot*1e4:.2e} m^-2 s^-1 (ratio {tot*1e4/3.44e11:.0f}); their lifetime P = 0.086")
R_bx = 134*ne70/ne_PC_100t
print(f"K-40 beta decays per day / solar nu interactions per day = {A_K40*bm*86400:.3e}/{R_bx:.3f} = {A_K40*bm*86400/R_bx:.1e}")
print(f"body's own nu per day x P(~7.7e-21) = {(anti+nu)*86400*n_e_cm3*1.16e-45*20:.1e} self-interactions/day (order of magnitude only)")
