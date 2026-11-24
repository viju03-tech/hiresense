"""Semantic similarity between resume text and job description.

Tries, in order:
1. sentence-transformers (all-MiniLM-L6-v2) if HIRESENSE_SEMANTIC_MODEL=1
   and the model loads (off by default so a cold start never downloads
   weights unexpectedly).
2. TF-IDF cosine similarity via scikit-learn — labelled "tfidf".
3. Plain word-overlap fallback if scikit-learn is missing.

Returns {score: 0-100, method: str}. A document-similarity signal only —
never a hiring score on its own.
"""
import os
import re

_WORD = re.compile(r"[a-z0-9][a-z0-9+\-#]*")


def _tokens(text: str) -> set[str]:
    return set(_WORD.findall((text or "").lower()))


def semantic_similarity(resume_text: str, job_text: str) -> dict:
    if not (resume_text or "").strip() or not (job_text or "").strip():
        return {"score": 0.0, "method": "none"}

    if os.environ.get("HIRESENSE_SEMANTIC_MODEL") == "1":
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity

            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            vectors = model.encode([resume_text[:8000], job_text[:8000]])
            value = float(cosine_similarity([vectors[0]], [vectors[1]])[0][0])
            return {"score": round(max(0.0, value) * 100, 2), "method": "sentence-transformers"}
        except Exception:
            pass

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vec = TfidfVectorizer(stop_words="english", max_features=5000)
        matrix = vec.fit_transform([resume_text, job_text])
        value = float(cosine_similarity(matrix[0], matrix[1])[0][0])
        return {"score": round(max(0.0, value) * 100, 2), "method": "tfidf"}
    except Exception:
        pass

    a, b = _tokens(resume_text), _tokens(job_text)
    if not a or not b:
        return {"score": 0.0, "method": "word-overlap"}
    return {"score": round(len(a & b) / len(a | b) * 100, 2), "method": "word-overlap"}
