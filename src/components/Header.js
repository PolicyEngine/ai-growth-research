import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Header.css";

function Header() {
  const location = useLocation();

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
          <Link to="/" className="header-title-link">
            <span className="header-title">AI Growth Research</span>
          </Link>
        </div>

        <nav className="header-nav">
          <Link
            to="/"
            className={`nav-link ${location.pathname === "/" ? "active" : ""}`}
          >
            Home
          </Link>
          <Link
            to="/research"
            className={`nav-link ${location.pathname === "/research" ? "active" : ""}`}
          >
            Research
          </Link>
          <Link
            to="/policy-analysis"
            className={`nav-link ${location.pathname === "/policy-analysis" ? "active" : ""}`}
          >
            Policy Analysis
          </Link>
          <Link
            to="/references"
            className={`nav-link ${location.pathname === "/references" ? "active" : ""}`}
          >
            References
          </Link>
        </nav>

        <div className="header-right">
          <a
            href="https://github.com/PolicyEngine"
            className="header-link github-link"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="PolicyEngine GitHub"
          >
            <img
              src={`${process.env.PUBLIC_URL}/github-logo.svg`}
              alt="GitHub"
              className="github-logo"
            />
          </a>
        </div>
      </div>
    </header>
  );
}

export default Header;
