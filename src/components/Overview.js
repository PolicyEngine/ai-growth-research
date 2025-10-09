import React from "react";
import "./Overview.css";

function Overview() {
  const challenges = [
    {
      icon: "📈",
      title: "Rising Incomes",
      desc: "Productivity gains, unevenly distributed",
    },
    {
      icon: "🏭",
      title: "Capital Share Growth",
      desc: "AI replacing or augmenting labor",
    },
    {
      icon: "⚠️",
      title: "Labor Disruption",
      desc: "Potential technological unemployment",
    },
    {
      icon: "📊",
      title: "Growing Inequality",
      desc: "Gap between beneficiaries and displaced",
    },
  ];

  const approach = [
    {
      step: 1,
      title: "AI Economic Shocks",
      desc: "Income changes, unemployment, capital share shifts",
    },
    {
      step: 2,
      title: "Policy Mediation",
      desc: "Taxes, transfers, UBI proposals, safety nets",
    },
    {
      step: 3,
      title: "Distributional Outcomes",
      desc: "Income, consumption, wealth inequality effects",
    },
    {
      step: 4,
      title: "Cross-Policy Comparison",
      desc: "How different interventions shape outcomes",
    },
  ];

  return (
    <div id="overview" className="overview-section">
      <div className="section-header">
        <h2>Research Overview</h2>
        <p className="section-subtitle">
          Examining the causal chain: AI economic shocks → policy interventions
          → distributional outcomes
        </p>
      </div>

      {/* Challenge Section - Icon Grid */}
      <div className="challenge-container">
        <h3 className="subsection-title">Potential AI Economic Shocks</h3>
        <p className="intro-text">
          AI could drive major changes in income distribution through various
          mechanisms:
        </p>
        <div className="icon-grid">
          {challenges.map((item, idx) => (
            <div key={idx} className="icon-card">
              <div className="icon-large">{item.icon}</div>
              <h4>{item.title}</h4>
              <p>{item.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Approach Section - Process Flow */}
      <div className="approach-container">
        <h3 className="subsection-title">Research Framework</h3>
        <p className="intro-text">
          We examine how economic policies mediate the relationship between AI
          shocks and distributional outcomes. Researchers provide AI economic
          scenarios as inputs, we microsimulate policy responses, and analyze
          resulting distributions of income, consumption, and wealth.
        </p>
        <div className="process-flow">
          {approach.map((item, idx) => (
            <div key={idx} className="process-step">
              <div className="step-number">{item.step}</div>
              <div className="step-content">
                <h4>{item.title}</h4>
                <p>{item.desc}</p>
              </div>
              {idx < approach.length - 1 && <div className="flow-arrow">→</div>}
            </div>
          ))}
        </div>
        <p className="integration-note">
          <strong>Integration possibility:</strong> Combine PolicyEngine
          microsimulation with general equilibrium models like{" "}
          <a
            href="https://pslmodels.github.io/OG-USA/"
            target="_blank"
            rel="noopener noreferrer"
          >
            OG-USA
          </a>{" "}
          for comprehensive economic-fiscal analysis.
        </p>
      </div>

      {/* Uncertainty Section - Highlight Box */}
      <div className="uncertainty-box">
        <div className="box-content">
          <h3>Quantifying Uncertainty</h3>
          <p>
            Traditional policy analysis reports only point estimates (e.g., CBO
            baseline forecasts). AI-driven economic change involves profound
            uncertainty. We'll model ranges of scenarios to show how policy
            impacts vary across different AI trajectories.
          </p>
          <div className="stats-row">
            <div className="stat-item">
              <div className="stat-value">Multiple</div>
              <div className="stat-label">AI Scenarios</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">Probabilistic</div>
              <div className="stat-label">Forecasts</div>
            </div>
            <div className="stat-item">
              <div className="stat-value">Robust</div>
              <div className="stat-label">Policy Analysis</div>
            </div>
          </div>
        </div>
      </div>

      {/* Why This Matters - Impact Grid */}
      <div className="impact-section">
        <h3 className="subsection-title">Why This Matters</h3>
        <div className="impact-grid">
          <div className="impact-card">
            <span className="impact-icon">🔬</span>
            <h4>Understand Mediation</h4>
            <p>
              How do policies shape AI's distributional impacts on income,
              consumption, wealth?
            </p>
          </div>
          <div className="impact-card">
            <span className="impact-icon">📊</span>
            <h4>Compare Interventions</h4>
            <p>
              Contrast how current policies vs. alternatives mediate AI shocks
            </p>
          </div>
          <div className="impact-card">
            <span className="impact-icon">🎲</span>
            <h4>Quantify Uncertainty</h4>
            <p>
              Model ranges of AI scenarios and policy responses, not just point
              estimates
            </p>
          </div>
          <div className="impact-card">
            <span className="impact-icon">🌐</span>
            <h4>Open Collaboration</h4>
            <p>
              Transparent microsimulation enables researchers to test their own
              assumptions
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;
