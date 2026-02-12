import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const Technical = () => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [listening, setListening] = useState(false);

  const recognitionRef = useRef(null);
  const navigate = useNavigate();

  /* ================================
     1️⃣ LOAD ALL QUESTIONS FROM BACKEND
  ================================== */
  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_all_technical_questions")
      .then(res => res.json())
      .then(data => {
        console.log("Questions Loaded:", data.questions);
        setQuestions(data.questions);
      })
      .catch(err => console.error("Fetch error:", err));
  }, []);

  /* ================================
     2️⃣ SETUP SPEECH RECOGNITION (ONCE)
  ================================== */
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      console.log("🎙 Mic Started");
      setListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("📝 Answer:", transcript);

      setAnswers(prev => [...prev, transcript]);

      // Wait 5 seconds before next question
      setTimeout(() => {
        setCurrentIndex(prev => prev + 1);
      }, 5000);
    };

    recognition.onerror = (event) => {
      console.error("Recognition Error:", event.error);
    };

    recognition.onend = () => {
      console.log("🎙 Mic Stopped");
      setListening(false);
    };

    recognitionRef.current = recognition;

  }, []);

  /* ================================
     3️⃣ SPEAK QUESTION WHEN INDEX CHANGES
  ================================== */
  useEffect(() => {
    if (!questions.length) return;
    if (currentIndex >= questions.length) return;

    const question = questions[currentIndex];

    console.log("Speaking Question:", question);

    const utterance = new SpeechSynthesisUtterance(question);
    utterance.rate = 1;
    utterance.pitch = 1;

    utterance.onend = () => {
      console.log("Speech finished. Starting mic...");
      recognitionRef.current?.start();
    };

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);

  }, [currentIndex, questions]);

  /* ================================
     4️⃣ NAVIGATE TO HR AFTER COMPLETION
  ================================== */
  useEffect(() => {
    if (!questions.length) return;

    if (currentIndex === questions.length) {
      console.log("Technical round completed.");
      console.log("Collected Answers:", answers);

      setTimeout(() => {
        navigate("/hr");
      }, 1000);
    }
  }, [currentIndex, questions.length, answers, navigate]);

  /* ================================
     5️⃣ UI RENDER
  ================================== */

  if (!questions.length) {
    return (
      <div style={{ padding: "100px", fontSize: "20px" }}>
        Loading Technical Questions...
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "white",
        padding: "100px"
      }}
    >
      <h2>Technical Round</h2>

      <p>
        Question {currentIndex + 1} of {questions.length}
      </p>

      {currentIndex < questions.length && (
        <h3>{questions[currentIndex]}</h3>
      )}

      {listening && (
        <div
          style={{
            marginTop: "20px",
            color: "lime",
            fontWeight: "bold",
            fontSize: "18px"
          }}
        >
          🎙 Listening... Speak Now
        </div>
      )}
    </div>
  );
};

export default Technical;
