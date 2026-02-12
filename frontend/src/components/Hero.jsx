import { useNavigate } from "react-router-dom";

export default function Hero() {
  const navigate = useNavigate();
  return (
    
    <section className="hero">
      <div className="hero-content">
        <h1>
          Master Your <span>AI Interview</span> Before It Matters
        </h1>
        <p>
          Experience realistic interview simulations powered by intelligent evaluation and voice interaction.
        </p>
        <div className="hero-buttons">
          <button onClick={() => navigate("/upload")} className="cta">
            Get Started
          </button>
          <button className="secondary-btn">Learn More</button>
        </div>
      </div>
    </section>
  );
}
