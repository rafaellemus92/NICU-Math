"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { ABP_DOMAINS } from "@/lib/domains";
import Link from "next/link";

interface Snippet {
  text: string;
  highlights: [number, number][];
}

interface ExploreChunk {
  id: number;
  documentId: number;
  documentTitle: string;
  pageStart: number | null;
  pageEnd: number | null;
  domain: string | null;
  ring: string | null;
  snippets: Snippet[];
  fullText: string;
}

interface RelatedTerm {
  term: string;
  count: number;
  domains: string[];
}

interface CrossDomainLink {
  term: string;
  domains: string[];
  chunkCount: number;
}

interface ExploreConcept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  ring1_identity: string | null;
  exam_relevance: number;
}

interface ExploreResult {
  query: string;
  chunks: ExploreChunk[];
  relatedTerms: RelatedTerm[];
  domainBreakdown: { domain: string; count: number }[];
  crossDomainLinks: CrossDomainLink[];
  concepts: ExploreConcept[];
  totalChunks: number;
}

const RING_COLORS: Record<string, string> = {
  identity: "#3B82F6",
  taxonomy: "#22C55E",
  associations: "#EAB308",
  distinctions: "#EF4444",
  edge: "#A855F7",
};

function domainColor(id: string | null) {
  return ABP_DOMAINS.find((d) => d.id === id)?.color || "#71717A";
}
function domainAbbrev(id: string | null) {
  return ABP_DOMAINS.find((d) => d.id === id)?.abbrev || id || "";
}
function domainName(id: string | null) {
  return ABP_DOMAINS.find((d) => d.id === id)?.name || id || "";
}

function HighlightedText({ snippet }: { snippet: Snippet }) {
  if (snippet.highlights.length === 0) {
    return <span>{snippet.text}</span>;
  }

  const parts: React.ReactNode[] = [];
  let lastEnd = 0;

  for (const [start, end] of snippet.highlights) {
    if (start > lastEnd) {
      parts.push(
        <span key={`t-${lastEnd}`}>{snippet.text.substring(lastEnd, start)}</span>
      );
    }
    parts.push(
      <mark
        key={`h-${start}`}
        className="bg-amber-400/30 text-amber-200 rounded px-0.5"
      >
        {snippet.text.substring(start, end)}
      </mark>
    );
    lastEnd = end;
  }
  if (lastEnd < snippet.text.length) {
    parts.push(
      <span key={`t-${lastEnd}`}>{snippet.text.substring(lastEnd)}</span>
    );
  }

  return <>{parts}</>;
}

export default function ExplorePage() {
  const [query, setQuery] = useState("");
  const [domain, setDomain] = useState("");
  const [result, setResult] = useState<ExploreResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [expandedChunks, setExpandedChunks] = useState<Set<number>>(new Set());
  const debounceRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  const search = useCallback(async (q: string, d: string) => {
    if (!q.trim()) {
      setResult(null);
      return;
    }
    setLoading(true);
    try {
      const params = new URLSearchParams({ q });
      if (d) params.set("domain", d);
      const res = await fetch(`/api/explore?${params}`);
      const data = await res.json();
      setResult(data);
      setExpandedChunks(new Set());
    } catch {
      // ignore
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => search(query, domain), 300);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, domain, search]);

  const appendSearch = (term: string) => {
    setQuery((prev) => {
      const terms = prev.trim().split(/\s+/);
      if (terms.includes(term)) return prev;
      return prev.trim() + " " + term;
    });
  };

  const toggleExpand = (id: number) => {
    setExpandedChunks((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold mb-1">Explore</h1>
        <p className="text-zinc-500 text-sm">
          Deep search with related terms, cross-domain connections, and source context
        </p>
      </div>

      {/* Search bar */}
      <div className="flex gap-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., choline, surfactant, NEC..."
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-3 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-amber-400 font-mono text-sm"
            autoFocus
          />
          {loading && (
            <div className="absolute right-3 top-3.5 w-4 h-4 border-2 border-zinc-500 border-t-amber-400 rounded-full animate-spin" />
          )}
        </div>
        <select
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-3 text-zinc-300 text-sm focus:outline-none focus:border-amber-400"
        >
          <option value="">All domains</option>
          {ABP_DOMAINS.map((d) => (
            <option key={d.id} value={d.id}>
              {d.abbrev}
            </option>
          ))}
        </select>
      </div>

      {result && result.totalChunks > 0 && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main results column */}
          <div className="lg:col-span-2 space-y-4">
            {/* Related concepts */}
            {result.concepts.length > 0 && (
              <div>
                <h3 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                  Related Concepts
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.concepts.map((c: ExploreConcept) => (
                    <Link
                      key={c.id}
                      href={`/concept/${c.slug}`}
                      className="flex items-center gap-2 px-3 py-1.5 bg-zinc-900 border border-zinc-700 rounded-lg text-sm hover:border-zinc-500 transition-colors"
                    >
                      <span className="font-medium text-zinc-200">{c.name}</span>
                      <span
                        className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                        style={{
                          backgroundColor: domainColor(c.primary_domain) + "20",
                          color: domainColor(c.primary_domain),
                        }}
                      >
                        {domainAbbrev(c.primary_domain)}
                      </span>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Source chunks with highlights */}
            <div>
              <h3 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                Source Text ({result.totalChunks} chunks)
              </h3>
              <div className="space-y-2">
                {result.chunks.map((ch) => (
                  <div
                    key={ch.id}
                    className="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden"
                  >
                    {/* Chunk header */}
                    <div className="flex items-center gap-2 px-4 py-2 border-b border-zinc-800/50">
                      {ch.domain && (
                        <span
                          className="text-[10px] px-1.5 py-0.5 rounded font-mono font-bold"
                          style={{
                            backgroundColor: domainColor(ch.domain) + "20",
                            color: domainColor(ch.domain),
                          }}
                        >
                          {domainAbbrev(ch.domain)}
                        </span>
                      )}
                      {ch.ring && (
                        <span
                          className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                          style={{
                            backgroundColor: (RING_COLORS[ch.ring] || "#71717A") + "20",
                            color: RING_COLORS[ch.ring] || "#71717A",
                          }}
                        >
                          {ch.ring}
                        </span>
                      )}
                      <span className="text-[10px] text-zinc-600">
                        {ch.documentTitle}
                      </span>
                      {ch.pageStart && (
                        <span className="text-[10px] text-zinc-600">
                          p.{ch.pageStart}
                          {ch.pageEnd && ch.pageEnd !== ch.pageStart
                            ? `–${ch.pageEnd}`
                            : ""}
                        </span>
                      )}
                      <div className="flex-1" />
                      <button
                        onClick={() => toggleExpand(ch.id)}
                        className="text-[10px] text-zinc-500 hover:text-zinc-300"
                      >
                        {expandedChunks.has(ch.id) ? "collapse" : "expand"}
                      </button>
                    </div>

                    {/* Snippets with highlights */}
                    <div className="px-4 py-3">
                      {expandedChunks.has(ch.id) ? (
                        <p className="text-xs text-zinc-300 leading-relaxed whitespace-pre-wrap">
                          {ch.fullText}
                        </p>
                      ) : (
                        <div className="space-y-2">
                          {ch.snippets.map((snippet, i) => (
                            <p
                              key={i}
                              className="text-xs text-zinc-400 leading-relaxed"
                            >
                              <HighlightedText snippet={snippet} />
                            </p>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Domain breakdown */}
            <div>
              <h3 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                Domain Distribution
              </h3>
              <div className="space-y-1">
                {result.domainBreakdown.map((db) => (
                  <button
                    key={db.domain}
                    onClick={() =>
                      setDomain(domain === db.domain ? "" : db.domain)
                    }
                    className={`w-full flex items-center gap-2 px-3 py-1.5 rounded text-xs transition-colors ${
                      domain === db.domain
                        ? "bg-zinc-800 border border-zinc-600"
                        : "hover:bg-zinc-900"
                    }`}
                  >
                    <div
                      className="w-2 h-2 rounded-full shrink-0"
                      style={{ backgroundColor: domainColor(db.domain) }}
                    />
                    <span
                      className="font-mono font-bold"
                      style={{ color: domainColor(db.domain) }}
                    >
                      {domainAbbrev(db.domain)}
                    </span>
                    <span className="text-zinc-500 truncate">
                      {domainName(db.domain)}
                    </span>
                    <div className="flex-1" />
                    <span className="text-zinc-400 font-mono">{db.count}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Related terms */}
            {result.relatedTerms.length > 0 && (
              <div>
                <h3 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                  Related Terms
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {result.relatedTerms.map((rt) => (
                    <button
                      key={rt.term}
                      onClick={() => appendSearch(rt.term)}
                      className="group flex items-center gap-1 px-2 py-1 bg-zinc-900 border border-zinc-800 rounded text-[10px] hover:border-zinc-600 transition-colors"
                    >
                      <span className="text-zinc-300 group-hover:text-amber-400">
                        {rt.term}
                      </span>
                      <span className="text-zinc-600">{rt.count}</span>
                      {rt.domains.length > 1 && (
                        <div className="flex -space-x-0.5">
                          {rt.domains.slice(0, 3).map((d) => (
                            <div
                              key={d}
                              className="w-1.5 h-1.5 rounded-full"
                              style={{ backgroundColor: domainColor(d) }}
                            />
                          ))}
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Cross-domain links */}
            {result.crossDomainLinks.length > 0 && (
              <div>
                <h3 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                  Cross-Domain Connections
                </h3>
                <div className="space-y-2">
                  {result.crossDomainLinks.map((cl) => (
                    <button
                      key={cl.term}
                      onClick={() => appendSearch(cl.term)}
                      className="w-full text-left px-3 py-2 bg-zinc-900 border border-zinc-800 rounded-lg hover:border-zinc-600 transition-colors"
                    >
                      <div className="text-xs text-zinc-200 font-medium mb-1">
                        {cl.term}
                      </div>
                      <div className="flex items-center gap-1">
                        {cl.domains.map((d) => (
                          <span
                            key={d}
                            className="text-[9px] px-1 py-0.5 rounded font-mono"
                            style={{
                              backgroundColor: domainColor(d) + "20",
                              color: domainColor(d),
                            }}
                          >
                            {domainAbbrev(d)}
                          </span>
                        ))}
                        <span className="text-[9px] text-zinc-600 ml-1">
                          {cl.chunkCount} chunks
                        </span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {result && result.totalChunks === 0 && query.trim() && (
        <div className="text-center py-12 text-zinc-500 text-sm">
          No results found for &ldquo;{query}&rdquo;
        </div>
      )}
    </div>
  );
}
