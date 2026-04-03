import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();

  const density = db
    .prepare(
      `SELECT domain_primary as domain, COUNT(*) as count
       FROM chunks
       WHERE domain_primary IS NOT NULL
       GROUP BY domain_primary
       ORDER BY count DESC`
    )
    .all();

  return NextResponse.json({ density });
}
