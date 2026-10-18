A cells-to-pair model of attunement

# Shared Air

When a mother holds her baby and their heart rates rise and fall together, what carries it? This model builds three answers from the same pacemaker and breathing cells, then asks which bedside measurements could tell them apart.

**Perceived**

Mom perceives the infant's state and responds. The bond runs through two nervous systems, with a delay.

**Physical**

Contact acts on the infant's cells directly. Warmth changes pacemaker kinetics; mom's heartbeat pushes on the infant's pacemaker. Nobody has to notice anything.

**Alike**

Nothing passes between them. Two bodies built alike share a room, its alarms and its rhythms.

Each world is kept pure so its fingerprint is clean. Real life may mix them; the tests are built so a mixture could be taken apart.

Live

## The bedside, simulated

0:00

Infant RR — · node sync —

Mom RR — · node sync —

Outer ring: sinoatrial pacemaker cells. Inner ring: respiratory rhythm cells. A cell lights when it fires. A heartbeat is the moment the ring fires together. The bar under each ring is arousal, the hidden state the cells respond to.

Heart rate, last 90 seconds InfantMomAnother parent in the pod

Breathing, last 20 seconds *Inspiration rises, expiration falls*

Where mom's heart is at each infant beat *locking — · other parent —*

A synchrogram. Each dot is one infant beat, placed by how far mom is through her own cardiac cycle. Scattered dots mean the hearts are timing independently. Horizontal bands mean the infant's beats fall at preferred moments of mom's cycle. The locking index is 0 for random, 1 for locked; the other parent gives the chance level.

Infant · mom—

Infant · other parent—

Difference—

Rate synchrony is the peak correlation of 5-second heart rate within ±10 seconds of lag, over the last 90 seconds. The other parent shares the room but not the bond. Here the two adults are matched in noise and exposure, so the difference isolates the bond; at a real bedside it does only if they are matched. One window is noisy. The tests below average many sessions.

Which world

Perceived Physical Alike

Mom

Out of the room At the bedside Skin-to-skin Skin-to-skin, asleep

Infant breathing

Own (CPAP) Ventilator

Events

[ ] Singing or prayer

Small factors

Responsiveness1.00

Perceived world. How strongly mom is moved by the infant's distress and acts on it. Zero means she notices nothing.

Response delay1.5 s

Perceived world. Time between the infant's change and mom's response. Timing decides whether a response settles or overshoots.

Mom's steadiness1.00×

How fast mom settles her own arousal. Slow to anger, in James's terms.

Mom's chest warmth0.35 °C

Physical world. Degrees above the warmer's set point. Skin-to-skin, the infant's temperature drifts toward it over about seven minutes, and the pacemaker runs about 8% faster per degree.

Pulse entrainment6.0

Physical world. How hard each maternal heartbeat pushes on the infant's pacemaker cells, in rad/s at the peak of the pulse. The infant's cells run at about 16 rad/s on their own. Test 5 shows what each value means.

Infant pacemaker gap junctions1.00×

Coupling between sinoatrial cells. Below about 0.3× the cells stop firing together and the rhythm turns irregular.

Infant vagal tone0.50

Resting parasympathetic brake on the pacemaker. Higher tone, slower heart, more room to respond.

The live bench uses these at once. The tests use them when you press Run.

Six tests

## What could tell the worlds apart

Each test runs many simulated sessions in all three worlds. A test is useful only if the worlds give different answers. Results below use the default settings until you run them with yours.

Test 1

### Shared room or shared bond?

Thirty five-minute sessions per world, skin-to-skin, with alarms and unit noise reaching everyone in the pod. Each dot is one session's peak rate synchrony. The infant's heart rate is compared with three people: mom, another parent in the same pod at the same time, and a mom from a different session (the usual surrogate).

Default settings

#### At the bedside

Record a second adult in the same pod at the same time: another parent, or a nurse sitting nearby. Pseudo-pairs built from other days remove the room along with the bond, so beating them proves only that the room is shared. The second adult has to be matched to mom: the same exposure to alarms and activity, and similar signal quality. An unmatched control can produce a positive difference with no bond at all, simply because its signal is noisier. Comparing the same mother across conditions (awake and asleep, holding and not) avoids the problem.

Test 2

### Who moves first?

The same sessions, now asking about direction. For every lag from −15 to +15 seconds, the infant–other-parent correlation is subtracted from the infant–mom correlation. With a matched control, what remains is timing the room doesn't explain. Positive lag means the infant changed first.

Default settings

#### At the bedside

The direction here is an assumption built into the perceived world: the infant's distress reaches mom faster than mom's calm reaches the infant. Real recordings could show the opposite. The test is whether any consistent lag survives after the room is subtracted.

Test 3

### The ventilator as a control

On controlled ventilation, the machine sets the infant's breathing. If the bond runs through arousal, it should disappear from breathing and persist in heart rate. Bars show the bond-specific rate synchrony (mom minus other parent) in each channel, with standard error.

Default settings

#### At the bedside

On the ventilator, breathing synchrony is zero by construction. The informative result is heart-rate synchrony that survives. Ventilation also travels with sedation and severity, so the cleanest comparison is the same infant held before and after extubation, at the same time of day.

Test 4

### Is more coupling better?

Perceived world. Responsiveness is swept from 0 to 3. A heel stick lands at 80 seconds. Recovery is the time until the infant's heart rate returns within 10 bpm of baseline and stays there 15 seconds. The lower panel shows rate synchrony at each setting. Fourteen runs per point; the band is the middle half of runs. In the physical world this sweep does nothing: responsiveness isn't in its equations.

Default settings

#### At the bedside

Measure recovery, not harmony. After a heel stick or suctioning, time how long heart rate and saturation take to return to baseline when the infant is held by mom versus lying in the bed. Code mom's response latency from video. Jaffe and Beebe found that mid-range vocal coordination at 4 months predicted secure attachment and the highest coordination predicted insecure attachment. In this model the shape doesn't need the delay; removing it changes almost nothing. The falling side is soothing. The rising side is a second stable state: above a responsiveness of about 2, a large enough disturbance flips the pair into sustained co-arousal, because mom's arousal both returns to the infant and limits her soothing. Remove that capacity limit and the second state disappears. That is one mechanism that could produce the shape, not proof that it is the one at work.

Test 5

### Beats, not rates

If mom's heartbeat pushes on the infant's pacemaker through contact, the signature isn't in rates. It's in timing: infant beats fall at preferred moments of mom's cycle, near a 2:1 ratio. The phase-locking index measures that from two sets of beat times. Dots: one session each, from the Test 1 sessions, against mom and against the other parent. Then the index against the strength of the push, in the physical world.

Default settings

#### At the bedside

This needs beat times from both ECGs, not monitor heart rates. Plot the synchrogram and compare against twin surrogates. Van Leeuwen and colleagues did exactly this for six mothers and their fetuses with magnetocardiography and found brief epochs of 3:2, 5:3 and 4:3 locking, more often during fast paced maternal breathing, with no support for a direct path through breathing movements. That is what weak forcing near a ratio produces: intermittent locking, not a locked rhythm. After birth, the medium changes from amniotic fluid and tissue to air and skin.

Test 6

### The first fifteen minutes

Three minutes at the bedside, then skin-to-skin for twelve. Top: infant heart rate relative to the pre-contact baseline, averaged over fourteen runs, with mom awake (solid) and asleep (dashed). Middle: how much that heart rate wanders from run to run. Bottom: infant temperature. No alarms.

Default settings

#### At the bedside

The cheapest discriminating experiment is a sleeping mother. Kangaroo-care sessions where mom falls asleep happen anyway. If the infant's response to contact survives her sleep, it isn't running through her responsiveness. Log a skin temperature probe alongside heart rate, because the heat channel is small and slow and a few beats per minute will hide in noise without it. The kangaroo-care literature also reports the mother's chest temperature adjusting to the infant's; this model doesn't include that, and it would be worth measuring.

How it's built

## Three levels, each built from the one below

CellsLevel 1

The sinoatrial node is 24 pacemaker cells. Each is a phase oscillator with its own natural rate (about ±7% scatter), joined to the others by gap junctions. A heartbeat is the moment the population completes a cycle together. Breathing comes from 12 respiratory rhythm cells built the same way. Vagal tone slows the pacemakers and sympathetic drive speeds them. Each inspiration briefly withdraws vagal tone, which produces respiratory sinus arrhythmia without being programmed in. Temperature scales every pacemaker's rate at Q10 = 2.2.

PersonLevel 2

One hidden variable, arousal, drives vagal withdrawal, sympathetic drive and breathing rate. It relaxes toward baseline (about 30 s for the infant, 20 s for an adult) and carries its own noise. A heel stick raises the infant's arousal. An alarm raises everyone's. Asleep, mom's arousal settles lower and she perceives nothing.

Pair, perceivedLevel 3

Mom perceives the infant's distress after a delay. It raises her own arousal (contagion) and drives a soothing action that lowers the infant's arousal over about four seconds. Her capacity to soothe falls as her own arousal climbs. Her arousal also leaks back to the infant (mirroring). All worlds share a slow unit noise (light, sound, activity) and the alarms. Singing or prayer adds a small calming input and raises the infant's vagal tone by 12%, a placeholder for the channel a music therapy study would measure.

Pair, physicalLevel 3

Two channels, both needing skin-to-skin contact and neither needing anyone to notice. Heat: the infant's temperature drifts toward mom's chest with a time constant of about seven minutes, and the pacemaker cells run faster as they warm. Pulse: each maternal heartbeat is a brief push on every infant pacemaker cell, shaped like a pressure pulse. In this world the perceived paths are cut; in the perceived world these are.

```
cell k     dθₖ/dt = ωₖ·(1 + 0.25·S)(1 − 0.4·V)·Q10^(T/10) + K_gap·r·sin(ψ − θₖ) − ε·P(ψ_mom)·sin θₖ
           V = V₀·(1 − 0.8·A)·(1 − RSA·insp),   S = 0.1 + 0.5·A⁺,   P(ψ) = e^{2(cos ψ − 1)} − mean
infant     dAᵢ/dt = (−Aᵢ + 0.8·U)/30 − C + g·0.04·Aₘ(t−τ) − 0.02·Aᵢ³ + noise
mom        dAₘ/dt = (−(Aₘ − A₀) + 0.8·U)/(20/steadiness) + g·0.10·Aᵢ(t−τ) − 0.02·Aₘ³ + noise
soothing   dC/dt  = (g·0.30·Aᵢ(t−τ)·cap(Aₘ) − C)/4,   cap = 1/(1 + (Aₘ/0.8)²)
heat       dT/dt  = contact·(T_chest − T)/400 + (1 − contact)·(0 − T)/400
perceived  g = responsiveness × presence × awake,   ε = 0,   heat off
physical   g = 0,   ε = pulse × contact,   heat on
alike      g = 0,   ε = 0,   heat off
locking    2:1, to first order in weak forcing: |ω_infant − 2·ω_mom| < ε·a₂/2,   a₂ = 0.19 (second harmonic of P)
```

A note on scale

A cell is mostly water, and it is tempting to reach for Navier–Stokes. But at a cell's size the Reynolds number is about 10⁻⁵. The inertial term that makes those equations hard vanishes, and what remains is Stokes flow: linear, time-reversible, no turbulence. At the cell, water matters as the solvent for the ion gradients that set the pacemaker's rate, and the right equations are Hodgkin–Huxley, not Navier–Stokes. Navier–Stokes is the physics of the infant's aorta, where the Reynolds number runs into the thousands and the flow is pulsatile. It describes each body from the inside. After birth no fluid connects the two bodies; what they share is heat, pressure, sound, light and air.

Limits

## What this model can't tell you

- Which world is real. All three are built to be equally plausible. The model shows which measurements could separate them and roughly how many sessions it might take. Only recordings can decide.
- Any number here as a clinical value. Every parameter was chosen to give realistic resting heart and breathing rates, not fitted to patients. The temperature coefficient and the chest warmth are assumptions to check.
- How strong the pulse channel is. The slider's default is set so the live synchrogram shows something; Test 5 says what strength full locking would need and why that is far more than a pressure wave through two chest walls could deliver.
- The direction of influence. Test 2's lag follows from assumptions about contagion and soothing.
- Much of the physiology. Arousal is one number. Real infants carry pain, sedation, cortisol and illness. An infant with trisomy 18 and a cardiac lesion would change nearly every parameter.
- Cellular detail. The cells are phase oscillators. They capture synchronization, not ion channels, action potential shape or conduction.
- Life before birth. Even then maternal and fetal blood never mix: the placenta couples two circulations across a membrane, through heat, gases and nutrients. Van Leeuwen's prenatal locking was recorded in that setting, before this model begins.
- Ratios other than n:1. The locking index here detects 2:1 and 3:1. Real recordings need n:m analysis (3:2, 5:3), as in the prenatal work.
- Whose good the response serves. The equations describe how two bodies move each other. Nothing in them distinguishes care from skilled manipulation.

If one of these worlds is the real one, the math can describe the breath. It still won't be the life the breath carries.

Revised October 16 after an independent audit by ChatGPT. The inverted U in Test 4 turned out not to need the delay, the other-parent contrast needs a matched control, and the locking condition holds to first order.