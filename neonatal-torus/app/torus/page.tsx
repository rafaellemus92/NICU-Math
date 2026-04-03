"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import dynamic from "next/dynamic";
import { ABP_DOMAINS } from "@/lib/domains";

// Dynamic import for Three.js (needs client-side only)
const Torus3D = dynamic(() => import("@/components/Torus3D"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] bg-zinc-950 rounded-xl border border-zinc-800 flex items-center justify-center">
      <div className="text-zinc-500 text-sm">Loading 3D visualization...</div>
    </div>
  ),
});

interface Concept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  exam_relevance: number;
  ring1_identity: string | null;
}

export default function TorusPage() {
  const router = useRouter();
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [chunkDensity, setChunkDensity] = useState<
    { domain: string; count: number }[]
  >([]);
  const [view, setView] = useState<"3d" | "grid">("3d");

  useEffect(() => {
    // Fetch concepts
    fetch("/api/concepts?limit=500")
      .then((r) => r.json())
      .then((d) => setConcepts(d.concepts || []))
      .catch(() => {});

    // Fetch chunk density per domain
    fetch("/api/density")
      .then((r) => r.json())
      .then((d) => setChunkDensity(d.density || []))
      .catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Torus Map</h1>
          <p className="text-zinc-500 text-sm">
            Knowledge surface — domains on the ring, depth from identity to edge
          </p>
        </div>
        <div className="flex gap-1 bg-zinc-900 border border-zinc-700 rounded-lg p-0.5">
          <button
            onClick={() => setView("3d")}
            className={`px-3 py-1.5 text-xs rounded-md transition-colors ${
              view === "3d"
                ? "bg-zinc-700 text-zinc-100"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            3D Torus
          </button>
          <button
            onClick={() => setView("grid")}
            className={`px-3 py-1.5 text-xs rounded-md transition-colors ${
              view === "grid"
                ? "bg-zinc-700 text-zinc-100"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            Domain Grid
          </button>
        </div>
      </div>

      {view === "3d" ? (
        <Torus3D
          concepts={concepts}
          chunkDensity={chunkDensity}
          onConceptClick={(slug) => router.push(`/concept/${slug}`)}
        />
      ) : (
        /* Flat grid fallback */
        <div className="grid grid-cols-5 gap-2">
          {ABP_DOMAINS.map((d) => {
            const density = chunkDensity.find((cd) => cd.domain === d.id);
            const domainConcepts = concepts.filter(
              (c) => c.primary_domain === d.id
            );

            return (
              <div
                key={d.id}
                className="rounded-lg p-3 flex flex-col items-center justify-center text-center"
                style={{
                  backgroundColor: d.color + "15",
                  border: `1px solid ${d.color}30`,
                  minHeight: `${Math.max(80, d.exam_percent * 10)}px`,
                }}
              >
                <span
                  className="text-xs font-bold font-mono"
                  style={{ color: d.color }}
                >
                  {d.abbrev}
                </span>
                <span className="text-[10px] text-zinc-500 mt-1">
                  {d.exam_percent}%
                </span>
                {density && (
                  <span className="text-[9px] text-zinc-600">
                    {density.count} chunks
                  </span>
                )}
                {domainConcepts.length > 0 && (
                  <div className="flex flex-wrap gap-0.5 mt-2 justify-center">
                    {domainConcepts.map((c) => (
                      <a
                        key={c.id}
                        href={`/concept/${c.slug}`}
                        className="w-2 h-2 rounded-full hover:scale-150 transition-transform"
                        style={{ backgroundColor: d.color }}
                        title={c.name}
                      />
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      <div className="text-center text-zinc-600 text-xs">
        {concepts.length} concepts | {chunkDensity.reduce((s, d) => s + d.count, 0)} chunks across {chunkDensity.length} domains
      </div>
    </div>
  );
}
