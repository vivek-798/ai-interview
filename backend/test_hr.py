from rounds.hr import load_hr_questions, evaluate_hr_answers

questions = load_hr_questions()

user_answers = {
    1: "I am a computer science student with strong skills and projects in Python",
    2: "My biggest strength is problem solving and continuous learning",
    3: "You should hire me because my skills add value to the company"
}

result = evaluate_hr_answers(questions, user_answers)
print(result)
