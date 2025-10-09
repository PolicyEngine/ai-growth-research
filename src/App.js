import React from "react";
import "./App.css";
import Header from "./components/Header";
import Hero from "./components/Hero";
import ExampleProjects from "./components/ExampleProjects";
import Overview from "./components/Overview";
import PolicyEngineCapabilities from "./components/PolicyEngineCapabilities";
import Research from "./components/Research";
import Stakeholders from "./components/Stakeholders";
import TechnicalRequirements from "./components/TechnicalRequirements";
import PolicyScenarios from "./components/PolicyScenarios";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="App">
      <Header />
      <Hero />
      <ExampleProjects />
      <Overview />
      <PolicyEngineCapabilities />
      <Research />
      <PolicyScenarios />
      <TechnicalRequirements />
      <Stakeholders />
      <Footer />
    </div>
  );
}

export default App;
