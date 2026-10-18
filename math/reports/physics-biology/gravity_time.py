# Gravitational time dilation near Earth + Wow! signal numbers
# Constants (sources):
#   c   = 299792458 m/s exact (CODATA 2022, physics.nist.gov/cgi-bin/cuu/Value?c)
#   g_n = 9.80665 m/s^2 exact conventional (CODATA 2022, .../Value?gn)
#   g_Chou = 9.80 m/s^2 local value used by Chou et al. 2010 (Boulder)
#   NASA Earth fact sheet: GM = 0.39860e6 km^3/s^2, mean radius 6371.000 km,
#       g_eq = 9.780, g_pole = 9.83 m/s^2
#   NASA Sun fact sheet: GM = 132,712e6 km^3/s^2
#   AU = 149,597,870,700 m (IAU 2012 Res. B2, exact)
import numpy as np
c   = 299_792_458.0
gn  = 9.80665
gC  = 9.80
yr  = 365.25*86400          # Julian year, s
T80 = 80*yr

print("== (2) Gravitational time dilation, weak field: df/f = g*dh/c^2 ==")
print(f"c^2 = {c**2:.6e} m^2/s^2")
print(f"80 Julian years = 80*365.25*86400 = {T80:.6e} s")
for g,lab in [(gn,'g_n 9.80665'),(gC,'g 9.80 (Chou)'),(9.780,'g equator 9.780'),(9.83,'g pole 9.83')]:
    for h in [1.0,1.7]:
        r = g*h/c**2
        print(f"  {lab:16s} h={h:4.2f} m: g*h/c^2 = {g}*{h}/{c**2:.6e} = {r:.4e};"
              f"  over 80 yr: {r*T80:.4e} s = {r*T80*1e9:.1f} ns")
r1 = gn*1.0/c**2; r17 = gn*1.7/c**2
print(f"per day, 1.7 m: {r17*86400*1e12:.2f} ps/day")
print(f"time for head-feet (1.7 m) offset to reach 1 us: {1e-6/r17:.3e} s = {1e-6/r17/yr:.0f} yr")
print(f"time for head-feet offset to reach 1 s: {1/r17:.3e} s = {1/r17/yr:.3e} yr")

print("\n== Chou et al. 2010 check (33 cm) ==")
p33 = gC*0.33/c**2
print(f"predicted 9.80*0.33/c^2 = {p33:.3e}  vs measured (4.1 +/- 1.6)e-17 ->"
      f" diff = {(4.1e-17-p33)/1.6e-17:.2f} sigma")
print(f"inferred height from measured: 4.1e-17*c^2/9.80 = {4.1e-17*c**2/gC*100:.1f} cm (paper: 37 +/- 15 cm)")
print(f"per metre: 9.80/c^2 = {gC/c**2:.3e} (paper: ~1.1e-16 per m)")
for yrs in [79,80]:
    print(f"33 cm over {yrs} yr: {p33*yrs*yr*1e9:.1f} ns (NIST release: ~90 ns over 79 yr)")

print("\n== Bothwell et al. 2022 check (per mm) ==")
pmm = gC*1e-3/c**2
print(f"predicted g*1mm/c^2 (g=9.80) = {pmm:.3e} per mm (paper: 1.09e-19/mm)")
meas, sig = 9.8e-20, 2.3e-20
print(f"measured 9.8(2.3)e-20/mm: ratio meas/pred = {meas/pmm:.2f} +/- {sig/pmm:.2f};"
      f" deviation = {(pmm-meas)/sig:.2f} sigma")
print(f"implied g from measured gradient: {meas*c**2/1e-3:.2f} +/- {sig*c**2/1e-3:.2f} m/s^2")

print("\n== Context: whole potential wells (weak field, phi/c^2) ==")
GME = 0.39860e6*1e9; RE = 6371.000e3
GMS = 132712e6*1e9;  AU = 149_597_870_700.0
e = GME/(RE*c**2); s = GMS/(AU*c**2)
print(f"Earth surface vs infinity: GM/(R c^2) = {GME:.4e}/({RE:.4e}*{c**2:.4e}) = {e:.4e};"
      f" over 80 yr = {e*T80:.2f} s")
print(f"Sun's potential at 1 AU: GM/(AU c^2) = {s:.4e}; over 80 yr = {s*T80:.1f} s")
print(f"Ratio head-feet (1.7 m) to Earth-surface well: {r17/e:.2e}")

print("\n== Velocity time dilation for comparison: v^2/(2c^2) ==")
for v in [1.0,10.0]:
    print(f"  v={v:4.1f} m/s: {v**2/(2*c**2):.3e}")

print("\n== (3) Wow! signal numbers ==")
f_HI = 1420.405751768e6   # Hz, H hyperfine (to be sourced)
h = 6.62607015e-34; eV = 1.602176634e-19
print(f"HI 21-cm: lambda = c/f = {c/f_HI*100:.3f} cm; E = h f = {h*f_HI/eV*1e6:.3f} micro-eV")
for lab,f in [('Kraus 1994',1420.3556e6),('Ehman 1998',1420.4556e6),('Mendez 2025',1420.726e6)]:
    df = f-f_HI
    v = -c*df/f_HI  # radio-convention radial velocity, + = receding
    print(f"  {lab}: f-f_HI = {df/1e3:+.1f} kHz -> radio-convention v_r = {v/1e3:+.1f} km/s")
snr = {'6':6,'E':14,'Q':26,'U':30,'J':19,'5':5}
print("6EQUJ5 code (A=10..Z=35):", {k:(v if k.isdigit() else ord(k)-ord('A')+10) for k,v in snr.items()})
print(f"duration: 6 samples x 12 s = {6*12} s (10 s integration + ~2 s processing each)")
print(f"Big Ear channel width 10 kHz -> fractional bandwidth 10e3/{f_HI:.4e} = {10e3/f_HI:.2e}")
