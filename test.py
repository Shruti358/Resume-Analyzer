from utils import extract_skills
from ml_model import analyze_resume

# Sample data
resume_text = "I know Python and Pandas"
job_text = "Looking for Python, SQL, Machine Learning"

# Extract skills
resume_skills = extract_skills(resume_text)
job_skills = extract_skills(job_text)

print("Resume Skills:", resume_skills)
print("Job Skills:", job_skills)

# Analyze
result = analyze_resume(resume_skills, job_skills)

print("\nFinal Result:")
print(result)