"""Database setup. SQLite is the default so the project runs with zero
setup; set DATABASE_URL to a PostgreSQL URL to use Postgres instead
(e.g. via docker compose up -d db)."""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./hiresense.db",
)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models import entities  # noqa: F401  (register models)

    Base.metadata.create_all(bind=engine)
