import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

interface PathNode {
  conceptId: number;
  name: string;
  slug: string;
  domain: string;
  explanation: string | null;
  weight: number;
  step: number;
}

/**
 * GET /api/traverse?conceptId=1&relation=embryology
 *
 * Finds a directed chain of concepts starting from the given concept,
 * following edges of the specified relation_type.
 * Uses sequence_order if present, otherwise follows by weight.
 */
export async function GET(req: NextRequest) {
  const conceptId = req.nextUrl.searchParams.get("conceptId");
  const relation = req.nextUrl.searchParams.get("relation");

  if (!conceptId || !relation) {
    return NextResponse.json(
      { error: "conceptId and relation are required" },
      { status: 400 }
    );
  }

  const db = getDb();
  const startId = parseInt(conceptId);

  // Get the starting concept
  const startConcept = db
    .prepare("SELECT id, name, slug, primary_domain FROM concepts WHERE id = ?")
    .get(startId) as { id: number; name: string; slug: string; primary_domain: string } | undefined;

  if (!startConcept) {
    return NextResponse.json({ error: "Concept not found" }, { status: 404 });
  }

  // Build the path: follow outgoing edges of this relation_type
  const path: PathNode[] = [
    {
      conceptId: startConcept.id,
      name: startConcept.name,
      slug: startConcept.slug,
      domain: startConcept.primary_domain,
      explanation: null,
      weight: 1,
      step: 0,
    },
  ];

  const visited = new Set<number>([startId]);
  let currentId = startId;

  // Walk forward along the chain
  for (let i = 0; i < 20; i++) {
    const next = db
      .prepare(
        `SELECT ce.target_id, ce.weight, ce.explanation, ce.sequence_order,
                c.name, c.slug, c.primary_domain
         FROM concept_edges ce
         JOIN concepts c ON c.id = ce.target_id
         WHERE ce.source_id = ? AND ce.relation_type = ?
         ORDER BY ce.sequence_order ASC, ce.weight DESC
         LIMIT 1`
      )
      .get(currentId, relation) as {
      target_id: number;
      weight: number;
      explanation: string | null;
      name: string;
      slug: string;
      primary_domain: string;
    } | undefined;

    if (!next || visited.has(next.target_id)) break;

    visited.add(next.target_id);
    path.push({
      conceptId: next.target_id,
      name: next.name,
      slug: next.slug,
      domain: next.primary_domain,
      explanation: next.explanation,
      weight: next.weight,
      step: path.length,
    });
    currentId = next.target_id;
  }

  // Also walk backward to find predecessors (the start might be mid-chain)
  currentId = startId;
  const prePath: PathNode[] = [];
  for (let i = 0; i < 20; i++) {
    const prev = db
      .prepare(
        `SELECT ce.source_id, ce.weight, ce.explanation, ce.sequence_order,
                c.name, c.slug, c.primary_domain
         FROM concept_edges ce
         JOIN concepts c ON c.id = ce.source_id
         WHERE ce.target_id = ? AND ce.relation_type = ?
         ORDER BY ce.sequence_order ASC, ce.weight DESC
         LIMIT 1`
      )
      .get(currentId, relation) as {
      source_id: number;
      weight: number;
      explanation: string | null;
      name: string;
      slug: string;
      primary_domain: string;
    } | undefined;

    if (!prev || visited.has(prev.source_id)) break;

    visited.add(prev.source_id);
    prePath.unshift({
      conceptId: prev.source_id,
      name: prev.name,
      slug: prev.slug,
      domain: prev.primary_domain,
      explanation: prev.explanation,
      weight: prev.weight,
      step: 0, // will be reassigned
    });
    currentId = prev.source_id;
  }

  // Merge: prePath + path, renumber steps
  const fullPath = [...prePath, ...path];
  fullPath.forEach((node, i) => (node.step = i));

  // Find the index of the original concept in the full path
  const originIndex = fullPath.findIndex((n) => n.conceptId === startId);

  // Also find all available relation types from this concept
  const availableRelations = db
    .prepare(
      `SELECT DISTINCT relation_type, COUNT(*) as count
       FROM concept_edges
       WHERE source_id = ? OR target_id = ?
       GROUP BY relation_type
       ORDER BY count DESC`
    )
    .all(startId, startId) as { relation_type: string; count: number }[];

  return NextResponse.json({
    path: fullPath,
    originIndex,
    relation,
    availableRelations,
    totalSteps: fullPath.length,
  });
}
