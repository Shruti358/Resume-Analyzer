"""Test script for Resume Analyzer"""

from utils import extract_skills
from ml_model import analyze_resume

def test_basic_analysis():
    """Test basic resume analysis"""
    
    print("=" * 50)
    print("🧪 Testing Resume Analyzer")
    print("=" * 50)
    
    # Sample data
    resume_text = "I have 5 years of experience with Python, Pandas, NumPy. I also know SQL and AWS."
    job_text = "We are looking for candidates with Python, SQL, Machine Learning, Deep Learning, and TensorFlow experience."
    
    print(f"\n📄 Resume: {resume_text}")
    print(f"\n💼 Job Description: {job_text}")
    
    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    
    print(f"\n✅ Resume Skills Found: {resume_skills}")
    print(f"✅ Job Skills Required: {job_skills}")
    
    # Analyze
    result = analyze_resume(resume_skills, job_skills)
    
    print("\n📊 Analysis Results:")
    print(f"  - Match Score: {int(result['match_score'] * 100)}%")
    print(f"  - Skills Matched: {len(result['matched_skills'])}")
    print(f"  - Missing Skills: {result['missing_skills']}")
    print(f"  - Confidence: {int(result['probability'] * 100)}%")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_basic_analysis()