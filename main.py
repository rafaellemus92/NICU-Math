# api/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles  # keep only this import
from contextlib import asynccontextmanager
from pathlib import Path
import logging, os

from .db import ensure_schema
from .search import router as search_router
from .answer import router as answer_router
from .bayes import router as bayes_router


logging.basicConfig(level=logging.INFO)
app = FastAPI(title="NICU API")

# Routes
app.include_router(search_router, tags=["search"])
app.include_router(answer_router, tags=["answer"])
app.include_router(bayes_router, tags=["scenario"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static PDFs under /files
library_dir = os.getenv("LIBRARY_DIR")
if not library_dir:
    candidates = [Path.cwd() / "library", Path(__file__).resolve().parent / "library"]
    for p in candidates:
        if p.exists():
            library_dir = str(p)
            break

if library_dir and Path(library_dir).exists():
    app.mount("/files", StaticFiles(directory=library_dir), name="files")
else:
    logging.getLogger("uvicorn.error").warning(
        "Static files directory not found; skipping /files mount. "
        "Set LIBRARY_DIR or create a 'library' folder."
    )

@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        ensure_schema()
        logging.info("✅ pgvector extension & schema ensured.")
    except Exception as e:
        logging.exception("❌ DB init failed (pgvector/schema).", exc_info=e)
        raise
    yield

app.router.lifespan_context = lifespan


@app.get("/healthz", summary="Health check")
def healthz():
    return {"status": "ok"}