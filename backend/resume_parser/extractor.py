from resume_parser.parser import extract_text_from_pdf

SKILL_KEYWORDS = [
    "python", "java", "sql", "flask", "django",
    "html", "css", "javascript", "react",
    "machine learning", "data structures"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILL_KEYWORDS:
        if skill in text.lower():
            found_skills.append(skill)
    return found_skills


def parse_resume(pdf_path):
    # 1. Extract raw text from PDF
    raw_text = extract_text_from_pdf(pdf_path)

    # 2. Extract skills
    skills = extract_skills(raw_text)

    # 3. Return structured data
    return {
        "skills": skills,
        "raw_text": raw_text
    }
