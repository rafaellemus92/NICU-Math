"use client";

import { useState } from "react";

interface OysterRingsProps {
  ring1_identity: string | null;
  ring2_taxonomy: string | null;
  ring3_associations: string | null;
  ring4_distinctions: string | null;
  ring5_edge: string | null;
}

const RINGS = [
  { key: "ring1_identity", label: "Identity", sublabel: "What is it?", color: "#3B82F6", num: 1 },
  { key: "ring2_taxonomy", label: "Taxonomy", sublabel: "Where does it live?", color: "#22C55E", num: 2 },
  { key: "ring3_associations", label: "Associations", sublabel: "What comes with it?", color: "#EAB308", num: 3 },
  { key: "ring4_distinctions", label: "Distinctions", sublabel: "What is it NOT?", color: "#EF4444", num: 4 },
  { key: "ring5_edge", label: "Edge", sublabel: "The board pearl", color: "#A855F7", num: 5 },
] as const;

export default function OysterRings(props: OysterRingsProps) {
  const [expandedRings, setExpandedRings] = useState<Set<string>>(new Set(["ring1_identity"]));

  const toggle = (key: string) => {
    setExpandedRings((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  return (
    <div className="space-y-2">
      {RINGS.map((ring) => {
        const content = props[ring.key];
        const expanded = expandedRings.has(ring.key);

        return (
          <div
            key={ring.key}
            className="border rounded-lg overflow-hidden transition-all"
            style={{ borderColor: content ? ring.color + "40" : "#27272A" }}
          >
            <button
              onClick={() => toggle(ring.key)}
              className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-zinc-900/50 transition-colors"
            >
              <span
                className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0"
                style={{
                  backgroundColor: ring.color + "20",
                  color: ring.color,
                }}
              >
                {ring.num}
              </span>
              <div className="flex-1 min-w-0">
                <span className="font-medium text-sm" style={{ color: ring.color }}>
                  {ring.label}
                </span>
                <span className="text-zinc-500 text-xs ml-2">{ring.sublabel}</span>
              </div>
              <span className="text-zinc-500 text-xs">
                {expanded ? "−" : "+"}
              </span>
            </button>

            {expanded && (
              <div className="px-4 pb-4 pl-14">
                {content ? (
                  <div className="text-sm text-zinc-300 leading-relaxed whitespace-pre-wrap">
                    {content}
                  </div>
                ) : (
                  <div className="text-sm text-zinc-600 italic">
                    No content yet
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
