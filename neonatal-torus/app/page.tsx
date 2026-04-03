import SearchBar from "@/components/SearchBar";
import DomainBar from "@/components/DomainBar";
import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Neonatal Torus</h1>
        <p className="text-zinc-500 text-sm">
          Search concepts, source text, and board pearls across all 20 ABP domains
        </p>
      </div>

      <SearchBar />

      <div className="pt-4">
        <h2 className="text-sm text-zinc-500 uppercase tracking-wider mb-3">
          ABP Exam Weight Distribution
        </h2>
        <DomainBar />
      </div>

      <div className="flex justify-center gap-4 pt-4">
        <Link
          href="/upload"
          className="px-4 py-2 bg-amber-400/10 text-amber-400 border border-amber-400/30 rounded-lg text-sm hover:bg-amber-400/20 transition-colors"
        >
          Upload a textbook
        </Link>
        <Link
          href="/torus"
          className="px-4 py-2 bg-zinc-800 text-zinc-300 border border-zinc-700 rounded-lg text-sm hover:bg-zinc-700 transition-colors"
        >
          View torus map
        </Link>
      </div>
    </div>
  );
}
