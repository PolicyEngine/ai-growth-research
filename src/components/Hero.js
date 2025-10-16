import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>How do economic policies mediate AI's impact on inequality?</h1>
        <p className="hero-subtitle">
          PolicyEngine models how alternative policies—UBI, expanded safety nets,
          capital taxation—shape distributional outcomes under AI-driven
          economic change.
        </p>
        <p className="hero-description">
          Our open-source microsimulation platform enables rigorous, transparent
          analysis for policymakers, researchers, and the public.
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
