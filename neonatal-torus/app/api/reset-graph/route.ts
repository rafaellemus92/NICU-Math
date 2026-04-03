import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

/**
 * POST /api/reset-graph
 *
 * Clears graph data and optionally reseeds.
 *
 * Body options:
 * - clear_v2: true (default) — clear graph_nodes, graph_edges, graph_citations
 * - clear_legacy: false (default) — clear concepts, concept_edges, citations
 * - clear_documents: false (default) — clear documents + chunks
 * - reseed: false (default) — run seed-graph after clearing
 * - extract: false (default) — run extract-graph after clearing
 */
export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}));
  const clearV2 = body.clear_v2 !== false;
  const clearLegacy = !!body.clear_legacy;
  const clearDocuments = !!body.clear_documents;
  const reseed = !!body.reseed;
  const extract = !!body.extract;

  const db = getDb();
  const results: string[] = [];

  const tx = db.transaction(() => {
    if (clearV2) {
      try {
        db.exec("DELETE FROM graph_citations");
        db.exec("DELETE FROM graph_edges");
        db.exec("DELETE FROM graph_nodes");
        // Reset FTS
        try { db.exec("INSERT INTO graph_nodes_fts(graph_nodes_fts) VALUES('rebuild')"); } catch { /* ok */ }
        results.push("Cleared graph_nodes, graph_edges, graph_citations");
      } catch (e) {
        results.push(`Error clearing v2: ${e instanceof Error ? e.message : String(e)}`);
      }
    }

    if (clearLegacy) {
      try {
        db.exec("DELETE FROM citations");
        db.exec("DELETE FROM concept_edges");
        db.exec("DELETE FROM concepts");
        try { db.exec("INSERT INTO concepts_fts(concepts_fts) VALUES('rebuild')"); } catch { /* ok */ }
        results.push("Cleared concepts, concept_edges, citations");
      } catch (e) {
        results.push(`Error clearing legacy: ${e instanceof Error ? e.message : String(e)}`);
      }
    }

    if (clearDocuments) {
      try {
        db.exec("DELETE FROM chunks");
        db.exec("DELETE FROM documents");
        try { db.exec("INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild')"); } catch { /* ok */ }
        results.push("Cleared documents and chunks");
      } catch (e) {
        results.push(`Error clearing documents: ${e instanceof Error ? e.message : String(e)}`);
      }
    }
  });

  tx();

  // Reseed
  if (reseed) {
    try {
      const seedUrl = new URL("/api/seed-graph", req.url);
      await fetch(seedUrl.toString(), { method: "POST" });
      results.push("Reseeded graph v2 example data");
    } catch (e) {
      results.push(`Reseed error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  // Re-extract
  if (extract) {
    try {
      const extractUrl = new URL("/api/extract-graph", req.url);
      await fetch(extractUrl.toString(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "{}",
      });
      results.push("Re-extracted graph from chunks");
    } catch (e) {
      results.push(`Extract error: ${e instanceof Error ? e.message : String(e)}`);
    }
  }

  // Final counts
  const counts = {
    graph_nodes: (db.prepare("SELECT COUNT(*) as c FROM graph_nodes").get() as { c: number }).c,
    graph_edges: (db.prepare("SELECT COUNT(*) as c FROM graph_edges").get() as { c: number }).c,
    chunks: (db.prepare("SELECT COUNT(*) as c FROM chunks").get() as { c: number }).c,
    documents: (db.prepare("SELECT COUNT(*) as c FROM documents").get() as { c: number }).c,
  };

  return NextResponse.json({ success: true, results, counts });
}
