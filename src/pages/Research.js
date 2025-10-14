import React from "react";
import Research from "../components/Research";
import StochasticForecasting from "../components/StochasticForecasting";
import UpratingViewer from "../components/UpratingViewer";
import TechnicalRequirements from "../components/TechnicalRequirements";

function ResearchPage() {
  return (
    <>
      <div className="section section-alt" style={{ paddingTop: "6rem" }}>
        <h1
          style={{
            textAlign: "center",
            marginBottom: "1rem",
            fontSize: "3rem",
          }}
        >
          Research Context
        </h1>
        <p
          style={{
            textAlign: "center",
            fontSize: "1.2rem",
            maxWidth: "800px",
            margin: "0 auto 3rem",
          }}
        >
          Academic research on AI economics, labor markets, and probabilistic
          forecasting for microsimulation
        </p>
      </div>
      <Research />
      <StochasticForecasting />
      <UpratingViewer />
      <TechnicalRequirements />
      <div
        className="section"
        style={{ textAlign: "center", padding: "3rem 2rem" }}
      >
        <a
          href="/"
          style={{
            color: "#319795",
            fontSize: "1.1rem",
            textDecoration: "none",
          }}
        >
          ← Back to Home
        </a>
      </div>
    </>
  );
}

export default ResearchPage;
