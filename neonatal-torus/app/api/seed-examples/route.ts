import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function ensureConcept(
  db: ReturnType<typeof getDb>,
  name: string,
  domain: string,
  identity: string,
  extra?: {
    ring2?: string;
    ring3?: string;
    ring4?: string;
    ring5?: string;
    timeline?: string;
    pearls?: string[];
    relevance?: number;
  }
): number {
  const slug = slugify(name);
  const existing = db
    .prepare("SELECT id FROM concepts WHERE slug = ?")
    .get(slug) as { id: number } | undefined;

  if (existing) return existing.id;

  const result = db
    .prepare(
      `INSERT INTO concepts (name, slug, primary_domain, ring1_identity, ring2_taxonomy,
       ring3_associations, ring4_distinctions, ring5_edge, timeline, board_pearls, exam_relevance)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .run(
      name, slug, domain, identity,
      extra?.ring2 || null,
      extra?.ring3 || null,
      extra?.ring4 || null,
      extra?.ring5 || null,
      extra?.timeline || null,
      extra?.pearls ? JSON.stringify(extra.pearls) : null,
      extra?.relevance ?? 0.6
    );
  return result.lastInsertRowid as number;
}

function ensureEdge(
  db: ReturnType<typeof getDb>,
  sourceId: number,
  targetId: number,
  relationType: string,
  weight: number,
  explanation: string,
  sequenceOrder?: number
) {
  const existing = db
    .prepare(
      "SELECT id FROM concept_edges WHERE source_id = ? AND target_id = ? AND relation_type = ?"
    )
    .get(sourceId, targetId, relationType);
  if (existing) return;

  db.prepare(
    `INSERT INTO concept_edges (source_id, target_id, relation_type, weight, explanation, sequence_order)
     VALUES (?, ?, ?, ?, ?, ?)`
  ).run(sourceId, targetId, relationType, weight, explanation, sequenceOrder ?? null);
}

export async function POST() {
  const db = getDb();

  const tx = db.transaction(() => {
    // ═══════════════════════════════════════════════════════
    // PDA — Embryology chain
    // ═══════════════════════════════════════════════════════
    const arch6 = ensureConcept(db, "6th Pharyngeal Arch", "mfm",
      "The 6th pharyngeal arch gives rise to the pulmonary arteries and the ductus arteriosus.",
      {
        ring2: "Pharyngeal arch system, branchial apparatus",
        ring5: "Left 6th arch → ductus arteriosus + left pulmonary artery. Right 6th arch regresses.",
        timeline: "Embryology: weeks 4-7",
        relevance: 0.5,
      }
    );

    const ductus = ensureConcept(db, "Ductus Arteriosus", "cv",
      "A fetal vascular connection between the pulmonary artery and the descending aorta, allowing blood to bypass the lungs.",
      {
        ring2: "Fetal circulation shunts: ductus arteriosus, ductus venosus, foramen ovale",
        ring3: "PGE2 keeps it open in utero. Falls in PGE2 + rise in O2 after birth triggers closure.",
        ring4: "Distinct from PDA — ductus arteriosus is normal in fetal life, PDA is its pathologic persistence.",
        ring5: "Indomethacin/ibuprofen close PDA by inhibiting prostaglandin synthesis. PGE1 infusion keeps it open in ductal-dependent lesions.",
        timeline: "Fetal life → closes within 24-72h after birth",
        pearls: [
          "PGE1 keeps ductus open — critical for ductal-dependent lesions",
          "Indomethacin closes PDA by blocking COX → decreasing PGE2",
          "Functional closure by 24-72h, anatomic closure by 2-3 weeks",
        ],
        relevance: 0.85,
      }
    );

    const pda = ensureConcept(db, "Patent Ductus Arteriosus", "cv",
      "Failure of the ductus arteriosus to close after birth, resulting in a persistent left-to-right shunt from aorta to pulmonary artery.",
      {
        ring2: "Congenital heart disease, acyanotic left-to-right shunts",
        ring3: "Prematurity, RDS, fluid overload, BPD, NEC (from diastolic steal), IVH",
        ring4: "Distinguish from innocent murmur, VSD, aortopulmonary window. PDA has continuous 'machinery' murmur.",
        ring5: "Most common heart defect in premature infants. Congenital rubella → PDA association is classic board question.",
        timeline: "Neonatal: days 1-7, often symptomatic day 3-5 in preterms",
        pearls: [
          "Machinery murmur — continuous, best at left infraclavicular",
          "Wide pulse pressure and bounding pulses",
          "Congenital rubella + PDA is classic board association",
          "Ibuprofen preferred over indomethacin (fewer renal side effects)",
        ],
        relevance: 0.9,
      }
    );

    const arch4 = ensureConcept(db, "4th Pharyngeal Arch", "mfm",
      "The 4th pharyngeal arch gives rise to the aortic arch (left side) and the right subclavian artery.",
      {
        ring2: "Pharyngeal arch system",
        ring4: "4th arch → aortic arch vs 6th arch → ductus arteriosus. Common board comparison.",
        ring5: "Interrupted aortic arch type B → 22q11 deletion (DiGeorge). Aberrant right subclavian from abnormal 4th arch.",
        timeline: "Embryology: weeks 4-7",
        relevance: 0.5,
      }
    );

    const aorticArch = ensureConcept(db, "Aortic Arch", "cv",
      "The aortic arch connects the ascending aorta to the descending aorta, giving rise to the brachiocephalic, left common carotid, and left subclavian arteries.",
      {
        ring3: "Coarctation of the aorta, interrupted aortic arch, vascular rings",
        ring5: "Right-sided aortic arch → associated with tetralogy of Fallot and DiGeorge",
        relevance: 0.6,
      }
    );

    // Embryology chain: 6th arch → ductus → PDA
    ensureEdge(db, arch6, ductus, "embryology", 0.9, "6th pharyngeal arch gives rise to ductus arteriosus", 1);
    ensureEdge(db, ductus, pda, "embryology", 0.9, "Failure to close → PDA", 2);
    // Parallel: 4th arch → aortic arch
    ensureEdge(db, arch4, aorticArch, "embryology", 0.8, "4th pharyngeal arch gives rise to aortic arch", 1);
    // Distinction: arch comparisons
    ensureEdge(db, arch6, arch4, "distinction", 0.7, "6th arch → ductus vs 4th arch → aortic arch");

    // ═══════════════════════════════════════════════════════
    // Rubella — Association chain
    // ═══════════════════════════════════════════════════════
    const rubella = ensureConcept(db, "Congenital Rubella", "id",
      "Congenital infection caused by rubella virus, leading to classic triad: sensorineural hearing loss, cataracts, and congenital heart disease (especially PDA).",
      {
        ring2: "TORCH infections, congenital viral infections",
        ring3: "PDA, pulmonary artery stenosis, cataracts, sensorineural hearing loss, blueberry muffin rash, thrombocytopenia, radiolucent bone disease",
        ring4: "Distinguish from congenital CMV (periventricular calcifications, microcephaly) vs rubella (cataracts, PDA).",
        ring5: "Rubella is the only TORCH infection where PDA is the classic cardiac lesion.",
        pearls: [
          "Classic triad: hearing loss + cataracts + PDA",
          "Rubella → PDA (not VSD, not ASD — specifically PDA)",
          "Blueberry muffin rash = dermal erythropoiesis",
        ],
        relevance: 0.8,
      }
    );

    ensureEdge(db, rubella, pda, "infectious_association", 0.9, "Congenital rubella classically causes PDA");
    ensureEdge(db, rubella, pda, "association", 0.9, "PDA is the hallmark cardiac lesion of congenital rubella");

    // ═══════════════════════════════════════════════════════
    // Lung Development — Timeline chain
    // ═══════════════════════════════════════════════════════
    const pseudoglandular = ensureConcept(db, "Pseudoglandular Phase", "resp",
      "Lung development stage (weeks 5-17) characterized by branching morphogenesis of the airways. All conducting airways formed by end of this phase.",
      {
        ring2: "Lung development phases: embryonic → pseudoglandular → canalicular → saccular → alveolar",
        ring3: "CPAM type I, II, III form during this phase",
        ring5: "All conducting airways complete by week 17 — no new airways form after this",
        timeline: "Embryology: weeks 5-17",
        relevance: 0.7,
      }
    );

    const canalicular = ensureConcept(db, "Canalicular Phase", "resp",
      "Lung development stage (weeks 16-26) during which respiratory bronchioles form, type II pneumocytes appear, and surfactant production begins. The first point at which gas exchange is theoretically possible.",
      {
        ring2: "Lung development phases",
        ring3: "Viability limit, surfactant production onset, type I and II pneumocyte differentiation",
        ring4: "Gas exchange possible from ~24 weeks (late canalicular). Before this = incompatible with postnatal life.",
        ring5: "Limit of viability (~22-24 weeks) corresponds to late canalicular phase — this is WHY periviable infants struggle.",
        timeline: "Embryology: weeks 16-26",
        pearls: [
          "First surfactant production begins in canalicular phase",
          "Viability limit = late canalicular phase (~24 weeks)",
          "Type II pneumocytes differentiate → surfactant production",
        ],
        relevance: 0.85,
      }
    );

    const saccular = ensureConcept(db, "Saccular Phase", "resp",
      "Lung development stage (weeks 24-36) characterized by formation of terminal saccules (primitive alveoli), thinning of interstitium, and increasing surfactant production.",
      {
        ring2: "Lung development phases",
        ring3: "RDS in premature infants, antenatal steroids, surfactant replacement",
        ring5: "Most premature infants are born in saccular phase — this is the target for antenatal steroids",
        timeline: "Embryology: weeks 24-36",
        relevance: 0.7,
      }
    );

    const alveolar = ensureConcept(db, "Alveolar Phase", "resp",
      "Final lung development stage (36 weeks to ~8 years) characterized by septation of saccules into true alveoli. Number of alveoli increases from ~50 million at birth to ~300 million by age 8.",
      {
        ring2: "Lung development phases",
        ring3: "BPD (bronchopulmonary dysplasia) — arrest of alveolarization",
        ring5: "BPD = disrupted alveolarization. New BPD in extremely preterm infants = arrested at saccular→alveolar transition.",
        timeline: "36 weeks gestation to ~8 years",
        pearls: [
          "50M alveoli at birth → 300M by age 8",
          "BPD = arrested alveolarization",
        ],
        relevance: 0.7,
      }
    );

    // Timeline chain
    ensureEdge(db, pseudoglandular, canalicular, "timeline", 0.9, "Pseudoglandular → Canalicular (week 16-17 transition)", 1);
    ensureEdge(db, canalicular, saccular, "timeline", 0.9, "Canalicular → Saccular (week 24-26 transition)", 2);
    ensureEdge(db, saccular, alveolar, "timeline", 0.9, "Saccular → Alveolar (week 36 transition)", 3);

    // CPAM — pathology overlay
    const cpam = ensureConcept(db, "CPAM", "resp",
      "Congenital Pulmonary Airway Malformation — a developmental hamartomatous lesion of the lung with cystic and/or solid components arising from abnormal branching morphogenesis.",
      {
        ring2: "Congenital lung malformations: CPAM, pulmonary sequestration, congenital lobar emphysema, bronchogenic cyst",
        ring3: "Hydrops (if large), polyhydramnios, mediastinal shift, postnatal respiratory distress",
        ring4: "CPAM communicates with airway (enhances with contrast) vs sequestration has systemic arterial supply (feeding vessel from aorta).",
        ring5: "CPAM communicates with tracheobronchial tree. Sequestration has systemic (aortic) blood supply. This distinction is the #1 board question on congenital lung lesions.",
        pearls: [
          "CPAM = communicates with airway, pulmonary blood supply",
          "Sequestration = NO airway communication, SYSTEMIC blood supply",
          "Type I (large cysts) most common, best prognosis",
        ],
        relevance: 0.75,
      }
    );

    const sequestration = ensureConcept(db, "Pulmonary Sequestration", "resp",
      "A mass of non-functioning lung tissue that lacks normal communication with the tracheobronchial tree and receives its blood supply from a systemic artery (typically from the aorta).",
      {
        ring2: "Congenital lung malformations",
        ring3: "Recurrent infections, feeding vessel from aorta visible on CT angiography",
        ring4: "No airway communication (vs CPAM). Systemic arterial supply (vs normal pulmonary). Intralobar (within visceral pleura) vs extralobar (own pleural investment).",
        ring5: "Extralobar sequestration associated with other anomalies (CDH, foregut malformations). Intralobar presents later with recurrent infections.",
        pearls: [
          "Systemic artery from aorta = pathognomonic finding",
          "Extralobar → associated with CDH",
        ],
        relevance: 0.65,
      }
    );

    ensureEdge(db, canalicular, cpam, "association", 0.6, "CPAM arises during pseudoglandular-canalicular transition");
    ensureEdge(db, cpam, sequestration, "differential", 0.85, "CPAM vs sequestration: airway communication and blood supply");
    ensureEdge(db, cpam, sequestration, "distinction", 0.85, "CPAM communicates with airway; sequestration has systemic blood supply");

    // Management edges
    ensureEdge(db, pda, ductus, "physiology", 0.8, "PDA = persistent patency of the ductus arteriosus");

    // Cross-links
    ensureEdge(db, pda, rubella, "association", 0.9, "Congenital rubella classically causes PDA");
  });

  tx();

  return NextResponse.json({
    success: true,
    message: "Example data seeded: PDA embryology chain, lung development timeline, CPAM/sequestration differentials, rubella associations",
  });
}
