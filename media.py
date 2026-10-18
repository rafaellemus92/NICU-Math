# api/app/media.py
from typing import List, Dict, Any
from fastapi import APIRouter, Query
from db import get_conn
from search import _embed, _pgvector_literal

router = APIRouter()

@router.get("/tables", summary="Tables relevant to a query")
def tables(query: str, k_docs: int = 5, limit: int = 12) -> List[Dict[str, Any]]:
    v = _pgvector_literal(_embed(query))
    sql_docs = """
      SELECT d.id
      FROM chunks c JOIN documents d ON d.id=c.document_id
      ORDER BY c.embedding <-> %(v)s::vector
      LIMIT %(k)s
    """
    sql_tables = """
      SELECT t.id, t.document_id, t.page, t.preview_md
      FROM tables_extracted t
      WHERE t.document_id = ANY(%(doc_ids)s)
      LIMIT %(limit)s
    """
    with get_conn() as con, con.cursor() as cur:
        cur.execute(sql_docs, {"v": v, "k": k_docs})
        doc_ids = [r[0] for r in cur.fetchall()]
        if not doc_ids:
            return []
        cur.execute(sql_tables, {"doc_ids": doc_ids, "limit": limit})
        rows = cur.fetchall()
    return [
        {"id": r[0], "document_id": r[1], "page": r[2], "preview_md": r[3]}
        for r in rows
    ]

@router.get("/figures", summary="Figures relevant to a query")
def figures(query: str, k_docs: int = 5, limit: int = 12) -> List[Dict[str, Any]]:
    v = _pgvector_literal(_embed(query))
    sql_docs = """
      SELECT d.id
      FROM chunks c JOIN documents d ON d.id=c.document_id
      ORDER BY c.embedding <-> %(v)s::vector
      LIMIT %(k)s
    """
    sql_figs = """
      SELECT f.id, f.document_id, f.page, f.image_path, f.caption
      FROM figures_extracted f
      WHERE f.document_id = ANY(%(doc_ids)s)
      LIMIT %(limit)s
    """
    with get_conn() as con, con.cursor() as cur:
        cur.execute(sql_docs, {"v": v, "k": k_docs})
        doc_ids = [r[0] for r in cur.fetchall()]
        if not doc_ids:
            return []
        cur.execute(sql_figs, {"doc_ids": doc_ids, "limit": limit})
        rows = cur.fetchall()
    return [
        {"id": r[0], "document_id": r[1], "page": r[2], "image_url": f"/{r[3]}", "caption": r[4]}
        for r in rows
    ]