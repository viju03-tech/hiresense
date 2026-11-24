def calculate_skill_score(resume_skills: list[str], job_skills: list[str]) -> float:
    required = set(job_skills)
    if not required:
        return 0.0
    matched = set(resume_skills) & required
    return round((len(matched) / len(required)) * 100, 2)
