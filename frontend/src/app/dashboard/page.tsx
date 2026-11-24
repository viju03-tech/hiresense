"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, type AnalysisResult } from "@/lib/api";
import Nav from "@/components/Nav";

export default function DashboardPage() {
  const [items, setItems] = useState<AnalysisResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const router = useRouter();

  async function load() {
    try {
      const r = await api.get("/api/history");
      setItems(r.data.analyses);
    } catch {
      setError("Please log in to see your history.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function remove(id: string) {
    if (!confirm("Delete this analysis?")) return;
    await api.delete(`/api/analysis/${id}`);
    setItems(items.filter((i) => i.id !== id));
  }

  if (loading) return <main className="min-h-screen px-5"><Nav /><p className="mx-auto max-w-5xl py-10 text-zinc-400">Loading…</p></main>;
  if (error) return (
    <main className="min-h-screen px-5"><Nav />
      <div className="mx-auto max-w-5xl py-10">
        <p className="text-red-400">{error}</p>
        <Link href="/login" className="mt-4 inline-block rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold">Log in</Link>
      </div>
    </main>
  );

  const avg = items.length ? Math.round(items.reduce((s, i) => s + i.score, 0) / items.length) : 0;

  return (
    <main className="min-h-screen px-5 pb-10">
      <Nav />
      <section className="mx-auto max-w-5xl py-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="mt-2 text-zinc-400">
          {items.length} saved {items.length === 1 ? "analysis" : "analyses"}
          {items.length > 0 && <> · average score <b className="text-violet-300">{avg}%</b></>}
        </p>
        <Link href="/" className="mt-4 inline-block rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold">+ New analysis</Link>
        {items.length === 0 ? (
          <p className="mt-8 rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-zinc-400">
            No saved analyses yet. Log in, then run an analysis from the home page — it will appear here.
          </p>
        ) : (
          <div className="mt-8 space-y-3">
            {items.map((a) => (
              <div key={a.id} className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-white/10 bg-white/[0.03] p-4">
                <div>
                  <p className="font-semibold">{a.job_title || a.filename || "Analysis"}</p>
                  <p className="text-xs text-zinc-500">{a.created_at ? new Date(a.created_at).toLocaleString() : ""} · {a.matched_skills.length}/{a.job_skills.length} skills matched</p>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-2xl font-bold text-violet-300">{a.score}%</span>
                  <Link href={`/analysis/${a.id}`} className="rounded-lg border border-white/10 px-3 py-1.5 text-sm">View</Link>
                  <button onClick={() => a.id && remove(a.id)} className="rounded-lg border border-red-400/30 px-3 py-1.5 text-sm text-red-300">Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
