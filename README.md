# AI Resume Analyzer

A comprehensive, intelligent resume analysis system that extracts data from resumes, compares with job descriptions, and provides personalized learning recommendations.

## Features

### 🔹 1. Resume Data Extraction (STRICT & ACCURATE)
- ✅ Extract ONLY information present in the resume
- ✅ No assumptions or generalizations
- ✅ Full Name, Email, Phone Number
- ✅ Skills (technical + soft skills)
- ✅ Education (course name, degree, branch, university)
- ✅ Experience (if present)
- ✅ Returns "Not Found" for missing fields

### 🔹 2. Course Detection Issue Fixed
- ✅ Identifies courses ONLY from education section
- ✅ Lists all courses (no defaults or repetition)
- ✅ Returns "Not Mentioned" if no course found
- ✅ No hallucination or guessing

### 🔹 3. Skill Analysis (ACCURATE)
- ✅ Extracts skills from resume accurately
- ✅ Avoids repetition
- ✅ No irrelevant guesses
- ✅ Comprehensive technical skills database
- ✅ Soft skills detection

### 🔹 4. Job Description Comparison
- ✅ Compares resume skills with job description
- ✅ Matched Skills → presence in both resume and job
- ✅ Missing Skills → required in job but NOT in resume
- ✅ Extra Skills → in resume but NOT required

### 🔹 5. Skill Match Percentage
- ✅ Calculates: Match % = (Matched Skills / Total Job Required Skills) × 100
- ✅ Rounded to nearest integer
- ✅ Accurate calculation based on job requirements

### 🔹 6. Smart Skill Recommendations
- ✅ Recommends ONLY relevant missing skills from job description
- ✅ Prioritizes most important skills first
- ✅ No generic suggestions
- ✅ Based on job market demand

### 🔹 7. Resume Statistics (ACTUAL PAGE COUNT)
- ✅ Detects actual number of pages in uploaded resume
- ✅ NOT hardcoded (e.g., always 2)
- ✅ Works for both PDF and DOCX formats
- ✅ Accurate counting

### 🔹 8. Learning Resources (COMPREHENSIVE)
For each recommended skill:
- ✅ 1 YouTube video (relevant & beginner-friendly)
- ✅ 1 short learning resource (course/article)
- ✅ Direct links to resources
- ✅ Career-focused recommendations

### 🔹 9. Output Format (STRICT JSON)
```json
{
  "basic_info": {
    "name": "",
    "email": "",
    "phone": ""
  },
  "education": [],
  "experience": [],
  "skills": {
    "extracted": [],
    "matched": [],
    "missing": [],
    "extra": []
  },
  "match_percentage": "",
  "recommendations": [],
  "resume_stats": {
    "pages": ""
  },
  "learning_resources": {
    "skill_name": {
      "youtube": "",
      "resource": ""
    }
  }
}
```

### 🔹 10. Quality Rules
- ✅ NO hallucination of data
- ✅ NO repeated output for different resumes
- ✅ EVERYTHING resume-specific
- ✅ Accuracy over completeness

## Installation

### Requirements
- Python 3.8+
- Streamlit
- pandas
- plotly
- PyPDF2
- python-docx

### Setup

1. **Clone or download the project**
```bash
cd Resume-Analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements_modern.txt
```

3. **Run the application**
```bash
# On Windows (PowerShell)
.\run.bat

# On Windows (Command Prompt)
run.bat

# On macOS/Linux
bash run.sh

# Or directly with Streamlit
streamlit run app.py
```

## Usage

### Web Interface (Streamlit)

1. Open the application in your browser
2. Navigate to "📤 Upload Resume"
3. Upload a PDF or DOCX resume
4. Paste job description (optional but recommended)
5. Click "🔍 Analyze Resume"
6. View comprehensive analysis:
   - Extracted information
   - Skill matching
   - Match percentage
   - Recommendations
   - Learning resources

### Programmatic API Usage

```python
from resume_api import analyze, analyze_json

# Get analysis as dictionary
result = analyze("/path/to/resume.pdf", "job description text")

# Get analysis as JSON string
json_result = analyze_json("/path/to/resume.pdf", "job description text")

# Access specific data
name = result['basic_info']['name']
matched_skills = result['skills']['matched']
match_percentage = result['match_percentage']
recommendations = result['recommendations']
```

## Project Structure

```
Resume-Analyzer/
├── app.py                      # Main Streamlit application
├── resume_parser.py            # Resume file parsing module
├── skill_analyzer.py           # Skill analysis & job comparison
├── resume_api.py              # Programmatic API
├── config.json                 # Configuration
├── requirements_modern.txt     # Python dependencies
├── run.bat                     # Windows batch runner
├── run.sh                      # Linux/macOS shell runner
├── Uploaded_Resumes/          # Directory for uploaded files
└── README.md                   # This file
```

## Modules

### resume_parser.py
**ResumeParser Class**
- `parse_resume()` - Parse PDF or DOCX file
- `parse_pdf()` - Extract text from PDF
- `parse_docx()` - Extract text from DOCX
- `extract_name()` - Extract full name
- `extract_email()` - Extract email address
- `extract_phone()` - Extract phone number
- `extract_education()` - Extract education details
- `extract_skills()` - Extract technical skills
- `extract_experience()` - Extract work experience
- `get_page_count()` - Get actual page count
- `parse_full_resume()` - Complete parsing

### skill_analyzer.py
**SkillAnalyzer Class**
- `extract_skills_from_text()` - Extract skills from job description
- `match_skills()` - Compare resume vs job skills
- `get_learning_resources()` - Get learning resources for skill
- `recommend_skills()` - Generate recommendations

**ResumeAnalyzer Class**
- `analyze()` - Complete analysis
- `to_json()` - Convert to JSON

### resume_api.py
**ResumeAnalysisAPI Class**
- `analyze_resume_file()` - Analyze with job description
- Convenience functions: `analyze()`, `analyze_json()`

## Supported File Formats

- **PDF** (.pdf)
- **DOCX** (.docx) - Microsoft Word
- Max file size: 200MB

## Skills Database

The system includes recognition for:

**Programming Languages**
Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, TypeScript, Scala, Perl, R, MATLAB, Objective-C, Groovy, Haskell, Elixir

**Web Frameworks**
React, Vue.js, Angular, Django, Flask, Node.js, Express, Spring, ASP.NET, Laravel, FastAPI, Fastify, NestJS, Next.js, Nuxt.js, Ruby on Rails

**Databases**
SQL, MySQL, PostgreSQL, MongoDB, Redis, Cassandra, DynamoDB, Firebase, Oracle, SQLite, Elasticsearch, Neo4j, CouchDB, MariaDB

**Cloud Platforms**
AWS, Azure, Google Cloud, Heroku, Digital Ocean, Linode, CloudFlare, IBM Cloud, Oracle Cloud, Alibaba Cloud

**Tools & Platforms**
Git, Docker, Kubernetes, Jenkins, GitHub, GitLab, Bitbucket, JIRA, Slack, Linux, Windows, MacOS, Nginx, Apache, Terraform, Ansible

**Data & ML**
Machine Learning, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, Data Analysis, Statistical Analysis, Deep Learning, NLP, Computer Vision, Apache Spark, Hadoop, Big Data

**Soft Skills**
Communication, Leadership, Problem Solving, Team Work, Project Management, Agile, Scrum, Time Management, Critical Thinking, Collaboration, Presentation, Documentation

**Testing & QA**
Unit Testing, Integration Testing, Testing, QA, Selenium, Jest, Pytest, Mocha, Chai, JUnit

**DevOps**
CI/CD, System Design, Microservices, Scalability, High Availability, Performance Optimization, Security

## Learning Resources

The system provides personalized learning resources for:
- YouTube tutorials (beginner-friendly)
- Online courses and documentation
- Over 25+ skills with curated resources

## Features Highlights

✨ **Modern UI** - Beautiful glassmorphism design with animations
📊 **Interactive Charts** - Visual analytics of skill distribution
📥 **Export Options** - Download analysis as JSON or CSV
🎯 **Smart Recommendations** - Prioritized skill recommendations
📈 **Match Percentage** - Instant feedback on job fit
🔍 **Accurate Extraction** - No hallucination or assumptions
📚 **Learning Path** - Resources to acquire missing skills

## Quality Assurance

✅ No data hallucination
✅ Unique output for each resume
✅ Accurate page count detection
✅ Strict JSON format
✅ No hardcoded values
✅ Resume-specific analysis
✅ Accuracy over completeness

## Example Output

```json
{
  "basic_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-0123"
  },
  "education": [
    {
      "degree": "Bachelor of Science",
      "branch": "Computer Science",
      "university": "Stanford University"
    }
  ],
  "skills": {
    "extracted": ["Python", "JavaScript", "React", "SQL", "AWS"],
    "matched": ["Python", "JavaScript"],
    "missing": ["TypeScript", "Kubernetes"],
    "extra": ["SQL"]
  },
  "match_percentage": 40,
  "recommendations": [
    {
      "skill": "TypeScript",
      "priority": "high"
    }
  ],
  "resume_stats": {
    "pages": 1,
    "skills_count": 5,
    "education_count": 1,
    "experience_count": 2
  },
  "learning_resources": {
    "TypeScript": {
      "youtube": "https://www.youtube.com/watch?v=BCg4perUb7w",
      "resource": "https://www.typescriptlang.org/docs/"
    }
  }
}
```

## Troubleshooting

### Issue: "File not supported"
- **Solution**: Ensure the file is in PDF or DOCX format (.pdf or .docx extension)

### Issue: "No skills detected"
- **Solution**: Ensure skills are clearly mentioned in the resume (e.g., "Skills: Python, JavaScript")

### Issue: "Page count incorrect"
- **Solution**: This shouldn't happen. Please check the original file. DOCX page count is estimated from content length.

### Issue: "Email not found"
- **Solution**: Ensure email follows standard format (e.g., john@example.com)

## Contributing

To add more skills or learning resources:
1. Edit `TECHNICAL_SKILLS` dict in `resume_parser.py`
2. Edit `LEARNING_RESOURCES` dict in `skill_analyzer.py`
3. Ensure consistent naming and formatting

## License

This project is open source and available for educational purposes.

## Support

For issues or feature requests, please create an issue in the project repository.

---

**Version**: 2.0
**Last Updated**: 2024
**Author**: Resume Analyzer Team
