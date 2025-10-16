import React, { useState } from "react";
import {
  getAllReferences,
  getReferencesByType,
  formatAPACitation,
  formatBibTeX,
} from "../data/references";
import "./References.css";

function References() {
  const [filterType, setFilterType] = useState("all");
  const [showBibTeX, setShowBibTeX] = useState({});

  const references =
    filterType === "all" ? getAllReferences() : getReferencesByType(filterType);

  const referenceTypes = [
    { value: "all", label: "All References" },
    { value: "article", label: "Journal Articles" },
    { value: "book", label: "Books" },
    { value: "inproceedings", label: "Conference Papers" },
    { value: "techreport", label: "Technical Reports" },
    { value: "misc", label: "Other" },
  ];

  const toggleBibTeX = (id) => {
    setShowBibTeX((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const copyBibTeX = (reference) => {
    const bibtex = formatBibTeX(reference);
    navigator.clipboard.writeText(bibtex);
    // Could add a toast notification here
  };

  return (
    <div className="references-page">
      <div className="references-hero">
        <div className="container">
          <h1>References</h1>
          <p className="references-subtitle">
            Academic literature on AI economics, labor impacts, distributional
            effects, and microsimulation modeling
          </p>
        </div>
      </div>

      <div className="container references-content">
        <div className="references-controls">
          <label htmlFor="type-filter">Filter by type: </label>
          <select
            id="type-filter"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="type-filter"
          >
            {referenceTypes.map((type) => (
              <option key={type.value} value={type.value}>
                {type.label}
              </option>
            ))}
          </select>
          <span className="reference-count">
            {references.length} reference{references.length !== 1 ? "s" : ""}
          </span>
        </div>

        <div className="references-list">
          {references.length === 0 ? (
            <div className="no-references">
              <p>No references found for this category.</p>
            </div>
          ) : (
            references.map((ref) => (
              <div key={ref.id} className="reference-item">
                <div className="reference-header">
                  <span className="reference-type">{ref.type}</span>
                  <span className="reference-year">{ref.year}</span>
                </div>

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

                {ref.abstract && (
                  <details className="reference-abstract">
                    <summary>Abstract</summary>
                    <p>{ref.abstract}</p>
                  </details>
                )}

                <div className="reference-actions">
                  <button
                    onClick={() => toggleBibTeX(ref.id)}
                    className="action-button"
                  >
                    {showBibTeX[ref.id] ? "Hide" : "Show"} BibTeX
                  </button>
                  <button
                    onClick={() => copyBibTeX(ref)}
                    className="action-button"
                  >
                    Copy BibTeX
                  </button>
                </div>

                {showBibTeX[ref.id] && (
                  <pre className="bibtex-block">{formatBibTeX(ref)}</pre>
                )}
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
