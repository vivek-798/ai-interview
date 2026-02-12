import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
import sounddevice as sd
import numpy as np
import threading
import whisper
import tempfile
import scipy.io.wavfile as wav


model = whisper.load_model("base")

def listen_and_transcribe():
    # Set default device (optional, but helps if you have multiple audio devices)
    # You might need to change the device number. Run python -m sounddevice to list devices
    # sd.default.device = 1

    print("🎙️ Recording... Press ENTER to stop.")

    samplerate = 16000
    recording = []
    is_recording = True

    def stop_recording():
        nonlocal is_recording
        input()  # wait for Enter key
        is_recording = False

    thread = threading.Thread(target=stop_recording)
    thread.start()

    try:
        with sd.InputStream(samplerate=samplerate, channels=1) as stream:
            while is_recording:
                audio_chunk, _ = stream.read(1024)
                recording.append(audio_chunk)

        audio_data = np.concatenate(recording)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav.write(tmp.name, samplerate, audio_data)
            try:
                result = model.transcribe(tmp.name)
                text = result["text"].strip()
            except Exception as e:
                print(f"Transcription error: {e}")
                text = "[Transcription failed]"

    except Exception as e:
        print(f"Recording error: {e}")
        return "[No audio recorded]"

    if text == "":
        print("No speech detected")
        return "[No speech detected]"

    return text

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
