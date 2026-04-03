"use client";

interface Edge {
  relation_type: string;
  weight: number;
  target_name: string;
  target_slug: string;
  explanation: string | null;
}

export default function FiberView({ edges }: { edges: Edge[] }) {
  if (edges.length === 0) {
    return <div className="text-zinc-600 text-sm">No connections yet</div>;
  }

  const grouped = new Map<string, Edge[]>();
  for (const e of edges) {
    const list = grouped.get(e.relation_type) || [];
    list.push(e);
    grouped.set(e.relation_type, list);
  }

  return (
    <div className="space-y-4">
      {Array.from(grouped.entries()).map(([type, typeEdges]) => (
        <div key={type}>
          <h4 className="text-xs text-zinc-500 uppercase tracking-wider mb-2">
            {type}
          </h4>
          <div className="space-y-1">
            {typeEdges.map((e, i) => (
              <a
                key={i}
                href={`/concept/${e.target_slug}`}
                className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-zinc-800/50 transition-colors"
              >
                <span className="text-sm text-zinc-200">{e.target_name}</span>
                <div className="flex-1" />
                <div className="w-16 h-1 bg-zinc-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-zinc-500 rounded-full"
                    style={{ width: `${e.weight * 100}%` }}
                  />
                </div>
              </a>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
