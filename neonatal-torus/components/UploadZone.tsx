"use client";

import { useState, useCallback, useRef } from "react";

interface UploadResult {
  success: boolean;
  documentId: number;
  title: string;
  filename: string;
  sourceType: string;
  pageCount: number | null;
  chunkCount: number;
  textLength: number;
}

export default function UploadZone({
  onUploadComplete,
}: {
  onUploadComplete?: (result: UploadResult) => void;
}) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState("");
  const [error, setError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleUpload = useCallback(
    async (file: File) => {
      setError(null);
      setUploading(true);
      setProgress("Uploading and extracting text...");

      try {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Upload failed");
        }

        setProgress(
          `Done! ${data.chunkCount} chunks extracted from ${data.pageCount ?? "?"} pages`
        );
        onUploadComplete?.(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
        setProgress("");
      } finally {
        setUploading(false);
      }
    },
    [onUploadComplete]
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleUpload(file);
    },
    [handleUpload]
  );

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      onClick={() => fileRef.current?.click()}
      className={`
        border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all
        ${
          dragging
            ? "border-amber-400 bg-amber-400/10"
            : "border-zinc-600 hover:border-zinc-400 bg-zinc-900/50"
        }
        ${uploading ? "pointer-events-none opacity-60" : ""}
      `}
    >
      <input
        ref={fileRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleUpload(file);
        }}
      />

      <div className="text-4xl mb-4">{uploading ? "⏳" : "📄"}</div>

      {uploading ? (
        <div>
          <div className="text-zinc-300 font-mono text-sm">{progress}</div>
          <div className="mt-4 w-48 h-1 bg-zinc-700 rounded-full mx-auto overflow-hidden">
            <div className="h-full bg-amber-400 rounded-full animate-pulse w-2/3" />
          </div>
        </div>
      ) : (
        <>
          <p className="text-zinc-300 font-medium mb-2">
            Drop a PDF or DOCX here
          </p>
          <p className="text-zinc-500 text-sm">
            or click to browse — text will be extracted, chunked, and auto-tagged
          </p>
        </>
      )}

      {error && (
        <div className="mt-4 text-red-400 text-sm font-mono">{error}</div>
      )}

      {progress && !uploading && !error && (
        <div className="mt-4 text-emerald-400 text-sm font-mono">{progress}</div>
      )}
    </div>
  );
}
