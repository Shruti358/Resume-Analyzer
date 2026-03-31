def analyze_resume(resume_skills, job_skills):
    """
    Analyze resume against job description.
    
    Args:
        resume_skills (list): Skills found in resume
        job_skills (list): Skills required for the job
    
    Returns:
        dict: Analysis results with match score, missing skills, and learning path
    """
    
    # Find matched skills
    matched = set(resume_skills) & set(job_skills)
    
    # Calculate match score
    match_score = len(matched) / len(job_skills) if job_skills else 0
    
    # Find missing skills
    missing_skills = list(set(job_skills) - set(resume_skills))
    
    # Calculate probability (with boost for high match)
    probability = min(match_score * 1.1, 1.0)
    
    # Create learning path ranked by priority
    learning_path = sorted(missing_skills)
    
    return {
        "match_score": match_score,
        "missing_skills": missing_skills,
        "probability": probability,
        "learning_path": learning_path,
        "matched_skills": list(matched),
        "total_job_skills": len(job_skills),
        "total_resume_skills": len(resume_skills)
    }