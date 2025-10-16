import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>AI and Distributional Policy Research</h1>
        <p className="hero-subtitle">
          How do economic policies mediate AI's impact on inequality?
        </p>
        <p className="hero-description">
          A PolicyEngine research initiative examining how policy interventions
          shape distributional outcomes when AI drives economic transformation.
        </p>
        <div className="hero-cta">
          <a
            href="mailto:hello@policyengine.org?subject=AI Distributional Policy Research"
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
