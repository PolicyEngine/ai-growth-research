import React from "react";
import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import BudgetLabMemo from "./BudgetLabMemo";

describe("BudgetLabMemo", () => {
  it("renders the memo title and byline from generated content", () => {
    render(
      <MemoryRouter>
        <BudgetLabMemo />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole("heading", {
        name: /AI, the tax system, and the bottom of the distribution/i,
      }),
    ).toBeTruthy();
    expect(screen.getByText(/Max Ghenis/)).toBeTruthy();
  });

  it("renders the scenario results table", () => {
    render(
      <MemoryRouter>
        <BudgetLabMemo />
      </MemoryRouter>,
    );
    expect(screen.getAllByRole("table").length).toBeGreaterThan(3);
    expect(screen.getByText("Rapid / expansive")).toBeTruthy();
  });

  it("links to the interactive version", () => {
    render(
      <MemoryRouter>
        <BudgetLabMemo />
      </MemoryRouter>,
    );
    expect(
      screen.getByRole("link", { name: /interactive version/i }),
    ).toBeTruthy();
  });
});
