import React from "react";
import {
  getAllReferences,
  formatAPACitation,
  formatBibTeX,
} from "../data/references";
import "./References.css";

function References() {
  const references = getAllReferences();

  return (
    <div className="references-page">
      <div className="section section-alt" style={{ paddingTop: "6rem" }}>
        <h1
          style={{
            textAlign: "center",
            marginBottom: "1rem",
            fontSize: "3rem",
          }}
        >
          References
        </h1>
        <p
          style={{
            textAlign: "center",
            fontSize: "1.2rem",
            maxWidth: "800px",
            margin: "0 auto 3rem",
          }}
        >
          Academic literature on AI economics, labor impacts, distributional
          effects, and microsimulation modeling
        </p>
      </div>

      <div className="container references-content">
        <div className="references-list">
          {references.length === 0 ? (
            <div className="no-references">
              <p>No references found for this category.</p>
            </div>
          ) : (
            references.map((ref) => (
              <div key={ref.id} className="reference-item">
                <a
                  href={ref.doi ? `https://doi.org/${ref.doi}` : ref.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="reference-citation-link"
                >
                  <div
                    className="reference-citation"
                    dangerouslySetInnerHTML={{
                      __html: formatAPACitation(ref),
                    }}
                  />
                </a>
              </div>
            ))
          )}
        </div>

        <div className="references-footer">
          <h3>Download All References</h3>
          <p>
            Click below to download all references in BibTeX format for use with
            citation managers like Zotero, Mendeley, or BibDesk.
          </p>
          <button
            onClick={() => {
              const allBibtex = getAllReferences()
                .map((ref) => formatBibTeX(ref))
                .join("\n\n");
              const blob = new Blob([allBibtex], { type: "text/plain" });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "ai-growth-references.bib";
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="download-button"
          >
            Download BibTeX File
          </button>
        </div>
      </div>
    </div>
  );
}

export default References;
