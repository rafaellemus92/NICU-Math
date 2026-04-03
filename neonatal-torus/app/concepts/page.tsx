"use client";

import { useState, useEffect } from "react";
import { ABP_DOMAINS } from "@/lib/domains";
import ConceptCard from "@/components/ConceptCard";
import Link from "next/link";

interface Concept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  ring1_identity: string | null;
  exam_relevance: number;
  board_pearls: string | null;
}

export default function ConceptsPage() {
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [total, setTotal] = useState(0);
  const [domain, setDomain] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams();
    if (domain) params.set("domain", domain);
    params.set("limit", "200");

    fetch(`/api/concepts?${params}`)
      .then((r) => r.json())
      .then((d) => {
        setConcepts(d.concepts || []);
        setTotal(d.total || 0);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [domain]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Concepts</h1>
          <p className="text-zinc-500 text-sm">{total} total</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-300 text-sm focus:outline-none focus:border-amber-400"
          >
            <option value="">All domains</option>
            {ABP_DOMAINS.map((d) => (
              <option key={d.id} value={d.id}>
                {d.abbrev} — {d.name}
              </option>
            ))}
          </select>
          <Link
            href="/concepts/new"
            className="px-4 py-2 bg-amber-400 text-zinc-900 rounded-lg text-sm font-medium hover:bg-amber-300 transition-colors"
          >
            + New Concept
          </Link>
        </div>
      </div>

      {loading ? (
        <div className="text-zinc-500 text-sm">Loading...</div>
      ) : concepts.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-zinc-500 mb-4">No concepts yet</p>
          <Link
            href="/concepts/new"
            className="px-4 py-2 bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg text-sm hover:bg-amber-400/20 transition-colors"
          >
            Create your first concept
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {concepts.map((c) => (
            <ConceptCard key={c.id} {...c} />
          ))}
        </div>
      )}
    </div>
  );
}
