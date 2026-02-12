from utils.voice_input import listen_and_transcribe
from utils.voice_output import speak


def communication_round():

    print("\n=== Communication Round ===")

    speak("Now I would like to assess your communication skills.")
    speak("Please introduce yourself and talk about your background, skills, and interests for thirty seconds.")

    user_answer = listen_and_transcribe(duration=15)

    print("📝 You:", user_answer)

    word_count = len(user_answer.split())

    if word_count > 40:
        score = 9
        feedback = "Excellent communication."
    elif word_count > 20:
        score = 6
        feedback = "Good communication."
    else:
        score = 3
        feedback = "Needs improvement."

    speak("Thank you. That was helpful.")

    return {
        "score": score,
        "word_count": word_count,
        "feedback": feedback,
        "transcript": user_answer
    }
