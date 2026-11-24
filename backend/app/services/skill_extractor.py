"""Skill extraction against a larger taxonomy with aliases and categories.

Canonical skill -> (category, [aliases]). Aliases are matched case-insensitively
with word boundaries; the canonical name is what is returned, so downstream
matching stays stable. ~100 canonical skills.
"""
import re

TAXONOMY: dict[str, tuple[str, list[str]]] = {
    "python": ("Languages", ["py", "python3"]),
    "java": ("Languages", ["java se", "java ee"]),
    "c": ("Languages", []),
    "c++": ("Languages", ["cpp", "c plus plus"]),
    "c#": ("Languages", ["csharp", "c sharp"]),
    "javascript": ("Languages", ["js", "ecmascript"]),
    "typescript": ("Languages", ["ts"]),
    "go": ("Languages", ["golang"]),
    "rust": ("Languages", []),
    "ruby": ("Languages", []),
    "php": ("Languages", []),
    "swift": ("Languages", []),
    "kotlin": ("Languages", []),
    "scala": ("Languages", []),
    "r": ("Languages", ["r programming"]),
    "sql": ("Languages", ["structured query language"]),
    "html": ("Languages", ["html5"]),
    "css": ("Languages", ["css3"]),
    "bash": ("Languages", ["shell scripting", "shell"]),
    "machine learning": ("Data & AI", ["ml", "machine-learning"]),
    "deep learning": ("Data & AI", ["dl"]),
    "data science": ("Data & AI", ["data-science"]),
    "data analysis": ("Data & AI", ["data analytics"]),
    "nlp": ("Data & AI", ["natural language processing"]),
    "computer vision": ("Data & AI", ["cv"]),
    "pandas": ("Data & AI", []),
    "numpy": ("Data & AI", []),
    "scikit-learn": ("Data & AI", ["sklearn", "scikit learn"]),
    "tensorflow": ("Data & AI", ["tf", "keras"]),
    "pytorch": ("Data & AI", ["torch"]),
    "opencv": ("Data & AI", []),
    "matplotlib": ("Data & AI", []),
    "seaborn": ("Data & AI", []),
    "statistics": ("Data & AI", ["statistical analysis"]),
    "power bi": ("Data & AI", ["powerbi"]),
    "tableau": ("Data & AI", []),
    "excel": ("Data & AI", ["microsoft excel", "spreadsheets"]),
    "spark": ("Data & AI", ["apache spark", "pyspark"]),
    "hadoop": ("Data & AI", []),
    "airflow": ("Data & AI", ["apache airflow"]),
    "etl": ("Data & AI", ["extract transform load"]),
    "llm": ("Data & AI", ["large language models", "generative ai", "genai"]),
    "prompt engineering": ("Data & AI", []),
    "transformers": ("Data & AI", ["hugging face"]),
    "mlops": ("Data & AI", ["ml ops"]),
    "feature engineering": ("Data & AI", []),
    "a/b testing": ("Data & AI", ["ab testing"]),
    "react": ("Web", ["react.js", "reactjs"]),
    "next.js": ("Web", ["nextjs", "next js"]),
    "angular": ("Web", ["angularjs"]),
    "vue": ("Web", ["vue.js", "vuejs"]),
    "node.js": ("Web", ["nodejs", "node"]),
    "fastapi": ("Web", []),
    "flask": ("Web", []),
    "django": ("Web", []),
    "express": ("Web", ["express.js"]),
    "spring": ("Web", ["spring boot"]),
    "laravel": ("Web", []),
    "tailwind": ("Web", ["tailwind css", "tailwindcss"]),
    "bootstrap": ("Web", []),
    "rest api": ("Web", ["restful api", "rest apis", "rest"]),
    "graphql": ("Web", []),
    "websocket": ("Web", ["websockets"]),
    "flutter": ("Mobile", []),
    "react native": ("Mobile", []),
    "android": ("Mobile", ["android development"]),
    "ios": ("Mobile", ["ios development"]),
    "postgresql": ("Databases", ["postgres", "psql"]),
    "mysql": ("Databases", []),
    "mongodb": ("Databases", ["mongo"]),
    "redis": ("Databases", []),
    "sqlite": ("Databases", []),
    "oracle": ("Databases", []),
    "elasticsearch": ("Databases", ["elastic search"]),
    "database design": ("Databases", []),
    "aws": ("Cloud & DevOps", ["amazon web services"]),
    "azure": ("Cloud & DevOps", ["microsoft azure"]),
    "gcp": ("Cloud & DevOps", ["google cloud", "google cloud platform"]),
    "docker": ("Cloud & DevOps", ["containerization"]),
    "kubernetes": ("Cloud & DevOps", ["k8s"]),
    "terraform": ("Cloud & DevOps", []),
    "jenkins": ("Cloud & DevOps", []),
    "ci/cd": ("Cloud & DevOps", ["continuous integration", "continuous deployment"]),
    "git": ("Cloud & DevOps", ["github", "gitlab", "version control"]),
    "linux": ("Cloud & DevOps", ["unix"]),
    "nginx": ("Cloud & DevOps", []),
    "devops": ("Cloud & DevOps", []),
    "microservices": ("Cloud & DevOps", ["micro services"]),
    "cybersecurity": ("Security", ["cyber security", "infosec"]),
    "penetration testing": ("Security", ["pentesting", "pen testing"]),
    "network security": ("Security", []),
    "owasp": ("Security", []),
    "encryption": ("Security", []),
    "pytest": ("Testing", []),
    "unit testing": ("Testing", ["unit tests"]),
    "jest": ("Testing", []),
    "selenium": ("Testing", []),
    "cypress": ("Testing", []),
    "tdd": ("Testing", ["test driven development"]),
    "figma": ("Design", ["ui/ux", "ui ux", "ux design"]),
    "jira": ("Tools", ["agile", "scrum"]),
    "agile": ("Tools", ["scrum"]),
    "project management": ("Tools", []),
    "communication": ("Soft Skills", []),
    "leadership": ("Soft Skills", []),
    "teamwork": ("Soft Skills", ["collaboration"]),
    "problem solving": ("Soft Skills", ["analytical thinking"]),
}

SKILLS = list(TAXONOMY.keys())

_PATTERNS: list[tuple[str, re.Pattern]] = []
for canonical, (_cat, aliases) in TAXONOMY.items():
    terms = sorted([canonical] + aliases, key=len, reverse=True)
    for term in terms:
        _PATTERNS.append((canonical, re.compile(r"(?<![\w])" + re.escape(term) + r"(?![\w])")))


def extract_skills(text: str) -> list[str]:
    normalized = (text or "").lower()
    found: set[str] = set()
    for canonical, pattern in _PATTERNS:
        if pattern.search(normalized):
            found.add(canonical)
    return [s for s in SKILLS if s in found]


def extract_skills_by_category(text: str) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for skill in extract_skills(text):
        out.setdefault(TAXONOMY[skill][0], []).append(skill)
    return out


def skill_category(skill: str) -> str:
    return TAXONOMY.get(skill, ("Other", []))[0]
