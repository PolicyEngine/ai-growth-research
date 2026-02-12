import React from "react";
import { Link } from "react-router-dom";
import Hero from "../components/Hero";
import Challenge from "../components/Challenge";
import Approach from "../components/Approach";
import ExampleProjects from "../components/ExampleProjects";
import Evidence from "../components/Evidence";
import Ecosystem from "../components/Ecosystem";
import GetInvolved from "../components/GetInvolved";

function Home() {
  return (
    <main>
      <Hero />
      <Challenge />
      <Approach />
      <ExampleProjects />
      <Evidence />
      <Ecosystem />
      <div id="get-involved">
        <GetInvolved />
      </div>
      <div className="dive-deeper-section">
        <h2>Dive deeper</h2>
        <p>
          Explore the academic research context and technical implementation, or
          examine the policy scenarios we can analyze.
        </p>
        <div className="dive-deeper-links">
          <Link to="/research" className="cta-button primary">
            Research context {"\u2192"}
          </Link>
          <Link to="/policy-analysis" className="cta-button primary">
            Policy analysis {"\u2192"}
          </Link>
          <Link to="/references" className="cta-button secondary">
            References {"\u2192"}
          </Link>
        </div>
      </div>
    </main>
  );
}

export default Home;
