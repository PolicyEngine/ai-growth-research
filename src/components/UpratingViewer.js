import React, { useState, useEffect, useMemo } from "react";
import Papa from "papaparse";

function UpratingViewer() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [expandedCategory, setExpandedCategory] = useState(null);

  useEffect(() => {
    fetch(`${process.env.PUBLIC_URL}/data/uprating_analysis.csv`)
      .then((response) => response.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            setData(results.data);
            setLoading(false);
          },
          error: (err) => {
            setError(err.message);
            setLoading(false);
          },
        });
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const groupedData = useMemo(() => {
    if (!data.length) return {};

    const grouped = {};
    data.forEach((row) => {
      const category = row.uprating_category || "Unknown";
      if (!grouped[category]) {
        grouped[category] = [];
      }
      grouped[category].push(row);
    });

    return grouped;
  }, [data]);

  const categories = useMemo(() => {
    return Object.keys(groupedData).sort((a, b) => {
      return groupedData[b].length - groupedData[a].length;
    });
  }, [groupedData]);

  const filteredData = useMemo(() => {
    let filtered = groupedData;

    if (selectedCategory !== "all") {
      filtered = { [selectedCategory]: groupedData[selectedCategory] };
    }

    if (searchTerm) {
      const result = {};
      Object.keys(filtered).forEach((category) => {
        const matchingRows = filtered[category].filter((row) => {
          const searchLower = searchTerm.toLowerCase();
          return (
            row.path?.toLowerCase().includes(searchLower) ||
            row.description?.toLowerCase().includes(searchLower) ||
            row.uprating?.toLowerCase().includes(searchLower)
          );
        });
        if (matchingRows.length > 0) {
          result[category] = matchingRows;
        }
      });
      return result;
    }

    return filtered;
  }, [groupedData, selectedCategory, searchTerm]);

  const totalParams = useMemo(() => {
    return Object.values(filteredData).reduce(
      (sum, params) => sum + params.length,
      0,
    );
  }, [filteredData]);

  if (loading) {
    return (
      <div className="section" style={{ textAlign: "center", padding: "3rem" }}>
        <p>Loading uprating parameters...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="section" style={{ textAlign: "center", padding: "3rem" }}>
        <p style={{ color: "#e53e3e" }}>Error loading data: {error}</p>
      </div>
    );
  }

  return (
    <div id="uprating-viewer" className="section section-alt">
      <h2>PolicyEngine-US Uprating Parameters</h2>
      <p
        style={{
          textAlign: "center",
          maxWidth: "800px",
          margin: "0 auto 2rem",
          fontSize: "1.1rem",
        }}
      >
        Explore the 318 parameters in PolicyEngine-US that grow over time based
        on different economic indicators. These growth factors create correlated
        uncertainty in long-term policy projections.
      </p>

      {/* Search and Filter Controls */}
      <div
        style={{
          maxWidth: "800px",
          margin: "0 auto 2rem",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <input
          type="text"
          placeholder="Search by parameter name, path, or description..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: "0.75rem 1rem",
            fontSize: "1rem",
            border: "2px solid #e2e8f0",
            borderRadius: "8px",
            width: "100%",
          }}
        />

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <label htmlFor="category-filter" style={{ fontWeight: "500" }}>
            Filter by category:
          </label>
          <select
            id="category-filter"
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{
              padding: "0.5rem 1rem",
              fontSize: "1rem",
              border: "2px solid #e2e8f0",
              borderRadius: "8px",
              flex: 1,
            }}
          >
            <option value="all">
              All Categories ({data.length} parameters)
            </option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category} ({groupedData[category].length})
              </option>
            ))}
          </select>
        </div>

        <p
          style={{ textAlign: "center", color: "#718096", fontSize: "0.95rem" }}
        >
          Showing {totalParams} parameters
          {searchTerm && ` matching "${searchTerm}"`}
        </p>
      </div>

      {/* Grouped Parameter Display */}
      <div className="grid">
        {Object.keys(filteredData).map((category) => {
          const params = filteredData[category];
          const isExpanded = expandedCategory === category;

          return (
            <div
              key={category}
              className={`card ${isExpanded ? "expanded" : ""}`}
              onClick={() => setExpandedCategory(isExpanded ? null : category)}
              style={{ cursor: "pointer" }}
            >
              <h3
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                }}
              >
                {category}
                <span
                  style={{
                    fontSize: "0.9rem",
                    color: "#319795",
                    fontWeight: "normal",
                  }}
                >
                  {params.length} {isExpanded ? "▼" : "▶"}
                </span>
              </h3>

              {isExpanded && (
                <div
                  style={{ marginTop: "1rem" }}
                  onClick={(e) => e.stopPropagation()}
                >
                  <div
                    style={{
                      maxHeight: "400px",
                      overflowY: "auto",
                      border: "1px solid #e2e8f0",
                      borderRadius: "4px",
                      padding: "1rem",
                    }}
                  >
                    {params.slice(0, 50).map((param, idx) => (
                      <div
                        key={idx}
                        style={{
                          marginBottom: "1rem",
                          paddingBottom: "1rem",
                          borderBottom:
                            idx < params.length - 1
                              ? "1px solid #e2e8f0"
                              : "none",
                        }}
                      >
                        <div
                          style={{
                            fontFamily: "monospace",
                            fontSize: "0.85rem",
                            color: "#2d3748",
                            marginBottom: "0.25rem",
                          }}
                        >
                          <strong>{param.path}</strong>
                        </div>
                        {param.description && (
                          <div
                            style={{
                              fontSize: "0.9rem",
                              color: "#4a5568",
                              marginBottom: "0.25rem",
                            }}
                          >
                            {param.description}
                          </div>
                        )}
                        <div
                          style={{
                            fontSize: "0.85rem",
                            color: "#718096",
                            marginTop: "0.25rem",
                          }}
                        >
                          Uprating: <code>{param.uprating}</code>
                        </div>
                        <a
                          href={`https://github.com/PolicyEngine/policyengine-us/blob/master/policyengine_us/parameters/${param.file_path}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            fontSize: "0.85rem",
                            color: "#319795",
                            textDecoration: "none",
                            marginTop: "0.5rem",
                            display: "inline-block",
                          }}
                          onClick={(e) => e.stopPropagation()}
                        >
                          View source →
                        </a>
                      </div>
                    ))}
                    {params.length > 50 && (
                      <p
                        style={{
                          textAlign: "center",
                          color: "#718096",
                          fontSize: "0.9rem",
                          marginTop: "1rem",
                        }}
                      >
                        Showing first 50 of {params.length} parameters. Use
                        search to narrow results.
                      </p>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {Object.keys(filteredData).length === 0 && (
        <p
          style={{
            textAlign: "center",
            color: "#718096",
            fontSize: "1.1rem",
            marginTop: "2rem",
          }}
        >
          No parameters match your search criteria.
        </p>
      )}

      <div
        className="card"
        style={{ marginTop: "2rem", backgroundColor: "#f0f9ff" }}
      >
        <h3>About These Parameters</h3>
        <p>
          Each parameter in PolicyEngine-US that changes over time uses an
          "uprating" method to project its value forward. The uprating method
          determines which economic indicator drives the growth:
        </p>
        <ul style={{ marginTop: "1rem" }}>
          <li>
            <strong>IRS Chained CPI-U:</strong> Most federal tax parameters
            (brackets, deductions, credits) indexed to chained CPI-U
          </li>
          <li>
            <strong>CPI-U Direct:</strong> Some state parameters and benefit
            amounts indexed to standard CPI-U
          </li>
          <li>
            <strong>SSA CPI-W:</strong> Social Security parameters indexed to
            CPI-W (wage earners)
          </li>
          <li>
            <strong>Income by Source:</strong> CBO projections for different
            income types (wages, capital gains, dividends, etc.)
          </li>
          <li>
            <strong>Other:</strong> Population growth, state-specific inflation,
            wage indexes
          </li>
        </ul>
        <p style={{ marginTop: "1rem" }}>
          These growth factors are correlated but not perfectly - modeling their
          joint distribution is critical for accurate long-term projections
          under AI scenarios.
        </p>
      </div>
    </div>
  );
}

export default UpratingViewer;
