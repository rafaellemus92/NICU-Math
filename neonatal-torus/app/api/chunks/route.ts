import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: NextRequest) {
  const db = getDb();
  const documentId = req.nextUrl.searchParams.get("documentId");
  const domain = req.nextUrl.searchParams.get("domain");
  const q = req.nextUrl.searchParams.get("q");
  const limit = parseInt(req.nextUrl.searchParams.get("limit") || "50");
  const offset = parseInt(req.nextUrl.searchParams.get("offset") || "0");

  let query = `
    SELECT ch.id, ch.document_id, ch.page_start, ch.page_end,
           substr(ch.text, 1, 300) as preview, ch.text,
           ch.domain_primary, ch.ring_label,
           d.title as document_title
    FROM chunks ch
    LEFT JOIN documents d ON d.id = ch.document_id
    WHERE 1=1
  `;
  const params: (string | number)[] = [];

  if (documentId) {
    query += " AND ch.document_id = ?";
    params.push(parseInt(documentId));
  }
  if (domain) {
    query += " AND ch.domain_primary = ?";
    params.push(domain);
  }
  if (q) {
    query += " AND ch.text LIKE ?";
    params.push(`%${q}%`);
  }

  query += " ORDER BY ch.id LIMIT ? OFFSET ?";
  params.push(limit, offset);

  const chunks = db.prepare(query).all(...params);
  return NextResponse.json({ chunks });
}
