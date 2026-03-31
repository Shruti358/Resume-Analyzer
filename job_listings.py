"""Sample job catalog for recommendations (skills used for ranking; not shown in UI)."""

import pandas as pd

# skills: comma-separated tokens matched against extract_skills() output
JOBS_RECORDS = [
    {
        "Job Title": "Data Scientist",
        "Company Name": "Affinity Solutions",
        "Location": "New York, NY",
        "Industry": "Advertising & Marketing",
        "skills": "python,machine learning,pandas,numpy,data analysis,sql",
    },
    {
        "Job Title": "Healthcare Data Scientist",
        "Company Name": "Tecolote Research",
        "Location": "Albuquerque, NM",
        "Industry": "Aerospace & Defense",
        "skills": "python,machine learning,data analysis,sql,r",
    },
    {
        "Job Title": "Data Scientist",
        "Company Name": "KnowBe4",
        "Location": "Clearwater, FL",
        "Industry": "Security Services",
        "skills": "python,machine learning,sql,data analysis",
    },
    {
        "Job Title": "Data Scientist",
        "Company Name": "PNNL",
        "Location": "Richland, WA",
        "Industry": "Energy",
        "skills": "python,machine learning,deep learning,tensorflow,data analysis",
    },
    {
        "Job Title": "Healthcare Data Scientist",
        "Company Name": "University of Maryland Medical System",
        "Location": "Linthicum, MD",
        "Industry": "Health Care Services",
        "skills": "python,r,machine learning,data analysis,sql",
    },
]


def load_jobs_df() -> pd.DataFrame:
    return pd.DataFrame(JOBS_RECORDS)


def rank_jobs_by_resume_skills(resume_skills: list[str], jobs: pd.DataFrame) -> pd.DataFrame:
    """Rank jobs by overlap between resume skills and each job's skill set."""
    resume_set = {s.lower().strip() for s in resume_skills if s}
    scores: list[float] = []
    for _, row in jobs.iterrows():
        raw = row["skills"]
        if isinstance(raw, str):
            job_skills = {t.strip().lower() for t in raw.split(",") if t.strip()}
        else:
            job_skills = set()
        if not job_skills:
            scores.append(0.0)
            continue
        matched = resume_set & job_skills
        scores.append(len(matched) / len(job_skills))
    out = jobs.copy()
    out["_score"] = scores
    out = out.sort_values("_score", ascending=False, kind="mergesort")
    return out.drop(columns=["skills", "_score"]).reset_index(drop=True)
