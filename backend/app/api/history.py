from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.entities import Analysis, User

router = APIRouter(tags=["history"])


def _out(a: Analysis) -> dict:
    return {
        "id": a.id, "filename": a.filename, "job_title": a.job_title,
        "score": a.score, "semantic_score": a.semantic_score,
        "semantic_method": a.semantic_method,
        "resume_skills": a.resume_skills, "job_skills": a.job_skills,
        "matched_skills": a.matched_skills, "missing_skills": a.missing_skills,
        "recommendations": a.recommendations,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.get("/history")
def list_history(limit: int = 50, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (db.query(Analysis).filter(Analysis.user_id == user.id)
            .order_by(Analysis.created_at.desc()).limit(min(limit, 100)).all())
    return {"analyses": [_out(r) for r in rows], "count": len(rows)}


@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return _out(row)


@router.delete("/analysis/{analysis_id}")
def delete_analysis(analysis_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == user.id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    db.delete(row)
    db.commit()
    return {"deleted": True, "id": analysis_id}
