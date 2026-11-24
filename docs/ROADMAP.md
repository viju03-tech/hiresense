# HireSense implementation roadmap

## Stage 1 — Backend foundation
- [x] FastAPI app and health endpoint
- [x] PDF/DOCX parsing
- [x] Starter skill extraction
- [x] Skill matching and transparent coverage score
- [x] Upload endpoint
- [x] Starter tests

## Stage 2 — Database and authentication
- [ ] Configure PostgreSQL and SQLAlchemy session dependency
- [ ] Add Alembic migrations
- [ ] Add registration/login and secure password hashing
- [ ] Add JWT access tokens and authorization checks
- [ ] Persist resumes and analyses with per-user ownership
- [ ] Add analysis history API

## Stage 3 — AI/ML
- [ ] Build a larger skills taxonomy with aliases and categories
- [ ] Evaluate extraction precision/recall on a consented test set
- [ ] Add sentence-transformer similarity at skill/requirement level
- [ ] Add evidence-grounded recommendations
- [ ] Document scoring weights and limitations

## Stage 4 — Frontend
- [x] Landing page and upload form
- [x] Results display
- [ ] Login/register
- [ ] Dashboard and analysis history
- [ ] Detailed result page and charts
- [ ] Downloadable PDF report

## Stage 5 — Quality and security
- [ ] Validate file signatures and MIME types
- [ ] Add malware scanning / parser isolation
- [ ] Add rate limits and stronger input validation
- [ ] Add frontend and API integration tests
- [ ] Add privacy controls, retention and deletion
- [ ] Add accessibility and mobile testing

## Stage 6 — Deployment
- [ ] Deploy Next.js frontend
- [ ] Deploy FastAPI backend
- [ ] Provision managed PostgreSQL
- [ ] Configure secrets, CORS, HTTPS and health checks
- [ ] Configure backups, logs and monitoring
- [ ] Publish documentation and demo

## Delivered status (2026-11-23 build)
- [x] Stage 1 — backend foundation, parsers, taxonomy (~100 skills, aliases, categories), matching, upload API
- [x] Stage 2 — SQLite default + Postgres via DATABASE_URL, tables created on startup, JWT register/login (bcrypt), user-owned analyses, history API (list/get/delete)
- [x] Stage 3 — TF-IDF semantic similarity in the request path; sentence-transformers optional via HIRESENSE_SEMANTIC_MODEL=1; evidence-grounded recommendations with real resources
- [x] Stage 4 — login/register, dashboard + history, detail page with charts, PDF/CSV reports, dark/light theme
- [x] Stage 5 — file-signature validation, 5 MB limit, rate limiting, no resume text stored/logged; 16 pytest tests passing; frontend `npm run build` passes
- [x] Stage 6 — Docker: compose now runs db + backend + frontend; Dockerfiles added
- [ ] Still open: Alembic migrations (create_all used instead), OCR for scanned PDFs, no malware scanning, no CSRF tokens, no email verification / password reset, no live deployment test, sentence-transformers not installed/tested (TF-IDF verified instead)
