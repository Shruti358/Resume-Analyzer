import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import json

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords', quiet=True)

# Predefined skill list (all lowercase for case-insensitive matching)
SKILLS = [
    "python", "java", "c++", "sql", "machine learning",
    "deep learning", "pandas", "numpy", "data analysis",
    "dsa", "html", "css", "javascript", "react",
    "node", "aws", "cloud", "tensorflow"
]

def load_data(csv_file_path):
    """
    Load the CSV file containing resume_text and job_description columns.

    Args:
        csv_file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        df = pd.read_csv(csv_file_path)
        required_columns = ['resume_text', 'job_description']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {csv_file_path}")
    except Exception as e:
        raise Exception(f"Error loading CSV: {str(e)}")

def clean_text(text):
    """
    Clean the input text by converting to lowercase, removing punctuation, and removing stopwords.

    Args:
        text (str): Input text to clean.

    Returns:
        str: Cleaned text.
    """
    if not isinstance(text, str) or not text.strip():
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation using regex
    text = re.sub(r'[^\w\s]', '', text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]

    return ' '.join(filtered_words)

def extract_skills(text, skills_list):
    """
    Extract skills from the cleaned text that match the predefined skills list.

    Args:
        text (str): Cleaned text.
        skills_list (list): List of skills to check for.

    Returns:
        list: List of matched skills.
    """
    if not text:
        return []

    matched_skills = []
    for skill in skills_list:
        if skill in text:
            matched_skills.append(skill)

    return matched_skills

def preprocess_data(df):
    """
    Preprocess the DataFrame to extract skills from resume and job descriptions.

    Args:
        df (pd.DataFrame): DataFrame with resume_text and job_description columns.

    Returns:
        list: List of dictionaries with resume_skills and job_skills.
    """
    processed_data = []

    for _, row in df.iterrows():
        # Clean texts
        cleaned_resume = clean_text(row['resume_text'])
        cleaned_job = clean_text(row['job_description'])

        # Extract skills
        resume_skills = extract_skills(cleaned_resume, SKILLS)
        job_skills = extract_skills(cleaned_job, SKILLS)

        # Append to processed data
        processed_data.append({
            "resume_skills": resume_skills,
            "job_skills": job_skills
        })

    return processed_data

def save_to_json(data, output_file_path):
    """
    Save the processed data to a JSON file.

    Args:
        data (list): List of dictionaries to save.
        output_file_path (str): Path to the output JSON file.
    """
    try:
        with open(output_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Processed data saved to {output_file_path}")
    except Exception as e:
        raise Exception(f"Error saving JSON: {str(e)}")

def main():
    """
    Main function to run the preprocessing pipeline.
    """
    # File paths (adjust as needed)
    csv_file_path = 'data.csv'  # Replace with actual CSV file path
    output_file_path = 'processed_data.json'

    # Load data
    df = load_data(csv_file_path)

    # Preprocess data
    processed_data = preprocess_data(df)

    # Save to JSON
    save_to_json(processed_data, output_file_path)

if __name__ == "__main__":
    main()