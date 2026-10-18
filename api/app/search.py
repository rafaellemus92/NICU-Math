# api/app/search.py
from typing import List, Optional, Dict, Any, Tuple
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
from .db import get_conn

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


router = APIRouter()

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language question")
    k: int = Field(5, ge=1, le=50, description="How many passages to return")

class Passage(BaseModel):
    document_id: int
    title: Optional[str]
    path: Optional[str]
    chunk_index: int
    excerpt: str
    score: float
    content: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[Passage]

def _embed(text: str) -> list[float]:
    if os.getenv("NICU_OFFLINE", "1") != "0" or not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(503, "External embeddings are disabled or not configured.")
    client = OpenAI()
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=[text])
    return resp.data[0].embedding

def _pgvector_literal(vec: list[float]) -> str:
    return "[" + ",".join(f"{x:.7f}" for x in vec) + "]"

def _get_or_make_query_vec(con, q: str) -> list[float]:
    with con.cursor() as cur:
        cur.execute("SELECT v FROM query_cache WHERE q=%s", (q,))
        row = cur.fetchone()
        if row:
            return list(row[0])
    v = _embed(q)
    with con.cursor() as cur:
        cur.execute(
            "INSERT INTO query_cache(q, v) VALUES (%s, %s) "
            "ON CONFLICT (q) DO UPDATE SET v=EXCLUDED.v, ts=now()",
            (q, _pgvector_literal(v)),
        )
    return v

def _semantic_topk(con, v_lit: str, k: int) -> List[Dict[str, Any]]:
    sql = """
      SELECT d.id, d.title, d.source_path, c.chunk_index, c.content,
             (c.embedding <-> %(v)s::vector) AS score
      FROM chunks c
      JOIN documents d ON d.id = c.document_id
      ORDER BY c.embedding <-> %(v)s::vector
      LIMIT %(k)s;
    """
    out = []
    with con.cursor() as cur:
        cur.execute(sql, {"v": v_lit, "k": k})
        for r in cur.fetchall():
            out.append(dict(
                document_id=r[0], title=r[1], path=r[2],
                chunk_index=r[3], content=r[4], score=float(r[5])
            ))
    return out

def _lexical_topk(con, q: str, k: int) -> List[Dict[str, Any]]:
    sql = """
      SELECT d.id, d.title, d.source_path, c.chunk_index, c.content,
             ts_rank_cd(c.tsv, plainto_tsquery('english', %(q)s)) AS score
      FROM chunks c
      JOIN documents d ON d.id = c.document_id
      WHERE c.tsv @@ plainto_tsquery('english', %(q)s)
      ORDER BY score DESC
      LIMIT %(k)s;
    """
    out = []
    with con.cursor() as cur:
        cur.execute(sql, {"q": q, "k": k})
        for r in cur.fetchall():
            out.append(dict(
                document_id=r[0], title=r[1], path=r[2],
                chunk_index=r[3], content=r[4], score=float(r[5])
            ))
    return out

def _rrf_merge(sem_rows: List[Dict[str, Any]],
               lex_rows: List[Dict[str, Any]],
               k: int,
               k_rrf: int = 60) -> List[Dict[str, Any]]:
    def key(r): return (r["document_id"], r["chunk_index"])
    scores: Dict[Tuple[int, int], float] = {}
    pick: Dict[Tuple[int, int], Dict[str, Any]] = {}

    for i, r in enumerate(sem_rows):
        kk = key(r)
        scores[kk] = scores.get(kk, 0.0) + 1.0 / (k_rrf + i + 1)
        pick[kk] = r
    for i, r in enumerate(lex_rows):
        kk = key(r)
        scores[kk] = scores.get(kk, 0.0) + 1.0 / (k_rrf + i + 1)
        pick.setdefault(kk, r)

    merged = []
    for kk, s in scores.items():
        r = dict(pick[kk]); r["score"] = s
        merged.append(r)

    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged[:k]

@router.post("/search", response_model=SearchResponse, summary="Hybrid (semantic + lexical) search")
def search(req: SearchRequest) -> SearchResponse:
    k = req.k
    k_sem = max(k * 3, 12)
    k_lex = max(k * 3, 12)
    with get_conn() as con:
        v = _get_or_make_query_vec(con, req.query)
        v_lit = _pgvector_literal(v)
        sem = _semantic_topk(con, v_lit, k_sem)
        lex = _lexical_topk(con, req.query, k_lex)
        merged = _rrf_merge(sem, lex, k)
    rows: List[Passage] = []
    for r in merged:
        excerpt = r["content"] or ""
        if len(excerpt) > 420:
            excerpt = excerpt[:420].rstrip() + "…"
        rows.append(Passage(
            document_id=r["document_id"],
            title=r["title"],
            path=r["path"],
            chunk_index=r["chunk_index"],
            excerpt=excerpt,
            score=float(r["score"]),
            content=None,
        ))
    return SearchResponse(results=rows)