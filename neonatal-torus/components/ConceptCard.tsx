"use client";

import Link from "next/link";
import { ABP_DOMAINS } from "@/lib/domains";

interface ConceptCardProps {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  ring1_identity: string | null;
  exam_relevance: number;
  board_pearls: string | null;
}

export default function ConceptCard(props: ConceptCardProps) {
  const domain = ABP_DOMAINS.find((d) => d.id === props.primary_domain);

  let pearls: string[] = [];
  if (props.board_pearls) {
    try {
      pearls = JSON.parse(props.board_pearls);
    } catch {
      // ignore
    }
  }

  return (
    <Link
      href={`/concept/${props.slug}`}
      className="block bg-zinc-900 border border-zinc-800 rounded-lg p-4 hover:border-zinc-600 transition-colors"
    >
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-bold text-zinc-100">{props.name}</h3>
        {domain && (
          <span
            className="text-xs px-2 py-0.5 rounded font-mono shrink-0 ml-2"
            style={{
              backgroundColor: domain.color + "20",
              color: domain.color,
            }}
          >
            {domain.abbrev}
          </span>
        )}
      </div>

      {props.ring1_identity && (
        <p className="text-sm text-zinc-400 line-clamp-2 mb-2">
          {props.ring1_identity}
        </p>
      )}

      {pearls.length > 0 && (
        <div className="text-xs text-amber-400/80 line-clamp-1">
          {pearls[0]}
        </div>
      )}

      <div className="mt-2 flex items-center gap-2">
        <div className="h-1 flex-1 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-amber-400 rounded-full"
            style={{ width: `${props.exam_relevance * 100}%` }}
          />
        </div>
        <span className="text-[10px] text-zinc-500">
          {Math.round(props.exam_relevance * 100)}%
        </span>
      </div>
    </Link>
  );
}
