def analyze_resume(resume_skills, job_skills):
    
    matched = set(resume_skills) & set(job_skills)
    
    match_score = len(matched) / len(job_skills) if job_skills else 0
    
    missing_skills = list(set(job_skills) - set(resume_skills))
    
    probability = match_score * 1.1
    if probability > 1:
        probability = 1
    
    return {
        "match_score": match_score,
        "missing_skills": missing_skills,
        "probability": probability,
        "learning_path": missing_skills
    }