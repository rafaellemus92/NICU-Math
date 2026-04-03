import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";
import { suggestConcepts } from "@/lib/ingest";

export async function GET(req: NextRequest) {
  const documentId = req.nextUrl.searchParams.get("documentId");

  if (!documentId) {
    return NextResponse.json({ error: "documentId required" }, { status: 400 });
  }

  const db = getDb();
  const doc = db.prepare("SELECT * FROM documents WHERE id = ?").get(parseInt(documentId));
  if (!doc) {
    return NextResponse.json({ error: "Document not found" }, { status: 404 });
  }

  const chunks = db
    .prepare(
      "SELECT id, page_start, page_end, substr(text, 1, 200) as preview, domain_primary, ring_label FROM chunks WHERE document_id = ? ORDER BY id"
    )
    .all(parseInt(documentId));

  const domainCounts = db
    .prepare(
      "SELECT domain_primary, COUNT(*) as count FROM chunks WHERE document_id = ? AND domain_primary IS NOT NULL GROUP BY domain_primary ORDER BY count DESC"
    )
    .all(parseInt(documentId));

  const suggestions = suggestConcepts(parseInt(documentId));

  return NextResponse.json({
    document: doc,
    chunks,
    domainCounts,
    suggestions,
  });
}
