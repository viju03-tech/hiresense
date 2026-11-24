"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import Nav from "@/components/Nav";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      const r = await api.post("/api/auth/login", { email, password });
      localStorage.setItem("hiresense_token", r.data.access_token);
      localStorage.setItem("hiresense_user", JSON.stringify(r.data.user));
      router.push("/dashboard");
    } catch {
      setError("Invalid email or password.");
    }
  }

  return (
    <main className="min-h-screen px-5 pb-10">
      <Nav />
      <form onSubmit={submit} className="mx-auto mt-12 max-w-md space-y-4 rounded-3xl border border-white/10 bg-white/[0.03] p-8">
        <h1 className="text-2xl font-bold">Log in</h1>
        <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email"
          className="w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm outline-none focus:border-violet-500" />
        <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password"
          className="w-full rounded-xl border border-white/10 bg-black/30 p-3 text-sm outline-none focus:border-violet-500" />
        {error && <p role="alert" className="text-sm text-red-400">{error}</p>}
        <button className="w-full rounded-xl bg-violet-600 px-6 py-3 font-semibold hover:bg-violet-500">Log in</button>
        <p className="text-sm text-zinc-400">No account? <Link href="/register" className="text-violet-300 underline">Sign up</Link></p>
      </form>
    </main>
  );
}
