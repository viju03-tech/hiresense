"""Upload analysis endpoint.

Security: extension + file-signature (magic bytes) validation, 5 MB limit,
simple per-IP rate limiting, and no resume text in logs or error responses.
If the caller is logged in, the analysis is saved to their history;
anonymous analysis still works and is not persisted.
"""
import os
import time
from collections import defaultdict
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from app.api.auth import get_optional_user
from app.core.database import get_db
from app.models.entities import Analysis, User
from app.services.docx_parser import extract_docx_text
from app.services.matcher import match_skills
from app.services.pdf_parser import extract_pdf_text
from app.services.recommendations import build_recommendations
from app.services.semantic_matcher import semantic_similarity
from app.services.skill_extractor import extract_skills, extract_skills_by_category

router = APIRouter(tags=["analysis"])

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
# Magic bytes: PDF starts with %PDF; DOCX is a ZIP archive (PK\x03\x04).
MAGIC = {".pdf": b"%PDF", ".docx": b"PK\x03\x04"}

# Simple in-memory rate limit: 10 uploads / minute per IP.
_RATE: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = int(os.environ.get("HIRESENSE_RATE_LIMIT", "10"))


def _check_rate(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = [t for t in _RATE[ip] if now - t < 60]
    if len(bucket) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Try again in a minute.")
    bucket.append(now)
    _RATE[ip] = bucket


@router.post("/analyze-upload")
async def analyze_upload(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form(...),
    job_title: str = Form(""),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    _check_rate(request)
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    if not job_description.strip():
        raise HTTPException(status_code=422, detail="Job description cannot be empty.")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 5 MB limit.")
    if not content.startswith(MAGIC[extension]):
        raise HTTPException(
            status_code=400,
            detail="File contents do not match its extension. Upload a real PDF or DOCX file.",
        )

    temp_path = None
    try:
        with NamedTemporaryFile(suffix=extension, delete=False) as temp:
            temp.write(content)
            temp_path = temp.name

        resume_text = extract_pdf_text(temp_path) if extension == ".pdf" else extract_docx_text(temp_path)
        if not resume_text.strip():
            raise HTTPException(status_code=422, detail="No readable text found. Scanned PDFs need OCR, which is not included yet.")

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_description)
        result = match_skills(resume_skills, job_skills)
        semantic = semantic_similarity(resume_text, job_description)
        recommendations = build_recommendations(result["missing_skills"], job_description)

        analysis_id = None
        if user is not None:
            row = Analysis(
                user_id=user.id, filename=file.filename or "",
                job_title=job_title.strip() or None,
                score=result["score"], semantic_score=semantic["score"],
                semantic_method=semantic["method"],
                resume_skills=resume_skills, job_skills=job_skills,
                matched_skills=result["matched_skills"],
                missing_skills=result["missing_skills"],
                recommendations=recommendations,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            analysis_id = row.id

        return {
            "id": analysis_id,
            "score": result["score"],
            "score_type": "recognized_required_skill_coverage",
            "semantic_score": semantic["score"],
            "semantic_method": semantic["method"],
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "total_required": result["total_required"],
            "by_category": extract_skills_by_category(resume_text),
            "recommendations": recommendations,
            "saved": analysis_id is not None,
            "note": (
                "This is a keyword-based skill coverage metric, not an ATS score "
                "or a prediction of hiring success."
                if job_skills
                else "No skills from the taxonomy were recognized in the job description."
            ),
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Could not read this document.") from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
