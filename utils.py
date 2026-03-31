import re
from typing import Set

try:
    import nltk
    from nltk.corpus import stopwords
except ModuleNotFoundError:
    nltk = None
    stopwords = None

def _get_stop_words() -> Set[str]:
    """
    Best-effort stopwords loader.
    - If NLTK is installed and corpus is available/downloadable, returns english stopwords.
    - Otherwise returns an empty set (so app never crashes).
    """
    if nltk is None or stopwords is None:
        return set()

    try:
        nltk.download("stopwords", quiet=True)
        return set(stopwords.words("english"))
    except Exception:
        return set()

STOP_WORDS = _get_stop_words()

# Predefined skill list
SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "pandas", "numpy", "data analysis",
    "dsa", "html", "css", "javascript", "react",
    "node", "aws", "cloud", "tensorflow", "keras",
    "scikit-learn", "r", "scala", "spark", "gcp",
    "docker", "kubernetes", "git", "linux", "windows",
    "salesforce", "sap", "oracle", "mongodb", "postgresql"
]

def clean_text(text):
    """Clean text by removing punctuation and stopwords"""
    if not isinstance(text, str) or not text.strip():
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS]
    
    return ' '.join(filtered_words)

def extract_skills(text, skills_list=SKILLS):
    """Extract skills from text using predefined skill list"""
    cleaned_text = clean_text(text)
    found = []
    
    for skill in skills_list:
        if skill in cleaned_text:
            if skill not in found:
                found.append(skill)
    
    return found