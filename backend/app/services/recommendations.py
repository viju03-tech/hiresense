"""Evidence-grounded recommendations for missing skills.

Only skills that actually appear in the job description are recommended.
Each entry links to a real, free, official learning resource — no invented
skills, courses, or credentials are ever generated.
"""
import re

RESOURCES: dict[str, dict] = {
    "python": {"resource": "Python official tutorial", "url": "https://docs.python.org/3/tutorial/"},
    "sql": {"resource": "SQLBolt interactive SQL lessons", "url": "https://sqlbolt.com/"},
    "javascript": {"resource": "MDN JavaScript guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"},
    "typescript": {"resource": "TypeScript handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html"},
    "react": {"resource": "React official docs", "url": "https://react.dev/learn"},
    "next.js": {"resource": "Next.js learn course", "url": "https://nextjs.org/learn"},
    "node.js": {"resource": "Node.js official guides", "url": "https://nodejs.org/en/learn"},
    "fastapi": {"resource": "FastAPI tutorial", "url": "https://fastapi.tiangolo.com/tutorial/"},
    "django": {"resource": "Django official tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/"},
    "flask": {"resource": "Flask tutorial", "url": "https://flask.palletsprojects.com/en/stable/tutorial/"},
    "machine learning": {"resource": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
    "deep learning": {"resource": "DeepLearning.AI free courses", "url": "https://www.deeplearning.ai/courses/"},
    "data science": {"resource": "Kaggle Learn (free)", "url": "https://www.kaggle.com/learn"},
    "pandas": {"resource": "pandas user guide", "url": "https://pandas.pydata.org/docs/user_guide/index.html"},
    "numpy": {"resource": "NumPy quickstart", "url": "https://numpy.org/doc/stable/user/quickstart.html"},
    "scikit-learn": {"resource": "scikit-learn user guide", "url": "https://scikit-learn.org/stable/user_guide.html"},
    "tensorflow": {"resource": "TensorFlow tutorials", "url": "https://www.tensorflow.org/tutorials"},
    "pytorch": {"resource": "PyTorch tutorials", "url": "https://pytorch.org/tutorials/"},
    "nlp": {"resource": "Hugging Face NLP course", "url": "https://huggingface.co/learn/nlp-course"},
    "computer vision": {"resource": "OpenCV tutorials", "url": "https://docs.opencv.org/4.x/d9/df8/tutorial_root.html"},
    "docker": {"resource": "Docker getting started", "url": "https://docs.docker.com/get-started/"},
    "kubernetes": {"resource": "Kubernetes basics", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/"},
    "aws": {"resource": "AWS Skill Builder (free tier)", "url": "https://skillbuilder.aws/"},
    "git": {"resource": "Pro Git book (free)", "url": "https://git-scm.com/book/en/v2"},
    "postgresql": {"resource": "PostgreSQL tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html"},
    "power bi": {"resource": "Microsoft Power BI guided learning", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"},
    "tableau": {"resource": "Tableau free training", "url": "https://www.tableau.com/learn/training"},
    "excel": {"resource": "Microsoft Excel support & training", "url": "https://support.microsoft.com/en-us/excel"},
    "cybersecurity": {"resource": "Google Cybersecurity Certificate (Coursera)", "url": "https://www.coursera.org/professional-certificates/google-cybersecurity"},
}

GENERIC = {"resource": "Search the official documentation for this skill", "url": "https://duckduckgo.com/"}


def build_recommendations(missing_skills: list[str], job_description: str) -> list[dict]:
    """One recommendation per missing skill, with evidence from the JD."""
    jd = (job_description or "").lower()
    out = []
    for skill in missing_skills:
        # Evidence: how many times the skill (or its name) appears in the JD.
        mentions = len(re.findall(re.escape(skill), jd)) or 1
        info = RESOURCES.get(skill, GENERIC)
        out.append({
            "skill": skill,
            "evidence": f"Appears in the job description ({mentions} mention{'s' if mentions != 1 else ''}) but was not found in the resume.",
            "suggestion": f"Add a project or experience that demonstrates {skill}, or complete a short course and list it.",
            "resource": info["resource"],
            "url": info["url"],
        })
    return out
