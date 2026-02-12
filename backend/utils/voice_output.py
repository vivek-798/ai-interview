import pyttsx3
import time

engine = pyttsx3.init()

engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)  # small natural pause
