# Physics and biology fact-check

The user is a neonatologist with a mathematics background. They proposed a set of ideas that link particle physics, gravity and cosmology to physiology and medicine, and asked for rigorous pushback rather than validation. This report checks each idea against primary sources and attaches computed numbers.

**Method.**

- The claims were split into four clusters, and each was checked independently:
  - **particles:** Higgs, W/Z, gluons, fermions and bosons, dark matter;
  - **glucose and the weak force:** quark content of glucose, the breath loop, radioactivity in the body, neutrinos;
  - **biology:** zinc spark, iodine, trisomies, the strong force and mutation, body topology, end of life;
  - **gravity:** time dilation, the idiom, the Wow! signal.
- Every derived number (counts, ratios, rates, fractions) was computed in a Python script. The inputs came from the sources cited: PDG 2026, CODATA 2022 via NIST, ENSDF, NCBI, Ensembl and the papers linked below. Measured values such as survival rates are quoted from their sources.
- A separate adversarial verifier then:
  - recomputed every number;
  - checked the headline citations against the source text;
  - listed corrections.

The verifier found no arithmetic errors in any headline figure. Its corrections concern wording, attribution and how strong a verdict should be. All of them are applied below and listed in [What the verifier changed](#what-the-verifier-changed).

**Verdicts used.**

- **True / partly true:** the claim, or part of it, matches the evidence.
- **Metaphor that maps onto real structure:** the analogy has a real counterpart in the physics, but it is not literally true.
- **False as stated:** contradicted by measurement or by established theory.
- **Unsupported:** a possibility with no evidence and no known mechanism. It cannot strictly be shown false.
- **Outside physics:** not a testable physical claim.

**See also.** [`../letters/words.md`](../letters/words.md#2-ideas-and-their-status) is a plain-language companion that covers many of the same ideas with its own status words. Where the two differ, this report is the authority.

| Idea | Verdict | Section |
|---|---|---|
| People as fermions, communication as bosons | Metaphor that maps onto real structure | [1.1](#11-people-as-fermions-communication-as-bosons) |
| W, Z and gluon as one force | Partly true | [1.2](#12-w-z-and-gluon-as-one-all-encompassing-force) |
| Three sets of four particles | True as one valid counting | [1.3](#13-three-sets-of-four) |
| Glucose at the quark level | True (counts); mass budget needs better wording | [1.4](#14-glucose-at-the-quark-level) |
| The breath loop and its leak | Metaphor that maps onto real structure | [1.5](#15-the-breath-loop-and-its-leak) |
| The weak force inside every body | True | [1.6](#16-the-weak-force-inside-every-body) |
| Gravity changes time for the body | Partly true (real, but about 1e-16 per metre) | [1.7](#17-gravity-changes-how-fast-time-passes-for-the-body) |
| The body as a torus, the gut as a second brain | Metaphor that maps onto real structure | [1.8](#18-the-body-as-a-torus-the-gut-as-a-second-brain) |
| Massless Higgs in the Navier-Stokes centre line | False as stated | [2.1](#21-the-higgs-boson-and-the-navier-stokes-centre-line) |
| Weak force as speech and love; Dirac equation as a torus | False as stated | [2.2](#22-weak-force-as-speech-and-love-people-as-fermions-dirac-equation-as-a-torus) |
| Neutrinos and perception | Unsupported; physically implausible | [2.3](#23-neutrinos-and-perception) |
| Dark matter outside space-time | Unsupported as stated | [2.4](#24-dark-matter-outside-space-time) |
| The Wow! signal (pulsar, explained, neutrinos) | False / a proposal / false | [2.5](#25-the-wow-signal) |
| Trisomy 13, 18, 21 and DNA size | Partly true: gene dosage, not DNA size | [3.1](#31-trisomy-13-18-and-21-dna-size-versus-gene-dosage) |
| The strong force and trisomies | False as stated | [3.2](#32-trisomies-and-the-strong-force) |
| Zinc spark at conception | True | [3.3](#33-the-zinc-spark-at-conception) |
| Thyroid iodine and intelligence | Partly true | [3.4](#34-thyroid-iodine-and-intelligence) |
| A "trinity" of generations | Outside physics | [4.1](#41-the-trinity) |
| Dark matter and the afterlife | Outside physics | [4.2](#42-dark-matter-and-the-afterlife) |
| End-of-life memory and felt time | Partly true (phenomena real); the gravity link is false as stated (about 1e-16 per metre; no part in felt time) | [4.3](#43-end-of-life-memory-and-the-perception-of-time) |
| "The gravity of the situation" | Metaphor; the history runs the other way | [4.4](#44-the-gravity-of-the-situation) |

---

## 1. Where the intuition lands on real physics

### 1.1 People as fermions, communication as bosons

**Verdict: metaphor that maps onto real structure.** The structure of the analogy is right. The literal readings are not, and are covered in [2.2](#22-weak-force-as-speech-and-love-people-as-fermions-dirac-equation-as-a-torus).

- In quantum field theory, matter is made of spin-1/2 fermions. Forces act by exchanging spin-1 gauge bosons: the photon, W, Z and gluons. The 1984 Nobel citation calls the W and Z "communicators of weak interaction".
- Spin-1/2 has a real topological signature. The rotation operator is U(θ) = exp(−iθσ_z/2). Computed:
  - U(2π) = −I and U(4π) = +I;
  - the ordinary rotation gives R(2π) = I.
- SU(2) is the 3-sphere S³ and double-covers SO(3) ≅ RP³, with π₁(SO(3)) = Z/2. This is what the belt (plate) trick shows.
- Neutron interferometry measured the 4π periodicity. Rauch et al. (1978) obtained 716.8 ± 3.8° against a predicted 720°, a difference of 0.84σ.

Sources: [Nobel 1984](https://www.nobelprize.org/prizes/physics/1984/summary/), [Rauch et al. 1978](https://link.springer.com/doi/10.1007/BF01321193), [Stoytchev, topology of SO(3)](https://arxiv.org/abs/2310.19665). A minority view disputes how the 4π experiments should be interpreted, but not the measured numbers: [Sassoli de Bianchi](https://arxiv.org/abs/1601.07053).

### 1.2 W, Z and gluon as one all-encompassing force

**Verdict: partly true.** The W, Z and photon really are unified. Adding the gluon is a hypothesis that has not been confirmed.

- **Electroweak unification is established.** The W, Z and photon come from one SU(2)×U(1) theory (Nobel 1979: Glashow, Salam, Weinberg). The W and Z were discovered in 1983 (Nobel 1984).
- **The Standard Model gauge group** is SU(3)×SU(2)×U(1), which has 8 + 3 + 1 = 12 gauge bosons.
- **Grand unification (adding the gluon) is hypothetical.**
  - The PDG 2026 review says coupling unification "fails in the SM".
  - With supersymmetry (MSSM), the couplings meet near M_G ≈ 2e16 GeV with α_G⁻¹ ≈ 24.3. Supersymmetry has not been observed.
- **Proton decay, the key GUT prediction, has not been seen.**
  - Super-Kamiokande (450 kton·yr) gives τ/B(p→e⁺π⁰) > 2.4e34 yr at 90% CL. That is 1.74e24 times the age of the universe.
  - The mode-independent limit (p → invisible) is τ > 9e29 yr.
  - A 70 kg body has 4.2e28 nucleons. Even if every nucleon were a proton, the bound allows fewer than 1.8e-6 such decays per year.
- **Gravity is not unified with the other forces.** The graviton has not been observed; its mass bound is < 1.76e-23 eV.
- **The Standard Model has many free parameters,** so it is not a single all-encompassing force. The minimal Standard Model (massless neutrinos) has 19. Including the measured neutrino masses and mixing brings this to about 26 (Dirac neutrinos) to 28 (Majorana neutrinos).

Sources: [Nobel 1979](https://www.nobelprize.org/prizes/physics/1979/summary/), [Nobel 1984](https://www.nobelprize.org/prizes/physics/1984/summary/), [PDG 2026 GUT review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-guts.pdf), [Super-K, PRD 102, 112011](https://arxiv.org/abs/2010.16098), [PDG 2026 baryon summary](https://pdg.lbl.gov/2026/tables/rpp2026-sum-baryons.pdf), [PDG 2026 cosmological parameters](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-cosmological-parameters.pdf).

### 1.3 Three sets of four

**Verdict: true as one valid counting.** The "trinity" reading is outside physics ([4.1](#41-the-trinity)).

- **The basic count.** There are 3 generations of fermions. Each generation has 4 types: an up-type quark, a down-type quark, a charged lepton and a neutrino. That gives 4 × 3 = 12.
- **"12" depends on how you count:**
  - with 3 colours per quark: 24;
  - adding antiparticles: 48;
  - as chiral (Weyl) fields: 15 per generation, 45 in total, or 48 with right-handed neutrinos.
- **Measured number of light neutrino species (Z invisible width).** This counts only neutrinos that couple to the Z and are lighter than M_Z/2. Cosmology's baseline N_eff is 3.044.

  | Analysis | N_ν | Distance from 3 |
  |---|---|---|
  | LEP-SLC 2006 | 2.9840 ± 0.0082 | 1.95σ below |
  | Janot & Jadach 2020 (corrected Bhabha cross-section; used by PDG 2026) | 2.9963 ± 0.0074 | 0.50σ |

- **Colour is fixed at 3 by anomaly cancellation.** Within each generation the anomaly cancels only if N_c·(1/3) − 1 = 0, i.e. N_c = 3. This holds generation by generation, so it says nothing about how many generations there are.
- **Why there are 3 generations is unexplained.** Known constraints:
  - CP violation in quark mixing needs at least 3 generations. The number of CP phases is (n−1)(n−2)/2: 0 for n = 2 and 1 for n = 3 (Kobayashi-Maskawa, Nobel 2008).
  - QCD asymptotic freedom needs n_f ≤ 16, i.e. at most 8 generations.
  - No known principle fixes the number at exactly 3.
- **The other real "12"** is the gauge bosons, but they group as 8/3/1, not 4/4/4.

Sources: [PDG 2026 neutrino-types listing](https://pdg.lbl.gov/2026/listings/rpp2026-list-number-neutrino-types.pdf), [PDG 2026 light neutrino types review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-light-neutrino-types.pdf), [Janot & Jadach 2020](https://arxiv.org/abs/1912.02067), [PDG 2026 GUT review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-guts.pdf), [PDG 2026 QCD review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-qcd.pdf), [Nobel 2008](https://www.nobelprize.org/prizes/physics/2008/summary/).

### 1.4 Glucose at the quark level

**Verdict: the counts are exact.** "About 99% of the mass is gluons" needs better wording.

For C₆H₁₂O₆ built from ¹²C, ¹H and ¹⁶O:

| Protons | Neutrons | Electrons | Nucleons | Valence up quarks | Valence down quarks | Valence quarks |
|---|---|---|---|---|---|---|
| 96 | 84 | 96 | 180 | 276 | 264 | 540 |

- **Mass.** The monoisotopic mass is 180.06338810 u = 167,727.98 MeV, matching NIST's 180.0633881.
- **Natural glucose is not monoisotopic.** About 1.07% of carbon atoms are ¹³C and about 0.2% of oxygen atoms are ¹⁸O.
- **"Valence" is a bookkeeping label.** Each nucleon also holds a sea of quark-antiquark pairs and gluons whose number is not fixed.

Mass budget of one molecule, as a share of its rest energy (167.728 GeV):

| Component | Energy | Share |
|---|---|---|
| Valence quark rest masses (Higgs-given; PDG MS-bar at 2 GeV, m_u = 2.16, m_d = 4.70 MeV) | 1,836.96 MeV | 1.095% (1.073–1.118%) |
| Electron masses (Higgs-given) | 49.056 MeV | 0.0292% |
| Nucleon masses minus valence quark masses (QCD dynamics) | 167,160.66 MeV | 99.66% |
| Nuclear binding (B(¹²C) = 92.162 MeV, B(¹⁶O) = 127.619 MeV) | −1,318.69 MeV | −0.786% |
| Chemical energy of complete oxidation | 29.07 eV per molecule | 1.73e-10 (NIST ΔcH = −2805.0 kJ/mol) to 1.80e-10 (ΔG′ ≈ −2910 kJ/mol) |

The first four rows sum to 100.00%, as the verifier checked.

**Correction to "99% from gluons".** The 1%/99% split counts only the valence rest masses. A lattice-QCD decomposition of the proton (Yang et al. 2018) splits the mass differently:

| Contribution | Share of proton mass |
|---|---|
| Quark kinetic and potential energy | about 32–33% |
| Gluon field energy | about 36–37% |
| Trace anomaly | about 23% |
| u, d and s quark-mass condensate (sigma terms) | about 9% |

The split depends on the renormalisation scheme and scale. An accurate statement is: "about 99% of the mass is QCD interaction energy, not quark rest mass". Gluon field energy alone is about a third.

**Body scale.** Metabolising 2000 kcal releases 8.368 MJ, which removes E/c² = 9.3e-11 kg of mass: about 93 ng per day.

Sources: [NIST isotopic compositions](https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl), [NIST WebBook, glucose](https://webbook.nist.gov/cgi/cbook.cgi?ID=C50997&Mask=2), [NIST WebBook, α-D-glucose combustion](https://webbook.nist.gov/cgi/cbook.cgi?ID=C492626&Mask=2), [PDG quark summary](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf), [BioNumbers ΔG′](https://bionumbers.hms.harvard.edu/bionumber.aspx?id=103388), [eQuilibrator](https://equilibrator.weizmann.ac.il/static/classic_rxns/classic_reactions/glucose_ox.html), [Yang et al., PRL 121, 212001](https://arxiv.org/abs/1808.08677).

### 1.5 The breath loop and its leak

**Verdict: metaphor that maps onto real structure.** Counted as CO₂ out per O₂ in, the gas loop closes exactly only for carbohydrate. On a mixed diet the "leak" is real and measurable.

Respiratory quotient (RQ) = CO₂ produced / O₂ consumed:

| Fuel | RQ | O₂ not returned as CO₂ |
|---|---|---|
| Glucose, C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O | 6/6 = 1.000 | 0% |
| Palmitate, C₁₆H₃₂O₂ + 23 O₂ → 16 CO₂ + 16 H₂O | 16/23 = 0.6957 | 30.4% |
| Protein (albumin equation) | 63/77 = 0.818 | 18.2% |
| Mixed diet | about 0.80–0.85 | about 15–20% |

- **Where the extra oxygen goes.** The O₂ that does not come back as CO₂ leaves the body bound in water.
- **Even at RQ = 1 the loop does not close atom for atom:**
  - O₂ is reduced to water at complex IV. This step is textbook biochemistry; no source for it was fetched.
  - Oxygen atoms in CO₂ exchange rapidly with body water, via carbonic anhydrase.
- **Metabolic water.** Glucose yields 0.600 g of water per g; palmitate 1.124 g/g. ICRP 23 Reference Man lists 350 mL/day of water from oxidation of food.
- **Anatomic dead space** is about 150 mL in an adult, roughly 30% of a 500 mL tidal volume, or about 2 mL/kg. The StatPearls pages returned 403 when fetched, so these figures come from search excerpts of those pages.
- **Respiratory water loss** is about 400 mL/day in an unstressed adult.
  - An independent estimate gives 250–304 g/day. It uses the Buck vapour formula (43.9 g/m³ saturated at 37 °C, 37.5 at 34 °C, 8.6 for inspired air at 20 °C and 50% RH) and 8.64 m³/day of ventilation.
  - The loss falls toward zero with fully humidified 37 °C inspired gas, as on a ventilator.
  - Metabolic water roughly offsets it.

Sources: [OpenAnesthesia, respiratory quotient](https://www.openanesthesia.org/keywords/respiratory-quotient/), [Som et al. 2015, CO₂-water oxygen exchange](https://pmc.ncbi.nlm.nih.gov/articles/PMC4454186), [ICRP 23 water balance (BioNumbers)](https://bionumbers.hms.harvard.edu/files/Water%20balance%20for%20reference%20man.pdf), [StatPearls, dead space](https://www.statpearls.com/point-of-care/24497), [StatPearls, respiratory dead space](https://www.statpearls.com/point-of-care/17518), [Brandis, insensible water loss](https://med.libretexts.org/Bookshelves/Anatomy_and_Physiology/Fluid_Physiology_(Brandis)/03%3A_Water_Balance/3.02%3A_Insensible_Water_Loss).

### 1.6 The weak force inside every body

**Verdict: true.** Beta decay of ⁴⁰K and ¹⁴C goes on continuously in every person. Each decay emits a neutrino or antineutrino.

Inputs from ICRP 23 Reference Man (70 kg): K = 140 g and C = 16,000 g.

| Isotope | Nuclear data (ENSDF) | Atoms / specific activity | Activity in body |
|---|---|---|---|
| ⁴⁰K | T½ = 1.248e9 y; abundance 0.0117%; β⁻ 89.28(11)%; EC + β⁺ 10.72(11)% | 2.52e20 atoms (16.7 mg) | 4,440 Bq (31.7 Bq/g K); cited values 3,850–5,000 Bq |
| ¹⁴C | T½ = 5700 ± 30 y; 100% β⁻; modern ¹⁴C/C = 1.176e-12 | 0.227 Bq/g C | 3,635 Bq (16 kg C) or 2,863 Bq (12.6 kg C); a cited value is 3,150 Bq |

- **Neutrino emission.** The body emits 7,600 antineutrinos/s (6.57e8 per day) and 476 neutrinos/s (4.11e7 per day): about 7.0e8 per day in total. Using the HPS value of 5,000 Bq for ⁴⁰K gives 7.5e8 per day. Rb-87, H-3 and the U/Th series are not included.
- **⁴⁰K gamma rays.** About 470 to 530 gammas of 1461 keV are produced per second (4,440 to 5,000 Bq × about 10.6%). Most escape the body, but not all.
- **Beta decays.** There are 3.4e8 ⁴⁰K β⁻ decays per day.
- **Neutrino self-interactions.** Almost none of the emitted neutrinos interact. Order of magnitude: about 5e-12 self-interactions per day.

**¹⁴C in DNA. Verdict: true, but negligibly small next to ordinary somatic mutation.**

- **Mechanism.** Ab initio simulations (Sassi et al. 2014) show that ¹⁴C → ¹⁴N transmutation can break sugar-backbone bonds and create mutagenic mispairs. Whether DNA repair recognises the extra nitrogen is unknown.
- **Per nucleus.** A diploid genome is 2 × 3.055e9 bp (T2T-CHM13) with 19–20 C atoms per base pair, i.e. 1.16–1.22e11 C atoms. That is 0.137–0.144 ¹⁴C atoms and 1.66–1.75e-5 ¹⁴C decays per nucleus per year.
- **Body-wide.** With about 3e12 nucleated cells (Sender 2016), this gives about 1.4e5 decays per day (1.6/s), or about 4e9 over 80 years.
- **Discrepancy with Sassi.** Sassi et al. state about 5e10 per lifetime. That figure is reproduced only if all 3.72e13 body cells (Bianconi 2013) carry a genome. Red cells have no nucleus, so this suggests about a 10× overcount. This is an inference about their method.
- **Comparison.** An adult stem cell gains about 40 new mutations per year (Blokzijl 2016). 1.7e-5 / 40 = 4e-7: even if every ¹⁴C decay in DNA caused a mutation, it would add under a millionth of the somatic burden.

Sources: [ENSDF ⁴⁰K](https://www.nndc.bnl.gov/ensnds/40/K/adopted.pdf), [ENSDF ¹⁴C](https://www.nndc.bnl.gov/ensnds/14/C/adopted.pdf), [ICRP 23 element content (BioNumbers)](https://bionumbers.hms.harvard.edu/files/Reference%20man-total%20body%20content%20for%20some%20elements.pdf), [HPS, radioactivity in the body](https://hps.org/ate_faq/faqradbods/), [Springer, body ¹⁴C](https://link.springer.com/article/10.1007/s10311-007-0100-7), [Radiocarbon, modern-carbon standard](https://journals.uair.arizona.edu/index.php/radiocarbon/article/download/691/696), [Sassi et al. 2014](https://pubmed.ncbi.nlm.nih.gov/24121105/), [Nurk et al. 2022 (T2T-CHM13)](https://pubmed.ncbi.nlm.nih.gov/35357919/), [Sender cell count (BioNumbers)](https://bionumbers.hms.harvard.edu/bionumber.aspx?id=112985), [Bianconi et al. 2013](https://pubmed.ncbi.nlm.nih.gov/23829164/), [Blokzijl et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27698416/).

### 1.7 Gravity changes how fast time passes for the body

**Verdict: partly true.** Gravitational time dilation is real and has been measured at human scales. But near Earth's surface it is about 1e-16 per metre, far too small to matter for biology.

In a weak field, a clock that is higher by h runs faster by the fraction g·h/c². The calculation uses c = 299,792,458 m/s and g_n = 9.80665 m/s², both exact by definition.

| Height difference | Fractional rate | Accumulated over 80 years |
|---|---|---|
| 0.33 m | 3.60e-17 | 91 ns |
| 1 m | 1.091e-16 (3.44 ns per year) | 275 ns |
| 1.7 m (head versus feet) | 1.855e-16 (16.0 ps per day) | 468 ns, i.e. about 470 ns (467.0–469.4 ns for g from equator to pole) |

- **How slowly it builds.** The head-to-feet difference takes 171 years to reach 1 µs.
- **Measured: Chou et al. 2010.** Raising an Al⁺ optical clock by 33 cm gave a fractional shift of (4.1 ± 1.6)e-17, against a predicted 3.60e-17 (0.31σ). Over 79 years that height gives 89.7 ns, matching NIST's "about 90 billionths of a second over 79 years".
- **Measured: Bothwell et al. 2022.** The shift was measured inside a single millimetre-sized cloud of about 100,000 ⁸⁷Sr atoms. Predicted: −1.09e-19 per mm; measured: −9.8(2.3)e-20 per mm (the preprint's final value). The ratio is 0.90 ± 0.21, i.e. 0.48σ from the prediction.
- **Context: whole potential wells.** Earth's entire well compared with deep space is 6.96e-10, or 1.76 s over 80 years. The Sun's potential at 1 AU is 9.87e-9, or 24.9 s.
- **Context: motion.** Running at 10 m/s slows a clock by 5.56e-16, three times the head-to-feet gravitational effect.

Sources: [Chou et al. 2010](https://pubmed.ncbi.nlm.nih.gov/20929843/), [NIST release](https://www.nist.gov/news-events/news/2010/09/nist-pair-aluminum-atomic-clocks-reveal-einsteins-relativity-personal), [Bothwell et al. 2022](https://doi.org/10.1038/s41586-021-04349-7) ([preprint](https://arxiv.org/abs/2109.12238)), [CODATA c](https://physics.nist.gov/cgi-bin/cuu/Value?c), [CODATA g_n](https://physics.nist.gov/cgi-bin/cuu/Value?gn), [NASA Earth fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html), [NASA Sun fact sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html).

### 1.8 The body as a torus; the gut as a second brain

**Verdict: metaphor that maps onto real structure.** A torus is the minimum: the body is a handlebody of genus at least 1, and the genus is higher once the nose and tear ducts are counted. "Second brain" fits the gut's autonomy, but the gut has well under 1% of the brain's neurons.

The genus is the number of independent loops in the network of tubes open to the outside, counting the outside as one node: genus = E − V + C (edges minus vertices plus connected components).

| Configuration | Genus |
|---|---|
| Mouth to anus only | 1 |
| + nostrils joining the pharynx through the choanae | 3 |
| + 4 lacrimal puncta (canaliculi → lacrimal sac → nasolacrimal duct → nose) | 7 |
| Female: + vagina, uterus and two fallopian tubes opening into the peritoneal sac | 8 |
| Male, both eardrums perforated or with ear tubes (Eustachian tubes are dead ends while eardrums are intact) | 9 |
| Male, imperforate anus | 6 |
| Male, bilateral choanal atresia | 5 |

- **Genus 7 is a convention.** The popular "genus 7" depends on what is counted and on a minimum hole size; it is not a fixed fact.
- **The gut lumen is outside.** Topologically the lumen is outside the body, so the enteric nervous system lines an external surface.
- **Neuron count.** Estimates of enteric neurons disagree:
  - Michel et al. 2022, the most systematic count: 168 million;
  - Furness et al. 2014: 200–600 million.

  Against the brain's 86.1 billion (Azevedo 2009), that is 0.20–0.70%. The "400–600 million" figure is the upper end of an older range.
- **Autonomy.** The enteric nervous system of the small intestine and colon contains complete reflex circuits. Cutting the vagal or sympathetic connections has minor effects on gut function.

Sources: [StatPearls, nasolacrimal anatomy](https://www.statpearls.com/point-of-care/23996), [NCBI Bookshelf NBK547660](https://www.ncbi.nlm.nih.gov/books/NBK547660/), [Vsauce (reaches the same 7)](https://www.youtube.com/watch?v=egEraZP9yXQ), [Furness et al. 2014](https://doi.org/10.1007/978-1-4939-0897-4_3), [Michel et al. 2022](https://doi.org/10.1111/nmo.14440), [Azevedo et al. 2009](https://doi.org/10.1002/cne.21974).

---

## 2. Where it needs correcting

### 2.1 The Higgs boson and the Navier-Stokes centre line

Claim: "The Higgs boson is massless and could live in the infinite center line that makes Navier-Stokes smooth."

**Verdict: false as stated.**

**The Higgs is not massless.**

| Particle | Mass (PDG 2026) | Note |
|---|---|---|
| Higgs boson | 125.13 ± 0.11 GeV | 133.4 proton masses; PDG 2025 gave 125.20 ± 0.11 |
| W boson | 80.3625 ± 0.0077 GeV | excludes the 2022 CDF value |
| Z boson | 91.1879 ± 0.0020 GeV | |
| Photon | < 1e-18 eV | massless |
| Gluon | 0 in theory | a mass of a few MeV is not ruled out |
| Graviton | < 1.76e-23 eV | hypothetical |

**The field and the boson are different things.**

- **The Higgs field fills all of space,** with the same nonzero value everywhere: v = (√2 G_F)^(−1/2) = 246.22 GeV. It is not confined to a line.
  - The W, Z and fermion masses come from v.
  - The photon and gluon stay massless because U(1)_em and SU(3)_colour are unbroken.
- **The Higgs boson is a short-lived excitation of that field.** Its lifetime is τ ≈ 1.6e-22 s for the Standard Model width (Γ = 4.1 MeV), or 2.2e-22 s for the measured central width (Γ = 3.0 +1.5/−0.7 MeV). It travels cτ ≈ 44–86 fm before decaying. It cannot "live" anywhere in a fluid.
- **The Higgs mechanism gives about 1% of a proton's mass.** (2 × 2.16 + 4.70) / 938.272 = 0.96%, in the MS-bar scheme, so the figure is scheme-dependent.

**The weak force cannot reach fluid scales.**

- The weak force has range ħc/(M_W c²) = 2.455e-18 m (2.164e-18 m using the Z mass).
- In water, the nearest-neighbour O-O distance is 2.80(1) Å; this was measured in ambient water, not at 37 °C. The mean spacing from the density at 37 °C is 3.11 Å.
- So the weak range is 1.1e8 to 1.4e8 times smaller than the distance between water molecules.

**Navier-Stokes contains no particle physics.** It is a classical continuum equation. For water at 37 °C, the only microphysics it uses is ρ = 993.33 kg/m³ and μ = 691.3 µPa·s (ν = 6.96e-7 m²/s). It contains no particles, no Higgs field and no weak force.

**Status of the Clay problem.** The Clay problem asks whether smooth 3D solutions exist for all time or can blow up. On 8 September 2026 OpenAI posted a paper, *Finite time blowup for Navier–Stokes*, with a Lean formalisation, claiming finite-time blowup with a smooth, compactly supported external force. Its Theorem 1.1 gives Clay's alternative (C), and its Corollary 10.6 the periodic alternative (D). On 11 September Clay spoke of "the announcement that the Navier-Stokes problem has apparently been settled" and said its process "is deliberately unhurried". Its problem page still lists the problem as "Active" (checked 17 and 18 Oct 2026), so Clay has not accepted the claim. Scientific American (21 Sep 2026) quotes Luis Silvestre: "The Clay problem is settled, but the main problem for the Navier-Stokes equations is not." The unforced alternatives (A) and (B) remain open. OpenAI's own announcement page could not be opened here (HTTP 403); its paper could. The same status, with the same sources, is in [`../ns-phase-audit/enstrophy-jet/RESULTS.md`](../ns-phase-audit/enstrophy-jet/RESULTS.md) §8.

**On the "centre line".**

- Caffarelli-Kohn-Nirenberg (1982) proved that, for suitable weak solutions, the singular set has zero one-dimensional parabolic Hausdorff measure: P¹(S) = 0. Fefferman's Clay statement (2000) calls this "the best partial regularity theorem known so far".
- Fefferman notes that the singular set "cannot contain a spacetime curve of the form {(x,t): x = φ(t)}". That is a single point moving in time, not a line.
- A spatial line segment at a single instant also has P¹ > 0, so a singular line or filament is excluded as well.
- Smoothness is a property of the whole solution. It is not supplied by something that lives on a line.

Sources: [PDG 2026 gauge and Higgs bosons](https://pdg.lbl.gov/2026/tables/rpp2026-sum-gauge-higgs-bosons.pdf), [PDG 2025 gauge and Higgs bosons](https://pdg.lbl.gov/2025/tables/rpp2025-sum-gauge-higgs-bosons.pdf), [PDG 2026 Higgs review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-higgs-boson.pdf), [PDG 2026 quarks](https://pdg.lbl.gov/2026/tables/rpp2026-sum-quarks.pdf), [CODATA G_F](https://physics.nist.gov/cgi-bin/cuu/Value?gf), [CODATA ħc](https://physics.nist.gov/cgi-bin/cuu/Value?hbcmevf), [Skinner et al. 2013, ambient water](https://pubmed.ncbi.nlm.nih.gov/23445023/), [NIST water properties](https://webbook.nist.gov/cgi/fluid.cgi?ID=C7732185&Action=Page), [Fefferman, Clay problem statement](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), [Clay Navier-Stokes page](https://www.claymath.org/millennium/navier-stokes-equation/), [OpenAI, Finite time blowup for Navier–Stokes (8 Sep 2026)](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), [Clay announcement, 11 Sep 2026](https://www.claymath.org/news/navier-stokes-announcement/), [Quanta, 8 Sep 2026](https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/), [Howlett, Scientific American, 21 Sep 2026](https://www.scientificamerican.com/article/did-openai-solve-the-wrong-navier-stokes-problem/), [NYU Shanghai RITS news item](https://rits.shanghai.nyu.edu/ai/openai-navier-stokes-proof-credit-dispute/).

### 2.2 Weak force as speech and love; people as fermions; Dirac equation as a torus

**Verdict: false as stated, for all three literal readings.**

- **Communication is electromagnetic, not weak.** All biological communication (speech, nerve signals, chemistry, light) is electromagnetic and carried by photons. At chemical energies (E = 13.6 eV) the effective weak coupling is G_F E² = 2.16e-21, against α = 7.30e-3: a ratio of 3.0e-19.
- **People are not fermions in any physical sense.**
  - Quantum statistics only matters when the thermal de Broglie wavelength is comparable to the spacing between particles. At 310 K it is 4.8e-25 m for a 70 kg body and 4.2e-9 m for a free electron.
  - Pauli exclusion (Nobel 1945) does real work for electrons: atomic shells, chemistry, why matter is solid. It does nothing for whole people.
- **The Dirac equation is not a torus.**
  - The Dirac equation is a first-order relativistic wave equation for 4-component spinors. It contains no toroidal structure.
  - The torus T² has fundamental group Z × Z. The spaces behind spin-1/2 are S³ (simply connected) and RP³ (Z/2), not a torus.
  - The torus image belongs to body topology ([1.8](#18-the-body-as-a-torus-the-gut-as-a-second-brain)), not to the Dirac equation.

Sources: [Nobel 1945](https://www.nobelprize.org/prizes/physics/1945/summary/), [CODATA G_F](https://physics.nist.gov/cgi-bin/cuu/Value?gf), [CODATA α⁻¹](https://physics.nist.gov/cgi-bin/cuu/Value?alphinv), [CODATA Rydberg energy](https://physics.nist.gov/cgi-bin/cuu/Value?rydhcev), [CODATA electron mass](https://physics.nist.gov/cgi-bin/cuu/Value?me), [Familton, quaternions and rotation groups](https://arxiv.org/abs/1504.04885).

### 2.3 Neutrinos and perception

**Verdict: unsupported; physically implausible.** "Could be related" is a possibility, so it cannot strictly be shown false. But there is no evidence and no mechanism, and the numbers below weigh heavily against it. What is true is that enormous numbers of neutrinos pass through us.

**How many pass through.**

- The standard solar model (B16-GS98) gives a flux at Earth of 6.54e10 cm⁻² s⁻¹, of which 91.5% is pp neutrinos.
- Borexino measured the pp flux at (6.6 ± 0.7)e10. An independent check from the solar luminosity (IAU nominal 3.828e26 W, Q = 26.731 MeV) gives 6.51e10.
- Through a body of projected area 0.5–1 m², that is 3.3e14 to 6.5e14 per second, or 2.8e19 to 5.6e19 per day. At night they arrive through the Earth.

**How many interact.** A 70 kg body holds 2.31e28 electrons.

| Route | Interactions per day | Notes |
|---|---|---|
| Cross-sections, pp neutrino-electron scattering | 0.039 (all ν_μ/ν_τ) to 0.139 (all ν_e) | oscillation puts the truth in between |
| Borexino Phase-II rates scaled to the body | 0.13 (pp + ⁷Be + pep); pp alone is 0.094 | about 47 per year (34 from pp alone; about 49 with CNO added, [`../letters/check_numbers.txt`](../letters/check_numbers.txt)); about 3,800 over 80 years |

- **Energy deposited.** Each interaction deposits at most 0.261 MeV.
- **Per neutrino.** The chance that one neutrino interacts while crossing 20 cm of tissue is about 8e-21.
- **Coherent scattering off nuclei** is not included. Its maximum recoil energy on ¹⁶O is only 23.7 eV.
- **Popular figures are too low.**
  - R. Davis's Nobel lecture: "the atoms in the human body capture a neutrino about every seventy years, or once in a lifetime".
  - J. Riordan, *Mental Floss* (18 July 2023): "In your entire lifetime, one or two solar neutrinos will hit an atom in your body."
  - *Symmetry* magazine (C. Walter, 2010) gives about a 1-in-4 chance per lifetime. That page refused the request here; the figure was seen only as quoted in outreach material.
  - A widely used school worksheet (KCL) gets an 8.6% chance per lifetime. It assumes about 1,800–1,900 times too few solar neutrinos, and a per-neutrino chance of 1e-22.
  - The Borexino-scaled figure, about 3,800 in 80 years, is about 3.6 orders of magnitude above "once in a lifetime" and about 4.6 above the worksheet's 0.086.

**Comparison with the body's own radioactivity.** The body undergoes 3.4e8 ⁴⁰K β⁻ decays per day, each depositing up to 1.311 MeV. That is about 3e9 times more events than solar-neutrino interactions:

- 2.6e9 against the Borexino-scaled total (3.6e9 against pp alone);
- 2.4e9 to 8.8e9 across the cross-section range.

No known mechanism links neutrinos to perception. A proposed link would have to explain why rare neutrino events matter when beta decays inside the body are about 3e9 times more frequent and more energetic.

Sources: [Vinyoles et al., standard solar models](https://arxiv.org/abs/1611.09867), [IAU 2015 nominal solar values](https://arxiv.org/abs/1510.07674), [Bahcall, Kamionkowski & Sirlin 1995](https://arxiv.org/abs/astro-ph/9502003), [Borexino, PRD 100, 082004](https://arxiv.org/abs/1707.09279), [ICRP 23 element content](https://bionumbers.hms.harvard.edu/files/Reference%20man-total%20body%20content%20for%20some%20elements.pdf), [KCL worksheet](https://www.kcl.ac.uk/physics/assets/pdf/outreach-invisible-explorers-neutrino-calculations-answers.pdf), [Davis, Nobel lecture, Rev Mod Phys 75, 985 (2003)](https://doi.org/10.1103/RevModPhys.75.985), [Riordan, Mental Floss, 2023](https://www.mentalfloss.com/science/physics/neutrino-particle-facts), [ENSDF ⁴⁰K](https://www.nndc.bnl.gov/ensnds/40/K/adopted.pdf).

### 2.4 Dark matter "outside space-time"

**Verdict: unsupported as stated.**

- **Observed dark matter is inside spacetime.** All evidence for dark matter is gravitational: stellar velocity dispersions, rotation curves, the virial theorem, lensing, the CMB and structure formation (PDG 2026 review). Dark matter is detected because it curves spacetime and moves within it.
- **Speculative models.** Some brane-world models put dark matter on a hidden or folded brane, off our 4-D brane (Arkani-Hamed et al. 2000, "Manyfold universe"). Even there it is still inside a higher-dimensional spacetime and is still seen only by its gravity. Kaluza-Klein dark matter is different: it moves in compact extra dimensions together with all ordinary matter, so it is not off our brane. None of these models involves death or an afterlife.

**How much there is.**

- Dark matter is 26.4% of the critical density and 84.4% of all matter.
- Two datasets differ slightly on its density: Planck gives Ω_c h² = 0.1200 ± 0.0012; the P-ACT-LB2 combination gives 0.1174 ± 0.0006.
- The local density near the Sun is uncertain. Published values span 0.2–1.5 GeV/cm³:
  - PDG 2026: 0.2–0.6 from global methods, 0.3–1.5 from Gaia, 0.47 ± 0.05 and 0.55 ± 0.17 from individual studies;
  - de Salas & Widmark 2021: 0.4–0.6 local, 0.3–0.5 global.

**Dark matter in a 70-litre body at any instant.**

| Local density | Mass in the body | Proton masses |
|---|---|---|
| 0.2 GeV/cm³ | 2.5e-23 kg | 1.49e4 |
| 0.4 GeV/cm³ | 5.0e-23 kg (7e-25 of body mass) | 2.98e4 |
| 0.6 GeV/cm³ | 7.5e-23 kg | 4.48e4 |

- **Number of particles.** This depends on the unknown particle mass. At 0.4 GeV/cm³: 280 particles if the mass is 100 GeV, 700 if 40 GeV, 28,000 if 1 GeV.
- **It does not stay.** It moves at about 233 km/s, crossing 1 m in 4.3 µs.
- **Any non-gravitational interaction is tightly limited.** LZ (4.2 tonne·yr) gives σ_SI < 2.2e-48 cm² at 40 GeV.
- **Crude upper bound on scatters in the body.** Assumptions: the whole body treated as ¹⁶O; coherent A² scaling; no form factor or detection threshold; WIMP-proton reduced mass 0.9168 GeV.
  - Result: σ_N ≈ 7.88e-44 cm², and fewer than 1.6e-3 scatters per year (1.53e-3), i.e. fewer than one every ~650 years.
  - This is an order-of-magnitude bound for a 40 GeV WIMP only.

Sources: [PDG 2026 dark matter review](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-dark-matter.pdf), [PDG 2026 cosmological parameters](https://pdg.lbl.gov/2026/reviews/rpp2026-rev-cosmological-parameters.pdf), [de Salas & Widmark 2021](https://arxiv.org/abs/2012.11477), [Read 2014](https://arxiv.org/abs/1404.1938), [Famaey 2015](https://arxiv.org/abs/1501.01788), [LZ, PRL 135, 011802](https://arxiv.org/abs/2410.17036), [CODATA eV-kg](https://physics.nist.gov/cgi-bin/cuu/Value?evkg), [Arkani-Hamed et al. 2000, Manyfold universe](https://arxiv.org/abs/hep-ph/9911386).

### 2.5 The Wow! signal

**(a) "The Wow pulsar." Verdict: false as stated.** The Wow! signal was a single narrowband radio transient, not a pulsar.

**What was detected.**

- Ohio State's Big Ear telescope recorded it at about 11:16 pm EDT on 15 Aug 1977 (03:16 UTC on 16 Aug, per the 2025 re-analysis).
- It appeared in one 10 kHz channel (fractional bandwidth 7.0e-6) and in only one of the two feed horns.
- The printout "6EQUJ5" encodes signal-to-noise values of 6, 14, 26, 30, 19 and 5; the peak was 30.0–31.0σ.

**Duration.** The 72 s figure is six 12-s samples: the time the fixed beam took to sweep across the source. Because the signal did not appear in the second horn, Ehman limits its actual duration to about 2.5 minutes or less.

**Never repeated.** Searches that found nothing:

- about 60 more days at the same declination at Big Ear;
- the VLA in 1995–96 (Gray & Marvel 2001);
- the 26 m Hobart telescope in 1999, with six 14-hour observations (Gray & Ellingsen 2002).

**Why it is not a pulsar.**

- Pulsars emit regular pulse trains across many frequencies and recur at the same sidereal time. The first pulsar, CP 1919, had pulses about 1.3 s apart.
- The Wow! signal was in a single channel, held a constant average within each sample, and never recurred.
- CP 1919's early nickname "LGM-1" ("Little Green Men") is the likely source of the mix-up.

**The frequency is disputed.** Published values, with their offsets from the hydrogen line at 1420.405751768 MHz:

| Source | Frequency | Offset from the hydrogen line |
|---|---|---|
| Kraus 1994 | 1420.3556 MHz | −50.2 kHz |
| Ehman 1998 | 1420.4556 ± 0.005 MHz | +49.8 kHz |
| Méndez et al. 2025 | 1420.726 ± 0.005 MHz | +320.2 kHz |

Méndez et al. 2025 also give a flux of 256 ± 63 Jy and a duration of 73.4 ± 0.5 s.

**(b) "It has been explained." Verdict: a proposal, not settled.**

- **Arecibo Wow! I** (Méndez, Ortiz Ceballos & Zuluaga, arXiv:2408.08513; submitted to ApJ, with no journal reference as of 17 Oct 2026). Archival Arecibo drift scans from 2020 show narrowband (about 10 kHz) hydrogen-line signals from small cold hydrogen clouds, about 100 times weaker than the Wow!.
  - The hypothesis: a strong transient source, such as a magnetar flare, suddenly brightened such a cloud through maser-like stimulated emission.
  - The authors say it "could be the first recorded event" of such a flare, so the mechanism itself has never been observed.
- **Arecibo Wow! II** (arXiv:2508.10657) revises the position, flux and frequency. It argues for an astrophysical origin rather than radio interference, but does not confirm the flare.
- **Earlier proposals.** A comet hypothesis (Paris 2017) is regarded as discredited.
- **Status.** The cause is unknown.

**(c) "Related to neutrinos." Verdict: false as stated.** No physical or published link exists.

- The signal was radio photons at the hydrogen 21-cm line (photon energy 5.874 µeV, wavelength 21.106 cm), produced by an electromagnetic spin-flip transition.
- Neutrinos carry no charge and interact only through the weak force and gravity, so a radio receiver cannot register them.
- None of the Wow! analyses mentions neutrinos.
- "Relativity" enters only through ordinary Doppler and reference-frame corrections to the line frequency.

Sources: [Ehman, Big Ear Wow! page](https://www.bigear.org/Wow30th/wow30th.htm), [Gray & Marvel 2001](https://doi.org/10.1086/318272), [Gray & Ellingsen 2002](https://doi.org/10.1086/342646), [Arecibo Wow! I](https://arxiv.org/abs/2408.08513), [Arecibo Wow! II](https://arxiv.org/abs/2508.10657), [Manchester, 50 years of pulsars](https://arxiv.org/abs/1801.04323), [Linda Hall Library, Jocelyn Bell Burnell](https://www.lindahall.org/about/news/scientist-of-the-day/jocelyn-bell-burnell), [NIST, hydrogen hyperfine frequency](https://tf.nist.gov/general/pdf/13.pdf), [T2K, neutrino detection](https://t2k-experiment.org/neutrinos/neutrino-detection/), [Wikipedia, Wow! signal](https://en.wikipedia.org/wiki/Wow!_signal).

---

## 3. The medicine

### 3.1 Trisomy 13, 18 and 21: DNA size versus gene dosage

**Verdict: partly true.** Life after birth is possible with these trisomies. But raw DNA size is the wrong variable: viability is better predicted by the number of extra dosage-sensitive genes (a rank ordering over about seven chromosomes, not a fitted statistic).

**Genome size.** A 46,XX genome is 6,062,084,834 bp from GRCh38.p14 chromosome lengths, or 6.11 Gb from T2T-CHM13. The often-quoted "about 6.2 Gb" is 2 × the GRCh38 total of 3.099 Gb, which includes unplaced scaffolds.

| Extra chromosome | Length, GRCh38 (Mb) | Extra DNA, % of 46,XX genome (GRCh38 / T2T) | Protein-coding genes (Ensembl 116) | Extra genes, % of 20,094 | Genes per Mb | Outcome |
|---|---|---|---|---|---|---|
| +21 | 46.7 | 0.77 / 0.74 | 221 | 1.10 | 4.73 | Liveborn. US median age at death 57 years in 2019 (IQR 49–61), up from 1 year in 1968 |
| +18 | 80.4 | 1.33 / 1.32 | 267 | 1.33 | 3.32 | Liveborn. Median survival 8–9 days; 1-year survival 12.6–13.4% |
| +13 | 114.4 | 1.89 / 1.86 | 322 | 1.60 | 2.82 | Liveborn. Median survival 5–12.5 days; 1-year survival 11.5–19.8% |
| +22 | 50.8 | 0.84 / 0.84 | 447 | 2.22 | 8.80 | Occasionally liveborn; survival usually days to weeks |
| +9 | 138.4 | 2.28 / 2.47 | 776 | 3.86 | 5.61 | Rare full-trisomy livebirths reported (noted by the verifier; not separately sourced here) |
| +16 | 90.3 | 1.49 / 1.58 | 856 | 4.26 | 9.48 | Commonest trisomy in recognised pregnancies (at least 1%); almost uniformly embryonic lethal |
| +X (47,XXX) | 156.0 | 2.57 / 2.52 | 867 (mostly silenced) | 4.31 | 5.56 | Usually mild; about 1 in 1,000 female births, only about 10% diagnosed |

**Survival with trisomy 18 and 13.** The two population cohorts give different results:

| Cohort | Median survival, T18 | Median survival, T13 | 1-year survival, T18 / T13 | Longer-term survival, T18 / T13 |
|---|---|---|---|---|
| Ontario 1991–2012 (Nelson 2016) | 9 days | 12.5 days | 12.6% / 19.8% | 10-year: 9.8% / 12.9% |
| 9 US states 1999–2007 (Meyer 2016) | 8 days | 5 days | 13.4% / 11.5% | 5-year: 12.3% / 9.7% |

The cohorts disagree on whether T13 or T18 does worse.

**The pattern.**

- **Fewest genes, not shortest chromosomes.** The three autosomes with the fewest protein-coding genes (21, 18, 13) are exactly the three whose full trisomies regularly survive to birth. The next-fewest is chromosome 22 (447 genes), whose full trisomy is occasionally liveborn.
- **Length does not predict it.** Chromosome 13 is only the 10th-shortest autosome. Chromosome 19 is shorter (58.6 Mb) but carries 1,479 genes.
- **Correction from the verifier.** Trisomies 13, 18 and 21 are the only full autosomal trisomies that *regularly* survive to birth. Full, non-mosaic trisomy 22 (and rarely trisomy 9) also occurs in liveborns, usually surviving days to weeks:
  - Tinkle et al. collected 23 cases, with median survival of 4 days;
  - Heinrich et al. 2013 reported a survivor to 29 days;
  - Phung et al. 2023 reported a survivor after cardiac surgery, and give a reported lifespan range of minutes to 3 years.
- **Counterexample: trisomy 16.** Chromosome 16 is shorter than chromosome 13 (length ratio 0.79) but has 2.66 times the genes. Its trisomy is the commonest in human pregnancy and is almost never compatible with development to term.
- **Counterexample: 47,XXX.** The extra X adds more DNA (156 Mb) than any viable autosomal trisomy, yet the condition is usually mild. The reason is X-inactivation:
  - more than 15% of X genes escape or variably escape inactivation (Balaton & Brown 2021);
  - 15% of 867 is about 130 genes with extra dosage, compared with 221 extra genes in trisomy 21.

The confidence in "gene count predicts viability" is medium: it is a strong correlation, not a full mechanism. Gene counts also depend on the annotation. NCBI Gene (queried 18 Oct 2026; [`../letters/ncbi_gene_counts.txt`](../letters/ncbi_gene_counts.txt)) gives chr21 254, chr18 277, chr13 354, chr22 478 and chr19 1,459, against Ensembl 116's 221, 267, 322, 447 and 1,479. Under both, 21, 18 and 13 are the three autosomes with the fewest genes, then 22, and chr19 has the highest gene density, so the pattern is unchanged.

Sources:
- Genome data: [NCBI GRCh38.p14](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001405.40/), [NCBI T2T-CHM13v2.0](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_009914755.1/), [Ensembl BioMart, release 116](https://www.ensembl.org/biomart/martview).
- Aneuploidy and trisomy 16: [Nagaoka et al. 2012](https://pubmed.ncbi.nlm.nih.gov/22705668/), [Hassold et al. 1995](https://pubmed.ncbi.nlm.nih.gov/7573048/), [Manor et al. 2021](https://doi.org/10.1002/ajmg.a.62368).
- Survival: [Iulita et al. 2022](https://doi.org/10.1001/jamanetworkopen.2022.12910), [Nelson et al. 2016](https://doi.org/10.1001/jama.2016.9819), [Meyer et al. 2016](https://doi.org/10.1002/ajmg.a.37495).
- Sex chromosomes: [Tartaglia et al. 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC2883963), [Balaton & Brown 2021](https://doi.org/10.1186/s13072-021-00404-9).
- Trisomy 22: [Heinrich et al. 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3569106), [Phung et al. 2023](https://bmcpediatr.biomedcentral.com/articles/10.1186/s12887-023-03949-8).

### 3.2 Trisomies and the strong force

Claim: "Consider the effect of gluon (strong force) on trisomies, genetic mutations, etc."

**Verdict: false as stated.** Trisomies arise from errors in chromosome segregation. That is biochemistry, driven by electromagnetic interactions. The strong force acts only inside atomic nuclei and is identical in every cell, whatever the karyotype.

**Where trisomies come from.**

- **Trisomy 21.** The extra chromosome is maternal in 95.3% of cases and paternal in 4.7% (Antonarakis 1991; 184 of 193 families).
- **Most aneuploidy** comes from errors in maternal meiosis I (Hassold 2007).
- **Trisomy 16.** All 62 cases studied were maternal, virtually all from meiosis I (Hassold 1995).

**How common it is** (Nagaoka et al. 2012):

- at least 10% of pregnancies are aneuploid, possibly more than 50% near the end of the reproductive lifespan;
- about 0.3% of newborns are aneuploid, against approximately 35% of spontaneous abortions.

The leading explanations for the maternal-age effect are loss of cohesin on oocyte chromosomes and altered crossover patterns.

**Scale of the strong force.**

| Quantity | Value |
|---|---|
| Range of the nuclear force, ħ/(m_π c) | 1.414 fm |
| Bohr radius / that range | 37,429 |
| Nuclear binding per nucleon in ¹²C | 7.680 MeV |
| That binding / hydrogen ionisation energy (13.6 eV) | 5.6e5 |

**Where gluons do matter.** About 99% of nucleon mass is strong-interaction energy ([1.4](#14-glucose-at-the-quark-level)). This is the same in every cell and has no bearing on karyotype.

**The only nuclear route to mutation is radiation from decay.** Even then, the DNA damage is done by electromagnetic ionisation. Data from RERF on the children of atomic-bomb survivors:

- there was no excess of stable structural chromosome aberrations: 18 of 8,322 (0.22%) in the exposed group against 25 of 7,976 (0.31%) in controls;
- each group had exactly one newly arisen aberration;
- caveats: aneuploidy was not this endpoint, and no child was examined before age 12.

Sources: [Antonarakis 1991](https://pubmed.ncbi.nlm.nih.gov/1825697/), [Hassold et al. 2007](https://pubmed.ncbi.nlm.nih.gov/17911163/), [Hassold et al. 1995](https://pubmed.ncbi.nlm.nih.gov/7573048/), [Nagaoka et al. 2012](https://pubmed.ncbi.nlm.nih.gov/22705668/), [PDG meson summary (π mass)](https://pdg.lbl.gov/2025/tables/rpp2025-sum-mesons.pdf), [CODATA Bohr radius](https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0), [CODATA neutron mass](https://physics.nist.gov/cgi-bin/cuu/Value?mnu), [RERF chromosome aberrations in F1](https://www.rerf.or.jp/en/programs/roadmap_e/health_effects-en/geneefx-en/chromeab).

### 3.3 The zinc spark at conception

**Verdict: true.** The zinc spark is a real, well-characterised event. It is ion chemistry (release of Zn²⁺ by exocytosis), not light emitted by the egg and not a particle-physics event.

- **What it is.** When the egg is activated it releases zinc into the surrounding medium in coordinated bursts that follow the calcium oscillations.
- **First report.** Kim et al. 2011 in *ACS Chemical Biology*, using mouse eggs; the spark is conserved in nonhuman primates.
- **Timing in mice.** The first sparks come about 20 minutes after fertilisation, with 1 to 5 rounds in the first 2 hours.
- **Before fertilisation.** In the final hours of maturation, a mouse oocyte takes up more than 20 billion zinc atoms: 33.2 fmol, or 2.17 pg (a lower bound).
- **Function.** The drop in intracellular zinc is needed to leave metaphase-II arrest; raising zinc again re-arrests the egg.
- **Human eggs (Duncan et al. 2016).**
  - Removing zinc with TPEN was enough on its own to restart the cell cycle.
  - No sperm were used. Eggs were activated with calcium ionophores or PLCζ cRNA.
  - Spark amplitude varied between eggs. The authors say this "suggests" quality differences but did not test it.
- **Embryo quality (mice only; Zhang et al. 2016).**
  - Selecting embryos by spark profile more than doubled the share that reached blastocyst.
  - Spark amplitude correlated with total cell number (R = 0.9209).
  - The claim that sparks predict quality in human IVF comes from press coverage, not from a human study.
- **It is not light.** The "spark" is the glow of a fluorescent zinc dye (FluoZin-3, 50 µM in the medium) that lights up when it binds released Zn²⁺. Calcium was tracked with Fluo-4.

Sources: [Kim et al. 2011](https://doi.org/10.1021/cb200084y), [NIH release](https://www.nih.gov/news-events/news-releases/zinc-sparks-fly-egg-within-minutes-fertilization), [Duncan et al. 2016](https://doi.org/10.1038/srep24737), [Zhang et al. 2016](https://doi.org/10.1038/srep22772), [CIAAW atomic weights](https://www.ciaaw.org/atomic-weights.htm), [CODATA N_A](https://physics.nist.gov/cgi-bin/cuu/Value?na).

### 3.4 Thyroid iodine and intelligence

**Verdict: partly true.** It is well established that iodine is needed for normal brain development and that deficiency lowers population IQ. The idea that iodine use drove the evolution of human intelligence is a contested hypothesis.

**Hormone chemistry.**

| Hormone | Formula | Iodine atoms | Molar mass | Iodine share of mass |
|---|---|---|---|---|
| T4 | C₁₅H₁₁I₄NO₄ | 4 | 776.874 g/mol | 65.3% |
| T3 | C₁₅H₁₂I₃NO₄ | 3 | 650.977 g/mol | 58.5% |

**Iodine is the heaviest required element.** Iodine (Z = 53) is the heaviest element with an established human dietary requirement; molybdenum (Z = 42) is next.

**Scale of deficiency.**

- Hetzel (2002) calls it "the most common preventable cause of brain damage", with about 2.2 billion people at risk.
- Zimmermann et al. (2008) call it "the most common cause of preventable mental impairment worldwide", with about 2 billion people with insufficient intake.
- A 1999 WHO Secretariat report to the World Health Assembly (A52/11, paragraph 2; the same sentence is in EB103/27, 1998) says that in 1990 the Assembly recognised iodine deficiency as "the world's greatest single cause of preventable mental retardation" (today's term is intellectual disability). The 1990 resolution itself, WHA43.2, does not contain that phrase. It set the goal of eliminating iodine deficiency disorders as a major public health problem by 2000.

**IQ effects.** The meta-analyses disagree on the size:

| Meta-analysis | Population | IQ effect | Note |
|---|---|---|---|
| Bleichrodt & Born 1994 | 18 studies, mostly observational | 13.5 points | not linked here |
| Qian et al. 2005 | 37 Chinese studies, 12,291 children | 12.45 points lower in severely deficient areas | 8.7 points recovered with iodine before or during pregnancy |
| Bougma et al. 2013 | children aged 5 and under | 6.9 to 10.2 points lower | weak study designs |

**Evolution.**

- Thyroid hormones are ancient. They are used across vertebrates and act in many invertebrates (Heyland & Moroz 2005), so iodine dependence long predates hominins.
- The "shore-based diet" hypothesis (Cunnane, Crawford) remains open:
  - Langdon 2006 calls its premise unsupported;
  - Carlson & Kingston 2007 argue that a terrestrial diet suffices;
  - Cunnane et al. 2007 rebut.

Sources: [ChEBI T4](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:18332), [ChEBI T3](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:18258), [Hetzel 2002](https://pubmed.ncbi.nlm.nih.gov/12077619/), [Zimmermann et al. 2008](https://doi.org/10.1016/S0140-6736(08)61005-3), [WHO, iodine deficiency](https://www.who.int/data/nutrition/nlis/info/iodine-deficiency), [WHO A52/11 (1999)](https://apps.who.int/gb/ebwha/pdf_files/WHA52/ew11.pdf), [WHA43.2 (1990)](https://iris.who.int/handle/10665/173510), [Qian et al. 2005](https://pubmed.ncbi.nlm.nih.gov/15734706/), [Bougma et al. 2013](https://doi.org/10.3390/nu5041384), [Heyland & Moroz 2005](https://doi.org/10.1242/jeb.01877), [Langdon 2006](https://doi.org/10.1079/bjn20061805), [Carlson & Kingston 2007](https://doi.org/10.1002/ajhb.20683), [Cunnane et al. 2007](https://doi.org/10.1002/ajhb.20673), [CIAAW atomic weights](https://www.ciaaw.org/atomic-weights.htm).

---

## 4. Outside physics

Section 4.3 is here for its end-of-life part. Its gravity link is testable, and it is false as stated.

### 4.1 The "trinity"

Physics has 3 generations of 4 fermion types ([1.3](#13-three-sets-of-four)). The number 3 is unexplained: CP violation needs at least 3 generations, and asymptotic freedom allows at most 8. Calling the 3 generations a "trinity" gives them a meaning that physics cannot test. It is outside physics.

### 4.2 Dark matter and the afterlife

**Verdict: outside physics.**

- Nothing in physics singles out death. A body's atoms persist and keep interacting electromagnetically before and after death. Protons do not decay on any relevant timescale: more than 1e34 years in the p → e⁺π⁰ mode.
- Dark matter passing through a body amounts to about 5e-23 kg at any instant, and it interacts so weakly that it scatters there less than once per ~650 years ([2.4](#24-dark-matter-outside-space-time)).
- A dark-matter link to the afterlife has no testable mechanism. Even the speculative extra-dimensional dark-sector models say nothing about death.

### 4.3 End-of-life memory and the perception of time

Claim: "During end-of-life care, memories are able to penetrate deeper into the subconscious mind ... my perception of time is affected by gravity in relation to bosons."

**Verdict: partly true. The end-of-life phenomena are real and documented. The link to gravity is false as stated (about 1e-16 per metre; no part in felt time).** "Penetrate deeper into the subconscious" is not a defined, measured construct, and "in relation to bosons" is too vague to test; those parts are outside physics.

**What is documented.**

- **End-of-life dreams and visions.** Kerr et al. 2014 enrolled 66 hospice inpatients and analysed 59. Most reported at least one dream or vision. Dreams of deceased people were more comforting and became more common as death approached. An 88% figure appears in a hospice article but was not checked against the paper's full text.
- **Terminal (paradoxical) lucidity.** Nahm et al. 2012 review case reports spanning 250 years. Mashour et al. 2019 say it would challenge current assumptions "if systematically confirmed". The evidence is anecdotal.
- **A gamma surge in the dying brain:**
  - Borjigin et al. 2013 (rats): a transient, coherent burst of gamma oscillations within 30 s of cardiac arrest, exceeding waking levels.
  - Xu et al. 2023: a gamma surge in 2 of 4 comatose patients after ventilation was withdrawn, driven by global hypoxia and including the posterior cortical "hot zone".
  - Vicente et al. 2022: increased gamma coupling in one 87-year-old with a subdural haematoma during cardiac arrest. This is a single case, and the brain injury is a confounder.
- **Felt time is constructed by the brain** (Wittmann 2013).
- **Fear-induced "slow motion" is a memory effect.** In Stetson et al. 2007, people in a 31 m free fall later judged their own fall 36% longer than others' falls, but their visual time resolution did not improve. The authors conclude: "time-slowing is a function of recollection, not perception".

**Gravity's part.** The gravitational effect at human scales is about 1e-16: about 470 ns between head and feet over 80 years ([1.7](#17-gravity-changes-how-fast-time-passes-for-the-body)). It plays no role. A testable version of the user's observation would be a neurophysiological hypothesis about richer memory encoding and recall near death.

Sources: [Kerr et al. 2014](https://doi.org/10.1089/jpm.2013.0371), [Hospice Buffalo article](https://hospicebuffalo.com/news/in-the-news/what-deathbed-visions-teach-us-about-living), [Nahm et al. 2012](https://doi.org/10.1016/j.archger.2011.06.031), [Mashour et al. 2019](https://doi.org/10.1016/j.jalz.2019.04.002), [Borjigin et al. 2013](https://doi.org/10.1073/pnas.1308285110), [Xu et al. 2023](https://doi.org/10.1073/pnas.2216268120), [Vicente et al. 2022](https://pubmed.ncbi.nlm.nih.gov/35273490/), [Wittmann 2013](https://pubmed.ncbi.nlm.nih.gov/23403747/), [Stetson et al. 2007](https://pubmed.ncbi.nlm.nih.gov/18074019/).

### 4.4 "The gravity of the situation"

**Verdict: a metaphor, but the history runs the other way.** Both meanings come from one root meaning "heavy". The seriousness sense came first, and physics borrowed the word from it.

- **Root.** Latin *gravitas* ("heaviness; dignity, seriousness") comes from *gravis* ("heavy, serious"), from the Proto-Indo-European root \*gʷreh₂- ("heavy"). Sanskrit *guru* ("weighty, venerable") shares the root.
- **The seriousness sense came first.** In English it dates from about 1500 (Etymonline), or 1509 (Merriam-Webster).
- **The physical sense came later.** The sense of downward tendency appears in the 1620s; Bacon's *Sylva Sylvarum* (1626/27) uses it.
- **Newton did not coin the word.** His *Principia* (1687) gave it the meaning of one universal attraction.
- **Timeline.** The seriousness sense is about 120 years older than the physical sense and about 180 years older than Newton's universal sense.

The idiom is about weight in the sense of load and consequence: the meaning the word had before physics. It does not show that gravitation and seriousness are the same thing.

Sources: [Etymonline, gravity](https://www.etymonline.com/word/gravity), [Etymonline, gravitation](https://www.etymonline.com/word/gravitation), [Merriam-Webster](https://www.merriam-webster.com/dictionary/gravity), [Wiktionary (cites the OED)](https://en.wiktionary.org/wiki/gravity), [Stanford, cultural history of gravity](https://einstein.stanford.edu/STEP/information/data/gravityhist2.html), [Rochester, Sylva Sylvarum](https://rbscp.lib.rochester.edu/3613), [Newton Project, Principia](https://newtonproject.ox.ac.uk/catalogue/record/THEM00094).

---

## What the verifier changed

The verifier recomputed every number and found no arithmetic errors. It made these corrections, all of which are applied above:

| Item | Original | Corrected |
|---|---|---|
| Liveborn trisomies | 13, 18 and 21 are "the only full autosomal trisomies seen in newborns" | They are the only ones that *regularly* survive to birth. Full trisomy 22 (and rarely 9) is occasionally liveborn |
| Navier-Stokes centre line | Fefferman's x = φ(t) read as a "moving line" | It is a moving point. A singular line is still excluded, because P¹(S) = 0 |
| Water O-O distance | 2.80 Å "at 37 °C" | 2.80(1) Å in ambient water. The weak range is 1.1e8–1.4e8 times smaller |
| Aneuploidy in miscarriages | "More than 35%" | Approximately 35% (Nagaoka) |
| ⁴⁰K gamma rays | About 500/s "escaping" | About 470–530/s *produced*; most escape |
| Dark-matter scatter bound | Reduced mass labelled μ_n | It is μ_p = 0.9168 GeV; the result is unchanged (< 1.53e-3/yr) |
| Higgs lifetime | 2.2e-22 s | 1.6e-22 s (SM width 4.1 MeV) to 2.2e-22 s (measured central width) |
| Standard Model parameters | 19 | 19 in the minimal SM; about 26–28 with neutrino masses |
| ⁴⁰K betas vs solar-neutrino interactions | 3.7e9 | About 3e9 (2.6e9–3.6e9, Borexino-scaled) |
| Dark matter outside space-time | False | Unsupported |
| Neutrinos and perception | False | Unsupported / physically implausible |

**Changed on 18 October 2026, after comparison with [`../letters/words.md`](../letters/words.md).** The gravity link in 4.3 (outside physics → false as stated); the Clay status in 2.1 (now from the primary sources); the Borexino row and the popular figures in 2.3 (now sourced); gene counts across annotations in 3.1; the WHO wording in 3.4; the brane example in 2.4; the rounding of the weak range in 2.1 (197.3269804 MeV fm / 80362.5 MeV = 2.45546e-3 fm, which `particle_cluster_output.txt` prints as 2.4555e-18 m). `physbio_factcheck_results.json` was not changed.

---

## Reproduction

The scripts, their outputs and the small data tables are in [`physics-biology/`](physics-biology/).

| File | What it computes | Needs |
|---|---|---|
| [`particle_cluster.py`](physics-biology/particle_cluster.py) | Higgs, W/Z, weak range, proton decay, 3 × 4 counting, spin-1/2, dark matter in the body (sections 1.1–1.3, 2.1, 2.2, 2.4) | numpy |
| [`glucose_weak.py`](physics-biology/glucose_weak.py) | Glucose counts and mass budget, RQ, respiratory water, ⁴⁰K/¹⁴C, ¹⁴C in DNA, solar neutrinos (1.4–1.6, 2.3) | standard library |
| [`gravity_time.py`](physics-biology/gravity_time.py) | Time dilation, Chou and Bothwell checks, potential wells, Wow! signal numbers (1.7, 2.5) | numpy |
| [`compute_bio.py`](physics-biology/compute_bio.py) | Zinc, iodine, chromosome lengths and gene counts, strong-force scales, genus, ENS, end-of-life numbers (1.8, 3.1–3.4, 4.3) | numpy; reads `data/` |
| [`verify/v1.py`](physics-biology/verify/v1.py) – [`v4.py`](physics-biology/verify/v4.py) | The adversarial verifier's independent recomputation. `verify/pubmed_ids.txt` lists the PubMed IDs whose abstracts it checked | numpy (v2), otherwise standard library |
| [`physbio_factcheck_results.json`](physics-biology/physbio_factcheck_results.json) | Machine-readable record of the four cluster reports and the verification (claims, verdicts, facts, numbers, sources, confidence, corrections) | — |

Each script has a matching `*_output.txt` next to it. To re-run:

```
cd physics-biology
python3 particle_cluster.py
python3 glucose_weak.py
python3 gravity_time.py
python3 compute_bio.py
python3 verify/v1.py   # likewise v2.py, v3.py, v4.py
```

**Re-run check.** On 18 Oct 2026, each script was re-run with `timeout 300 python3 -I` from an unrelated working directory. All exited cleanly and none needs network access.

- `particle_cluster.py`, `glucose_weak.py` and `gravity_time.py` reproduced their stored outputs byte for byte.
- `compute_bio.py` and `verify/v1.py`–`v4.py` had no stored output, so their outputs were saved from this run.
- `compute_bio.py` now reads `data/` relative to its own location. For this report it also prints chromosomes 22 and 9; that change only adds lines to its output.

**Data in [`physics-biology/data/`](physics-biology/data/).**

- `grch38_chr.json`, `chm13_chr.json`, `grch38_report.json`, `seqrep_test.json`: NCBI Datasets chromosome and assembly reports for GRCh38.p14 and T2T-CHM13v2.0. `seqrep_test.json` is a small test subset.
- `mart_all.tsv`: Ensembl 116 BioMart protein-coding genes with their chromosomes. `mart_pc.tsv` is an earlier partial export.
- `chebi_18332.json`, `chebi_18258.json`: ChEBI entries for T4 and T3.
- `nist/iso_K.txt`, `nist/iso_H.txt`: NIST isotopic-composition pages for potassium and hydrogen, saved as HTML.
- `ensdf/k40.txt`, `ensdf/c14.txt`: ENSDF adopted levels for ⁴⁰K and ¹⁴C, as text.

**Helper tools in [`physics-biology/tools/`](physics-biology/tools/).** These are not needed to reproduce the numbers.

- `epmc_search.py` searches Europe PMC. It **needs network access**.
- `epmc.py` downloads an article's full-text XML from Europe PMC to a file you name and prints keyword contexts. It **needs network access** and works only for articles with open full text there; it returned HTTP 500 for PMC3551553. Do not commit the files it writes.
- `kw.py` prints keyword contexts from a local text file and works offline.

**Not included.** During the check, the clusters and the verifier read the full text of PDG reviews, summary tables and listings, paper abstracts and full texts (for example Fefferman's problem statement, Chou et al. and Bothwell et al.) and other web pages. These are copyrighted text and were deleted. The values taken from them are written into the scripts with citations and are linked above. Some downloads had failed and contained no data, and were also deleted: a PubChem "server busy" response and two IAEA Cloudflare challenge pages saved as `.csv`.

**About the JSON record.** `physbio_factcheck_results.json` is the record as produced *before* the verifier's corrections were applied; the corrections themselves are stored in its `verification` block. Where it differs from this report, this report is the corrected version. Its script paths were rewritten as paths relative to the file; nothing else in it was changed.
