from app.services.matcher import match_skills


def test_skill_matching():
    result = match_skills(
        ["python", "sql", "pandas"],
        ["python", "sql", "aws"],
    )
    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["aws"]
    assert result["score"] == 66.67


def test_no_recognized_job_skills():
    result = match_skills(["python"], [])
    assert result["score"] == 0.0
    assert result["total_required"] == 0
