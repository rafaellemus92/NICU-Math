"use client";

import { useState, useEffect } from "react";

interface Chunk {
  id: number;
  document_id: number;
  page_start: number | null;
  page_end: number | null;
  preview: string;
  text: string;
  domain_primary: string | null;
  ring_label: string | null;
  document_title: string;
}

interface Citation {
  id: number;
  concept_id: number;
  chunk_id: number;
  claim_text: string | null;
  ring_layer: string | null;
  chunk_text: string;
  page_start: number | null;
  document_title: string;
}

const RING_OPTIONS = [
  { value: "", label: "Any ring" },
  { value: "identity", label: "Identity" },
  { value: "taxonomy", label: "Taxonomy" },
  { value: "associations", label: "Associations" },
  { value: "distinctions", label: "Distinctions" },
  { value: "edge", label: "Edge" },
];

const RING_COLORS: Record<string, string> = {
  identity: "#3B82F6",
  taxonomy: "#22C55E",
  associations: "#EAB308",
  distinctions: "#EF4444",
  edge: "#A855F7",
};

export default function CitationLinker({ conceptId }: { conceptId: number }) {
  const [citations, setCitations] = useState<Citation[]>([]);
  const [chunks, setChunks] = useState<Chunk[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [showSearch, setShowSearch] = useState(false);
  const [claimText, setClaimText] = useState("");
  const [ringLayer, setRingLayer] = useState("");
  const [selectedChunkId, setSelectedChunkId] = useState<number | null>(null);
  const [saving, setSaving] = useState(false);

  // Load existing citations
  useEffect(() => {
    fetch(`/api/citations?conceptId=${conceptId}`)
      .then((r) => r.json())
      .then((d) => setCitations(d.citations || []))
      .catch(() => {});
  }, [conceptId]);

  // Search chunks
  useEffect(() => {
    if (!searchQuery.trim()) {
      setChunks([]);
      return;
    }
    const timeout = setTimeout(() => {
      fetch(`/api/chunks?q=${encodeURIComponent(searchQuery)}&limit=20`)
        .then((r) => r.json())
        .then((d) => setChunks(d.chunks || []))
        .catch(() => {});
    }, 300);
    return () => clearTimeout(timeout);
  }, [searchQuery]);

  const addCitation = async () => {
    if (!selectedChunkId) return;
    setSaving(true);
    try {
      const res = await fetch("/api/citations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          concept_id: conceptId,
          chunk_id: selectedChunkId,
          claim_text: claimText || null,
          ring_layer: ringLayer || null,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setCitations((prev) => [...prev, data.citation]);
        setSelectedChunkId(null);
        setClaimText("");
        setRingLayer("");
        setShowSearch(false);
        setSearchQuery("");
      }
    } catch {
      // ignore
    } finally {
      setSaving(false);
    }
  };

  const removeCitation = async (id: number) => {
    await fetch(`/api/citations?id=${id}`, { method: "DELETE" });
    setCitations((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm text-zinc-500 uppercase tracking-wider">
          Citations ({citations.length})
        </h3>
        <button
          type="button"
          onClick={() => setShowSearch(!showSearch)}
          className="text-xs px-3 py-1.5 bg-zinc-800 text-zinc-300 border border-zinc-700 rounded-lg hover:bg-zinc-700 transition-colors"
        >
          {showSearch ? "Cancel" : "+ Link source chunk"}
        </button>
      </div>

      {/* Existing citations */}
      {citations.length > 0 && (
        <div className="space-y-2">
          {citations.map((cit) => (
            <div
              key={cit.id}
              className="bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 group"
            >
              {cit.claim_text && (
                <p className="text-sm text-zinc-300 mb-2">{cit.claim_text}</p>
              )}
              <p className="text-xs text-zinc-500 line-clamp-2">
                {cit.chunk_text.substring(0, 200)}...
              </p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-[10px] text-zinc-600">{cit.document_title}</span>
                {cit.page_start && (
                  <span className="text-[10px] text-zinc-600">p.{cit.page_start}</span>
                )}
                {cit.ring_layer && (
                  <span
                    className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                    style={{
                      backgroundColor: (RING_COLORS[cit.ring_layer] || "#71717A") + "20",
                      color: RING_COLORS[cit.ring_layer] || "#71717A",
                    }}
                  >
                    {cit.ring_layer}
                  </span>
                )}
                <div className="flex-1" />
                <button
                  type="button"
                  onClick={() => removeCitation(cit.id)}
                  className="text-xs text-zinc-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Search + Link panel */}
      {showSearch && (
        <div className="bg-zinc-900/50 border border-zinc-700 rounded-lg p-4 space-y-3">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search source chunks..."
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
            autoFocus
          />

          {/* Chunk results */}
          {chunks.length > 0 && (
            <div className="max-h-60 overflow-y-auto space-y-1">
              {chunks.map((ch) => (
                <button
                  key={ch.id}
                  type="button"
                  onClick={() => setSelectedChunkId(ch.id)}
                  className={`w-full text-left px-3 py-2 rounded-md text-xs transition-colors ${
                    selectedChunkId === ch.id
                      ? "bg-amber-400/10 border border-amber-400/30"
                      : "hover:bg-zinc-800"
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-zinc-600">#{ch.id}</span>
                    <span className="text-zinc-500">{ch.document_title}</span>
                    {ch.page_start && (
                      <span className="text-zinc-600">p.{ch.page_start}</span>
                    )}
                    {ch.domain_primary && (
                      <span className="text-zinc-500 font-mono">{ch.domain_primary}</span>
                    )}
                  </div>
                  <p className="text-zinc-400 line-clamp-2">
                    {ch.preview || ch.text.substring(0, 200)}
                  </p>
                </button>
              ))}
            </div>
          )}

          {/* Citation details */}
          {selectedChunkId && (
            <div className="space-y-2 pt-2 border-t border-zinc-800">
              <input
                type="text"
                value={claimText}
                onChange={(e) => setClaimText(e.target.value)}
                placeholder="What claim does this source support? (optional)"
                className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
              />
              <div className="flex items-center gap-2">
                <select
                  value={ringLayer}
                  onChange={(e) => setRingLayer(e.target.value)}
                  className="bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-2 text-zinc-300 text-xs focus:outline-none"
                >
                  {RING_OPTIONS.map((r) => (
                    <option key={r.value} value={r.value}>
                      {r.label}
                    </option>
                  ))}
                </select>
                <button
                  type="button"
                  onClick={addCitation}
                  disabled={saving}
                  className="px-3 py-2 bg-amber-400 text-zinc-900 rounded-lg text-xs font-medium hover:bg-amber-300 disabled:opacity-50"
                >
                  {saving ? "Linking..." : "Link Citation"}
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
