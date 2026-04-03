"use client";

import { useState } from "react";
import { ABP_DOMAINS } from "@/lib/domains";

interface ConceptData {
  id?: number;
  name: string;
  primary_domain: string;
  secondary_domains: string[];
  ring1_identity: string;
  ring2_taxonomy: string;
  ring3_associations: string;
  ring4_distinctions: string;
  ring5_edge: string;
  timeline: string;
  board_pearls: string[];
  exam_relevance: number;
  source_notes: string;
}

const RING_META = [
  { key: "ring1_identity", label: "Identity", sublabel: "What is it?", color: "#3B82F6", placeholder: "Define this concept — what it is, its core mechanism or feature..." },
  { key: "ring2_taxonomy", label: "Taxonomy", sublabel: "Where does it live?", color: "#22C55E", placeholder: "Classification, types, stages, grading systems..." },
  { key: "ring3_associations", label: "Associations", sublabel: "What comes with it?", color: "#EAB308", placeholder: "Complications, comorbidities, risk factors, associated findings..." },
  { key: "ring4_distinctions", label: "Distinctions", sublabel: "What is it NOT?", color: "#EF4444", placeholder: "Differential diagnosis, key distinguishing features, what to rule out..." },
  { key: "ring5_edge", label: "Edge", sublabel: "The board pearl", color: "#A855F7", placeholder: "High-yield facts, rare exceptions, pathognomonic findings, board pearls..." },
] as const;

const EMPTY_CONCEPT: ConceptData = {
  name: "",
  primary_domain: "resp",
  secondary_domains: [],
  ring1_identity: "",
  ring2_taxonomy: "",
  ring3_associations: "",
  ring4_distinctions: "",
  ring5_edge: "",
  timeline: "",
  board_pearls: [],
  exam_relevance: 0.5,
  source_notes: "",
};

export default function ConceptForm({
  initial,
  onSave,
  onCancel,
}: {
  initial?: Partial<ConceptData>;
  onSave: (data: ConceptData) => Promise<void>;
  onCancel?: () => void;
}) {
  const [data, setData] = useState<ConceptData>(() => {
    if (!initial) return { ...EMPTY_CONCEPT };
    return {
      ...EMPTY_CONCEPT,
      ...initial,
      secondary_domains: initial.secondary_domains || [],
      board_pearls: initial.board_pearls || [],
    };
  });
  const [newPearl, setNewPearl] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEdit = !!initial?.id;

  const update = <K extends keyof ConceptData>(key: K, value: ConceptData[K]) => {
    setData((prev) => ({ ...prev, [key]: value }));
  };

  const addPearl = () => {
    if (!newPearl.trim()) return;
    update("board_pearls", [...data.board_pearls, newPearl.trim()]);
    setNewPearl("");
  };

  const removePearl = (i: number) => {
    update("board_pearls", data.board_pearls.filter((_, idx) => idx !== i));
  };

  const toggleSecondaryDomain = (id: string) => {
    if (data.secondary_domains.includes(id)) {
      update("secondary_domains", data.secondary_domains.filter((d) => d !== id));
    } else {
      update("secondary_domains", [...data.secondary_domains, id]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!data.name.trim()) {
      setError("Name is required");
      return;
    }
    setSaving(true);
    setError(null);
    try {
      await onSave(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-400/10 border border-red-400/30 rounded-lg px-4 py-3 text-red-400 text-sm">
          {error}
        </div>
      )}

      {/* Name + Domain */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1">
            Concept Name
          </label>
          <input
            type="text"
            value={data.name}
            onChange={(e) => update("name", e.target.value)}
            placeholder="e.g., Respiratory Distress Syndrome"
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
            autoFocus
          />
        </div>
        <div>
          <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1">
            Primary Domain
          </label>
          <select
            value={data.primary_domain}
            onChange={(e) => update("primary_domain", e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
          >
            {ABP_DOMAINS.map((d) => (
              <option key={d.id} value={d.id}>
                {d.abbrev} — {d.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Secondary Domains */}
      <div>
        <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-2">
          Secondary Domains
        </label>
        <div className="flex flex-wrap gap-1.5">
          {ABP_DOMAINS.filter((d) => d.id !== data.primary_domain).map((d) => {
            const active = data.secondary_domains.includes(d.id);
            return (
              <button
                key={d.id}
                type="button"
                onClick={() => toggleSecondaryDomain(d.id)}
                className="text-xs px-2 py-1 rounded font-mono transition-colors"
                style={{
                  backgroundColor: active ? d.color + "30" : "transparent",
                  color: active ? d.color : "#71717A",
                  border: `1px solid ${active ? d.color + "50" : "#3f3f46"}`,
                }}
              >
                {d.abbrev}
              </button>
            );
          })}
        </div>
      </div>

      {/* Oyster Rings */}
      <div className="space-y-4">
        <h3 className="text-sm text-zinc-500 uppercase tracking-wider">Oyster Rings</h3>
        {RING_META.map((ring) => (
          <div key={ring.key}>
            <label className="flex items-center gap-2 mb-1">
              <span
                className="w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
                style={{ backgroundColor: ring.color + "20", color: ring.color }}
              >
                {ring.key.charAt(4)}
              </span>
              <span className="text-sm font-medium" style={{ color: ring.color }}>
                {ring.label}
              </span>
              <span className="text-xs text-zinc-500">{ring.sublabel}</span>
            </label>
            <textarea
              value={data[ring.key]}
              onChange={(e) => update(ring.key, e.target.value)}
              placeholder={ring.placeholder}
              rows={3}
              className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-200 text-sm focus:outline-none resize-y"
              style={{ borderColor: data[ring.key] ? ring.color + "40" : undefined }}
            />
          </div>
        ))}
      </div>

      {/* Board Pearls */}
      <div>
        <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-2">
          Board Pearls
        </label>
        {data.board_pearls.length > 0 && (
          <div className="space-y-1.5 mb-3">
            {data.board_pearls.map((pearl, i) => (
              <div
                key={i}
                className="flex items-start gap-2 bg-amber-400/5 border border-amber-400/20 rounded-lg px-3 py-2"
              >
                <span className="text-amber-400 text-xs mt-0.5">*</span>
                <span className="text-amber-200 text-sm flex-1">{pearl}</span>
                <button
                  type="button"
                  onClick={() => removePearl(i)}
                  className="text-zinc-500 hover:text-red-400 text-xs"
                >
                  x
                </button>
              </div>
            ))}
          </div>
        )}
        <div className="flex gap-2">
          <input
            type="text"
            value={newPearl}
            onChange={(e) => setNewPearl(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                addPearl();
              }
            }}
            placeholder="Add a board pearl..."
            className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-amber-200 text-sm focus:outline-none focus:border-amber-400"
          />
          <button
            type="button"
            onClick={addPearl}
            className="px-3 py-2 bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg text-sm hover:bg-amber-400/20"
          >
            Add
          </button>
        </div>
      </div>

      {/* Exam Relevance + Source Notes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1">
            Exam Relevance ({Math.round(data.exam_relevance * 100)}%)
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={data.exam_relevance}
            onChange={(e) => update("exam_relevance", parseFloat(e.target.value))}
            className="w-full accent-amber-400"
          />
        </div>
        <div>
          <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1">
            Source Notes
          </label>
          <input
            type="text"
            value={data.source_notes}
            onChange={(e) => update("source_notes", e.target.value)}
            placeholder="e.g., Brodsky Ch. 12"
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
          />
        </div>
      </div>

      {/* Timeline */}
      <div>
        <label className="block text-xs text-zinc-500 uppercase tracking-wider mb-1">
          Timeline
        </label>
        <input
          type="text"
          value={data.timeline}
          onChange={(e) => update("timeline", e.target.value)}
          placeholder="e.g., Embryology (wk 4-7) → Prenatal → Birth → Neonatal (day 1-3)"
          className="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-zinc-100 text-sm focus:outline-none focus:border-amber-400"
        />
      </div>

      {/* Actions */}
      <div className="flex gap-3 pt-2">
        <button
          type="submit"
          disabled={saving}
          className="px-5 py-2.5 bg-amber-400 text-zinc-900 rounded-lg text-sm font-medium hover:bg-amber-300 disabled:opacity-50 transition-colors"
        >
          {saving ? "Saving..." : isEdit ? "Update Concept" : "Create Concept"}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="px-5 py-2.5 bg-zinc-800 text-zinc-300 rounded-lg text-sm hover:bg-zinc-700 transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}
