def extract_skills(text):
    skills = ["python","java","sql","ml","pandas"]
    found = []
    
    for skill in skills:
        if skill in text.lower():
            found.append(skill)
    
    return found