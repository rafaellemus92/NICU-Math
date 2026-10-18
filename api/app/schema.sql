-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- ========== Tables ==========
CREATE TABLE IF NOT EXISTS documents (
  id          BIGSERIAL PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,  -- needed for ON CONFLICT
  title       TEXT,
  meta        JSONB
);

-- Match your embedding model dimension (text-embedding-3-small = 1536)
CREATE TABLE IF NOT EXISTS chunks (
  id           BIGSERIAL PRIMARY KEY,
  document_id  BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index  INTEGER NOT NULL,
  content      TEXT NOT NULL,
  embedding    VECTOR(1536),
  tsv          tsvector,             -- for FTS
  UNIQUE (document_id, chunk_index)
);

-- ========== Indexes ==========
-- Helpful btrees
CREATE INDEX IF NOT EXISTS idx_chunks_document      ON chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_chunks_doc_chunk     ON chunks(document_id, chunk_index);

-- Vector ANN (use ivfflat after you have some data; lists tunable)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_ivf
  ON chunks USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);

-- Full‑text search
CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON chunks USING GIN(tsv);

-- Keep tsv up to date (create trigger once)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'chunks_tsv_update') THEN
    CREATE TRIGGER chunks_tsv_update
    BEFORE INSERT OR UPDATE ON chunks
    FOR EACH ROW
    EXECUTE FUNCTION tsvector_update_trigger('tsv','pg_catalog.english','content');
  END IF;
END$$;

-- Backfill any existing rows once (safe to re-run)
UPDATE chunks SET tsv = to_tsvector('english', content) WHERE tsv IS NULL;

-- Tiny query-embedding cache (optional)
CREATE TABLE IF NOT EXISTS query_cache (
  q  TEXT PRIMARY KEY,
  v  VECTOR(1536),
  ts TIMESTAMPTZ DEFAULT now()
);

-- Table for storing Monte Carlo scenario runs
CREATE TABLE IF NOT EXISTS scenario_runs (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  model_name TEXT NOT NULL,
  inputs JSONB NOT NULL,
  assumptions JSONB,
  summary JSONB,
  n_samples INT NOT NULL,
  seed INT,
  notes TEXT
);

-- audit table for Monte Carlo runs (used by bayes.py)
CREATE TABLE IF NOT EXISTS scenario_runs (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now(),
  model_name TEXT NOT NULL,
  inputs JSONB NOT NULL,
  assumptions JSONB,
  summary JSONB,
  n_samples INT NOT NULL,
  seed INT,
  notes TEXT
);

-- scripts/sql/020_tables_figures.sql
CREATE TABLE IF NOT EXISTS tables_extracted (
  id SERIAL PRIMARY KEY,
  document_id INT REFERENCES documents(id) ON DELETE CASCADE,
  page INT NOT NULL,
  title TEXT,
  csv TEXT NOT NULL,          -- normalized CSV (small)
  preview_md TEXT,            -- short markdown preview for UI
  sha1 TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS figures_extracted (
  id SERIAL PRIMARY KEY,
  document_id INT REFERENCES documents(id) ON DELETE CASCADE,
  page INT NOT NULL,
  caption TEXT,
  bbox JSONB,                 -- {"x0":..,"y0":..,"x1":..,"y1":..}
  image_path TEXT NOT NULL,   -- relative path under ./static/figures/
  sha1 TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT now()
);

-- scripts/sql/020_tables_figures.sql
CREATE TABLE IF NOT EXISTS tables_extracted (
  id SERIAL PRIMARY KEY,
  document_id INT REFERENCES documents(id) ON DELETE CASCADE,
  page INT NOT NULL,
  title TEXT,
  csv TEXT NOT NULL,          -- normalized CSV (small)
  preview_md TEXT,            -- short markdown preview for UI
  sha1 TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS figures_extracted (
  id SERIAL PRIMARY KEY,
  document_id INT REFERENCES documents(id) ON DELETE CASCADE,
  page INT NOT NULL,
  caption TEXT,
  bbox JSONB,                 -- {"x0":..,"y0":..,"x1":..,"y1":..}
  image_path TEXT NOT NULL,   -- relative path under ./static/figures/
  sha1 TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT now()
);