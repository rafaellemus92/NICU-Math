"use client";

import { ABP_DOMAINS } from "@/lib/domains";

interface TorusMapProps {
  concepts?: Array<{
    id: number;
    name: string;
    slug: string;
    primary_domain: string;
  }>;
}

export default function TorusMap({ concepts = [] }: TorusMapProps) {
  const conceptsByDomain = new Map<string, typeof concepts>();
  for (const c of concepts) {
    const list = conceptsByDomain.get(c.primary_domain) || [];
    list.push(c);
    conceptsByDomain.set(c.primary_domain, list);
  }

  return (
    <div className="grid grid-cols-5 gap-2">
      {ABP_DOMAINS.map((d) => {
        const domainConcepts = conceptsByDomain.get(d.id) || [];
        return (
          <div
            key={d.id}
            className="rounded-lg p-3 flex flex-col items-center justify-center text-center relative overflow-hidden"
            style={{
              backgroundColor: d.color + "15",
              border: `1px solid ${d.color}30`,
              minHeight: `${Math.max(80, d.exam_percent * 12)}px`,
            }}
          >
            <span className="text-xs font-bold font-mono" style={{ color: d.color }}>
              {d.abbrev}
            </span>
            <span className="text-[10px] text-zinc-500 mt-1">
              {d.exam_percent}%
            </span>
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
  );
}
