import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();

  const concepts = db
    .prepare(
      `SELECT id, name, slug, primary_domain, secondary_domains,
              exam_relevance, ring1_identity, ring2_taxonomy,
              ring3_associations, ring4_distinctions, ring5_edge,
              board_pearls, timeline
       FROM concepts
       ORDER BY name`
    )
    .all();

  const edges = db
    .prepare(
      `SELECT source_id, target_id, relation_type, weight, explanation
       FROM concept_edges
       ORDER BY weight DESC`
    )
    .all();

  const density = db
    .prepare(
      `SELECT domain_primary as domain, COUNT(*) as count
       FROM chunks
       WHERE domain_primary IS NOT NULL
       GROUP BY domain_primary
       ORDER BY count DESC`
    )
    .all();

  return NextResponse.json({ concepts, edges, density });
}
