import React from "react";
import Hero from "../components/Hero";
import Challenge from "../components/Challenge";
import Approach from "../components/Approach";
import Evidence from "../components/Evidence";
import Ecosystem from "../components/Ecosystem";
import GetInvolved from "../components/GetInvolved";

function Home() {
  return (
    <main>
      <Hero />
      <Challenge />
      <Approach />
      <Evidence />
      <Ecosystem />
      <div id="get-involved">
        <GetInvolved />
      </div>
    </main>
  );
}

export default Home;
