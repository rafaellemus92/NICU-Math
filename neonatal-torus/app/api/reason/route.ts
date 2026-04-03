import { NextRequest, NextResponse } from "next/server";
import {
  parseQuery, rankConcepts, buildFocusedState,
  getAllNodes, getAllEdges, getAvailableTraversals, traversePath,
} from "@/lib/graph-engine";
import type { TraversalMode } from "@/lib/graph-types";

/**
 * GET /api/reason?q=...&focusId=...
 *
 * The core reasoning endpoint. Accepts either:
 * - A free-text query (board-style stem fragment)
 * - A focusId (direct concept selection)
 * - Both (query + focus for refinement)
 *
 * Returns a FocusedTorusState with ranked concepts, differentials,
 * active pathways, domain heat, and jump points.
 */
export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q") || "";
  const focusId = req.nextUrl.searchParams.get("focusId");

  const state = buildFocusedState(
    q,
    focusId ? parseInt(focusId) : undefined
  );

  return NextResponse.json(state);
}

/**
 * GET /api/reason/graph
 *
 * Returns the full graph for torus rendering.
 */
export async function POST(req: NextRequest) {
  const body = await req.json();
  const action = body.action;

  if (action === "graph") {
    const nodes = getAllNodes();
    const edges = getAllEdges();
    return NextResponse.json({ nodes, edges });
  }

  if (action === "traverse") {
    const { nodeId, mode } = body;
    if (!nodeId || !mode) {
      return NextResponse.json({ error: "nodeId and mode required" }, { status: 400 });
    }
    const result = traversePath(nodeId, mode as TraversalMode);
    const available = getAvailableTraversals(nodeId);
    return NextResponse.json({ ...result, available });
  }

  if (action === "parse") {
    const { query } = body;
    const features = parseQuery(query || "");
    const ranked = rankConcepts(features);
    return NextResponse.json({ features, ranked });
  }

  return NextResponse.json({ error: "Unknown action" }, { status: 400 });
}
