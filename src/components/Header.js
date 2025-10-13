import React, { useState, useEffect, useMemo } from "react";
import "./Header.css";

function Header() {
  const [activeSection, setActiveSection] = useState("");

  const sections = useMemo(
    () => [
      { id: "examples", label: "What PE Does" },
      { id: "overview", label: "Overview" },
      { id: "research", label: "Research" },
      { id: "stochastic-forecasting", label: "Stochastic Forecasting" },
      { id: "scenarios", label: "Scenarios" },
      { id: "stakeholders", label: "Stakeholders" },
    ],
    [],
  );

  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY + 100;

      for (const section of sections) {
        const element = document.getElementById(section.id);
        if (element) {
          const { offsetTop, offsetHeight } = element;
          if (
            scrollPosition >= offsetTop &&
            scrollPosition < offsetTop + offsetHeight
          ) {
            setActiveSection(section.id);
            break;
          }
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll();

    return () => window.removeEventListener("scroll", handleScroll);
  }, [sections]);

  const scrollToSection = (id) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <header className="header-bar">
      <div className="header-content">
        <div className="header-left">
          <a href="https://policyengine.org" className="logo-link">
            <img
              src={`${process.env.PUBLIC_URL}/policyengine-logo.svg`}
              alt="PolicyEngine"
              className="header-logo"
            />
          </a>
          <span className="header-divider">|</span>
          <span className="header-title">AI Growth Research</span>
        </div>

        <nav className="header-nav">
          {sections.map((section) => (
            <button
              key={section.id}
              className={`nav-link ${activeSection === section.id ? "active" : ""}`}
              onClick={() => scrollToSection(section.id)}
            >
              {section.label}
            </button>
          ))}
        </nav>

        <div className="header-right">
          <a
            href="https://policyengine.org/us"
            className="header-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            PE-US
          </a>
          <a
            href="https://github.com/PolicyEngine"
            className="header-link"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </div>
      </div>
    </header>
  );
}

export default Header;
