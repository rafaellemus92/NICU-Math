const DOMAIN_KEYWORDS: Record<string, string[]> = {
  mfm: [
    "maternal", "fetal", "placenta", "preeclampsia", "chorioamnionitis",
    "gestational", "prenatal", "obstetric", "amniotic", "umbilical cord",
    "preterm labor", "PPROM", "oligohydramnios", "polyhydramnios",
    "intrauterine growth", "IUGR", "SGA", "LGA", "twin-twin", "TTTS",
  ],
  asphyx: [
    "asphyxia", "resuscitation", "Apgar", "HIE", "hypoxic-ischemic",
    "encephalopathy", "cooling", "hypothermia", "NRP", "meconium aspiration",
    "perinatal depression", "cord gas", "base deficit",
  ],
  cv: [
    "PDA", "patent ductus", "coarctation", "tetralogy", "Fallot",
    "transposition", "VSD", "ASD", "cardiac", "heart", "prostaglandin",
    "indomethacin", "ibuprofen", "echocardiography", "murmur",
    "hypoplastic left", "truncus", "aortic", "pulmonary hypertension", "PPHN",
  ],
  resp: [
    "surfactant", "ventilator", "BPD", "bronchopulmonary dysplasia", "RDS",
    "respiratory distress", "CPAP", "pneumothorax", "intubation", "extubation",
    "tracheal", "oxygen", "FiO2", "HFOV", "high-frequency", "apnea",
    "caffeine", "lung", "alveolar", "tidal volume",
  ],
  gen: [
    "trisomy", "karyotype", "deletion", "autosomal", "X-linked",
    "chromosome", "genetic", "syndrome", "dysmorphic", "congenital anomaly",
    "microarray", "mutation", "gene", "inheritance", "recessive", "dominant",
    "DiGeorge", "Turner", "Down syndrome", "Edward",
  ],
  nutr: [
    "nutrition", "feeding", "breast milk", "formula", "TPN",
    "parenteral nutrition", "enteral", "calorie", "protein", "lipid",
    "carnitine", "vitamin", "mineral", "growth", "fortifier", "NEC prevention",
    "gavage", "oral feeding",
  ],
  renal: [
    "renal", "kidney", "sodium", "potassium", "electrolyte", "fluid",
    "dehydration", "oliguria", "creatinine", "GFR", "hyponatremia",
    "hyperkalemia", "diuretic", "furosemide", "hydronephrosis",
    "posterior urethral", "multicystic",
  ],
  endo: [
    "thyroid", "cortisol", "adrenal", "glucose", "hypoglycemia",
    "hyperglycemia", "insulin", "calcium", "phosphorus", "parathyroid",
    "temperature", "thermoregulation", "hypothermia", "metabolic",
    "newborn screen", "CAH", "congenital adrenal",
  ],
  immuno: [
    "immune", "immunoglobulin", "IgG", "IgA", "IgM", "T-cell", "B-cell",
    "neutrophil", "lymphocyte", "SCID", "immunodeficiency", "complement",
    "antibody", "vaccination",
  ],
  id: [
    "sepsis", "meningitis", "infection", "antibiotic", "GBS",
    "group B strep", "TORCH", "CMV", "cytomegalovirus", "herpes", "HSV",
    "syphilis", "toxoplasmosis", "rubella", "HIV", "fungal", "candida",
    "coagulase-negative", "bacteremia",
  ],
  gi: [
    "NEC", "necrotizing enterocolitis", "malrotation", "volvulus", "atresia",
    "Hirschsprung", "meconium ileus", "omphalocele", "gastroschisis",
    "intestinal", "bowel", "feeding intolerance", "bilious", "obstruction",
    "esophageal atresia", "TEF",
  ],
  bili: [
    "bilirubin", "jaundice", "phototherapy", "kernicterus", "exchange transfusion",
    "conjugated", "unconjugated", "direct", "indirect", "Coombs",
    "hemolytic", "Rh", "ABO incompatibility", "G6PD", "Crigler-Najjar",
  ],
  skin: [
    "skin", "rash", "dermatitis", "hemangioma", "nevus", "epidermolysis",
    "ichthyosis", "collodion", "erythema toxicum", "pustular melanosis",
    "cutis marmorata",
  ],
  heme: [
    "anemia", "polycythemia", "thrombocytopenia", "platelet", "coagulation",
    "DIC", "bleeding", "transfusion", "hemoglobin", "hematocrit",
    "reticulocyte", "iron", "erythropoietin", "leukemia", "tumor",
    "neuroblastoma", "teratoma",
  ],
  neuro: [
    "seizure", "EEG", "IVH", "intraventricular hemorrhage", "PVL",
    "periventricular", "hydrocephalus", "shunt", "fontanelle", "cranial",
    "ultrasound", "MRI", "brain", "cerebral", "neural tube", "myelomeningocele",
    "spina bifida", "tone", "hypotonia",
  ],
  ndo: [
    "developmental", "follow-up", "Bayley", "neurodevelopmental", "outcome",
    "cerebral palsy", "hearing", "vision", "ROP screening", "early intervention",
    "developmental delay", "milestone",
  ],
  eent: [
    "ROP", "retinopathy", "hearing screening", "ABR", "OAE", "choanal",
    "cleft palate", "cleft lip", "Pierre Robin", "ear", "eye", "cataract",
    "glaucoma", "nasolacrimal", "subglottic", "laryngomalacia",
  ],
  pharm: [
    "pharmacology", "drug", "dosing", "half-life", "clearance", "metabolism",
    "cytochrome", "P450", "renal clearance", "hepatic", "therapeutic",
    "toxicity", "drug interaction", "pharmacokinetics",
  ],
  ethics: [
    "ethics", "palliative", "end-of-life", "counseling", "consent",
    "viability", "periviable", "prognosis", "shared decision", "DNR",
    "withdrawal", "comfort care", "disparities", "quality of life",
  ],
  qi: [
    "quality improvement", "QI", "statistics", "p-value", "confidence interval",
    "odds ratio", "relative risk", "NNT", "sensitivity", "specificity",
    "study design", "RCT", "randomized", "meta-analysis", "systematic review",
    "evidence-based", "Cochrane",
  ],
};

const RING_PATTERNS: Record<string, RegExp[]> = {
  identity: [
    /\bis\s+(?:a|an|the)\b/i,
    /\bdefined\s+as\b/i,
    /\bcharacterized\s+by\b/i,
    /\brefers\s+to\b/i,
    /\bdefinition\b/i,
  ],
  taxonomy: [
    /\bclassified\s+as\b/i,
    /\btypes?\s+(?:include|of)\b/i,
    /\bcategories\b/i,
    /\bstages?\s+(?:of|include)\b/i,
    /\bgrade\s+[IVX1-4]/i,
    /\bseverity\b/i,
  ],
  associations: [
    /\bassociated\s+with\b/i,
    /\bcomplications?\s+(?:include|of)\b/i,
    /\bcomorbidit/i,
    /\brisk\s+factors?\b/i,
    /\bcommonly\s+(?:seen|found|occurs)\b/i,
  ],
  distinctions: [
    /\bdifferential\s+diagnosis\b/i,
    /\bdistinguished\s+from\b/i,
    /\bin\s+contrast\s+to\b/i,
    /\bversus\b/i,
    /\bvs\.?\b/i,
    /\bunlike\b/i,
    /\bdifference\s+between\b/i,
  ],
  edge: [
    /\bnotably\b/i,
    /\bimportantly\b/i,
    /\brare\b/i,
    /\bexception\b/i,
    /\bpearl\b/i,
    /\bhigh[- ]yield\b/i,
    /\bboard\b/i,
    /\bpathognomonic\b/i,
  ],
};

export function detectDomains(text: string): { primary: string | null; secondary: string[] } {
  const lower = text.toLowerCase();
  const scores: Record<string, number> = {};

  for (const [domain, keywords] of Object.entries(DOMAIN_KEYWORDS)) {
    let score = 0;
    for (const kw of keywords) {
      const kwLower = kw.toLowerCase();
      // Count occurrences
      let idx = 0;
      while ((idx = lower.indexOf(kwLower, idx)) !== -1) {
        score++;
        idx += kwLower.length;
      }
    }
    if (score > 0) scores[domain] = score;
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  if (sorted.length === 0) return { primary: null, secondary: [] };

  return {
    primary: sorted[0][0],
    secondary: sorted.slice(1, 4).map(([d]) => d),
  };
}

export function detectRing(text: string): string | null {
  const scores: Record<string, number> = {};

  for (const [ring, patterns] of Object.entries(RING_PATTERNS)) {
    let score = 0;
    for (const pat of patterns) {
      const matches = text.match(new RegExp(pat, "gi"));
      if (matches) score += matches.length;
    }
    if (score > 0) scores[ring] = score;
  }

  const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return sorted.length > 0 ? sorted[0][0] : null;
}
