import json

def load_questions():
    with open("questions/python_questions.json", "r") as file:
        return json.load(file)
def select_questions(resume_skills):
    questions = load_questions()
    selected_questions = []


    for q in questions:
        if q["skill"] in resume_skills:
            selected_questions.append(q)

    return selected_questions


# # Evaluate answers using keyword matching (NORMAL VERSION)
def evaluate_answers(questions,user_answers):
    total_score=0
    max_score=len(questions)*10
    detailed_feedback=[]

    for q in questions:
        qid=q["id"]
        keywords=q["keywords"]
        answer = user_answers.get(qid,"").lower()

        match_count=0
        for kw in keywords:
            if kw in answer:
                match_count+=1

        score=(match_count/len(keywords))*10
        total_score+=score


        detailed_feedback.append({
            "question": q["question"],
            "score": round(score, 2),
            "matched_keywords": match_count,
            "expected_keywords": keywords
        })
    return {
        "total_score": round(total_score, 2),
        "max_score": max_score,
        "feedback": detailed_feedback
    }