from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")


class Analysis(Base):
    """One resume-vs-job analysis. user_id is NULL for anonymous analyses;
    resume text itself is never stored — only the filename and skills."""
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    semantic_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    semantic_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resume_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    job_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    matched_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    missing_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")
