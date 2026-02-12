import { useEffect, useState } from "react";
import "./Final.css";

const Final = () => {
  const [result, setResult] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/final_result")
      .then(res => res.json())
      .then(data => {
        console.log("Final Result:", data);
        setResult(data);
      })
      .catch(err => console.error(err));
  }, []);

  if (!result) {
    return <div style={{ padding: "100px" }}>Loading Final Result...</div>;
  }

  return (
    <div className="final-container">
      <div className="final-card">

        <h2>Interview Result</h2>

        <div className="overall-score">
          <div className="score-circle">
            {result.overall_score}%
          </div>
          <h3>{result.decision}</h3>
        </div>

        <div className="section-scores">
          {Object.entries(result.sections).map(([section, score]) => (
            <div key={section} className="section-item">
              <div className="section-header">
                <span>{section}</span>
                <span>{score}%</span>
              </div>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${score}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
};

export default Final;
