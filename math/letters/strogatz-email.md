# Email to Steven Strogatz (draft)

The text below is the draft as written. It has not been sent. Words in square brackets are
placeholders to fill in before sending; the checklist under "Before you send" says what goes in
each. Copy it from the rendered page, not the raw file.

---

Subject: A NICU clinician's question about the first breath as a bifurcation

Dear Professor Strogatz,

I'm a [role] at [hospital], and I have one question in your area. A pointer to a paper would be more than enough.

At birth, breathing switches from the intermittent bursts of fetal life to a continuous rhythm; at death, the rhythm stops. Is there a standard way to tell whether a switch like that is a bifurcation (the oscillation born or destroyed as a parameter crosses a threshold) or a jump between two coexisting states? And could breath-to-breath data at the bedside tell the two apart?

Why I ask: Paydarfar and colleagues found a Winfree phase singularity in the cat respiratory rhythm, and gentle random mattress vibration has reduced apnea in preterm infants. With help from AI tools, I also built a toy model of mother-infant cardiac coupling: Kuramoto pacemaker cells plus a delayed "attunement" loop between the two people. In the model, more attunement isn't always better; past a saddle-node bifurcation the pair can lock into a high-arousal state. I also found that the synchrony index R alone doesn't determine its own future, which I now see is what the Watanabe-Strogatz and Ott-Antonsen reductions address.

The model is here: [link]. Any errors are mine.

Thank you for Sync, and for [your On Point conversation on October 13].

[Full name, credentials]\
[Role, unit, institution]

P.S. Ecclesiastes' refrain word hevel, usually translated "vanity," literally means breath or vapor. Working at the first breath, I find that hard to forget.

---

## Before you send

- [ ] **Spell it Steven**, not Stephen, in the greeting, the address line and any notes.
- [ ] **Confirm the episode you heard.** The likely one is WBUR *On Point*, 13 October 2026, "AI is
  steamrolling through math. Why does that matter?", with Strogatz, Hugo Duminil-Copin and Francis Su
  [12]. This is not confirmed. If you are not sure, cut the clause and end with "Thank you for Sync."
- [ ] **Fill every bracket**: [role], [hospital], [link], [your On Point conversation on October 13],
  [Full name, credentials] and [Role, unit, institution]. No bracket should be left in the email.
- [ ] **Put the live Shared Air page in [link]**: https://nicu-math.vercel.app/shared-air. That is
  the corrected page, deployed from
  [`../../web/public/shared-air/index.html`](../../web/public/shared-air/index.html). Before sending,
  check that it opens without a login and on a phone.
- [ ] **Check the rest of the site.** The [link] page has no links to the rest of the site, but its
  root, https://nicu-math.vercel.app/, still shows the earlier "Navier-Stokes Regularity in the
  Neonatal Lung" pages from PR #8 (`web/app/page.tsx`, `web/app/proof/page.tsx`,
  `web/app/layout.tsx`). They call that work "a conditional regularity result" and say
  Navier-Stokes blowup is "observed" in the lung. That does not match
  [`../README.md`](../README.md#what-remains-open) ("This work does not touch the Millennium
  problem") or the item below about keeping Navier-Stokes out of this email. Either revise those
  pages first (call the Laplace-pressure mapping P = 2γ/r an analogy: alveolar collapse is a
  clinical event, not a Navier-Stokes singularity), or send knowing that he may find them.
- [ ] **Keep faith, Navier-Stokes and QED for a later reply.** They are not in this email, and they
  should stay out until he writes back.

## Sources for the claims in this email

Each claim in the email is listed with its source. Notes say where a claim is narrower than it might
sound.

**Fetal breathing is intermittent; at birth it becomes continuous.**
Dawes et al. 1972 [1]: in fetal lambs, breathing movements are "normally but intermittently present"
over most of gestation. Patrick et al. 1980 [2]: human fetal breathing over the last 10 weeks of
pregnancy, with pauses of up to 122 minutes. What starts continuous breathing at birth is not settled
(Rigatto 1996 [3]).

**A bifurcation: an oscillation born or destroyed as a parameter crosses a threshold.**
Strogatz, *Nonlinear Dynamics and Chaos* [4]: "A limit cycle is an isolated closed trajectory" (§7.0).
A supercritical Hopf bifurcation is one standard way an oscillation is born (§8.2). Other ways cycles
are born or destroyed are in §8.4.

**Paydarfar and colleagues found a Winfree phase singularity in the cat respiratory rhythm.**
Paydarfar, Eldridge & Kiley 1986 [5]. Weak stimuli of the superior laryngeal nerve gave type 1
resetting and strong ones type 0, with a phase singularity in between. This paper shows the
singularity exists. It does not show a single stimulus stopping breathing. That "abolished"
oscillation comes from a later model paper (Paydarfar & Buerkel 1995 [6]). The topological argument
is Winfree's [7, 8].

**Gentle random mattress vibration has reduced apnea in preterm infants.**
Bloch-Salisbury et al. 2009 [9]: in 10 preterm infants, subthreshold random vibration roughly halved
breathing irregularity and pauses longer than 5 s. Smith et al. 2015 [10]: a randomized crossover
trial in 36 infants at one center, where apnea events were roughly halved during stimulation.

**Kuramoto pacemaker cells.** The Shared Air page models the sinoatrial node as 24 phase oscillators
(16 in its batch tests), each with its own natural rate (about ±7% scatter), coupled to one another
through gap junctions (the "Cells" level in the page's model section; source
[`../../web/public/shared-air/index.html`](../../web/public/shared-air/index.html)).
That is the Kuramoto setup [11]. The page itself does not use the name.

**Past a saddle-node bifurcation the pair can lock into a high-arousal state.** This is the model's
own result, not a published finding. The Shared Air audit
([`../shared-air/AUDIT.md`](../shared-air/AUDIT.md), section 4) finds that with noise off, a second
stable state with both partners aroused appears at a responsiveness of about g = 2.07. This needs the
page's default rule that mom's capacity to soothe halves once her own arousal reaches 0.8. With that
capacity held fixed, no such state appears below g_c ≈ 3.86, where the rest state itself loses
stability.

For the noise-free, zero-delay model these steps are also proved in Lean, in
[`Bistability.lean`](../wyrd-mathlib/WyrdMathlib/Limits/Bistability.lean): with the cap, rest is the
only steady state up to g = 2 (`only_rest_upto_two`), a co-arousal state exists at g = 2.1
(`coarousal_exists_above_two`) and it is stable at g = 3 (`coarousal_stable_at_three`). Without the
cap, any other steady state forces rest to be unstable (`no_coarousal_without_cap_general`), and rest
is stable exactly for g < g_c = 15/8 + √2265/24 ≈ 3.858 (`stable_iff` in
[`Optimal.lean`](../wyrd-mathlib/WyrdMathlib/SharedAir/Optimal.lean), `gc_bounds` in
[`Specific.lean`](../wyrd-mathlib/WyrdMathlib/SharedAir/Specific.lean)). The repository guide,
[`../README.md`](../README.md), lists these as proved in Lean; they were not rebuilt for this folder.
The numerical saddle-node, g ≈ 2.06888, is in
[`../numerics/shared-air-limits/limits_checks.out.txt`](../numerics/shared-air-limits/limits_checks.out.txt).

**R alone doesn't determine its own future.** Shared Air audit, item C10: two four-cell
configurations both have R = 1/2, but one has R' = K/4 and the other R' = 0, because their second
moments differ. The same example is proved in Lean, for four cells and for the page's 24
(`same_synchrony_different_future` and `same_synchrony_different_future_24` in
[`PhaseMoments.lean`](../wyrd-mathlib/WyrdMathlib/SharedAir/PhaseMoments.lean)). This is Watanabe and Strogatz's territory [13, 14], and it is what the Ott-Antonsen
reduction [15] resolves for large populations. For identical oscillators, R closes on the Poisson
submanifold (Marvel, Mirollo & Strogatz 2009 [16]).

**Sync.** Strogatz, *Sync* [17].

**On Point, October 13.** See the checklist. The episode is real [12]. Whether it is the one you heard
is not confirmed.

**Hevel literally means breath or vapor.** Brown-Driver-Briggs lexicon: "vapour, breath; figurative
vanity" [18]. The NET Bible note on Ecclesiastes 1:2 gives the literal sense as "man's transitory
breath, evanescent vapor" [19]. "Vanity of vanities" is *havel havalim*, a Hebrew superlative.

**Steven, not Stephen.** His name is Steven Henry Strogatz (Harvard PhD thesis, 1986 [20]).

### Full citations

1. Dawes GS, Fox HE, Leduc BM, Liggins GC, Richards RT. Respiratory movements and rapid eye movement sleep in the foetal lamb. *J Physiol.* 1972;220(1):119-143. doi:10.1113/jphysiol.1972.sp009698
2. Patrick J, Campbell K, Carmichael L, Natale R, Richardson B. Patterns of human fetal breathing during the last 10 weeks of pregnancy. *Obstet Gynecol.* 1980;56(1):24-30. PMID 7383483
3. Rigatto H. Regulation of fetal breathing. *Reprod Fertil Dev.* 1996;8(1):23-33. doi:10.1071/RD9960023
4. Strogatz SH. *Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering.* 2nd ed. Boulder, CO: Westview Press; 2015 (reissued by CRC Press, 2018). Sections 7.0, 8.2, 8.4.
5. Paydarfar D, Eldridge FL, Kiley JP. Resetting of mammalian respiratory rhythm: existence of a phase singularity. *Am J Physiol.* 1986;250(4 Pt 2):R721-R727. doi:10.1152/ajpregu.1986.250.4.R721
6. Paydarfar D, Buerkel DM. Dysrhythmias of the respiratory oscillator. *Chaos.* 1995;5(1):18-29. doi:10.1063/1.166067
7. Winfree AT. *The Geometry of Biological Time.* New York: Springer; 1980 (2nd ed. 2001, doi:10.1007/978-1-4757-3484-3).
8. Glass L, Winfree AT. Discontinuities in phase-resetting experiments. *Am J Physiol.* 1984;246(2 Pt 2):R251-R258. doi:10.1152/ajpregu.1984.246.2.R251
9. Bloch-Salisbury E, Indic P, Bednarek F, Paydarfar D. Stabilizing immature breathing patterns of preterm infants using stochastic mechanosensory stimulation. *J Appl Physiol.* 2009;107(4):1017-1027. doi:10.1152/japplphysiol.00058.2009
10. Smith VC, Kelty-Stephen D, Qureshi Ahmad M, Mao W, Cakert K, Osborne J, Paydarfar D. Stochastic resonance effects on apnea, bradycardia, and oxygenation: a randomized controlled trial. *Pediatrics.* 2015;136(6):e1561-e1568. doi:10.1542/peds.2015-1334
11. Kuramoto Y. *Chemical Oscillations, Waves, and Turbulence.* Berlin: Springer; 1984. doi:10.1007/978-3-642-69689-3
12. WBUR *On Point*. AI is steamrolling through math. Why does that matter? 13 October 2026. Guests Steven Strogatz, Hugo Duminil-Copin, Francis Su. https://www.wbur.org/onpoint/2026/10/13/ai-steamrolling-math-solve
13. Watanabe S, Strogatz SH. Integrability of a globally coupled oscillator array. *Phys Rev Lett.* 1993;70(16):2391-2394. doi:10.1103/PhysRevLett.70.2391
14. Watanabe S, Strogatz SH. Constants of motion for superconducting Josephson arrays. *Physica D.* 1994;74:197-253.
15. Ott E, Antonsen TM. Low dimensional behavior of large systems of globally coupled oscillators. *Chaos.* 2008;18(3):037113. doi:10.1063/1.2930766
16. Marvel SA, Mirollo RE, Strogatz SH. Identical phase oscillators with global sinusoidal coupling evolve by Möbius group action. *Chaos.* 2009;19(4):043104. doi:10.1063/1.3247089
17. Strogatz S. *Sync: The Emerging Science of Spontaneous Order.* New York: Hyperion; 2003.
18. Brown F, Driver SR, Briggs CA. *A Hebrew and English Lexicon of the Old Testament* (BDB), entry הֶבֶל (Strong's H1892). Online: https://biblehub.com/hebrew/1892.htm
19. NET Bible, translators' note on Ecclesiastes 1:2. https://www.biblegateway.com/passage/?search=Ecclesiastes+1%3A2&version=NET
20. Strogatz SH. The mathematical structure of the human sleep-wake cycle. PhD thesis, Harvard University; 1986. Published as *Lecture Notes in Biomathematics* vol. 69, Springer; 1986.
