import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>How do economic policies mediate AI's impact on inequality?</h1>
        <p className="hero-subtitle">
          A PolicyEngine research initiative providing a framework for analyzing
          how different policy responses shape distributional outcomes under
          AI-driven economic change—without forecasting AI's impacts or
          prescribing optimal policies.
        </p>
        <div className="hero-cta">
          <a
            href="mailto:hello@policyengine.org?subject=AI and Inequality Research"
            className="cta-button primary"
          >
            Connect with us
          </a>
        </div>
      </div>
    </div>
  );
}

export default Hero;
