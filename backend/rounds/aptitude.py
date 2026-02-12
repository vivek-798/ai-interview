import json
import random

def load_aptitude_questions():
    with open("questions/aptitude_questions.json", "r") as f:
        questions = json.load(f)
    return questions

def conduct_aptitude_test():
    questions = load_aptitude_questions()

    num_questions = min(20, len(questions))
    selected = random.sample(questions, num_questions)

    correct = 0

    print("\n=== Aptitude Round ===")

    for q in selected:
        print("\n", q["question"])
        for option in q["options"]:
            print("-", option)

        user_input = input("Your answer: ")

        if user_input.strip().lower() == q["answer"].lower():
            correct += 1

    score_percentage = (correct / num_questions) * 100

    return {
        "total_questions": num_questions,
        "correct": correct,
        "Score_percentage": score_percentage
    }
