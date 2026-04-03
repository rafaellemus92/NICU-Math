import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const db = getDb();
  const concept = db.prepare("SELECT * FROM concepts WHERE id = ?").get(parseInt(id));

  if (!concept) {
    return NextResponse.json({ error: "Concept not found" }, { status: 404 });
  }

  return NextResponse.json({ concept });
}

export async function PUT(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  try {
    const body = await req.json();
    const db = getDb();

    const existing = db.prepare("SELECT * FROM concepts WHERE id = ?").get(parseInt(id)) as
      | { id: number }
      | undefined;

    if (!existing) {
      return NextResponse.json({ error: "Concept not found" }, { status: 404 });
    }

    const {
      name,
      primary_domain,
      secondary_domains,
      ring1_identity,
      ring2_taxonomy,
      ring3_associations,
      ring4_distinctions,
      ring5_edge,
      timeline,
      board_pearls,
      exam_relevance,
      source_notes,
    } = body;

    const slug = name ? slugify(name) : undefined;

    db.prepare(
      `UPDATE concepts SET
        name = COALESCE(?, name),
        slug = COALESCE(?, slug),
        primary_domain = COALESCE(?, primary_domain),
        secondary_domains = ?,
        ring1_identity = ?,
        ring2_taxonomy = ?,
        ring3_associations = ?,
        ring4_distinctions = ?,
        ring5_edge = ?,
        timeline = ?,
        board_pearls = ?,
        exam_relevance = COALESCE(?, exam_relevance),
        source_notes = ?,
        updated_at = CURRENT_TIMESTAMP
      WHERE id = ?`
    ).run(
      name || null,
      slug || null,
      primary_domain || null,
      secondary_domains ? JSON.stringify(secondary_domains) : null,
      ring1_identity ?? null,
      ring2_taxonomy ?? null,
      ring3_associations ?? null,
      ring4_distinctions ?? null,
      ring5_edge ?? null,
      timeline ?? null,
      board_pearls ? JSON.stringify(board_pearls) : null,
      exam_relevance ?? null,
      source_notes ?? null,
      parseInt(id)
    );

    const updated = db.prepare("SELECT * FROM concepts WHERE id = ?").get(parseInt(id));
    return NextResponse.json({ concept: updated });
  } catch (error) {
    console.error("Update concept error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to update concept" },
      { status: 500 }
    );
  }
}

export async function DELETE(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const db = getDb();

  const existing = db.prepare("SELECT * FROM concepts WHERE id = ?").get(parseInt(id));
  if (!existing) {
    return NextResponse.json({ error: "Concept not found" }, { status: 404 });
  }

  const tx = db.transaction(() => {
    db.prepare("DELETE FROM citations WHERE concept_id = ?").run(parseInt(id));
    db.prepare("DELETE FROM concept_edges WHERE source_id = ? OR target_id = ?").run(
      parseInt(id),
      parseInt(id)
    );
    // Delete from FTS
    db.prepare(
      "INSERT INTO concepts_fts(concepts_fts, rowid, name, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls) VALUES ('delete', ?, ?, ?, ?, ?, ?, ?, ?)"
    ).run(
      parseInt(id),
      ...(["name", "ring1_identity", "ring2_taxonomy", "ring3_associations", "ring4_distinctions", "ring5_edge", "board_pearls"] as const).map(
        (k) => (existing as Record<string, unknown>)[k] ?? null
      )
    );
    db.prepare("DELETE FROM concepts WHERE id = ?").run(parseInt(id));
  });

  tx();
  return NextResponse.json({ success: true });
}
