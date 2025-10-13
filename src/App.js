import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import ResearchPage from "./pages/Research";
import PolicyAnalysis from "./pages/PolicyAnalysis";

function App() {
  return (
    <Router basename={process.env.PUBLIC_URL}>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/policy-analysis" element={<PolicyAnalysis />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
