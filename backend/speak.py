import pyttsx3

# Initialize engine ONCE (VERY IMPORTANT)
engine = pyttsx3.init()

def robo_anchor():
    engine.setProperty('rate', 145)
    engine.setProperty('volume', 1.0)

    print("🤖 Robo Anchor Started...\n")

    script = """
    Hello everyone.
    I am your robo anchor.
    Welcome to today's program.

    Let us begin with the highlights.

    First news.
    Python is one of the most powerful programming languages in the world.

    Second news.
    Artificial intelligence is changing the future of technology.

    Third news.
    Students who practice daily will achieve great success.

    That brings us to the end of today's session.
    Thank you for listening.
    Have a great day ahead.
    """

    engine.say(script)
    engine.runAndWait()

if __name__ == "__main__":
    robo_anchor()
