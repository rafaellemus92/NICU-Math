import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: NextRequest) {
  const conceptId = req.nextUrl.searchParams.get("conceptId");
  const db = getDb();

  if (!conceptId) {
    return NextResponse.json({ error: "conceptId required" }, { status: 400 });
  }

  const citations = db
    .prepare(
      `SELECT ci.*, ch.text as chunk_text, ch.page_start, ch.page_end,
              ch.domain_primary, d.title as document_title
       FROM citations ci
       JOIN chunks ch ON ch.id = ci.chunk_id
       JOIN documents d ON d.id = ch.document_id
       WHERE ci.concept_id = ?
       ORDER BY ci.id`
    )
    .all(parseInt(conceptId));

  return NextResponse.json({ citations });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { concept_id, chunk_id, claim_text, ring_layer } = body;

    if (!concept_id || !chunk_id) {
      return NextResponse.json(
        { error: "concept_id and chunk_id are required" },
        { status: 400 }
      );
    }

    const db = getDb();

    // Verify both exist
    const concept = db.prepare("SELECT id FROM concepts WHERE id = ?").get(concept_id);
    const chunk = db.prepare("SELECT id FROM chunks WHERE id = ?").get(chunk_id);

    if (!concept) {
      return NextResponse.json({ error: "Concept not found" }, { status: 404 });
    }
    if (!chunk) {
      return NextResponse.json({ error: "Chunk not found" }, { status: 404 });
    }

    const result = db
      .prepare(
        "INSERT INTO citations (concept_id, chunk_id, claim_text, ring_layer) VALUES (?, ?, ?, ?)"
      )
      .run(concept_id, chunk_id, claim_text || null, ring_layer || null);

    const citation = db
      .prepare(
        `SELECT ci.*, ch.text as chunk_text, ch.page_start, d.title as document_title
         FROM citations ci
         JOIN chunks ch ON ch.id = ci.chunk_id
         JOIN documents d ON d.id = ch.document_id
         WHERE ci.id = ?`
      )
      .get(result.lastInsertRowid);

    return NextResponse.json({ citation }, { status: 201 });
  } catch (error) {
    console.error("Create citation error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to create citation" },
      { status: 500 }
    );
  }
}

export async function DELETE(req: NextRequest) {
  const id = req.nextUrl.searchParams.get("id");
  if (!id) {
    return NextResponse.json({ error: "id required" }, { status: 400 });
  }

  const db = getDb();
  db.prepare("DELETE FROM citations WHERE id = ?").run(parseInt(id));
  return NextResponse.json({ success: true });
}
