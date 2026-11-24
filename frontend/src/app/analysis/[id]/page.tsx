"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, type AnalysisResult } from "@/lib/api";
import Nav from "@/components/Nav";
import ResultCard from "@/components/ResultCard";

export default function AnalysisDetailPage() {
  const params = useParams();
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get(`/api/analysis/${params.id}`)
      .then((r) => setResult(r.data))
      .catch(() => setError("Analysis not found or you are not logged in."));
  }, [params.id]);

  return (
    <main className="min-h-screen px-5 pb-10">
      <Nav />
      <section className="mx-auto max-w-5xl py-8">
        <Link href="/dashboard" className="text-sm text-violet-300">← Back to dashboard</Link>
        {error && <p className="mt-6 text-red-400">{error}</p>}
        {!result && !error && <p className="mt-6 text-zinc-400">Loading…</p>}
        {result && (
          <div className="mt-6">
            <h1 className="mb-1 text-2xl font-bold">{result.job_title || result.filename || "Analysis"}</h1>
            <p className="mb-6 text-sm text-zinc-500">{result.created_at ? new Date(result.created_at).toLocaleString() : ""}</p>
            <ResultCard result={result} />
          </div>
        )}
      </section>
    </main>
  );
}
