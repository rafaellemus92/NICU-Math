-- ABP exam domains with official weights
CREATE TABLE IF NOT EXISTS domains (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  abbrev TEXT NOT NULL,
  exam_percent REAL NOT NULL,
  color TEXT NOT NULL
);

-- Uploaded source documents
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  filename TEXT NOT NULL,
  filepath TEXT NOT NULL,
  source_type TEXT NOT NULL CHECK(source_type IN ('pdf','docx','manual')),
  page_count INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Extracted text chunks
CREATE TABLE IF NOT EXISTS chunks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document_id INTEGER NOT NULL REFERENCES documents(id),
  page_start INTEGER,
  page_end INTEGER,
  text TEXT NOT NULL,
  domain_primary TEXT REFERENCES domains(id),
  domain_secondary TEXT,
  ring_label TEXT CHECK(ring_label IN ('identity','taxonomy','associations','distinctions','edge')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Core concept entries
CREATE TABLE IF NOT EXISTS concepts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  primary_domain TEXT NOT NULL REFERENCES domains(id),
  secondary_domains TEXT,
  ring1_identity TEXT,
  ring2_taxonomy TEXT,
  ring3_associations TEXT,
  ring4_distinctions TEXT,
  ring5_edge TEXT,
  timeline TEXT,
  board_pearls TEXT,
  exam_relevance REAL DEFAULT 0.5,
  source_notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Connections between concepts (torus fibers)
CREATE TABLE IF NOT EXISTS concept_edges (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id INTEGER NOT NULL REFERENCES concepts(id),
  target_id INTEGER NOT NULL REFERENCES concepts(id),
  relation_type TEXT NOT NULL CHECK(relation_type IN ('distinction','association','mechanism','treatment','genetic','temporal')),
  weight REAL NOT NULL DEFAULT 0.5,
  explanation TEXT,
  UNIQUE(source_id, target_id, relation_type)
);

-- Citation links: concept claims → source chunks
CREATE TABLE IF NOT EXISTS citations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  concept_id INTEGER NOT NULL REFERENCES concepts(id),
  chunk_id INTEGER NOT NULL REFERENCES chunks(id),
  claim_text TEXT,
  ring_layer TEXT CHECK(ring_layer IN ('identity','taxonomy','associations','distinctions','edge'))
);

-- Full-text search on concepts
CREATE VIRTUAL TABLE IF NOT EXISTS concepts_fts USING fts5(
  name,
  ring1_identity,
  ring2_taxonomy,
  ring3_associations,
  ring4_distinctions,
  ring5_edge,
  board_pearls,
  content=concepts,
  content_rowid=id
);

-- Full-text search on chunks
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  text,
  content=chunks,
  content_rowid=id
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS concepts_ai AFTER INSERT ON concepts BEGIN
  INSERT INTO concepts_fts(rowid, name, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls)
  VALUES (new.id, new.name, new.ring1_identity, new.ring2_taxonomy, new.ring3_associations, new.ring4_distinctions, new.ring5_edge, new.board_pearls);
END;

CREATE TRIGGER IF NOT EXISTS concepts_au AFTER UPDATE ON concepts BEGIN
  INSERT INTO concepts_fts(concepts_fts, rowid, name, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls)
  VALUES ('delete', old.id, old.name, old.ring1_identity, old.ring2_taxonomy, old.ring3_associations, old.ring4_distinctions, old.ring5_edge, old.board_pearls);
  INSERT INTO concepts_fts(rowid, name, ring1_identity, ring2_taxonomy, ring3_associations, ring4_distinctions, ring5_edge, board_pearls)
  VALUES (new.id, new.name, new.ring1_identity, new.ring2_taxonomy, new.ring3_associations, new.ring4_distinctions, new.ring5_edge, new.board_pearls);
END;

-- Trigger to keep chunks FTS in sync
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
  INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
END;

CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
  INSERT INTO chunks_fts(chunks_fts, rowid, text) VALUES ('delete', old.id, old.text);
  INSERT INTO chunks_fts(rowid, text) VALUES (new.id, new.text);
END;
