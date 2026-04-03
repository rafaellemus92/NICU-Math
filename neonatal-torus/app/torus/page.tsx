import { ABP_DOMAINS } from "@/lib/domains";

export default function TorusPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-2">Torus Map</h1>
        <p className="text-zinc-500 text-sm">
          Knowledge surface visualization — coming in Phase 3
        </p>
      </div>

      {/* Placeholder: domain grid sized by exam weight */}
      <div className="grid grid-cols-5 gap-2">
        {ABP_DOMAINS.map((d) => (
          <div
            key={d.id}
            className="rounded-lg p-3 flex flex-col items-center justify-center text-center"
            style={{
              backgroundColor: d.color + "15",
              border: `1px solid ${d.color}30`,
              minHeight: `${Math.max(60, d.exam_percent * 10)}px`,
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
          </div>
        ))}
      </div>

      <div className="text-center text-zinc-600 text-sm">
        Upload source material and create concepts to populate the torus
      </div>
    </div>
  );
}
