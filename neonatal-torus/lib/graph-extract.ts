import { getDb } from "./db";
import { upsertNode, upsertEdge } from "./graph-engine";
import type { ConceptType, RelationType } from "./graph-types";

// ═══════════════════════════════════════════════════════════════════
// Auto-extraction: PDF chunks → graph nodes + typed edges
// Rule-based extraction using term dictionaries and pattern matching.
// No external API calls. Everything runs locally.
// ═══════════════════════════════════════════════════════════════════

// ── Term Dictionary ────────────────────────────────────────────────
// Maps recognized medical terms → { concept_type, domain, aliases }

interface TermEntry {
  canonical: string;
  type: ConceptType;
  domain: string;
  aliases: string[];
  features: string[];
  weight: number;
}

const TERM_DICT: TermEntry[] = [
  // Nutrition / breast milk
  { canonical: "Choline", type: "physiology", domain: "nutr", aliases: ["choline"], features: ["choline", "phosphatidylcholine", "acetylcholine"], weight: 0.6 },
  { canonical: "Breast Milk", type: "treatment", domain: "nutr", aliases: ["breast milk", "human milk", "mother's milk", "breastmilk"], features: ["breast milk", "human milk", "lactation"], weight: 0.65 },
  { canonical: "Phosphatidylcholine", type: "physiology", domain: "nutr", aliases: ["phosphatidylcholine", "lecithin"], features: ["phosphatidylcholine", "lecithin", "cell membrane"], weight: 0.45 },
  { canonical: "Acetylcholine", type: "physiology", domain: "neuro", aliases: ["acetylcholine", "ACh"], features: ["acetylcholine", "neuromuscular", "cholinergic"], weight: 0.5 },
  { canonical: "TPN", type: "treatment", domain: "nutr", aliases: ["TPN", "total parenteral nutrition", "parenteral nutrition"], features: ["TPN", "parenteral", "IV nutrition"], weight: 0.6 },
  { canonical: "NEC", type: "disease", domain: "gi", aliases: ["NEC", "necrotizing enterocolitis"], features: ["NEC", "necrotizing", "pneumatosis", "portal venous gas"], weight: 0.85 },
  // Respiratory
  { canonical: "Surfactant", type: "treatment", domain: "resp", aliases: ["surfactant", "exogenous surfactant"], features: ["surfactant", "DPPC", "type II pneumocyte"], weight: 0.8 },
  { canonical: "RDS", type: "disease", domain: "resp", aliases: ["RDS", "respiratory distress syndrome", "hyaline membrane disease"], features: ["RDS", "respiratory distress", "ground glass", "air bronchograms"], weight: 0.85 },
  { canonical: "BPD", type: "disease", domain: "resp", aliases: ["BPD", "bronchopulmonary dysplasia", "chronic lung disease"], features: ["BPD", "bronchopulmonary", "chronic lung", "oxygen at 36 weeks"], weight: 0.8 },
  { canonical: "Apnea of Prematurity", type: "disease", domain: "resp", aliases: ["apnea of prematurity", "AOP"], features: ["apnea", "caffeine", "methylxanthine", "periodic breathing"], weight: 0.7 },
  { canonical: "CPAP", type: "treatment", domain: "resp", aliases: ["CPAP", "continuous positive airway pressure", "nasal CPAP", "nCPAP"], features: ["CPAP", "continuous positive", "noninvasive"], weight: 0.6 },
  { canonical: "Pneumothorax", type: "disease", domain: "resp", aliases: ["pneumothorax", "air leak"], features: ["pneumothorax", "air leak", "chest tube", "needle decompression"], weight: 0.65 },
  // Cardiovascular
  { canonical: "PDA", type: "disease", domain: "cv", aliases: ["PDA", "patent ductus arteriosus"], features: ["PDA", "patent ductus", "machinery murmur", "ductus arteriosus"], weight: 0.9 },
  { canonical: "VSD", type: "disease", domain: "cv", aliases: ["VSD", "ventricular septal defect"], features: ["VSD", "ventricular septal", "holosystolic murmur"], weight: 0.7 },
  { canonical: "ASD", type: "disease", domain: "cv", aliases: ["ASD", "atrial septal defect"], features: ["ASD", "atrial septal", "fixed split S2"], weight: 0.55 },
  { canonical: "Coarctation of the Aorta", type: "disease", domain: "cv", aliases: ["coarctation", "CoA"], features: ["coarctation", "upper extremity hypertension", "rib notching", "bicuspid aortic valve"], weight: 0.7 },
  { canonical: "PPHN", type: "disease", domain: "cv", aliases: ["PPHN", "persistent pulmonary hypertension"], features: ["PPHN", "pulmonary hypertension", "nitric oxide", "iNO"], weight: 0.75 },
  { canonical: "Tetralogy of Fallot", type: "disease", domain: "cv", aliases: ["TOF", "tetralogy of Fallot", "tet of Fallot"], features: ["tetralogy", "Fallot", "tet spell", "boot-shaped heart", "overriding aorta"], weight: 0.7 },
  // Neurology
  { canonical: "IVH", type: "disease", domain: "neuro", aliases: ["IVH", "intraventricular hemorrhage"], features: ["IVH", "intraventricular", "germinal matrix", "grade I-IV"], weight: 0.8 },
  { canonical: "PVL", type: "disease", domain: "neuro", aliases: ["PVL", "periventricular leukomalacia"], features: ["PVL", "periventricular", "white matter", "leukomalacia"], weight: 0.7 },
  { canonical: "HIE", type: "disease", domain: "asphyx", aliases: ["HIE", "hypoxic-ischemic encephalopathy"], features: ["HIE", "hypoxic-ischemic", "cooling", "therapeutic hypothermia", "Sarnat"], weight: 0.85 },
  { canonical: "Seizures (Neonatal)", type: "symptom", domain: "neuro", aliases: ["neonatal seizures", "seizures"], features: ["seizure", "EEG", "phenobarbital", "subtle seizure", "clonic"], weight: 0.7 },
  { canonical: "Myasthenia Gravis (Neonatal)", type: "disease", domain: "neuro", aliases: ["neonatal myasthenia", "transient neonatal MG"], features: ["myasthenia", "hypotonia", "ptosis", "weak cry", "acetylcholine receptor"], weight: 0.55 },
  // Infectious
  { canonical: "Sepsis (Neonatal)", type: "disease", domain: "id", aliases: ["neonatal sepsis", "early-onset sepsis", "late-onset sepsis", "EOS", "LOS"], features: ["sepsis", "blood culture", "antibiotics", "GBS", "E. coli"], weight: 0.85 },
  { canonical: "GBS", type: "infectious_agent", domain: "id", aliases: ["GBS", "group B streptococcus", "Streptococcus agalactiae"], features: ["GBS", "group B strep", "IAP", "intrapartum"], weight: 0.75 },
  { canonical: "CMV", type: "infectious_agent", domain: "id", aliases: ["CMV", "cytomegalovirus", "congenital CMV"], features: ["CMV", "cytomegalovirus", "periventricular calcifications", "hearing loss"], weight: 0.65 },
  { canonical: "Congenital Rubella", type: "infectious_agent", domain: "id", aliases: ["rubella", "congenital rubella syndrome", "CRS"], features: ["rubella", "cataracts", "PDA", "blueberry muffin"], weight: 0.7 },
  // Hematology
  { canonical: "Neonatal Jaundice", type: "disease", domain: "bili", aliases: ["jaundice", "hyperbilirubinemia", "neonatal jaundice"], features: ["jaundice", "bilirubin", "phototherapy", "exchange transfusion", "kernicterus"], weight: 0.8 },
  { canonical: "Polycythemia", type: "disease", domain: "heme", aliases: ["polycythemia", "neonatal polycythemia"], features: ["polycythemia", "hematocrit", "partial exchange", "hyperviscosity"], weight: 0.5 },
  { canonical: "DIC", type: "disease", domain: "heme", aliases: ["DIC", "disseminated intravascular coagulation"], features: ["DIC", "disseminated intravascular", "coagulopathy", "fibrinogen"], weight: 0.6 },
  // Genetics
  { canonical: "Trisomy 21", type: "genetic_mechanism", domain: "gen", aliases: ["trisomy 21", "Down syndrome", "T21"], features: ["trisomy 21", "Down", "Brushfield spots", "sandal gap", "duodenal atresia"], weight: 0.7 },
  { canonical: "Trisomy 18", type: "genetic_mechanism", domain: "gen", aliases: ["trisomy 18", "Edwards syndrome", "T18"], features: ["trisomy 18", "Edwards", "clenched fists", "rocker-bottom feet"], weight: 0.65 },
  { canonical: "Trisomy 13", type: "genetic_mechanism", domain: "gen", aliases: ["trisomy 13", "Patau syndrome", "T13"], features: ["trisomy 13", "Patau", "holoprosencephaly", "cutis aplasia"], weight: 0.65 },
  { canonical: "DiGeorge Syndrome", type: "syndrome", domain: "gen", aliases: ["DiGeorge", "22q11 deletion", "velocardiofacial"], features: ["DiGeorge", "22q11", "thymic aplasia", "hypocalcemia", "truncus"], weight: 0.65 },
  // Endocrine
  { canonical: "Neonatal Hypoglycemia", type: "disease", domain: "endo", aliases: ["hypoglycemia", "neonatal hypoglycemia", "low blood sugar"], features: ["hypoglycemia", "glucose", "dextrose", "IDM", "SGA"], weight: 0.75 },
  { canonical: "Congenital Hypothyroidism", type: "disease", domain: "endo", aliases: ["congenital hypothyroidism", "CH"], features: ["hypothyroid", "TSH", "T4", "newborn screen", "thyroid"], weight: 0.65 },
  // Renal
  { canonical: "Posterior Urethral Valves", type: "disease", domain: "renal", aliases: ["PUV", "posterior urethral valves"], features: ["posterior urethral", "hydronephrosis", "oligohydramnios", "keyhole sign"], weight: 0.55 },
  // GI
  { canonical: "Hirschsprung Disease", type: "disease", domain: "gi", aliases: ["Hirschsprung", "Hirschsprung disease", "congenital megacolon"], features: ["Hirschsprung", "aganglionic", "transition zone", "suction biopsy", "delayed meconium"], weight: 0.65 },
  { canonical: "Malrotation", type: "disease", domain: "gi", aliases: ["malrotation", "intestinal malrotation"], features: ["malrotation", "volvulus", "bilious emesis", "Ladd bands", "upper GI"], weight: 0.7 },
  // Pharmacology
  { canonical: "Indomethacin", type: "pharmacology", domain: "pharm", aliases: ["indomethacin", "indocin"], features: ["indomethacin", "COX inhibitor", "PDA closure", "NSAID"], weight: 0.6 },
  { canonical: "Caffeine", type: "pharmacology", domain: "pharm", aliases: ["caffeine", "caffeine citrate"], features: ["caffeine", "methylxanthine", "apnea", "AOP"], weight: 0.6 },
  { canonical: "Prostaglandin E1", type: "pharmacology", domain: "pharm", aliases: ["PGE1", "prostaglandin E1", "alprostadil"], features: ["PGE1", "prostaglandin", "ductal-dependent", "ductus open"], weight: 0.65 },
  // MFM
  { canonical: "Preeclampsia", type: "disease", domain: "mfm", aliases: ["preeclampsia", "pre-eclampsia", "toxemia"], features: ["preeclampsia", "hypertension", "proteinuria", "HELLP", "magnesium sulfate"], weight: 0.7 },
  { canonical: "Chorioamnionitis", type: "disease", domain: "mfm", aliases: ["chorioamnionitis", "intraamniotic infection"], features: ["chorioamnionitis", "maternal fever", "foul-smelling", "funisitis"], weight: 0.65 },
  { canonical: "Magnesium Sulfate", type: "pharmacology", domain: "mfm", aliases: ["magnesium sulfate", "MgSO4", "mag sulfate"], features: ["magnesium sulfate", "tocolytic", "neuroprotection", "preeclampsia", "contractions"], weight: 0.6 },
];

// ── Relationship Patterns ──────────────────────────────────────────

interface RelPattern {
  pattern: RegExp;
  type: RelationType;
  extractTarget?: boolean; // whether the second term is the target
}

const REL_PATTERNS: RelPattern[] = [
  // "X is treated with Y" / "treatment of X includes Y"
  { pattern: /\btreated?\s+(?:with|by|using)\b/i, type: "treated_with" },
  { pattern: /\btreatment\s+(?:of|for|includes?)\b/i, type: "treated_with" },
  { pattern: /\bmanage[ds]?\s+(?:with|by)\b/i, type: "managed_with" },
  // "X causes Y" / "X leads to Y"
  { pattern: /\bcauses?\b/i, type: "causes" },
  { pattern: /\bleads?\s+to\b/i, type: "causes" },
  { pattern: /\bresults?\s+in\b/i, type: "causes" },
  // "X is associated with Y"
  { pattern: /\bassociated\s+with\b/i, type: "associated_with" },
  { pattern: /\bcomplication[s]?\s+(?:of|include)\b/i, type: "associated_with" },
  // "X presents with Y"
  { pattern: /\bpresents?\s+with\b/i, type: "presents_with" },
  { pattern: /\bcharacterized\s+by\b/i, type: "presents_with" },
  { pattern: /\bmanifests?\s+(?:as|with)\b/i, type: "presents_with" },
  // "X is distinguished from Y"
  { pattern: /\bdistinguish\w*\s+from\b/i, type: "distinguished_from" },
  { pattern: /\bin\s+contrast\s+to\b/i, type: "distinguished_from" },
  { pattern: /\bvs\.?\b/i, type: "compared_with" },
  { pattern: /\bversus\b/i, type: "compared_with" },
  // "X is a component of Y" / "X is found in Y"
  { pattern: /\bcomponent\s+of\b/i, type: "part_of" },
  { pattern: /\bfound\s+in\b/i, type: "located_in" },
  { pattern: /\bsource\s+of\b/i, type: "associated_with" },
  { pattern: /\bcontains?\b/i, type: "associated_with" },
  // "X is important for Y" / "required for Y"
  { pattern: /\bimportant\s+for\b/i, type: "contributes_to" },
  { pattern: /\brequired\s+for\b/i, type: "depends_on" },
  { pattern: /\bessential\s+for\b/i, type: "depends_on" },
  { pattern: /\bnecessary\s+for\b/i, type: "depends_on" },
  // "X is a precursor of Y"
  { pattern: /\bprecursor\s+(?:of|to)\b/i, type: "develops_into" },
  { pattern: /\bconverted\s+(?:to|into)\b/i, type: "develops_into" },
  // "X is screened by Y" / "diagnosed by Y"
  { pattern: /\bscreened?\s+(?:by|with|using)\b/i, type: "screened_by" },
  { pattern: /\bdiagnos\w+\s+(?:by|with|using)\b/i, type: "diagnosed_by" },
  // "X increases/decreases Y"
  { pattern: /\bincreases?\b/i, type: "increases" },
  { pattern: /\bdecreases?\b/i, type: "decreases" },
  { pattern: /\binhibits?\b/i, type: "decreases" },
  // "X is contraindicated in Y"
  { pattern: /\bcontraindicated\b/i, type: "contraindicated_with" },
];

// ── Main Extraction Function ───────────────────────────────────────

export function extractGraphFromChunks(options?: {
  documentId?: number;
  limit?: number;
}): { nodesCreated: number; edgesCreated: number; chunksProcessed: number } {
  const db = getDb();

  let query = "SELECT id, text, domain_primary FROM chunks";
  const params: (string | number)[] = [];
  if (options?.documentId) {
    query += " WHERE document_id = ?";
    params.push(options.documentId);
  }
  query += ` ORDER BY id LIMIT ${options?.limit || 5000}`;

  const chunks = db.prepare(query).all(...params) as Array<{
    id: number;
    text: string;
    domain_primary: string | null;
  }>;

  let nodesCreated = 0;
  let edgesCreated = 0;

  // Pass 1: Extract nodes — find recognized terms in chunks
  const termHits = new Map<string, { entry: TermEntry; chunkIds: number[]; contexts: string[] }>();

  for (const chunk of chunks) {
    const textLower = chunk.text.toLowerCase();

    for (const entry of TERM_DICT) {
      const allTerms = [entry.canonical.toLowerCase(), ...entry.aliases.map((a) => a.toLowerCase())];

      for (const term of allTerms) {
        if (textLower.includes(term)) {
          const existing = termHits.get(entry.canonical) || { entry, chunkIds: [], contexts: [] };
          if (!existing.chunkIds.includes(chunk.id)) {
            existing.chunkIds.push(chunk.id);
            // Extract a context sentence
            const idx = textLower.indexOf(term);
            const start = Math.max(0, chunk.text.lastIndexOf(".", idx - 1) + 1);
            const end = Math.min(chunk.text.length, chunk.text.indexOf(".", idx + term.length) + 1 || idx + 150);
            existing.contexts.push(chunk.text.substring(start, end).trim());
          }
          termHits.set(entry.canonical, existing);
          break; // Found this entry, move on
        }
      }
    }
  }

  // Create nodes for terms found in chunks
  const nodeIdMap = new Map<string, number>();

  for (const [canonical, hit] of termHits) {
    // Build definition from first few contexts
    const definition = hit.contexts.slice(0, 3).join(" ").substring(0, 300);

    const nodeId = upsertNode({
      name: canonical,
      concept_type: hit.entry.type,
      primary_domain: hit.entry.domain,
      aliases: hit.entry.aliases,
      short_definition: definition || undefined,
      board_weight_score: hit.entry.weight,
      query_feature_terms: hit.entry.features,
    });

    // Update density_score based on how many chunks mention this term
    db.prepare("UPDATE graph_nodes SET density_score = ?, evidence_count = ? WHERE id = ?")
      .run(Math.min(hit.chunkIds.length / 10, 1.0), hit.chunkIds.length, nodeId);

    nodeIdMap.set(canonical, nodeId);
    nodesCreated++;
  }

  // Pass 2: Extract edges — find co-occurring terms and relationship patterns
  for (const chunk of chunks) {
    const textLower = chunk.text.toLowerCase();

    // Find all terms present in this chunk
    const presentTerms: string[] = [];
    for (const [canonical, hit] of termHits) {
      const allTerms = [canonical.toLowerCase(), ...hit.entry.aliases.map((a) => a.toLowerCase())];
      if (allTerms.some((t) => textLower.includes(t))) {
        presentTerms.push(canonical);
      }
    }

    if (presentTerms.length < 2) continue;

    // For each pair of terms in the same chunk, try to find a typed relationship
    for (let i = 0; i < presentTerms.length; i++) {
      for (let j = i + 1; j < presentTerms.length; j++) {
        const termA = presentTerms[i];
        const termB = presentTerms[j];
        const nodeA = nodeIdMap.get(termA);
        const nodeB = nodeIdMap.get(termB);
        if (!nodeA || !nodeB) continue;

        // Find the text between the two terms
        const aEntry = termHits.get(termA)!.entry;
        const bEntry = termHits.get(termB)!.entry;
        const aTerms = [aEntry.canonical.toLowerCase(), ...aEntry.aliases.map((s) => s.toLowerCase())];
        const bTerms = [bEntry.canonical.toLowerCase(), ...bEntry.aliases.map((s) => s.toLowerCase())];

        let posA = -1, posB = -1;
        for (const t of aTerms) { const p = textLower.indexOf(t); if (p >= 0 && (posA < 0 || p < posA)) posA = p; }
        for (const t of bTerms) { const p = textLower.indexOf(t); if (p >= 0 && (posB < 0 || p < posB)) posB = p; }

        if (posA < 0 || posB < 0) continue;

        // Get the text between them (or nearby)
        const minPos = Math.min(posA, posB);
        const maxPos = Math.max(posA, posB);
        const between = chunk.text.substring(minPos, Math.min(maxPos + 50, chunk.text.length));

        // Try to match a relationship pattern
        let matched = false;
        for (const rp of REL_PATTERNS) {
          if (rp.pattern.test(between)) {
            const sourceId = posA < posB ? nodeA : nodeB;
            const targetId = posA < posB ? nodeB : nodeA;

            upsertEdge({
              source_id: sourceId,
              target_id: targetId,
              relation_type: rp.type,
              weight: 0.5,
              confidence: 0.6,
              explanation: between.substring(0, 150).trim(),
            });
            edgesCreated++;
            matched = true;
            break;
          }
        }

        // If no pattern matched but terms co-occur, create a generic association
        if (!matched) {
          upsertEdge({
            source_id: nodeA,
            target_id: nodeB,
            relation_type: "associated_with",
            weight: 0.3,
            confidence: 0.4,
            explanation: `Co-occur in source text: "${between.substring(0, 100).trim()}"`,
          });
          edgesCreated++;
        }
      }
    }
  }

  return { nodesCreated, edgesCreated, chunksProcessed: chunks.length };
}
