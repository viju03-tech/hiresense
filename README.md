# HireSense — AI Resume Analyzer

**Live website:** https://viju03-tech.github.io/hiresense/

Upload a resume and get a real, explainable analysis — skill match score, ATS score, salary estimate, and the jobs you can apply for, ranked by match %.

> The live website (`index.html`) runs entirely in your browser — no server, no uploads. The `backend/` + `frontend/` folders are the full-stack version of the same product (FastAPI + Next.js + PostgreSQL/SQLite).

## Live website

Open https://viju03-tech.github.io/hiresense/ — upload a PDF or DOCX resume (or paste the text) and see your results. No account needed; history is saved in your browser only.

- **Resume analysis** — skill match score, matched vs. missing skills, skill-by-category breakdown
- **Jobs you can apply for** — 32 tech + non-tech roles ranked by match %, required skills shown as have vs. missing, best match highlighted. No job description needed.
- **Job description matching** — paste any job description (optional) for a match score and semantic similarity
- **ATS score** — 0–100 with a 13-point breakdown and fixes
- **Salary estimate** — rough India-market range per role, labelled as an estimate
- **Experience level** — Fresher / Junior / Mid-level / Senior, detected from the resume
- **Skill-gap learning plan** — steps and free resource links for missing skills
- **Job links** — real LinkedIn / Indeed / Naukri searches per role, Chennai / Bangalore / Remote filters
- **Resume builder** — auto-fixes headings, bullets and duplicates, download an improved PDF
- **Compare** — score two resumes side by side
- **Dashboard** — analysis history, saved/shortlisted jobs, PDF/CSV reports

**Coverage:** 199 skills across 18 categories, 32 roles — Data Scientist, Machine Learning Engineer, AI Engineer, Data Analyst, Backend / Frontend / Full Stack Developer, DevOps, Cloud, Cybersecurity, UI/UX Designer, Digital Marketing, Content Writer, HR / Recruiter, Accountant, Sales, Customer Support, Business Analyst, Operations, Logistics, Teacher / Trainer, Nurse / Healthcare, Event Manager, and more.

## Full-stack version

A full-stack project using **Python + FastAPI + Next.js + PostgreSQL (SQLite fallback)**.

### Features

- PDF and DOCX text extraction (file-signature validation, 5 MB limit)
- ~100-skill taxonomy with aliases and categories (Languages, Data & AI, Web, Cloud & DevOps, Security, Testing, …)
- Matched and missing skills, explainable skill-coverage score
- Semantic similarity: TF-IDF cosine by default; optional sentence-transformers embeddings (`HIRESENSE_SEMANTIC_MODEL=1`)
- Recommendations for missing skills, grounded in the job description, with real free resources
- JWT register/login (bcrypt password hashing); analysis works anonymously, history needs login
- Persistence: SQLite by default (`./hiresense.db`), PostgreSQL via `DATABASE_URL`
- Analysis history API: `GET /api/history`, `GET /api/analysis/{id}`, `DELETE /api/analysis/{id}`
- PDF and CSV report downloads: `GET /api/analysis/{id}/report.pdf` / `.csv`
- Next.js frontend: upload + results with charts, login/register, dashboard with history, detail pages, dark/light theme
- Rate limiting (10 uploads/minute per IP by default), no resume text stored or logged
- Pytest suite (16 tests — all passing)

### Requirements

- Python 3.11+ (tested on Python 3.12; on Windows, Python 3.13/3.15 works — create the venv with your Python)
- Node.js 20+, npm
- PostgreSQL only if you want it (or Docker Desktop); SQLite works with zero setup

### Quick start — Windows (PowerShell)

**Backend**
```powershell
cd backend
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Optional: edit .env to set a long random SECRET_KEY and a DATABASE_URL for Postgres
uvicorn app.main:app --reload
```
API: http://localhost:8000 — Docs: http://localhost:8000/docs — Health: http://localhost:8000/api/health

**Frontend** (second terminal)
```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```
Frontend: http://localhost:3000

**Try it:** open the frontend, sign up (optional — anonymous analysis works too), choose a PDF/DOCX resume, paste a job description, and click **Analyze resume**.

### Quick start — Docker

```bash
docker compose up --build
```
Backend on :8000, frontend on :3000, Postgres on :5432. Change the placeholder password in `.env.example` before any real deployment.

### API

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/health` | — | Health check |
| POST | `/api/analyze-upload` | optional | multipart: `file` (PDF/DOCX ≤ 5 MB), `job_description`, `job_title` |
| POST | `/api/auth/register` | — | `{name, email, password}` → JWT |
| POST | `/api/auth/login` | — | `{email, password}` → JWT |
| GET | `/api/auth/me` | JWT | Current user |
| GET | `/api/history` | JWT | Saved analyses |
| GET | `/api/analysis/{id}` | JWT | One analysis |
| DELETE | `/api/analysis/{id}` | JWT | Delete an analysis |
| GET | `/api/analysis/{id}/report.pdf` | JWT | PDF report |
| GET | `/api/analysis/{id}/report.csv` | JWT | CSV report |

### Scoring

Skill coverage: `matched unique required skills / total unique required skills × 100`. Semantic similarity is a separate TF-IDF (or embedding) document-similarity signal, shown alongside — it does not change the skill score. Neither measures seniority, quality, experience depth, or hiring suitability.

> This is a development project, not a production-ready hiring or ATS system. The score is a keyword-based skill coverage metric, not a probability of getting hired. Review the privacy and security checklist before deploying with real resumes.

## Project structure

```text
HireSense/
├── index.html          # live website (GitHub Pages) — standalone, runs in the browser
├── README.md
├── LICENSE             # MIT
├── .gitignore
├── docker-compose.yml  # db + backend + frontend
├── backend/            # FastAPI: api, core, models, services, tests
├── frontend/           # Next.js: upload, results, dashboard, login/register
└── docs/               # ARCHITECTURE.md, ROADMAP.md
```

## Author

Built by **Viju B** (viju03-tech) — B.E. CSE, Sathyabama Institute of Science and Technology, Data Science & ML.

## License

MIT — see [LICENSE](LICENSE).
