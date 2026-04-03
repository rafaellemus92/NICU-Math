import { NextResponse } from "next/server";
import { getDb } from "@/lib/db";

export async function GET() {
  const db = getDb();
  const issues: string[] = [];

  // Table existence
  const tables = db.prepare(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
  ).all() as { name: string }[];
  const tableNames = tables.map((t) => t.name);

  // Counts
  const count = (table: string) => {
    try {
      return (db.prepare(`SELECT COUNT(*) as c FROM ${table}`).get() as { c: number }).c;
    } catch { return -1; }
  };

  const counts = {
    domains: count("domains"),
    documents: count("documents"),
    chunks: count("chunks"),
    concepts_legacy: count("concepts"),
    concept_edges_legacy: count("concept_edges"),
    graph_nodes: count("graph_nodes"),
    graph_edges: count("graph_edges"),
    graph_citations: count("graph_citations"),
    citations: count("citations"),
  };

  // Validate graph_nodes — check for missing required fields
  let nodesWithIssues: unknown[] = [];
  if (counts.graph_nodes > 0) {
    nodesWithIssues = db.prepare(`
      SELECT id, slug, name, primary_domain, concept_type
      FROM graph_nodes
      WHERE name IS NULL OR name = ''
         OR slug IS NULL OR slug = ''
         OR primary_domain IS NULL OR primary_domain = ''
         OR concept_type IS NULL OR concept_type = ''
    `).all();
    if ((nodesWithIssues as unknown[]).length > 0) {
      issues.push(`${(nodesWithIssues as unknown[]).length} graph_nodes missing required fields`);
    }
  }

  // Validate graph_edges — check for dangling references
  let danglingEdges: unknown[] = [];
  if (counts.graph_edges > 0) {
    danglingEdges = db.prepare(`
      SELECT e.id, e.source_id, e.target_id, e.relation_type
      FROM graph_edges e
      LEFT JOIN graph_nodes s ON s.id = e.source_id
      LEFT JOIN graph_nodes t ON t.id = e.target_id
      WHERE s.id IS NULL OR t.id IS NULL
    `).all();
    if ((danglingEdges as unknown[]).length > 0) {
      issues.push(`${(danglingEdges as unknown[]).length} graph_edges reference missing nodes`);
    }
  }

  // Validate legacy concept_edges — same check
  let danglingLegacyEdges: unknown[] = [];
  if (counts.concept_edges_legacy > 0) {
    try {
      danglingLegacyEdges = db.prepare(`
        SELECT e.id, e.source_id, e.target_id, e.relation_type
        FROM concept_edges e
        LEFT JOIN concepts s ON s.id = e.source_id
        LEFT JOIN concepts t ON t.id = e.target_id
        WHERE s.id IS NULL OR t.id IS NULL
      `).all();
      if ((danglingLegacyEdges as unknown[]).length > 0) {
        issues.push(`${(danglingLegacyEdges as unknown[]).length} legacy concept_edges reference missing concepts`);
      }
    } catch {
      issues.push("Could not validate legacy concept_edges (table may have schema issues)");
    }
  }

  // Check which graph source the torus would use
  let torusSource = "none";
  if (counts.graph_nodes > 0) {
    torusSource = "graph_v2";
  } else if (counts.concepts_legacy > 0) {
    torusSource = "legacy";
  }

  // Domain validation
  let invalidDomains: unknown[] = [];
  if (counts.graph_nodes > 0) {
    invalidDomains = db.prepare(`
      SELECT n.id, n.name, n.primary_domain
      FROM graph_nodes n
      LEFT JOIN domains d ON d.id = n.primary_domain
      WHERE d.id IS NULL
    `).all();
    if ((invalidDomains as unknown[]).length > 0) {
      issues.push(`${(invalidDomains as unknown[]).length} graph_nodes have invalid primary_domain`);
    }
  }

  // Sample data
  const sampleNodes = counts.graph_nodes > 0
    ? db.prepare("SELECT id, slug, name, primary_domain, concept_type FROM graph_nodes LIMIT 5").all()
    : [];
  const sampleEdges = counts.graph_edges > 0
    ? db.prepare("SELECT id, source_id, target_id, relation_type, weight FROM graph_edges LIMIT 5").all()
    : [];

  return NextResponse.json({
    status: issues.length === 0 ? "healthy" : "issues_found",
    tables: tableNames,
    counts,
    torus_source: torusSource,
    issues,
    dangling_edges: danglingEdges,
    dangling_legacy_edges: danglingLegacyEdges,
    nodes_with_issues: nodesWithIssues,
    invalid_domains: invalidDomains,
    sample_nodes: sampleNodes,
    sample_edges: sampleEdges,
  });
}
