import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Neonatal Torus",
  description: "ABP Neonatal-Perinatal Medicine Board Study Tool",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="font-mono bg-zinc-950 text-zinc-100 min-h-screen antialiased">
        <nav className="border-b border-zinc-800 px-6 py-3">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2 text-zinc-100 hover:text-amber-400 transition-colors">
              <span className="text-lg font-bold tracking-tight">Neonatal Torus</span>
              <span className="text-xs text-zinc-500 hidden sm:inline">ABP Board Study</span>
            </Link>
            <div className="flex items-center gap-4 text-sm">
              <Link href="/" className="text-zinc-400 hover:text-zinc-100 transition-colors">
                Search
              </Link>
              <Link href="/upload" className="text-zinc-400 hover:text-zinc-100 transition-colors">
                Upload
              </Link>
              <Link href="/torus" className="text-zinc-400 hover:text-zinc-100 transition-colors">
                Torus
              </Link>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-6 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
