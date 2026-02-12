# app.py
# Main controller of Interview OS
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from rounds.communication import communication_round
from rounds.technical import conduct_voice_technical_round, select_questions
# from rounds.aptitude import conduct_aptitude_test
from rounds.coding import conduct_coding_round
from rounds.hr import conduct_voice_hr_round
from resume_parser.extractor import parse_resume
from rounds.video_hr import video_hr_round
from utils.voice_output import speak

import random
from sentence_transformers import SentenceTransformer, util


app = Flask(__name__)
app.secret_key = "interview_os_secret"
CORS(app)


technical_questions = [
    "What is a list in Python?",
    "What is a stack?",
    "Explain list vs tuple.",
    "What is a dictionary in Python?"
]
@app.route("/get_technical_question", methods=["GET"])
def get_technical_question():
    return jsonify({
        "question": "What is a stack in Python?"
    })
@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]

    upload_path = "resumes/uploads"
    os.makedirs(upload_path, exist_ok=True)

    file_path = os.path.join(upload_path, file.filename)
    file.save(file_path)

    # Parse resume
    from resume_parser.extractor import parse_resume
    result = parse_resume(file_path)

    return jsonify(result)

app.secret_key = "interview_os_secret"  # add this once

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

    # 🔥 Store in session
    session["aptitude"] = {
        "score": score,
        "percentage": percentage
    }

    return jsonify({
        "message": "Aptitude completed"
    })
@app.route("/final_report", methods=["GET"])
def final_report():

    report = {
        "aptitude": session.get("aptitude", {}),
        "technical": session.get("technical", {}),
        "coding": session.get("coding", {}),
        "communication": session.get("communication", {}),
        "hr": session.get("hr", {})
    }

    return jsonify(report)
@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["audio"]

    audio_path = "temp.wav"
    audio.save(audio_path)

    result = whisper_model.transcribe(audio_path)

    return jsonify({"text": result["text"]})

# 🔥 Load semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# ==============================
# AI FEEDBACK ENGINE
# ==============================

def generate_ai_feedback(report):
    base_feedback_options = [
        "The candidate shows strong analytical and problem solving skills.",
        "The candidate demonstrates solid technical understanding.",
        "Communication skills require further improvement.",
        "The candidate performs well in coding challenges.",
        "The candidate shows confidence in structured interviews.",
        "The candidate needs to improve conceptual clarity."
    ]

    text_data = report["communication"]["transcript"]

    embeddings = model.encode([text_data] + base_feedback_options, convert_to_tensor=True)

    query_embedding = embeddings[0]
    option_embeddings = embeddings[1:]

    similarities = util.cos_sim(query_embedding, option_embeddings)[0]
    top_indices = similarities.argsort(descending=True)[:2]

    selected_feedback = [base_feedback_options[i] for i in top_indices]

    return selected_feedback


# ==============================
# FINAL DECISION ENGINE
# ==============================

def calculate_final_decision(report):

    total_score = 0
    count = 0

    if "technical" in report:
        total_score += (report["technical"]["total_score"] /
                        report["technical"]["max_score"]) * 100
        count += 1

    if "coding" in report:
        total_score += report["coding"]["score"]
        count += 1

    if "communication" in report:
        total_score += (report["communication"]["score"] / 10) * 100
        count += 1

    if "hr" in report:
        total_score += (report["hr"]["total_score"] /
                        report["hr"]["max_score"]) * 100
        count += 1

    if "video_hr" in report:
        total_score += (report["video_hr"]["confidence_score"] / 10) * 100
        count += 1

    final_percentage = total_score / count if count > 0 else 0

    if final_percentage >= 75:
        recommendation = "Strong Hire"
    elif final_percentage >= 55:
        recommendation = "Consider"
    else:
        recommendation = "Needs Improvement"

    return round(final_percentage, 2), recommendation



# ==============================
# STRENGTH & WEAKNESS ANALYSIS
# ==============================

def analyze_strengths_weaknesses(report):

    scores = {}

    scores["Aptitude"] = report["aptitude"]["Score_percentage"]
    scores["Technical"] = (report["technical"]["total_score"] / report["technical"]["max_score"]) * 100
    scores["Coding"] = report["coding"]["score"]
    scores["Communication"] = (report["communication"]["score"] / 10) * 100
    scores["HR"] = (report["hr"]["total_score"] / report["hr"]["max_score"]) * 100

    strongest = max(scores, key=scores.get)
    weakest = min(scores, key=scores.get)

    return strongest, weakest, scores


# ==============================
# MAIN INTERVIEW FLOW
# ==============================

def run_interview():

    print("=== Interview OS Started ===")

    # 1️⃣ Resume Parsing
    resume_data = parse_resume("resumes/uploads/sample_resume.pdf")
    resume_skills = resume_data["skills"]

    # 2️⃣ Aptitude Round
    # aptitude_result = conduct_aptitude_test()

    # 3️⃣ Technical Round (Voice-based + Semantic scoring)
    technical_questions = select_questions(resume_skills)
    technical_answers = conduct_voice_technical_round(technical_questions)
    technical_result = evaluate_answers(technical_questions, technical_answers)

    # 4️⃣ Coding Round
    user_code = """
def reverse_string(s):
    return s[::-1]
"""
    coding_test_cases = [
        {"input": "hello", "output": "olleh"},
        {"input": "python", "output": "nohtyp"}
    ]

    coding_result = conduct_coding_round()

    # 5️⃣ Communication Round (Voice)
    communication_result = communication_round()

    # 6️⃣ HR Round
    hr_result = conduct_voice_hr_round()

    speak("Now we will move to the final video evaluation round.")

    video_result = video_hr_round(duration=20)




    # ==========================
    # FINAL REPORT
    # ==========================

    final_report = {
        # "aptitude": aptitude_result,
        "technical": technical_result,
        "coding": coding_result,
        "communication": communication_result,
        "hr": hr_result,
        "video_hr": video_result,

    }

    print("\n=== FINAL REPORT ===")
    print(final_report)

    # Overall Score
    final_score, decision = calculate_final_decision(final_report)

    print("\n=== OVERALL RESULT ===")
    print("Final Score:", round(final_score, 2), "%")
    print("Recommendation:", decision)
    speak("The interview has concluded.")
    speak(f"Your final score is {round(final_score,2)} percent.")
    speak(f"Recommendation: {decision}.")

    # Performance Analysis
    strongest, weakest, detailed_scores = analyze_strengths_weaknesses(final_report)

    print("\n=== PERFORMANCE ANALYSIS ===")
    print("Strongest Area:", strongest)
    print("Needs Improvement:", weakest)

    print("\nDetailed Scores:")
    for area, score in detailed_scores.items():
        print(f"{area}: {round(score, 2)}%")

    # AI Generated Feedback
    ai_feedback = generate_ai_feedback(final_report)

    print("\n=== AI GENERATED FEEDBACK ===")
    for line in ai_feedback:
        print("-", line)


if __name__ == "__main__":
    app.run(debug=True)
