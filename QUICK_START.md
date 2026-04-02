# 🚀 Quick Start Guide - Resume Analyzer

## Installation & Setup (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements_modern.txt
```

### Step 2: Run Tests (verify everything works)
```bash
python test_system.py
```

Expected output:
```
🎉 All tests passed! Ready to run:
   streamlit run app.py
```

### Step 3: Start the Application
```bash
# Easy way - Windows
run.bat

# Easy way - Linux/macOS
bash run.sh

# Or directly with Streamlit
streamlit run app.py
```

Open your browser: **http://localhost:8501**

---

## How to Use the Web Application

### Using the Resume Analyzer (Step-by-Step)

#### 1. **Upload Your Resume**
   - Click "📤 Upload Resume" in sidebar
   - Select PDF or DOCX file from your computer
   - File should be under 200MB

#### 2. **Add Job Description** (Optional but Recommended)
   - Paste the job description text
   - System will analyze skill requirements
   - Better recommendations when provided

#### 3. **Click "Analyze Resume"**
   - System analyzes and compares
   - Takes 2-5 seconds typically
   - Shows progress while analyzing

#### 4. **View the Dashboard**
   - See all extracted information
   - View skill match analysis
   - Check recommendations
   - Download learning resources

---

## Understanding Your Analysis Report

### 📊 Basic Information
Shows your contact details extracted from resume

### 🛠️ Extracted Skills
All technical and soft skills found in your resume

### ✅ Matched Skills
Skills that appear in both your resume and job description

### ❌ Missing Skills
Skills required in the job but not in your resume

### 📈 Match Percentage
Your resume skill alignment with the job
- **90-100%**: Excellent fit
- **70-89%**: Good fit
- **50-69%**: Fair fit
- **Below 50%**: Needs development

### 📚 Learning Resources
YouTube videos and courses to learn missing skills

### 📥 Export Options
- Download JSON report (detailed analysis)
- Download CSV with skills list

---

## Programmatic Usage

### Python API

```python
from resume_api import analyze

# Analyze a resume with job description
result = analyze(
    "/path/to/resume.pdf",
    "Job description text here..."
)

# Access the results
name = result['basic_info']['name']
email = result['basic_info']['email']
match_percentage = result['match_percentage']
skills = result['skills']['extracted']
recommendations = result['recommendations']
```

### Get JSON Output

```python
from resume_api import analyze_json

# Get analysis as JSON string
json_string = analyze_json(
    "/path/to/resume.pdf",
    "Job description"
)

# Write to file
with open("analysis.json", "w") as f:
    f.write(json_string)
```

---

## File Formats Supported

- ✅ **PDF** (.pdf) - Most common
- ✅ **DOCX** (.docx) - Microsoft Word
- ❌ DOC - Not supported
- ❌ TXT - Not supported

**Converting to DOCX**:
- Word: Save as .docx
- Google Docs: Download > Microsoft Word (.docx)
- LibreOffice: Save > Microsoft Word (.docx)

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named..."
**Solution**:
```bash
pip install -r requirements_modern.txt
```

### Issue: No skills detected
**Solution**:
- Ensure skills are clearly listed in resume
- Try separate "Skills" section with skill names
- Common format: "Python, JavaScript, React"

### Issue: Email/Phone not found
**Solution**:
- Use standard formats:
  - Email: john@example.com
  - Phone: +1-555-0123 or (555) 555-0123

### Issue: "Streamlit not found"
**Solution**:
```bash
pip install streamlit
# Or reinstall all
pip install -r requirements_modern.txt
```

### Issue: Page count wrong for DOCX
**Solution**:
- Page count is estimated for DOCX files
- PDF page count is exact
- Convert DOCX to PDF for accurate count

---

## Example Resume Analysis

### Sample Input
**Resume**: john_doe_resume.pdf
```
John Doe
john@example.com
(555) 123-4567

EDUCATION
Bachelor of Science in Computer Science
Stanford University

SKILLS
Programming: Python, JavaScript, React
Database: SQL, MongoDB
Tools: Git, Docker, AWS
```

**Job Description**:
```
Software Engineer - We need:
- Python (required)
- JavaScript (required)
- TypeScript (preferred)
- AWS (required)
- Kubernetes (preferred)
```

### Sample Output
```json
{
  "basic_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "(555) 123-4567"
  },
  "skills": {
    "extracted": ["Python", "JavaScript", "React", "SQL", "MongoDB", "Git", "Docker", "AWS"],
    "matched": ["Python", "JavaScript", "AWS"],
    "missing": ["TypeScript", "Kubernetes"],
    "extra": ["React", "SQL", "MongoDB", "Git", "Docker"]
  },
  "match_percentage": 60,
  "recommendations": [
    {
      "skill": "TypeScript",
      "priority": "high"
    },
    {
      "skill": "Kubernetes",
      "priority": "medium"
    }
  ],
  "resume_stats": {
    "pages": 1,
    "skills_count": 8
  },
  "learning_resources": {
    "TypeScript": {
      "youtube": "https://www.youtube.com/watch?v=BCg4perUb7w",
      "resource": "https://www.typescriptlang.org/docs/"
    },
    "Kubernetes": {
      "youtube": "https://www.youtube.com/watch?v=X48VuDVv0Z0",
      "resource": "https://kubernetes.io/docs/tutorials/"
    }
  }
}
```

---

## Best Practices

### ✅ DO:
- Use clear section headers (SKILLS, EDUCATION, EXPERIENCE)
- List skills explicitly (not hidden in descriptions)
- Include actual job description for better analysis
- Use standard formats (john@example.com)
- Keep resume well-formatted

### ❌ DON'T:
- Use graphics or images (might not parse)
- Include skills in paragraphs only (use explicit list)
- Skip job description (limits recommendations)
- Use non-standard formats for contact info
- Upload corrupted PDF files

---

## Performance Guide

| Task | Time | Notes |
|------|------|-------|
| Upload Resume | Instant | File size dependent |
| Analysis | 2-5 sec | Depends on resume length |
| Report Export | Instant | JSON/CSV generation |
| Page Load | 1-2 sec | UI rendering |

**Optimization Tips**:
- Smaller resume files = faster analysis
- Well-formatted resumes = more accurate extraction
- Clearer job descriptions = better recommendations

---

## Settings & Preferences

Navigate to **⚙️ Settings** page to:
- Update account information
- Configure notification preferences
- Set theme and language
- Manage data sharing options

---

## Data Privacy

- ✅ Resumes are **NOT** stored
- ✅ Analysis is **done locally**
- ✅ Files are **temporary**
- ✅ No data collection
- ✅ No tracking

---

## Support & Help

### Getting Help:
1. Check README.md for detailed docs
2. Run test_system.py to verify setup
3. Check IMPLEMENTATION_SUMMARY.md for features

### Common Questions:

**Q: Where are my resumes stored?**
A: They are not stored. Files are temporary and deleted after analysis.

**Q: Can I analyze multiple resumes?**
A: Yes, upload and analyze one at a time.

**Q: How accurate is the analysis?**
A: Accuracy depends on resume format. Well-structured resumes = better results.

**Q: Can I get the raw JSON output?**
A: Yes, download JSON report from the dashboard.

**Q: How many skills does the system recognize?**
A: 120+ technical and soft skills.

**Q: Can I add custom skills?**
A: Edit TECHNICAL_SKILLS in resume_parser.py and LEARNING_RESOURCES in skill_analyzer.py.

---

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 512MB minimum
- **Storage**: 100MB for installation
- **Internet**: For learning resource links
- **Browser**: Modern browser (Chrome, Firefox, Edge, Safari)

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Stop Streamlit app |
| `R` | Rerun app |
| `C` | Clear cache |

---

## Environment Variables

Optional configuration:
```bash
# Control Streamlit behavior
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
```

---

## Getting Started Video

1. Open application: `streamlit run app.py`
2. Upload your resume
3. Add job description
4. Click "Analyze Resume"
5. Review results
6. Download report

**Total time**: ~5 minutes for first analysis

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run test_system.py
3. ✅ Start application (streamlit run app.py)
4. ✅ Upload your resume
5. ✅ Get skill analysis
6. ✅ Download recommendations

---

## Tips & Tricks

- **Better extraction**: Use clear section headers
- **Match job better**: Provide complete job description
- **Learn faster**: Sort recommendations by priority
- **Track progress**: Download and save reports

---

## Updates & News

Check README.md and IMPLEMENTATION_SUMMARY.md for:
- New features
- Bug fixes
- Performance improvements
- Latest skills added

---

**Ready to analyze your resume? Let's go! 🚀**

```bash
streamlit run app.py
```

---

**Version**: 2.0
**Last Updated**: April 2, 2026
