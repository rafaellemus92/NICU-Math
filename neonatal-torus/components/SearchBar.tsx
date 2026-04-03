"use client";

import { useState, useEffect, useRef } from "react";
import { ABP_DOMAINS } from "@/lib/domains";

interface SearchResult {
  concepts: Array<{
    id: number;
    name: string;
    slug: string;
    primary_domain: string;
    ring1_identity: string | null;
  }>;
  chunks: Array<{
    id: number;
    preview?: string;
    text: string;
    domain_primary: string | null;
    document_title: string | null;
    page_start: number | null;
  }>;
}

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [domain, setDomain] = useState("");
  const [ring, setRing] = useState("");
  const [results, setResults] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>(undefined);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (!query.trim()) {
      setResults(null);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams({ q: query });
        if (domain) params.set("domain", domain);
        if (ring) params.set("ring", ring);
        const res = await fetch(`/api/search?${params}`);
        const data = await res.json();
        setResults(data);
        setSelectedIndex(0);
      } catch {
        // ignore
      } finally {
        setLoading(false);
      }
    }, 200);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, domain, ring]);

  const domainColor = (id: string | null) =>
    ABP_DOMAINS.find((d) => d.id === id)?.color || "#71717A";
  const domainAbbrev = (id: string | null) =>
    ABP_DOMAINS.find((d) => d.id === id)?.abbrev || "";

  const allResults = [
    ...(results?.concepts.map((c) => ({ type: "concept" as const, ...c })) || []),
    ...(results?.chunks.map((c) => ({ type: "chunk" as const, ...c })) || []),
  ];

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((i) => Math.min(i + 1, allResults.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && allResults[selectedIndex]) {
      const item = allResults[selectedIndex];
      if (item.type === "concept" && "slug" in item) {
        window.location.href = `/concept/${item.slug}`;
      }
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <div className="flex gap-2 mb-2">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search concepts and source text..."
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
        <select
          value={ring}
          onChange={(e) => setRing(e.target.value)}
          className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-3 text-zinc-300 text-sm focus:outline-none focus:border-amber-400"
        >
          <option value="">All rings</option>
          <option value="identity">Identity</option>
          <option value="taxonomy">Taxonomy</option>
          <option value="associations">Associations</option>
          <option value="distinctions">Distinctions</option>
          <option value="edge">Edge</option>
        </select>
      </div>

      {results && (query.trim().length > 0) && (
        <div className="bg-zinc-900 border border-zinc-700 rounded-lg overflow-hidden divide-y divide-zinc-800">
          {allResults.length === 0 && (
            <div className="p-4 text-zinc-500 text-sm">No results found</div>
          )}

          {results.concepts.length > 0 && (
            <div className="p-3">
              <div className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                Concepts
              </div>
              {results.concepts.map((c, i) => (
                <a
                  key={c.id}
                  href={`/concept/${c.slug}`}
                  className={`block px-3 py-2 rounded-md text-sm transition-colors ${
                    selectedIndex === i
                      ? "bg-zinc-800 text-zinc-100"
                      : "text-zinc-300 hover:bg-zinc-800/50"
                  }`}
                >
                  <span className="font-medium">{c.name}</span>
                  <span
                    className="ml-2 text-xs px-1.5 py-0.5 rounded font-mono"
                    style={{
                      backgroundColor: domainColor(c.primary_domain) + "20",
                      color: domainColor(c.primary_domain),
                    }}
                  >
                    {domainAbbrev(c.primary_domain)}
                  </span>
                  {c.ring1_identity && (
                    <span className="ml-2 text-zinc-500 text-xs truncate">
                      {c.ring1_identity.substring(0, 80)}...
                    </span>
                  )}
                </a>
              ))}
            </div>
          )}

          {results.chunks.length > 0 && (
            <div className="p-3">
              <div className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
                Source Text
              </div>
              {results.chunks.slice(0, 10).map((ch) => (
                <div
                  key={ch.id}
                  className="px-3 py-2 rounded-md text-sm text-zinc-400 hover:bg-zinc-800/50"
                >
                  <div className="flex items-center gap-2 mb-1">
                    {ch.domain_primary && (
                      <span
                        className="text-xs px-1.5 py-0.5 rounded font-mono"
                        style={{
                          backgroundColor:
                            domainColor(ch.domain_primary) + "20",
                          color: domainColor(ch.domain_primary),
                        }}
                      >
                        {domainAbbrev(ch.domain_primary)}
                      </span>
                    )}
                    {ch.document_title && (
                      <span className="text-xs text-zinc-600">
                        {ch.document_title}
                      </span>
                    )}
                    {ch.page_start && (
                      <span className="text-xs text-zinc-600">
                        p.{ch.page_start}
                      </span>
                    )}
                  </div>
                  <div className="text-zinc-400 text-xs line-clamp-2">
                    {ch.text.substring(0, 200)}...
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
