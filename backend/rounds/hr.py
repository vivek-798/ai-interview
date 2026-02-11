import json

def load_hr_questions():
    with open("questions/hr_questions.json", "r") as file:
        return json.load(file)


def evaluate_hr_answers(questions, user_answers):
    total_score = 0
    max_score = len(questions) * 10
    feedback = []

    for q in questions:
        qid = q["id"]
        keywords = q["keywords"]
        answer = user_answers.get(qid, "").lower()

        matched = 0
        for kw in keywords:
            if kw in answer:
                matched += 1

        score = (matched / len(keywords)) * 10
        total_score += score

        feedback.append({
            "question": q["question"],
            "score": round(score, 2),
            "matched_keywords": matched,
            "expected_keywords": keywords
        })

    return {
        "total_score": round(total_score, 2),
        "max_score": max_score,
        "feedback": feedback
    }
