# api/app/pdf_utils.py
import io, os, hashlib
from typing import List, Dict, Any, Optional
import pdfplumber
from PIL import Image

FIG_DIR = os.getenv("FIG_OUT_DIR", "static/figures")

def _sha1_bytes(b: bytes) -> str:
    return hashlib.sha1(b).hexdigest()

def extract_tables_pdfplumber(pdf_path: str, max_pages: int = 50) -> List[Dict[str, Any]]:
    out = []
    with pdfplumber.open(pdf_path) as pdf:
        for pi, page in enumerate(pdf.pages[:max_pages]):
            # pdfplumber's basic table extractor (works surprisingly often)
            tables = page.extract_tables()
            for t in tables or []:
                # Normalize to CSV
                rows = [",".join((c or "").replace(",", " ").strip()) for c in t]
                csv = "\n".join(rows)
                if not csv.strip():
                    continue
                preview_md = "\n".join([f"| {' | '.join(r.split(','))} |" for r in rows[:6]])
                out.append(dict(page=pi+1, csv=csv, preview_md=preview_md))
    return out

def extract_figures_pymupdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Uses pdfplumber raster (fast path) for embedded images (works for most PDFs).
    If a page has XObjects, we export them as PNGs.
    """
    os.makedirs(FIG_DIR, exist_ok=True)
    found = []
    with pdfplumber.open(pdf_path) as pdf:
        for pi, page in enumerate(pdf.pages):
            # page.images is a list of embedded image metadata
            for imeta in page.images:
                x0, y0, x1, y1 = imeta["x0"], imeta["y0"], imeta["x1"], imeta["y1"]
                # Crop the region out of a rasterized page
                # Render at higher DPI for legibility
                im = page.to_image(resolution=180).original
                w, h = im.size
                # pdfplumber coords are in PDF points (origin bottom-left).
                # The rendered image has origin top-left; flip Y.
                crop = im.crop((int(x0), int(h - y1), int(x1), int(h - y0)))
                buf = io.BytesIO()
                crop.save(buf, format="PNG")
                b = buf.getvalue()
                sha1 = _sha1_bytes(b)
                out_path = os.path.join(FIG_DIR, f"{sha1}.png")
                if not os.path.exists(out_path):
                    with open(out_path, "wb") as f:
                        f.write(b)
                found.append(dict(
                    page=pi+1,
                    bbox={"x0":x0,"y0":y0,"x1":x1,"y1":y1},
                    image_path=out_path,
                    sha1=sha1,
                    caption=None,   # optional: fill later with nearby text
                ))
    return found