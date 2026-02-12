import json
import random
from utils.voice_input import listen_and_transcribe
from utils.voice_output import speak
from sentence_transformers import SentenceTransformer, util

# Load semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_technical_questions():
    with open("questions/python_questions.json", "r") as f:
        return json.load(f)


def select_questions(resume_skills):
    questions = load_technical_questions()

    filtered = [
        q for q in questions
        if q["skill"].lower() in [s.lower() for s in resume_skills]
    ]

    if len(filtered) < 3:
        filtered = questions  # fallback if not enough skill match

    return random.sample(filtered, min(3, len(filtered)))

def conduct_voice_technical_round(questions):
    print("\n=== Technical Round ===")

    answers = {}

    for q in questions:

        print("\n🤖 AI:", q["question"])
        speak(q["question"])

        print("🎙️ Your answer:")
        user_answer = listen_and_transcribe()
        print("📝 You:", user_answer)

        # 🔥 Follow-up Question
        follow_up = "Can you give me a real-world example?"
        print("\n🤖 AI:", follow_up)
        speak(follow_up)

        example_answer = listen_and_transcribe()
        print("📝 You:", example_answer)

        # Combine both answers
        combined_answer = user_answer + " " + example_answer
        answers[q["id"]] = combined_answer

    return answers
