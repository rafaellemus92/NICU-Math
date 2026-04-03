import { NextRequest, NextResponse } from "next/server";
import { getDb } from "@/lib/db";

interface ChunkRow {
  id: number;
  document_id: number;
  page_start: number | null;
  page_end: number | null;
  text: string;
  domain_primary: string | null;
  domain_secondary: string | null;
  ring_label: string | null;
  document_title: string;
}

/**
 * Enhanced search: returns chunks with highlights, related terms,
 * cross-domain connections, and co-occurrence data.
 */
export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q");
  const domain = req.nextUrl.searchParams.get("domain");

  if (!q || q.trim().length === 0) {
    return NextResponse.json({
      query: "",
      chunks: [],
      relatedTerms: [],
      domainBreakdown: [],
      crossDomainLinks: [],
    });
  }

  const db = getDb();
  const searchTerms = q.trim().split(/\s+/).filter(Boolean);

  // 1. Find matching chunks via LIKE (more reliable than FTS for partial matches)
  let chunkQuery = `
    SELECT ch.id, ch.document_id, ch.page_start, ch.page_end, ch.text,
           ch.domain_primary, ch.domain_secondary, ch.ring_label,
           d.title as document_title
    FROM chunks ch
    LEFT JOIN documents d ON d.id = ch.document_id
    WHERE (${searchTerms.map(() => "ch.text LIKE ?").join(" OR ")})
  `;
  const params: string[] = searchTerms.map((t) => `%${t}%`);

  if (domain) {
    chunkQuery += " AND ch.domain_primary = ?";
    params.push(domain);
  }

  chunkQuery += " ORDER BY ch.id LIMIT 100";
  const chunks = db.prepare(chunkQuery).all(...params) as ChunkRow[];

  // 2. Extract highlighted snippets from each chunk
  const highlightedChunks = chunks.map((ch) => {
    const snippets = extractSnippets(ch.text, searchTerms, 120);
    return {
      id: ch.id,
      documentId: ch.document_id,
      documentTitle: ch.document_title,
      pageStart: ch.page_start,
      pageEnd: ch.page_end,
      domain: ch.domain_primary,
      ring: ch.ring_label,
      snippets,
      fullText: ch.text,
    };
  });

  // 3. Find related terms that co-occur with search terms
  const relatedTerms = findRelatedTerms(chunks, searchTerms);

  // 4. Domain breakdown — how many chunks per domain
  const domainMap = new Map<string, number>();
  for (const ch of chunks) {
    if (ch.domain_primary) {
      domainMap.set(ch.domain_primary, (domainMap.get(ch.domain_primary) || 0) + 1);
    }
  }
  const domainBreakdown = Array.from(domainMap.entries())
    .map(([domain, count]) => ({ domain, count }))
    .sort((a, b) => b.count - a.count);

  // 5. Cross-domain links — terms that appear in multiple domains
  const crossDomainLinks = findCrossDomainLinks(chunks, searchTerms);

  // 6. Find related concepts
  const concepts = db
    .prepare(
      `SELECT * FROM concepts WHERE ${searchTerms
        .map(
          () =>
            "(name LIKE ? OR ring1_identity LIKE ? OR ring2_taxonomy LIKE ? OR ring3_associations LIKE ? OR ring4_distinctions LIKE ? OR ring5_edge LIKE ? OR board_pearls LIKE ?)"
        )
        .join(" OR ")} LIMIT 20`
    )
    .all(
      ...searchTerms.flatMap((t) => {
        const like = `%${t}%`;
        return [like, like, like, like, like, like, like];
      })
    );

  return NextResponse.json({
    query: q,
    chunks: highlightedChunks,
    relatedTerms,
    domainBreakdown,
    crossDomainLinks,
    concepts,
    totalChunks: chunks.length,
  });
}

/**
 * Extract snippets around search terms with surrounding context.
 */
function extractSnippets(
  text: string,
  terms: string[],
  contextChars: number
): { text: string; highlights: [number, number][] }[] {
  const snippets: { text: string; highlights: [number, number][] }[] = [];
  const lower = text.toLowerCase();
  const used = new Set<number>();

  for (const term of terms) {
    const termLower = term.toLowerCase();
    let idx = 0;
    while ((idx = lower.indexOf(termLower, idx)) !== -1) {
      // Avoid overlapping snippets
      const snippetKey = Math.floor(idx / contextChars);
      if (!used.has(snippetKey)) {
        used.add(snippetKey);
        const start = Math.max(0, idx - contextChars);
        const end = Math.min(text.length, idx + term.length + contextChars);
        const snippet = text.substring(start, end);

        // Find all term positions within this snippet
        const highlights: [number, number][] = [];
        const snippetLower = snippet.toLowerCase();
        for (const t of terms) {
          const tLower = t.toLowerCase();
          let si = 0;
          while ((si = snippetLower.indexOf(tLower, si)) !== -1) {
            highlights.push([si, si + t.length]);
            si += t.length;
          }
        }

        snippets.push({
          text: (start > 0 ? "..." : "") + snippet + (end < text.length ? "..." : ""),
          highlights: highlights.sort((a, b) => a[0] - b[0]),
        });
      }
      idx += term.length;
      if (snippets.length >= 3) break;
    }
    if (snippets.length >= 3) break;
  }

  return snippets;
}

/**
 * Find medical/scientific terms that frequently co-occur with search terms.
 */
function findRelatedTerms(
  chunks: ChunkRow[],
  searchTerms: string[]
): { term: string; count: number; domains: string[] }[] {
  // Medical term patterns — capitalized terms, abbreviations, multi-word medical terms
  const termRegex =
    /\b(?:[A-Z]{2,}(?:-[A-Z]+)*|[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}(?:\s+(?:syndrome|disease|deficiency|receptor|pathway|transport|channel|protein))?)\b/g;

  const termCounts = new Map<string, { count: number; domains: Set<string> }>();
  const searchLower = new Set(searchTerms.map((t) => t.toLowerCase()));

  for (const chunk of chunks) {
    const matches = chunk.text.match(termRegex) || [];
    const seen = new Set<string>();

    for (const match of matches) {
      const cleaned = match.trim();
      if (
        cleaned.length < 3 ||
        cleaned.length > 50 ||
        searchLower.has(cleaned.toLowerCase()) ||
        /^(The|This|That|These|Those|Which|Where|When|What|With|From|Into|Also|Most|Some|Many|Each|Both|More|Less|Very|Such|Only|Just|Even|Than|Then|They|Their|There|Have|Has|Had|Been|Were|Was|Are|Not|And|But|For|Nor|Yet)$/i.test(
          cleaned
        )
      ) {
        continue;
      }

      if (!seen.has(cleaned.toLowerCase())) {
        seen.add(cleaned.toLowerCase());
        const existing = termCounts.get(cleaned.toLowerCase()) || {
          count: 0,
          domains: new Set<string>(),
        };
        existing.count++;
        if (chunk.domain_primary) existing.domains.add(chunk.domain_primary);
        termCounts.set(cleaned.toLowerCase(), existing);
      }
    }
  }

  return Array.from(termCounts.entries())
    .filter(([, v]) => v.count >= 2)
    .map(([term, v]) => ({
      term,
      count: v.count,
      domains: Array.from(v.domains),
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 20);
}

/**
 * Find concepts/terms that bridge multiple domains.
 */
function findCrossDomainLinks(
  chunks: ChunkRow[],
  searchTerms: string[]
): { term: string; domains: string[]; chunkCount: number }[] {
  // Group chunks by domain, find terms that appear across domains
  const domainTerms = new Map<string, Set<string>>();

  for (const chunk of chunks) {
    if (!chunk.domain_primary) continue;
    if (!domainTerms.has(chunk.domain_primary)) {
      domainTerms.set(chunk.domain_primary, new Set());
    }

    // Extract key terms
    const words = chunk.text.match(
      /\b[A-Z][a-z]+(?:[-][a-z]+)*\b|\b[A-Z]{2,}\b/g
    );
    if (words) {
      for (const w of words) {
        if (w.length >= 3) {
          domainTerms.get(chunk.domain_primary)!.add(w.toLowerCase());
        }
      }
    }
  }

  // Find terms in multiple domains
  const allTerms = new Map<string, Set<string>>();
  for (const [domain, terms] of domainTerms) {
    for (const term of terms) {
      if (!allTerms.has(term)) allTerms.set(term, new Set());
      allTerms.get(term)!.add(domain);
    }
  }

  // Filter to search-relevant cross-domain terms
  const searchLower = searchTerms.map((t) => t.toLowerCase());

  return Array.from(allTerms.entries())
    .filter(([term, domains]) => {
      if (domains.size < 2) return false;
      // Prioritize terms related to search
      return (
        searchLower.some((s) => term.includes(s) || s.includes(term)) ||
        domains.size >= 3
      );
    })
    .map(([term, domains]) => ({
      term,
      domains: Array.from(domains),
      chunkCount: chunks.filter(
        (ch) => ch.text.toLowerCase().includes(term)
      ).length,
    }))
    .sort((a, b) => b.domains.length - a.domains.length || b.chunkCount - a.chunkCount)
    .slice(0, 15);
}
