from app.services.scorer import calculate_skill_score


def match_skills(resume_skills: list[str], job_skills: list[str]) -> dict:
    resume_set = set(resume_skills)
    required = list(dict.fromkeys(job_skills))
    matched = [skill for skill in required if skill in resume_set]
    missing = [skill for skill in required if skill not in resume_set]
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "total_required": len(required),
        "score": calculate_skill_score(resume_skills, required),
    }
