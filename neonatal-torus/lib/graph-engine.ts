import { getDb } from "./db";
import type {
  GraphNode, GraphEdge, QueryFeature, FocusedTorusState,
  ConceptType, TimelineTag, RelationType, TraversalMode, FeatureType,
} from "./graph-types";
import { TRAVERSAL_MODES } from "./graph-types";

// ── Row → Object helpers ───────────────────────────────────────────

function parseJson<T>(val: string | null, fallback: T): T {
  if (!val) return fallback;
  try { return JSON.parse(val); } catch { return fallback; }
}

function rowToNode(row: Record<string, unknown>): GraphNode {
  return {
    id: row.id as number,
    slug: row.slug as string,
    name: row.name as string,
    aliases: parseJson(row.aliases as string | null, []),
    concept_type: row.concept_type as ConceptType,
    short_definition: (row.short_definition as string) || null,
    primary_domain: row.primary_domain as string,
    secondary_domains: parseJson(row.secondary_domains as string | null, []),
    board_weight_score: (row.board_weight_score as number) || 0.5,
    density_score: (row.density_score as number) || 0,
    timeline_positions: parseJson(row.timeline_positions as string | null, []),
    ring_identity: (row.ring_identity as string) || null,
    ring_taxonomy: (row.ring_taxonomy as string) || null,
    ring_associations: (row.ring_associations as string) || null,
    ring_distinctions: (row.ring_distinctions as string) || null,
    ring_edge: (row.ring_edge as string) || null,
    evidence_count: (row.evidence_count as number) || 0,
    query_feature_terms: parseJson(row.query_feature_terms as string | null, []),
    hidden: !!(row.hidden as number),
  };
}

function rowToEdge(row: Record<string, unknown>): GraphEdge {
  return {
    id: row.id as number,
    source_id: row.source_id as number,
    target_id: row.target_id as number,
    relation_type: row.relation_type as RelationType,
    weight: (row.weight as number) || 0.5,
    confidence: (row.confidence as number) || 0.8,
    directional: !!(row.directional as number),
    label: (row.label as string) || null,
    explanation: (row.explanation as string) || null,
    query_boost_terms: parseJson(row.query_boost_terms as string | null, []),
    hidden: !!(row.hidden as number),
    sequence_order: (row.sequence_order as number) || null,
  };
}

// ── Node CRUD ──────────────────────────────────────────────────────

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "");
}

export function upsertNode(data: {
  name: string;
  concept_type: ConceptType;
  primary_domain: string;
  aliases?: string[];
  short_definition?: string;
  secondary_domains?: string[];
  board_weight_score?: number;
  timeline_positions?: TimelineTag[];
  ring_identity?: string;
  ring_taxonomy?: string;
  ring_associations?: string;
  ring_distinctions?: string;
  ring_edge?: string;
  query_feature_terms?: string[];
}): number {
  const db = getDb();
  const slug = slugify(data.name);

  const existing = db.prepare("SELECT id FROM graph_nodes WHERE slug = ?").get(slug) as { id: number } | undefined;
  if (existing) {
    db.prepare(`UPDATE graph_nodes SET
      name=?, aliases=?, concept_type=?, short_definition=?,
      primary_domain=?, secondary_domains=?, board_weight_score=?,
      timeline_positions=?, ring_identity=?, ring_taxonomy=?,
      ring_associations=?, ring_distinctions=?, ring_edge=?,
      query_feature_terms=?, updated_at=CURRENT_TIMESTAMP
      WHERE id=?`
    ).run(
      data.name,
      JSON.stringify(data.aliases || []),
      data.concept_type,
      data.short_definition || null,
      data.primary_domain,
      JSON.stringify(data.secondary_domains || []),
      data.board_weight_score ?? 0.5,
      JSON.stringify(data.timeline_positions || []),
      data.ring_identity || null,
      data.ring_taxonomy || null,
      data.ring_associations || null,
      data.ring_distinctions || null,
      data.ring_edge || null,
      JSON.stringify(data.query_feature_terms || []),
      existing.id,
    );
    return existing.id;
  }

  const result = db.prepare(`INSERT INTO graph_nodes
    (slug, name, aliases, concept_type, short_definition, primary_domain,
     secondary_domains, board_weight_score, timeline_positions,
     ring_identity, ring_taxonomy, ring_associations, ring_distinctions, ring_edge,
     query_feature_terms)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
  ).run(
    slug, data.name,
    JSON.stringify(data.aliases || []),
    data.concept_type,
    data.short_definition || null,
    data.primary_domain,
    JSON.stringify(data.secondary_domains || []),
    data.board_weight_score ?? 0.5,
    JSON.stringify(data.timeline_positions || []),
    data.ring_identity || null,
    data.ring_taxonomy || null,
    data.ring_associations || null,
    data.ring_distinctions || null,
    data.ring_edge || null,
    JSON.stringify(data.query_feature_terms || []),
  );
  return result.lastInsertRowid as number;
}

export function upsertEdge(data: {
  source_id: number;
  target_id: number;
  relation_type: RelationType;
  weight?: number;
  confidence?: number;
  directional?: boolean;
  label?: string;
  explanation?: string;
  query_boost_terms?: string[];
  sequence_order?: number;
}): number {
  const db = getDb();
  const existing = db.prepare(
    "SELECT id FROM graph_edges WHERE source_id=? AND target_id=? AND relation_type=?"
  ).get(data.source_id, data.target_id, data.relation_type) as { id: number } | undefined;

  if (existing) return existing.id;

  const result = db.prepare(`INSERT INTO graph_edges
    (source_id, target_id, relation_type, weight, confidence, directional,
     label, explanation, query_boost_terms, sequence_order)
    VALUES (?,?,?,?,?,?,?,?,?,?)`
  ).run(
    data.source_id, data.target_id, data.relation_type,
    data.weight ?? 0.5, data.confidence ?? 0.8,
    (data.directional ?? true) ? 1 : 0,
    data.label || null, data.explanation || null,
    JSON.stringify(data.query_boost_terms || []),
    data.sequence_order ?? null,
  );
  return result.lastInsertRowid as number;
}

// ── Queries ────────────────────────────────────────────────────────

export function getNode(id: number): GraphNode | null {
  const db = getDb();
  const row = db.prepare("SELECT * FROM graph_nodes WHERE id=?").get(id);
  return row ? rowToNode(row as Record<string, unknown>) : null;
}

export function getNodeBySlug(slug: string): GraphNode | null {
  const db = getDb();
  const row = db.prepare("SELECT * FROM graph_nodes WHERE slug=?").get(slug);
  return row ? rowToNode(row as Record<string, unknown>) : null;
}

export function getAllNodes(): GraphNode[] {
  const db = getDb();
  return (db.prepare("SELECT * FROM graph_nodes WHERE hidden=0 ORDER BY name").all() as Record<string, unknown>[])
    .map(rowToNode);
}

export function getAllEdges(): GraphEdge[] {
  const db = getDb();
  return (db.prepare("SELECT * FROM graph_edges WHERE hidden=0").all() as Record<string, unknown>[])
    .map(rowToEdge);
}

export function getNodeEdges(nodeId: number): GraphEdge[] {
  const db = getDb();
  return (db.prepare(
    "SELECT * FROM graph_edges WHERE (source_id=? OR target_id=?) AND hidden=0 ORDER BY weight DESC"
  ).all(nodeId, nodeId) as Record<string, unknown>[]).map(rowToEdge);
}

export function getNeighborNodes(nodeId: number): GraphNode[] {
  const db = getDb();
  return (db.prepare(`
    SELECT DISTINCT n.* FROM graph_nodes n
    JOIN graph_edges e ON (
      (e.source_id=? AND e.target_id=n.id) OR
      (e.target_id=? AND e.source_id=n.id)
    )
    WHERE n.hidden=0 AND e.hidden=0
    ORDER BY n.board_weight_score DESC
  `).all(nodeId, nodeId) as Record<string, unknown>[]).map(rowToNode);
}

// ── Traversal ──────────────────────────────────────────────────────

export function traversePath(
  startId: number,
  mode: TraversalMode,
  maxDepth: number = 15
): { path: GraphNode[]; edges: GraphEdge[] } {
  const db = getDb();
  const modeConfig = TRAVERSAL_MODES[mode];
  const relTypes = modeConfig.relations;
  const placeholders = relTypes.map(() => "?").join(",");

  const nodes: GraphNode[] = [];
  const pathEdges: GraphEdge[] = [];
  const visited = new Set<number>();

  // Walk forward
  let currentId = startId;
  const startNode = getNode(startId);
  if (!startNode) return { path: [], edges: [] };
  nodes.push(startNode);
  visited.add(startId);

  for (let i = 0; i < maxDepth; i++) {
    const nextEdge = db.prepare(`
      SELECT * FROM graph_edges
      WHERE source_id=? AND relation_type IN (${placeholders}) AND hidden=0
      ORDER BY sequence_order ASC, weight DESC LIMIT 1
    `).get(currentId, ...relTypes) as Record<string, unknown> | undefined;

    if (!nextEdge || visited.has(nextEdge.target_id as number)) break;

    const edge = rowToEdge(nextEdge);
    const nextNode = getNode(edge.target_id);
    if (!nextNode) break;

    pathEdges.push(edge);
    nodes.push(nextNode);
    visited.add(nextNode.id);
    currentId = nextNode.id;
  }

  // Walk backward from start to find predecessors
  currentId = startId;
  const preNodes: GraphNode[] = [];
  const preEdges: GraphEdge[] = [];

  for (let i = 0; i < maxDepth; i++) {
    const prevEdge = db.prepare(`
      SELECT * FROM graph_edges
      WHERE target_id=? AND relation_type IN (${placeholders}) AND hidden=0
      ORDER BY sequence_order ASC, weight DESC LIMIT 1
    `).get(currentId, ...relTypes) as Record<string, unknown> | undefined;

    if (!prevEdge || visited.has(prevEdge.source_id as number)) break;

    const edge = rowToEdge(prevEdge);
    const prevNode = getNode(edge.source_id);
    if (!prevNode) break;

    preEdges.unshift(edge);
    preNodes.unshift(prevNode);
    visited.add(prevNode.id);
    currentId = prevNode.id;
  }

  return {
    path: [...preNodes, ...nodes],
    edges: [...preEdges, ...pathEdges],
  };
}

export function getAvailableTraversals(nodeId: number): Array<{
  mode: TraversalMode;
  edgeCount: number;
  sampleTarget: string | null;
}> {
  const db = getDb();
  const edges = getNodeEdges(nodeId);

  const results: Array<{ mode: TraversalMode; edgeCount: number; sampleTarget: string | null }> = [];

  for (const [mode, config] of Object.entries(TRAVERSAL_MODES)) {
    const relSet = new Set(config.relations);
    const matching = edges.filter((e) => relSet.has(e.relation_type));
    if (matching.length > 0) {
      const targetId = matching[0].source_id === nodeId
        ? matching[0].target_id
        : matching[0].source_id;
      const targetNode = db.prepare("SELECT name FROM graph_nodes WHERE id=?").get(targetId) as { name: string } | undefined;
      results.push({
        mode: mode as TraversalMode,
        edgeCount: matching.length,
        sampleTarget: targetNode?.name || null,
      });
    }
  }

  return results;
}

// ── Query Parser ───────────────────────────────────────────────────

const GESTATION_PATTERN = /(\d+)\s*(?:wk|week|wker|weeks?)\s*(?:gestation|GA|gest\.?)?/gi;
const AGE_PATTERN = /(?:day|DOL)\s*(\d+)|(\d+)\s*(?:day|DOL)\s*(?:old)?/gi;

const FEATURE_PATTERNS: Array<{ pattern: RegExp; type: FeatureType }> = [
  { pattern: /\b(?:IUGR|SGA|FGR|growth\s+restrict)/gi, type: "growth" },
  { pattern: /\b(?:cleft|lip|palate|micrognathia|low.set.ears?|hypertelorism|epicanthal|flat\s+nasal|webbed\s+neck|short\s+neck|cystic\s+hygroma)/gi, type: "dysmorphism" },
  { pattern: /\b(?:VSD|ASD|PDA|TOF|coarctation|murmur|cyanosis|heart\s+defect|CHD)/gi, type: "cardiac" },
  { pattern: /\b(?:seizure|hypotonia|hypertonia|lethargy|apnea|IVH|EEG|fontanelle)/gi, type: "neurologic" },
  { pattern: /\b(?:ultrasound|echo|MRI|CT|X-ray|radiograph|cyst|mass|calcification|effusion)/gi, type: "imaging" },
  { pattern: /\b(?:cfDNA|NIPT|amniocentesis|CVS|quad\s+screen|AFP|karyotype|microarray|FISH)/gi, type: "prenatal_screening" },
  { pattern: /\b(?:hemoglobin|hematocrit|platelet|WBC|CRP|glucose|calcium|sodium|potassium|bilirubin|creatinine|BUN|ammonia|lactate)/gi, type: "lab" },
  { pattern: /\b(?:syndactyly|polydactyly|clinodactyly|single\s+palmar|simian\s+crease|brachydactyly)/gi, type: "physical_exam" },
  { pattern: /\b(?:intubat|surfactant|CPAP|ventilat|phototherapy|exchange\s+transfusion|cooling)/gi, type: "management" },
];

export function parseQuery(raw: string): QueryFeature[] {
  const features: QueryFeature[] = [];
  const text = raw.trim();
  if (!text) return features;

  // Extract gestational age
  let match;
  GESTATION_PATTERN.lastIndex = 0;
  while ((match = GESTATION_PATTERN.exec(text)) !== null) {
    features.push({
      term: match[0],
      normalized_term: `${match[1]} weeks gestation`,
      feature_type: "age_gestation",
      matched_node_ids: [],
      confidence: 0.95,
    });
  }

  // Extract day of life
  AGE_PATTERN.lastIndex = 0;
  while ((match = AGE_PATTERN.exec(text)) !== null) {
    const day = match[1] || match[2];
    features.push({
      term: match[0],
      normalized_term: `day ${day}`,
      feature_type: "timeline",
      matched_node_ids: [],
      confidence: 0.9,
    });
  }

  // Pattern-based feature extraction
  for (const { pattern, type } of FEATURE_PATTERNS) {
    pattern.lastIndex = 0;
    while ((match = pattern.exec(text)) !== null) {
      features.push({
        term: match[0],
        normalized_term: match[0].toLowerCase().trim(),
        feature_type: type,
        matched_node_ids: [],
        confidence: 0.8,
      });
    }
  }

  // Remaining terms as free text
  let remaining = text;
  for (const f of features) {
    remaining = remaining.replace(f.term, "");
  }
  const freeTerms = remaining.trim().split(/\s+/).filter((t) => t.length > 2);
  for (const t of freeTerms) {
    if (/^(the|and|with|for|from|has|was|are|but|not|this|that|who)$/i.test(t)) continue;
    features.push({
      term: t,
      normalized_term: t.toLowerCase(),
      feature_type: "free_text",
      matched_node_ids: [],
      confidence: 0.5,
    });
  }

  return features;
}

// ── Concept Ranking ────────────────────────────────────────────────

export function rankConcepts(
  features: QueryFeature[],
  limit: number = 10
): Array<{ node: GraphNode; score: number; matchedFeatures: string[] }> {
  const db = getDb();
  const allNodes = getAllNodes();
  const scored: Array<{ node: GraphNode; score: number; matchedFeatures: string[] }> = [];

  for (const node of allNodes) {
    let score = 0;
    const matchedFeatures: string[] = [];
    const searchables = [
      node.name,
      ...node.aliases,
      node.short_definition || "",
      ...node.query_feature_terms,
      node.ring_identity || "",
      node.ring_associations || "",
      node.ring_distinctions || "",
      node.ring_edge || "",
    ].map((s) => s.toLowerCase());

    const searchText = searchables.join(" ");

    for (const feature of features) {
      const term = feature.normalized_term.toLowerCase();
      if (searchText.includes(term)) {
        score += feature.confidence * 2;
        matchedFeatures.push(feature.term);
      }
      // Partial match on aliases
      for (const alias of node.aliases) {
        if (alias.toLowerCase().includes(term) || term.includes(alias.toLowerCase())) {
          score += feature.confidence * 1.5;
          if (!matchedFeatures.includes(feature.term)) matchedFeatures.push(feature.term);
        }
      }
    }

    // Board weight boost
    score *= (0.5 + node.board_weight_score);

    // Evidence density boost
    score *= (1 + node.density_score * 0.5);

    if (score > 0) {
      scored.push({ node, score, matchedFeatures });
    }
  }

  // Also search neighbor edges for boost terms
  for (const item of scored) {
    const edges = getNodeEdges(item.node.id);
    for (const edge of edges) {
      for (const bt of edge.query_boost_terms) {
        for (const feature of features) {
          if (bt.toLowerCase().includes(feature.normalized_term) ||
              feature.normalized_term.includes(bt.toLowerCase())) {
            item.score += 0.3;
          }
        }
      }
    }
  }

  return scored.sort((a, b) => b.score - a.score).slice(0, limit);
}

// ── Build Focused Torus State ──────────────────────────────────────

export function buildFocusedState(
  query: string,
  focusNodeId?: number
): FocusedTorusState {
  const features = parseQuery(query);
  const ranked = rankConcepts(features, 20);

  const focusNode = focusNodeId
    ? getNode(focusNodeId)
    : ranked[0]?.node || null;

  // Differentials
  const differentials = focusNode
    ? getNodeEdges(focusNode.id)
        .filter((e) =>
          ["distinguished_from", "compared_with", "board_trap_vs",
           "mimic_of", "often_confused_with"].includes(e.relation_type)
        )
        .map((e) => {
          const otherId = e.source_id === focusNode.id ? e.target_id : e.source_id;
          const node = getNode(otherId);
          return node ? { node, score: e.weight, reason: e.explanation || e.relation_type } : null;
        })
        .filter(Boolean) as Array<{ node: GraphNode; score: number; reason: string }>
    : [];

  // Active edges from focus
  const activeEdges = focusNode ? getNodeEdges(focusNode.id) : [];

  // Domain scoring
  const domainScores = new Map<string, number>();
  for (const item of ranked) {
    const d = item.node.primary_domain;
    domainScores.set(d, (domainScores.get(d) || 0) + item.score);
  }
  const dominant_domains = Array.from(domainScores.entries())
    .map(([domain, score]) => ({ domain, score }))
    .sort((a, b) => b.score - a.score);

  // Available traversal paths
  const active_pathways: Partial<Record<TraversalMode, number[]>> = {};
  if (focusNode) {
    const available = getAvailableTraversals(focusNode.id);
    for (const a of available) {
      const { path } = traversePath(focusNode.id, a.mode);
      if (path.length > 1) {
        active_pathways[a.mode] = path.map((n) => n.id);
      }
    }
  }

  // Suggested jump points
  const suggested_jump_points: FocusedTorusState["suggested_jump_points"] = [];
  if (focusNode) {
    const available = getAvailableTraversals(focusNode.id);
    for (const a of available) {
      suggested_jump_points.push({
        node_id: focusNode.id,
        mode: a.mode,
        reason: `${a.edgeCount} ${TRAVERSAL_MODES[a.mode].label} connections${a.sampleTarget ? ` (e.g., ${a.sampleTarget})` : ""}`,
      });
    }
  }

  // Heat map: all matched nodes
  const torus_heat = ranked.map((r) => ({
    node_id: r.node.id,
    intensity: Math.min(r.score / (ranked[0]?.score || 1), 1),
  }));

  return {
    query,
    parsed_features: features,
    focus_node: focusNode,
    top_differentials: differentials,
    dominant_domains,
    active_edges: activeEdges,
    suggested_jump_points,
    active_pathways,
    torus_heat,
  };
}
