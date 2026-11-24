"""Downloadable PDF / CSV reports for a saved analysis. PDF is built with
PyMuPDF (already a dependency) — no extra report library needed."""
import csv
import io

import fitz
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.entities import Analysis, User

router = APIRouter(tags=["reports"])


def _get(aid: str, user: User, db: Session) -> Analysis:
    row = db.query(Analysis).filter(Analysis.id == aid, Analysis.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return row


@router.get("/analysis/{analysis_id}/report.csv")
def report_csv(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = _get(analysis_id, user, db)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["HireSense analysis report"])
    w.writerow(["analysis_id", a.id])
    w.writerow(["filename", a.filename])
    w.writerow(["score", a.score])
    w.writerow(["semantic_score", a.semantic_score or ""])
    w.writerow(["semantic_method", a.semantic_method or ""])
    w.writerow([])
    w.writerow(["skill", "status"])
    for s in a.matched_skills:
        w.writerow([s, "matched"])
    for s in a.missing_skills:
        w.writerow([s, "missing"])
    w.writerow([])
    w.writerow(["skill", "recommendation", "resource", "url"])
    for r in a.recommendations:
        w.writerow([r.get("skill"), r.get("suggestion"), r.get("resource"), r.get("url")])
    return Response(content=buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="hiresense-{a.id}.csv"'})


@router.get("/analysis/{analysis_id}/report.pdf")
def report_pdf(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    a = _get(analysis_id, user, db)
    doc = fitz.open()
    page = doc.new_page()
    y = 60.0
    def line(text: str, size: int = 12, bold: bool = False):
        nonlocal y, page
        if y > 760:
            page = doc.new_page(); y = 60.0
        font = "hebo" if bold else "helv"  # PyMuPDF base-14 font names
        page.insert_text((50, y), text[:140], fontsize=size, fontname=font)
        y += size + 8
    line("HireSense — Resume Analysis Report", 18, True)
    line(f"Analysis: {a.id}", 10)
    line(f"Resume file: {a.filename or '-'}", 11)
    line(f"Skill coverage score: {a.score}%", 14, True)
    if a.semantic_score is not None:
        line(f"Semantic similarity ({a.semantic_method}): {a.semantic_score}%", 11)
    line("", 10)
    line("Matched skills", 13, True)
    line(", ".join(a.matched_skills) if a.matched_skills else "None", 11)
    line("Missing skills", 13, True)
    line(", ".join(a.missing_skills) if a.missing_skills else "None", 11)
    line("Recommendations", 13, True)
    for r in a.recommendations:
        line(f"- {r.get('skill')}: {r.get('suggestion')}", 11)
        line(f"  Resource: {r.get('resource')} — {r.get('url')}", 10)
    line("", 10)
    line("This is a skill-coverage metric, not a hiring decision.", 10)
    pdf = bytes(doc.tobytes())
    return Response(content=pdf, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="hiresense-{a.id}.pdf"'})
