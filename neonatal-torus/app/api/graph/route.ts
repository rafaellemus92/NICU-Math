import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();

  // Try graph v2 tables first
  const v2Count = db.prepare(
    "SELECT COUNT(*) as c FROM sqlite_master WHERE type='table' AND name='graph_nodes'"
  ).get() as { c: number };

  let concepts: unknown[] = [];
  let edges: unknown[] = [];

  if (v2Count.c > 0) {
    const nodeCount = db.prepare("SELECT COUNT(*) as c FROM graph_nodes").get() as { c: number };

    if (nodeCount.c > 0) {
      // Use graph v2 tables — map to torus-compatible format
      concepts = db.prepare(`
        SELECT id, slug, name, primary_domain, secondary_domains,
               board_weight_score as exam_relevance,
               ring_identity as ring1_identity,
               ring_taxonomy as ring2_taxonomy,
               ring_associations as ring3_associations,
               ring_distinctions as ring4_distinctions,
               ring_edge as ring5_edge,
               timeline_positions as timeline
        FROM graph_nodes
        WHERE hidden = 0
        ORDER BY name
      `).all();

      edges = db.prepare(`
        SELECT source_id, target_id, relation_type, weight, explanation
        FROM graph_edges
        WHERE hidden = 0
        ORDER BY weight DESC
      `).all();
    }
  }

  // Fall back to legacy tables if v2 is empty
  if (concepts.length === 0) {
    try {
      concepts = db.prepare(`
        SELECT id, name, slug, primary_domain, secondary_domains,
               exam_relevance, ring1_identity, ring2_taxonomy,
               ring3_associations, ring4_distinctions, ring5_edge,
               board_pearls, timeline
        FROM concepts
        ORDER BY name
      `).all();
    } catch {
      concepts = [];
    }

    try {
      edges = db.prepare(`
        SELECT source_id, target_id, relation_type, weight, explanation
        FROM concept_edges
        ORDER BY weight DESC
      `).all();
    } catch {
      edges = [];
    }
  }

  // Validate edges — remove any that reference missing node IDs
  const nodeIds = new Set((concepts as Array<{ id: number }>).map((c) => c.id));
  const validEdges = (edges as Array<{ source_id: number; target_id: number }>).filter(
    (e) => nodeIds.has(e.source_id) && nodeIds.has(e.target_id)
  );

  const density = db.prepare(`
    SELECT domain_primary as domain, COUNT(*) as count
    FROM chunks
    WHERE domain_primary IS NOT NULL
    GROUP BY domain_primary
    ORDER BY count DESC
  `).all();

  return NextResponse.json({
    concepts,
    edges: validEdges,
    density,
    _meta: {
      source: concepts.length > 0 && v2Count.c > 0 ? "graph_v2" : "legacy",
      nodeCount: concepts.length,
      edgeCount: validEdges.length,
      droppedEdges: (edges as unknown[]).length - validEdges.length,
    },
  });
}
