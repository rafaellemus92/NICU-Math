import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const conceptId = parseInt(id);
  const db = getDb();

  // Get connected concepts via edges
  const connections = db
    .prepare(
      `SELECT c.id, c.name, c.slug, c.primary_domain,
              ce.relation_type, ce.weight, ce.explanation
       FROM concept_edges ce
       JOIN concepts c ON c.id = ce.target_id
       WHERE ce.source_id = ?
       UNION
       SELECT c.id, c.name, c.slug, c.primary_domain,
              ce.relation_type, ce.weight, ce.explanation
       FROM concept_edges ce
       JOIN concepts c ON c.id = ce.source_id
       WHERE ce.target_id = ?
       ORDER BY weight DESC`
    )
    .all(conceptId, conceptId);

  // Get citations
  const citations = db
    .prepare(
      `SELECT ci.id, ci.claim_text, ci.ring_layer,
              ch.text as chunk_text, ch.page_start,
              d.title as document_title
       FROM citations ci
       JOIN chunks ch ON ch.id = ci.chunk_id
       JOIN documents d ON d.id = ch.document_id
       WHERE ci.concept_id = ?
       ORDER BY ci.id`
    )
    .all(conceptId);

  return NextResponse.json({ connections, citations });
}
