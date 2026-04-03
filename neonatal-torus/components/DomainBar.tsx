"use client";

import { ABP_DOMAINS } from "@/lib/domains";

export default function DomainBar({
  counts,
}: {
  counts?: Record<string, number>;
}) {
  return (
    <div className="w-full">
      {/* Visual bar */}
      <div className="flex rounded-lg overflow-hidden h-8 mb-3">
        {ABP_DOMAINS.map((d) => (
          <div
            key={d.id}
            className="relative group transition-all hover:opacity-90"
            style={{
              backgroundColor: d.color,
              width: `${d.exam_percent}%`,
              minWidth: d.exam_percent > 2 ? undefined : "8px",
            }}
          >
            <div className="absolute inset-0 flex items-center justify-center">
              {d.exam_percent >= 4 && (
                <span className="text-[10px] font-bold text-white/90 drop-shadow-sm">
                  {d.abbrev}
                </span>
              )}
            </div>
            <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block z-10">
              <div className="bg-zinc-800 text-zinc-100 text-xs rounded px-2 py-1 whitespace-nowrap shadow-lg border border-zinc-700">
                {d.name} — {d.exam_percent}%
                {counts && counts[d.id] !== undefined && (
                  <span className="text-zinc-400 ml-1">
                    ({counts[d.id]} chunks)
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Legend (compact) */}
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {ABP_DOMAINS.map((d) => (
          <div key={d.id} className="flex items-center gap-1 text-xs text-zinc-400">
            <div
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: d.color }}
            />
            <span className="font-mono">{d.abbrev}</span>
            <span className="text-zinc-600">{d.exam_percent}%</span>
            {counts && counts[d.id] !== undefined && (
              <span className="text-zinc-500">({counts[d.id]})</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
