import React from "react";
import "./PolicyEngineCapabilities.css";

function PolicyEngineCapabilities() {
  const capabilities = [
    {
      title: "Open-source microsimulation",
      icon: "🔓",
      description:
        "Transparent, auditable tax-benefit modeling enables collaborative examination of policy coordination problems.",
    },
    {
      title: "AI pioneer in policy analysis",
      icon: "🤖",
      description:
        "First policy analysis platform to integrate LLMs (April 3, 2023)—just 3 weeks after GPT-4 launched. Substantial ongoing AI integration.",
    },
    {
      title: "Real-time policy impact",
      icon: "⚡",
      description:
        "Instant calculation of distributional effects across US federal and state programs for millions of households.",
    },
    {
      title: "Collaborative research",
      icon: "🤝",
      description:
        "Open platform enables researchers worldwide to validate, extend, and build upon policy simulations.",
    },
  ];

  return (
    <div id="capabilities" className="capabilities-section">
      <div className="capabilities-container">
        <div className="capabilities-header">
          <h2>Why PolicyEngine?</h2>
          <p>
            PolicyEngine is uniquely positioned to model AI economic scenarios
            through our open-source microsimulation platform that already
            leverages AI substantially.
          </p>
        </div>

        <div className="capabilities-grid">
          {capabilities.map((cap, idx) => (
            <div key={idx} className="capability-card">
              <div className="capability-icon">{cap.icon}</div>
              <h3>{cap.title}</h3>
              <p>{cap.description}</p>
            </div>
          ))}
        </div>

        <div className="open-source-box">
          <div className="box-content">
            <h3>🌐 Open source enables transparent analysis</h3>
            <p>
              Unlike proprietary economic models, PolicyEngine's open-source
              approach enables transparent, collaborative examination of complex
              coordination problems. This is especially critical for AI
              scenarios where assumptions and methodologies must be scrutinized
              by the research community.
            </p>
            <div className="links-row">
              <a
                href="https://policyengine.org/us/ai"
                target="_blank"
                rel="noopener noreferrer"
                className="capability-link"
              >
                Explore AI features →
              </a>
              <a
                href="https://github.com/policyengine"
                target="_blank"
                rel="noopener noreferrer"
                className="capability-link"
              >
                View on GitHub →
              </a>
              <a
                href="https://blog.policyengine.org"
                target="_blank"
                rel="noopener noreferrer"
                className="capability-link"
              >
                Read our research →
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PolicyEngineCapabilities;
