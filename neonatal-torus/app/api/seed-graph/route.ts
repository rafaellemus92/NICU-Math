import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { upsertNode, upsertEdge } from "@/lib/graph-engine";

export async function POST() {
  const db = getDb();
  const tx = db.transaction(() => {
    // ═══ PDA / ARCH CHAIN ═══
    const arch6 = upsertNode({ name: "Left 6th Pharyngeal Arch", concept_type: "embryology_stage", primary_domain: "mfm",
      short_definition: "Embryonic structure giving rise to ductus arteriosus and left pulmonary artery",
      aliases: ["6th branchial arch", "sixth pharyngeal arch"],
      timeline_positions: ["embryology"],
      ring_identity: "The 6th pharyngeal arch gives rise to the pulmonary arteries and the ductus arteriosus.",
      ring_edge: "Left 6th arch → ductus arteriosus + left pulmonary artery. Right 6th arch regresses.",
      board_weight_score: 0.6,
      query_feature_terms: ["pharyngeal arch", "branchial arch", "ductus", "embryology"],
    });
    const arch4 = upsertNode({ name: "Left 4th Pharyngeal Arch", concept_type: "embryology_stage", primary_domain: "mfm",
      short_definition: "Embryonic structure giving rise to the aortic arch",
      aliases: ["4th branchial arch", "fourth pharyngeal arch"],
      timeline_positions: ["embryology"],
      ring_identity: "The 4th pharyngeal arch gives rise to the aortic arch (left) and right subclavian artery.",
      ring_edge: "Interrupted aortic arch type B → 22q11 deletion (DiGeorge). Aberrant right subclavian from abnormal 4th arch.",
      board_weight_score: 0.55,
      query_feature_terms: ["pharyngeal arch", "aortic arch", "DiGeorge"],
    });
    const ductus = upsertNode({ name: "Ductus Arteriosus", concept_type: "anatomy", primary_domain: "cv",
      short_definition: "Fetal vascular connection between pulmonary artery and descending aorta, bypassing the lungs",
      aliases: ["DA"],
      timeline_positions: ["prenatal", "delivery_room"],
      ring_identity: "A fetal vascular connection between the pulmonary artery and the descending aorta.",
      ring_taxonomy: "Fetal circulation shunts: ductus arteriosus, ductus venosus, foramen ovale",
      ring_associations: "PGE2 keeps it open in utero. Falls in PGE2 + rise in O2 triggers closure.",
      ring_edge: "PGE1 keeps ductus open — critical for ductal-dependent lesions. Indomethacin closes by blocking COX.",
      board_weight_score: 0.85,
      query_feature_terms: ["ductus arteriosus", "fetal circulation", "PGE", "prostaglandin"],
    });
    const aorticArch = upsertNode({ name: "Aortic Arch", concept_type: "anatomy", primary_domain: "cv",
      short_definition: "Connects ascending to descending aorta; gives rise to brachiocephalic, left carotid, left subclavian",
      aliases: ["aorta"],
      ring_associations: "Coarctation, interrupted aortic arch, vascular rings",
      ring_edge: "Right-sided aortic arch → tetralogy of Fallot and DiGeorge association",
      board_weight_score: 0.6,
      query_feature_terms: ["aortic arch", "coarctation"],
    });
    const pda = upsertNode({ name: "Patent Ductus Arteriosus", concept_type: "disease", primary_domain: "cv",
      short_definition: "Failure of ductus arteriosus to close after birth; persistent left-to-right shunt aorta→PA",
      aliases: ["PDA"],
      secondary_domains: ["resp", "nutr"],
      timeline_positions: ["first_24h", "first_week", "neonatal_course"],
      ring_identity: "Failure of the ductus arteriosus to close after birth, resulting in a persistent left-to-right shunt.",
      ring_taxonomy: "Congenital heart disease, acyanotic left-to-right shunts",
      ring_associations: "Prematurity, RDS, fluid overload, BPD, NEC (diastolic steal), IVH",
      ring_distinctions: "Continuous 'machinery' murmur. Distinguish from VSD, aortopulmonary window, innocent murmur.",
      ring_edge: "Most common heart defect in premature infants. Congenital rubella → PDA is classic board question.",
      board_weight_score: 0.92,
      query_feature_terms: ["PDA", "patent ductus", "machinery murmur", "bounding pulses", "wide pulse pressure", "premature heart"],
    });
    const boundingPulses = upsertNode({ name: "Bounding Pulses", concept_type: "physical_exam_finding", primary_domain: "cv",
      short_definition: "Forceful peripheral pulses from wide pulse pressure; classic finding in PDA and aortic regurgitation",
      aliases: ["bounding peripheral pulses", "hyperdynamic pulses"],
      board_weight_score: 0.5,
      query_feature_terms: ["bounding pulses", "wide pulse pressure", "hyperdynamic"],
    });
    const widePP = upsertNode({ name: "Widened Pulse Pressure", concept_type: "physical_exam_finding", primary_domain: "cv",
      short_definition: "Increased difference between systolic and diastolic blood pressure; seen in PDA, AR, thyrotoxicosis",
      aliases: ["wide pulse pressure"],
      board_weight_score: 0.45,
      query_feature_terms: ["wide pulse pressure", "pulse pressure"],
    });
    const indomethacin = upsertNode({ name: "Indomethacin", concept_type: "pharmacology", primary_domain: "pharm",
      short_definition: "NSAID COX inhibitor used to close PDA by blocking prostaglandin synthesis",
      aliases: ["indocin"],
      ring_edge: "Renal side effects: decreased GFR, oliguria. Ibuprofen preferred for fewer renal effects.",
      board_weight_score: 0.65,
      query_feature_terms: ["indomethacin", "indocin", "COX inhibitor", "PDA closure"],
    });
    const ibuprofen = upsertNode({ name: "Ibuprofen", concept_type: "pharmacology", primary_domain: "pharm",
      short_definition: "NSAID used for PDA closure; preferred over indomethacin for fewer renal side effects",
      board_weight_score: 0.6,
      query_feature_terms: ["ibuprofen", "PDA closure"],
    });
    const acetaminophen = upsertNode({ name: "Acetaminophen (for PDA)", concept_type: "pharmacology", primary_domain: "pharm",
      short_definition: "Alternative PDA treatment; acts via peroxidase pathway rather than COX",
      aliases: ["paracetamol for PDA"],
      ring_edge: "Emerging evidence as PDA treatment with fewer hemodynamic side effects than NSAIDs",
      board_weight_score: 0.45,
      query_feature_terms: ["acetaminophen PDA", "paracetamol PDA"],
    });

    // PDA edges
    upsertEdge({ source_id: arch6, target_id: ductus, relation_type: "arises_from", weight: 0.95, explanation: "6th pharyngeal arch gives rise to ductus arteriosus", sequence_order: 1 });
    upsertEdge({ source_id: ductus, target_id: pda, relation_type: "congenital_result_of", weight: 0.9, explanation: "Failure of ductus to close → PDA", sequence_order: 2 });
    upsertEdge({ source_id: arch4, target_id: aorticArch, relation_type: "arises_from", weight: 0.9, explanation: "4th pharyngeal arch gives rise to aortic arch" });
    upsertEdge({ source_id: ductus, target_id: aorticArch, relation_type: "compared_with", weight: 0.7, explanation: "6th arch → ductus vs 4th arch → aortic arch" });
    upsertEdge({ source_id: arch6, target_id: arch4, relation_type: "embryology_contrast", weight: 0.7, explanation: "6th arch → ductus vs 4th arch → aortic arch" });
    upsertEdge({ source_id: pda, target_id: boundingPulses, relation_type: "presents_with", weight: 0.85, explanation: "Bounding pulses from wide pulse pressure in PDA" });
    upsertEdge({ source_id: pda, target_id: widePP, relation_type: "presents_with", weight: 0.85, explanation: "Wide pulse pressure from diastolic runoff through PDA" });
    upsertEdge({ source_id: pda, target_id: indomethacin, relation_type: "treated_with", weight: 0.85, explanation: "Indomethacin closes PDA by inhibiting COX → decreasing PGE2" });
    upsertEdge({ source_id: pda, target_id: ibuprofen, relation_type: "treated_with", weight: 0.85, explanation: "Ibuprofen closes PDA; preferred over indomethacin for fewer renal effects" });
    upsertEdge({ source_id: pda, target_id: acetaminophen, relation_type: "treated_with", weight: 0.6, explanation: "Acetaminophen: emerging alternative for PDA closure" });

    // ═══ RUBELLA → PDA ═══
    const rubella = upsertNode({ name: "Congenital Rubella", concept_type: "infectious_agent", primary_domain: "id",
      short_definition: "Congenital infection: classic triad of sensorineural hearing loss, cataracts, PDA",
      aliases: ["rubella", "german measles", "congenital rubella syndrome", "CRS"],
      secondary_domains: ["cv", "eent"],
      timeline_positions: ["prenatal", "neonatal_course"],
      ring_identity: "Congenital infection caused by rubella virus, leading to classic triad: hearing loss, cataracts, PDA.",
      ring_associations: "PDA, pulmonary artery stenosis, cataracts, sensorineural hearing loss, blueberry muffin rash",
      ring_distinctions: "Rubella → cataracts + PDA vs CMV → periventricular calcifications + microcephaly",
      ring_edge: "Rubella is the only TORCH infection where PDA is the classic cardiac lesion.",
      board_weight_score: 0.82,
      query_feature_terms: ["rubella", "TORCH", "cataracts", "blueberry muffin", "congenital heart PDA"],
    });
    upsertEdge({ source_id: rubella, target_id: pda, relation_type: "associated_with", weight: 0.95, explanation: "PDA is the hallmark cardiac lesion of congenital rubella" });
    upsertEdge({ source_id: rubella, target_id: pda, relation_type: "caused_by_infection", weight: 0.9, explanation: "Rubella virus damages fetal cardiovascular system → PDA" });

    // ═══ LUNG DEVELOPMENT TIMELINE ═══
    const embryonicLung = upsertNode({ name: "Embryonic Stage (Lung)", concept_type: "embryology_stage", primary_domain: "resp",
      short_definition: "Lung development weeks 3-5: lung bud from foregut, initial branching",
      aliases: ["embryonic lung stage"],
      timeline_positions: ["embryology"],
      board_weight_score: 0.4,
      query_feature_terms: ["lung bud", "foregut", "embryonic lung"],
    });
    const pseudoglandular = upsertNode({ name: "Pseudoglandular Stage", concept_type: "embryology_stage", primary_domain: "resp",
      short_definition: "Lung development weeks 5-17: all conducting airways form via branching morphogenesis",
      aliases: ["pseudoglandular phase"],
      timeline_positions: ["embryology"],
      ring_identity: "Lung development stage (weeks 5-17): branching morphogenesis of airways. All conducting airways formed.",
      ring_associations: "CPAM types form during this phase",
      ring_edge: "All conducting airways complete by week 17 — no new airways after this",
      board_weight_score: 0.65,
      query_feature_terms: ["pseudoglandular", "branching morphogenesis", "conducting airways"],
    });
    const canalicular = upsertNode({ name: "Canalicular Stage", concept_type: "embryology_stage", primary_domain: "resp",
      short_definition: "Lung development weeks 16-26: respiratory bronchioles form, type II pneumocytes appear, surfactant begins",
      aliases: ["canalicular phase"],
      timeline_positions: ["embryology", "prenatal"],
      ring_identity: "Weeks 16-26: respiratory bronchioles form, type II pneumocytes differentiate, surfactant production begins.",
      ring_edge: "Limit of viability (~22-24 weeks) corresponds to late canalicular phase. This is WHY periviable infants struggle.",
      board_weight_score: 0.8,
      query_feature_terms: ["canalicular", "viability", "surfactant onset", "type II pneumocyte", "periviable"],
    });
    const saccular = upsertNode({ name: "Saccular Stage", concept_type: "embryology_stage", primary_domain: "resp",
      short_definition: "Lung development weeks 24-36: terminal saccules form, interstitium thins, surfactant increases",
      aliases: ["saccular phase"],
      timeline_positions: ["prenatal"],
      ring_identity: "Weeks 24-36: terminal saccules (primitive alveoli), thinning interstitium, increasing surfactant.",
      ring_edge: "Most premature infants born in saccular phase — target for antenatal steroids",
      board_weight_score: 0.7,
      query_feature_terms: ["saccular", "terminal saccules", "antenatal steroids"],
    });
    const alveolar = upsertNode({ name: "Alveolar Stage", concept_type: "embryology_stage", primary_domain: "resp",
      short_definition: "Lung development 36wk to ~8yr: septation of saccules into true alveoli (50M→300M)",
      aliases: ["alveolar phase"],
      timeline_positions: ["neonatal_course", "chronic_followup"],
      ring_identity: "36 weeks to ~8 years: septation into true alveoli. 50M at birth → 300M by age 8.",
      ring_associations: "BPD = arrest of alveolarization",
      ring_edge: "New BPD in extremely preterm = arrested saccular→alveolar transition",
      board_weight_score: 0.7,
      query_feature_terms: ["alveolar", "alveolarization", "BPD", "septation"],
    });
    const earlySurfactant = upsertNode({ name: "Early Surfactant Production", concept_type: "physiology", primary_domain: "resp",
      short_definition: "Type II pneumocytes begin producing surfactant during canalicular phase (~20-24 weeks)",
      board_weight_score: 0.5,
      query_feature_terms: ["surfactant production", "type II pneumocyte", "lamellar body"],
    });

    // Timeline edges
    upsertEdge({ source_id: embryonicLung, target_id: pseudoglandular, relation_type: "stage_precedes", weight: 0.9, explanation: "Embryonic → Pseudoglandular (week 5)", sequence_order: 1 });
    upsertEdge({ source_id: pseudoglandular, target_id: canalicular, relation_type: "stage_precedes", weight: 0.9, explanation: "Pseudoglandular → Canalicular (weeks 16-17)", sequence_order: 2 });
    upsertEdge({ source_id: canalicular, target_id: saccular, relation_type: "stage_precedes", weight: 0.9, explanation: "Canalicular → Saccular (weeks 24-26)", sequence_order: 3 });
    upsertEdge({ source_id: saccular, target_id: alveolar, relation_type: "stage_precedes", weight: 0.9, explanation: "Saccular → Alveolar (week 36)", sequence_order: 4 });
    upsertEdge({ source_id: canalicular, target_id: earlySurfactant, relation_type: "associated_with", weight: 0.75, explanation: "Surfactant production begins during canalicular phase" });

    // CPAM / Sequestration
    const cpam = upsertNode({ name: "CPAM", concept_type: "pathology", primary_domain: "resp",
      short_definition: "Congenital Pulmonary Airway Malformation — hamartomatous lung lesion with cystic/solid components",
      aliases: ["congenital pulmonary airway malformation", "CCAM", "congenital cystic adenomatoid malformation"],
      timeline_positions: ["prenatal", "neonatal_course"],
      ring_identity: "Hamartomatous lesion from abnormal branching morphogenesis with cystic and/or solid components.",
      ring_distinctions: "CPAM communicates with airway. Sequestration has systemic arterial supply. #1 board question.",
      ring_edge: "CPAM = airway communication + pulmonary blood supply. Sequestration = no airway + systemic supply.",
      board_weight_score: 0.75,
      query_feature_terms: ["CPAM", "CCAM", "cystic lung", "congenital lung malformation"],
    });
    const sequestration = upsertNode({ name: "Pulmonary Sequestration", concept_type: "pathology", primary_domain: "resp",
      short_definition: "Non-functioning lung tissue with no airway communication, receiving systemic arterial blood supply",
      aliases: ["bronchopulmonary sequestration", "BPS"],
      timeline_positions: ["prenatal", "neonatal_course"],
      ring_identity: "Mass of non-functioning lung tissue lacking tracheobronchial communication, with systemic arterial supply.",
      ring_distinctions: "No airway communication (vs CPAM). Systemic arterial supply (vs pulmonary). Intralobar vs extralobar.",
      ring_edge: "Systemic artery from aorta = pathognomonic. Extralobar → associated with CDH.",
      board_weight_score: 0.65,
      query_feature_terms: ["sequestration", "systemic arterial supply", "feeding vessel aorta"],
    });
    const airwayCommunication = upsertNode({ name: "Airway Communication", concept_type: "imaging_finding", primary_domain: "resp",
      short_definition: "Connection between a lung lesion and the tracheobronchial tree — present in CPAM, absent in sequestration",
      board_weight_score: 0.35,
      query_feature_terms: ["airway communication", "tracheobronchial"],
    });
    const systemicSupply = upsertNode({ name: "Systemic Arterial Supply", concept_type: "imaging_finding", primary_domain: "resp",
      short_definition: "Blood supply from a systemic artery (typically aorta) rather than pulmonary circulation — hallmark of sequestration",
      board_weight_score: 0.4,
      query_feature_terms: ["systemic arterial supply", "feeding vessel", "aorta supply"],
    });

    upsertEdge({ source_id: cpam, target_id: pseudoglandular, relation_type: "developmental_neighbor", weight: 0.65, explanation: "CPAM arises during pseudoglandular-canalicular transition" });
    upsertEdge({ source_id: cpam, target_id: sequestration, relation_type: "distinguished_from", weight: 0.9, explanation: "CPAM: airway communication + pulmonary supply vs Sequestration: no airway + systemic supply" });
    upsertEdge({ source_id: sequestration, target_id: cpam, relation_type: "distinguished_from", weight: 0.9, explanation: "Sequestration lacks airway communication, has systemic arterial supply" });
    upsertEdge({ source_id: cpam, target_id: airwayCommunication, relation_type: "associated_with", weight: 0.85, explanation: "CPAM communicates with tracheobronchial tree" });
    upsertEdge({ source_id: sequestration, target_id: systemicSupply, relation_type: "associated_with", weight: 0.9, explanation: "Sequestration has systemic arterial supply from aorta" });
    upsertEdge({ source_id: cpam, target_id: sequestration, relation_type: "board_trap_vs", weight: 0.8, explanation: "Board loves asking CPAM vs sequestration distinction" });

    // ═══ TRIPLOIDY / PRENATAL SCREENING ═══
    const triploidy = upsertNode({ name: "Triploidy", concept_type: "genetic_mechanism", primary_domain: "gen",
      short_definition: "69 chromosomes (3n). Most common cause: dispermy. Severe IUGR, multiple anomalies, partial molar placenta.",
      aliases: ["69,XXX", "69,XXY", "triploid"],
      secondary_domains: ["mfm"],
      timeline_positions: ["prenatal"],
      ring_identity: "Complete extra set of chromosomes (69 total). Usually lethal. Diandric vs digynic origin affects phenotype.",
      ring_associations: "Severe IUGR, syndactyly, cleft lip/palate, VSD, posterior fossa anomalies, partial mole, low fetal fraction on cfDNA",
      ring_distinctions: "Triploidy missed by cfDNA (low fetal fraction). Compare with trisomy 13, trisomy 18.",
      ring_edge: "Low fetal fraction on cfDNA + severe IUGR + multiple anomalies = think triploidy. cfDNA is NOT a screen for triploidy.",
      board_weight_score: 0.7,
      query_feature_terms: ["triploidy", "69 chromosomes", "low fetal fraction", "partial mole", "severe IUGR syndactyly"],
    });
    const severeIUGR = upsertNode({ name: "Severe IUGR", concept_type: "symptom", primary_domain: "mfm",
      short_definition: "Fetal growth restriction below 3rd percentile or with abnormal Dopplers",
      aliases: ["severe FGR", "severe growth restriction", "IUGR"],
      board_weight_score: 0.6,
      query_feature_terms: ["IUGR", "FGR", "growth restriction", "small for gestational age"],
    });
    const cleftLipPalate = upsertNode({ name: "Cleft Lip/Palate", concept_type: "anatomy", primary_domain: "eent",
      short_definition: "Congenital orofacial cleft; associated with trisomy 13, triploidy, and many syndromes",
      aliases: ["cleft lip", "cleft palate", "orofacial cleft"],
      board_weight_score: 0.5,
      query_feature_terms: ["cleft lip", "cleft palate", "orofacial"],
    });
    const posteriorFossaCyst = upsertNode({ name: "Posterior Fossa Cyst", concept_type: "imaging_finding", primary_domain: "neuro",
      short_definition: "Cystic lesion in posterior fossa; differential includes Dandy-Walker, Blake pouch cyst, mega cisterna magna",
      aliases: ["posterior fossa anomaly"],
      board_weight_score: 0.45,
      query_feature_terms: ["posterior fossa", "Dandy-Walker", "Blake pouch"],
    });
    const vsd = upsertNode({ name: "VSD", concept_type: "disease", primary_domain: "cv",
      short_definition: "Ventricular septal defect — most common congenital heart defect overall",
      aliases: ["ventricular septal defect"],
      ring_edge: "Most common CHD overall (not in preterms — that's PDA). Perimembranous most common type.",
      board_weight_score: 0.7,
      query_feature_terms: ["VSD", "ventricular septal defect"],
    });
    const syndactyly = upsertNode({ name: "Syndactyly", concept_type: "physical_exam_finding", primary_domain: "gen",
      short_definition: "Fusion of digits; associated with triploidy, Apert syndrome, Poland sequence",
      board_weight_score: 0.4,
      query_feature_terms: ["syndactyly", "fused digits", "webbed fingers"],
    });
    const cfdna = upsertNode({ name: "cfDNA Screening", concept_type: "diagnostic_test", primary_domain: "gen",
      short_definition: "Cell-free DNA screening (NIPT) for common aneuploidies; limited by fetal fraction",
      aliases: ["NIPT", "noninvasive prenatal testing", "cell-free DNA"],
      secondary_domains: ["mfm"],
      ring_identity: "Screens for trisomy 21, 18, 13 and sex chromosome aneuploidies using cell-free fetal DNA in maternal blood.",
      ring_distinctions: "Screening test, not diagnostic. Requires adequate fetal fraction (>4%). Does NOT screen for triploidy.",
      ring_edge: "Low fetal fraction → consider triploidy, trisomy 18, obesity, early GA. No-call result needs follow-up.",
      board_weight_score: 0.7,
      query_feature_terms: ["cfDNA", "NIPT", "cell-free DNA", "fetal fraction", "noninvasive prenatal"],
    });
    const lowFetalFraction = upsertNode({ name: "Low Fetal Fraction", concept_type: "lab_pattern", primary_domain: "gen",
      short_definition: "Insufficient fetal DNA in maternal sample (<4%); causes include early GA, obesity, triploidy, trisomy 18",
      aliases: ["low FF", "insufficient fetal fraction"],
      ring_edge: "Low fetal fraction is NOT 'normal negative.' Must be worked up — associated with triploidy and T18.",
      board_weight_score: 0.55,
      query_feature_terms: ["low fetal fraction", "no call NIPT", "insufficient fetal fraction"],
    });
    const trisomy13 = upsertNode({ name: "Trisomy 13", concept_type: "genetic_mechanism", primary_domain: "gen",
      short_definition: "Patau syndrome: holoprosencephaly, cleft lip/palate, polydactyly, cutis aplasia, cardiac defects",
      aliases: ["Patau syndrome", "T13"],
      ring_edge: "Midline defects: holoprosencephaly, cleft, omphalocele. Cutis aplasia of scalp is characteristic.",
      board_weight_score: 0.65,
      query_feature_terms: ["trisomy 13", "Patau", "holoprosencephaly", "cutis aplasia"],
    });
    const trisomy18 = upsertNode({ name: "Trisomy 18", concept_type: "genetic_mechanism", primary_domain: "gen",
      short_definition: "Edwards syndrome: clenched fists, rocker-bottom feet, VSD, IUGR, micrognathia",
      aliases: ["Edwards syndrome", "T18"],
      ring_edge: "Clenched fists with overlapping fingers (2nd over 3rd, 5th over 4th). Also low fetal fraction on cfDNA.",
      board_weight_score: 0.65,
      query_feature_terms: ["trisomy 18", "Edwards", "clenched fists", "rocker-bottom feet"],
    });

    // Triploidy edges
    upsertEdge({ source_id: severeIUGR, target_id: triploidy, relation_type: "suggested_by", weight: 0.7, explanation: "Severe IUGR with multiple anomalies suggests triploidy" });
    upsertEdge({ source_id: cleftLipPalate, target_id: triploidy, relation_type: "associated_with", weight: 0.5, explanation: "Cleft lip/palate associated with triploidy" });
    upsertEdge({ source_id: posteriorFossaCyst, target_id: triploidy, relation_type: "associated_with", weight: 0.5, explanation: "Posterior fossa anomalies seen in triploidy" });
    upsertEdge({ source_id: vsd, target_id: triploidy, relation_type: "associated_with", weight: 0.4, explanation: "VSD associated with triploidy" });
    upsertEdge({ source_id: syndactyly, target_id: triploidy, relation_type: "associated_with", weight: 0.6, explanation: "Syndactyly is characteristic of triploidy" });
    upsertEdge({ source_id: triploidy, target_id: cfdna, relation_type: "missed_by", weight: 0.9, explanation: "cfDNA does not screen for triploidy; results in no-call/low fetal fraction" });
    upsertEdge({ source_id: lowFetalFraction, target_id: triploidy, relation_type: "suggested_by", weight: 0.7, explanation: "Low fetal fraction on cfDNA should raise suspicion for triploidy" });
    upsertEdge({ source_id: lowFetalFraction, target_id: trisomy18, relation_type: "associated_with", weight: 0.5, explanation: "Trisomy 18 also associated with low fetal fraction" });
    upsertEdge({ source_id: cfdna, target_id: lowFetalFraction, relation_type: "limited_by", weight: 0.8, explanation: "cfDNA requires adequate fetal fraction (>4%)" });
    upsertEdge({ source_id: triploidy, target_id: trisomy13, relation_type: "compared_with", weight: 0.6, explanation: "Both have cleft lip and multiple anomalies but triploidy has 69 chromosomes" });
    upsertEdge({ source_id: triploidy, target_id: trisomy18, relation_type: "compared_with", weight: 0.65, explanation: "Both cause IUGR and low fetal fraction but different chromosome count" });
    upsertEdge({ source_id: trisomy13, target_id: trisomy18, relation_type: "compared_with", weight: 0.5, explanation: "Both lethal trisomies but different phenotypes" });

    // Cross-chain pearls
    upsertEdge({ source_id: pda, target_id: vsd, relation_type: "compared_with", weight: 0.5, explanation: "PDA = most common in preterms, VSD = most common overall" });
    upsertEdge({ source_id: pda, target_id: vsd, relation_type: "board_trap_vs", weight: 0.7, explanation: "Board trap: 'most common CHD' = VSD overall, PDA in preterms" });
  });
  tx();

  return NextResponse.json({
    success: true,
    message: "Graph v2 seeded: PDA/arch embryology, rubella associations, lung development timeline, CPAM/sequestration differentials, triploidy/prenatal screening chain",
  });
}
