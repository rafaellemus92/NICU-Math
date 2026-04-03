// ═══════════════════════════════════════════════════════════════════
// Neonatal Torus Graph Type System
// ═══════════════════════════════════════════════════════════════════

// ── Concept Types ──────────────────────────────────────────────────

export const CONCEPT_TYPES = [
  "syndrome", "disease", "anatomy", "embryology_stage", "physiology",
  "pathology", "imaging_finding", "physical_exam_finding", "symptom",
  "diagnostic_test", "lab_pattern", "treatment", "pharmacology",
  "procedure", "differential", "infectious_agent", "genetic_mechanism",
  "developmental_process", "risk_factor", "outcome", "board_pearl",
] as const;
export type ConceptType = (typeof CONCEPT_TYPES)[number];

// ── Timeline Tags ──────────────────────────────────────────────────

export const TIMELINE_TAGS = [
  "preconception", "embryology", "prenatal", "delivery_room",
  "first_minutes", "first_24h", "first_week", "neonatal_course",
  "chronic_followup",
] as const;
export type TimelineTag = (typeof TIMELINE_TAGS)[number];

// ── Relation Types ─────────────────────────────────────────────────

export const RELATION_TYPES = [
  // Structural / foundational
  "part_of", "develops_into", "arises_from", "branch_of",
  "located_in", "associated_with",
  // Embryology / development
  "embryology_precedes", "embryology_contrast", "stage_precedes",
  "stage_follows", "developmental_neighbor", "congenital_result_of",
  // Physiology / mechanism
  "causes", "contributes_to", "mediated_by", "physiologic_contrast",
  "increases", "decreases", "maintains", "closes", "shunts_to", "depends_on",
  // Differential reasoning
  "mimic_of", "distinguished_from", "compared_with",
  "board_trap_vs", "often_confused_with",
  // Clinical presentation
  "presents_with", "associated_exam_finding", "associated_imaging",
  "associated_lab_pattern", "associated_history", "associated_risk_factor",
  // Diagnostics
  "screened_by", "diagnosed_by", "suggested_by",
  "confirmed_by", "missed_by", "limited_by",
  // Treatment / management
  "treated_with", "managed_with", "responsive_to",
  "unresponsive_to", "contraindicated_with", "requires",
  // Infectious / teratogenic / maternal-fetal
  "caused_by_infection", "associated_with_teratogen",
  "maternal_association", "prenatal_screening_association",
  // Educational / board logic
  "pearl_for", "high_yield_neighbor",
  "same_cluster_as", "puncture_neighbor",
] as const;
export type RelationType = (typeof RELATION_TYPES)[number];

// ── Traversal Modes ────────────────────────────────────────────────

export const TRAVERSAL_MODES = {
  embryology: {
    label: "Embryology",
    icon: "E",
    color: "#818CF8",
    description: "Developmental origin chains",
    relations: [
      "arises_from", "develops_into", "embryology_precedes",
      "embryology_contrast", "congenital_result_of", "developmental_neighbor",
    ] as RelationType[],
  },
  timeline: {
    label: "Timeline",
    icon: "T",
    color: "#34D399",
    description: "Developmental stages in sequence",
    relations: [
      "stage_precedes", "stage_follows", "developmental_neighbor",
      "associated_history",
    ] as RelationType[],
  },
  physiology: {
    label: "Physiology",
    icon: "P",
    color: "#3B82F6",
    description: "Physiologic mechanism paths",
    relations: [
      "causes", "contributes_to", "mediated_by", "increases",
      "decreases", "maintains", "shunts_to", "depends_on",
    ] as RelationType[],
  },
  differential: {
    label: "Differentials",
    icon: "D",
    color: "#EF4444",
    description: "Differential reasoning chains",
    relations: [
      "mimic_of", "distinguished_from", "compared_with",
      "board_trap_vs", "often_confused_with",
    ] as RelationType[],
  },
  diagnosis: {
    label: "Diagnosis",
    icon: "Dx",
    color: "#FBBF24",
    description: "Diagnostic workup paths",
    relations: [
      "screened_by", "diagnosed_by", "suggested_by",
      "confirmed_by", "missed_by", "limited_by",
    ] as RelationType[],
  },
  management: {
    label: "Management",
    icon: "Rx",
    color: "#F472B6",
    description: "Treatment and management paths",
    relations: [
      "treated_with", "managed_with", "responsive_to",
      "unresponsive_to", "contraindicated_with", "requires",
    ] as RelationType[],
  },
  maternal_fetal: {
    label: "Maternal-Fetal",
    icon: "MF",
    color: "#C084FC",
    description: "Maternal-fetal associations",
    relations: [
      "maternal_association", "prenatal_screening_association",
      "associated_with_teratogen", "caused_by_infection",
    ] as RelationType[],
  },
  infectious: {
    label: "Infectious",
    icon: "ID",
    color: "#FB923C",
    description: "Infectious associations",
    relations: [
      "caused_by_infection", "associated_with", "presents_with",
      "associated_exam_finding",
    ] as RelationType[],
  },
  pearl: {
    label: "Pearls",
    icon: "*",
    color: "#F59E0B",
    description: "Board pearls and high-yield connections",
    relations: [
      "pearl_for", "high_yield_neighbor",
      "puncture_neighbor", "board_trap_vs",
    ] as RelationType[],
  },
} as const;

export type TraversalMode = keyof typeof TRAVERSAL_MODES;

// ── Feature Types (for query parsing) ──────────────────────────────

export const FEATURE_TYPES = [
  "age_gestation", "timeline", "physical_exam", "imaging",
  "anatomy", "cardiac", "neurologic", "dysmorphism", "growth",
  "prenatal_screening", "lab", "management", "free_text",
] as const;
export type FeatureType = (typeof FEATURE_TYPES)[number];

// ── Graph Node interface ───────────────────────────────────────────

export interface GraphNode {
  id: number;
  slug: string;
  name: string;
  aliases: string[];
  concept_type: ConceptType;
  short_definition: string | null;
  primary_domain: string;
  secondary_domains: string[];
  board_weight_score: number;
  density_score: number;
  timeline_positions: TimelineTag[];
  ring_identity: string | null;
  ring_taxonomy: string | null;
  ring_associations: string | null;
  ring_distinctions: string | null;
  ring_edge: string | null;
  evidence_count: number;
  query_feature_terms: string[];
  hidden: boolean;
}

// ── Graph Edge interface ───────────────────────────────────────────

export interface GraphEdge {
  id: number;
  source_id: number;
  target_id: number;
  relation_type: RelationType;
  weight: number;
  confidence: number;
  directional: boolean;
  label: string | null;
  explanation: string | null;
  query_boost_terms: string[];
  hidden: boolean;
  sequence_order: number | null;
}

// ── Query feature ──────────────────────────────────────────────────

export interface QueryFeature {
  term: string;
  normalized_term: string;
  feature_type: FeatureType;
  matched_node_ids: number[];
  confidence: number;
}

// ── Focused torus state ────────────────────────────────────────────

export interface FocusedTorusState {
  query: string;
  parsed_features: QueryFeature[];
  focus_node: GraphNode | null;
  top_differentials: Array<{ node: GraphNode; score: number; reason: string }>;
  dominant_domains: Array<{ domain: string; score: number }>;
  active_edges: GraphEdge[];
  suggested_jump_points: Array<{ node_id: number; mode: TraversalMode; reason: string }>;
  active_pathways: Partial<Record<TraversalMode, number[]>>;
  torus_heat: Array<{ node_id: number; intensity: number }>;
}
