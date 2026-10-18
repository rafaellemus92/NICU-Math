"""Local synthetic research API; evidence services are opt-in."""
from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, HTTPException
from bayes import router as bayes_router

# Fail closed: only an explicit 0 enables legacy external services.
OFFLINE = os.getenv("NICU_OFFLINE", "1") != "0"


@asynccontextmanager
async def lifespan(_: FastAPI):
    if not OFFLINE:
        from db import ensure_schema
        ensure_schema()
    yield


app = FastAPI(title="NICU Synthetic Research API", lifespan=lifespan)
app.include_router(bayes_router, tags=["scenario"])

if OFFLINE:
    @app.post("/search")
    @app.post("/answer")
    def evidence_unavailable():
        raise HTTPException(503, "Evidence services are disabled in offline mode.")
else:
    from search import router as search_router
    from answer import router as answer_router
    app.include_router(search_router, tags=["search"])
    app.include_router(answer_router, tags=["answer"])


@app.get("/healthz", summary="Health check")
def healthz():
    return {"status": "ok", "mode": "offline" if OFFLINE else "evidence"}
