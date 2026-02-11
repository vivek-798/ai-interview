import whisper
import sounddevice as sd
import numpy as np

MODEL_NAME = "base"
SAMPLE_RATE = 16000
DURATION = 8  # ⬅️ increased duration (important)


def listen_and_transcribe():
    print("🎙️ Recording... Speak clearly and continuously")

    # Record audio
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.float32
    )
    sd.wait()

    # Convert to 1D
    audio = audio.flatten()

    # 🔥 NORMALIZE AUDIO (CRITICAL FIX)
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    # Load model once (cache-friendly)
    model = whisper.load_model(MODEL_NAME)

    # 🔥 FORCE LANGUAGE + DISABLE SILENCE FILTERING
    result = model.transcribe(
        audio,
        language="en",
        fp16=False,
        temperature=0,
        no_speech_threshold=0.1,
        logprob_threshold=-1.0,
        condition_on_previous_text=False
    )

    text = result.get("text", "").strip()

    # Debug fallback
    if not text:
        return "[No speech detected – please speak louder and continuously]"

    return text
