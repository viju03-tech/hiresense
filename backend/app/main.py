import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analysis import router as analysis_router
from app.api.auth import router as auth_router
from app.api.history import router as history_router
from app.api.reports import router as reports_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="HireSense API",
    description="Resume and job-description skill comparison API",
    version="0.2.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in os.environ.get(
    "FRONTEND_ORIGIN", "http://localhost:3000").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

app.include_router(analysis_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(reports_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "service": "HireSense API"}


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "HireSense API"}
