"""Computations for the biology/medicine fact-check cluster.
All inputs are values fetched from primary sources (paths/URLs noted inline).
Run: python3 compute_bio.py  (needs numpy; reads data/grch38_chr.json, data/chm13_chr.json, data/mart_all.tsv)."""
import json, collections, os
import numpy as np

# downloaded inputs live in data/ next to this script
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
hr = lambda s: print("\n" + "=" * 8, s, "=" * 8)

# ---------------------------------------------------------------- (1) zinc spark
hr("1 ZINC SPARK")
NA = 6.02214076e23            # NIST CODATA 2022, exact
Zn = 65.38                    # CIAAW standard atomic weight
atoms = 20e9                  # Kim et al. 2011 ACS Chem Biol: "over twenty billion zinc atoms"
mol = atoms / NA
print(f"20e9 Zn atoms = {atoms:.3g}/{NA:.6g} = {mol:.3e} mol = {mol*1e15:.1f} fmol")
print(f"mass = {mol:.3e} mol x {Zn} g/mol = {mol*Zn:.3e} g = {mol*Zn*1e12:.2f} pg")

# ---------------------------------------------------------------- (2) iodine
hr("2 IODINE / THYROID")
AW = dict(C=12.011, H=1.008, N=14.007, O=15.999, I=126.90447)  # CIAAW (conventional C,H,N,O; I standard)
def mw(f): return sum(AW[e]*n for e, n in f.items())
T4 = dict(C=15, H=11, I=4, N=1, O=4)   # ChEBI:18332 C15H11I4NO4
T3 = dict(C=15, H=12, I=3, N=1, O=4)   # ChEBI:18258 C15H12I3NO4
for name, f, chebi in [("T4", T4, 776.872), ("T3", T3, 650.976)]:
    m = mw(f); fi = f["I"]*AW["I"]/m
    print(f"{name}: MW = {m:.3f} (ChEBI {chebi}); iodine mass = {f['I']}x126.90447 = {f['I']*AW['I']:.3f}; "
          f"iodine mass fraction = {fi*100:.1f}%")
# essential trace elements with established human requirement (IOM/NASEM DRIs) by atomic number
Z = dict(F=9, Cr=24, Mn=25, Fe=26, Cu=29, Zn=30, Se=34, Mo=42, I=53)
print("Z of DRI trace elements:", sorted(Z.items(), key=lambda kv: kv[1]), "-> max:", max(Z, key=Z.get))
# IQ conversions (1 SD = 15 IQ points)
print("Qian 2005: 0.83 SD x 15 =", round(0.83*15, 2), "; 0.58 SD x 15 =", round(0.58*15, 2))
print("Bougma 2013: 0.46 SD x 15 =", round(0.46*15, 2), "; 0.68 SD x 15 =", round(0.68*15, 2))

# ---------------------------------------------------------------- (3) trisomy sizes
hr("3 TRISOMY: DNA SIZE vs GENE DOSAGE")
def load_lengths(fn):
    d = json.load(open(fn)); L = {}
    for r in d["reports"]:
        if r.get("role") == "assembled-molecule" and r.get("assembly_unit") == "Primary Assembly":
            L[r["chr_name"]] = int(r["length"])
    return L
G38 = load_lengths(f"{B}/grch38_chr.json")     # NCBI Datasets, GCF_000001405.40 (GRCh38.p14)
T2T = load_lengths(f"{B}/chm13_chr.json")      # NCBI Datasets, GCF_009914755.1 (T2T-CHM13v2.0)
auto = [str(i) for i in range(1, 23)]
for tag, L in [("GRCh38.p14", G38), ("T2T-CHM13v2.0", T2T)]:
    A = sum(L[c] for c in auto)
    fem = 2*A + 2*L["X"]; male = 2*A + L["X"] + L["Y"]
    print(f"[{tag}] haploid autosomes = {A:,}; 46,XX = 2*{A:,} + 2*{L['X']:,} = {fem:,} bp; "
          f"46,XY = {male:,} bp")
    for c in ["13", "18", "21", "22", "9", "16", "X"]:
        base = fem if c == "X" else fem
        print(f"   chr{c}: {L[c]:,} bp = {L[c]/1e6:.1f} Mb; extra copy / 46,XX genome = "
              f"{L[c]:,}/{fem:,} = {100*L[c]/fem:.2f}%  (vs 46,XY: {100*L[c]/male:.2f}%)")
# protein-coding genes, Ensembl release 116 BioMart (biotype=protein_coding)
pc = collections.Counter(l.split("\t")[1].strip() for l in open(f"{B}/mart_all.tsv") if "\t" in l)
nuc = sum(v for k, v in pc.items() if k != "MT")
print(f"Ensembl 116 protein-coding genes: nuclear total = {nuc:,} (MT {pc['MT']})")
for c in ["13", "18", "21", "22", "9", "16", "X"]:
    print(f"   chr{c}: {pc[c]} genes = {100*pc[c]/nuc:.2f}% of nuclear coding genes; "
          f"density = {pc[c]}/{G38[c]/1e6:.1f} Mb = {pc[c]/(G38[c]/1e6):.2f} genes/Mb")
print(f"chr16 vs chr13: length ratio {G38['16']/G38['13']:.2f}, gene ratio {pc['16']/pc['13']:.2f}")
print(f"chrX vs chr21: length ratio {G38['X']/G38['21']:.2f}, gene ratio {pc['X']/pc['21']:.2f}")
print(f"chrX vs chr13: length ratio {G38['X']/G38['13']:.2f}")
# X escape: Balaton & Brown 2021: >15% of X genes escape or variably escape
print(f"If ~15% of {pc['X']} X coding genes escape XCI -> ~{0.15*pc['X']:.0f} genes with extra dosage in 47,XXX "
      f"(vs {pc['21']} for +21)")
# parental origin T21 (Antonarakis 1991 NEJM)
print(f"T21 maternal origin: 184/193 = {184/193*100:.1f}%; paternal 9/193 = {9/193*100:.1f}%")

# ---------------------------------------------------------------- (4) strong force scale
hr("4 STRONG FORCE vs CHEMISTRY")
hbarc = 197.3269804           # MeV fm, CODATA 2022 exact
mpi = 139.57039               # MeV, PDG 2025 (pi+-)
a0_fm = 5.29177210544e-11 / 1e-15  # Bohr radius in fm, CODATA 2022
Ry = 13.605693122990          # eV, CODATA 2022
r_yuk = hbarc / mpi
print(f"Yukawa range hbar/(m_pi c) = {hbarc}/{mpi} = {r_yuk:.3f} fm")
print(f"Bohr radius = {a0_fm:,.0f} fm -> a0 / range = {a0_fm/r_yuk:,.0f}")
mH, mn, u = 1.00782503223, 1.00866491606, 931.49410372   # NIST: m(1H) u, m_n u (CODATA 2022), u in MeV
BE = (6*mH + 6*mn - 12.0) * u
print(f"B(12C) = (6*{mH} + 6*{mn} - 12) u * {u} MeV/u = {BE:.3f} MeV; per nucleon = {BE/12:.3f} MeV")
print(f"per-nucleon nuclear binding / hydrogen ionization (Ry) = {BE/12*1e6:.3e} eV / {Ry} eV = {BE/12*1e6/Ry:.2e}")
mu, md, mp, mneu = 2.16, 4.70, 938.27208943, 939.56542194   # PDG 2025 MSbar(2 GeV); CODATA 2022
print(f"proton: (2*{mu}+{md}) / {mp} = {(2*mu+md):.2f}/{mp:.3f} = {100*(2*mu+md)/mp:.2f}% of mass from quark rest masses")
print(f"neutron: ({mu}+2*{md}) / {mneu} = {(mu+2*md):.2f}/{mneu:.3f} = {100*(mu+2*md)/mneu:.2f}%")
# RERF: stable aberrations children of A-bomb survivors
print(f"RERF F1 stable aberrations: exposed 18/8322 = {100*18/8322:.2f}%; control 25/7976 = {100*25/7976:.2f}%")

# ---------------------------------------------------------------- (5) topology
hr("5 TOPOLOGY: GENUS = CYCLE RANK OF TUBE GRAPH (exterior = one vertex)")
def cycle_rank(edges):
    V = sorted({v for e in edges for v in e}); idx = {v: i for i, v in enumerate(V)}
    parent = list(range(len(V)))
    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in edges: parent[f(idx[a])] = f(idx[b])
    C = len({f(i) for i in range(len(V))})
    return len(edges) - len(V) + C, len(edges), len(V), C
gut = [("Ext", "Pharynx"),            # mouth
       ("Pharynx", "Ext")]            # oesophagus -> anus
nose = [("Ext", "NasL"), ("NasL", "Pharynx"), ("Ext", "NasR"), ("NasR", "Pharynx")]   # nostrils + choanae
lac = []
for s in "LR":                        # upper + lower punctum -> canaliculi -> sac -> NLD -> inferior meatus
    lac += [("Ext", f"Sac{s}"), ("Ext", f"Sac{s}"), (f"Sac{s}", f"Nas{s}")]
fem = [("Ext", "Uterus"), ("Uterus", "Periton"), ("Uterus", "Periton")]   # vagina; 2 fallopian tubes into closed sac
eust = [("Pharynx", "MidEarL"), ("Pharynx", "MidEarR")]                  # dead ends while eardrums intact
eardrum_perf = [("MidEarL", "Ext"), ("MidEarR", "Ext")]
models = [("mouth+anus only", gut),
          ("+ nostrils", gut + nose),
          ("+ nostrils + 4 lacrimal puncta", gut + nose + lac),
          ("+ Eustachian tubes, intact eardrums", gut + nose + lac + eust),
          ("female: + vagina/uterus/2 tubes/peritoneum", gut + nose + lac + fem),
          ("both eardrums perforated / ear tubes (male)", gut + nose + lac + eust + eardrum_perf),
          ("imperforate anus (no GI exit) + nostrils + puncta", [gut[0]] + nose + lac),
          ("bilateral choanal atresia (male, with puncta)", gut + [nose[0], nose[2]] + lac)]
for name, E in models:
    g, e, v, c = cycle_rank(E)
    print(f"  {name:52s}: E={e:2d} V={v:2d} C={c} -> genus = E-V+C = {g}")

# ENS
hr("5b ENTERIC NEURONS")
brain = 86.1e9   # Azevedo 2009
for n, src in [(168e6, "Michel 2022"), (200e6, "Furness 2014 low"), (600e6, "Furness 2014 high")]:
    print(f"  {src}: {n:.3g} / {brain:.3g} = {100*n/brain:.2f}% of brain neuron count")

# ---------------------------------------------------------------- (6) gravity vs end of life
hr("6 GRAVITATIONAL TIME DILATION AT HUMAN SCALES")
g, c = 9.80665, 299792458.0     # CODATA 2022 (standard gravity, exact), c exact
yr = 365.25*86400
for h in [0.33, 1.0]:
    f = g*h/c**2
    print(f"  h = {h} m: dt/t = g h / c^2 = {g}*{h}/{c:.0f}^2 = {f:.3e}; per year {f*yr*1e9:.2f} ns; "
          f"over 80 yr {f*80*yr*1e9:.0f} ns")
print(f"  Kerr 2014: 59 analysed of 66 consented -> {59/66*100:.0f}% retained")
print(f"  Xu 2023: 2 of 4 patients showed gamma surge = {2/4*100:.0f}%")

hr("3b AUTOSOME RANKINGS (viable full trisomies = 13, 18, 21)")
auto_by_genes = sorted(auto, key=lambda c: pc[c])
auto_by_len = sorted(auto, key=lambda c: G38[c])
print("fewest coding genes:", [(c, pc[c]) for c in auto_by_genes[:5]])
print("shortest:", [(c, round(G38[c]/1e6, 1)) for c in auto_by_len[:6]])
print("chr13 length rank among autosomes (1 = shortest):", auto_by_len.index("13") + 1)
print("chr19:", G38["19"]/1e6, "Mb,", pc["19"], "coding genes")
