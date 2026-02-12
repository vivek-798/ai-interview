# app.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "interview_os_secret"
CORS(app, supports_credentials=True)


# ===============================
# TECHNICAL QUESTIONS (STATIC FOR HACKATHON)
# ===============================

TECHNICAL_QUESTIONS = [
    "What is a stack in Python?",
    "Explain list vs tuple.",
    "What is a dictionary in Python?"
]


# ===============================
# RESUME UPLOAD
# ===============================

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    upload_path = "resumes/uploads"
    os.makedirs(upload_path, exist_ok=True)

    file_path = os.path.join(upload_path, file.filename)
    file.save(file_path)

    # For hackathon demo we just return success
    return jsonify({
        "message": "Resume uploaded successfully",
        "filename": file.filename
    })


# ===============================
# APTITUDE SUBMIT
# ===============================

@app.route("/submit_aptitude", methods=["POST"])
def submit_aptitude():
    data = request.json
    user_answers = data.get("answers", {})

    correct_answers = {
        0: "5 days",
        1: "32",
        2: "10 m/s"
    }

    score = 0
    for index, answer in user_answers.items():
        if correct_answers[int(index)] == answer:
            score += 1

    percentage = (score / len(correct_answers)) * 100

    session["aptitude"] = {
        "score": score,
        "percentage": percentage
    }

    return jsonify({
        "message": "Aptitude completed",
        "score": score,
        "percentage": percentage
    })


# ===============================
# GET ALL TECHNICAL QUESTIONS
# ===============================

@app.route("/get_all_technical_questions", methods=["GET"])
def get_all_technical_questions():
    return jsonify({
        "questions": TECHNICAL_QUESTIONS
    })


# ===============================
# SAVE TECHNICAL RESULTS
# ===============================

@app.route("/submit_technical", methods=["POST"])
def submit_technical():
    data = request.json
    answers = data.get("answers", [])

    session["technical"] = {
        "total_questions": len(TECHNICAL_QUESTIONS),
        "answers": answers
    }

    return jsonify({
        "message": "Technical round completed"
    })
# hr round


hr_questions = [
    "Tell me about yourself.",
    "What is your biggest strength?",
    "Why should we hire you?"
]

@app.route("/get_hr_questions")
def get_hr_questions():
    return jsonify({"questions": hr_questions})


# ===============================
# FINAL REPORT
# ===============================

@app.route("/final_result", methods=["GET"])
def final_result():

    # Get data from session (safe defaults)
    aptitude = session.get("aptitude", {"score": 0, "percentage": 0})
    technical = session.get("technical", {"score": 70})
    hr = session.get("hr", {"score": 65})

    # 🔥 For now simple calculation
    overall = (
        aptitude.get("percentage", 0) +
        technical.get("score", 0) +
        hr.get("score", 0)
    ) / 3

    if overall >= 75:
        decision = "Strong Hire"
    elif overall >= 55:
        decision = "Consider"
    else:
        decision = "Needs Improvement"

    return jsonify({
        "overall_score": round(overall, 2),
        "decision": decision,
        "sections": {
            "Aptitude": aptitude.get("percentage", 0),
            "Technical": technical.get("score", 70),
            "HR": hr.get("score", 65)
        }
    })


# ===============================
# RUN SERVER
# ===============================

if __name__ == "__main__":
    app.run(debug=True)
