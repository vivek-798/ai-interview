import { useState, useEffect } from "react";

export default function Technical() {
  const [question, setQuestion] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_technical_question")
      .then(res => res.json())
      .then(data => {
        setQuestion(data.question);
      })
      .catch(err => {
        console.error("Fetch error:", err);
      });
  }, []);

  useEffect(() => {
    if (question) {
      const utterance = new SpeechSynthesisUtterance(question);
      speechSynthesis.speak(utterance);
    }
  }, [question]);

  return (
    <div style={{ padding: "100px" }}>
      <h2>Technical Round</h2>

      {question ? (
        <p>{question}</p>
      ) : (
        <p>Loading question...</p>
      )}
    </div>
  );
}
