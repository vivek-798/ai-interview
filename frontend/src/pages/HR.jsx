import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const hrQuestions = [
  "Tell me about yourself.",
  "What is your biggest strength?",
  "Why should we hire you?"
];

const HR = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const navigate = useNavigate();

  // 🎥 Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      streamRef.current = stream;
    } catch (err) {
      console.error("Camera error:", err);
    }
  };

  // 🛑 Stop camera
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
  };

  // 🔊 Speak Question
  const speakQuestion = (text) => {
    return new Promise((resolve) => {
      const utterance = new SpeechSynthesisUtterance(text);

      utterance.rate = 1;
      utterance.pitch = 1;
      utterance.volume = 1;

      utterance.onend = () => resolve();

      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    });
  };

  // 🔥 Main Question Flow
  useEffect(() => {
    if (currentIndex >= hrQuestions.length) {
      stopCamera();
      navigate("/final");
      return;
    }

    const runHRRound = async () => {
      await speakQuestion(hrQuestions[currentIndex]);
      await startCamera();

      // Wait 15 seconds per question
      setTimeout(() => {
        stopCamera();
        setCurrentIndex(prev => prev + 1);
      }, 15000);
    };

    runHRRound();

  }, [currentIndex]);

  return (
    <div style={{ padding: "80px", textAlign: "center" }}>
      <h2>HR Video Round</h2>
      <h3>{hrQuestions[currentIndex]}</h3>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        width="400"
        style={{ borderRadius: "10px", marginTop: "20px" }}
      />
    </div>
  );
};

export default HR;
