# api/app/answer.py
from typing import List, Optional, Dict, Any
import os

from fastapi import APIRouter
from pydantic import BaseModel, Field
from openai import OpenAI

from .db import get_conn
from .search import _embed, _pgvector_literal, Passage  # reuse Passage schema

router = APIRouter()

# ---------------- LLM setup (optional) ----------------
ANSWER_MODEL = os.getenv("ANSWER_MODEL", "gpt-4o-mini")


def _get_openai_client() -> Optional[OpenAI]:
    """Create a client only if OPENAI_API_KEY is available.
    This avoids crashing the API on startup if the key isn't set.
    """
    if os.getenv("NICU_OFFLINE", "1") != "0":
        return None
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    try:
        return OpenAI(api_key=key)
    except Exception:
        return None


_openai_client: Optional[OpenAI] = _get_openai_client()


# ---------------- Schemas ----------------
class AnswerRequest(BaseModel):
    query: str = Field(..., description="Clinical question")
    k: int = Field(6, ge=1, le=20, description="How many passages to use")


class Citation(BaseModel):
    document_id: int
    title: Optional[str]
    path: Optional[str]
    chunk_index: int
    snippet: str


class AnswerResponse(BaseModel):
    answer: str
    answer_markdown: str
    citations: List[Citation]
    sources: List[Passage]  # for UI “Sources” accordion


# ---------------- Data access ----------------

def _fetch_passages(query: str, k: int) -> List[Dict[str, Any]]:
    """Semantic top-k by pgvector distance."""
    vec = _embed(query)
    v_lit = _pgvector_literal(vec)

    sql = """
    SELECT
        d.id AS document_id,
        d.title,
        d.source_path AS path,
        c.chunk_index,
        c.content,
        (c.embedding <-> %(v)s::vector) AS score
    FROM chunks c
    JOIN documents d ON d.id = c.document_id
    ORDER BY c.embedding <-> %(v)s::vector
    LIMIT %(k)s;
    """

    rows: List[Dict[str, Any]] = []
    with get_conn() as con, con.cursor() as cur:
        cur.execute(sql, {"v": v_lit, "k": k})
        for r in cur.fetchall():
            rows.append(
                {
                    "document_id": r[0],
                    "title": r[1],
                    "path": r[2],
                    "chunk_index": r[3],
                    "content": r[4],
                    "score": float(r[5]),
                }
            )
    return rows


# ---------------- Formatting helpers ----------------

def _format_citations(passages: List[Dict[str, Any]]) -> List[Citation]:
    """
    Convert raw passage rows into lightweight citation objects for the UI.
    Trims long snippets and guards against missing fields.
    """
    out: List[Citation] = []
    for p in passages:
        snippet = (p.get("content") or "").strip()
        if len(snippet) > 480:
            snippet = snippet[:480].rstrip() + "…"
        out.append(
            Citation(
                document_id=int(p.get("document_id")),
                title=p.get("title"),
                path=p.get("path"),
                chunk_index=int(p.get("chunk_index")),
                snippet=snippet,
            )
        )
    return out


def _cheap_extractive_answer(query: str, passages: List[Dict[str, Any]]) -> str:
    if not passages:
        return f"**Question:** {query}\n\n_No evidence passages found._"

    bullets = []
    for p in passages[: min(5, len(passages))]:
        text = " ".join((p["content"] or "").split())
        if len(text) > 220:
            text = text[:220].rstrip() + "…"
        src = p["title"] or (p["path"] or "document")
        bullets.append(f"- **{src} (chunk {p['chunk_index']})**: {text}")

    return (
        f"### Clinical Question\n{query}\n\n"
        f"### Key Extracted Evidence\n" + "\n".join(bullets) +
        "\n\n### Quick Take\nPatterns only, not synthesized. See full LLM answer for interpretation."
    )

# ---------------- LLM answer (optional) ----------------

def _llm_answer(query: str, passages: List[Dict[str, Any]]) -> str:
    """
    Produces a research-only summary.
    Uses only retrieved passages and returns a consistent Markdown layout.
    """
    if _openai_client is None:
        raise RuntimeError("OpenAI client not available")

    # Build a compact, numbered context to support clean [1],[2] citations
    context_blocks: List[str] = []
    for i, p in enumerate(passages, 1):
        title = p.get("title") or (p.get("path") or "document")
        snippet = (p.get("content") or "").strip()
        if len(snippet) > 1800:
            snippet = snippet[:1800].rsplit(" ", 1)[0] + " …"
        context_blocks.append(f"[{i}] {title} (chunk {p.get('chunk_index')}):\n{snippet}")
    context = "\n\n".join(context_blocks)

    prompt = (
        f"Synthetic research question: {query}\n\n"
        "Summarize ONLY the numbered passages for research and education. "
        "Separate reported evidence, hypotheses and unvalidated models. "
        "Do not provide patient-specific treatment recommendations, doses or action plans. "
        "State uncertainty and cite passage numbers.\n\n"
        f"Passages:\n{context}\n"
    )

    resp = _openai_client.chat.completions.create(
        model=ANSWER_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a synthetic research and education assistant. "
                    "Use only supplied passages, distinguish evidence from speculation, "
                    "and do not give patient-specific treatment recommendations."
                )
            },
            {
                "role": "user",
                "content": prompt  # your assembled question + numbered passages
            },
        ],
        temperature=0.1,  # tighter, more repeatable
        top_p=0.9,  # slight diversity without drift
        presence_penalty=0.0,
        frequency_penalty=0.0,
        max_tokens=600,  # keeps it succinct; raise if you routinely truncate
        timeout=20,
    )
    text = resp.choices[0].message.content.strip()

    header = "**Research summary — not clinically validated**\n\n"
    footer = "\n\n---\n_Answer generated strictly from retrieved passages._"
    return header + text + footer

# ---------------- Route ----------------

@router.post("/answer", response_model=AnswerResponse, summary="Answer a clinical question")
def answer(req: AnswerRequest) -> AnswerResponse:
    passages = _fetch_passages(req.query, req.k)
    citations = _format_citations(passages)

    try:
        final_text = _llm_answer(req.query, passages) if passages else "No evidence passages found."
    except Exception:
        final_text = _cheap_extractive_answer(req.query, passages)

    # Dicts → Passage objects for the UI “sources” list
    # Provide excerpt=content (UI only displays excerpt)
    sources: List[Passage] = [
        Passage(
            document_id=p["document_id"],
            title=p["title"],
            path=p["path"],
            chunk_index=p["chunk_index"],
            content=p["content"],
            excerpt=p["content"],
            score=p["score"],
        )
        for p in passages
    ]

    return AnswerResponse(
        answer=final_text,
        answer_markdown=final_text,
        citations=citations,
        sources=sources,
    )