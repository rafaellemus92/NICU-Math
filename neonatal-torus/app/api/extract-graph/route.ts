import { NextRequest, NextResponse } from "next/server";
import { extractGraphFromChunks } from "@/lib/graph-extract";

/**
 * POST /api/extract-graph
 *
 * Auto-extracts graph nodes and edges from uploaded PDF chunks.
 * Optionally filter by documentId.
 *
 * This is the "make it work automatically" endpoint — no manual
 * concept creation needed.
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const documentId = body.documentId ? parseInt(body.documentId) : undefined;

    const result = extractGraphFromChunks({ documentId });

    return NextResponse.json({
      success: true,
      ...result,
      message: `Extracted ${result.nodesCreated} nodes and ${result.edgesCreated} edges from ${result.chunksProcessed} chunks`,
    });
  } catch (error) {
    console.error("Graph extraction error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Extraction failed" },
      { status: 500 }
    );
  }
}
