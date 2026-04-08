"""
Modern Professional Resume Analyzer UI - Streamlit Application
Features: Modern Design, Glassmorphism, Icons, Animations, and Interactive Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import os
import tempfile
from ats_checker import render_ats_checker_page
from resume_parser import ResumeParser
from skill_analyzer import ResumeAnalyzer

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# CUSTOM STYLING - LIGHT THEME WITH ANIMATIONS
# ============================================================================

def inject_custom_styles():
    """Inject custom CSS for light theme with animations"""
    st.markdown("""
    <style>
        /* Global Styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: #f9fafb !important;
            color: #222222;
            font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* Background decorative elements */
        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: none;
            pointer-events: none;
            z-index: 0;
        }
        
        /* Decorative geometric shapes */
        [data-testid="stAppViewContainer"]::after {
            content: '';
            position: fixed;
            bottom: -100px;
            left: -100px;
            width: 300px;
            height: 300px;
            background: none;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: none;
        }
        
        /* Floating animation for decorations */
        @keyframes float {
            0%, 100% {
                transform: translateY(0px) translateX(0px);
            }
            25% {
                transform: translateY(-20px) translateX(10px);
            }
            50% {
                transform: translateY(-40px) translateX(20px);
            }
            75% {
                transform: translateY(-20px) translateX(10px);
            }
        }
        
        /* Decorative sticker styles */
        .stMainBlockContainer::before {
            content: '';
            position: fixed;
            top: 10%;
            right: 2%;
            font-size: 80px;
            color: transparent;
            z-index: 0;
            pointer-events: none;
            animation: none;
        }
        
        .stMainBlockContainer::after {
            content: '';
            position: fixed;
            bottom: 15%;
            left: 3%;
            font-size: 120px;
            color: transparent;
            z-index: 0;
            pointer-events: none;
            animation: none;
        }
        
        /* Top right accent */
        [data-testid="stSidebar"]::before {
            content: '';
            position: absolute;
            top: 20%;
            right: -30px;
            font-size: 60px;
            color: transparent;
            z-index: 1;
            pointer-events: none;
            animation: none;
        }
        
        /* Bottom left accent */
        [data-testid="stSidebar"]::after {
            content: '';
            position: absolute;
            bottom: 10%;
            left: -20px;
            font-size: 100px;
            color: transparent;
            z-index: 0;
            pointer-events: none;
            animation: none;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #e5e7eb !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #333333 !important;
        }
        
        .stSidebarContent {
            padding-top: 2rem;
        }
        
        /* Main Content */
        [data-testid="stMainBlockContainer"] {
            padding: 2rem;
        }
        
        /* Card Styling */
        .glass-card {
            background: #ffffff !important;
            border-radius: 14px !important;
            border: 1px solid #e5e7eb !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06) !important;
            transition: all 0.3s ease !important;
            animation: none !important;
        }
        
        .glass-card:hover {
            background: #ffffff !important;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08) !important;
            transform: none !important;
        }
        
        /* Animation: Slide Up */
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Animation: Glow Effect */
        @keyframes glow {
            0%, 100% {
                box-shadow: none;
            }
            50% {
                box-shadow: none;
            }
        }
        
        /* Animation: Fluorescent Glow */
        @keyframes fluorescent-glow {
            0%, 100% {
                box-shadow: none;
            }
            50% {
                box-shadow: none;
            }
        }
        
        /* Animation: Pop Up (Modal Style) */
        @keyframes popUp {
            from {
                opacity: 0;
                transform: scale(0.8) translateY(20px);
            }
            to {
                opacity: 1;
                transform: scale(1) translateY(0);
            }
        }
        
        /* Animation: Fade In */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        /* Animation: Slide From Left */
        @keyframes slideFromLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Animation: Slide From Right */
        @keyframes slideFromRight {
            from {
                opacity: 0;
                transform: translateX(30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .glow-effect {
            animation: none;
        }
        
        .fluorescent-glow {
            animation: none;
        }
        
        .pop-up {
            animation: popUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        .slide-left {
            animation: slideFromLeft 0.5s ease-out;
        }
        
        .slide-right {
            animation: slideFromRight 0.5s ease-out;
        }
        
        /* Headers */
        h1 {
            font-size: 3rem !important;
            font-weight: 800 !important;
            color: #111111 !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -1px !important;
        }
        
        h2 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #111111 !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            display: flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
            font-weight: 600 !important;
            color: #555555 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        /* Button Styling */
        .stButton > button {
            background: #4F46E5 !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.72rem 1.1rem !important;
            border-radius: 8px !important;
            border: none !important;
            font-size: 1rem !important;
            box-shadow: 0 6px 14px rgba(79, 70, 229, 0.22) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            background: #4338CA !important;
            box-shadow: 0 8px 16px rgba(67, 56, 202, 0.24) !important;
            transform: translateY(-1px) !important;
        }
        
        .stButton > button:active {
            transform: scale(0.98) !important;
        }
        
        /* Secondary Button */
        .secondary-button > button {
            background: rgba(79, 70, 229, 0.08) !important;
            color: #4F46E5 !important;
            border: 1px solid #4F46E5 !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
        }
        
        .secondary-button > button:hover {
            background: rgba(79, 70, 229, 0.12) !important;
            border-color: #4338CA !important;
        }
        
        /* Input Fields */
        .stTextInput input, .stTextArea textarea {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            color: #333333 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            caret-color: #4F46E5 !important;
        }
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #999999 !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            background: rgba(255, 255, 255, 1) !important;
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.16) !important;
        }
        
        /* Selectbox and Dropdown */
        .stSelectbox {
            color: #333333 !important;
        }
        
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            color: #333333 !important;
        }
        
        /* Checkbox */
        .stCheckbox {
            color: #333333 !important;
        }
        
        .stCheckbox > label {
            color: #333333 !important;
        }
        
        /* File Uploader */
        .stFileUploader {
            background: rgba(79, 70, 229, 0.04) !important;
            border: 2px dashed #4F46E5 !important;
            border-radius: 8px !important;
            padding: 2rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            background: rgba(79, 70, 229, 0.08) !important;
            border-color: #4338CA !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }
        
        /* File uploader button */
        .stFileUploader button {
            background: #4F46E5 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            border: none !important;
            cursor: pointer !important;
        }
        
        .stFileUploader button:hover {
            background: #4338CA !important;
            box-shadow: 0 4px 12px rgba(67, 56, 202, 0.24) !important;
        }
        
        /* File uploader label */
        .stFileUploader label {
            color: #333333 !important;
            font-weight: 600 !important;
        }
        
        /* Subtitle */
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #666666;
            margin-bottom: 2rem;
            letter-spacing: 0.5px;
        }
        
        /* Tags/Pills */
        .skill-tag {
            display: inline-block;
            background: #eef2ff !important;
            border: 1px solid #c7d2fe !important;
            color: #3730a3 !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 20px !important;
            margin: 0.4rem !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
        }
        
        .skill-tag:hover {
            background: #e0e7ff !important;
            box-shadow: none !important;
            transform: none !important;
        }
        
        .missing-tag {
            background: #fee2e2 !important;
            border: 1px solid #fecaca !important;
            color: #EF4444 !important;
            box-shadow: none !important;
        }
        
        .missing-tag:hover {
            background: #fee2e2 !important;
            box-shadow: none !important;
            transform: none !important;
        }
        
        .recommended-tag {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(76, 175, 80, 0.05)) !important;
            border: 1px solid #4caf50 !important;
            color: #2e7d32 !important;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1) !important;
        }
        
        .recommended-tag:hover {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.15), rgba(76, 175, 80, 0.1)) !important;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Progress Circle */
        .progress-circle {
            text-align: center;
            padding: 2rem;
            animation: slideUp 0.6s ease-out;
        }
        
        .progress-value {
            font-size: 3.5rem;
            font-weight: 800;
            color: #1d4ed8;
            margin: 1rem 0;
        }
        
        .progress-label {
            font-size: 1.1rem;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Success Message */
        .success-message {
            background: rgba(76, 175, 80, 0.1) !important;
            border: 1px solid #4caf50 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            color: #2e7d32 !important;
            text-align: center !important;
        }
        
        /* Info Box */
        .info-box {
            background: #eef2ff !important;
            border: 1px solid #c7d2fe !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            color: #222222 !important;
        }
        
        /* Section Divider */
        .section-divider {
            height: 1px;
            background: #e5e7eb;
            margin: 1.5rem 0;
        }

        .ats-highlight-card {
            background: linear-gradient(135deg, #eef2ff 0%, #e0ecff 100%);
            border: 1px solid #c7d2fe;
            border-radius: 14px;
            box-shadow: 0 8px 18px rgba(79, 70, 229, 0.14);
            padding: 1.2rem 1.4rem;
            margin: 0.5rem 0 1.25rem 0;
        }

        .ats-highlight-title {
            color: #3730a3;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            margin: 0;
        }

        .ats-highlight-score {
            color: #111111;
            font-size: 2rem;
            line-height: 1.2;
            font-weight: 800;
            margin: 0.3rem 0 0 0;
        }

        /* Never keep empty DOM blocks in layout */
        div:empty {
            display: none !important;
            height: auto !important;
            padding: 0 !important;
            margin: 0 !important;
            background: transparent !important;
            border: 0 !important;
            min-height: 0 !important;
        }
        
        /* Stat Card */
        .stat-card {
            background: #f8faff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            animation: popUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }
        
        .stat-card:hover {
            background: #eef2ff !important;
            box-shadow: 0 8px 18px rgba(79, 70, 229, 0.12) !important;
            transform: translateY(-2px) !important;
        }
        
        .stat-value {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: #1d4ed8 !important;
        }
        
        .stat-label {
            font-size: 0.9rem !important;
            color: #999999 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            margin-top: 0.5rem !important;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            h1 {
                font-size: 2rem !important;
            }
            
            h2 {
                font-size: 1.5rem !important;
            }
            
            .glass-card {
                padding: 1.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_side_navigation():
    """Create sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <style>
            .sidebar-header {
                text-align: center;
                padding: 1.5rem 0;
                border-bottom: 1px solid #e0e0e0;
                margin-bottom: 2rem;
            }
            .nav-item {
                padding: 0.75rem 1rem;
                margin: 0.5rem 0;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .nav-item:hover {
                background: rgba(79, 70, 229, 0.12);
            }
            .nav-item-active {
                background: rgba(79, 70, 229, 0.18);
                border-left: 3px solid #4F46E5;
                padding-left: calc(1rem - 3px);
            }
        </style>
        <div class="sidebar-header">
            <h3 style="margin:0; font-size:1.5rem;">Resume AI</h3>
            <p style="margin:0.5rem 0 0 0; font-size:0.85rem; color:#475569;">Your Smart Career Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        page = st.radio(
            "Navigate",
            ["Upload Resume", "ATS Checker", "Analysis Dashboard", "Feedback", "Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="padding: 1rem; font-size: 0.85rem; color: #64748b; text-align: center;">
            <p>Built with using Streamlit</p>
            <p>Version 2.0 - Modern UI</p>
        </div>
        """, unsafe_allow_html=True)
        
        return page

def display_upload_form():
    """Display the resume upload form on the main screen"""
    st.markdown("""
    <style>
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            margin-bottom: 2rem;
        }
        .hero-subtitle {
            font-size: 1.3rem;
            color: #1f2937;
            margin-bottom: 1rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="hero-section">
        <p class="hero-subtitle">Welcome to the Future of Resume Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 style="text-align: center; margin-top: 0;">Upload Your Resume</h2>
        <p style="text-align: center; color: #334155; font-size: 1rem; margin-bottom: 1.5rem;">
            Get AI-powered insights about your resume in seconds
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .upload-message {
                text-align: center;
                color: #334155;
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .file-info {
                text-align: center;
                color: #555555;
                font-size: 0.85rem;
                margin-top: -0.5rem;
            }
        </style>
        <p class="upload-message">Click or drag your resume below</p>
        <p class="file-info">Supported formats: PDF, DOCX (Max 200MB)</p>
        """, unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            help="Upload your resume in PDF or DOCX format"
        )
        
        if uploaded_file:
            st.markdown(f"""
            <div style="background: rgba(76, 175, 80, 0.2); border: 2px solid rgba(76, 175, 80, 0.6); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; box-shadow: 0 8px 24px rgba(76, 175, 80, 0.2);">
                <p style="margin: 0; color: #81c784; font-size: 1.1rem; font-weight: 600;">File Selected</p>
                <p style="margin: 0.5rem 0 0 0; color: #1f2937; font-size: 0.95rem;">{uploaded_file.name}</p>
                <p style="margin: 0.25rem 0 0 0; color: #475569; font-size: 0.85rem;">{uploaded_file.size / 1024:.1f} KB</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Job Description Section
            st.markdown("""
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.75rem;">Job Description (Optional)</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0 0 1rem 0;">Paste the job description to get better skill matching</p>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Paste job description here",
                placeholder="Software Engineer - Required: Python, React, AWS, Docker, System Design...",
                height=120,
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume", use_container_width=True, key="analyze_btn"):
                    st.session_state.is_loading = True
                    with st.spinner("Analyzing your resume..."):
                        try:
                            # Analyze the resume
                            analysis_result = analyze_resume(uploaded_file, job_description)

                            # Store in session
                            st.session_state.resume_uploaded = True
                            st.session_state.resume_data = analysis_result
                            st.session_state.current_file = uploaded_file.name
                            st.session_state.show_dashboard = True
                        finally:
                            st.session_state.is_loading = False

                        st.success("Resume analyzed! Redirecting to dashboard...")
                        st.rerun()
            
            with col2:
                if st.button("Clear File", use_container_width=True, key="clear_btn"):
                    st.session_state.resume_uploaded = False
                    st.session_state.show_dashboard = False
                    st.rerun()
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 2rem;">What We Analyze</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        ("Technical Skills", "Identifies programming languages, frameworks, and tools"),
        ("Experience Match", "Compares your background with job requirements"),
        ("Growth Areas", "Suggests skills to improve your profile"),
        ("Personalized Tips", "Get actionable recommendations")
    ]
    
    for col, (title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="margin: 0; text-align: center;">
                <h3 style="font-size: 1.1rem; margin: 0.5rem 0; color: #1f2937;">{title}</h3>
                <p style="font-size: 0.9rem; color: #475569; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def analyze_resume(uploaded_file, job_description=""):
    """Analyze uploaded resume and compare with job description"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        # Parse resume
        parser = ResumeParser()
        resume_data = parser.parse_full_resume(tmp_path)
        
        # Analyze resume with job description
        analyzer = ResumeAnalyzer()
        analysis_result = analyzer.analyze(resume_data, job_description)
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return analysis_result
    
    except Exception as e:
        return {
            "error": str(e),
            "basic_info": {
                "name": "Error",
                "email": "Not Found",
                "phone": "Not Found"
            },
            "education": [],
            "experience": [],
            "skills": {
                "extracted": [],
                "matched": [],
                "missing": [],
                "extra": []
            },
            "match_percentage": 0,
            "ats_score": 0,
            "ats_feedback": "Low match, significant improvement needed",
            "keyword_analysis": {"matched": [], "missing": []},
            "section_feedback": {
                "skills": "Unable to evaluate skills due to analysis error.",
                "keywords": "Unable to evaluate keywords due to analysis error.",
                "structure": "Unable to evaluate structure due to analysis error.",
                "completeness": "Unable to evaluate completeness due to analysis error."
            },
            "recommendations": [],
            "resume_stats": {"pages": 0}
        }

def create_ats_gauge_chart(ats_score):
    """Create ATS score gauge visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ats_score,
        number={'suffix': "%", 'font': {'size': 40, 'color': '#222222'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#222222'},
            'bar': {'color': '#4F46E5', 'thickness': 0.35},
            'steps': [
                {'range': [0, 40], 'color': '#fee2e2'},
                {'range': [40, 60], 'color': '#fef3c7'},
                {'range': [60, 80], 'color': '#e0e7ff'},
                {'range': [80, 100], 'color': '#dcfce7'},
            ],
            'threshold': {
                'line': {'color': '#222222', 'width': 4},
                'thickness': 0.8,
                'value': ats_score
            }
        },
        title={'text': "ATS Score", 'font': {'size': 18, 'color': '#222222'}}
    ))

    fig.update_layout(
        margin=dict(l=25, r=25, t=70, b=25),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222222')
    )
    return fig

def create_skill_match_pie_chart(matched_skills, missing_skills):
    """Create pie chart of matched vs missing skills."""
    fig = go.Figure(data=[go.Pie(
        labels=['Matched Skills', 'Missing Skills'],
        values=[len(matched_skills), len(missing_skills)],
        marker=dict(colors=['#22C55E', '#EF4444']),
        hole=0.35,
        sort=False,
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
    )])

    fig.update_layout(
        title="Skill Match Distribution",
        title_font_size=18,
        title_x=0.5,
        showlegend=True,
        margin=dict(l=25, r=25, t=70, b=25),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222222')
    )
    return fig

def create_missing_vs_matched_bar_chart(matched_skills, missing_skills):
    """Create bar chart comparing matched and missing skills."""
    fig = go.Figure(data=[
        go.Bar(
            x=['Matched Skills', 'Missing Skills'],
            y=[len(matched_skills), len(missing_skills)],
            marker_color=['#22C55E', '#EF4444'],
            text=[len(matched_skills), len(missing_skills)],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])

    fig.update_layout(
        title="Missing vs Matched Skills",
        title_font_size=18,
        title_x=0.5,
        xaxis_title="",
        yaxis_title="Count",
        margin=dict(l=25, r=25, t=70, b=25),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222222'),
        yaxis=dict(gridcolor='rgba(15, 23, 42, 0.08)')
    )
    return fig

def create_keyword_match_chart(matched_keywords, missing_keywords):
    """Create keyword match chart for ATS keyword analysis."""
    fig = go.Figure(data=[
        go.Bar(
            name='Matched',
            x=['Keywords'],
            y=[len(matched_keywords)],
            marker_color='#4F46E5',
            text=[len(matched_keywords)],
            textposition='auto'
        ),
        go.Bar(
            name='Missing',
            x=['Keywords'],
            y=[len(missing_keywords)],
            marker_color='#F59E0B',
            text=[len(missing_keywords)],
            textposition='auto'
        )
    ])

    fig.update_layout(
        title="Keyword Match Overview",
        title_font_size=18,
        title_x=0.5,
        barmode='group',
        yaxis_title='Count',
        margin=dict(l=25, r=25, t=70, b=25),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222222'),
        yaxis=dict(gridcolor='rgba(15, 23, 42, 0.08)')
    )
    return fig

def display_skill_tags(skills, tag_type="skill"):
    """Display skills as styled tags"""
    html_content = ""
    css_class = "skill-tag"
    if tag_type == "missing":
        css_class = "skill-tag missing-tag"
    elif tag_type == "recommended":
        css_class = "skill-tag recommended-tag"
    
    for skill in skills:
        html_content += f'<span class="{css_class}">{skill}</span>'
    
    st.markdown(html_content, unsafe_allow_html=True)

def create_animated_progress(value, max_value=100):
    """Create animated progress bar"""
    percentage = (value / max_value) * 100
    
    html = f"""
    <div style="margin: 2rem 0;">
        <div style="background: #e5e7eb; border-radius: 50px; height: 10px; overflow: hidden; border: 1px solid #d1d5db;">
            <div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); height: 100%; width: {percentage}%; border-radius: 50px; transition: width 1s ease-in-out;"></div>
        </div>
        <p style="text-align: center; margin-top: 0.75rem; font-size: 0.95rem; color: #334155;">
            {value}%
        </p>
    </div>
    """
    return html

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def page_upload():
    """Resume Upload Page"""
    st.markdown("""
    <style>
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            margin-bottom: 2rem;
        }
        .hero-subtitle {
            font-size: 1.3rem;
            color: #1f2937;
            margin-bottom: 1rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="hero-section">
        <p class="hero-subtitle">Welcome to the Future of Resume Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <h2 style="text-align: center; margin-top: 0;">Upload Your Resume</h2>
        <p style="text-align: center; color: #334155; font-size: 1rem; margin-bottom: 1.5rem;">
            Get AI-powered insights about your resume in seconds
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .upload-message {
                text-align: center;
                color: #334155;
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .file-info {
                text-align: center;
                color: #555555;
                font-size: 0.85rem;
                margin-top: -0.5rem;
            }
        </style>
        <p class="upload-message">Click or drag your resume below</p>
        <p class="file-info">Supported formats: PDF, DOCX (Max 200MB)</p>
        """, unsafe_allow_html=True)
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            help="Upload your resume in PDF or DOCX format"
        )
        
        if uploaded_file:
            st.markdown(f"""
            <div style="background: rgba(76, 175, 80, 0.2); border: 2px solid rgba(76, 175, 80, 0.6); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; box-shadow: 0 8px 24px rgba(76, 175, 80, 0.2);">
                <p style="margin: 0; color: #81c784; font-size: 1.1rem; font-weight: 600;">File Selected</p>
                <p style="margin: 0.5rem 0 0 0; color: #1f2937; font-size: 0.95rem;">{uploaded_file.name}</p>
                <p style="margin: 0.25rem 0 0 0; color: #475569; font-size: 0.85rem;">{uploaded_file.size / 1024:.1f} KB</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Job Description Section
            st.markdown("""
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.75rem;">Job Description (Optional)</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0 0 1rem 0;">Paste the job description to get better skill matching</p>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Paste job description here",
                placeholder="Software Engineer - Required: Python, React, AWS, Docker, System Design...",
                height=120,
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume", use_container_width=True, key="analyze_btn"):
                    st.session_state.is_loading = True
                    with st.spinner("Analyzing your resume..."):
                        try:
                            # Analyze the resume
                            analysis_result = analyze_resume(uploaded_file, job_description)

                            # Store in session
                            st.session_state.resume_uploaded = True
                            st.session_state.resume_data = analysis_result
                            st.session_state.current_file = uploaded_file.name
                            st.session_state.show_dashboard = True
                        finally:
                            st.session_state.is_loading = False

                        st.success("Resume analyzed! Redirecting to dashboard...")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Clear File", use_container_width=True, key="clear_btn"):
                    st.session_state.resume_uploaded = False
                    st.session_state.show_dashboard = False
                    st.rerun()
        
        st.markdown("""
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 2rem;">What We Analyze</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        ("Technical Skills", "Identifies programming languages, frameworks, and tools"),
        ("Experience Match", "Compares your background with job requirements"),
        ("Growth Areas", "Suggests skills to improve your profile"),
        ("Personalized Tips", "Get actionable recommendations")
    ]
    
    for col, (title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="margin: 0; text-align: center;">
                <h3 style="font-size: 1.1rem; margin: 0.5rem 0; color: #1f2937;">{title}</h3>
                <p style="font-size: 0.9rem; color: #475569; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def page_dashboard():
    """Analysis Dashboard Page"""
    if st.session_state.get("is_loading", False):
        with st.spinner("Loading analysis..."):
            pass
        return

    if "resume_data" not in st.session_state or not st.session_state.get("resume_uploaded"):
        st.markdown("""
        <div class="info-box" style="text-align: center;">
            <h3 style="margin: 0; margin-bottom: 0.5rem;">No Resume Uploaded Yet</h3>
            <p style="margin: 0;">Please upload a resume from the Upload Resume page to see the analysis dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    data = st.session_state.resume_data
    
    # Check for errors
    if "error" in data:
        st.error(f"Error analyzing resume: {data['error']}")
        return
    
    # Extract data
    basic_info = data.get('basic_info', {})
    extracted_skills = data.get('skills', {}).get('extracted', [])
    matched_skills = data.get('skills', {}).get('matched', [])
    missing_skills = data.get('skills', {}).get('missing', [])
    match_percentage = data.get('match_percentage', 0)
    ats_score = data.get('ats_score', 0)
    ats_feedback = data.get('ats_feedback', 'No ATS feedback available')
    section_feedback = data.get('section_feedback', {})
    keyword_analysis = data.get('keyword_analysis', {})
    matched_keywords = keyword_analysis.get('matched', [])
    missing_keywords = keyword_analysis.get('missing', [])
    recommendations = data.get('recommendations', [])
    resume_stats = data.get('resume_stats', {})
    learning_resources = data.get('learning_resources', {})
    
    # Header
    name = basic_info.get('name', 'Unknown')
    email = basic_info.get('email', 'Not Found')
    phone = basic_info.get('phone', 'Not Found')
    pages = resume_stats.get('pages', 0)

    has_basic_info = any([
        name not in {'Unknown', 'Not Found', ''},
        email not in {'Not Found', ''},
        phone not in {'Not Found', ''},
        pages > 0,
        len(data.get('education', [])) > 0,
        len(data.get('experience', [])) > 0,
    ])
    has_skill_analysis = any([
        len(extracted_skills) > 0,
        len(matched_skills) > 0,
        len(missing_skills) > 0,
        len(matched_keywords) > 0,
        len(missing_keywords) > 0,
    ])
    has_ats_content = any([
        ats_score > 0,
        match_percentage > 0,
        len(matched_keywords) > 0,
        len(missing_keywords) > 0,
        resume_stats.get('education_count', 0) > 0,
        resume_stats.get('experience_count', 0) > 0,
    ])
    has_chart_data = any([
        len(matched_skills) > 0,
        len(missing_skills) > 0,
        len(matched_keywords) > 0,
        len(missing_keywords) > 0,
    ])
    has_section_feedback = any(
        isinstance(msg, str) and msg.strip()
        for msg in section_feedback.values()
    ) if isinstance(section_feedback, dict) else False
    has_export_data = any([
        has_basic_info,
        has_skill_analysis,
        has_ats_content,
        len(recommendations) > 0,
    ])
    
    st.markdown(f"""
    <h2>Analysis Report for {name}</h2>
    <p style="color: #64748b; margin-bottom: 1.5rem;">{email} | {phone} | {pages} page(s)</p>
    """, unsafe_allow_html=True)

    # 1) ATS Score (top highlight)
    if has_ats_content:
        st.markdown(f"""
        <div class="ats-highlight-card">
            <p class="ats-highlight-title">ATS Score Summary</p>
            <p class="ats-highlight-score">ATS Score: {ats_score:.0f}/100</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""<h2 style="margin-top: 2.0rem;">ATS Score</h2>""", unsafe_allow_html=True)
        col1, col2 = st.columns([1.2, 1.8])
        with col1:
            st.markdown("""<div class="glass-card" style="padding: 1rem;">""", unsafe_allow_html=True)
            st.plotly_chart(create_ats_gauge_chart(ats_score), use_container_width=True)
            st.markdown(create_animated_progress(ats_score), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
            st.markdown(f"""
            <h3 style="margin-top: 0; color: #0f172a;">{ats_feedback}</h3>
            <p style="color: #334155; margin-bottom: 0.75rem;">Skills Match: <strong>{match_percentage}%</strong></p>
            <p style="color: #334155; margin-bottom: 0.75rem;">Keyword Match: <strong>{len(matched_keywords)} matched / {len(matched_keywords) + len(missing_keywords)} tracked</strong></p>
            <p style="color: #334155; margin-bottom: 0;">Resume Completeness: <strong>{resume_stats.get('education_count', 0)} education, {resume_stats.get('experience_count', 0)} experience entries</strong></p>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 2) Basic Info
    if has_basic_info:
        st.markdown("""<h2 style="margin-top: 2.5rem;">Basic Information</h2>""", unsafe_allow_html=True)
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown(f"**Name:** {name}")
        with info_col2:
            st.markdown(f"**Email:** {email}")
        with info_col3:
            st.markdown(f"**Phone:** {phone}")
        st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0;'>", unsafe_allow_html=True)
        st.markdown(f"**Education Records:** {len(data.get('education', []))} | **Experience Records:** {len(data.get('experience', []))} | **Resume Pages:** {pages}")
        st.markdown("</div>", unsafe_allow_html=True)

    # 3) Skill Analysis
    if has_skill_analysis:
        st.markdown("""<h2 style="margin-top: 2.5rem;">Skill Analysis</h2>""", unsafe_allow_html=True)
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#334155;'>Detected <strong>{len(extracted_skills)}</strong> technical skills from your resume.</p>", unsafe_allow_html=True)
        if extracted_skills:
            display_skill_tags(extracted_skills, "skill")

        if matched_skills:
            st.markdown("<p style='color:#334155; margin-top:1rem;'><strong>Matched Skills</strong></p>", unsafe_allow_html=True)
            display_skill_tags(matched_skills, "skill")
        if missing_skills:
            st.markdown("<p style='color:#334155; margin-top:1rem;'><strong>Missing Skills</strong></p>", unsafe_allow_html=True)
            display_skill_tags(missing_skills, "missing")

        if matched_keywords or missing_keywords:
            st.markdown("<p style='color:#334155; margin-top:1rem;'><strong>Keyword Analysis</strong></p>", unsafe_allow_html=True)
            keyword_col1, keyword_col2 = st.columns(2)
            with keyword_col1:
                st.markdown(f"Matched Keywords: {len(matched_keywords)}")
                if matched_keywords:
                    display_skill_tags(matched_keywords, "skill")
            with keyword_col2:
                st.markdown(f"Missing Keywords: {len(missing_keywords)}")
                if missing_keywords:
                    display_skill_tags(missing_keywords, "missing")
        st.markdown("</div>", unsafe_allow_html=True)

    # Section-wise feedback
    if has_section_feedback:
        st.markdown("""<h3 style="margin-top: 1.5rem;">Section Feedback</h3>""", unsafe_allow_html=True)
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        st.markdown(
            f"- **Skills:** {section_feedback.get('skills', 'Not available')}\n"
            f"- **Keywords:** {section_feedback.get('keywords', 'Not available')}\n"
            f"- **Structure:** {section_feedback.get('structure', 'Not available')}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # 4) Charts / Graphs
    if has_chart_data:
        st.markdown("""<h2 style="margin-top: 2.5rem;">Charts and Graphs</h2>""", unsafe_allow_html=True)
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1:
            st.markdown("""<div class="glass-card" style="padding: 1rem;">""", unsafe_allow_html=True)
            st.plotly_chart(create_skill_match_pie_chart(matched_skills, missing_skills), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with row1_col2:
            st.markdown("""<div class="glass-card" style="padding: 1rem;">""", unsafe_allow_html=True)
            st.plotly_chart(create_missing_vs_matched_bar_chart(matched_skills, missing_skills), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("""<div class="glass-card" style="padding: 1rem;">""", unsafe_allow_html=True)
            st.plotly_chart(create_keyword_match_chart(matched_keywords, missing_keywords), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with chart_col2:
            st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
            stats = [
                ("Extracted Skills", resume_stats.get('skills_count', 0)),
                ("Matched Skills", len(matched_skills)),
                ("Missing Skills", len(missing_skills)),
                ("Matched Keywords", len(matched_keywords)),
            ]
            for label, value in stats:
                st.markdown(f"<p style='margin: 0.5rem 0; color: #334155;'><strong>{label}:</strong> {value}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 5) Recommendations
    st.markdown("""<h2 style="margin-top: 2.5rem;">Recommendations</h2>""", unsafe_allow_html=True)
    if recommendations:
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        recommended_skill_names = [rec.get('skill', '') for rec in recommendations]
        display_skill_tags(recommended_skill_names, "recommended")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No skill recommendations generated. Provide a detailed job description for targeted suggestions.")

    # 6) Learning Resources
    if recommendations:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Learning Resources</h2>
        <p style="color: #64748b; margin-bottom: 1.5rem;">
            Top resources to help you master missing skills
        </p>
        """, unsafe_allow_html=True)
        
        for i, rec in enumerate(recommendations[:3]):
            skill_name = rec.get('skill', 'Unknown')
            resource_item = learning_resources.get(skill_name, {})
            
            st.markdown(f"""
            <h3 style="font-size: 1.1rem; margin-top: 1.5rem; margin-bottom: 0.75rem;">{skill_name}</h3>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **YouTube Video**
                - [{resource_item.get('youtube_title', 'Video')}]({resource_item.get('youtube', '#')})
                """)
            
            with col2:
                st.markdown(f"""
                **Learning Resource**
                - [{resource_item.get('resource_title', 'Resource')}]({resource_item.get('resource', '#')})
                """)
    
    # ========== SECTION 12: EXPORT ANALYSIS ==========
    if has_export_data:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Export Analysis</h2>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Export as JSON
            json_str = json.dumps(data, indent=2)
            st.download_button(
                label="Download JSON Report",
                data=json_str,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )

        with col2:
            # Export as CSV (skills data)
            skills_df = pd.DataFrame({
                "Skill": extracted_skills,
                "Status": ["Extracted"] * len(extracted_skills)
            })
            csv = skills_df.to_csv(index=False)
            st.download_button(
                label="Download Skills CSV",
                data=csv,
                file_name=f"resume_skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    

def page_feedback():
    """Feedback Page"""
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 2rem;">Send Us Your Feedback</h2>
    <p style="text-align: center; color: #475569; margin-bottom: 2rem;">
        Help us improve the Resume Analyzer by sharing your thoughts and suggestions
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        
        # Feedback form
        with st.form("feedback_form"):
            name = st.text_input("👤 Your Name", placeholder="John Doe")
            email = st.text_input("📧 Your Email", placeholder="john@example.com")
            feedback_type = st.selectbox(
                "📝 Feedback Type",
                ["Bug Report", "Feature Request", "General Feedback", "Compliment"]
            )
            feedback_text = st.text_area(
                "💭 Your Feedback",
                placeholder="Share your thoughts here...",
                height=150
            )
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✉️ Submit Feedback", use_container_width=True)
            
            if submitted and name and email and feedback_text:
                st.markdown("""
                <div class="success-message">
                    <h3 style="margin: 0; font-size: 1.1rem;">✓ Thank You!</h3>
                    <p style="margin: 0.5rem 0 0 0;">Your feedback has been received successfully.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Store feedback (in real app, save to database)
                feedback_data = {
                    "timestamp": datetime.now().isoformat(),
                    "name": name,
                    "email": email,
                    "type": feedback_type,
                    "message": feedback_text
                }
                
                # Save to local JSON for demo
                feedback_file = "feedback_log.json"
                feedback_list = []
                if os.path.exists(feedback_file):
                    with open(feedback_file, "r") as f:
                        feedback_list = json.load(f)
                feedback_list.append(feedback_data)
                with open(feedback_file, "w") as f:
                    json.dump(feedback_list, f, indent=2)
            
            elif submitted:
                st.warning("⚠️ Please fill in all fields before submitting.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Additional info
    st.markdown("<div class='section-divider' style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Chat Support</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0;">Available 24/7</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Email Support</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0;">support@resumeai.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Social Media</h3>
            <p style="color: #475569; font-size: 0.9rem; margin: 0;">@ResumeAI</p>
        </div>
        """, unsafe_allow_html=True)

def page_settings():
    """Settings Page"""
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 2rem;">Settings & Preferences</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        
        # Account Settings
        st.markdown("""<h3 style="margin-top: 0;">Account Settings</h3>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", "John Doe")
        with col2:
            email = st.text_input("Email", "john@example.com")
        
        # Notification Settings
        st.markdown("""<h3>🔔 Notification Settings</h3>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            email_notifications = st.checkbox("Email Notifications", value=True)
            weekly_digest = st.checkbox("Weekly Digest", value=False)
        with col2:
            job_alerts = st.checkbox("Job Alerts", value=True)
            updates = st.checkbox("Product Updates", value=True)
        
        # Preference Settings
        st.markdown("""<h3>🎨 Preference Settings</h3>""", unsafe_allow_html=True)
        
        theme = st.selectbox("Theme", ["Dark", "Light", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        
        # Data Settings
        st.markdown("""<h3>📊 Data & Privacy</h3>""", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            data_sharing = st.checkbox("Allow Data Analytics", value=False)
        with col2:
            marketing = st.checkbox("Marketing Emails", value=False)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Changes", use_container_width=True):
                st.markdown("""
                <div class="success-message">
                    <p style="margin: 0;">✓ Settings saved successfully!</p>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            if st.button("🔄 Reset to Default", use_container_width=True):
                st.info("Settings reset to default values")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    # Initialize session state
    if "resume_uploaded" not in st.session_state:
        st.session_state.resume_uploaded = False
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    if "show_dashboard" not in st.session_state:
        st.session_state.show_dashboard = False
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    
    # Inject custom styles
    inject_custom_styles()
    
    # Create main title
    st.markdown("""
    <style>
        .main-title {
            text-align: center;
            padding: 2rem 0 1rem 0;
        }
    </style>
    <div class="main-title">
        <h1>AI Resume Analyzer</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    current_page = create_side_navigation()
    
    # Auto navigate to dashboard if analysis just completed
    if st.session_state.show_dashboard:
        st.session_state.show_dashboard = False
        current_page = "Analysis Dashboard"

    if current_page == "ATS Checker":
        render_ats_checker_page()
        return
    
    # MAIN SCREEN: Show upload form or dashboard based on state
    if not st.session_state.resume_uploaded or st.session_state.resume_data is None:
        # Display upload section on main screen
        if current_page == "Feedback":
            page_feedback()
        elif current_page == "Settings":
            page_settings()
        else:
            # Default: Show upload form on main screen
            display_upload_form()
    else:
        # Show dashboard view with sidebar routing
        if current_page == "Feedback":
            page_feedback()
        elif current_page == "Settings":
            page_settings()
        else:
            # Show the analysis dashboard
            page_dashboard()

if __name__ == "__main__":
    main()
