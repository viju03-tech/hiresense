"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { getStoredUser, logout } from "@/lib/api";

export default function Nav() {
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);
  const [theme, setTheme] = useState("dark");

  useEffect(() => {
    setUser(getStoredUser());
    const saved = localStorage.getItem("hiresense_theme") || "dark";
    setTheme(saved);
    document.documentElement.dataset.theme = saved;
  }, []);

  function toggleTheme() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    localStorage.setItem("hiresense_theme", next);
    document.documentElement.dataset.theme = next;
  }

  return (
    <nav className="mx-auto flex max-w-5xl items-center justify-between px-5 py-4">
      <Link href="/" className="text-xl font-bold tracking-tight">
        <span className="text-violet-400">✦</span> HireSense
      </Link>
      <div className="flex items-center gap-3 text-sm">
        <button onClick={toggleTheme} className="rounded-lg border border-white/10 px-3 py-1.5" aria-label="Toggle theme">
          {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
        </button>
        {user ? (
          <>
            <Link href="/dashboard" className="rounded-lg border border-white/10 px-3 py-1.5">Dashboard</Link>
            <span className="hidden text-zinc-400 sm:inline">{user.name}</span>
            <button onClick={() => { logout(); window.location.href = "/"; }} className="rounded-lg bg-white/10 px-3 py-1.5">Log out</button>
          </>
        ) : (
          <>
            <Link href="/login" className="rounded-lg border border-white/10 px-3 py-1.5">Log in</Link>
            <Link href="/register" className="rounded-lg bg-violet-600 px-3 py-1.5 font-semibold">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  );
}
