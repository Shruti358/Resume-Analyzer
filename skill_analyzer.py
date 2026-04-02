"""
Skill Analysis Module - Compare resume skills with job description
Calculate match percentages and provide recommendations
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class SkillAnalyzer:
    """Analyze skills and provide recommendations"""
    
    # Learning resources database
    LEARNING_RESOURCES = {
        "python": {
            "youtube": "https://www.youtube.com/watch?v=_uQrJ0TkSuc",
            "youtube_title": "Python for Everybody - Full Course",
            "resource": "https://www.codecademy.com/learn/learn-python",
            "resource_title": "Codecademy - Learn Python"
        },
        "javascript": {
            "youtube": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
            "youtube_title": "JavaScript Crash Course - Traversy Media",
            "resource": "https://www.codecademy.com/learn/introduction-to-javascript",
            "resource_title": "Codecademy - JavaScript Basics"
        },
        "typescript": {
            "youtube": "https://www.youtube.com/watch?v=BCg4perUb7w",
            "youtube_title": "TypeScript Tutorial - Full Course",
            "resource": "https://www.typescriptlang.org/docs/",
            "resource_title": "Official TypeScript Documentation"
        },
        "react": {
            "youtube": "https://www.youtube.com/watch?v=9u-_-cBaevo",
            "youtube_title": "React.js Tutorial for Beginners",
            "resource": "https://react.dev/learn",
            "resource_title": "Official React Documentation"
        },
        "angular": {
            "youtube": "https://www.youtube.com/watch?v=0LhBvp8qpro",
            "youtube_title": "Angular Full Course",
            "resource": "https://angular.io/guide/setup-local",
            "resource_title": "Angular Official Guide"
        },
        "vue.js": {
            "youtube": "https://www.youtube.com/watch?v=FXpIoQ_rT_c",
            "youtube_title": "Vue.js Tutorial - Full Course",
            "resource": "https://vuejs.org/guide/introduction.html",
            "resource_title": "Vue.js Official Guide"
        },
        "node.js": {
            "youtube": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
            "youtube_title": "Node.js Tutorial for Beginners",
            "resource": "https://nodejs.org/en/docs/",
            "resource_title": "Node.js Documentation"
        },
        "django": {
            "youtube": "https://www.youtube.com/watch?v=rHux0gMZ3Eg",
            "youtube_title": "Django for Beginners",
            "resource": "https://www.djangoproject.com/start/",
            "resource_title": "Django Getting Started"
        },
        "flask": {
            "youtube": "https://www.youtube.com/watch?v=Wfng6nTI84E",
            "youtube_title": "Flask by Example - Miguel Grinberg",
            "resource": "https://flask.palletsprojects.com/",
            "resource_title": "Flask Official Documentation"
        },
        "aws": {
            "youtube": "https://www.youtube.com/watch?v=r4G-m2QR6SQ",
            "youtube_title": "AWS Full Course for Beginners",
            "resource": "https://aws.amazon.com/getting-started/",
            "resource_title": "AWS Getting Started"
        },
        "azure": {
            "youtube": "https://www.youtube.com/watch?v=iJKW5oSQmIs",
            "youtube_title": "Azure for Beginners",
            "resource": "https://learn.microsoft.com/en-us/azure/",
            "resource_title": "Microsoft Azure Learning"
        },
        "docker": {
            "youtube": "https://www.youtube.com/watch?v=3c-iBn73dRM",
            "youtube_title": "Docker Tutorial for Beginners",
            "resource": "https://docs.docker.com/get-started/",
            "resource_title": "Docker Official Documentation"
        },
        "kubernetes": {
            "youtube": "https://www.youtube.com/watch?v=X48VuDVv0Z0",
            "youtube_title": "Kubernetes for Beginners",
            "resource": "https://kubernetes.io/docs/tutorials/",
            "resource_title": "Kubernetes Tutorials"
        },
        "git": {
            "youtube": "https://www.youtube.com/watch?v=RRvYo5Z51Ss",
            "youtube_title": "Git & GitHub Crash Course",
            "resource": "https://git-scm.com/book/en/v2",
            "resource_title": "Pro Git Book"
        },
        "sql": {
            "youtube": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "youtube_title": "SQL Tutorial for Beginners",
            "resource": "https://www.w3schools.com/sql/",
            "resource_title": "W3Schools SQL Tutorial"
        },
        "mongodb": {
            "youtube": "https://www.youtube.com/watch?v=ofme2o29ngU",
            "youtube_title": "MongoDB Crash Course",
            "resource": "https://docs.mongodb.com/manual/",
            "resource_title": "MongoDB Official Documentation"
        },
        "machine learning": {
            "youtube": "https://www.youtube.com/watch?v=aircAruvnKk",
            "youtube_title": "Machine Learning Crash Course",
            "resource": "https://developers.google.com/machine-learning/crash-course",
            "resource_title": "Google ML Crash Course"
        },
        "tensorflow": {
            "youtube": "https://www.youtube.com/watch?v=tPYj3fFJGjk",
            "youtube_title": "TensorFlow 2.0 Complete Course",
            "resource": "https://www.tensorflow.org/tutorials",
            "resource_title": "TensorFlow Official Tutorials"
        },
        "pytorch": {
            "youtube": "https://www.youtube.com/watch?v=EMXfZB8FVUA",
            "youtube_title": "PyTorch Tutorial for Beginners",
            "resource": "https://pytorch.org/tutorials/",
            "resource_title": "PyTorch Official Tutorials"
        },
        "system design": {
            "youtube": "https://www.youtube.com/watch?v=UzLRB4IIcL4",
            "youtube_title": "System Design Interview Course",
            "resource": "https://www.educative.io/courses/grokking-the-system-design-interview",
            "resource_title": "Educative - System Design Interview"
        },
        "ci/cd": {
            "youtube": "https://www.youtube.com/watch?v=scEDHE3B4Mw",
            "youtube_title": "CI/CD with GitHub Actions",
            "resource": "https://docs.github.com/en/actions",
            "resource_title": "GitHub Actions Documentation"
        },
        "rest api": {
            "youtube": "https://www.youtube.com/watch?v=lsMQRaeKNUI",
            "youtube_title": "REST API Tutorial",
            "resource": "https://www.restapitutorial.com/",
            "resource_title": "REST API Tutorial"
        },
        "microservices": {
            "youtube": "https://www.youtube.com/watch?v=mPma-YIEUqc",
            "youtube_title": "Microservices Architecture",
            "resource": "https://microservices.io/",
            "resource_title": "Microservices.io"
        },
        "agile": {
            "youtube": "https://www.youtube.com/watch?v=Z9QbYZh1fXM",
            "youtube_title": "Agile Methodology Tutorial",
            "resource": "https://www.agilealliance.org/agile101/",
            "resource_title": "Agile Alliance - Agile 101"
        },
        "scrum": {
            "youtube": "https://www.youtube.com/watch?v=p1--8gKrMNs",
            "youtube_title": "Scrum for Beginners",
            "resource": "https://scrumguides.org/",
            "resource_title": "Official Scrum Guide"
        },
        "data analysis": {
            "youtube": "https://www.youtube.com/watch?v=vmEHY5-riNE",
            "youtube_title": "Data Analysis with Python",
            "resource": "https://www.kaggle.com/learn/data-cleaning",
            "resource_title": "Kaggle - Data Analysis"
        },
        "deep learning": {
            "youtube": "https://www.youtube.com/watch?v=aircAruvnKk",
            "youtube_title": "Deep Learning Specialization",
            "resource": "https://www.deeplearning.ai/",
            "resource_title": "DeepLearning.AI Courses"
        }
    }
    
    @staticmethod
    def extract_skills_from_text(text: str) -> List[str]:
        """Extract skill keywords from job description"""
        skills = []
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Technical keywords to search for
        skill_keywords = [
            "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust", "kotlin",
            "typescript", "react", "angular", "vue.js", "vue", "django", "flask", "node.js",
            "express", "spring", "asp.net", "laravel", "fastapi",
            "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb",
            "aws", "azure", "google cloud", "gcp", "heroku", "docker", "kubernetes",
            "git", "github", "gitlab", "jenkins", "ci/cd",
            "machine learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
            "linux", "windows", "nginx", "apache",
            "rest api", "graphql", "microservices", "system design",
            "agile", "scrum", "jira", "testing", "unit testing", "selenium",
            "data analysis", "big data", "spark", "hadoop",
            "devops", "terraform", "ansible", "deep learning", "nlp"
        ]
        
        for skill in skill_keywords:
            # Use word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                skills.append(skill)
        
        return skills
    
    @staticmethod
    def match_skills(
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Tuple[List[str], List[str], List[str], int]:
        """
        Compare resume skills with job description skills
        
        Returns:
            - matched_skills: Skills in both resume and job description
            - missing_skills: Skills in job description but not in resume
            - extra_skills: Skills in resume but not in job description
            - match_percentage: Percentage of job skills found in resume
        """
        
        # Normalize for comparison (lowercase)
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matched = []
        missing = []
        extra = set(resume_skills)
        
        for job_skill in job_skills:
            job_skill_lower = job_skill.lower()
            
            found = False
            for resume_skill in resume_skills:
                if resume_skill.lower() == job_skill_lower:
                    if job_skill not in matched:
                        matched.append(job_skill)
                    if resume_skill in extra:
                        extra.discard(resume_skill)
                    found = True
                    break
            
            if not found and job_skill not in missing:
                missing.append(job_skill)
        
        # Calculate match percentage
        if len(job_skills) > 0:
            match_percentage = int((len(matched) / len(job_skills)) * 100)
        else:
            match_percentage = 0
        
        return matched, missing, list(extra), match_percentage
    
    @staticmethod
    def get_learning_resources(skill: str) -> Optional[Dict]:
        """Get learning resources for a skill"""
        skill_lower = skill.lower()
        
        # Direct match
        if skill_lower in SkillAnalyzer.LEARNING_RESOURCES:
            return SkillAnalyzer.LEARNING_RESOURCES[skill_lower]
        
        # Try partial match
        for key in SkillAnalyzer.LEARNING_RESOURCES:
            if key in skill_lower or skill_lower in key:
                return SkillAnalyzer.LEARNING_RESOURCES[key]
        
        # Default resource if not found
        return {
            "youtube": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}",
            "youtube_title": f"Search YouTube for {skill}",
            "resource": f"https://www.google.com/search?q={skill.replace(' ', '+')}+tutorial",
            "resource_title": f"Google Search for {skill} Tutorial"
        }
    
    @staticmethod
    def recommend_skills(
        missing_skills: List[str],
        max_recommendations: int = 5
    ) -> List[Dict]:
        """Generate learning recommendations for missing skills"""
        
        # Prioritize skills (more common/valuable first)
        priority_skills = [
            "typescript", "aws", "system design", "kubernetes", "docker",
            "machine learning", "tensorflow", "ci/cd", "microservices",
            "react", "node.js", "sql"
        ]
        
        # Sort missing skills by priority
        sorted_missing = []
        
        # Add priority skills first
        for priority_skill in priority_skills:
            for missing_skill in missing_skills:
                if missing_skill.lower() == priority_skill:
                    sorted_missing.append(missing_skill)
                    break
        
        # Add remaining skills
        for missing_skill in missing_skills:
            if missing_skill not in sorted_missing:
                sorted_missing.append(missing_skill)
        
        # Generate recommendations
        recommendations = []
        for skill in sorted_missing[:max_recommendations]:
            resources = SkillAnalyzer.get_learning_resources(skill)
            recommendations.append({
                "skill": skill,
                "youtube": resources.get("youtube"),
                "youtube_title": resources.get("youtube_title"),
                "resource": resources.get("resource"),
                "resource_title": resources.get("resource_title")
            })
        
        return recommendations


class ResumeAnalyzer:
    """Complete resume analysis combining parsing and skill analysis"""
    
    def __init__(self):
        self.skill_analyzer = SkillAnalyzer()
    
    def analyze(
        self,
        resume_data: Dict,
        job_description: str = ""
    ) -> Dict:
        """
        Complete resume analysis
        
        Args:
            resume_data: Parsed resume data from ResumeParser
            job_description: Job description text for comparison
        
        Returns:
            Structured analysis result in required JSON format
        """
        
        # Extract skills from job description
        job_skills = SkillAnalyzer.extract_skills_from_text(job_description)
        resume_skills = resume_data.get('skills', [])
        
        # Analyze skill match
        matched, missing, extra, match_percentage = SkillAnalyzer.match_skills(
            resume_skills,
            job_skills if job_skills else resume_skills
        )
        
        # Get recommendations
        recommendations = SkillAnalyzer.recommend_skills(missing)
        
        # Build learning resources map
        learning_resources = {}
        for rec in recommendations:
            skill = rec['skill']
            learning_resources[skill] = {
                "youtube": rec['youtube'],
                "youtube_title": rec['youtube_title'],
                "resource": rec['resource'],
                "resource_title": rec['resource_title']
            }
        
        # Build the response
        response = {
            "basic_info": resume_data.get('basic_info', {}),
            "education": resume_data.get('education', []),
            "experience": resume_data.get('experience', []),
            "skills": {
                "extracted": resume_skills,
                "matched": matched,
                "missing": missing,
                "extra": extra
            },
            "match_percentage": match_percentage,
            "job_skills_detected": job_skills,
            "recommendations": [
                {
                    "skill": rec['skill'],
                    "priority": "high" if i < 3 else "medium"
                }
                for i, rec in enumerate(recommendations)
            ],
            "resume_stats": {
                "pages": resume_data.get('pages', 0),
                "skills_count": len(resume_skills),
                "education_count": len(resume_data.get('education', [])),
                "experience_count": len(resume_data.get('experience', []))
            },
            "learning_resources": learning_resources
        }
        
        return response
    
    def to_json(self, analysis_result: Dict) -> str:
        """Convert analysis to JSON string"""
        return json.dumps(analysis_result, indent=2)
