"use client";

import { useState, useEffect, useCallback, Component, type ReactNode } from "react";
import dynamic from "next/dynamic";
import { ABP_DOMAINS } from "@/lib/domains";
import ConceptPanel from "@/components/ConceptPanel";
import TraversalPanel from "@/components/TraversalPanel";
import type { TorusConcept, TorusEdge, TorusDensity, FiberHoverInfo, TraversalPathData } from "@/components/ConceptTorus";
import type { ActiveTraversal } from "@/components/TraversalPanel";

// ── Error Boundary for Three.js ────────────────────────────────────

class TorusErrorBoundary extends Component<
  { children: ReactNode; onError?: (error: Error) => void },
  { error: Error | null }
> {
  constructor(props: { children: ReactNode; onError?: (error: Error) => void }) {
    super(props);
    this.state = { error: null };
  }
  static getDerivedStateFromError(error: Error) {
    return { error };
  }
  componentDidCatch(error: Error) {
    this.props.onError?.(error);
  }
  render() {
    if (this.state.error) {
      return (
        <div className="w-full h-full bg-zinc-950 flex items-center justify-center p-8">
          <div className="bg-red-950/50 border border-red-800 rounded-xl p-6 max-w-lg text-center">
            <div className="text-red-400 font-bold text-sm mb-2">Torus Render Error</div>
            <div className="text-red-300/70 text-xs font-mono mb-4 break-all">
              {this.state.error.message}
            </div>
            <button
              onClick={() => this.setState({ error: null })}
              className="px-3 py-1.5 text-xs bg-zinc-800 text-zinc-300 rounded hover:bg-zinc-700"
            >
              Retry
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

const ConceptTorus = dynamic(() => import("@/components/ConceptTorus"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full bg-zinc-950 flex items-center justify-center">
      <div className="text-zinc-600 text-sm">Loading torus...</div>
    </div>
  ),
});

// ── Graph data validation ──────────────────────────────────────────

interface GraphMeta {
  source: string;
  nodeCount: number;
  edgeCount: number;
  droppedEdges: number;
}

function validateGraphData(
  concepts: TorusConcept[],
  edges: TorusEdge[]
): { valid: boolean; issues: string[] } {
  const issues: string[] = [];
  const nodeIds = new Set(concepts.map((c) => c.id));

  // Check for concepts missing required fields
  for (const c of concepts) {
    if (!c.slug) issues.push(`Node ${c.id} (${c.name}) missing slug`);
    if (!c.primary_domain) issues.push(`Node ${c.id} (${c.name}) missing primary_domain`);
  }

  // Check for edges referencing missing nodes
  let danglingCount = 0;
  for (const e of edges) {
    if (!nodeIds.has(e.source_id) || !nodeIds.has(e.target_id)) {
      danglingCount++;
    }
  }
  if (danglingCount > 0) {
    issues.push(`${danglingCount} edges reference missing nodes`);
  }

  return { valid: issues.length === 0, issues };
}

export default function TorusPage() {
  // Data
  const [concepts, setConcepts] = useState<TorusConcept[]>([]);
  const [edges, setEdges] = useState<TorusEdge[]>([]);
  const [density, setDensity] = useState<TorusDensity[]>([]);
  const [seeded, setSeeded] = useState(false);
  const [graphMeta, setGraphMeta] = useState<GraphMeta | null>(null);
  const [graphIssues, setGraphIssues] = useState<string[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [resetting, setResetting] = useState(false);

  // UI state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<TorusConcept[]>([]);
  const [selectedConcept, setSelectedConcept] = useState<TorusConcept | null>(null);
  const [focusConceptId, setFocusConceptId] = useState<number | null>(null);
  const [activeDomain, setActiveDomain] = useState<string | null>(null);
  const [fiberHover, setFiberHover] = useState<FiberHoverInfo | null>(null);
  const [showSearch, setShowSearch] = useState(false);
  const [activePanel, setActivePanel] = useState<"concept" | "traversal">("concept");
  const [traversalPath, setTraversalPath] = useState<TraversalPathData | null>(null);

  // Load graph data with validation
  const loadGraph = useCallback(() => {
    setLoadError(null);
    fetch("/api/graph")
      .then((r) => {
        if (!r.ok) throw new Error(`Graph API returned ${r.status}`);
        return r.json();
      })
      .then((d) => {
        const c = d.concepts || [];
        const e = d.edges || [];
        const dens = d.density || [];

        // Validate before setting state
        const { issues } = validateGraphData(c, e);
        setGraphIssues(issues);
        setGraphMeta(d._meta || null);

        // Filter out any concepts missing slug (would crash torus)
        const validConcepts = c.filter((n: TorusConcept) => n.slug && n.primary_domain);
        setConcepts(validConcepts);
        setEdges(e);
        setDensity(dens);
      })
      .catch((err) => {
        setLoadError(err instanceof Error ? err.message : "Failed to load graph");
        setConcepts([]);
        setEdges([]);
      });
  }, []);

  useEffect(() => {
    loadGraph();
  }, [loadGraph]);

  // Seed example data
  const seedExamples = useCallback(async () => {
    setSeeded(true);
    await fetch("/api/seed-examples", { method: "POST" });
    loadGraph();
  }, [loadGraph]);

  // Reset and rebuild graph
  const resetAndRebuild = useCallback(async () => {
    setResetting(true);
    setLoadError(null);
    setGraphIssues([]);
    try {
      await fetch("/api/reset-graph", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ clear_v2: true, clear_legacy: true, reseed: true, extract: true }),
      });
      loadGraph();
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : "Reset failed");
    } finally {
      setResetting(false);
    }
  }, [loadGraph]);

  // Search concepts
  useEffect(() => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }
    const q = searchQuery.toLowerCase();
    const matches = concepts.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        (c.ring1_identity && c.ring1_identity.toLowerCase().includes(q))
    );
    setSearchResults(matches.slice(0, 12));
  }, [searchQuery, concepts]);

  // Select a concept
  const selectConcept = useCallback(
    (concept: TorusConcept) => {
      setSelectedConcept(concept);
      setFocusConceptId(concept.id);
      setSearchQuery("");
      setSearchResults([]);
      setShowSearch(false);
    },
    []
  );

  // Navigate to a connected concept (from panel or traversal)
  const navigateToConcept = useCallback(
    (conceptId: number) => {
      const c = concepts.find((x) => x.id === conceptId);
      if (c) selectConcept(c);
    },
    [concepts, selectConcept]
  );

  // Handle traversal changes
  const handleTraversalChange = useCallback(
    (traversal: ActiveTraversal | null) => {
      if (traversal && traversal.conceptIds.length > 1) {
        setTraversalPath({
          conceptIds: traversal.conceptIds,
          currentStep: traversal.currentStep,
          relation: traversal.relation,
        });
      } else {
        setTraversalPath(null);
      }
    },
    []
  );

  // Clear focus
  const clearFocus = useCallback(() => {
    setSelectedConcept(null);
    setFocusConceptId(null);
    setTraversalPath(null);
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "/" && !showSearch) {
        e.preventDefault();
        setShowSearch(true);
      }
      if (e.key === "Escape") {
        if (showSearch) {
          setShowSearch(false);
          setSearchQuery("");
        } else if (selectedConcept) {
          clearFocus();
        }
      }
      // Tab between concept and traversal panels
      if (e.key === "t" && selectedConcept && !showSearch) {
        e.preventDefault();
        setActivePanel((p) => (p === "concept" ? "traversal" : "concept"));
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [showSearch, selectedConcept, clearFocus]);

  const panelOpen = !!selectedConcept;

  return (
    <div className="fixed inset-0 bg-zinc-950 flex flex-col" style={{ top: "49px" }}>
      {/* Top bar */}
      <div className="shrink-0 flex items-center justify-between px-4 py-2 border-b border-zinc-800/50 bg-zinc-950/80 backdrop-blur-sm z-20">
        <div className="flex items-center gap-3">
          <h1 className="text-sm font-bold text-zinc-300">Torus</h1>

          {/* Search */}
          <div className="relative">
            {showSearch ? (
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search concept..."
                  className="w-72 bg-zinc-900 border border-zinc-600 rounded-lg px-3 py-1.5 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
                  autoFocus
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && searchResults[0]) {
                      selectConcept(searchResults[0]);
                    }
                  }}
                />
                {searchResults.length > 0 && (
                  <div className="absolute top-full left-0 right-0 mt-1 bg-zinc-900 border border-zinc-700 rounded-lg overflow-hidden shadow-xl z-50">
                    {searchResults.map((c) => (
                      <button
                        key={c.id}
                        onClick={() => selectConcept(c)}
                        className="w-full text-left px-3 py-2 text-sm hover:bg-zinc-800 transition-colors flex items-center gap-2"
                      >
                        <div
                          className="w-2 h-2 rounded-full shrink-0"
                          style={{
                            backgroundColor:
                              ABP_DOMAINS.find((d) => d.id === c.primary_domain)
                                ?.color || "#71717A",
                          }}
                        />
                        <span className="text-zinc-200 font-medium truncate">
                          {c.name}
                        </span>
                        <span className="text-[10px] text-zinc-500 ml-auto shrink-0">
                          {ABP_DOMAINS.find((d) => d.id === c.primary_domain)
                            ?.abbrev || c.primary_domain}
                        </span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={() => setShowSearch(true)}
                className="flex items-center gap-2 px-3 py-1.5 bg-zinc-900 border border-zinc-800 rounded-lg text-zinc-500 text-sm hover:border-zinc-600 transition-colors"
              >
                <span>Search concept</span>
                <kbd className="text-[9px] bg-zinc-800 px-1 py-0.5 rounded text-zinc-600">/</kbd>
              </button>
            )}
          </div>

          {/* Focus indicator */}
          {selectedConcept && (
            <div className="flex items-center gap-2 px-3 py-1 bg-zinc-900 border border-zinc-700 rounded-lg">
              <div
                className="w-2 h-2 rounded-full"
                style={{
                  backgroundColor:
                    ABP_DOMAINS.find((d) => d.id === selectedConcept.primary_domain)
                      ?.color || "#71717A",
                }}
              />
              <span className="text-xs text-zinc-200 font-medium">
                {selectedConcept.name}
              </span>
              <button
                onClick={clearFocus}
                className="text-zinc-500 hover:text-zinc-300 text-xs ml-1"
              >
                x
              </button>
            </div>
          )}

          {/* Traversal indicator */}
          {traversalPath && (
            <div className="flex items-center gap-1 px-2 py-1 bg-amber-400/10 border border-amber-400/20 rounded-lg">
              <span className="text-[10px] text-amber-400">
                Traversing: {traversalPath.relation}
              </span>
              <span className="text-[10px] text-amber-400/60">
                step {traversalPath.currentStep + 1}/{traversalPath.conceptIds.length}
              </span>
            </div>
          )}
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-2">
          {/* Panel toggle */}
          {selectedConcept && (
            <div className="flex gap-0.5 bg-zinc-900 border border-zinc-800 rounded-lg p-0.5">
              <button
                onClick={() => setActivePanel("concept")}
                className={`px-2 py-1 text-[10px] rounded transition-colors ${
                  activePanel === "concept"
                    ? "bg-zinc-700 text-zinc-200"
                    : "text-zinc-500 hover:text-zinc-300"
                }`}
              >
                Concept
              </button>
              <button
                onClick={() => setActivePanel("traversal")}
                className={`px-2 py-1 text-[10px] rounded transition-colors ${
                  activePanel === "traversal"
                    ? "bg-amber-400/20 text-amber-400"
                    : "text-zinc-500 hover:text-zinc-300"
                }`}
              >
                Traverse
              </button>
            </div>
          )}

          {/* Seed / Extract buttons */}
          {concepts.length === 0 && !seeded && (
            <div className="flex gap-2">
              <button
                onClick={seedExamples}
                className="px-3 py-1.5 text-[10px] bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg hover:bg-amber-400/20 transition-colors"
              >
                Seed example data
              </button>
              <button
                onClick={async () => {
                  setSeeded(true);
                  await fetch("/api/seed-graph", { method: "POST" });
                  await fetch("/api/extract-graph", { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
                  loadGraph();
                }}
                className="px-3 py-1.5 text-[10px] bg-emerald-400/10 text-emerald-400 border border-emerald-400/30 rounded-lg hover:bg-emerald-400/20 transition-colors"
              >
                Build graph from PDFs
              </button>
            </div>
          )}

          {/* Domain filter pills */}
          <div className="flex gap-0.5">
            {ABP_DOMAINS.filter((d) => d.exam_percent >= 5).map((d) => (
              <button
                key={d.id}
                onClick={() =>
                  setActiveDomain(activeDomain === d.id ? null : d.id)
                }
                className="w-3 h-3 rounded-sm transition-all hover:scale-150"
                style={{
                  backgroundColor:
                    activeDomain === d.id ? d.color : d.color + "40",
                  border:
                    activeDomain === d.id
                      ? `1px solid ${d.color}`
                      : "1px solid transparent",
                }}
                title={`${d.name} (${d.exam_percent}%)`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex min-h-0 relative">
        {/* Error / issue banners */}
        {loadError && (
          <div className="absolute top-2 left-1/2 -translate-x-1/2 z-30 bg-red-950/90 border border-red-800 rounded-lg px-4 py-2 text-xs text-red-300 flex items-center gap-3 backdrop-blur-sm">
            <span>Graph load error: {loadError}</span>
            <button onClick={resetAndRebuild} disabled={resetting}
              className="px-2 py-1 bg-red-800/50 rounded text-red-200 hover:bg-red-700/50 disabled:opacity-50">
              {resetting ? "Resetting..." : "Reset & Rebuild"}
            </button>
          </div>
        )}
        {graphIssues.length > 0 && !loadError && (
          <div className="absolute top-2 left-1/2 -translate-x-1/2 z-30 bg-amber-950/90 border border-amber-800 rounded-lg px-4 py-2 text-xs text-amber-300 flex items-center gap-3 backdrop-blur-sm">
            <div>
              <span className="font-bold">Graph issues:</span>{" "}
              {graphIssues.slice(0, 2).join("; ")}
              {graphIssues.length > 2 && ` (+${graphIssues.length - 2} more)`}
            </div>
            <button onClick={resetAndRebuild} disabled={resetting}
              className="px-2 py-1 bg-amber-800/50 rounded text-amber-200 hover:bg-amber-700/50 shrink-0 disabled:opacity-50">
              {resetting ? "Fixing..." : "Fix"}
            </button>
          </div>
        )}

        {/* Torus viewport with error boundary */}
        <div className="flex-1">
          <TorusErrorBoundary onError={(e) => setLoadError(e.message)}>
            <ConceptTorus
              concepts={concepts}
              edges={edges}
              chunkDensity={density}
              focusConceptId={focusConceptId}
              activeDomain={activeDomain}
              traversalPath={traversalPath}
              onConceptSelect={selectConcept}
              onDomainSelect={setActiveDomain}
              onFiberHover={setFiberHover}
            />
          </TorusErrorBoundary>
        </div>

        {/* Right panel */}
        {panelOpen && selectedConcept && (
          <div className="w-[340px] shrink-0 overflow-hidden">
            {activePanel === "concept" ? (
              <ConceptPanel
                concept={selectedConcept}
                onClose={clearFocus}
                onConceptNavigate={navigateToConcept}
              />
            ) : (
              <TraversalPanel
                conceptId={selectedConcept.id}
                conceptName={selectedConcept.name}
                onTraversalChange={handleTraversalChange}
                onJumpToNode={navigateToConcept}
              />
            )}
          </div>
        )}

        {/* Fiber hover tooltip */}
        {fiberHover && (
          <div
            className="fixed z-50 pointer-events-none"
            style={{
              left: fiberHover.screenPos.x + 12,
              top: fiberHover.screenPos.y - 20,
            }}
          >
            <div className="bg-zinc-900/95 border border-zinc-700 rounded-lg px-3 py-2 text-[10px] shadow-xl backdrop-blur-sm">
              <div className="text-zinc-200 font-bold">
                {fiberHover.sourceName}{" "}
                <span className="text-zinc-500">→</span>{" "}
                {fiberHover.targetName}
              </div>
              <div className="flex items-center gap-2 mt-1 text-zinc-400">
                <span className="font-mono">{fiberHover.relationType}</span>
                <span>weight: {Math.round(fiberHover.weight * 100)}%</span>
              </div>
              {fiberHover.explanation && (
                <div className="text-zinc-500 mt-1 max-w-48">
                  {fiberHover.explanation}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Legend */}
        <div className="absolute bottom-3 left-3 bg-zinc-900/70 backdrop-blur-sm border border-zinc-800/50 rounded-lg p-2.5 text-[9px] z-10">
          <div className="text-zinc-500 uppercase tracking-wider mb-1 font-bold">
            Navigation
          </div>
          <div className="text-zinc-500 space-y-0.5">
            <div>
              <span className="text-zinc-400">/</span> search ·{" "}
              <span className="text-zinc-400">click</span> node ·{" "}
              <span className="text-zinc-400">t</span> toggle traverse ·{" "}
              <span className="text-zinc-400">ESC</span> clear
            </div>
            <div>Ring = Domain · Tube = Timeline · Size = Relevance</div>
          </div>
          {traversalPath && (
            <div className="mt-1.5 text-amber-400/60">
              <span className="text-amber-400">Traversal:</span>{" "}
              <span className="text-zinc-400">←</span>{" "}
              <span className="text-zinc-400">→</span> step ·{" "}
              <span className="text-zinc-400">space</span> play
            </div>
          )}
        </div>

        {/* Stats */}
        <div className="absolute bottom-3 right-3 text-[9px] text-zinc-700 z-10">
          {concepts.length} concepts · {edges.length} edges ·{" "}
          {density.reduce((s, d) => s + d.count, 0)} chunks
        </div>
      </div>
    </div>
  );
}
