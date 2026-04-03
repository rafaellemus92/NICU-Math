import Database from "better-sqlite3";
import path from "path";
import fs from "fs";
import { ABP_DOMAINS } from "./domains";

const DB_PATH = path.join(process.cwd(), "data", "neonatal-torus.db");
const SCHEMA_PATH = path.join(process.cwd(), "lib", "schema.sql");
const GRAPH_SCHEMA_PATH = path.join(process.cwd(), "lib", "graph-schema.sql");

let _db: Database.Database | null = null;

export function getDb(): Database.Database {
  if (_db) return _db;

  const dataDir = path.dirname(DB_PATH);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  _db = new Database(DB_PATH);
  _db.pragma("journal_mode = WAL");
  _db.pragma("foreign_keys = ON");

  // Migrate old concept_edges if needed
  migrateEdgesTable(_db);

  // Run original schema
  const schema = fs.readFileSync(SCHEMA_PATH, "utf-8");
  _db.exec(schema);

  // Run graph v2 schema
  const graphSchema = fs.readFileSync(GRAPH_SCHEMA_PATH, "utf-8");
  _db.exec(graphSchema);

  // Seed domains if empty
  const count = _db.prepare("SELECT COUNT(*) as c FROM domains").get() as { c: number };
  if (count.c === 0) {
    const insert = _db.prepare(
      "INSERT INTO domains (id, name, abbrev, exam_percent, color) VALUES (?, ?, ?, ?, ?)"
    );
    const tx = _db.transaction(() => {
      for (const d of ABP_DOMAINS) {
        insert.run(d.id, d.name, d.abbrev, d.exam_percent, d.color);
      }
    });
    tx();
  }

  return _db;
}

function migrateEdgesTable(db: Database.Database) {
  const tableExists = db
    .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='concept_edges'")
    .get();

  if (!tableExists) return;

  const cols = db.prepare("PRAGMA table_info(concept_edges)").all() as Array<{ name: string }>;
  const hasSequenceOrder = cols.some((c) => c.name === "sequence_order");

  if (!hasSequenceOrder) {
    db.exec("PRAGMA foreign_keys = OFF");
    db.exec(`
      CREATE TABLE concept_edges_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER NOT NULL REFERENCES concepts(id),
        target_id INTEGER NOT NULL REFERENCES concepts(id),
        relation_type TEXT NOT NULL,
        weight REAL NOT NULL DEFAULT 0.5,
        explanation TEXT,
        sequence_order INTEGER,
        UNIQUE(source_id, target_id, relation_type)
      );
      INSERT INTO concept_edges_new (id, source_id, target_id, relation_type, weight, explanation)
        SELECT id, source_id, target_id, relation_type, weight, explanation FROM concept_edges;
      DROP TABLE concept_edges;
      ALTER TABLE concept_edges_new RENAME TO concept_edges;
    `);
    db.exec("PRAGMA foreign_keys = ON");
  }
}
