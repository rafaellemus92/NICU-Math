import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q");
  const domain = req.nextUrl.searchParams.get("domain");
  const ring = req.nextUrl.searchParams.get("ring");
  const type = req.nextUrl.searchParams.get("type") || "all"; // "concepts", "chunks", "all"

  if (!q || q.trim().length === 0) {
    return NextResponse.json({ concepts: [], chunks: [] });
  }

  const db = getDb();
  // Escape FTS special characters and add prefix matching
  const ftsQuery = q
    .trim()
    .split(/\s+/)
    .map((word) => `"${word.replace(/"/g, "")}"*`)
    .join(" ");

  const results: { concepts: unknown[]; chunks: unknown[] } = {
    concepts: [],
    chunks: [],
  };

  // Search concepts
  if (type === "all" || type === "concepts") {
    let conceptQuery = `
      SELECT c.*, rank
      FROM concepts_fts fts
      JOIN concepts c ON c.id = fts.rowid
      WHERE concepts_fts MATCH ?
    `;
    const conceptParams: (string | number)[] = [ftsQuery];

    if (domain) {
      conceptQuery += " AND c.primary_domain = ?";
      conceptParams.push(domain);
    }

    conceptQuery += " ORDER BY rank LIMIT 50";

    try {
      results.concepts = db.prepare(conceptQuery).all(...conceptParams);
    } catch {
      // FTS query failed, fall back to LIKE
      let fallback = "SELECT * FROM concepts WHERE name LIKE ?";
      const fbParams: string[] = [`%${q}%`];
      if (domain) {
        fallback += " AND primary_domain = ?";
        fbParams.push(domain);
      }
      fallback += " LIMIT 50";
      results.concepts = db.prepare(fallback).all(...fbParams);
    }
  }

  // Search chunks
  if (type === "all" || type === "chunks") {
    let chunkQuery = `
      SELECT ch.*, d.title as document_title, rank
      FROM chunks_fts fts
      JOIN chunks ch ON ch.id = fts.rowid
      LEFT JOIN documents d ON d.id = ch.document_id
      WHERE chunks_fts MATCH ?
    `;
    const chunkParams: (string | number)[] = [ftsQuery];

    if (domain) {
      chunkQuery += " AND ch.domain_primary = ?";
      chunkParams.push(domain);
    }
    if (ring) {
      chunkQuery += " AND ch.ring_label = ?";
      chunkParams.push(ring);
    }

    chunkQuery += " ORDER BY rank LIMIT 50";

    try {
      results.chunks = db.prepare(chunkQuery).all(...chunkParams);
    } catch {
      let fallback = "SELECT ch.*, d.title as document_title FROM chunks ch LEFT JOIN documents d ON d.id = ch.document_id WHERE ch.text LIKE ?";
      const fbParams: string[] = [`%${q}%`];
      if (domain) {
        fallback += " AND ch.domain_primary = ?";
        fbParams.push(domain);
      }
      fallback += " LIMIT 50";
      results.chunks = db.prepare(fallback).all(...fbParams);
    }
  }

  return NextResponse.json(results);
}
