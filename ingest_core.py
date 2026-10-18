# api/app/ingest_core.py
from __future__ import annotations
import os, glob
from pathlib import Path
from typing import Iterable, List, Dict, Any

from openai import OpenAI
from db import get_conn, ensure_schema
from search import _pgvector_literal

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
_client = OpenAI(api_key=OPENAI_API_KEY) if os.getenv("NICU_OFFLINE", "1") == "0" and OPENAI_API_KEY else None

def _iter_pdf_paths(library_dir: Path) -> Iterable[Path]:
    yield from (Path(p) for p in glob.glob(str(library_dir / "**" / "*.pdf"), recursive=True))

def _read_pdf_text(path: Path) -> List[str]:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    out = []
    for page in reader.pages:
        try:
            txt = (page.extract_text() or "").strip()
        except Exception:
            txt = ""
        out.append(txt)
    return out

def _embed_batch(texts: List[str]) -> List[List[float]]:
    if not _client:
        raise RuntimeError("OPENAI_API_KEY is not set; cannot embed.")
    resp = _client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]

def _upsert_document_and_chunks(pdf_path: Path) -> int:
    title = pdf_path.stem
    full_path = str(pdf_path)
    pages = _read_pdf_text(pdf_path)

    chunks: List[tuple[int, str]] = []
    for idx, page_text in enumerate(pages):
        text = " ".join(page_text.split())
        if text:
            chunks.append((idx, text))
    if not chunks:
        print(f"⚠️  No non-empty pages: {pdf_path}")
        return 0

    B = 64
    vecs: List[List[float]] = []
    for i in range(0, len(chunks), B):
        vecs.extend(_embed_batch([t for _, t in chunks[i:i+B]]))

    with get_conn() as con, con.cursor() as cur:
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
        cur.execute("DELETE FROM chunks WHERE document_id = %s;", (doc_id,))
        for (chunk_index, text), vec in zip(chunks, vecs):
            cur.execute(
                """
                INSERT INTO chunks(document_id, chunk_index, content, embedding, tsv)
                VALUES (%s, %s, %s, %s::vector, to_tsvector('english', %s));
                """,
                (doc_id, chunk_index, text, _pgvector_literal(vec), text),
            )
    print(f"✅ Ingested {pdf_path.name} — {len(chunks)} chunks")
    return len(chunks)

def ingest_all(library_dir: Path) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    ensure_schema()
    pdfs = list(_iter_pdf_paths(library_dir))
    total_chunks = 0
    done, failed = [], []
    for p in pdfs:
        try:
            total_chunks += _upsert_document_and_chunks(p)
            done.append(str(p))
        except Exception as e:
            print(f"❌ Failed {p.name}: {e}")
            failed.append({"path": str(p), "error": str(e)})
    return {"pdfs": len(pdfs), "chunks": total_chunks, "failed": failed}