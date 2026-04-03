"use client";

import { useState, useEffect, use } from "react";
import { useRouter } from "next/navigation";
import ConceptForm from "@/components/ConceptForm";
import CitationLinker from "@/components/CitationLinker";

interface ConceptRow {
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

export default function EditConceptPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  const [concept, setConcept] = useState<ConceptRow | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/concepts/${id}`)
      .then((r) => r.json())
      .then((d) => setConcept(d.concept || null))
      .catch(() => setError("Failed to load concept"))
      .finally(() => setLoading(false));
  }, [id]);

  const handleDelete = async () => {
    if (!confirm("Delete this concept? This will also remove all its citations and edges.")) {
      return;
    }
    setDeleting(true);
    try {
      const res = await fetch(`/api/concepts/${id}`, { method: "DELETE" });
      if (res.ok) {
        router.push("/concepts");
      } else {
        setError("Failed to delete");
      }
    } catch {
      setError("Failed to delete");
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return <div className="text-zinc-500 text-sm">Loading...</div>;
  }

  if (!concept) {
    return <div className="text-red-400 text-sm">Concept not found</div>;
  }

  // Parse JSON fields for the form
  let secondaryDomains: string[] = [];
  try {
    secondaryDomains = concept.secondary_domains ? JSON.parse(concept.secondary_domains) : [];
  } catch { /* ignore */ }

  let boardPearls: string[] = [];
  try {
    boardPearls = concept.board_pearls ? JSON.parse(concept.board_pearls) : [];
  } catch { /* ignore */ }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Edit: {concept.name}</h1>
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="px-3 py-1.5 text-xs text-red-400 border border-red-400/30 rounded-lg hover:bg-red-400/10 disabled:opacity-50 transition-colors"
        >
          {deleting ? "Deleting..." : "Delete Concept"}
        </button>
      </div>

      {error && (
        <div className="bg-red-400/10 border border-red-400/30 rounded-lg px-4 py-3 text-red-400 text-sm">
          {error}
        </div>
      )}

      <ConceptForm
        initial={{
          id: concept.id,
          name: concept.name,
          primary_domain: concept.primary_domain,
          secondary_domains: secondaryDomains,
          ring1_identity: concept.ring1_identity || "",
          ring2_taxonomy: concept.ring2_taxonomy || "",
          ring3_associations: concept.ring3_associations || "",
          ring4_distinctions: concept.ring4_distinctions || "",
          ring5_edge: concept.ring5_edge || "",
          timeline: concept.timeline || "",
          board_pearls: boardPearls,
          exam_relevance: concept.exam_relevance,
          source_notes: concept.source_notes || "",
        }}
        onSave={async (data) => {
          const res = await fetch(`/api/concepts/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });

          if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || "Failed to update concept");
          }

          const { concept: updated } = await res.json();
          router.push(`/concept/${updated.slug}`);
        }}
        onCancel={() => router.push(`/concept/${concept.slug}`)}
      />

      {/* Citation Linker */}
      <div className="border-t border-zinc-800 pt-6">
        <CitationLinker conceptId={concept.id} />
      </div>
    </div>
  );
}
