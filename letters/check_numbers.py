"""Recompute the derived numbers quoted in words.md.

Standard library only. Run from this folder:
    python3 check_numbers.py           # print, and compare with check_numbers.txt
    python3 check_numbers.py --write   # rewrite check_numbers.txt
Bracketed numbers in comments refer to the source list in words.md.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "check_numbers.txt"

# Constants
C = 299792458.0               # m/s, exact
G0 = 9.80665                  # m/s^2, standard gravity
NA = 6.02214076e23            # 1/mol, exact
EV = 1.602176634e-19          # J, exact
U_MEV = 931.49410242          # MeV per atomic mass unit
YEAR = 365.25 * 86400         # s
ME_U = 5.48579909e-4          # electron mass in u


def glucose():
    # C6H12O6 built from the main isotopes 12C, 1H, 16O.
    n = {"C": 6, "H": 12, "O": 6}
    z = {"C": 6, "H": 1, "O": 8}
    nn = {"C": 6, "H": 0, "O": 8}
    protons = sum(z[e] * n[e] for e in n)
    neutrons = sum(nn[e] * n[e] for e in n)
    up = 2 * protons + neutrons      # proton = uud, neutron = udd
    down = protons + 2 * neutrons
    # Atomic masses in u, AME2020 [70]
    mass_u = 6 * 12.0 + 12 * 1.007825031898 + 6 * 15.99491461926
    mass_mev = mass_u * U_MEV
    # Light-quark masses, PDG 2025, MS-bar at 2 GeV [28]
    mu, md = 2.16, 4.70
    quark_mev = up * mu + down * md
    electron_frac = protons * ME_U / mass_u
    # Nuclear binding, AME2020 binding energy per nucleon in keV [70]
    binding_mev = 6 * 12 * 7680.1446e-3 + 6 * 16 * 7976.2072e-3
    # Enthalpy of combustion of solid alpha-D-glucose, NIST WebBook [69]
    dch_kj = 2805.0
    combustion_ev = dch_kj * 1e3 / NA / EV
    return [
        ("glucose protons", protons),
        ("glucose neutrons", neutrons),
        ("glucose up quarks", up),
        ("glucose down quarks", down),
        ("glucose mass (MeV)", round(mass_mev)),
        ("quark rest mass, sum (MeV)", round(quark_mev)),
        ("quark rest mass share of glucose mass (%)", round(100 * quark_mev / mass_mev, 2)),
        ("electron share of glucose mass (%)", round(100 * electron_frac, 3)),
        ("energy released by burning one molecule (eV)", round(combustion_ev, 1)),
        ("nuclear binding energy of one molecule (MeV)", round(binding_mev, 1)),
        ("nuclear binding / combustion energy", f"{binding_mev * 1e6 / combustion_ev:.2e}"),
    ]


def time_dilation():
    per_m = G0 / C**2                      # fractional rate change per metre of height
    life = 80 * YEAR
    nist = 0.33 * per_m * 79 * YEAR        # NIST: 33 cm over a 79-year life [35]
    return [
        ("gravitational rate shift per metre of height", f"{per_m:.2e}"),
        ("time gained per metre over 80 years (microseconds)", round(per_m * life * 1e6, 2)),
        ("cross-check: 33 cm over 79 years (nanoseconds)", round(nist * 1e9)),
    ]


def potassium_40():
    # 140 g of potassium in a 70 kg adult [40]; 40K abundance 0.0117%; molar mass 39.964 g/mol.
    atoms = 140 * 0.000117 / 39.96399848 * NA
    rows = [("potassium-40 atoms in the body", f"{atoms:.2e}")]
    for t_half in (1.248e9, 1.277e9):      # half-lives in years, from [40] and [41]
        rate = atoms * 0.69314718056 / (t_half * YEAR)
        rows.append((f"K-40 decays per second (half-life {t_half:.4g} y)", int(round(rate, -1))))
    return rows, atoms * 0.69314718056 / (1.248e9 * YEAR)


def neutrinos(k40_per_s):
    # Borexino interaction rates, counts per day per 100 t of scintillator [44]
    rates = {"pp": 134.0, "7Be": 48.3, "pep": 2.43}
    e_per_100t = 3.307e31                  # electrons per 100 t [45]
    body_kg, z_over_a = 70.0, 0.55         # body treated as roughly water-like (water: 10/18)
    body_e = body_kg * 1e3 * z_over_a * NA
    per_day = sum(rates.values()) * body_e / e_per_100t
    per_year = per_day * 365.25
    return [
        ("electrons in a 70 kg body", f"{body_e:.2e}"),
        ("solar-neutrino electron collisions per year (pp+7Be+pep)", round(per_year)),
        ("same over 80 years", int(round(per_year * 80, -2))),
        ("K-40 decays per year / neutrino collisions per year", f"{k40_per_s * YEAR / per_year:.1e}"),
    ]


def chromosomes():
    # Lengths: UCSC hg38.chrom.sizes [57]. Protein-coding genes: NCBI Gene, 18 Oct 2026 [58].
    data = {"13": (114364328, 354), "18": (80373285, 277), "19": (58617616, 1459),
            "21": (46709983, 254), "22": (50818468, 478)}
    rows = []
    for c, (bp, genes) in data.items():
        rows.append((f"chr{c}: length (Mb), genes, genes per Mb",
                     f"{bp / 1e6:.1f}, {genes}, {genes / (bp / 1e6):.1f}"))
    return rows


def main():
    k40_rows, k40_rate = potassium_40()
    sections = [
        ("Glucose, quark by quark", glucose()),
        ("Gravity and time", time_dilation()),
        ("Potassium-40", k40_rows),
        ("Solar neutrinos in a body (rough estimate)", neutrinos(k40_rate)),
        ("Chromosomes", chromosomes()),
    ]
    lines = []
    for title, rows in sections:
        lines.append(f"## {title}")
        lines += [f"{k}: {v}" for k, v in rows]
        lines.append("")
    text = "\n".join(lines)
    print(text)
    if "--write" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT.name}")
    elif OUT.exists():
        same = OUT.read_text(encoding="utf-8") == text
        print("matches stored check_numbers.txt" if same else "DIFFERS from stored check_numbers.txt")
        return 0 if same else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
