"use client";

import { Bar, BarChart, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { AnalysisResult } from "@/lib/api";

function SkillList({ items, empty, tone }: { items: string[]; empty: string; tone: "good" | "bad" }) {
  if (!items.length) return <p className="text-sm text-zinc-500">{empty}</p>;
  const cls = tone === "good"
    ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-200"
    : "border-red-400/20 bg-red-400/10 text-red-200";
  return (
    <div className="flex flex-wrap gap-2">
      {items.map((s) => (
        <span key={s} className={`rounded-full border px-3 py-1 text-xs ${cls}`}>{s}</span>
      ))}
    </div>
  );
}

export default function ResultCard({ result }: { result: AnalysisResult }) {
  const pie = [
    { name: "Matched", value: result.matched_skills.length },
    { name: "Missing", value: result.missing_skills.length },
  ];
  const bars = [
    { name: "Skill coverage", value: result.score },
    { name: "Semantic similarity", value: result.semantic_score ?? 0 },
  ];
  const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  return (
    <section aria-live="polite" className="space-y-6 rounded-2xl border border-white/10 bg-black/20 p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm text-zinc-400">Recognized skill coverage</p>
          <p className="mt-1 text-5xl font-bold text-violet-300">{result.score}%</p>
          <p className="mt-2 max-w-md text-xs text-zinc-500">{result.note}</p>
          {result.semantic_score !== undefined && (
            <p className="mt-1 text-xs text-zinc-400">
              Semantic similarity ({result.semantic_method}): <b>{result.semantic_score}%</b> — a text-similarity signal, not a hiring score.
            </p>
          )}
          {result.saved && result.id && (
            <p className="mt-1 text-xs text-emerald-300">✓ Saved to your history.</p>
          )}
        </div>
        <div className="h-36 w-40">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={pie} dataKey="value" nameKey="name" innerRadius={35} outerRadius={55} paddingAngle={3}>
                <Cell fill="#34d399" /><Cell fill="#f87171" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="h-40">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={bars} layout="vertical">
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis type="category" dataKey="name" width={130} tick={{ fill: "#a1a1aa", fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="value" radius={[0, 6, 6, 0]}>
              <Cell fill="#8b5cf6" /><Cell fill="#38bdf8" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h2 className="mb-2 font-semibold">Matched skills ({result.matched_skills.length})</h2>
        <SkillList items={result.matched_skills} empty="No matching skills found." tone="good" />
      </div>
      <div>
        <h2 className="mb-2 font-semibold">Skills not found in resume ({result.missing_skills.length})</h2>
        <SkillList items={result.missing_skills} empty="No missing skills from the recognized list." tone="bad" />
      </div>
      {result.by_category && Object.keys(result.by_category).length > 0 && (
        <div>
          <h2 className="mb-2 font-semibold">Skills by category</h2>
          <div className="space-y-1 text-sm text-zinc-300">
            {Object.entries(result.by_category).map(([cat, skills]) => (
              <p key={cat}><b className="text-zinc-100">{cat}:</b> {skills.join(", ")}</p>
            ))}
          </div>
        </div>
      )}
      {result.recommendations && result.recommendations.length > 0 && (
        <div>
          <h2 className="mb-2 font-semibold">What to improve</h2>
          <ul className="space-y-3">
            {result.recommendations.map((r) => (
              <li key={r.skill} className="rounded-xl border border-white/10 bg-white/[0.02] p-3 text-sm">
                <p><b className="text-violet-200">{r.skill}</b> — {r.evidence}</p>
                <p className="mt-1 text-zinc-400">{r.suggestion}</p>
                <a href={r.url} target="_blank" rel="noopener noreferrer" className="text-violet-300 underline">{r.resource} ↗</a>
              </li>
            ))}
          </ul>
        </div>
      )}
      {result.id && (
        <div className="flex flex-wrap gap-3">
          <a href={`${apiBase}/api/analysis/${result.id}/report.pdf`} className="rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold">Download PDF report</a>
          <a href={`${apiBase}/api/analysis/${result.id}/report.csv`} className="rounded-xl border border-white/10 px-4 py-2 text-sm">Download CSV</a>
          <a href={`/analysis/${result.id}`} className="rounded-xl border border-white/10 px-4 py-2 text-sm">Open detail page</a>
        </div>
      )}
    </section>
  );
}
