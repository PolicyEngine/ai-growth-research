import React from "react";
import "./ExampleProjects.css";

function ExampleProjects() {
  const projects = [
    {
      title: "OBBBA Household-by-Household Analysis",
      description:
        "Interactive tool showing how the One Big Beautiful Bill Act affects over 20,000 representative household types.",
      image: `${process.env.PUBLIC_URL}/images/obbba-household-by-household.png`,
      url: "https://policyengine.org/us/research/obbba-household-by-household",
      type: "Distributional Impact",
    },
    {
      title: "AI-Written Policy Reports",
      description:
        "Automatically generated policy analysis reports using AI to synthesize microsimulation results.",
      image: `${process.env.PUBLIC_URL}/images/ai-analysis.png`,
      url: "https://policyengine.org/us/research/gpt-analysis",
      type: "AI Integration",
    },
    {
      title: "Household Benefit Eligibility API",
      description:
        "Programmatic access to calculate tax liabilities and benefit eligibility for any household configuration.",
      image: `${process.env.PUBLIC_URL}/images/how-developers-can-explore-the-policyengine-api.jpg`,
      url: "https://policyengine.org/us/research/how-developers-can-explore-the-policyengine-api",
      type: "Developer API",
    },
    {
      title: "Enhanced CPS Microdata",
      description:
        "Comprehensive survey enhancement enabling household-level tax-benefit microsimulation.",
      image: `${process.env.PUBLIC_URL}/images/enhanced-cps-launch.png`,
      url: "https://policyengine.org/us/research/enhanced-cps-launch",
      type: "Data Infrastructure",
    },
    {
      title: "ACA Premium Tax Credit Calculator",
      description:
        "Calculate health insurance subsidies under current and alternative policies.",
      image: `${process.env.PUBLIC_URL}/images/aca-calc-chart.png`,
      url: "https://policyengine.org/us/research/introducing-aca-calc",
      type: "Policy Calculator",
    },
    {
      title: "NBER TAXSIM Integration",
      description:
        "Partnership with National Bureau of Economic Research to expand tax microsimulation capabilities.",
      image: `${process.env.PUBLIC_URL}/images/policyengine-nber-mou-taxsim.png`,
      url: "https://policyengine.org/us/research/policyengine-nber-mou-taxsim",
      type: "Research Partnership",
    },
  ];

  return (
    <div id="examples" className="examples-section">
      <div className="examples-container">
        <div className="section-header">
          <h2>What PolicyEngine Does</h2>
          <p className="section-subtitle">
            Open-source tax-benefit microsimulation enabling distributional
            analysis of policy interventions
          </p>
        </div>

        <div className="projects-grid">
          {projects.map((project, idx) => (
            <a
              key={idx}
              href={project.url}
              target="_blank"
              rel="noopener noreferrer"
              className="project-card"
            >
              <div className="project-image-container">
                <img
                  src={project.image}
                  alt={project.title}
                  className="project-image"
                />
                <div className="project-type">{project.type}</div>
              </div>
              <div className="project-content">
                <h3>{project.title}</h3>
                <p>{project.description}</p>
                <span className="project-link-arrow">View project →</span>
              </div>
            </a>
          ))}
        </div>

        <div className="examples-footer">
          <p>
            These projects demonstrate PolicyEngine's capability to analyze how
            policies shape distributional outcomes. The AI research initiative
            extends this approach to model how policy interventions mediate
            AI-driven economic shocks.
          </p>
        </div>
      </div>
    </div>
  );
}

export default ExampleProjects;
