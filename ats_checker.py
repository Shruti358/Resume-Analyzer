from __future__ import annotations

import io
import json
import os
import re
from collections import Counter
from datetime import datetime
from typing import Dict, List, Tuple

import plotly.graph_objects as go
import streamlit as st
from docx import Document

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover - handled at runtime
    fitz = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:  # pragma: no cover - handled at runtime
    TfidfVectorizer = None
    cosine_similarity = None

from skill_analyzer import SkillAnalyzer

SAMPLE_RESUME_TEXT = """Aarav Sharma
aarav.sharma@example.com | +91 98765 43210

SUMMARY
Python developer with experience in Streamlit dashboards, data analysis, SQL, Docker, and machine learning projects.

SKILLS
Python, Streamlit, SQL, Pandas, NumPy, Machine Learning, Docker, Git, REST APIs, Problem Solving

EXPERIENCE
Data Analyst Intern - Pixel Labs
- Built a Streamlit analytics dashboard for resume scoring.
- Improved keyword tracking for internal hiring workflows.

PROJECTS
Resume Analyzer Dashboard
- Built a resume analysis tool with PDF parsing and skill matching.

EDUCATION
B.Tech in Computer Science - ABC University
"""

SAMPLE_JOB_DESCRIPTION = """We are looking for a Python Developer with experience in Streamlit, SQL, Docker, Git, Pandas, NumPy, REST APIs, and machine learning.
Candidates should have strong problem solving skills, projects in analytics, and a clear understanding of ATS optimized resumes."""

STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "have",
    "has", "he", "in", "is", "it", "its", "of", "on", "or", "that", "the",
    "this", "to", "was", "were", "will", "with", "we", "you", "your", "our",
    "they", "their", "them", "then", "than", "into", "about", "above", "below",
    "must", "should", "required", "preferred", "plus", "good", "strong", "skills",
    "skill", "role", "job", "position", "experience", "years", "year", "work",
    "team", "teams", "ability", "need", "needs", "looking", "candidate", "candidates",
    "responsible", "responsibilities", "etc", "etc.", "using", "use", "used", "based",
}

SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills", "core skills", "competencies", "expertise"],
    "education": ["education", "academic background", "academics", "qualifications"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "projects": ["projects", "project experience", "personal projects", "academic projects"],
}

COMMON_PHRASES = [
    "machine learning",
    "data analysis",
    "deep learning",
    "problem solving",
    "project management",
    "rest api",
    "rest apis",
    "resume parsing",
    "keyword matching",
    "ats optimized",
    "streamlit",
    "natural language processing",
    "nlp",
    "sql",
    "docker",
    "git",
    "pandas",
    "numpy",
    "python",
    "tableau",
    "power bi",
    "agile",
    "scrum",
]

LANGUAGE_PACKS = {
    "serious": {
        "English": {
            "strong": "Strong match. Your resume is fairly ATS-friendly.",
            "good": "Good match, but a few improvements can lift your score.",
            "moderate": "Moderate match. Add more job-specific keywords and sections.",
            "low": "Low match. The resume needs focused optimization for this job.",
            "keyword_prefix": "Missing keywords: ",
            "section_prefix": "Missing sections: ",
            "suggestion_prefix": "Suggestions: ",
        },
        "Hindi": {
            "strong": "Match strong hai. Resume ATS ke liye kaafi theek hai.",
            "good": "Match theek hai, lekin thodi aur polishing se score better ho sakta hai.",
            "moderate": "Match moderate hai. Job-specific keywords aur sections aur add karo.",
            "low": "Match low hai. Resume ko is job ke hisaab se achhe se optimize karna padega.",
            "keyword_prefix": "Missing keywords: ",
            "section_prefix": "Missing sections: ",
            "suggestion_prefix": "Suggestions: ",
        },
        "Hinglish": {
            "strong": "Bhai match strong hai. Resume ATS ke liye kaafi solid hai.",
            "good": "Theek-thaak match hai, bas thodi aur polishing chahiye.",
            "moderate": "Match average hai. Keywords aur sections aur strong karo.",
            "low": "Match low hai. Resume ko job ke hisaab se kaafi upgrade karna padega.",
            "keyword_prefix": "Missing keywords: ",
            "section_prefix": "Missing sections: ",
            "suggestion_prefix": "Suggestions: ",
        },
    },
    "savage": {
        "English": {
            "strong": "Strong enough. ATS will nod instead of crying.",
            "good": "Decent, but a few tweaks away from being scary for ATS.",
            "moderate": "Resume is mid. ATS wants more keywords and better structure.",
            "low": "Bhai this resume is not ATS-ready. It needs serious work.",
            "keyword_prefix": "Keywords missing in action: ",
            "section_prefix": "Sections missing like your GPA in college: ",
            "suggestion_prefix": "Fix list: ",
        },
        "Hindi": {
            "strong": "Resume strong hai. ATS bhi thoda impressed ho jayega.",
            "good": "Theek hai, par aur polish karoge to ATS khush ho jayega.",
            "moderate": "Resume average hai. Keywords aur structure aur solid karo.",
            "low": "Bhai ye resume ATS ke liye ready nahi hai. Kaafi kaam baaki hai.",
            "keyword_prefix": "Missing keywords: ",
            "section_prefix": "Missing sections: ",
            "suggestion_prefix": "Fix list: ",
        },
        "Hinglish": {
            "strong": "Bhai resume solid hai. ATS bhi thoda respect karega.",
            "good": "Theek hai, par aur masala daloge to aur bhi mast ho jayega.",
            "moderate": "Resume thoda mid hai. Keywords aur sections aur tight karo.",
            "low": "Bhai ye resume ATS-ready nahi hai. Abhi kaafi kaam bacha hai.",
            "keyword_prefix": "Keywords ka naam suna hai ya ignore kiya hai: ",
            "section_prefix": "Sections missing hain, jaise exam se pehle notes: ",
            "suggestion_prefix": "Fix list: ",
        },
    },
}

UI_LABELS = {
    "English": {
        "title": "ATS Resume Checker",
        "subtitle": "Upload a resume, paste the JD, and check how ATS-friendly it really is.",
        "upload_title": "Upload Resume",
        "jd_title": "Paste JD",
        "results_title": "Results Dashboard",
        "final_title": "Final Output Panel",
        "load_sample_resume": "Load Sample Resume",
        "load_sample_jd": "Load Sample JD",
        "analyze": "Analyze Resume",
        "savage_mode": "Savage Mode",
        "language": "Language",
        "sample_resume": "Sample resume loaded.",
        "sample_jd": "Sample JD loaded.",
        "missing_file": "Upload a PDF or DOCX resume, or load the sample resume.",
        "missing_jd": "Paste a job description before analyzing.",
        "invalid_file": "Unsupported file type. Please upload a PDF or DOCX file.",
        "empty_resume": "Resume text is empty. Please upload a valid file.",
        "empty_jd": "Job description is empty.",
        "ats_score": "ATS Score",
        "keyword_ratio": "Keyword Match Ratio",
        "matched_keywords": "Matched Keywords",
        "missing_keywords": "Missing Keywords",
        "section_analysis": "Section Analysis",
        "suggestions": "Suggestions",
        "feedback": "Feedback",
    },
    "Hindi": {
        "title": "ATS Resume Checker",
        "subtitle": "Resume upload karo, JD paste karo, aur ATS-friendly score dekho.",
        "upload_title": "Resume Upload",
        "jd_title": "JD Paste Karo",
        "results_title": "Results Dashboard",
        "final_title": "Final Output Panel",
        "load_sample_resume": "Sample Resume Load Karo",
        "load_sample_jd": "Sample JD Load Karo",
        "analyze": "Resume Analyze Karo",
        "savage_mode": "Savage Mode",
        "language": "Language",
        "sample_resume": "Sample resume load ho gaya.",
        "sample_jd": "Sample JD load ho gaya.",
        "missing_file": "PDF ya DOCX resume upload karo, ya sample resume load karo.",
        "missing_jd": "Analyze karne se pehle job description paste karo.",
        "invalid_file": "Unsupported file type. PDF ya DOCX upload karo.",
        "empty_resume": "Resume text empty hai. Valid file upload karo.",
        "empty_jd": "Job description empty hai.",
        "ats_score": "ATS Score",
        "keyword_ratio": "Keyword Match Ratio",
        "matched_keywords": "Matched Keywords",
        "missing_keywords": "Missing Keywords",
        "section_analysis": "Section Analysis",
        "suggestions": "Suggestions",
        "feedback": "Feedback",
    },
    "Hinglish": {
        "title": "ATS Resume Checker",
        "subtitle": "Resume upload karo, JD paste karo, aur dekh ATS kitna impressed hai.",
        "upload_title": "Resume Upload",
        "jd_title": "JD Paste Karo",
        "results_title": "Results Dashboard",
        "final_title": "Final Output Panel",
        "load_sample_resume": "Sample Resume Load Karo",
        "load_sample_jd": "Sample JD Load Karo",
        "analyze": "Resume Analyze Karo",
        "savage_mode": "Savage Mode",
        "language": "Language",
        "sample_resume": "Sample resume load ho gaya.",
        "sample_jd": "Sample JD load ho gaya.",
        "missing_file": "PDF ya DOCX resume upload karo, ya sample resume load karo.",
        "missing_jd": "Analyze karne se pehle job description paste karo.",
        "invalid_file": "Unsupported file type. PDF ya DOCX upload karo.",
        "empty_resume": "Resume text empty hai. Valid file upload karo.",
        "empty_jd": "Job description empty hai.",
        "ats_score": "ATS Score",
        "keyword_ratio": "Keyword Match Ratio",
        "matched_keywords": "Matched Keywords",
        "missing_keywords": "Missing Keywords",
        "section_analysis": "Section Analysis",
        "suggestions": "Suggestions",
        "feedback": "Feedback",
    },
}


def _read_file_bytes(file_obj) -> bytes:
    if file_obj is None:
        return b""
    if isinstance(file_obj, (bytes, bytearray)):
        return bytes(file_obj)
    if hasattr(file_obj, "getvalue"):
        return file_obj.getvalue()
    if hasattr(file_obj, "read"):
        return file_obj.read()
    if isinstance(file_obj, str) and os.path.exists(file_obj):
        with open(file_obj, "rb") as handle:
            return handle.read()
    return b""


def extract_text_from_pdf(file_obj) -> str:
    """Extract text from a PDF using PyMuPDF."""
    if fitz is None:
        raise RuntimeError("PyMuPDF is not installed. Please install 'pymupdf'.")

    data = _read_file_bytes(file_obj)
    if not data:
        return ""

    document = fitz.open(stream=data, filetype="pdf")
    try:
        pages = [page.get_text("text") for page in document]
    finally:
        document.close()
    return "\n".join(pages).strip()


def extract_text_from_docx(file_obj) -> str:
    """Extract text from a DOCX file using python-docx."""
    data = _read_file_bytes(file_obj)
    if not data:
        return ""

    document = Document(io.BytesIO(data))
    return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()


def extract_text_from_upload(file_obj) -> str:
    """Dispatch extractor based on uploaded file type."""
    if file_obj is None:
        return ""

    name = getattr(file_obj, "name", "") or ""
    suffix = os.path.splitext(name)[1].lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(file_obj)
    if suffix == ".docx":
        return extract_text_from_docx(file_obj)
    raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")


def _tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-/]{1,}", text.lower())
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def extract_keywords(text: str, max_keywords: int = 20) -> List[str]:
    """Extract important keywords from the job description."""
    if not text:
        return []

    text_lower = text.lower()
    keywords: List[str] = []

    # Technical keywords from the existing skill analyzer help a lot here.
    try:
        skill_keywords = SkillAnalyzer.extract_skills_from_text(text)
    except Exception:
        skill_keywords = []

    for keyword in skill_keywords:
        normalized = keyword.strip().lower()
        if normalized and normalized not in keywords:
            keywords.append(normalized)

    for phrase in COMMON_PHRASES:
        if phrase in text_lower and phrase not in keywords:
            keywords.append(phrase)

    token_counts = Counter(_tokenize(text))
    for token, _count in token_counts.most_common(max_keywords * 2):
        if token not in keywords:
            keywords.append(token)
        if len(keywords) >= max_keywords:
            break

    return keywords[:max_keywords]


def _phrase_present(text: str, phrase: str) -> bool:
    if not phrase:
        return False
    pattern = r"\\b" + re.escape(phrase.lower()) + r"\\b"
    return bool(re.search(pattern, text.lower()))


def compare_keywords(resume_text: str, jd_text: str) -> Tuple[List[str], List[str], List[str]]:
    """Compare job description keywords against resume text."""
    jd_keywords = extract_keywords(jd_text)
    matched = [keyword for keyword in jd_keywords if _phrase_present(resume_text, keyword)]
    missing = [keyword for keyword in jd_keywords if keyword not in matched]
    return matched, missing, jd_keywords


def calculate_ats_score(resume_text: str, jd_text: str) -> Tuple[float, float]:
    """Calculate ATS score using TF-IDF cosine similarity."""
    if not resume_text or not jd_text:
        return 0.0, 0.0

    if TfidfVectorizer is None or cosine_similarity is None:
        raise RuntimeError("scikit-learn is required for ATS scoring.")

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    matrix = vectorizer.fit_transform([resume_text, jd_text])
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
    score = round(similarity * 100, 2)
    return score, similarity


def analyze_sections(resume_text: str) -> Dict:
    """Check resume for required ATS sections."""
    text_lower = (resume_text or "").lower()
    section_status = {}

    for section_name, variants in SECTION_KEYWORDS.items():
        present = any(re.search(rf"\\b{re.escape(variant)}\\b", text_lower) for variant in variants)
        section_status[section_name] = present

    missing_sections = [name.title() for name, present in section_status.items() if not present]

    suggestions: List[str] = []
    if not section_status["skills"]:
        suggestions.append("Add a clear Skills section with tools, languages, and frameworks used in the job.")
    if not section_status["education"]:
        suggestions.append("Add an Education section with degree, university, and graduation details.")
    if not section_status["experience"]:
        suggestions.append("Add an Experience section with measurable achievements and role-specific impact.")
    if not section_status["projects"]:
        suggestions.append("Add a Projects section to show hands-on work and domain fit.")

    return {
        "present": section_status,
        "missing_sections": missing_sections,
        "suggestions": suggestions,
    }


def _pick_feedback_pack(tone: str, language: str) -> Dict[str, str]:
    tone_key = "savage" if tone.lower().startswith("savage") else "serious"
    language_key = language if language in LANGUAGE_PACKS[tone_key] else "English"
    return LANGUAGE_PACKS[tone_key][language_key]


def generate_feedback(
    score: float,
    missing_keywords: List[str],
    tone: str,
    language: str,
    missing_sections: List[str] | None = None,
) -> Dict:
    """Generate tone-aware feedback in the chosen language."""
    pack = _pick_feedback_pack(tone, language)
    missing_sections = missing_sections or []

    if score >= 80:
        base_message = pack["strong"]
    elif score >= 60:
        base_message = pack["good"]
    elif score >= 40:
        base_message = pack["moderate"]
    else:
        base_message = pack["low"]

    if missing_keywords:
        keyword_note = f"{pack['keyword_prefix']}{', '.join(missing_keywords[:8])}"
    else:
        keyword_note = "Great job. The keyword match is strong enough to look recruiter-friendly."
        if tone.lower().startswith("savage"):
            keyword_note = "Keywords bhi aa gaye. ATS ko ab thoda respect dena padega."

    if missing_sections:
        section_note = f"{pack['section_prefix']}{', '.join(missing_sections)}"
    else:
        section_note = "Core sections are present, which is good for ATS parsing."
        if tone.lower().startswith("savage"):
            section_note = "Sections present hain. Resume ab kam se kam ghost draft nahi lag raha."

    suggestion_lines: List[str] = []
    if missing_keywords:
        suggestion_lines.append(
            f"{pack['suggestion_prefix']}Add the missing keywords naturally in Summary, Experience, and Projects."
        )
    if missing_sections:
        suggestion_lines.append(
            f"{pack['suggestion_prefix']}Create missing sections with concise bullet points and measurable results."
        )
    if score < 60:
        suggestion_lines.append(
            f"{pack['suggestion_prefix']}Align the resume title and summary with the target job role."
        )
    if not suggestion_lines:
        suggestion_lines.append("Keep the language crisp, quantify achievements, and mirror the job description wording where truthful.")
        if tone.lower().startswith("savage"):
            suggestion_lines.append("Bas overstuff mat karo. ATS ko keyword salad nahi, balanced plate chahiye.")

    return {
        "headline": base_message,
        "keyword_note": keyword_note,
        "section_note": section_note,
        "suggestions": suggestion_lines,
    }


def build_ats_analysis(resume_text: str, jd_text: str, tone: str, language: str) -> Dict:
    """Run the full ATS analysis pipeline."""
    ats_score, similarity = calculate_ats_score(resume_text, jd_text)
    matched_keywords, missing_keywords, jd_keywords = compare_keywords(resume_text, jd_text)
    section_data = analyze_sections(resume_text)
    feedback = generate_feedback(
        score=ats_score,
        missing_keywords=missing_keywords,
        tone=tone,
        language=language,
        missing_sections=section_data["missing_sections"],
    )

    keyword_match_ratio = round((len(matched_keywords) / max(len(jd_keywords), 1)) * 100, 2)

    return {
        "ats_score": round(ats_score, 2),
        "similarity": round(similarity, 4),
        "keyword_match_ratio": keyword_match_ratio,
        "keywords": {
            "all": jd_keywords,
            "matched": matched_keywords,
            "missing": missing_keywords,
        },
        "sections": section_data,
        "feedback": feedback,
        "suggestions": feedback["suggestions"],
    }


def _gauge_chart(score: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 46, "color": "#222222"}},
            title={"text": "ATS Score", "font": {"size": 20, "color": "#222222"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#222222"},
                "bar": {"color": "#4F46E5", "thickness": 0.35},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 60], "color": "#fef3c7"},
                    {"range": [60, 80], "color": "#e0e7ff"},
                    {"range": [80, 100], "color": "#dcfce7"},
                ],
                "threshold": {"line": {"color": "#222222", "width": 4}, "thickness": 0.8, "value": score},
            },
        )
    )
    fig.update_layout(
        margin={"l": 25, "r": 25, "t": 70, "b": 25},
        height=310,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#222222"},
    )
    return fig


def _keyword_chart(matched_keywords: List[str], missing_keywords: List[str]) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Bar(
                name="Matched",
                x=["Keywords"],
                y=[len(matched_keywords)],
                marker_color="#22C55E",
                text=[len(matched_keywords)],
                textposition="auto",
            ),
            go.Bar(
                name="Missing",
                x=["Keywords"],
                y=[len(missing_keywords)],
                marker_color="#EF4444",
                text=[len(missing_keywords)],
                textposition="auto",
            ),
        ]
    )
    fig.update_layout(
        title="Keyword Match Ratio",
        title_x=0.5,
        barmode="group",
        yaxis_title="Count",
        margin={"l": 25, "r": 25, "t": 60, "b": 25},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#222222"},
        yaxis={"gridcolor": "rgba(15, 23, 42, 0.08)"},
        xaxis={"tickfont": {"color": "#222222"}},
    )
    return fig


def _progress_html(score: float, label: str = "ATS Score") -> str:
    return f"""
    <div style="margin-top: 0.75rem;">
        <div style="background:#e5e7eb;border-radius:999px;height:14px;overflow:hidden;border:1px solid #d1d5db;">
            <div style="width:{max(0, min(score, 100))}%;height:100%;background:linear-gradient(90deg,#4F46E5 0%,#22C55E 100%);border-radius:999px;"></div>
        </div>
        <p style="margin:0.6rem 0 0;color:#222222;font-weight:600;text-align:center;">{label}: {score:.0f}%</p>
    </div>
    """


def _chip_html(items: List[str], fill: str, border: str, text: str) -> str:
    return "".join(
        f'<span style="display:inline-block;margin:0.25rem 0.35rem 0 0;padding:0.45rem 0.8rem;border-radius:999px;background:{fill};border:1px solid {border};color:{text};font-size:0.9rem;font-weight:600;">{item}</span>'
        for item in items
    )


def _inject_ats_styles() -> None:
    st.markdown(
        """
        <style>
            .ats-shell {
                background: #f9fafb;
                border-radius: 18px;
                padding: 1rem;
            }
            .ats-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
                padding: 1.2rem;
            }
            .ats-title {
                color: #111111;
                font-weight: 900;
                letter-spacing: -0.03em;
            }
            .ats-subtitle {
                color: #555555;
                font-size: 1rem;
            }
            .ats-badge {
                display: inline-block;
                padding: 0.35rem 0.7rem;
                border-radius: 999px;
                background: #eef2ff;
                color: #4338ca;
                font-weight: 700;
                font-size: 0.82rem;
                border: 1px solid #c7d2fe;
            }
            .ats-highlight-card {
                background: linear-gradient(135deg, #eef2ff 0%, #e0ecff 100%);
                border: 1px solid #c7d2fe;
                border-radius: 14px;
                box-shadow: 0 8px 18px rgba(79, 70, 229, 0.14);
                padding: 1.1rem 1.2rem;
                margin: 0.4rem 0 1rem 0;
            }
            .ats-highlight-title {
                color: #3730a3;
                font-size: 0.92rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                margin: 0;
            }
            .ats-highlight-score {
                color: #111111;
                font-size: 2rem;
                font-weight: 800;
                line-height: 1.2;
                margin: 0.3rem 0 0 0;
            }
            div:empty {
                display: none !important;
                height: auto !important;
                padding: 0 !important;
                margin: 0 !important;
                background: transparent !important;
                border: 0 !important;
                min-height: 0 !important;
            }
            .stButton > button {
                border-radius: 8px !important;
                border: 0 !important;
                background: #4F46E5 !important;
                color: white !important;
                font-weight: 800 !important;
                padding: 0.72rem 1.1rem !important;
                box-shadow: 0 6px 14px rgba(79, 70, 229, 0.24) !important;
                transition: all 0.3s ease !important;
            }
            .stButton > button:hover {
                background: #4338CA !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 8px 16px rgba(67, 56, 202, 0.26) !important;
            }
            .stButton > button:active {
                transform: scale(0.98) !important;
            }
            .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
                border-radius: 10px !important;
                border: 1px solid #d1d5db !important;
                background: #ffffff !important;
                color: #222222 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _ensure_state_defaults() -> None:
    st.session_state.setdefault("ats_uploaded_file", None)
    st.session_state.setdefault("ats_resume_text", "")
    st.session_state.setdefault("ats_jd_text", SAMPLE_JOB_DESCRIPTION)
    st.session_state.setdefault("ats_use_sample_resume", True)
    st.session_state.setdefault("ats_use_sample_jd", True)
    st.session_state.setdefault("ats_language", "Hinglish")
    st.session_state.setdefault("ats_tone", False)
    st.session_state.setdefault("ats_result", None)
    st.session_state.setdefault("ats_error", "")
    st.session_state.setdefault("ats_loading", False)


def _get_labels() -> Dict[str, str]:
    language = st.session_state.get("ats_language", "English")
    if language not in UI_LABELS:
        language = "English"
    return UI_LABELS[language]


def _load_sample_resume() -> None:
    st.session_state.ats_use_sample_resume = True
    st.session_state.ats_resume_text = SAMPLE_RESUME_TEXT
    st.session_state.ats_uploaded_file = None
    st.session_state.ats_error = ""


def _load_sample_jd() -> None:
    st.session_state.ats_use_sample_jd = True
    st.session_state.ats_jd_text = SAMPLE_JOB_DESCRIPTION
    st.session_state.ats_error = ""


def _analyze_current_inputs(uploaded_file, jd_text: str, tone: str, language: str) -> Dict:
    if st.session_state.get("ats_use_sample_resume", False):
        resume_text = SAMPLE_RESUME_TEXT
    elif uploaded_file is not None:
        resume_text = extract_text_from_upload(uploaded_file)
    else:
        resume_text = ""

    if not resume_text.strip():
        raise ValueError(_get_labels()["missing_file"])
    if not jd_text.strip():
        raise ValueError(_get_labels()["missing_jd"])

    return build_ats_analysis(resume_text, jd_text, tone=tone, language=language)


def render_ats_checker_page() -> None:
    """Render the full ATS Resume Checker page in Streamlit."""
    _ensure_state_defaults()
    _inject_ats_styles()
    labels = _get_labels()

    st.markdown(
        f"""
        <div class="ats-shell">
            <h1 class="ats-title">{labels['title']}</h1>
            <p class="ats-subtitle">{labels['subtitle']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns([1.2, 1])
    with top_left:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<span class=\"ats-badge\">{labels['upload_title']}</span>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            help="Upload a PDF or DOCX resume",
        )
        if uploaded_file is not None:
            st.session_state.ats_uploaded_file = uploaded_file
            st.session_state.ats_use_sample_resume = False
            st.markdown(
                f"<p style='margin-top:0.75rem;color:#111111;font-weight:700;'>Selected: {uploaded_file.name}</p>",
                unsafe_allow_html=True,
            )
        else:
            if st.session_state.get("ats_use_sample_resume", False):
                st.markdown(
                    "<p style='margin-top:0.75rem;color:#111111;font-weight:700;'>Sample resume ready.</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<p style='margin-top:0.75rem;color:#555555;'>No file selected yet.</p>",
                    unsafe_allow_html=True,
                )

        sample_resume_col1, sample_resume_col2 = st.columns(2)
        with sample_resume_col1:
            if st.button(labels["load_sample_resume"], use_container_width=True):
                _load_sample_resume()
        with sample_resume_col2:
            if st.button("Clear Resume", use_container_width=True):
                st.session_state.ats_use_sample_resume = False
                st.session_state.ats_uploaded_file = None
                st.session_state.ats_resume_text = ""
                st.session_state.ats_result = None
                st.session_state.ats_error = ""
        st.markdown('</div>', unsafe_allow_html=True)

    with top_right:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<span class=\"ats-badge\">{labels['language']}</span>", unsafe_allow_html=True)
        st.session_state.ats_language = st.selectbox(
            labels["language"],
            ["English", "Hindi", "Hinglish"],
            index=["English", "Hindi", "Hinglish"].index(st.session_state.get("ats_language", "Hinglish")),
            label_visibility="collapsed",
        )
        st.session_state.ats_tone = st.toggle(labels["savage_mode"], value=st.session_state.get("ats_tone", False))
        mode_label = "Savage Mode" if st.session_state.ats_tone else "Serious Mode"
        mode_color = "#f43f5e" if st.session_state.ats_tone else "#16a34a"
        st.markdown(
            f"<p style='margin-top:0.75rem;color:{mode_color};font-weight:800;font-size:1rem;'>{mode_label}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#475569;margin:0.4rem 0 0;'>Serious mode = professional feedback. Savage mode = funny Hinglish roast.</p>",
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    jd_card, actions_card = st.columns([1.4, 0.8])
    with jd_card:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<span class=\"ats-badge\">{labels['jd_title']}</span>", unsafe_allow_html=True)
        jd_value = st.text_area(
            "Paste Job Description",
            value=st.session_state.get("ats_jd_text", SAMPLE_JOB_DESCRIPTION),
            height=220,
            placeholder="Paste the target job description here...",
            label_visibility="collapsed",
        )
        st.session_state.ats_jd_text = jd_value
        sample_jd_col1, sample_jd_col2 = st.columns(2)
        with sample_jd_col1:
            if st.button(labels["load_sample_jd"], use_container_width=True):
                _load_sample_jd()
                st.session_state.ats_jd_text = SAMPLE_JOB_DESCRIPTION
        with sample_jd_col2:
            if st.button("Clear JD", use_container_width=True):
                st.session_state.ats_jd_text = ""
                st.session_state.ats_use_sample_jd = False
                st.session_state.ats_result = None
                st.session_state.ats_error = ""
        st.markdown('</div>', unsafe_allow_html=True)

    with actions_card:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;color:#111111;'>Quick Start</h3>", unsafe_allow_html=True)
        st.markdown("<ul style='color:#555555;line-height:1.8;padding-left:1.2rem;'>", unsafe_allow_html=True)
        st.markdown("<li>Upload a PDF or DOCX resume.</li>", unsafe_allow_html=True)
        st.markdown("<li>Paste the JD or load the sample JD.</li>", unsafe_allow_html=True)
        st.markdown("<li>Choose language and tone.</li>", unsafe_allow_html=True)
        st.markdown("<li>Run ATS analysis and review missing sections.</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        if st.button(labels["analyze"], use_container_width=True):
            st.session_state.ats_loading = True
            try:
                result = _analyze_current_inputs(
                    st.session_state.get("ats_uploaded_file"),
                    st.session_state.get("ats_jd_text", ""),
                    tone="Savage Mode" if st.session_state.get("ats_tone", False) else "Serious Mode",
                    language=st.session_state.get("ats_language", "English"),
                )
                st.session_state.ats_result = result
                st.session_state.ats_error = ""
            except Exception as exc:
                st.session_state.ats_result = None
                st.session_state.ats_error = str(exc)
            finally:
                st.session_state.ats_loading = False
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("ats_loading", False):
        with st.spinner("Analyzing ATS match..."):
            st.stop()
        return

    if st.session_state.get("ats_error"):
        st.error(st.session_state.ats_error)

    result = st.session_state.get("ats_result")
    if not result:
        return

    score = float(result.get("ats_score", 0))
    matched_keywords = result.get("keywords", {}).get("matched", [])
    missing_keywords = result.get("keywords", {}).get("missing", [])
    missing_sections = result.get("sections", {}).get("missing_sections", [])
    suggestions = result.get("suggestions", [])
    feedback = result.get("feedback", {})

    st.markdown(
        f"""
        <div class="ats-highlight-card">
            <p class="ats-highlight-title">ATS Score Summary</p>
            <p class="ats-highlight-score">ATS Score: {score:.0f}/100</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"<h2 style='margin-top:1.5rem;color:#111111;'>{labels['results_title']}</h2>", unsafe_allow_html=True)
    score_col1, score_col2 = st.columns([1.2, 1.3])
    with score_col1:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.plotly_chart(_gauge_chart(score), use_container_width=True)
        st.markdown(_progress_html(score, labels["ats_score"]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with score_col2:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0;color:#111111;'>{labels['feedback']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#111111;font-size:1.02rem;font-weight:800;'>{feedback.get('headline', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#555555;'>{feedback.get('keyword_note', '')}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#555555;'>{feedback.get('section_note', '')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    kw_col1, kw_col2 = st.columns([1.2, 1])
    with kw_col1:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.plotly_chart(_keyword_chart(matched_keywords, missing_keywords), use_container_width=True)
        kw_ratio = result.get("keyword_match_ratio", 0.0)
        st.markdown(_progress_html(float(kw_ratio), labels["keyword_ratio"]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with kw_col2:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0;color:#111111;'>{labels['matched_keywords']}</h3>", unsafe_allow_html=True)
        if matched_keywords:
            st.markdown(_chip_html(matched_keywords, "#dcfce7", "#86efac", "#166534"), unsafe_allow_html=True)
        else:
            st.info("No matched keywords found.")
        st.markdown(f"<h3 style='margin-top:1rem;color:#111111;'>{labels['missing_keywords']}</h3>", unsafe_allow_html=True)
        if missing_keywords:
            st.markdown(_chip_html(missing_keywords, "#fee2e2", "#fca5a5", "#991b1b"), unsafe_allow_html=True)
        else:
            st.success("Great news: no missing keywords detected.")
        st.markdown('</div>', unsafe_allow_html=True)

    section_col1, section_col2 = st.columns([1.1, 1.2])
    with section_col1:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0;color:#111111;'>{labels['section_analysis']}</h3>", unsafe_allow_html=True)
        sections = result.get("sections", {}).get("present", {})
        for section_name in ["skills", "education", "experience", "projects"]:
            present = sections.get(section_name, False)
            label = section_name.title()
            color = "#22C55E" if present else "#EF4444"
            status = "Present" if present else "Missing"
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;gap:1rem;padding:0.55rem 0;border-bottom:1px dashed #e2e8f0;'>"
                f"<span style='color:#111111;font-weight:700;'>{label}</span>"
                f"<span style='color:{color};font-weight:800;'>{status}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
        if missing_sections:
            st.markdown(f"<p style='margin-top:1rem;color:#EF4444;font-weight:800;'>Missing: {', '.join(missing_sections)}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with section_col2:
        st.markdown('<div class="ats-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='margin-top:0;color:#111111;'>{labels['suggestions']}</h3>", unsafe_allow_html=True)
        if suggestions:
            st.markdown("<ul style='color:#555555;line-height:1.8;padding-left:1.2rem;'>", unsafe_allow_html=True)
            for suggestion in suggestions:
                st.markdown(f"<li>{suggestion}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)
        else:
            st.info("No extra suggestions. Your resume already covers the basics pretty well.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h2 style='margin-top:1.5rem;color:#111111;'>{labels['final_title']}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="ats-card">', unsafe_allow_html=True)
    final_left, final_right = st.columns([1.1, 1.2])
    with final_left:
        st.markdown(f"<p style='color:#111111;font-size:1.3rem;font-weight:900;margin:0;'>ATS Score: {score:.0f}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#555555;margin-top:0.5rem;'>Matched: {len(matched_keywords)} | Missing: {len(missing_keywords)} | Missing Sections: {len(missing_sections)}</p>", unsafe_allow_html=True)
    with final_right:
        st.markdown(f"<p style='color:#111111;font-weight:800;margin:0;'>Tone-based Feedback</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#555555;margin-top:0.5rem;'>{feedback.get('headline', '')}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "Download ATS JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name=f"ats_resume_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True,
    )
