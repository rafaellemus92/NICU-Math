# The words that drew me in

These notes go with the email to Steven Strogatz (`strogatz-email.md`). They are for a later reply,
if he writes back, and for anyone reading this repository.

- Part 1 lines up words used at the bedside, in the mathematics and in old texts.
- Part 2 checks a set of physics ideas against what physics says.
- Parts 3 to 5 are short essays.

Numbers in square brackets point to the source list at the end. A few numbers are worked out here
rather than taken from a source. They come from `check_numbers.py`, and its output is saved in
`check_numbers.txt`.

**Status words used below**

- **True**: established, with a source.
- **Open**: not known, or not settled.
- **Analogy**: a likeness, not a mechanism.
- **Doesn't hold**: physics says otherwise.

## 1. Shared vocabulary

The columns sit side by side because the same word is used in each. The links across columns are
analogies, not evidence.

| Word | At the bedside | In the mathematics | In the old words |
|---|---|---|---|
| Breath | first and last breath | an oscillation born (one standard route is a Hopf bifurcation) or stopped | hevel (Eccl), ruach, neshamah (Gen 2:7), pneuma (John 3:8); inspire/expire |
| Loop | pressure-volume loop (enclosed area = energy lost per breath); the circulation re-routes at birth | limit cycle; winding number; Winfree's 1 vs 0 | "the wind returneth again according to his circuits" (Eccl 1:6) |
| Turbulence | /s/, /sh/, /f/ | high Reynolds number; energy cascading to small scales | storm, then "a great calm" (Mark 4:39); "a still small voice" (1 Kgs 19:12) |
| Blow-up | - | something becomes infinite; the equation stops working | "incorruptible" (1 Cor 15:52), as metaphor |
| Harmony | vowels, /m/ | Fourier harmonics | - |
| Attunement | mom's responsiveness | coupling strength with delay; too much can trap the pair | - |
| Salience | what mom notices | which inputs get weight (gated coupling) | - |
| Light | phototherapy; the circadian clock | periodic forcing; phase response curve | - |
| One and many | an N-of-1 trial | individual cells vs the synchrony index R | - |

### Where each row comes from

- **Breath.** A fetus already breathes in bursts, so birth switches breathing from intermittent to
  continuous. It does not switch it from rest to rhythm [1, 2]. A Hopf bifurcation is one standard
  way an oscillation is born, not the only one [3]. Hevel means breath or vapor [4]. Ruach is wind,
  breath and spirit. Neshamah is "the breath of life" in Genesis 2:7. In John 3:8, pneuma means both
  wind and Spirit [5]. Inspire, respire and expire are Latin breath words [6]. In English, "expire"
  meant "die" before it meant "breathe out" [7].
- **Loop.** The area inside the pressure-volume loop is the mechanical energy lost in one breath [8].
  Oliveira and colleagues tie it to the entropy produced per breath: ΔS = ΔA/T [9]. At birth, lung
  aeration raises blood flow through the lungs, and the circulation changes from parallel to series
  [10]. A limit cycle is an isolated closed orbit [3]. Winfree's argument counts windings. Weak stimuli
  give a resetting curve of degree 1 and strong ones degree 0. Because a whole number cannot change
  smoothly, some stimulus in between leaves the phase undefined [11, 12]. The verse is Ecclesiastes 1:6
  in the King James Version. Its Hebrew reads literally "turning, turning goes the wind" [5].
- **Turbulence.** Fricatives get their noise from turbulent airflow at a narrow gap [13]. In /s/ and
  /sh/ the jet hits the teeth, which makes them loud [14]. /f/ is a weaker fricative made at the
  lip-teeth gap [15]. In the 3-D Navier-Stokes equations, the nonlinear term pushes energy to finer
  and finer scales while viscosity drains it [16]. The storm-and-calm passages are Mark 4:37-39 and
  1 Kings 19:11-12 [5]. (Tohu, in Genesis 1:2, means emptiness, not turbulence [5].)
- **Blow-up.** The Clay Millennium Problem asks whether smooth solutions of the 3-D Navier-Stokes
  equations stay smooth forever or can blow up in finite time [17]. In September 2026 OpenAI announced
  a proof of blow-up for the version with an outside force. Clay's statement speaks of "the
  announcement that the Navier-Stokes problem has apparently been settled" and calls its prize
  process "deliberately unhurried". Whether a fluid with no outside force can blow up is still
  **open** [18]. "Incorruptible" translates aphthartos, "not subject to decay". Using it for blow-up
  is a metaphor [5].
- **Harmony.** Vowels and /m/ are nearly periodic voiced sounds, shaped by the resonances of the vocal
  tract [19]. The harmonics-to-noise ratio measures how periodic a sustained vowel is [20].
- **Attunement.** This is the model's result, not a published finding. In the Shared Air model, past a
  saddle-node bifurcation the pair can get stuck with both partners aroused [21].
- **Salience.** This is a modeling proposal. No source makes the claim.
- **Light.** Phototherapy is photochemistry. Light turns bilirubin into forms the body can excrete
  [22]. It does not entrain anything. The circadian clock is set through retinal ganglion cells that
  contain melanopsin [23]. The current Cochrane review finds the evidence on cycled light in the NICU
  very uncertain [24]. In fruit flies, Winfree found that a light pulse of critical strength, at a
  critical phase, essentially stopped the circadian clock [11]. That is the bridge from light to the
  phase singularity.
- **One and many.** An N-of-1 trial is a randomized, repeated crossover within one patient [25]. The
  synchrony index R has no closed equation of its own. How R changes depends on a second summary of
  how the phases are spread (the second moment, Z₂), not on R alone [21, 26, 27]. At the bedside we
  see beat times, not R.

## 2. Ideas and their status

The first column gives each idea as you put it. The second says what physics says.

| Your idea | What physics says | Status | Sources |
|---|---|---|---|
| "3 sets of 4" particles | The 12 matter particles form three generations of four: an up-type quark, a down-type quark, a charged lepton and a neutrino. The Z boson's decay width counts the kinds of light neutrino: 2.9840 ± 0.0082, so three. That means three generations, unless a fourth has a very heavy neutrino. Why there are three is unknown. | **True.** Why three: **open**. The "trinity" is your reading: **analogy**. | [28, 29] |
| W, Z and gluon as one force | The W, Z and photon come from one electroweak force at high energy (Glashow, Salam and Weinberg; Nobel Prize 1979). The W and Z were found at CERN in 1983. Adding the gluon is grand unification, proposed in 1974. Its signature prediction, proton decay, has never been seen. For the decay p → e⁺π⁰, Super-Kamiokande puts the proton's lifetime above 2.4 × 10³⁴ years. | Electroweak: **true**. Grand unification: **open**. | [30, 31, 32, 33] |
| "The gravity of the situation" | In English, "gravity" meant seriousness or dignity from about 1500. The physical sense came in the 1620s. Both come from Latin *gravis*, heavy. Gravity does slow time: a clock 1 m higher runs faster by about 1.1 × 10⁻¹⁶. Optical clocks measured the effect over a 33 cm height in 2010. Over 80 years it adds up to about 0.3 microseconds per metre of height. | The word history: **true**. Gravity slowing time: **true**. As the reason serious moments feel heavy: **doesn't hold**. | [34, 35], `check_numbers.txt` |
| End-of-life memories going deeper | Time perception happens in the brain. After a 31 m free fall, people judged their own fall 36% longer than other people's falls. They could not see any faster during the fall. The authors propose that fear lays down richer memories, which seem longer afterward. "Paradoxical lucidity", a sudden return of clarity near death in severe dementia, has been reported, mostly in single case reports. Its mechanism is unknown. | Fear and remembered time: **true**. The mechanism of lucidity: **open**. A link to gravity: **doesn't hold**. | [36, 37] |
| Higgs massless at the center of Navier-Stokes | The Higgs boson has mass, about 125 GeV. The photon and the gluon are massless. The Navier-Stokes equations treat a fluid as a continuum, with no particles in it. | **Doesn't hold.** | [28, 17] |
| Gluons and trisomies | Gluons act inside protons and neutrons; a proton's radius is 0.84 × 10⁻¹⁵ m. A trisomy is an error in separating chromosomes, usually in the egg. The cohesion that holds paired chromosomes together weakens as the mother ages. That is cell biology, driven by electromagnetic chemistry, far above the gluon's scale. | **Doesn't hold.** | [28, 38, 39] |
| Weak force inside us | An adult body holds about 140 g of potassium. Its potassium-40 gives roughly 4,000 to 4,300 decays per second, depending on the potassium content and half-life assumed. Every decay is a weak-force event (about 89% beta decay, 11% electron capture). The radiation can damage DNA. Most DNA damage, though, comes from the cell's own chemistry: hydrolysis, oxidation and methylation. | **True.** | [40, 41, 42], `check_numbers.txt` |
| Neutrinos and perception | About 6.5 × 10¹⁰ solar neutrinos cross each square centimetre of you every second, and almost all pass straight through. Scaling the Borexino detector's measured rates to the electrons in a 70 kg body gives about 50 collisions a year, a few thousand in a lifetime. That is my rough estimate; popular accounts often say "one or two in a lifetime". Even my higher figure is about 3 billion times fewer events than the body's own potassium-40 decays. Events that rare cannot plausibly shape perception. | **Doesn't hold.** | [43, 44, 45], `check_numbers.txt` |
| Wow! and pulsars | Ohio State's Big Ear telescope picked up the Wow! signal on 15 August 1977. It was a strong, narrowband signal near the 1420 MHz hydrogen line. It lasted the full 72 s that the telescope could watch any one point of sky, and it has never been seen again. A pulsar repeats; Wow! did not. A 2024 preprint proposes a natural cause: a cold hydrogen cloud briefly brightened by a flare, perhaps from a magnetar. A 2025 follow-up revised the frequency to 1420.726 MHz. Both were still preprints when I checked (October 2026). Pulsars, first reported in 1968, are cosmic clocks: their pulses arrive with very regular timing. | **Doesn't hold**: they are separate things. The cause of Wow!: **open**. | [46, 47, 48, 49] |
| Dark matter outside spacetime | Dark matter is known only through its gravity: how galaxies rotate, how light bends, the pattern in the cosmic microwave background. In general relativity anything with gravity curves spacetime, so dark matter sits inside spacetime. No non-gravitational signal has been confirmed. The LZ experiment (2025) found no excess over its expected background. | **Doesn't hold.** What dark matter is: **open**. | [50, 51] |
| Zinc spark | At fertilization, mouse eggs release bursts of zinc, called zinc sparks (2011). Human eggs do the same when they are activated in the lab (2016). This is chemistry: zinc ions leaving the cell. | **True.** | [52, 53] |
| Iodine and intelligence | In 1990 the World Health Assembly recognized iodine deficiency as "the world's greatest single cause of preventable mental retardation" (today's term is intellectual disability). Thyroid hormone contains iodine. Newborns are screened for congenital hypothyroidism because, untreated, it causes intellectual disability. The idea that iodine-rich shore foods helped the human brain evolve is a hypothesis. | **True.** The evolutionary role: **open**. | [54, 55, 56] |
| Trisomies 13, 18, 21 | The only full autosomal trisomies that regularly survive to birth are 13, 18 and 21. Size is not the pattern: chromosome 21 is the smallest (46.7 Mb), but 18 is 80.4 Mb and 13 is 114.4 Mb. What they share is few genes: about 254 (21), 277 (18) and 354 (13) protein-coding genes. Chromosome 19 is small (58.6 Mb) but carries about 1,459 genes, the highest gene density of any human chromosome. Trisomy 19 is not seen at birth. A review puts the survival of 13, 18 and 21 down to their low gene numbers, with a "probably". | **True.** It is a lesson about gene dosage. | [38, 57, 58, 59, 60] |
| Body as torus, gut as second brain | Count only the gut, a tube from mouth to anus, and the body is topologically a torus. The nose and airway join the same tube, which adds exits and makes the honest count harder. The enteric nervous system has about 200 to 600 million neurons. In the small intestine and colon it has full reflex circuits that control muscle activity, fluid movement and local blood flow. "The Second Brain" is the title of Gershon's 1998 book. | Torus: **true** as a first approximation. "Second brain": **analogy**. | [61, 62, 63] |
| Dirac equation | Dirac's 1928 equation describes spin-1/2 particles such as the electron. It led him to predict an anti-electron in 1931. Anderson found it, the positron, in 1932. A spin-1/2 particle must turn 720 degrees, not 360, to come back to its starting state. Neutron experiments confirmed this in 1975. Nothing in the theory makes the electron a torus. The 720-degree turn is the real geometric surprise. | 720 degrees: **true**. A torus: **doesn't hold**. | [64, 65, 66, 67] |

## 3. Glucose, quark by quark

One glucose molecule, C₆H₁₂O₆ built from the common isotopes, has 96 protons and 84 neutrons. That
is 276 up quarks and 264 down quarks (`check_numbers.txt`).

- **About 1% is quark mass.** The quarks' rest masses, which come from the Higgs field, add up to
  about 1.1% of the molecule's mass [28]. Light-quark masses depend on how they are defined, so
  "about 1%" is the honest figure.
- **0.03% is electrons.** Their mass also comes from the Higgs field.
- **About 99% is energy (E = mc²).** It is the energy of the quarks moving, and of the gluon fields
  that bind them, inside each proton and neutron. Lattice calculations split it among quark motion,
  gluon-field energy and a purely quantum term [68]. "The energy of the gluon field" alone is a
  simplification.

Burning glucose releases about 29 eV per molecule [69]. Metabolism, which takes glucose all the way
to carbon dioxide and water, releases the same total by a slower route. All of that energy comes from
rearranging electrons between atoms. The nuclear binding energy inside the same molecule is about
1,319 MeV [70]. That is about 45 million times larger, and metabolism never touches it.

At each level new properties appear, and they need laws of their own. Knowing the level below does
not let you simply read them off. That is Philip Anderson's point in "More Is Different" (1972)
[71]. The aggregation results in the Shared Air audit teach the same lesson [21]. Lumping cells into one compartment misstates the water flux, and the
average synchrony R alone does not say what happens next. Choose the right level and the right
variables. The link from quarks to cells to a mother and infant is an **analogy**. The physics at
each level is real.

## 4. Metaphors with real physics behind them

These are metaphors. The physics inside each one is real. The bridge from the physics to a life is
not a physics claim.

- **Cooper pairs.** In a superconductor, two electrons, which are fermions, bind weakly by
  exchanging phonons, the quanta of vibration in the crystal [72]. A phonon is, in effect, a quantum
  of sound. Each pair behaves roughly like a boson, so many pairs can share one quantum state, and
  then current flows with zero resistance (Bardeen, Cooper and Schrieffer, 1957) [73]. The boson
  picture is approximate, because the pairs overlap heavily.
- **The weak force.** It is the only force that changes what a particle is: a neutron into a proton,
  or a proton into a neutron. The Sun's first fusion step, p + p → d + e⁺ + ν, needs it. That step is
  so slow that its rate cannot be measured in a laboratory and has to be calculated [74]. Its slowness
  is a large part of why the Sun burns steadily for billions of years instead of all at once.
- **Caffarelli, Kohn and Nirenberg (1982).** For "suitable" weak solutions of the Navier-Stokes
  equations, the set of space-time points where the solution could break down has zero
  one-dimensional (parabolic) Hausdorff measure [75]. In plain words: if the equation ever breaks
  down, the breakdown set is smaller than any curve in space-time. The theorem limits how large a
  breakdown set can be. It does not say whether one exists.

## 5. The leak, and after t = death

**The leak.** Breathing is open: oxygen comes in and carbon dioxide goes out. The pressure-volume
loop measures something else. Its enclosed area is the mechanical energy lost in each breath [8].
Oliveira and colleagues tie that area to the entropy produced per breath, ΔS = ΔA/T [9]. A loop that
enclosed no area would lose no energy. "A perfectly closed loop exchanges nothing; the leak is where
living happens" is a **metaphor**. It joins two different real things: gas exchange, and the energy
each breath dissipates.

**After t = death.** The closest real physics is the black-hole information paradox. In 1976 Hawking
argued that black holes destroy information [76]. In 1993 Page worked out what the radiation would
look like if the information survives, now called the Page curve [77]. In 2019, calculations in
simplified models of gravity reproduced the Page curve, using regions now called "islands"
[78, 79, 80], reviewed in [81]. Many theorists read these results as evidence that information is
preserved. The full mechanism is still **open**. And that is information about particles, not about a person. No
measurement reaches past death. That is where faith speaks and physics is silent.

## Sources

1. Dawes GS, Fox HE, Leduc BM, Liggins GC, Richards RT. Respiratory movements and rapid eye movement sleep in the foetal lamb. *J Physiol.* 1972;220(1):119-143. doi:10.1113/jphysiol.1972.sp009698
2. Patrick J, Campbell K, Carmichael L, Natale R, Richardson B. Patterns of human fetal breathing during the last 10 weeks of pregnancy. *Obstet Gynecol.* 1980;56(1):24-30. PMID 7383483
3. Strogatz SH. *Nonlinear Dynamics and Chaos.* 2nd ed. Boulder, CO: Westview Press; 2015. Sections 7.0 (limit cycles), 8.2 (Hopf bifurcations), 8.4 (global bifurcations of cycles).
4. Brown F, Driver SR, Briggs CA. *A Hebrew and English Lexicon of the Old Testament* (BDB), entry הֶבֶל, Strong's H1892: "vapour, breath; figurative vanity". https://biblehub.com/hebrew/1892.htm. NET Bible, translators' note on Ecclesiastes 1:2.
5. Bible passages in the King James Version, with Hebrew and Greek words from the Bible Hub interlinear and lexicons (BDB, Strong's, Thayer): Genesis 1:2 and 2:7; Ecclesiastes 1:6; 1 Kings 19:11-12; Mark 4:37-39; John 3:8; 1 Corinthians 15:52. https://biblehub.com/interlinear/
6. Lewis CT, Short C. *A Latin Dictionary* (1879), entries spiritus, spiro, inspiro, respiro, exspiro. Perseus Digital Library. https://www.perseus.tufts.edu/hopper/
7. Harper D. Online Etymology Dictionary, "expire". https://www.etymonline.com/word/expire
8. Mead J, Whittenberger JL, Radford EP. Surface tension as a factor in pulmonary volume-pressure hysteresis. *J Appl Physiol.* 1957;10(2):191-196. doi:10.1152/jappl.1957.10.2.191
9. Oliveira CLN, Araújo AD, Bates JHT, Andrade JS, Suki B. Entropy production and the pressure-volume curve of the lung. *Front Physiol.* 2016;7:73. doi:10.3389/fphys.2016.00073
10. Hillman NH, Kallapur SG, Jobe AH. Physiology of transition from intrauterine to extrauterine life. *Clin Perinatol.* 2012;39(4):769-783. doi:10.1016/j.clp.2012.09.009. Hooper SB, et al. Cardiovascular transition at birth: a physiological sequence. *Pediatr Res.* 2015;77(5):608-614. doi:10.1038/pr.2015.21
11. Winfree AT. *The Geometry of Biological Time.* New York: Springer; 1980. 2nd ed. 2001. doi:10.1007/978-1-4757-3484-3
12. Glass L, Winfree AT. Discontinuities in phase-resetting experiments. *Am J Physiol.* 1984;246(2 Pt 2):R251-R258. doi:10.1152/ajpregu.1984.246.2.R251
13. Stevens KN. Airflow and turbulence noise for fricative and stop consonants: static considerations. *J Acoust Soc Am.* 1971;50(4B):1180-1192. doi:10.1121/1.1912751
14. Shadle CH. The effect of geometry on source mechanisms of fricative consonants. *J Phonetics.* 1991;19(3-4):409-424. doi:10.1016/S0095-4470(19)30332-8
15. Jongman A, Wayland R, Wong S. Acoustic characteristics of English fricatives. *J Acoust Soc Am.* 2000;108(3):1252-1263. doi:10.1121/1.1288413
16. Tao T. Why global regularity for Navier-Stokes is hard. *What's new* (blog), 18 March 2007. https://terrytao.wordpress.com/2007/03/18/why-global-regularity-for-navier-stokes-is-hard/
17. Fefferman CL. Existence and smoothness of the Navier-Stokes equation. Clay Mathematics Institute, official problem description. https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf
18. Quanta Magazine. AI has solved one of math's $1 million Millennium Prize problems. 8 September 2026. https://www.quantamagazine.org/ai-has-solved-one-of-maths-1-million-millennium-prize-problems-20260908/. Clay Mathematics Institute. Navier-Stokes announcement, 11 September 2026. https://www.claymath.org/news/navier-stokes-announcement/. Howlett J. Did OpenAI solve the wrong Navier-Stokes problem? *Scientific American*, 21 September 2026. https://www.scientificamerican.com/article/did-openai-solve-the-wrong-navier-stokes-problem/
19. Fant G. *Acoustic Theory of Speech Production.* The Hague: Mouton; 1960.
20. Yumoto E, Gould WJ, Baer T. Harmonics-to-noise ratio as an index of the degree of hoarseness. *J Acoust Soc Am.* 1982;71(6):1544-1550. doi:10.1121/1.387808
21. Shared Air audit, this repository: `../shared-air/AUDIT.md`. Section 4 (the saddle-node and the stuck aroused state), item C8 (water aggregation identity), item C10 (phase-moment counterexample).
22. Maisels MJ, McDonagh AF. Phototherapy for neonatal jaundice. *N Engl J Med.* 2008;358(9):920-928. doi:10.1056/NEJMct0708376
23. Berson DM, Dunn FA, Takao M. Phototransduction by retinal ganglion cells that set the circadian clock. *Science.* 2002;295(5557):1070-1073. doi:10.1126/science.1067262. Hattar S, Liao HW, Takao M, Berson DM, Yau KW. Melanopsin-containing retinal ganglion cells: architecture, projections, and intrinsic photosensitivity. *Science.* 2002;295(5557):1065-1070. doi:10.1126/science.1069609
24. Morag I, Xiao YT, Bruschettini M. Cycled light in the intensive care unit for preterm and low birth weight infants. *Cochrane Database Syst Rev.* 2024;(12):CD006982. doi:10.1002/14651858.CD006982.pub5
25. Guyatt G, Sackett D, Taylor DW, Chong J, Roberts R, Pugsley S. Determining optimal therapy: randomized trials in individual patients. *N Engl J Med.* 1986;314(14):889-892. doi:10.1056/NEJM198604033141406
26. Ott E, Antonsen TM. Low dimensional behavior of large systems of globally coupled oscillators. *Chaos.* 2008;18(3):037113. doi:10.1063/1.2930766
27. Marvel SA, Mirollo RE, Strogatz SH. Identical phase oscillators with global sinusoidal coupling evolve by Möbius group action. *Chaos.* 2009;19(4):043104. doi:10.1063/1.3247089
28. Navas S, et al. (Particle Data Group). Review of Particle Physics. *Phys Rev D.* 2024;110:030001, and 2025 update. Summary tables used: gauge and Higgs bosons (Higgs 125.20 ± 0.11 GeV; W 80.3692 GeV; Z 91.1880 GeV; photon and gluon massless), quarks (u 2.16 MeV, d 4.70 MeV), baryons (proton charge radius 0.8409 fm).
29. ALEPH, DELPHI, L3, OPAL and SLD Collaborations; LEP Electroweak Working Group; SLD Electroweak and Heavy Flavour Groups. Precision electroweak measurements on the Z resonance. *Phys Rep.* 2006;427(5-6):257-454. doi:10.1016/j.physrep.2005.12.006
30. The Nobel Prize in Physics 1979: Sheldon Glashow, Abdus Salam, Steven Weinberg, "for their contributions to the theory of the unified weak and electromagnetic interaction between elementary particles, including, inter alia, the prediction of the weak neutral current". https://www.nobelprize.org/prizes/physics/1979/summary/
31. The Nobel Prize in Physics 1984: Carlo Rubbia, Simon van der Meer, for the project that led to the discovery of the W and Z particles (announced at CERN in January and May 1983). Press release: https://www.nobelprize.org/prizes/physics/1984/press-release/
32. Georgi H, Glashow SL. Unity of all elementary-particle forces. *Phys Rev Lett.* 1974;32(8):438-441. doi:10.1103/PhysRevLett.32.438
33. Takenaka A, et al. (Super-Kamiokande Collaboration). Search for proton decay via p → e⁺π⁰ and p → μ⁺π⁰ with an enlarged fiducial volume in Super-Kamiokande I-IV. *Phys Rev D.* 2020;102:112011. doi:10.1103/PhysRevD.102.112011
34. Harper D. Online Etymology Dictionary, "gravity": "c. 1500, 'weight, dignity, seriousness...'"; the scientific sense is "first recorded 1620s". https://www.etymonline.com/word/gravity
35. Chou CW, Hume DB, Rosenband T, Wineland DJ. Optical clocks and relativity. *Science.* 2010;329(5999):1630-1633. doi:10.1126/science.1192720. NIST's summary gives about 90 billionths of a second over 79 years for the 33 cm height difference.
36. Stetson C, Fiesta MP, Eagleman DM. Does time really slow down during a frightening event? *PLoS ONE.* 2007;2(12):e1295. doi:10.1371/journal.pone.0001295
37. Mashour GA, Frank L, Batthyany A, et al. Paradoxical lucidity: a potential paradigm shift for the neurobiology and treatment of severe dementias. *Alzheimers Dement.* 2019;15(8):1107-1114. doi:10.1016/j.jalz.2019.04.002
38. Nagaoka SI, Hassold TJ, Hunt PA. Human aneuploidy: mechanisms and new insights into an age-old problem. *Nat Rev Genet.* 2012;13(7):493-504. doi:10.1038/nrg3245. Table 1: the aneuploidies seen in newborns are +13, +18, +21 and sex-chromosome changes; most trisomies are maternal in origin.
39. Chiang T, Duncan FE, Schindler K, Schultz RM, Lampson MA. Evidence that weakened centromere cohesion is a leading cause of age-related aneuploidy in oocytes. *Curr Biol.* 2010;20(17):1522-1528. doi:10.1016/j.cub.2010.06.069
40. Wikipedia, "Potassium-40" (accessed 18 October 2026): a 70 kg body holds about 140 g of potassium, giving about 3,850 to 4,300 decays per second; half-life 1.248 × 10⁹ years. `check_numbers.txt` gives 4,250 to 4,340 per second for 140 g, using the half-lives in [40] and [41].
41. Fiorentini G, Lissia M, Mantovani F. Geo-neutrinos and Earth's interior. *Phys Rep.* 2007;453:117-172. doi:10.1016/j.physrep.2007.09.001. Potassium-40: 89.3% decay to calcium-40, 10.7% to argon-40 (electron capture); half-life 1.277 × 10⁹ years.
42. Lindahl T. Instability and decay of the primary structure of DNA. *Nature.* 1993;362(6422):709-715. doi:10.1038/362709a0
43. Bellerive A. Review of solar neutrino experiments. *Int J Mod Phys A.* 2004;19:1167-1179. doi:10.1142/S0217751X04019093. Total solar neutrino flux at Earth: 6.5 × 10¹⁰ per cm² per second.
44. Agostini M, et al. (Borexino Collaboration). Simultaneous precision spectroscopy of pp, ⁷Be, and pep solar neutrinos with Borexino Phase-II. *Phys Rev D.* 2019;100:082004. doi:10.1103/PhysRevD.100.082004. Rates: pp 134, ⁷Be 48.3, pep 2.43 counts per day per 100 t.
45. Borexino Collaboration. Final results of Borexino on CNO solar neutrinos. *Phys Rev D.* 2023;108:102005. doi:10.1103/PhysRevD.108.102005. Electron density (3.307 ± 0.015) × 10³¹ per 100 t.
46. Wikipedia, "Wow! signal" (accessed 18 October 2026): detected 15 August 1977 by Big Ear; the full 72-second observing window; Ehman's 1998 frequency 1420.4556 MHz.
47. Méndez A, Ortiz Ceballos K, Zuluaga JI. Arecibo Wow! I: an astrophysical explanation for the Wow! signal. arXiv:2408.08513 (2024, preprint).
48. Méndez A, Ortiz Ceballos KN, Zuluaga JI, et al. Arecibo Wow! II: revised properties of the Wow! signal from archival Ohio SETI data. arXiv:2508.10657 (2025, preprint).
49. Hewish A, Bell SJ, Pilkington JDH, Scott PF, Collins RA. Observation of a rapidly pulsating radio source. *Nature.* 1968;217(5130):709-713. doi:10.1038/217709a0
50. Bertone G, Hooper D. History of dark matter. *Rev Mod Phys.* 2018;90(4):045002. doi:10.1103/RevModPhys.90.045002
51. Aalbers J, et al. (LZ Collaboration). Dark matter search results from 4.2 tonne-years of exposure of the LUX-ZEPLIN (LZ) experiment. *Phys Rev Lett.* 2025;135:011802. doi:10.1103/4dyc-z8zf
52. Kim AM, Bernhardt ML, Kong BY, Ahn RW, Vogt S, Woodruff TK, O'Halloran TV. Zinc sparks are triggered by fertilization and facilitate cell cycle resumption in mammalian eggs. *ACS Chem Biol.* 2011;6(7):716-723. doi:10.1021/cb200084y
53. Duncan FE, Que EL, Zhang N, Feinberg EC, O'Halloran TV, Woodruff TK. The zinc spark is an inorganic signature of human egg activation. *Sci Rep.* 2016;6:24737. doi:10.1038/srep24737
54. World Health Organization. Prevention and control of iodine deficiency disorders. Report by the Secretariat, Fifty-second World Health Assembly, document A52/11, 13 April 1999, paragraph 2. https://apps.who.int/gb/ebwha/pdf_files/WHA52/ew11.pdf
55. Rose SR, Wassner AJ, Wintergerst KA, et al. Congenital hypothyroidism: screening and management. *Pediatrics.* 2023;151(1):e2022060420. doi:10.1542/peds.2022-060420
56. Cunnane SC. *Survival of the Fattest: The Key to Human Brain Evolution.* Hackensack, NJ: World Scientific; 2005.
57. UCSC Genome Browser, human assembly hg38 (GRCh38), chromosome sizes. https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes
58. NCBI Gene, protein-coding human genes per chromosome, queried 18 October 2026 with `<n>[chr] AND "Homo sapiens"[orgn] AND "genetype protein coding"[Properties] AND alive[prop]`.
59. Grimwood J, Gordon LA, Olsen A, et al. The DNA sequence and biology of human chromosome 19. *Nature.* 2004;428(6982):529-535. doi:10.1038/nature02399
60. Rice AM, McLysaght A. Dosage-sensitive genes in evolution and disease. *BMC Biol.* 2017;15:78. doi:10.1186/s12915-017-0418-y
61. Ratcliffe A. The human mug. *Chalkdust* (2025). https://chalkdustmagazine.com/features/the-human-mug/
62. Furness JB, Callaghan BP, Rivera LR, Cho HJ. The enteric nervous system and gastrointestinal innervation: integrated local and central control. *Adv Exp Med Biol.* 2014;817:39-71. doi:10.1007/978-1-4939-0897-4_3
63. Gershon MD. *The Second Brain.* New York: HarperCollins; 1998.
64. Dirac PAM. The quantum theory of the electron. *Proc R Soc Lond A.* 1928;117(778):610-624. doi:10.1098/rspa.1928.0023
65. Dirac PAM. Quantised singularities in the electromagnetic field. *Proc R Soc Lond A.* 1931;133(821):60-72. doi:10.1098/rspa.1931.0130
66. Anderson CD. The apparent existence of easily deflectable positives. *Science.* 1932;76(1967):238-239. doi:10.1126/science.76.1967.238. Anderson CD. The positive electron. *Phys Rev.* 1933;43(6):491-494. doi:10.1103/PhysRev.43.491
67. Rauch H, Zeilinger A, Badurek G, Wilfing A, Bauspiess W, Bonse U. Verification of coherent spinor rotation of fermions. *Phys Lett A.* 1975;54(6):425-427. doi:10.1016/0375-9601(75)90798-7. Werner SA, Colella R, Overhauser AW, Eagen CF. Observation of the phase shift of a neutron due to precession in a magnetic field. *Phys Rev Lett.* 1975;35(16):1053-1055. doi:10.1103/PhysRevLett.35.1053
68. Yang YB, Liang J, Bi YJ, Chen Y, Draper T, Liu KF, Liu Z. Proton mass decomposition from the QCD energy momentum tensor. *Phys Rev Lett.* 2018;121(21):212001. doi:10.1103/PhysRevLett.121.212001
69. NIST Chemistry WebBook, SRD 69, α-D-glucose: enthalpy of combustion of the solid, −2805.0 ± 1.3 kJ/mol. https://webbook.nist.gov/cgi/cbook.cgi?ID=C492626&Mask=2
70. Wang M, Huang WJ, Kondev FG, Audi G, Naimi S. The AME 2020 atomic mass evaluation (II). Tables, graphs and references. *Chin Phys C.* 2021;45(3):030003. doi:10.1088/1674-1137/abddaf. Binding energy per nucleon: carbon-12 7680.1446 keV, oxygen-16 7976.2072 keV.
71. Anderson PW. More is different. *Science.* 1972;177(4047):393-396. doi:10.1126/science.177.4047.393
72. Cooper LN. Bound electron pairs in a degenerate Fermi gas. *Phys Rev.* 1956;104(4):1189-1190. doi:10.1103/PhysRev.104.1189
73. Bardeen J, Cooper LN, Schrieffer JR. Theory of superconductivity. *Phys Rev.* 1957;108(5):1175-1204. doi:10.1103/PhysRev.108.1175
74. Adelberger EG, et al. Solar fusion cross sections. II. The pp chain and CNO cycles. *Rev Mod Phys.* 2011;83(1):195-245. doi:10.1103/RevModPhys.83.195. Section III: the rate of p + p → d + e⁺ + νₑ "is too small to be measured in the laboratory" and is calculated from weak-interaction theory.
75. Caffarelli L, Kohn R, Nirenberg L. Partial regularity of suitable weak solutions of the Navier-Stokes equations. *Comm Pure Appl Math.* 1982;35(6):771-831. doi:10.1002/cpa.3160350604
76. Hawking SW. Breakdown of predictability in gravitational collapse. *Phys Rev D.* 1976;14(10):2460-2473. doi:10.1103/PhysRevD.14.2460
77. Page DN. Information in black hole radiation. *Phys Rev Lett.* 1993;71(23):3743-3746. doi:10.1103/PhysRevLett.71.3743
78. Penington G. Entanglement wedge reconstruction and the information paradox. *J High Energy Phys.* 2020;2020(9):2. doi:10.1007/JHEP09(2020)002. arXiv:1905.08255 (May 2019).
79. Almheiri A, Engelhardt N, Marolf D, Maxfield H. The entropy of bulk quantum fields and the entanglement wedge of an evaporating black hole. *J High Energy Phys.* 2019;2019(12):63. doi:10.1007/JHEP12(2019)063
80. Almheiri A, Mahajan R, Maldacena J, Zhao Y. The Page curve of Hawking radiation from semiclassical geometry. *J High Energy Phys.* 2020;2020(3):149. doi:10.1007/JHEP03(2020)149. arXiv:1908.10996 (August 2019).
81. Almheiri A, Hartman T, Maldacena J, Shaghoulian E, Tajdini A. The entropy of Hawking radiation. *Rev Mod Phys.* 2021;93(3):035002. doi:10.1103/RevModPhys.93.035002
