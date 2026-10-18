# api/app/ingest.py
import os
from pathlib import Path
from typing import Iterable

import fitz  # PyMuPDF
from openai import OpenAI

from .db import get_conn

LIB_DIR = Path("/app/library")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")  # 1536 dims
client = OpenAI()  # reads OPENAI_API_KEY from env


def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    """Very simple paragraph grouper by character count."""
    paras = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, cur = [], ""
    for p in paras:
        if len(cur) + len(p) + 2 > max_chars:
            if cur:
                chunks.append(cur)
            cur = p
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        chunks.append(cur)
    return chunks


def embed(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [d.embedding for d in resp.data]


def upsert_pdf(pdf_path: Path) -> int:
    """Insert/update a document and (re)write all its chunks."""
    with get_conn() as con, con.cursor() as cur:
        # 1) Upsert the document row by unique source_path
        cur.execute(
            """
            INSERT INTO documents (source_path, title, meta)
            VALUES (%s, %s, %s)
            ON CONFLICT (source_path)
            DO UPDATE
              SET title = EXCLUDED.title,
                  meta  = EXCLUDED.meta
            RETURNING id
            """,
            (str(pdf_path), pdf_path.stem, None),
        )
        doc_id = cur.fetchone()[0]

        # 2) Extract full text
        doc = fitz.open(pdf_path)
        pages = [page.get_text("text") or "" for page in doc]
        doc.close()
        text = "\n".join(p for p in pages if p.strip())

        chunks = chunk_text(text)
        if not chunks:
            # Ensure we don't leave stale chunks if the PDF is empty
            cur.execute("DELETE FROM chunks WHERE document_id = %s", (doc_id,))
            return 0

        # 3) Embed in small batches
        B = 32
        vecs: list[list[float]] = []
        for i in range(0, len(chunks), B):
            vecs.extend(embed(chunks[i : i + B]))

        # 4) Clear previous chunks for this document (idempotent)
        cur.execute("DELETE FROM chunks WHERE document_id = %s", (doc_id,))

        # 5) Insert fresh chunks
        for idx, (content, vec) in enumerate(zip(chunks, vecs)):
            cur.execute(
                """
                INSERT INTO chunks (document_id, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s)
                """,
                (doc_id, idx, content, vec),
            )

        return len(chunks)


def main():
    pdfs = sorted(p for p in LIB_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {LIB_DIR}")
        return
    for p in pdfs:
        print(f"Ingesting: {p}")
        n = upsert_pdf(p)
        print(f"  -> {n} chunks")
    print("Done.")


if __name__ == "__main__":
    main()