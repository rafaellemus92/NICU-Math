import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export async function GET(req: NextRequest) {
  const db = getDb();
  const domain = req.nextUrl.searchParams.get("domain");
  const limit = parseInt(req.nextUrl.searchParams.get("limit") || "100");
  const offset = parseInt(req.nextUrl.searchParams.get("offset") || "0");

  let query = "SELECT * FROM concepts";
  const params: (string | number)[] = [];

  if (domain) {
    query += " WHERE primary_domain = ?";
    params.push(domain);
  }

  query += " ORDER BY name ASC LIMIT ? OFFSET ?";
  params.push(limit, offset);

  const concepts = db.prepare(query).all(...params);
  const total = db
    .prepare(
      domain
        ? "SELECT COUNT(*) as c FROM concepts WHERE primary_domain = ?"
        : "SELECT COUNT(*) as c FROM concepts"
    )
    .get(...(domain ? [domain] : [])) as { c: number };

  return NextResponse.json({ concepts, total: total.c });
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { name, primary_domain, secondary_domains, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls, exam_relevance, source_notes } = body;

    if (!name || !primary_domain) {
      return NextResponse.json(
        { error: "name and primary_domain are required" },
        { status: 400 }
      );
    }

    const db = getDb();
    const slug = slugify(name);

    const result = db
      .prepare(
        `INSERT INTO concepts (name, slug, primary_domain, secondary_domains, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls, exam_relevance, source_notes)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
      .run(
        name,
        slug,
        primary_domain,
        secondary_domains ? JSON.stringify(secondary_domains) : null,
        ring1_identity || null,
        ring2_taxonomy || null,
        ring3_associations || null,
        ring4_distinctions || null,
        ring5_edge || null,
        board_pearls ? JSON.stringify(board_pearls) : null,
        exam_relevance ?? 0.5,
        source_notes || null
      );

    const concept = db
      .prepare("SELECT * FROM concepts WHERE id = ?")
      .get(result.lastInsertRowid);

    return NextResponse.json({ concept }, { status: 201 });
  } catch (error) {
    console.error("Create concept error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to create concept" },
      { status: 500 }
    );
  }
}
