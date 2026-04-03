import SearchBar from "@/components/SearchBar";
import DomainBar from "@/components/DomainBar";
import ConceptCard from "@/components/ConceptCard";
import Link from "next/link";
import { getDb } from "@/lib/db";

export const dynamic = "force-dynamic";

export default function Home() {
  const db = getDb();
  const recentConcepts = db
    .prepare("SELECT * FROM concepts ORDER BY updated_at DESC LIMIT 6")
    .all() as Array<{
    id: number;
    name: string;
    slug: string;
    primary_domain: string;
    ring1_identity: string | null;
    exam_relevance: number;
    board_pearls: string | null;
  }>;

  const stats = db.prepare("SELECT COUNT(*) as c FROM concepts").get() as { c: number };
  const chunkStats = db.prepare("SELECT COUNT(*) as c FROM chunks").get() as { c: number };
  const docStats = db.prepare("SELECT COUNT(*) as c FROM documents").get() as { c: number };

  return (
    <div className="space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Neonatal Torus</h1>
        <p className="text-zinc-500 text-sm">
          Search concepts, source text, and board pearls across all 20 ABP domains
        </p>
        <div className="flex justify-center gap-6 text-xs text-zinc-600 pt-1">
          <span>{stats.c} concepts</span>
          <span>{chunkStats.c} chunks</span>
          <span>{docStats.c} documents</span>
        </div>
      </div>

      <SearchBar />

      {recentConcepts.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm text-zinc-500 uppercase tracking-wider">
              Recent Concepts
            </h2>
            <Link href="/concepts" className="text-xs text-zinc-500 hover:text-zinc-300 transition-colors">
              View all
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {recentConcepts.map((c) => (
              <ConceptCard key={c.id} {...c} />
            ))}
          </div>
        </div>
      )}

      <div className="pt-4">
        <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
          ABP Exam Weight Distribution
        </h2>
        <DomainBar />
      </div>

      <div className="flex justify-center gap-4 pt-4">
        <Link
          href="/concepts/new"
          className="px-4 py-2 bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg text-sm hover:bg-amber-400/20 transition-colors"
        >
          New concept
        </Link>
        <Link
          href="/upload"
          className="px-4 py-2 bg-zinc-800 text-zinc-300 border border-zinc-700 rounded-lg text-sm hover:bg-zinc-700 transition-colors"
        >
          Upload a textbook
        </Link>
        <Link
          href="/torus"
          className="px-4 py-2 bg-zinc-800 text-zinc-300 border border-zinc-700 rounded-lg text-sm hover:bg-zinc-700 transition-colors"
        >
          View torus map
        </Link>
      </div>
    </div>
  );
}
