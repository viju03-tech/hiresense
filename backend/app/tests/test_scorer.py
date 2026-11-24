from app.services.scorer import calculate_skill_score


def test_skill_score():
    assert calculate_skill_score(
        ["python", "sql"],
        ["python", "sql", "aws", "docker"],
    ) == 50.0


def test_empty_job_skills():
    assert calculate_skill_score(["python"], []) == 0.0
