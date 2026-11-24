from app.services.skill_extractor import extract_skills, extract_skills_by_category
from app.services.semantic_matcher import semantic_similarity
from app.services.recommendations import build_recommendations


def test_aliases_map_to_canonical():
    skills = extract_skills("I know golang, ReactJS and scikit learn.")
    assert "go" in skills
    assert "react" in skills
    assert "scikit-learn" in skills


def test_taxonomy_is_large():
    from app.services.skill_extractor import SKILLS
    assert len(SKILLS) >= 90


def test_by_category():
    cats = extract_skills_by_category("Python, pandas and Docker.")
    assert cats["Languages"] == ["python"]
    assert "docker" in cats.get("Cloud & DevOps", [])


def test_semantic_tfidf():
    r = semantic_similarity("python pandas machine learning", "python pandas data science")
    assert r["method"] in ("tfidf", "word-overlap", "sentence-transformers")
    assert 0 <= r["score"] <= 100
    assert semantic_similarity("", "python")["score"] == 0.0


def test_recommendations_only_for_missing():
    recs = build_recommendations(["docker"], "We need Docker and Kubernetes experience.")
    assert len(recs) == 1
    assert recs[0]["skill"] == "docker"
    assert recs[0]["url"].startswith("http")
    assert "job description" in recs[0]["evidence"]
