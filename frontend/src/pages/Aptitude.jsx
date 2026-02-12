import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Aptitude.css"
const questions = [
  {
    question: "If 5 workers complete a job in 10 days, how many days will 10 workers take?",
    options: ["5 days", "10 days", "20 days", "15 days"],
  },
  {
    question: "What comes next in the series: 2, 4, 8, 16, ?",
    options: ["18", "24", "32", "30"],
  },
  {
    question: "A train 100m long crosses a pole in 10 seconds. What is its speed?",
    options: ["10 m/s", "15 m/s", "20 m/s", "25 m/s"],
  },
];

export default function Aptitude() {
  const navigate = useNavigate();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState("");
  const [answers, setAnswers] = useState({});

  const handleNext = async () => {
    const updatedAnswers = {
      ...answers,
      [currentIndex]: selectedOption,
    };

    setAnswers(updatedAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(prev => prev + 1);
      setSelectedOption("");
    } else {
      // Send to backend
      const response = await fetch("http://127.0.0.1:5000/submit_aptitude", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answers: updatedAnswers }),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error("Server returned:", text);
        return;
      }

      const result = await response.json();
      console.log("Aptitude Result:", result);

      navigate("/technical");
    }
  };

  return (
    <div style={{ padding: "100px" }}>
      <h2>Aptitude Round</h2>

      <h3>{questions[currentIndex].question}</h3>

      {questions[currentIndex].options.map((option, index) => (
        <button
          key={index}
          onClick={() => setSelectedOption(option)}
          style={{
            display: "block",
            margin: "10px 0",
            padding: "10px",
            background: selectedOption === option ? "blue" : "gray",
            color: "white"
          }}
        >
          {option}
        </button>
      ))}

      <button
        onClick={handleNext}
        disabled={!selectedOption}
        style={{ marginTop: "20px", padding: "10px 20px" }}
      >
        {currentIndex === questions.length - 1 ? "Submit" : "Next"}
      </button>
    </div>
  );
}
