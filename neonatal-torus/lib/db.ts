import Database from "better-sqlite3";
import path from "path";
import fs from "fs";
import { ABP_DOMAINS } from "./domains";

const DB_PATH = path.join(process.cwd(), "data", "neonatal-torus.db");
const SCHEMA_PATH = path.join(process.cwd(), "lib", "schema.sql");

let _db: Database.Database | null = null;

export function getDb(): Database.Database {
  if (_db) return _db;

  // Ensure data directory exists
  const dataDir = path.dirname(DB_PATH);
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }

  _db = new Database(DB_PATH);
  _db.pragma("journal_mode = WAL");
  _db.pragma("foreign_keys = ON");

  // Run schema
  const schema = fs.readFileSync(SCHEMA_PATH, "utf-8");
  _db.exec(schema);

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
