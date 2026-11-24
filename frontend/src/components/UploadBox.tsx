"use client";

import { useState } from "react";
import { api, type AnalysisResult } from "@/lib/api";
import ResultCard from "./ResultCard";

export default function UploadBox() {
  const [file, setFile] = useState<File | null>(null);
  const [job, setJob] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function analyze() {
    if (!file || !job.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", job);
    formData.append("job_title", jobTitle);
    try {
      const response = await api.post<AnalysisResult>("/api/analyze-upload", formData);
      setResult(response.data);
    } catch (err: unknown) {
      const message =
        typeof err === "object" && err !== null && "response" in err
          ? String((err as { response?: { data?: { detail?: string } } }).response?.data?.detail || "Analysis failed.")
          : "Could not connect to HireSense API. Check that the backend is running.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid gap-6 rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8">
      <div>
        <label className="mb-2 block text-sm font-semibold">Your resume</label>
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => { setFile(e.target.files?.[0] || null); setResult(null); }}
          className="block w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm text-zinc-300 file:mr-4 file:rounded-lg file:border-0 file:bg-violet-600 file:px-4 file:py-2 file:text-white"
        />
        <p className="mt-2 text-xs text-zinc-500">PDF or DOCX · maximum 5 MB · file contents are verified, not just the name</p>
      </div>
      <div>
        <label className="mb-2 block text-sm font-semibold">Job title (optional)</label>
        <input value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} placeholder="e.g. Data Science Intern"
          className="w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm outline-none focus:border-violet-500" />
      </div>
      <div>
        <label className="mb-2 block text-sm font-semibold">Job description</label>
        <textarea value={job} onChange={(e) => setJob(e.target.value)} placeholder="Paste the job description here..." rows={8}
          className="w-full resize-y rounded-xl border border-white/10 bg-black/30 p-4 text-sm outline-none transition focus:border-violet-500" />
      </div>
      <button onClick={analyze} disabled={!file || !job.trim() || loading}
        className="rounded-xl bg-violet-600 px-6 py-3 font-semibold transition hover:bg-violet-500 disabled:cursor-not-allowed disabled:opacity-40">
        {loading ? "Analyzing..." : "Analyze resume"}
      </button>
      {error && <p role="alert" className="text-sm text-red-400">{error}</p>}
      {result && <ResultCard result={result} />}
    </div>
  );
}
