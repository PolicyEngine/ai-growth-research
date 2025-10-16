import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>Will AI Increase or Reduce Inequality?</h1>
        <p className="hero-subtitle">
          Policy choices will determine the answer.
        </p>
        <p className="hero-description">
          PolicyEngine models how alternative policy responses—universal basic
          income, expanded safety nets, capital taxation—shape inequality under
          AI-driven economic change. Our open-source microsimulation platform
          enables rigorous, transparent analysis for policymakers, researchers,
          and the public.
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
