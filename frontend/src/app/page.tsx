import Link from "next/link";
import Nav from "@/components/Nav";
import UploadBox from "@/components/UploadBox";

export default function Home() {
  return (
    <main className="min-h-screen px-5 pb-10">
      <Nav />
      <section className="mx-auto max-w-5xl py-12">
        <div className="max-w-2xl">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.25em] text-violet-300">
            Understand your career fit
          </p>
          <h1 className="text-4xl font-bold leading-tight md:text-6xl">
            Your career. <span className="text-violet-400">Analyzed smarter.</span>
          </h1>
          <p className="mt-5 max-w-xl text-zinc-400">
            Compare your resume with a job description, identify relevant skills,
            and discover opportunities to improve. Sign up to save your analyses
            and download PDF reports.
          </p>
          <div className="mt-5 flex gap-3">
            <Link href="/dashboard" className="rounded-xl bg-violet-600 px-4 py-2 text-sm font-semibold">My dashboard</Link>
            <Link href="/register" className="rounded-xl border border-white/10 px-4 py-2 text-sm">Create a free account</Link>
          </div>
        </div>
        <div className="mt-12">
          <UploadBox />
        </div>
        <p className="mt-5 text-xs text-zinc-500">
          Anonymous analyses are processed for the request only and are not saved.
          Logged-in analyses save the score and skills (never the resume text) to your history.
          Do not upload sensitive documents to an untrusted deployment.
        </p>
      </section>
    </main>
  );
}
