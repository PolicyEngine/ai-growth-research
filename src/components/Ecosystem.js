import React from "react";
import "./Ecosystem.css";

function Ecosystem() {
  const categories = [
    {
      title: "Research & academia",
      tagClass: "research",
      orgs: [
        {
          name: "EconTAI Initiative (UVA)",
          desc: "Led by Anton Korinek. Economics of Transformative AI curriculum and research.",
          url: "https://www.econtai.org/",
        },
        {
          name: "Stanford Digital Economy Lab",
          desc: 'Led by Erik Brynjolfsson. "Canaries in the Coal Mine" study, ETAI course.',
          url: "https://digitaleconomy.stanford.edu/",
        },
        {
          name: "MIT Future Tech Lab",
          desc: "Job displacement modeling by skill category. Iceberg Index.",
          url: "https://futuretech.mit.edu/",
        },
        {
          name: "Seth Benzell (Chapman)",
          desc: "17-region OLG CGE model of AI\u2019s global economic impact.",
          url: "https://digitalcommons.chapman.edu/economics_articles/288/",
        },
      ],
    },
    {
      title: "Policy & advocacy",
      tagClass: "policy",
      orgs: [
        {
          name: "Windfall Trust",
          desc: "Policy accelerator for the age of AI. Building global dividend fund mechanisms. FLI-funded.",
          url: "https://windfallclause.org/",
        },
        {
          name: "AGI Social Contract",
          desc: "Expert anthology on AI economic governance. Part of Windfall Trust.",
          url: "https://windfallclause.org/agi-social-contract",
        },
        {
          name: "Convergence Analysis",
          desc: "\u201CThreshold 2030\u201D conference modeling AI economic futures through 2030.",
          url: "https://www.convergenceanalysis.org/",
        },
        {
          name: "Brookings",
          desc: "AI tax policy frameworks, labor displacement analysis.",
          url: "https://www.brookings.edu/articles/future-tax-policy-a-public-finance-framework-for-the-age-of-ai/",
        },
      ],
    },
    {
      title: "Models & tools",
      tagClass: "models",
      orgs: [
        {
          name: "PolicyEngine",
          desc: "Open-source microsimulation for US, UK, Canada. This project.",
          url: "https://policyengine.org",
        },
        {
          name: "OG-USA (DeBacker & Evans)",
          desc: "Open-source overlapping generations model for fiscal policy.",
          url: "https://github.com/PSLmodels/OG-USA",
        },
        {
          name: "Don\u2019t Lose Your Job (Clay Wren)",
          desc: "Task-dependent AI displacement forecasting model.",
          url: "https://dontloseyour.job",
        },
      ],
    },
    {
      title: "Funders & forecasting",
      tagClass: "funders",
      orgs: [
        {
          name: "Open Philanthropy",
          desc: "Major funder of AI safety and economic research.",
          url: "https://www.openphilanthropy.org/",
        },
        {
          name: "Future of Life Institute",
          desc: "Funds Windfall Trust and AI governance work.",
          url: "https://futureoflife.org/",
        },
        {
          name: "Metaculus",
          desc: "Forecasting platform with AGI timeline and labor market questions.",
          url: "https://www.metaculus.com/",
        },
        {
          name: "EA Funds",
          desc: "Grantmaking across cause areas including AI governance.",
          url: "https://funds.effectivealtruism.org/",
        },
      ],
    },
  ];

  return (
    <div id="ecosystem" className="ecosystem-section">
      <div className="section-header">
        <span className="eyebrow">Who's working on this</span>
        <h2>The ecosystem</h2>
      </div>

      {categories.map((category, catIdx) => (
        <div key={catIdx} className="ecosystem-category">
          <h3 className="ecosystem-category-title">{category.title}</h3>
          <div className="ecosystem-org-grid">
            {category.orgs.map((org, orgIdx) => (
              <a
                key={orgIdx}
                href={org.url}
                target="_blank"
                rel="noopener noreferrer"
                className="ecosystem-org-card"
              >
                <div className="ecosystem-org-name">
                  {org.name} <span className="ecosystem-org-arrow">{"\u2192"}</span>
                </div>
                <p className="ecosystem-org-desc">{org.desc}</p>
                <span
                  className={`ecosystem-org-tag ${category.tagClass}`}
                >
                  {category.title}
                </span>
              </a>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Ecosystem;
