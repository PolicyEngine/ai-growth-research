import React from "react";
import Hero from "../components/Hero";
import ExampleProjects from "../components/ExampleProjects";
import Overview from "../components/Overview";
import Stakeholders from "../components/Stakeholders";

function Home() {
  return (
    <>
      <Hero />
      <ExampleProjects />
      <Overview />
      <div
        className="section"
        style={{ textAlign: "center", padding: "4rem 2rem" }}
      >
        <h2>Dive deeper</h2>
        <p
          style={{
            maxWidth: "800px",
            margin: "0 auto 2rem",
            fontSize: "1.1rem",
          }}
        >
          Explore the academic research context and technical implementation, or
          examine the policy scenarios we can analyze.
        </p>
        <div
          style={{
            display: "flex",
            gap: "2rem",
            justifyContent: "center",
            flexWrap: "wrap",
          }}
        >
          <a
            href="/research"
            className="cta-button primary"
            style={{ textDecoration: "none", minWidth: "200px" }}
          >
            Research Context →
          </a>
          <a
            href="/policy-analysis"
            className="cta-button primary"
            style={{ textDecoration: "none", minWidth: "200px" }}
          >
            Policy Analysis →
          </a>
        </div>
      </div>
      <Stakeholders />
    </>
  );
}

export default Home;
