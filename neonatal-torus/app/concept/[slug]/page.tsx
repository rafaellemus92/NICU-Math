import { getDb } from "@/lib/db";
import { ABP_DOMAINS } from "@/lib/domains";
import OysterRings from "@/components/OysterRings";
import Link from "next/link";
import { notFound } from "next/navigation";

interface Concept {
  id: number;
  name: string;
  slug: string;
  primary_domain: string;
  secondary_domains: string | null;
  ring1_identity: string | null;
  ring2_taxonomy: string | null;
  ring3_associations: string | null;
  ring4_distinctions: string | null;
  ring5_edge: string | null;
  timeline: string | null;
  board_pearls: string | null;
  exam_relevance: number;
  source_notes: string | null;
}

interface Citation {
  id: number;
  claim_text: string | null;
  ring_layer: string | null;
  chunk_text: string;
  page_start: number | null;
  document_title: string;
}

export default async function ConceptPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const db = getDb();

  const concept = db
    .prepare("SELECT * FROM concepts WHERE slug = ?")
    .get(slug) as Concept | undefined;

  if (!concept) notFound();

  const domain = ABP_DOMAINS.find((d) => d.id === concept.primary_domain);

  let secondaryDomains: string[] = [];
  if (concept.secondary_domains) {
    try {
      secondaryDomains = JSON.parse(concept.secondary_domains);
    } catch { /* ignore */ }
  }

  let pearls: string[] = [];
  if (concept.board_pearls) {
    try {
      pearls = JSON.parse(concept.board_pearls);
    } catch { /* ignore */ }
  }

  const citations = db
    .prepare(`
      SELECT ci.id, ci.claim_text, ci.ring_layer,
             ch.text as chunk_text, ch.page_start,
             d.title as document_title
      FROM citations ci
      JOIN chunks ch ON ch.id = ci.chunk_id
      JOIN documents d ON d.id = ch.document_id
      WHERE ci.concept_id = ?
      ORDER BY ci.id
    `)
    .all(concept.id) as Citation[];

  const edges = db
    .prepare(`
      SELECT ce.*, c2.name as target_name, c2.slug as target_slug
      FROM concept_edges ce
      JOIN concepts c2 ON c2.id = ce.target_id
      WHERE ce.source_id = ?
      UNION
      SELECT ce.*, c2.name as target_name, c2.slug as target_slug
      FROM concept_edges ce
      JOIN concepts c2 ON c2.id = ce.source_id
      WHERE ce.target_id = ?
    `)
    .all(concept.id, concept.id) as Array<{
    relation_type: string;
    weight: number;
    target_name: string;
    target_slug: string;
    explanation: string | null;
  }>;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="text-2xl font-bold">{concept.name}</h1>
          {domain && (
            <span
              className="text-xs px-2 py-1 rounded font-mono"
              style={{
                backgroundColor: domain.color + "20",
                color: domain.color,
              }}
            >
              {domain.abbrev}
            </span>
          )}
          {secondaryDomains.map((d) => {
            const sd = ABP_DOMAINS.find((x) => x.id === d);
            return sd ? (
              <span
                key={d}
                className="text-[10px] px-1.5 py-0.5 rounded font-mono"
                style={{
                  backgroundColor: sd.color + "15",
                  color: sd.color,
                }}
              >
                {sd.abbrev}
              </span>
            ) : null;
          })}
          <div className="flex-1" />
          <Link
            href={`/concepts/${concept.id}/edit`}
            className="px-3 py-1.5 text-xs text-zinc-400 border border-zinc-700 rounded-lg hover:bg-zinc-800 transition-colors"
          >
            Edit
          </Link>
        </div>
        <div className="flex items-center gap-4 text-sm text-zinc-500">
          <span>Exam relevance: {Math.round(concept.exam_relevance * 100)}%</span>
          {concept.source_notes && <span>{concept.source_notes}</span>}
        </div>
      </div>

      {/* Oyster Rings */}
      <div>
        <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
          Oyster Rings
        </h2>
        <OysterRings
          ring1_identity={concept.ring1_identity}
          ring2_taxonomy={concept.ring2_taxonomy}
          ring3_associations={concept.ring3_associations}
          ring4_distinctions={concept.ring4_distinctions}
          ring5_edge={concept.ring5_edge}
        />
      </div>

      {/* Board Pearls */}
      {pearls.length > 0 && (
        <div>
          <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
            Board Pearls
          </h2>
          <div className="space-y-2">
            {pearls.map((pearl, i) => (
              <div
                key={i}
                className="flex items-start gap-3 bg-amber-400/5 border border-amber-400/20 rounded-lg px-4 py-3"
              >
                <span className="text-amber-400 text-sm shrink-0 mt-0.5">*</span>
                <span className="text-amber-200 text-sm">{pearl}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Torus Fibers (connections) */}
      {edges.length > 0 && (
        <div>
          <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
            Torus Fibers
          </h2>
          <div className="grid gap-2">
            {edges.map((edge, i) => (
              <Link
                key={i}
                href={`/concept/${edge.target_slug}`}
                className="flex items-center gap-3 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 hover:border-zinc-600 transition-colors"
              >
                <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">
                  {edge.relation_type}
                </span>
                <span className="text-sm text-zinc-200 font-medium">
                  {edge.target_name}
                </span>
                <div className="flex-1" />
                <div className="w-20 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-zinc-500 rounded-full"
                    style={{ width: `${edge.weight * 100}%` }}
                  />
                </div>
                {edge.explanation && (
                  <span className="text-xs text-zinc-500 max-w-[200px] truncate">
                    {edge.explanation}
                  </span>
                )}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Citations */}
      {citations.length > 0 && (
        <div>
          <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
            Citations
          </h2>
          <div className="space-y-2">
            {citations.map((cit) => (
              <div
                key={cit.id}
                className="bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3"
              >
                {cit.claim_text && (
                  <p className="text-sm text-zinc-300 mb-2">{cit.claim_text}</p>
                )}
                <p className="text-xs text-zinc-500 line-clamp-3">
                  {cit.chunk_text}
                </p>
                <div className="flex gap-2 mt-2 text-[10px] text-zinc-600">
                  <span>{cit.document_title}</span>
                  {cit.page_start && <span>p.{cit.page_start}</span>}
                  {cit.ring_layer && <span>{cit.ring_layer}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
