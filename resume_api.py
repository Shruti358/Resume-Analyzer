"""
Resume Analyzer API Module
Provides programmatic access to resume analysis functionality
Returns strict JSON format as specified
"""

import json
from typing import Dict, Optional
from resume_parser import ResumeParser
from skill_analyzer import ResumeAnalyzer


class ResumeAnalysisAPI:
    """Main API for resume analysis"""
    
    def __init__(self):
        self.parser = ResumeParser()
        self.analyzer = ResumeAnalyzer()
    
    def analyze_resume_file(
        self,
        file_path: str,
        job_description: str = ""
    ) -> Dict:
        """
        Analyze a resume file and optionally compare with job description
        
        Args:
            file_path: Path to resume file (PDF or DOCX)
            job_description: Optional job description for comparison
        
        Returns:
            Structured JSON analysis result (strict format)
        """
        # Parse resume
        resume_data = self.parser.parse_full_resume(file_path)
        
        # Analyze
        analysis = self.analyzer.analyze(resume_data, job_description)
        
        # Return in strict JSON format
        return self._format_output(analysis)
    
    def _format_output(self, analysis: Dict) -> Dict:
        """
        Format output in strict JSON format as specified
        """
        return {
            "basic_info": {
                "name": analysis.get('basic_info', {}).get('name', 'Not Found'),
                "email": analysis.get('basic_info', {}).get('email', 'Not Found'),
                "phone": analysis.get('basic_info', {}).get('phone', 'Not Found')
            },
            "education": analysis.get('education', []),
            "skills": {
                "extracted": analysis.get('skills', {}).get('extracted', []),
                "matched": analysis.get('skills', {}).get('matched', []),
                "missing": analysis.get('skills', {}).get('missing', []),
                "extra": analysis.get('skills', {}).get('extra', [])
            },
            "match_percentage": analysis.get('match_percentage', 0),
            "recommendations": [
                {
                    "skill": rec.get('skill'),
                    "priority": rec.get('priority', 'medium')
                }
                for rec in analysis.get('recommendations', [])
            ],
            "resume_stats": {
                "pages": analysis.get('resume_stats', {}).get('pages', 0),
                "skills_count": analysis.get('resume_stats', {}).get('skills_count', 0),
                "education_count": analysis.get('resume_stats', {}).get('education_count', 0),
                "experience_count": analysis.get('resume_stats', {}).get('experience_count', 0)
            },
            "learning_resources": self._format_resources(
                analysis.get('learning_resources', {})
            )
        }
    
    def _format_resources(self, resources: Dict) -> Dict:
        """Format learning resources in strict format"""
        formatted = {}
        
        for skill, res in resources.items():
            formatted[skill] = {
                "youtube": res.get('youtube', ''),
                "resource": res.get('resource', '')
            }
        
        return formatted
    
    def get_json_string(self, file_path: str, job_description: str = "") -> str:
        """
        Analyze resume and return as JSON string
        """
        analysis = self.analyze_resume_file(file_path, job_description)
        return json.dumps(analysis, indent=2)


def analyze(file_path: str, job_description: str = "") -> Dict:
    """
    Convenient function to analyze resume
    
    Usage:
        result = analyze("/path/to/resume.pdf", "job description text")
    """
    api = ResumeAnalysisAPI()
    return api.analyze_resume_file(file_path, job_description)


def analyze_json(file_path: str, job_description: str = "") -> str:
    """
    Analyze resume and return JSON string
    
    Usage:
        json_result = analyze_json("/path/to/resume.pdf", "job description")
    """
    api = ResumeAnalysisAPI()
    return api.get_json_string(file_path, job_description)
