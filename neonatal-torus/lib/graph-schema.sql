-- ═══════════════════════════════════════════════════════════════════
-- Neonatal Torus Graph Schema v2
-- Concept nodes with rich typing + directional typed edges
-- ═══════════════════════════════════════════════════════════════════

-- Graph nodes: richer than the original concepts table
CREATE TABLE IF NOT EXISTS graph_nodes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  aliases TEXT,                -- JSON string[]
  concept_type TEXT NOT NULL,  -- see CONCEPT_TYPES in graph-types.ts
  short_definition TEXT,
  primary_domain TEXT NOT NULL REFERENCES domains(id),
  secondary_domains TEXT,      -- JSON string[]
  board_weight_score REAL DEFAULT 0.5,
  density_score REAL DEFAULT 0.0,
  timeline_positions TEXT,     -- JSON TimelineTag[]
  ring_identity TEXT,
  ring_taxonomy TEXT,
  ring_associations TEXT,
  ring_distinctions TEXT,
  ring_edge TEXT,
  evidence_count INTEGER DEFAULT 0,
  query_feature_terms TEXT,    -- JSON string[] for matching board stems
  hidden INTEGER DEFAULT 0,
  legacy_concept_id INTEGER,   -- FK to old concepts table for migration
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Graph edges: typed, directional, weighted, with confidence
CREATE TABLE IF NOT EXISTS graph_edges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER NOT NULL REFERENCES graph_nodes(id),
  target_id INTEGER NOT NULL REFERENCES graph_nodes(id),
  relation_type TEXT NOT NULL,  -- see RELATION_TYPES in graph-types.ts
  weight REAL NOT NULL DEFAULT 0.5,
  confidence REAL NOT NULL DEFAULT 0.8,
  directional INTEGER NOT NULL DEFAULT 1,
  label TEXT,
  explanation TEXT,
  query_boost_terms TEXT,      -- JSON string[]
  hidden INTEGER DEFAULT 0,
  sequence_order INTEGER,
  UNIQUE(source_id, target_id, relation_type)
);

-- Citation links: graph_node claims → source chunks
CREATE TABLE IF NOT EXISTS graph_citations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  node_id INTEGER NOT NULL REFERENCES graph_nodes(id),
  chunk_id INTEGER NOT NULL REFERENCES chunks(id),
  edge_id INTEGER REFERENCES graph_edges(id),
  claim_text TEXT,
  ring_layer TEXT
);

-- FTS on graph nodes
CREATE VIRTUAL TABLE IF NOT EXISTS graph_nodes_fts USING fts5(
  name,
  aliases,
  short_definition,
  ring_identity,
  ring_taxonomy,
  ring_associations,
  ring_distinctions,
  ring_edge,
  query_feature_terms,
  content=graph_nodes,
  content_rowid=id
);

-- Triggers for graph_nodes FTS sync
CREATE TRIGGER IF NOT EXISTS graph_nodes_ai AFTER INSERT ON graph_nodes BEGIN
  INSERT INTO graph_nodes_fts(rowid, name, aliases, short_definition,
    ring_identity, ring_taxonomy, ring_associations, ring_distinctions, ring_edge, query_feature_terms)
  VALUES (new.id, new.name, new.aliases, new.short_definition,
    new.ring_identity, new.ring_taxonomy, new.ring_associations, new.ring_distinctions, new.ring_edge, new.query_feature_terms);
END;

CREATE TRIGGER IF NOT EXISTS graph_nodes_au AFTER UPDATE ON graph_nodes BEGIN
  INSERT INTO graph_nodes_fts(graph_nodes_fts, rowid, name, aliases, short_definition,
    ring_identity, ring_taxonomy, ring_associations, ring_distinctions, ring_edge, query_feature_terms)
  VALUES ('delete', old.id, old.name, old.aliases, old.short_definition,
    old.ring_identity, old.ring_taxonomy, old.ring_associations, old.ring_distinctions, old.ring_edge, old.query_feature_terms);
  INSERT INTO graph_nodes_fts(rowid, name, aliases, short_definition,
    ring_identity, ring_taxonomy, ring_associations, ring_distinctions, ring_edge, query_feature_terms)
  VALUES (new.id, new.name, new.aliases, new.short_definition,
    new.ring_identity, new.ring_taxonomy, new.ring_associations, new.ring_distinctions, new.ring_edge, new.query_feature_terms);
END;
