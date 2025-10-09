import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>AI and Distributional Policy Research</h1>
        <p className="hero-subtitle">
          How do economic policies mediate AI's impact
          <br />
          on income, consumption, and wealth distribution?
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
          <div className="cta-event">
            <span className="event-icon">📅</span>
            <span className="event-text">
              Meet Max Ghenis or Daphne Hansell at EAG NYC this weekend
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Hero;
