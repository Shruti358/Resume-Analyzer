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
            background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%) !important;
            color: #333333;
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
            background: radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 10% 10%, rgba(102, 126, 234, 0.05) 0%, transparent 40%),
                        radial-gradient(circle at 90% 20%, rgba(118, 75, 162, 0.05) 0%, transparent 35%);
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
            background: radial-gradient(circle, rgba(102, 126, 234, 0.06) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: float 8s ease-in-out infinite;
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
            content: '◇';
            position: fixed;
            top: 10%;
            right: 2%;
            font-size: 80px;
            color: rgba(102, 126, 234, 0.08);
            z-index: 0;
            pointer-events: none;
            animation: float 12s ease-in-out infinite;
        }
        
        .stMainBlockContainer::after {
            content: '●';
            position: fixed;
            bottom: 15%;
            left: 3%;
            font-size: 120px;
            color: rgba(118, 75, 162, 0.06);
            z-index: 0;
            pointer-events: none;
            animation: float 15s ease-in-out infinite reverse;
        }
        
        /* Top right accent */
        [data-testid="stSidebar"]::before {
            content: '◇';
            position: absolute;
            top: 20%;
            right: -30px;
            font-size: 60px;
            color: rgba(102, 126, 234, 0.1);
            z-index: 1;
            pointer-events: none;
            animation: float 10s ease-in-out infinite;
        }
        
        /* Bottom left accent */
        [data-testid="stSidebar"]::after {
            content: '○';
            position: absolute;
            bottom: 10%;
            left: -20px;
            font-size: 100px;
            color: rgba(118, 75, 162, 0.08);
            z-index: 0;
            pointer-events: none;
            animation: float 13s ease-in-out infinite;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%) !important;
            border-right: 1px solid #e0e0e0 !important;
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
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 12px !important;
            border: 1px solid #e0e0e0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
            transition: all 0.3s ease !important;
            animation: popUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }
        
        .glass-card:hover {
            background: rgba(255, 255, 255, 1) !important;
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.6), 0 8px 24px rgba(0, 0, 0, 0.12) !important;
            transform: translateY(-4px) !important;
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
                box-shadow: 0 0 5px rgba(102, 126, 234, 0.5);
            }
            50% {
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
            }
        }
        
        /* Animation: Fluorescent Glow */
        @keyframes fluorescent-glow {
            0%, 100% {
                box-shadow: 0 0 10px rgba(102, 126, 234, 0.8), 0 0 20px rgba(102, 126, 234, 0.6);
            }
            50% {
                box-shadow: 0 0 20px rgba(102, 126, 234, 1), 0 0 40px rgba(102, 126, 234, 0.8);
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
            animation: glow 2s ease-in-out infinite;
        }
        
        .fluorescent-glow {
            animation: fluorescent-glow 3s ease-in-out infinite;
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            text-align: center !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -1px !important;
        }
        
        h2 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #333333 !important;
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 0.75rem 2rem !important;
            border-radius: 8px !important;
            border: none !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }
        
        .stButton > button:hover {
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 0 8px 24px rgba(102, 126, 234, 0.4) !important;
            transform: translateY(-3px) !important;
        }
        
        .stButton > button:active {
            transform: translateY(-1px) !important;
        }
        
        /* Secondary Button */
        .secondary-button > button {
            background: rgba(102, 126, 234, 0.1) !important;
            color: #667eea !important;
            border: 1px solid #667eea !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            border-radius: 8px !important;
        }
        
        .secondary-button > button:hover {
            background: rgba(102, 126, 234, 0.15) !important;
            border-color: #667eea !important;
        }
        
        /* Input Fields */
        .stTextInput input, .stTextArea textarea {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            color: #333333 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            caret-color: #667eea !important;
        }
        
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #999999 !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            background: rgba(255, 255, 255, 1) !important;
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
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
            background: rgba(102, 126, 234, 0.05) !important;
            border: 2px dashed #667eea !important;
            border-radius: 8px !important;
            padding: 2rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            background: rgba(102, 126, 234, 0.1) !important;
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* File uploader button */
        .stFileUploader button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            border: none !important;
            cursor: pointer !important;
        }
        
        .stFileUploader button:hover {
            opacity: 0.9 !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
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
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(102, 126, 234, 0.05)) !important;
            border: 1px solid #667eea !important;
            color: #667eea !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 20px !important;
            margin: 0.4rem !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        .skill-tag:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(102, 126, 234, 0.15)) !important;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.6), 0 4px 12px rgba(102, 126, 234, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        .missing-tag {
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.1), rgba(255, 71, 87, 0.05)) !important;
            border: 1px solid #ff4757 !important;
            color: #d32f2f !important;
            box-shadow: 0 2px 8px rgba(255, 71, 87, 0.1) !important;
        }
        
        .missing-tag:hover {
            background: linear-gradient(135deg, rgba(255, 71, 87, 0.15), rgba(255, 71, 87, 0.1)) !important;
            box-shadow: 0 4px 12px rgba(255, 71, 87, 0.15) !important;
            transform: translateY(-2px) !important;
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
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
            background: rgba(33, 150, 243, 0.1) !important;
            border: 1px solid #2196f3 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            color: #1565c0 !important;
        }
        
        /* Section Divider */
        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
            margin: 2rem 0;
        }
        
        /* Stat Card */
        .stat-card {
            background: rgba(102, 126, 234, 0.05) !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            animation: popUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }
        
        .stat-card:hover {
            background: rgba(102, 126, 234, 0.1) !important;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.5), 0 4px 12px rgba(0, 0, 0, 0.08) !important;
            transform: translateY(-6px) !important;
        }
        
        .stat-value {
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            -webkit-background-clip: text !important;
        
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
                background: rgba(102, 126, 234, 0.2);
            }
            .nav-item-active {
                background: rgba(102, 126, 234, 0.3);
                border-left: 3px solid #667eea;
                padding-left: calc(1rem - 3px);
            }
        </style>
        <div class="sidebar-header">
            <h3 style="margin:0; font-size:1.5rem;">Resume AI</h3>
            <p style="margin:0.5rem 0 0 0; font-size:0.85rem; color:rgba(255,255,255,0.6);">Your Smart Career Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        page = st.radio(
            "Navigate",
            ["Upload Resume", "Analysis Dashboard", "Feedback", "Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
        <div style="padding: 1rem; font-size: 0.85rem; color: rgba(255,255,255,0.5); text-align: center;">
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
            color: rgba(255,255,255,0.7);
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
        <p style="text-align: center; color: rgba(255,255,255,0.6); font-size: 1rem; margin-bottom: 1.5rem;">
            Get AI-powered insights about your resume in seconds
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .upload-message {
                text-align: center;
                color: rgba(255,255,255,0.7);
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .file-info {
                text-align: center;
                color: rgba(102, 126, 234, 0.7);
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
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.95rem;">{uploaded_file.name}</p>
                <p style="margin: 0.25rem 0 0 0; color: rgba(255,255,255,0.5); font-size: 0.85rem;">{uploaded_file.size / 1024:.1f} KB</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Job Description Section
            st.markdown("""
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.75rem;">Job Description (Optional)</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0 0 1rem 0;">Paste the job description to get better skill matching</p>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Paste job description here",
                placeholder="Software Engineer - Required: Python, React, AWS, Docker, System Design...",
                height=120,
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume", use_container_width=True, key="analyze_btn"):
                    with st.spinner("Analyzing your resume..."):
                        # Analyze the resume
                        analysis_result = analyze_resume(uploaded_file, job_description)
                        
                        # Store in session
                        st.session_state.resume_uploaded = True
                        st.session_state.resume_data = analysis_result
                        st.session_state.current_file = uploaded_file.name
                        st.session_state.show_dashboard = True
                        
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
                <h3 style="font-size: 1.1rem; margin: 0.5rem 0; color: #ffffff;">{title}</h3>
                <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6); margin: 0;">{desc}</p>
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
            "recommendations": [],
            "resume_stats": {"pages": 0}
        }

def create_skill_match_chart(extracted, missing, recommended):
    """Create interactive skill chart"""
    # Handle recommended as list of dicts or strings
    if recommended and isinstance(recommended[0], dict):
        recommended_count = len(recommended)
    else:
        recommended_count = len(recommended)
    
    categories = ['Extracted\nSkills', 'Missing\nSkills', 'Recommended\nSkills']
    values = [len(extracted), len(missing), recommended_count]
    colors = ['#667eea', '#ff4757', '#2ed573']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(color=colors),
            text=values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        )
    ])
    
    fig.update_layout(
        title="Skills Analysis Overview",
        title_font_size=18,
        title_x=0.5,
        xaxis_title="",
        yaxis_title="Number of Skills",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#ffffff'),
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False, zeroline=False, color='rgba(255,255,255,0.3)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)', color='rgba(255,255,255,0.3)'),
    )
    
    return fig

def create_skill_distribution_chart(extracted, missing, recommended):
    """Create pie chart for skill distribution"""
    # Handle recommended as list of dicts or strings
    if recommended and isinstance(recommended[0], dict):
        recommended_count = len(recommended)
    else:
        recommended_count = len(recommended)
    
    labels = ['Extracted Skills', 'Missing Skills', 'Recommended Skills']
    sizes = [len(extracted), len(missing), recommended_count]
    colors = ['#667eea', '#ff4757', '#2ed573']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=sizes,
        marker=dict(colors=colors),
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>',
    )])
    
    fig.update_layout(
        title="Skill Distribution",
        title_font_size=18,
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#ffffff'),
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True,
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
        <div style="background: rgba(255,255,255,0.08); border-radius: 50px; height: 8px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);">
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: {percentage}%; border-radius: 50px; transition: width 1s ease-in-out;"></div>
        </div>
        <p style="text-align: center; margin-top: 0.75rem; font-size: 0.95rem; color: rgba(255,255,255,0.7);">
            {value}% Match
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
            color: rgba(255,255,255,0.7);
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
        <p style="text-align: center; color: rgba(255,255,255,0.6); font-size: 1rem; margin-bottom: 1.5rem;">
            Get AI-powered insights about your resume in seconds
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .upload-message {
                text-align: center;
                color: rgba(255,255,255,0.7);
                margin-bottom: 1rem;
                font-size: 0.95rem;
            }
            .file-info {
                text-align: center;
                color: rgba(102, 126, 234, 0.7);
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
                <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7); font-size: 0.95rem;">{uploaded_file.name}</p>
                <p style="margin: 0.25rem 0 0 0; color: rgba(255,255,255,0.5); font-size: 0.85rem;">{uploaded_file.size / 1024:.1f} KB</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Job Description Section
            st.markdown("""
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.75rem;">Job Description (Optional)</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0 0 1rem 0;">Paste the job description to get better skill matching</p>
            """, unsafe_allow_html=True)
            
            job_description = st.text_area(
                "Paste job description here",
                placeholder="Software Engineer - Required: Python, React, AWS, Docker, System Design...",
                height=120,
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Analyze Resume", use_container_width=True, key="analyze_btn"):
                    with st.spinner("Analyzing your resume..."):
                        # Analyze the resume
                        analysis_result = analyze_resume(uploaded_file, job_description)
                        
                        # Store in session
                        st.session_state.resume_uploaded = True
                        st.session_state.resume_data = analysis_result
                        st.session_state.current_file = uploaded_file.name
                        st.session_state.show_dashboard = True
                        
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
                <h3 style="font-size: 1.1rem; margin: 0.5rem 0; color: #ffffff;">{title}</h3>
                <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6); margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def page_dashboard():
    """Analysis Dashboard Page"""
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
    extra_skills = data.get('skills', {}).get('extra', [])
    match_percentage = data.get('match_percentage', 0)
    recommendations = data.get('recommendations', [])
    resume_stats = data.get('resume_stats', {})
    learning_resources = data.get('learning_resources', {})
    
    # Header
    name = basic_info.get('name', 'Unknown')
    email = basic_info.get('email', 'Not Found')
    phone = basic_info.get('phone', 'Not Found')
    pages = resume_stats.get('pages', 0)
    
    st.markdown(f"""
    <h2>Analysis Report for {name}</h2>
    <p style="color: rgba(255,255,255,0.6); margin-bottom: 2rem;">
        {email} | {phone} | {pages} page(s)
    </p>
    """, unsafe_allow_html=True)
    
    # ========== SECTION 1: BASIC INFO ==========
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">Basic Information</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Name:** {name}")
    with col2:
        st.markdown(f"**Email:** {email}")
    with col3:
        st.markdown(f"**Phone:** {phone}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 2: EXTRACTED SKILLS ==========
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">Extracted Skills</h2>
    <p style="color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
        Found {count} relevant technical skills in your resume
    </p>
    """.replace("{count}", str(len(extracted_skills))), unsafe_allow_html=True)
    
    st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
    if extracted_skills:
        display_skill_tags(extracted_skills, "skill")
    else:
        st.info("No technical skills detected. Try adding specific skills to your resume.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 3: MATCHED SKILLS ==========
    if matched_skills:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Matched Skills</h2>
        <p style="color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
            These skills are present in both your resume and the job description
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        display_skill_tags(matched_skills, "skill")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 4: MISSING SKILLS ==========
    if missing_skills:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Missing Skills</h2>
        <p style="color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
            These are important skills for your target role that aren't in your resume
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        display_skill_tags(missing_skills, "missing")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 4B: RECOMMENDED SKILLS ==========
    if recommendations:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Recommended Skills</h2>
        <p style="color: rgba(255,255,255,0.6); margin-bottom: 1rem;">
            Priority skills to master from the missing skills list
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        recommended_skill_names = [rec.get('skill', '') for rec in recommendations]
        display_skill_tags(recommended_skill_names, "recommended")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 5: MATCH PERCENTAGE ==========
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">Overall Match Score</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="progress-circle">
            <div class="progress-value">{match_percentage}%</div>
            <div class="progress-label">Skills Match</div>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-top: 1rem;">
                Your resume matches {match_percentage}% of required skills
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Animated progress bar
        st.markdown(create_animated_progress(match_percentage), unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 6: INTERACTIVE CHARTS ==========
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">Visual Analytics</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        fig1 = create_skill_match_chart(
            extracted_skills,
            missing_skills,
            recommendations
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class="glass-card" style="padding: 1.5rem;">""", unsafe_allow_html=True)
        fig2 = create_skill_distribution_chart(
            extracted_skills,
            missing_skills,
            recommendations
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 7: EDUCATION ==========
    if data.get('education'):
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Education</h2>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        for edu in data['education']:
            st.markdown(f"""
            - **{edu.get('degree', 'Not Specified')}** in {edu.get('branch', 'Not Mentioned')}
              - {edu.get('university', 'Not Mentioned')}
            """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 8: EXPERIENCE ==========
    if data.get('experience'):
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Work Experience</h2>
        """, unsafe_allow_html=True)
        
        st.markdown("""<div class="glass-card">""", unsafe_allow_html=True)
        for exp in data['experience']:
            st.markdown(f"""
            - **{exp.get('position', 'Not Specified')}** at {exp.get('company', 'Not Specified')}
              - Duration: {exp.get('duration', 'Not Specified')}
            """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ========== SECTION 9: STATISTICS ==========
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">Statistics</h2>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("Extracted Skills", resume_stats.get('skills_count', 0)),
        ("Missing Skills", len(missing_skills)),
        ("Matched Skills", len(matched_skills)),
        ("Resume Pages", pages)
    ]
    
    for col, (label, value) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ========== SECTION 10: LEARNING RESOURCES ==========
    if recommendations:
        st.markdown("""
        <h2 style="margin-top: 2.5rem;">Recommended Learning Resources</h2>
        <p style="color: rgba(255,255,255,0.6); margin-bottom: 1.5rem;">
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
    st.markdown("""
    <h2 style="margin-top: 2.5rem;">📥 Export Analysis</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as JSON
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="📄 Download JSON Report",
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
            label="📊 Download Skills CSV",
            data=csv,
            file_name=f"resume_skills_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

def page_feedback():
    """Feedback Page"""
    st.markdown("""
    <h2 style="text-align: center; margin-bottom: 2rem;">Send Us Your Feedback</h2>
    <p style="text-align: center; color: rgba(255,255,255,0.6); margin-bottom: 2rem;">
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
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">Available 24/7</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Email Support</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">support@resumeai.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Social Media</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem; margin: 0;">@ResumeAI</p>
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
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
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
