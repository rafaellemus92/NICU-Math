#!/usr/bin/env python3
"""
Lightweight PDF ingester for NICU Evidence.

- Detects LIBRARY_DIR automatically (or pass --library)
- Ensures DB schema via api.app.db.ensure_schema()
- Inserts into documents/chunks with pgvector embeddings
"""

import argparse
import os
import sys
import glob
from pathlib import Path
from typing import Iterable, List


from openai import OpenAI
from .db import get_conn, ensure_schema
from .search import _pgvector_literal  # reuse their literal formatter

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

try:
    client = OpenAI(api_key=OPENAI_API_KEY) if os.getenv("NICU_OFFLINE", "1") == "0" and OPENAI_API_KEY else None
except Exception:
    client = None


def iter_pdf_paths(library_dir: Path) -> Iterable[Path]:
    # PDFs anywhere under library/
    yield from (Path(p) for p in glob.glob(str(library_dir / "**" / "*.pdf"), recursive=True))


def read_pdf_text(path: Path) -> List[str]:
    """Return a list of page texts. Uses PyPDF (pure python)."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            txt = page.extract_text() or ""
        except Exception:
            txt = ""
        pages.append(txt.strip())
    return pages


def embed_batch(texts: List[str]) -> List[List[float]]:
    if not client:
        raise RuntimeError("OPENAI_API_KEY is not set; cannot embed.")
    # OpenAI embeddings API can take a list
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def upsert_document_and_chunks(pdf_path: Path):
    title = pdf_path.stem
    full_path = str(pdf_path)

    pages = read_pdf_text(pdf_path)
    if not pages:
        print(f"⚠️  No text extracted: {pdf_path}")
        return

    # Simple chunking = one page per chunk (works fine to start)
    # You can later swap to sliding windows / sentence split etc.
    chunks = []
    for idx, page_text in enumerate(pages):
        text = " ".join(page_text.split())
        if text:
            chunks.append((idx, text))

    if not chunks:
        print(f"⚠️  No non-empty pages: {pdf_path}")
        return

    # Embed in batches
    B = 64
    vecs: List[List[float]] = []
    for i in range(0, len(chunks), B):
        vecs.extend(embed_batch([t for _, t in chunks[i:i+B]]))

    with get_conn() as con, con.cursor() as cur:
        # Upsert document; keep the same ID if already present
        cur.execute(
            """
            INSERT INTO documents(title, source_path)
            VALUES (%s, %s)
            ON CONFLICT (source_path) DO UPDATE SET title = EXCLUDED.title
            RETURNING id;
            """,
            (title, full_path),
        )
        doc_id = cur.fetchone()[0]

        # Delete prior chunks for this doc to keep it idempotent
        cur.execute("DELETE FROM chunks WHERE document_id = %s;", (doc_id,))

        # Insert chunks
        for (chunk_index, text), vec in zip(chunks, vecs):
            cur.execute(
                """
                INSERT INTO chunks(document_id, chunk_index, content, embedding, tsv)
                VALUES (%s, %s, %s, %s::vector, to_tsvector('english', %s));
                """,
                (doc_id, chunk_index, text, _pgvector_literal(vec), text),
            )
    print(f"✅ Ingested {pdf_path.name} — {len(chunks)} chunks")


def main():
    parser = argparse.ArgumentParser(description="Ingest PDFs into pgvector")
    parser.add_argument("--library", help="Path to library (defaults to $LIBRARY_DIR)")
    args = parser.parse_args()

    library_dir = Path(args.library or os.getenv("LIBRARY_DIR", "")).expanduser()
    if not library_dir or not library_dir.exists():
        print("❌ Library folder not found. Pass --library or set LIBRARY_DIR.")
        return

    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set. Export it before running.")
        return

    # Ensure DB schema exists
    ensure_schema()

    pdfs = list(iter_pdf_paths(library_dir))
    if not pdfs:
        print(f"⚠️  No PDFs under: {library_dir}")
        return

    print(f"📚 Library: {library_dir} — {len(pdfs)} PDFs")
    for p in pdfs:
        try:
            upsert_document_and_chunks(p)
        except Exception as e:
            print(f"❌ Failed {p.name}: {e}")


if __name__ == "__main__":
    main()