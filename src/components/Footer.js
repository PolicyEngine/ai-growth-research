import React from "react";
import "./Footer.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>About PolicyEngine</h4>
          <p>
            PolicyEngine is a nonprofit building open-source tax-benefit
            microsimulation models to make public policy more transparent,
            accessible, and impactful.
          </p>
        </div>
        <div className="footer-section">
          <h4>Links</h4>
          <ul>
            <li>
              <a
                href="https://policyengine.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                PolicyEngine.org
              </a>
            </li>
            <li>
              <a
                href="https://github.com/PolicyEngine"
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            </li>
            <li>
              <a
                href="https://policyengine.org/us/research"
                target="_blank"
                rel="noopener noreferrer"
              >
                Research
              </a>
            </li>
            <li>
              <a
                href="https://blog.policyengine.org"
                target="_blank"
                rel="noopener noreferrer"
              >
                Blog
              </a>
            </li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>Contact</h4>
          <p>
            Interested in collaborating on this research?
            <br />
            <a href="mailto:hello@policyengine.org">hello@policyengine.org</a>
          </p>
        </div>
      </div>
      <div className="footer-bottom">
        <p>
          &copy; {new Date().getFullYear()} PolicyEngine. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

export default Footer;
