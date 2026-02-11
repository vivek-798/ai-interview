import json

def load_aptitude_questions():
    with open("questions/aptitude_questions.json", "r") as file:
        return json.load(file)

def evaluate_aptitude(user_answers):
    questions=load_aptitude_questions()
    score=0

    for q in questions:
        qid = q["id"]
        if user_answers.get(qid)==q["answer"]:
            score+=1

    return {
        "total_questions" : len(questions),
        "correct":score,
        "Score_percentage":(score/len(questions))*100
        
    }