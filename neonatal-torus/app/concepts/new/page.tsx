"use client";

import { useRouter } from "next/navigation";
import ConceptForm from "@/components/ConceptForm";

export default function NewConceptPage() {
  const router = useRouter();

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">New Concept</h1>
      <ConceptForm
        onSave={async (data) => {
          const res = await fetch("/api/concepts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });

          if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error || "Failed to create concept");
          }

          const { concept } = await res.json();
          router.push(`/concept/${concept.slug}`);
        }}
        onCancel={() => router.push("/concepts")}
      />
    </div>
  );
}
