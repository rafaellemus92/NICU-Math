"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { ABP_DOMAINS } from "@/lib/domains";

// ── Types ──────────────────────────────────────────────────────────

interface PathNode {
  conceptId: number;
  name: string;
  slug: string;
  domain: string;
  explanation: string | null;
  weight: number;
  step: number;
}

interface TraversalResult {
  path: PathNode[];
  originIndex: number;
  relation: string;
  availableRelations: { relation_type: string; count: number }[];
  totalSteps: number;
}

export interface ActiveTraversal {
  path: PathNode[];
  currentStep: number;
  relation: string;
  conceptIds: number[];
}

interface TraversalPanelProps {
  conceptId: number;
  conceptName: string;
  onTraversalChange: (traversal: ActiveTraversal | null) => void;
  onJumpToNode: (conceptId: number) => void;
}

// ── Relation type metadata ─────────────────────────────────────────

const RELATION_META: Record<string, { label: string; icon: string; color: string; description: string }> = {
  embryology: { label: "Embryology", icon: "E", color: "#818CF8", description: "Developmental origin chain" },
  physiology: { label: "Physiology", icon: "P", color: "#3B82F6", description: "Physiologic mechanism path" },
  timeline: { label: "Timeline", icon: "T", color: "#34D399", description: "Developmental stages in sequence" },
  differential: { label: "Differentials", icon: "D", color: "#EF4444", description: "Differential diagnosis chain" },
  distinction: { label: "Distinctions", icon: "X", color: "#F87171", description: "Key distinguishing features" },
  mimic: { label: "Mimics", icon: "M", color: "#FB923C", description: "Conditions that mimic each other" },
  management: { label: "Management", icon: "R", color: "#FBBF24", description: "Treatment/management pathway" },
  treatment: { label: "Treatment", icon: "R", color: "#FBBF24", description: "Treatment approach" },
  infectious_association: { label: "Infectious", icon: "I", color: "#F472B6", description: "Infectious disease associations" },
  anatomy: { label: "Anatomy", icon: "A", color: "#06B6D4", description: "Structural anatomy relations" },
  association: { label: "Associations", icon: "~", color: "#A78BFA", description: "Associated conditions" },
  mechanism: { label: "Mechanism", icon: "M", color: "#60A5FA", description: "Mechanistic pathway" },
  genetic: { label: "Genetic", icon: "G", color: "#C084FC", description: "Genetic linkage" },
  temporal: { label: "Temporal", icon: "T", color: "#5EEAD4", description: "Time-based relation" },
};

function domainColor(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.color || "#71717A";
}

function domainAbbrev(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.abbrev || id;
}

// ── Component ──────────────────────────────────────────────────────

export default function TraversalPanel({
  conceptId,
  conceptName,
  onTraversalChange,
  onJumpToNode,
}: TraversalPanelProps) {
  const [availableRelations, setAvailableRelations] = useState<
    { relation_type: string; count: number }[]
  >([]);
  const [activeRelation, setActiveRelation] = useState<string | null>(null);
  const [traversal, setTraversal] = useState<TraversalResult | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [loading, setLoading] = useState(false);
  const animationRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  // Load available relations when concept changes
  useEffect(() => {
    setActiveRelation(null);
    setTraversal(null);
    setCurrentStep(0);
    onTraversalChange(null);

    fetch(`/api/traverse?conceptId=${conceptId}&relation=association`)
      .then((r) => r.json())
      .then((d) => {
        setAvailableRelations(d.availableRelations || []);
      })
      .catch(() => {});
  }, [conceptId, onTraversalChange]);

  // Load path when relation is selected
  useEffect(() => {
    if (!activeRelation) {
      setTraversal(null);
      onTraversalChange(null);
      return;
    }

    setLoading(true);
    fetch(`/api/traverse?conceptId=${conceptId}&relation=${activeRelation}`)
      .then((r) => r.json())
      .then((data: TraversalResult) => {
        setTraversal(data);
        setCurrentStep(data.originIndex);
        onTraversalChange({
          path: data.path,
          currentStep: data.originIndex,
          relation: activeRelation,
          conceptIds: data.path.map((n) => n.conceptId),
        });
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [activeRelation, conceptId, onTraversalChange]);

  // Update parent when step changes
  useEffect(() => {
    if (traversal && activeRelation) {
      onTraversalChange({
        path: traversal.path,
        currentStep,
        relation: activeRelation,
        conceptIds: traversal.path.map((n) => n.conceptId),
      });
    }
  }, [currentStep, traversal, activeRelation, onTraversalChange]);

  // Step forward/backward
  const stepForward = useCallback(() => {
    if (!traversal) return;
    setCurrentStep((s) => {
      const next = Math.min(s + 1, traversal.path.length - 1);
      onJumpToNode(traversal.path[next].conceptId);
      return next;
    });
  }, [traversal, onJumpToNode]);

  const stepBackward = useCallback(() => {
    if (!traversal) return;
    setCurrentStep((s) => {
      const prev = Math.max(s - 1, 0);
      onJumpToNode(traversal.path[prev].conceptId);
      return prev;
    });
  }, [traversal, onJumpToNode]);

  // Auto-animate through path
  const toggleAnimation = useCallback(() => {
    if (isAnimating) {
      setIsAnimating(false);
      if (animationRef.current) clearTimeout(animationRef.current);
      return;
    }

    if (!traversal) return;
    setIsAnimating(true);
    setCurrentStep(0);
    onJumpToNode(traversal.path[0].conceptId);

    let step = 0;
    const animate = () => {
      step++;
      if (step >= traversal.path.length) {
        setIsAnimating(false);
        return;
      }
      setCurrentStep(step);
      onJumpToNode(traversal.path[step].conceptId);
      animationRef.current = setTimeout(animate, 1200);
    };
    animationRef.current = setTimeout(animate, 1200);
  }, [isAnimating, traversal, onJumpToNode]);

  // Cleanup animation on unmount
  useEffect(() => {
    return () => {
      if (animationRef.current) clearTimeout(animationRef.current);
    };
  }, []);

  // Jump to specific step
  const jumpToStep = useCallback(
    (step: number) => {
      if (!traversal) return;
      setCurrentStep(step);
      onJumpToNode(traversal.path[step].conceptId);
      if (isAnimating) {
        setIsAnimating(false);
        if (animationRef.current) clearTimeout(animationRef.current);
      }
    },
    [traversal, onJumpToNode, isAnimating]
  );

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!traversal) return;
      if (e.key === "ArrowRight" || e.key === "j") {
        e.preventDefault();
        stepForward();
      }
      if (e.key === "ArrowLeft" || e.key === "k") {
        e.preventDefault();
        stepBackward();
      }
      if (e.key === " " && traversal) {
        e.preventDefault();
        toggleAnimation();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [traversal, stepForward, stepBackward, toggleAnimation]);

  return (
    <div className="h-full flex flex-col bg-zinc-950/95 border-l border-zinc-800">
      {/* Header */}
      <div className="px-3 py-2.5 border-b border-zinc-800/50 shrink-0">
        <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1">
          Traversal Mode
        </div>
        <div className="text-xs text-zinc-300 font-medium truncate">
          {conceptName}
        </div>
      </div>

      {/* Relation type selector */}
      <div className="px-3 py-2 border-b border-zinc-800/50 shrink-0">
        <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-2">
          Follow Path
        </div>
        <div className="flex flex-wrap gap-1">
          {availableRelations.map(({ relation_type, count }) => {
            const meta = RELATION_META[relation_type] || {
              label: relation_type,
              icon: "?",
              color: "#71717A",
              description: "",
            };
            const isActive = activeRelation === relation_type;

            return (
              <button
                key={relation_type}
                onClick={() =>
                  setActiveRelation(isActive ? null : relation_type)
                }
                className={`flex items-center gap-1 px-2 py-1 rounded text-[10px] transition-all ${
                  isActive
                    ? "ring-1"
                    : "hover:bg-zinc-800"
                }`}
                style={{
                  backgroundColor: isActive ? meta.color + "20" : "transparent",
                  color: isActive ? meta.color : "#A1A1AA",
                  borderColor: isActive ? meta.color + "50" : "transparent",
                  outlineColor: isActive ? meta.color : undefined,
                }}
                title={meta.description}
              >
                <span
                  className="w-3.5 h-3.5 rounded-sm flex items-center justify-center text-[8px] font-bold"
                  style={{
                    backgroundColor: meta.color + "25",
                    color: meta.color,
                  }}
                >
                  {meta.icon}
                </span>
                <span>{meta.label}</span>
                <span className="text-zinc-600 ml-0.5">{count}</span>
              </button>
            );
          })}
        </div>

        {availableRelations.length === 0 && (
          <div className="text-[10px] text-zinc-600 italic">
            No traversal paths available. Create concept edges to enable paths.
          </div>
        )}
      </div>

      {/* Path visualization */}
      {loading && (
        <div className="px-3 py-4 text-center text-zinc-600 text-xs">
          Loading path...
        </div>
      )}

      {traversal && traversal.path.length > 1 && (
        <>
          {/* Controls */}
          <div className="px-3 py-2 border-b border-zinc-800/50 shrink-0 flex items-center gap-2">
            <button
              onClick={stepBackward}
              disabled={currentStep === 0}
              className="px-2 py-1 text-xs bg-zinc-800 rounded hover:bg-zinc-700 disabled:opacity-30 disabled:hover:bg-zinc-800 transition-colors"
            >
              &larr;
            </button>
            <div className="flex-1 text-center text-[10px] text-zinc-500">
              Step {currentStep + 1} of {traversal.path.length}
            </div>
            <button
              onClick={stepForward}
              disabled={currentStep === traversal.path.length - 1}
              className="px-2 py-1 text-xs bg-zinc-800 rounded hover:bg-zinc-700 disabled:opacity-30 disabled:hover:bg-zinc-800 transition-colors"
            >
              &rarr;
            </button>
            <button
              onClick={toggleAnimation}
              className={`px-2 py-1 text-[10px] rounded transition-colors ${
                isAnimating
                  ? "bg-amber-400/20 text-amber-400 border border-amber-400/30"
                  : "bg-zinc-800 text-zinc-400 hover:bg-zinc-700"
              }`}
            >
              {isAnimating ? "Stop" : "Play"}
            </button>
          </div>

          {/* Progress bar */}
          <div className="px-3 py-1 shrink-0">
            <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${((currentStep + 1) / traversal.path.length) * 100}%`,
                  backgroundColor:
                    RELATION_META[traversal.relation]?.color || "#71717A",
                }}
              />
            </div>
          </div>

          {/* Step list */}
          <div className="flex-1 overflow-y-auto px-3 py-2">
            <div className="relative">
              {/* Vertical line */}
              <div
                className="absolute left-[9px] top-3 bottom-3 w-px"
                style={{
                  backgroundColor:
                    (RELATION_META[traversal.relation]?.color || "#71717A") + "30",
                }}
              />

              <div className="space-y-0.5">
                {traversal.path.map((node, i) => {
                  const isCurrent = i === currentStep;
                  const isPast = i < currentStep;
                  const relColor =
                    RELATION_META[traversal.relation]?.color || "#71717A";

                  return (
                    <button
                      key={`${node.conceptId}-${i}`}
                      onClick={() => jumpToStep(i)}
                      className={`w-full text-left relative flex items-start gap-2.5 px-1 py-1.5 rounded transition-all ${
                        isCurrent
                          ? "bg-zinc-800/80"
                          : "hover:bg-zinc-900/50"
                      }`}
                    >
                      {/* Node dot */}
                      <div className="relative z-10 shrink-0 mt-0.5">
                        <div
                          className={`w-[18px] h-[18px] rounded-full flex items-center justify-center text-[8px] font-bold transition-all ${
                            isCurrent ? "ring-2 scale-110" : ""
                          }`}
                          style={{
                            backgroundColor: isCurrent
                              ? relColor + "30"
                              : isPast
                              ? domainColor(node.domain) + "25"
                              : "#27272A",
                            color: isCurrent
                              ? relColor
                              : isPast
                              ? domainColor(node.domain)
                              : "#52525B",
                            outlineColor: isCurrent ? relColor : undefined,
                          }}
                        >
                          {i + 1}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-1.5">
                          <span
                            className={`text-[11px] font-medium truncate ${
                              isCurrent
                                ? "text-zinc-100"
                                : isPast
                                ? "text-zinc-300"
                                : "text-zinc-500"
                            }`}
                          >
                            {node.name}
                          </span>
                          <span
                            className="text-[8px] px-1 py-0 rounded font-mono shrink-0"
                            style={{
                              backgroundColor: domainColor(node.domain) + "15",
                              color: domainColor(node.domain),
                            }}
                          >
                            {domainAbbrev(node.domain)}
                          </span>
                        </div>

                        {/* Edge explanation (for steps after first) */}
                        {node.explanation && (
                          <div
                            className={`text-[9px] mt-0.5 leading-relaxed ${
                              isCurrent ? "text-zinc-400" : "text-zinc-600"
                            }`}
                          >
                            {node.explanation}
                          </div>
                        )}
                      </div>

                      {/* Arrow indicator for current */}
                      {isCurrent && (
                        <div
                          className="shrink-0 mt-1 text-[10px]"
                          style={{ color: relColor }}
                        >
                          &#9654;
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Keyboard hints */}
          <div className="px-3 py-2 border-t border-zinc-800/50 shrink-0">
            <div className="text-[8px] text-zinc-700 flex items-center gap-3">
              <span>
                <kbd className="bg-zinc-800 px-1 py-0.5 rounded">←</kbd>{" "}
                <kbd className="bg-zinc-800 px-1 py-0.5 rounded">→</kbd> step
              </span>
              <span>
                <kbd className="bg-zinc-800 px-1 py-0.5 rounded">space</kbd>{" "}
                play/stop
              </span>
            </div>
          </div>
        </>
      )}

      {traversal && traversal.path.length <= 1 && activeRelation && (
        <div className="px-3 py-4 text-center text-zinc-600 text-[11px]">
          No chain found for{" "}
          <span className="text-zinc-400">
            {RELATION_META[activeRelation]?.label || activeRelation}
          </span>{" "}
          from this concept.
          <div className="mt-2 text-zinc-700">
            Create edges with this relation type to enable traversal.
          </div>
        </div>
      )}
    </div>
  );
}
