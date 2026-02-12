import json
from utils.voice_input import listen_and_transcribe
from utils.voice_output import speak
from sentence_transformers import SentenceTransformer, util

# Load semantic model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_hr_questions():
    with open("questions/hr_questions.json", "r") as file:
        return json.load(file)


def conduct_voice_hr_round():
    questions = load_hr_questions()

    print("\n=== HR Round ===")

    total_score = 0
    feedback = []

    for q in questions:
        print("\n🤖 AI:", q["question"])
        speak(q["question"])

        print("🎙️ Speak your answer:")
        user_answer = listen_and_transcribe()
        print("📝 Transcribed:", user_answer)

        embeddings = model.encode(
            [q["expected_answer"], user_answer],
            convert_to_tensor=True
        )

        similarity = util.cos_sim(embeddings[0], embeddings[1]).item()

        score = round(similarity * 10, 2)
        total_score += score

        # 🔥 Adaptive HR response
        if similarity > 0.75:
            speak("That was a confident and well structured answer.")
        elif similarity > 0.4:
            speak("That answer is acceptable, but could be more structured.")
        else:
            speak("You may want to improve clarity and structure in your answer.")

        feedback.append({
            "question": q["question"],
            "score": score,
            "semantic_similarity": round(similarity, 2)
        })

    return {
        "total_score": round(total_score, 2),
        "max_score": len(questions) * 10,
        "feedback": feedback
    }
