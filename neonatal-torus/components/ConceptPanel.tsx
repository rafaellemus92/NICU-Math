"use client";

import { useState, useEffect } from "react";
import { ABP_DOMAINS } from "@/lib/domains";
import Link from "next/link";
import type { TorusConcept } from "./ConceptTorus";

interface Citation {
  id: number;
  claim_text: string | null;
  ring_layer: string | null;
  chunk_text: string;
  page_start: number | null;
  document_title: string;
}

interface ConnectedConcept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  relation_type: string;
  weight: number;
  explanation: string | null;
}

const RINGS = [
  { key: "ring1_identity" as const, label: "Identity", sub: "What is it?", color: "#3B82F6" },
  { key: "ring2_taxonomy" as const, label: "Taxonomy", sub: "Where does it live?", color: "#22C55E" },
  { key: "ring3_associations" as const, label: "Associations", sub: "What comes with it?", color: "#EAB308" },
  { key: "ring4_distinctions" as const, label: "Distinctions", sub: "What is it NOT?", color: "#EF4444" },
  { key: "ring5_edge" as const, label: "Edge", sub: "The board pearl", color: "#A855F7" },
];

const FIBER_STYLE_LABELS: Record<string, string> = {
  association: "solid line",
  distinction: "dotted",
  treatment: "double",
  mechanism: "solid",
  genetic: "dashed",
  temporal: "arc",
};

function domainColor(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.color || "#71717A";
}
function domainAbbrev(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.abbrev || id;
}
function domainName(id: string) {
  return ABP_DOMAINS.find((d) => d.id === id)?.name || id;
}

export default function ConceptPanel({
  concept,
  onClose,
  onConceptNavigate,
}: {
  concept: TorusConcept;
  onClose: () => void;
  onConceptNavigate: (conceptId: number) => void;
}) {
  const [expandedRing, setExpandedRing] = useState<string | null>("ring1_identity");
  const [connections, setConnections] = useState<ConnectedConcept[]>([]);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [showCitations, setShowCitations] = useState(false);

  // Fetch connections and citations
  useEffect(() => {
    fetch(`/api/concepts/${concept.id}/graph`)
      .then((r) => r.json())
      .then((d) => {
        setConnections(d.connections || []);
        setCitations(d.citations || []);
      })
      .catch(() => {});
  }, [concept.id]);

  // Parse JSON fields
  let secondaryDomains: string[] = [];
  try {
    secondaryDomains = concept.secondary_domains
      ? JSON.parse(concept.secondary_domains)
      : [];
  } catch { /* ignore */ }

  let pearls: string[] = [];
  try {
    pearls = concept.board_pearls ? JSON.parse(concept.board_pearls) : [];
  } catch { /* ignore */ }

  // Cross-domain reach
  const allDomains = new Set([concept.primary_domain, ...secondaryDomains]);
  for (const conn of connections) {
    allDomains.add(conn.primary_domain);
  }

  return (
    <div className="h-full flex flex-col bg-zinc-950 border-l border-zinc-800 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-zinc-800 shrink-0">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <h2 className="text-base font-bold text-zinc-100 leading-tight">
              {concept.name}
            </h2>
            <div className="flex items-center gap-1.5 mt-1 flex-wrap">
              <span
                className="text-[10px] px-1.5 py-0.5 rounded font-mono font-bold"
                style={{
                  backgroundColor: domainColor(concept.primary_domain) + "25",
                  color: domainColor(concept.primary_domain),
                }}
              >
                {domainAbbrev(concept.primary_domain)}
              </span>
              {secondaryDomains.map((d) => (
                <span
                  key={d}
                  className="text-[9px] px-1 py-0.5 rounded font-mono"
                  style={{
                    backgroundColor: domainColor(d) + "15",
                    color: domainColor(d),
                  }}
                >
                  {domainAbbrev(d)}
                </span>
              ))}
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-zinc-300 text-sm shrink-0 p-1"
          >
            x
          </button>
        </div>

        {/* Stats row */}
        <div className="flex items-center gap-3 mt-2 text-[10px] text-zinc-500">
          <div>
            <span className="text-zinc-400 font-bold">
              {Math.round(concept.exam_relevance * 100)}%
            </span>{" "}
            board density
          </div>
          <div>
            <span className="text-zinc-400 font-bold">{allDomains.size}</span>{" "}
            domain reach
          </div>
          <div>
            <span className="text-zinc-400 font-bold">{connections.length}</span>{" "}
            connections
          </div>
        </div>

        {/* Relevance bar */}
        <div className="mt-2 h-1 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full"
            style={{
              width: `${concept.exam_relevance * 100}%`,
              backgroundColor: domainColor(concept.primary_domain),
            }}
          />
        </div>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto">
        {/* Timeline */}
        {concept.timeline && (
          <div className="px-4 py-2 border-b border-zinc-800/50">
            <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-1">
              Timeline
            </div>
            <div className="text-[11px] text-zinc-400">{concept.timeline}</div>
          </div>
        )}

        {/* Oyster Rings */}
        <div className="px-4 py-3 border-b border-zinc-800/50">
          <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-2">
            Oyster Rings
          </div>
          <div className="space-y-1">
            {RINGS.map((ring) => {
              const content = concept[ring.key] as string | null | undefined;
              const isExpanded = expandedRing === ring.key;

              return (
                <div key={ring.key}>
                  <button
                    onClick={() =>
                      setExpandedRing(isExpanded ? null : ring.key)
                    }
                    className="w-full flex items-center gap-2 px-2 py-1.5 rounded text-left hover:bg-zinc-900/50 transition-colors"
                  >
                    <span
                      className="w-4 h-4 rounded-full flex items-center justify-center text-[8px] font-bold shrink-0"
                      style={{
                        backgroundColor: ring.color + "20",
                        color: ring.color,
                      }}
                    >
                      {ring.key.charAt(4)}
                    </span>
                    <span
                      className="text-[11px] font-medium flex-1"
                      style={{ color: content ? ring.color : "#52525B" }}
                    >
                      {ring.label}
                    </span>
                    <span className="text-[9px] text-zinc-600">
                      {isExpanded ? "−" : "+"}
                    </span>
                  </button>
                  {isExpanded && content && (
                    <div className="px-2 pb-2 pl-8">
                      <div className="text-[11px] text-zinc-300 leading-relaxed whitespace-pre-wrap">
                        {content}
                      </div>
                    </div>
                  )}
                  {isExpanded && !content && (
                    <div className="px-2 pb-2 pl-8 text-[11px] text-zinc-700 italic">
                      Not yet filled
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Board Pearls */}
        {pearls.length > 0 && (
          <div className="px-4 py-3 border-b border-zinc-800/50">
            <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-2">
              Board Pearls
            </div>
            <div className="space-y-1.5">
              {pearls.map((pearl, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 bg-amber-400/5 border border-amber-400/15 rounded px-2 py-1.5"
                >
                  <span className="text-amber-400 text-[10px] mt-0.5">*</span>
                  <span className="text-amber-200/90 text-[11px] leading-relaxed">
                    {pearl}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Connected Concepts */}
        {connections.length > 0 && (
          <div className="px-4 py-3 border-b border-zinc-800/50">
            <div className="text-[9px] text-zinc-600 uppercase tracking-wider mb-2">
              Connected Concepts ({connections.length})
            </div>
            <div className="space-y-1">
              {connections
                .sort((a, b) => b.weight - a.weight)
                .map((conn) => (
                  <button
                    key={`${conn.id}-${conn.relation_type}`}
                    onClick={() => onConceptNavigate(conn.id)}
                    className="w-full flex items-center gap-2 px-2 py-1.5 rounded text-left hover:bg-zinc-900/50 transition-colors group"
                  >
                    <div
                      className="w-1.5 h-1.5 rounded-full shrink-0"
                      style={{ backgroundColor: domainColor(conn.primary_domain) }}
                    />
                    <span className="text-[11px] text-zinc-300 group-hover:text-zinc-100 flex-1 truncate">
                      {conn.name}
                    </span>
                    <span className="text-[9px] text-zinc-600 font-mono">
                      {conn.relation_type}
                    </span>
                    {/* Weight bar */}
                    <div className="w-8 h-1 bg-zinc-800 rounded-full overflow-hidden shrink-0">
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${conn.weight * 100}%`,
                          backgroundColor: domainColor(conn.primary_domain),
                        }}
                      />
                    </div>
                  </button>
                ))}
            </div>
          </div>
        )}

        {/* Citations */}
        <div className="px-4 py-3">
          <button
            onClick={() => setShowCitations(!showCitations)}
            className="text-[9px] text-zinc-600 uppercase tracking-wider mb-2 hover:text-zinc-400 flex items-center gap-1"
          >
            Source Citations ({citations.length})
            <span>{showCitations ? "−" : "+"}</span>
          </button>
          {showCitations && citations.length > 0 && (
            <div className="space-y-2">
              {citations.map((cit) => (
                <div
                  key={cit.id}
                  className="bg-zinc-900/50 border border-zinc-800/50 rounded px-2 py-2"
                >
                  {cit.claim_text && (
                    <p className="text-[11px] text-zinc-300 mb-1">
                      {cit.claim_text}
                    </p>
                  )}
                  <p className="text-[10px] text-zinc-500 line-clamp-3">
                    {cit.chunk_text.substring(0, 200)}...
                  </p>
                  <div className="flex gap-2 mt-1 text-[9px] text-zinc-600">
                    <span>{cit.document_title}</span>
                    {cit.page_start && <span>p.{cit.page_start}</span>}
                    {cit.ring_layer && (
                      <span className="text-zinc-500">{cit.ring_layer}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
          {showCitations && citations.length === 0 && (
            <div className="text-[11px] text-zinc-700 italic">
              No citations linked yet
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="px-4 py-3 border-t border-zinc-800/50">
          <div className="flex gap-2">
            <Link
              href={`/concept/${concept.slug}`}
              className="px-3 py-1.5 text-[10px] bg-zinc-800 text-zinc-300 border border-zinc-700 rounded hover:bg-zinc-700 transition-colors"
            >
              Full page
            </Link>
            <Link
              href={`/concepts/${concept.id}/edit`}
              className="px-3 py-1.5 text-[10px] bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded hover:bg-amber-400/20 transition-colors"
            >
              Edit
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
