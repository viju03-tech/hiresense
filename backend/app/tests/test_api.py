"""API tests: auth, anonymous + logged-in analysis, history, reports."""
import io

import fitz
from fastapi.testclient import TestClient

from app.core.database import Base, engine
from app.main import app

client = TestClient(app)


def _pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)
    return bytes(doc.tobytes())


def _register(email="test@example.com"):
    r = client.post("/api/auth/register", json={"name": "Test", "email": email, "password": "password123"})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_health():
    assert client.get("/api/health").status_code == 200


def test_register_and_login():
    token = _register("a@example.com")
    r = client.post("/api/auth/login", json={"email": "a@example.com", "password": "password123"})
    assert r.status_code == 200
    assert r.json()["access_token"]
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == "a@example.com"


def test_duplicate_register():
    _register("dup@example.com")
    r = client.post("/api/auth/register", json={"name": "X", "email": "dup@example.com", "password": "password123"})
    assert r.status_code == 400


def test_anonymous_analysis_not_saved():
    pdf = _pdf_bytes("Python developer with pandas and SQL experience.")
    r = client.post("/api/analyze-upload",
                    files={"file": ("resume.pdf", io.BytesIO(pdf), "application/pdf")},
                    data={"job_description": "We need Python, pandas and Docker."})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["score"] == 66.67
    assert "docker" in data["missing_skills"]
    assert data["semantic_score"] is not None
    assert data["recommendations"]
    assert data["saved"] is False


def test_fake_pdf_rejected():
    r = client.post("/api/analyze-upload",
                    files={"file": ("resume.pdf", io.BytesIO(b"not a pdf at all"), "application/pdf")},
                    data={"job_description": "Python"})
    assert r.status_code == 400


def test_logged_in_analysis_history_and_reports():
    token = _register("b@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    pdf = _pdf_bytes("Python developer with pandas experience.")
    r = client.post("/api/analyze-upload",
                    files={"file": ("resume.pdf", io.BytesIO(pdf), "application/pdf")},
                    data={"job_description": "We need Python and Docker."},
                    headers=headers)
    assert r.status_code == 200, r.text
    aid = r.json()["id"]
    assert aid

    r = client.get("/api/history", headers=headers)
    assert r.status_code == 200
    assert r.json()["count"] == 1

    r = client.get(f"/api/analysis/{aid}", headers=headers)
    assert r.status_code == 200

    r = client.get(f"/api/analysis/{aid}/report.csv", headers=headers)
    assert r.status_code == 200
    assert "docker" in r.text

    r = client.get(f"/api/analysis/{aid}/report.pdf", headers=headers)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:4] == b"%PDF"

    r = client.delete(f"/api/analysis/{aid}", headers=headers)
    assert r.status_code == 200
    r = client.get("/api/history", headers=headers)
    assert r.json()["count"] == 0


def test_history_requires_login():
    assert client.get("/api/history").status_code == 401
