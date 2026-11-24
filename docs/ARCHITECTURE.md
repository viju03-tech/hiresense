# HireSense architecture

## Request flow
1. User selects a PDF/DOCX and pastes a job description in Next.js.
2. Browser sends multipart form data to FastAPI.
3. FastAPI validates extension, size, and job-description presence.
4. Parser extracts text from PDF or DOCX.
5. Skill extractor identifies terms from the starter vocabulary.
6. Matcher compares unique recognized job skills against resume skills.
7. API returns a coverage percentage and matched/missing lists.
8. Next.js renders the result.

## Current limitations
- No OCR for scanned/image-only PDFs.
- Skill vocabulary is intentionally small and exact-match based.
- Semantic model is an optional future experiment, not active in the request path.
- Database models are a foundation; the initial API does not persist uploads or analyses.
- Authentication, dashboard history, report export, and LLM recommendations are roadmap items.
