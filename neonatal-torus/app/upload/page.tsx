"use client";

import { useState } from "react";
import UploadZone from "@/components/UploadZone";
import DomainBar from "@/components/DomainBar";
import Link from "next/link";

interface ChunkPreview {
  id: number;
  page_start: number | null;
  page_end: number | null;
  preview: string;
  domain_primary: string | null;
  ring_label: string | null;
}

interface IngestData {
  document: { id: number; title: string; filename: string; page_count: number | null };
  chunks: ChunkPreview[];
  domainCounts: { domain_primary: string; count: number }[];
  suggestions: string[];
}

const RING_COLORS: Record<string, string> = {
  identity: "#3B82F6",
  taxonomy: "#22C55E",
  associations: "#EAB308",
  distinctions: "#EF4444",
  edge: "#A855F7",
};

export default function UploadPage() {
  const [ingestData, setIngestData] = useState<IngestData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUploadComplete = async (result: { documentId: number }) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/ingest?documentId=${result.documentId}`);
      const data = await res.json();
      setIngestData(data);
    } catch (err) {
      console.error("Failed to load ingest data:", err);
    } finally {
      setLoading(false);
    }
  };

  const domainCounts = ingestData
    ? Object.fromEntries(ingestData.domainCounts.map((d) => [d.domain_primary, d.count]))
    : undefined;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-2">Upload Source Material</h1>
        <p className="text-zinc-500 text-sm">
          Upload PDF or DOCX textbooks. Text will be extracted, split into chunks,
          and auto-tagged by ABP domain and Oyster Ring layer.
        </p>
      </div>

      <UploadZone onUploadComplete={handleUploadComplete} />

      {loading && (
        <div className="text-center text-zinc-400 text-sm">
          Loading extraction results...
        </div>
      )}

      {ingestData && (
        <div className="space-y-6">
          {/* Document summary */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-4">
            <h2 className="text-lg font-bold mb-2">{ingestData.document.title}</h2>
            <div className="flex gap-4 text-sm text-zinc-400">
              <span>{ingestData.document.filename}</span>
              {ingestData.document.page_count && (
                <span>{ingestData.document.page_count} pages</span>
              )}
              <span>{ingestData.chunks.length} chunks extracted</span>
            </div>
          </div>

          {/* Domain distribution */}
          <div>
            <h3 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
              Domain Distribution
            </h3>
            <DomainBar counts={domainCounts} />
          </div>

          {/* Concept suggestions */}
          {ingestData.suggestions.length > 0 && (
            <div>
              <h3 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
                Suggested Concepts ({ingestData.suggestions.length})
              </h3>
              <div className="flex flex-wrap gap-2">
                {ingestData.suggestions.slice(0, 50).map((s, i) => (
                  <span
                    key={i}
                    className="px-2 py-1 bg-zinc-800 border border-zinc-700 rounded text-xs text-zinc-300"
                  >
                    {s}
                  </span>
                ))}
                {ingestData.suggestions.length > 50 && (
                  <span className="px-2 py-1 text-xs text-zinc-500">
                    +{ingestData.suggestions.length - 50} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Chunk list */}
          <div>
            <h3 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
              Extracted Chunks
            </h3>
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {ingestData.chunks.map((chunk) => (
                <div
                  key={chunk.id}
                  className="bg-zinc-900 border border-zinc-800 rounded-lg p-3 text-sm"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-zinc-600 text-xs">#{chunk.id}</span>
                    {chunk.page_start && (
                      <span className="text-zinc-500 text-xs">
                        p.{chunk.page_start}
                        {chunk.page_end && chunk.page_end !== chunk.page_start
                          ? `-${chunk.page_end}`
                          : ""}
                      </span>
                    )}
                    {chunk.domain_primary && (
                      <span className="text-xs px-1.5 py-0.5 rounded font-mono bg-zinc-800 text-zinc-300">
                        {chunk.domain_primary}
                      </span>
                    )}
                    {chunk.ring_label && (
                      <span
                        className="text-xs px-1.5 py-0.5 rounded font-mono"
                        style={{
                          backgroundColor: (RING_COLORS[chunk.ring_label] || "#71717A") + "20",
                          color: RING_COLORS[chunk.ring_label] || "#71717A",
                        }}
                      >
                        {chunk.ring_label}
                      </span>
                    )}
                  </div>
                  <p className="text-zinc-400 text-xs leading-relaxed">
                    {chunk.preview}...
                  </p>
                </div>
              ))}
            </div>
          </div>

          <div className="flex gap-4">
            <Link
              href="/"
              className="px-4 py-2 bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg text-sm hover:bg-amber-400/20 transition-colors"
            >
              Search extracted text
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
