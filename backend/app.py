# app.py
# Main controller of Interview OS

from resume_parser.extractor import parse_resume
from rounds.aptitude import evaluate_aptitude
from rounds.technical import select_questions, evaluate_answers
from rounds.coding import evaluate_code
from rounds.hr import load_hr_questions, evaluate_hr_answers


def run_interview():
    print("=== Interview OS Started ===")

    # 1. Resume Parsing
    resume_data = parse_resume("resumes/uploads/sample_resume.pdf")
    resume_skills = resume_data["skills"]

    # 2. Aptitude Round
    aptitude_answers = {
        1: "5 days",
        2: "32",
        3: "10 m/s"
    }
    aptitude_result = evaluate_aptitude(aptitude_answers)

    # 3. Technical Round
    technical_questions = select_questions(resume_skills)
    technical_answers = {
        1: "A list is mutable and ordered collection",
        2: "Tuple is immutable",
        3: "Stack follows LIFO",
        4: "List mutable tuple immutable"
    }
    technical_result = evaluate_answers(technical_questions, technical_answers)

    # 4. Coding Round
    user_code = """
def reverse_string(s):
    return s[::-1]
"""
    coding_test_cases = [
        {"input": "hello", "output": "olleh"},
        {"input": "python", "output": "nohtyp"}
    ]
    coding_result = evaluate_code(user_code, "reverse_string", coding_test_cases)

    # 5. HR Round
    hr_questions = load_hr_questions()
    hr_answers = {
        1: "I am a passionate developer with strong skills",
        2: "Problem solving is my strength",
        3: "I bring value through skills"
    }
    hr_result = evaluate_hr_answers(hr_questions, hr_answers)

    # 6. Final Report
    final_report = {
        "aptitude": aptitude_result,
        "technical": technical_result,
        "coding": coding_result,
        "hr": hr_result
    }

    print("\n=== FINAL REPORT ===")
    print(final_report)


if __name__ == "__main__":
    run_interview()
