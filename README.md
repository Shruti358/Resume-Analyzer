# 🎯 AI Resume Analyzer

A sophisticated resume analysis tool that compares your resume against job descriptions and provides detailed skill matching analysis with personalized learning recommendations.

## ✨ Features

- **Smart Skill Extraction** - Automatically extracts technical skills from resume and job descriptions
- **Match Score Analysis** - Calculates matching percentage between your skills and job requirements
- **Missing Skills Detection** - Identifies which skills you need to learn
- **Learning Path** - Provides a prioritized list of skills to learn
- **Natural Language Processing** - Uses NLTK for text cleaning and analysis
- **Interactive UI** - Beautiful Streamlit web interface

## 🚀 Quick Start

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/Shruti358/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python -m streamlit run app.py
   ```

4. **Open in browser**:
   - Local: http://localhost:8501
   - Network: http://192.168.1.8:8501

## 📋 Usage

1. **Enter Your Resume** - Paste your resume text in the left text area
2. **Enter Job Description** - Paste the job description in the right text area
3. **Click "Analyze Resume"** - Get detailed analysis
4. **Review Results**:
   - Match Score percentage
   - Skills you already have
   - Missing skills to learn
   - Confidence rating

## 📦 Project Structure

```
Resume-Analyzer/
├── app.py                 # Main Streamlit application
├── ml_model.py           # Core analysis logic
├── utils.py              # Utility functions for skill extraction
├── preprocess.py         # Data preprocessing for batch analysis
├── matching.py           # Advanced matching algorithms
├── test.py               # Test script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Recognized Skills

The analyzer recognizes 30+ technical skills including:

**Programming Languages:**
- Python, Java, C++, R, Scala

**Data & ML:**
- Machine Learning, Deep Learning, Pandas, NumPy, Data Analysis, TensorFlow, Keras, Scikit-learn

**Web Development:**
- HTML, CSS, JavaScript, React, Node.js

**Databases:**
- SQL, MongoDB, PostgreSQL, Oracle

**Cloud & DevOps:**
- AWS, GCP, Docker, Kubernetes, Azure

**Other:**
- Git, Linux, Windows, DSA, SAP, Salesforce

## 📝 Files Description

### `app.py`
Main Streamlit application with:
- Text input areas for resume and job description
- Real-time skill extraction
- Interactive results display
- Error handling and validation

### `ml_model.py`
Core analysis engine:
- `analyze_resume()` - Compares resume skills with job requirements
- Returns match score, missing skills, and learning path

### `utils.py`
Utility functions:
- `clean_text()` - Text preprocessing and stopword removal
- `extract_skills()` - Skill extraction from text

### `preprocess.py`
Batch processing:
- Load CSV with resume and job description pairs
- Extract and analyze skills for multiple records
- Generate JSON output with results

### `matching.py`
Advanced matching:
- Cosine similarity calculation
- Vectorization of skills
- Multi-label classification

### `test.py`
Testing script:
- Run with `python test.py`
- Tests skill extraction and analysis functions
- Useful for debugging

## 🔍 Example

```
Resume: "I have 5 years of experience with Python, Pandas, NumPy and SQL"
Job: "We need Python, SQL, Machine Learning, Deep Learning expert"

Results:
- Match Score: 60%
- Skills Matched: Python, SQL
- Missing Skills: Machine Learning, Deep Learning
- Learning Path: Machine Learning → Deep Learning → TensorFlow
```

## 🛠️ Installation Issues

### Streamlit not recognized
If you get "streamlit is not recognized", use:
```bash
python -m streamlit run app.py
```

### Missing modules
Install all dependencies:
```bash
pip install -r requirements.txt
```

## 🔄 Development

### Running Tests
```bash
python test.py
```

### Batch Processing
```bash
python preprocess.py
```

This reads `data.csv` and generates `processed_data.json`

## 📊 Dependencies

- **streamlit** - Web app framework
- **pandas** - Data manipulation
- **scikit-learn** - Machine learning utilities
- **nltk** - Natural language processing
- **numpy** - Numerical computing

See `requirements.txt` for specific versions.

## 🐛 Troubleshooting

**App won't start:**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use correct Python path: `python -m streamlit run app.py`
- Check PORT 8501 is not in use

**Skills not recognized:**
- Check if skill name is in the SKILLS list
- Text must contain the exact skill name (case-insensitive)
- Special characters are automatically cleaned

**No results shown:**
- Ensure both resume and job description have at least one recognized skill
- Check the console for error messages

## 📧 Support

For issues, questions, or suggestions, please check the original repository or open an issue.

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Job Hunting! 🚀**
