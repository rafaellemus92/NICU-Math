import { NextRequest, NextResponse } from "next/server";
import { writeFile, mkdir } from "fs/promises";
import path from "path";
import { getDb } from "@/lib/db";
import { processDocument } from "@/lib/ingest";

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get("file") as File | null;

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }

    const filename = file.name;
    const ext = path.extname(filename).toLowerCase();

    if (![".pdf", ".docx"].includes(ext)) {
      return NextResponse.json(
        { error: "Only PDF and DOCX files are supported" },
        { status: 400 }
      );
    }

    // Save file to uploads/
    const uploadsDir = path.join(process.cwd(), "uploads");
    await mkdir(uploadsDir, { recursive: true });

    const timestamp = Date.now();
    const savedFilename = `${timestamp}-${filename}`;
    const filepath = path.join(uploadsDir, savedFilename);
    const buffer = Buffer.from(await file.arrayBuffer());
    await writeFile(filepath, buffer);

    // Extract text
    let fullText = "";
    let pageCount: number | null = null;
    const sourceType = ext === ".pdf" ? "pdf" : "docx";

    if (ext === ".pdf") {
      const { PDFParse } = await import("pdf-parse");
      const pdf = new PDFParse({ data: new Uint8Array(buffer) });
      const textResult = await pdf.getText();
      fullText = textResult.text;
      pageCount = textResult.pages.length;
      await pdf.destroy();
    } else {
      const mammoth = await import("mammoth");
      const result = await mammoth.extractRawText({ buffer });
      fullText = result.value;
    }

    if (!fullText.trim()) {
      return NextResponse.json(
        { error: "No text could be extracted from the file" },
        { status: 422 }
      );
    }

    // Save document record
    const db = getDb();
    const title = path.basename(filename, ext);
    const result = db
      .prepare(
        "INSERT INTO documents (title, filename, filepath, source_type, page_count) VALUES (?, ?, ?, ?, ?)"
      )
      .run(title, filename, filepath, sourceType, pageCount);

    const documentId = result.lastInsertRowid as number;

    // Process: chunk, tag, store
    const chunkCount = processDocument(documentId, fullText);

    return NextResponse.json({
      success: true,
      documentId,
      title,
      filename,
      sourceType,
      pageCount,
      chunkCount,
      textLength: fullText.length,
    });
  } catch (error) {
    console.error("Upload error:", error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Upload failed" },
      { status: 500 }
    );
  }
}
