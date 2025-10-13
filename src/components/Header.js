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
          <span className="header-title">AI Growth Research</span>
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
