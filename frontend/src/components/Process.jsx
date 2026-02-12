export default function Process() {
  const rounds = [
    "Technical Voice Round",
    "Coding Simulation",
    "Communication Assessment",
    "AI HR Video Interview"
  ];

  return (
    <section className="process">
      <div className="process-left">
        <h2>Our Interview Process</h2>
        <p>Step-by-step structured evaluation just like real companies.</p>
      </div>

      <div className="process-cards">
        {rounds.map((round, index) => (
          <div key={index} className="process-card">
            <h3>{round}</h3>
          </div>
        ))}
      </div>
    </section>
  );
}
