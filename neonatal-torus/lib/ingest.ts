import { getDb } from "./db";
import { detectDomains, detectRing } from "./tagger";

/**
 * Split text into chunks of roughly 500-800 words,
 * respecting section boundaries (headers, double newlines, page breaks).
 */
export function chunkText(
  text: string,
  targetWords: number = 600
): { text: string; pageStart: number | null; pageEnd: number | null }[] {
  const chunks: { text: string; pageStart: number | null; pageEnd: number | null }[] = [];

  // Split on page breaks first (form feed), then on section boundaries
  const pages = text.split(/\f/);
  let currentChunk = "";
  let chunkPageStart: number | null = null;
  let chunkPageEnd: number | null = null;

  for (let pageIdx = 0; pageIdx < pages.length; pageIdx++) {
    const pageNum = pageIdx + 1;
    const pageText = pages[pageIdx];

    // Split page into paragraphs (double newline or header-like patterns)
    const paragraphs = pageText.split(/\n{2,}|(?=\n[A-Z][A-Z\s]{3,}\n)/);

    for (const para of paragraphs) {
      const trimmed = para.trim();
      if (!trimmed) continue;

      const currentWords = currentChunk.split(/\s+/).filter(Boolean).length;
      const paraWords = trimmed.split(/\s+/).filter(Boolean).length;

      if (currentWords + paraWords > targetWords * 1.3 && currentWords > targetWords * 0.4) {
        // Flush current chunk
        if (currentChunk.trim()) {
          chunks.push({
            text: currentChunk.trim(),
            pageStart: chunkPageStart,
            pageEnd: chunkPageEnd,
          });
        }
        currentChunk = trimmed;
        chunkPageStart = pageNum;
        chunkPageEnd = pageNum;
      } else {
        if (!currentChunk) chunkPageStart = pageNum;
        currentChunk += (currentChunk ? "\n\n" : "") + trimmed;
        chunkPageEnd = pageNum;
      }
    }
  }

  // Flush remaining
  if (currentChunk.trim()) {
    chunks.push({
      text: currentChunk.trim(),
      pageStart: chunkPageStart,
      pageEnd: chunkPageEnd,
    });
  }

  return chunks;
}

/**
 * Process extracted text: chunk, tag, and store in database.
 */
export function processDocument(documentId: number, fullText: string): number {
  const db = getDb();
  const chunks = chunkText(fullText);

  const insertChunk = db.prepare(`
    INSERT INTO chunks (document_id, page_start, page_end, text, domain_primary, domain_secondary, ring_label)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  const tx = db.transaction(() => {
    for (const chunk of chunks) {
      const domains = detectDomains(chunk.text);
      const ring = detectRing(chunk.text);

      insertChunk.run(
        documentId,
        chunk.pageStart,
        chunk.pageEnd,
        chunk.text,
        domains.primary,
        domains.secondary.length > 0 ? JSON.stringify(domains.secondary) : null,
        ring
      );
    }
  });

  tx();
  return chunks.length;
}

/**
 * Extract suggested concept names from chunks (headings, bold terms).
 */
export function suggestConcepts(documentId: number): string[] {
  const db = getDb();
  const chunks = db
    .prepare("SELECT text FROM chunks WHERE document_id = ?")
    .all(documentId) as { text: string }[];

  const candidates = new Set<string>();

  for (const chunk of chunks) {
    // Match lines that look like headers (ALL CAPS, short lines)
    const headerMatches = chunk.text.match(/^[A-Z][A-Z\s/()-]{3,50}$/gm);
    if (headerMatches) {
      for (const h of headerMatches) {
        const cleaned = h.trim();
        if (cleaned.length > 3 && cleaned.length < 60) {
          candidates.add(cleaned);
        }
      }
    }

    // Match bold-like patterns (common in textbook text)
    const boldMatches = chunk.text.match(/\*\*(.+?)\*\*/g);
    if (boldMatches) {
      for (const b of boldMatches) {
        const cleaned = b.replace(/\*\*/g, "").trim();
        if (cleaned.length > 2 && cleaned.length < 60) {
          candidates.add(cleaned);
        }
      }
    }
  }

  return Array.from(candidates).sort();
}
