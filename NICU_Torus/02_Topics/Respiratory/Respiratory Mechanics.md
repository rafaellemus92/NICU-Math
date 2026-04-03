---
title: Respiratory Mechanics
domain: Respiratory
ring_focus: Taxonomy
gestational_axis: postnatal
phase_axis:
  - postnatal
tags:
  - nicu
  - boards
  - respiratory
  - physiology
  - ventilation
related_notes:
  - Lung Development
  - RDS
  - BPD
  - Surfactant
---

## 1. Identity

- **Respiratory mechanics** describes the physical properties governing airflow, lung inflation, and ventilation in the neonate
- Core concepts: compliance, resistance, time constants, FRC, and work of breathing
- Understanding mechanics is essential for rational ventilator management and avoiding iatrogenic lung injury
- Neonatal mechanics differ substantially from adult — particularly the highly compliant chest wall and disease-dependent changes in lung compliance

---

## 2. Taxonomy / Developmental Placement

- **Postnatal physiology** — applies from birth through NICU course
- Mechanics are dynamic: change with gestational age, disease state, surfactant administration, and ventilator intervention
- Developmental ring: **Taxonomy** — provides the physical framework for understanding all respiratory disease management
- Relevant to: [[RDS]] (↓ compliance), [[BPD]] (↑ resistance, variable compliance), meconium aspiration (↑ resistance, air trapping)

---

## 3. Structure

**Key Physical Properties:**

**1. Compliance (C)**
- Definition: **C = ΔV / ΔP** — volume change per unit pressure change; stiffness measure
- Units: mL/cmH₂O
- **Lung compliance (CL)**: elastic recoil of lung tissue; reduced in RDS (atelectasis, edema), ARDS, pulmonary edema; increased in emphysema/overdistension
- **Chest wall compliance (CCW)**: neonatal chest wall is highly compliant (cartilaginous, minimal ossification)
  - Very high CCW in preterm: chest wall collapses inward when respiratory muscles are weak → paradoxical breathing, poor FRC maintenance
  - This is why **CPAP** is critical — provides external distending pressure to compensate for poor chest wall support
- **Total respiratory system compliance (Crs)**: 1/Crs = 1/CL + 1/CCW
  - In neonates: CCW is very high (compliant), so Crs ≈ CL

**2. Resistance (R)**
- Definition: pressure required to generate flow; R = ΔP/Flow
- Units: cmH₂O/L/sec
- Primarily from **airways** (upper airway, ETT, bronchi)
- Increased in: meconium aspiration (plugs), BPD (airway remodeling, bronchomalacia), mucosal edema, bronchospasm
- ETT: significant resistance source — even small changes in ETT diameter dramatically affect resistance (R ∝ 1/r⁴ by Poiseuille)
- **Upper airway resistance**: neonates are obligate nasal breathers → nasal obstruction = significant resistance

**3. Time Constant (τ)**
- Definition: **τ = R × C** — time required for the lung to reach ~63% of its equilibrium volume
- Represents how quickly a lung unit fills or empties
- Clinical significance:
  - Short τ (low R, low C — e.g., RDS): fills/empties rapidly → requires fast rates acceptable; short I:E time adequate
  - Long τ (high R, high C — e.g., BPD, MAS): fills/empties slowly → needs long inflation time, risk of air trapping if I:E too short
  - 3–5 τ periods needed for complete equilibration
- **Air trapping**: if expiratory time < 3τ → gas accumulates → auto-PEEP → overdistension

**4. Functional Residual Capacity (FRC)**
- Volume of gas remaining in lungs at end-expiration
- **Normal FRC**: ~30 mL/kg in term neonate
- Maintained by balance of lung recoil (inward) and chest wall recoil (outward); in neonate, minimal chest wall recoil → FRC depends heavily on surfactant and active mechanisms (grunting, laryngeal braking)
- **Low FRC** (RDS, atelectasis): ↑ work of breathing, V/Q mismatch, hypoxia
- **PEEP/CPAP**: raises FRC by preventing end-expiratory collapse; normalizes FRC in RDS

**5. Work of Breathing (WOB)**
- Elastic work: to overcome lung and chest wall compliance (inflation)
- Resistive work: to overcome airway resistance (flow)
- Increased when: compliance ↓ (stiff lungs), resistance ↑ (obstructed airways), FRC low (atelectasis forces breathing on steep portion of P-V curve)
- Signs of increased WOB: tachypnea, grunting, nasal flaring, subcostal/intercostal retractions, head bobbing

---

## 4. Function

- **Normal mechanics enable spontaneous breathing at low WOB**
- FRC provides oxygen reservoir between breaths → prevents SpO₂ oscillations with each breath
- Appropriate τ ensures complete exhalation before next inspiration → prevents auto-PEEP
- Surfactant lowers surface tension → reduces elastic WOB (flat P-V curve slope at low volumes)

**Pressure-Volume (P-V) Curve:**
- Sigmoidal shape: flat at extremes (overdistension, atelectasis), steep in middle (optimal operating range)
- **Lower inflection point (LIP)**: pressure at which atelectatic lung units begin opening; PEEP should be set above LIP
- **Upper inflection point (UIP)**: pressure at which overdistension begins; peak inspiratory pressure (PIP) should stay below UIP
- Optimal ventilation: operate on steep portion of P-V curve → maximum volume change per pressure change = maximum efficiency

---

## 5. Dysfunction / Pathophysiology

**RDS (surfactant deficiency):**
- ↓ CL (atelectasis, stiff lungs), short τ, low FRC
- P-V curve: operating on flat lower portion → large pressure needed for small volume change
- Surfactant administration → rapidly shifts P-V curve → compliance improves dramatically

**BPD (chronic lung disease):**
- Variable: areas of atelectasis (low CL), areas of overdistension (high CL), fibrosis (low CL)
- Airway disease: ↑ resistance, bronchomalacia, air trapping
- Long τ: risk of air trapping with fast ventilator rates
- Pulmonary hypertension often co-exists (see [[Pulmonary Hypertension]])

**Meconium Aspiration Syndrome (MAS):**
- Ball-valve mechanism: partial airway obstruction → air enters but cannot exit → hyperinflation, air trapping
- Long τ: need slow rates, long expiratory time
- Surfactant inactivation → atelectasis coexists with overdistension (heterogeneous mechanics)

**Pulmonary edema (PDA, TTNB, heart failure):**
- Fluid in interstitium and alveoli → ↓ CL
- Also ↑ R (fluid in airways, mucosal edema)

---

## 6. Clinical Phenotype

- **Tachypnea**: primary response to ↓ CL (↑ elastic WOB) — faster, shallower breaths are mechanically efficient with stiff lungs
- **Grunting**: partial glottis closure on exhalation → generates auto-PEEP → maintains FRC
- **Nasal flaring**: ↓ nasal resistance during high WOB
- **Retractions**: negative intrathoracic pressure transmitted through compliant chest wall in preterm → visible substernally, subcostally, intercostally
- **Paradoxical breathing**: in preterm, high chest wall compliance → chest collapses inward during diaphragmatic contraction (especially in REM sleep)
- **Barrel chest / hyperinflation**: air trapping (BPD, MAS) → chronically high FRC

---

## 7. Differential / Distinctions

| Parameter | RDS | BPD | MAS | Normal Preterm |
|---|---|---|---|---|
| Compliance | ↓↓ | Variable (↓ + ↑) | Variable | ↓ (relative) |
| Resistance | Normal/↑ | ↑↑ | ↑↑ | Normal/↑ |
| Time constant | Short | Long | Long | Short |
| FRC | ↓↓ | Variable | ↑ (air trap) | ↓ |
| Ventilator strategy | Fast rates ok, PEEP | Slow rates, long exp | Slow rates, low PEEP | CPAP, short τ rates |

---

## 8. Diagnosis

- **Pulmonary function testing (PFT)**: bedside respiratory mechanics monitors (e.g., Florian, NM3) measure tidal volume, compliance, resistance in ventilated patients
- **Spirometry**: not feasible in NICU; passive mechanics used
- **CXR**: lung volume (hyperinflation vs atelectasis), disease pattern
- **Blood gas**: assess ventilatory adequacy (PaCO₂), oxygenation failure
- **P-V curve**: displayed on modern ventilators; guides PEEP and PIP setting
- **End-tidal CO₂**: assess adequacy of ventilation and detect ETT obstruction

---

## 9. Management

**Ventilator settings based on mechanics:**

- **PEEP**: set to recruit and maintain FRC above LIP; typical 4–6 cmH₂O for RDS; may be higher in severe disease
- **PIP**: set to achieve adequate tidal volume (~4–6 mL/kg for pressure-control); stay below UIP
- **Rate**: determined by τ — fast in RDS (short τ), slow in BPD/MAS (long τ)
  - Rule: expiratory time should be ≥3τ to prevent auto-PEEP
- **Inspiratory time (Ti)**: short in RDS (~0.3–0.4 sec); longer in BPD/MAS to allow full inflation
- **FiO₂**: titrate to SpO₂ targets (90–95% standard; 91–95% in BPD with PH)

**Volume-targeted ventilation (VTV):**
- Set target tidal volume (~4–6 mL/kg); ventilator automatically adjusts PIP to achieve it
- Reduces volutrauma as compliance changes (e.g., after surfactant)
- Associated with reduced BPD, pneumothorax, IVH vs pressure-limited alone

**High-frequency oscillatory ventilation (HFOV):**
- Delivers very small tidal volumes (< anatomic dead space) at high frequency (5–15 Hz)
- CO₂ eliminated by oscillation (diffusion enhancement, asymmetric velocity profiles)
- Maintains constant mean airway pressure (MAP) → constant lung volume → avoids atelectrauma
- Useful in air leak syndromes, PPHN, refractory RDS

---

## 10. Therapeutics

- **Surfactant**: most rapid improvement in compliance in RDS; normalizes P-V curve
- **CPAP**: provides PEEP to maintain FRC; reduces WOB
- **Caffeine**: increases respiratory drive (central); reduces apnea; reduces BPD (likely anti-inflammatory + improved respiratory muscle efficiency)
- **Bronchodilators** (salbutamol/albuterol, ipratropium): for airway resistance in BPD; modest benefit; do not reduce BPD
- **Diuretics** (furosemide, hydrochlorothiazide/spironolactone): improve CL by reducing pulmonary edema in BPD
- **Systemic steroids** (dexamethasone): improve CL in severe BPD; significant neurodevelopmental risk limits use

---

## 11. Complications / Outcomes

- **Volutrauma**: overdistension injury from excessive tidal volumes; major cause of BPD
- **Atelectrauma**: repeated opening and closing of collapsed alveoli; inflammatory injury
- **Air leak**: overdistension → alveolar rupture → pneumothorax, PIE, pneumomediastinum (see [[Air Leak]])
- **Chronic air trapping** (BPD, MAS): persistent hyperinflation, exercise intolerance
- **Diaphragm fatigue**: high WOB → respiratory failure → need for mechanical ventilation

---

## 12. Associations / Genetics / Maternal-Fetal Links

- **Gestational age**: primary determinant of mechanical maturity; extremely preterm have worst mechanics (short τ, ↓ CL, poor FRC maintenance)
- **Surfactant therapy**: transforms RDS mechanics dramatically; compliance improves rapidly
- **BPD genetics**: SPOCK2, VEGF variants associated with BPD susceptibility
- **Trisomy 21**: airway hypotonia, ↑ upper airway resistance, laryngomalacia, bronchomalacia → complex mechanics

---

## 13. Context / Board Framing

- **"Formula for compliance?"** → C = ΔV/ΔP
- **"Time constant?"** → τ = R × C; 3τ needed for complete exhalation
- **"Why does preterm have retractions?"** → High chest wall compliance → negative intrathoracic pressure deforms chest wall inward
- **"Why does RDS have short time constant?"** → Both R and C low → τ = R × C is short
- **"Why does BPD need slow ventilator rates?"** → Long τ (↑ R, ↑ C in some regions) → needs long expiratory time → slow rates prevent auto-PEEP
- **"Upper and lower inflection points?"** → LIP = PEEP target; UIP = PIP limit; operate on steep middle portion
- **"Volume-targeted vs pressure?"** → VTV reduces volutrauma as compliance changes; superior for BPD prevention
- **"What is grunting?"** → Auto-PEEP generation via partial glottic closure to maintain FRC

---

## 14. Edge Pearl

- **The paradox of the compliant neonatal chest wall**: In preterm infants, the chest wall is so compliant that it provides almost no outward recoil. This means the only thing maintaining FRC is surfactant (lowering surface tension) and active laryngeal braking (grunting). Remove either — give a muscle relaxant to a preterm without PEEP, or remove surfactant activity — and FRC collapses toward zero. This is why **PEEP must be provided at all times** on mechanical ventilation in a preterm, even during the inspiratory phase cycling. Failure to maintain PEEP (e.g., leak around uncuffed ETT) causes oscillating atelectasis with each breath — the definition of atelectrauma.

---

## Linked Notes

- [[Lung Development]]
- [[Surfactant]]
- [[RDS]]
- [[BPD]]
- [[Air Leak]]
- [[Pulmonary Hypertension]]
- [[Extrauterine Pulmonary Transition]]

---

## Visual Map Position

- **Ring**: Taxonomy (mechanical framework)
- **Gestational axis**: Postnatal
- **Hub**: central to all ventilator management decisions
- **Upstream**: [[Lung Development]] (structural basis), [[Surfactant]] (compliance determinant)
- **Downstream**: [[RDS]] management, [[BPD]] prevention, [[Air Leak]] risk

---

## Questions To Review

1. Define compliance, resistance, and time constant. Give the formula for each.
2. Why does the preterm infant have paradoxical chest wall movement?
3. How does RDS change lung compliance, and how does surfactant restore it?
4. Why must BPD patients be ventilated with slower rates than RDS patients?
5. What are the lower and upper inflection points on the P-V curve, and how do they guide PEEP and PIP settings?
6. What is volutrauma, and how does volume-targeted ventilation reduce it?
7. What is auto-PEEP and when does it occur in neonates?
8. Why is HFOV useful for air leak syndromes?
