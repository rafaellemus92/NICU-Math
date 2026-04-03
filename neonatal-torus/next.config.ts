import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["better-sqlite3", "pdfjs-dist", "pdf-parse"],
};

export default nextConfig;
