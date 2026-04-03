#!/usr/bin/env python3
"""
generate_canvas.py — NICU Torus Obsidian Canvas Generator
==========================================================
Scans 02_Topics/ subdirectories for Markdown files, reads YAML frontmatter
to extract domain and ring_focus metadata, then generates a radial
Obsidian Canvas JSON file (Canvas/NICU Torus Map.canvas).

Layout model
------------
  Orbit 0 (r=0)     : Center "NICU Torus" text card
  Orbit 1 (r=600)   : One file node per unique domain, evenly spaced on a circle
  Orbit 2 (r=1100)  : Topic file nodes clustered near their domain node
  Orbit 3 (r=1600+) : Concept-layer text cards for topics that have ring_focus
                      defined in frontmatter; each topic cluster uses a slightly
                      larger radius than its neighbour to avoid overlaps

Edge colour legend
------------------
  #888888  center  → domain
  #4a9eff  domain  → topic   (Respiratory)
  #ff4a4a  domain  → topic   (Cardiovascular)
  #aaaaaa  domain  → topic   (all other domains)
  #aa55ff  cross-domain link from related_notes frontmatter field
  #666666  topic   → concept spoke

Usage
-----
  cd NICU_Torus
  python generate_canvas.py                      # writes Canvas/NICU Torus Map.canvas
  python generate_canvas.py -o my_canvas.canvas  # custom output path
  python generate_canvas.py --topics-dir 02_Topics --output Canvas/out.canvas

Requirements: Python 3.7+.  PyYAML is used when available; falls back to a
built-in regex parser so no pip install is required.
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# YAML frontmatter parsing
# ---------------------------------------------------------------------------

def _parse_yaml_pyyaml(text: str) -> Dict[str, Any]:
    """Parse YAML using PyYAML."""
    import yaml  # type: ignore
    return yaml.safe_load(text) or {}


def _parse_yaml_regex(text: str) -> Dict[str, Any]:
    """
    Minimal fallback YAML parser using regex.
    Handles simple scalar values and flat lists (- item).
    Does not support nested mappings.
    """
    result: Dict[str, Any] = {}
    lines = text.splitlines()
    current_key: Optional[str] = None
    current_list: Optional[List[str]] = None

    for line in lines:
        # List item
        list_match = re.match(r"^  - (.+)$", line)
        if list_match and current_key is not None:
            if current_list is None:
                current_list = []
                result[current_key] = current_list
            current_list.append(list_match.group(1).strip())
            continue

        # Key: value
        kv_match = re.match(r"^(\w[\w_-]*)\s*:\s*(.*)", line)
        if kv_match:
            current_key = kv_match.group(1)
            value = kv_match.group(2).strip()
            current_list = None
            if value == "" or value is None:
                result[current_key] = None
            else:
                # Strip surrounding quotes
                value = re.sub(r'^["\']|["\']$', "", value)
                result[current_key] = value
            continue

    return result


def parse_frontmatter(filepath: Path) -> Dict[str, Any]:
    """
    Read a Markdown file and return its YAML frontmatter as a dict.
    Returns an empty dict if there is no frontmatter or parsing fails.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError:
        return {}

    # YAML frontmatter is delimited by --- lines
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not fm_match:
        return {}

    raw_yaml = fm_match.group(1)

    # Try PyYAML first, fall back to regex parser
    try:
        return _parse_yaml_pyyaml(raw_yaml)
    except Exception:
        pass

    try:
        return _parse_yaml_regex(raw_yaml)
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def _round(v: float) -> int:
    return round(v)


def radial_pos(
    cx: float, cy: float, r: float, angle_deg: float
) -> Tuple[int, int]:
    """Return (x, y) for a point at radius r and angle_deg from (cx, cy)."""
    rad = math.radians(angle_deg)
    return _round(cx + r * math.cos(rad)), _round(cy + r * math.sin(rad))


def outward_side(angle_deg: float) -> str:
    """The side of a node that faces *away* from the centre."""
    a = angle_deg % 360
    if 315 <= a or a < 45:
        return "right"
    elif 45 <= a < 135:
        return "bottom"
    elif 135 <= a < 225:
        return "left"
    else:
        return "top"


def inward_side(angle_deg: float) -> str:
    """The side of a node that faces *toward* the centre."""
    a = angle_deg % 360
    if 315 <= a or a < 45:
        return "left"
    elif 45 <= a < 135:
        return "top"
    elif 135 <= a < 225:
        return "right"
    else:
        return "bottom"


# ---------------------------------------------------------------------------
# Domain colour map
# ---------------------------------------------------------------------------

DOMAIN_COLORS: Dict[str, str] = {
    "Respiratory":   "#4a9eff",
    "Cardiovascular": "#ff4a4a",
}
DEFAULT_TOPIC_COLOR = "#aaaaaa"


def topic_color(domain: str) -> str:
    return DOMAIN_COLORS.get(domain, DEFAULT_TOPIC_COLOR)


# ---------------------------------------------------------------------------
# Canvas building
# ---------------------------------------------------------------------------

CONCEPT_LAYERS = [
    "Development",
    "Physiology",
    "Pathophysiology",
    "Diagnosis",
    "Management",
    "Pearl",
]

# Node / layout constants
CX, CY = 0, 0
DOM_R = 600
TOPIC_R = 1100
SPOKE_R_BASE = 1600
SPOKE_R_STEP = 160   # each successive spoke cluster is pushed out by this amount

DOM_W, DOM_H = 240, 60
TOPIC_W, TOPIC_H = 220, 50
CENTER_W, CENTER_H = 300, 100
SPOKE_W, SPOKE_H = 160, 40

TOPIC_SPREAD_DEG = 100   # total angular spread for topics within a domain
SPOKE_SPREAD_DEG = 40    # total angular spread for concept spokes per topic


def slugify(text: str) -> str:
    """Convert a name to a compact lowercase slug."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def scan_topics(topics_dir: Path) -> List[Dict[str, Any]]:
    """
    Walk topics_dir and collect metadata from each .md file.
    Returns a list of dicts: {name, domain, subdir, path, frontmatter}.
    """
    topics = []
    for md_file in sorted(topics_dir.rglob("*.md")):
        # subdir relative to topics_dir
        try:
            rel = md_file.relative_to(topics_dir)
        except ValueError:
            continue
        subdir = rel.parts[0] if len(rel.parts) > 1 else ""
        fm = parse_frontmatter(md_file)
        domain = fm.get("domain") or subdir or "Unknown"
        topics.append({
            "name": md_file.stem,
            "domain": domain,
            "subdir": subdir,
            "path": md_file,
            "frontmatter": fm,
        })
    return topics


def build_canvas(
    topics_dir: Path,
    vault_root: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Build and return the Obsidian Canvas JSON dict.

    Parameters
    ----------
    topics_dir : path to the 02_Topics directory
    vault_root : root of the vault (used to compute relative file paths for
                 Obsidian; defaults to topics_dir.parent)
    """
    if vault_root is None:
        vault_root = topics_dir.parent

    topics = scan_topics(topics_dir)

    # Collect unique domains in insertion order
    seen_domains: Dict[str, int] = {}
    for t in topics:
        d = t["domain"]
        if d not in seen_domains:
            seen_domains[d] = len(seen_domains)
    domain_list = list(seen_domains.keys())
    n_domains = len(domain_list)

    # Group topics by domain
    by_domain: Dict[str, List[Dict[str, Any]]] = {d: [] for d in domain_list}
    for t in topics:
        by_domain[t["domain"]].append(t)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    # ── Center node ─────────────────────────────────────────────────────────
    nodes.append({
        "id": "center",
        "type": "text",
        "x": CX - CENTER_W // 2,
        "y": CY - CENTER_H // 2,
        "width": CENTER_W,
        "height": CENTER_H,
        "text": "# NICU Torus\nKnowledge Map",
    })

    # ── Orbit 1: Domain nodes ────────────────────────────────────────────────
    domain_angles: Dict[str, float] = {}
    domain_ids: Dict[str, str] = {}

    for i, domain in enumerate(domain_list):
        angle = -90.0 + i * (360.0 / n_domains)
        domain_angles[domain] = angle
        nid = f"dom-{slugify(domain)}"
        domain_ids[domain] = nid

        x, y = radial_pos(CX, CY, DOM_R, angle)

        # Build file path for domain hub note
        # Convention: 01_Domains/<Domain Name>.md
        dom_file = f"01_Domains/{domain}.md"

        nodes.append({
            "id": nid,
            "type": "file",
            "x": x - DOM_W // 2,
            "y": y - DOM_H // 2,
            "width": DOM_W,
            "height": DOM_H,
            "file": dom_file,
        })

        edges.append({
            "id": f"edge-center-{nid}",
            "fromNode": "center",
            "toNode": nid,
            "fromSide": outward_side(angle),
            "toSide": inward_side(angle),
            "color": "#888888",
        })

    # ── Orbit 2: Topic nodes ────────────────────────────────────────────────
    topic_ids: Dict[str, str] = {}   # keyed by topic name
    topic_angles: Dict[str, float] = {}

    for domain, dom_topics in by_domain.items():
        if not dom_topics:
            continue
        base_angle = domain_angles[domain]
        n = len(dom_topics)
        color = topic_color(domain)
        dom_nid = domain_ids[domain]

        for i, t in enumerate(dom_topics):
            if n == 1:
                angle = base_angle
            else:
                half = TOPIC_SPREAD_DEG / 2
                angle = base_angle - half + i * (TOPIC_SPREAD_DEG / (n - 1))

            nid = f"topic-{slugify(domain)}-{slugify(t['name'])}"
            topic_ids[t["name"]] = nid
            topic_angles[t["name"]] = angle

            # Relative path from vault root
            rel_path = t["path"].relative_to(vault_root)
            file_path = rel_path.as_posix()

            x, y = radial_pos(CX, CY, TOPIC_R, angle)
            nodes.append({
                "id": nid,
                "type": "file",
                "x": x - TOPIC_W // 2,
                "y": y - TOPIC_H // 2,
                "width": TOPIC_W,
                "height": TOPIC_H,
                "file": file_path,
            })

            edges.append({
                "id": f"edge-{slugify(domain)}-{nid}",
                "fromNode": dom_nid,
                "toNode": nid,
                "fromSide": outward_side(angle),
                "toSide": inward_side(angle),
                "color": color,
            })

    # ── Orbit 3: Concept spoke nodes ────────────────────────────────────────
    spoke_index = 0   # incremented per ring_focus topic to offset radii

    for t in topics:
        fm = t["frontmatter"]
        if not fm.get("ring_focus"):
            continue

        name = t["name"]
        parent_nid = topic_ids.get(name)
        if parent_nid is None:
            continue

        base_angle = topic_angles.get(name, 0.0)
        spoke_r = SPOKE_R_BASE + spoke_index * SPOKE_R_STEP
        spoke_index += 1
        slug = slugify(name)
        n_layers = len(CONCEPT_LAYERS)

        for j, layer in enumerate(CONCEPT_LAYERS):
            if n_layers == 1:
                angle = base_angle
            else:
                half = SPOKE_SPREAD_DEG / 2
                angle = base_angle - half + j * (SPOKE_SPREAD_DEG / (n_layers - 1))

            layer_slug = slugify(layer)
            nid = f"spoke-{slug}-{layer_slug}"
            x, y = radial_pos(CX, CY, spoke_r, angle)

            nodes.append({
                "id": nid,
                "type": "text",
                "x": x - SPOKE_W // 2,
                "y": y - SPOKE_H // 2,
                "width": SPOKE_W,
                "height": SPOKE_H,
                "text": layer,
            })

            edges.append({
                "id": f"edge-spoke-{slug}-{layer_slug}",
                "fromNode": parent_nid,
                "toNode": nid,
                "fromSide": outward_side(angle),
                "toSide": inward_side(angle),
                "color": "#666666",
            })

    # ── Cross-domain edges from related_notes frontmatter ───────────────────
    seen_cross: set = set()

    for t in topics:
        fm = t["frontmatter"]
        related = fm.get("related_notes")
        if not related:
            continue
        if isinstance(related, str):
            related = [related]

        src_nid = topic_ids.get(t["name"])
        if src_nid is None:
            continue

        for rel_name in related:
            rel_name = str(rel_name).strip()
            tgt_nid = topic_ids.get(rel_name)
            if tgt_nid is None or tgt_nid == src_nid:
                continue
            # Avoid duplicate bidirectional edges
            pair = tuple(sorted([src_nid, tgt_nid]))
            if pair in seen_cross:
                continue
            seen_cross.add(pair)

            edges.append({
                "id": f"edge-cross-{slugify(t['name'])}-{slugify(rel_name)}",
                "fromNode": src_nid,
                "toNode": tgt_nid,
                "fromSide": "right",
                "toSide": "left",
                "color": "#aa55ff",
            })

    return {"nodes": nodes, "edges": edges}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a radial Obsidian Canvas JSON file from NICU Torus topic notes."
        )
    )
    parser.add_argument(
        "--topics-dir",
        default="02_Topics",
        help="Path to the topics directory (default: 02_Topics)",
    )
    parser.add_argument(
        "--vault-root",
        default=None,
        help=(
            "Vault root directory used to compute relative file paths for Obsidian. "
            "Defaults to the parent of --topics-dir."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.path.join("Canvas", "NICU Torus Map.canvas"),
        help=(
            "Output canvas file path "
            "(default: Canvas/NICU Torus Map.canvas)"
        ),
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2)",
    )
    args = parser.parse_args()

    # Resolve paths relative to the script's own directory so the script can
    # be run from any working directory via `python generate_canvas.py`.
    script_dir = Path(__file__).parent.resolve()

    topics_dir = Path(args.topics_dir)
    if not topics_dir.is_absolute():
        topics_dir = script_dir / topics_dir
    topics_dir = topics_dir.resolve()

    if not topics_dir.is_dir():
        print(f"ERROR: topics directory not found: {topics_dir}", file=sys.stderr)
        sys.exit(1)

    vault_root = (
        Path(args.vault_root).resolve()
        if args.vault_root
        else topics_dir.parent
    )

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = script_dir / output_path
    output_path = output_path.resolve()

    print(f"Scanning: {topics_dir}", file=sys.stderr)
    canvas = build_canvas(topics_dir, vault_root)

    n_nodes = len(canvas["nodes"])
    n_edges = len(canvas["edges"])
    print(f"Built canvas: {n_nodes} nodes, {n_edges} edges", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(canvas, indent=args.indent, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Written: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
