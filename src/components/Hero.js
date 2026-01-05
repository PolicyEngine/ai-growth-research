import React from "react";
import "./Hero.css";

function Hero() {
  return (
    <div className="hero">
      {/* Animated Floating Orbs */}
      <div className="hero-orb hero-orb-1" />
      <div className="hero-orb hero-orb-2" />
      <div className="hero-orb hero-orb-3" />

      <div className="hero-content">
        <h1>
          How do economic policies mediate{" "}
          <span className="highlight">AI's impact on inequality?</span>
        </h1>
        <p className="hero-subtitle">
          A PolicyEngine research initiative examining how policy interventions
          shape distributional outcomes when AI drives economic transformation.
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

      {/* Scroll Indicator */}
      <div className="hero-scroll">
        <span>Explore</span>
        <div className="hero-scroll-line" />
      </div>
    </div>
  );
}

export default Hero;
