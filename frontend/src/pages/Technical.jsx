import { useState, useEffect, useRef } from "react";

const Technical = () => {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const recognitionRef = useRef(null);

  // Fetch question
  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_technical_question")
      .then(res => res.json())
      .then(data => setQuestion(data.question))
      .catch(err => console.error(err));
  }, []);

  // Setup Speech Recognition
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      console.log("🎤 Listening...");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("User said:", transcript);
      setAnswer(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Speech error:", event.error);
    };

    recognitionRef.current = recognition;
  }, []);

  const speakQuestion = () => {
    if (!question) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(question);
    utterance.rate = 1;
    window.speechSynthesis.speak(utterance);
  };

  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  };

  return (
    <div style={{ padding: "100px" }}>
      <h2>Technical Round</h2>

      {question ? (
        <>
          <p>{question}</p>

          <button onClick={speakQuestion}>
            🔊 Hear Question
          </button>

          <br /><br />

          <button onClick={startListening}>
            🎤 Answer by Voice
          </button>

          {answer && (
            <div style={{ marginTop: "20px" }}>
              <strong>Your Answer:</strong>
              <p>{answer}</p>
            </div>
          )}
        </>
      ) : (
        <p>Loading question...</p>
      )}
    </div>
  );
};

export default Technical;
