def calculate_career_readiness(ats_score: int, job_match_score: int, skill_gap_count: int, project_count: int) -> int:
    """
    Calculates an overall Career Readiness Score (0-100).
    Factors:
    - ATS Score (40% weight)
    - Job Match Score (30% weight)
    - Skill Gap Impact (20% weight)
    - Project Experience (10% weight)
    """
    # ATS contribution (max 40)
    ats_contribution = (ats_score / 100) * 40
    
    # Job Match contribution (max 30)
    job_contribution = (job_match_score / 100) * 30
    
    # Skill Gap penalty (max 20)
    # Assume 0 gaps = full 20 points, 10+ gaps = 0 points
    gap_score = max(0, 20 - (skill_gap_count * 2))
    
    # Projects contribution (max 10)
    # Assume 3+ projects = full 10 points
    project_score = min(10, project_count * 3.33)
    
    total_score = int(ats_contribution + job_contribution + gap_score + project_score)
    return min(100, max(0, total_score))
