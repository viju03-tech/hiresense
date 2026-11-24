import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("hiresense_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export type Recommendation = {
  skill: string;
  evidence: string;
  suggestion: string;
  resource: string;
  url: string;
};

export type AnalysisResult = {
  id?: string | null;
  score: number;
  score_type: string;
  semantic_score?: number;
  semantic_method?: string;
  resume_skills: string[];
  job_skills: string[];
  matched_skills: string[];
  missing_skills: string[];
  total_required: number;
  by_category?: Record<string, string[]>;
  recommendations?: Recommendation[];
  saved?: boolean;
  note: string;
  filename?: string;
  job_title?: string | null;
  created_at?: string | null;
};

export function getStoredUser(): { name: string; email: string } | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("hiresense_user");
  return raw ? JSON.parse(raw) : null;
}

export function logout() {
  localStorage.removeItem("hiresense_token");
  localStorage.removeItem("hiresense_user");
}
