import React from "react";
import { describe, expect, it } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import AIScenarios, { realizationBreakeven } from "./AIScenarios";

describe("AIScenarios", () => {
  it("renders the section with scenario and variant controls", () => {
    render(<AIScenarios />);
    expect(
      screen.getByText("What forecasters expect, under current law"),
    ).toBeTruthy();
    expect(screen.getByRole("radio", { name: "Rapid" })).toBeTruthy();
    expect(screen.getByRole("radio", { name: "Proportional" })).toBeTruthy();
  });

  it("defaults to Rapid / proportional and shows its revenue", () => {
    render(<AIScenarios />);
    // Rapid / proportional revenue change is +$206B in the committed payload.
    expect(screen.getAllByText("+$206B").length).toBeGreaterThan(0);
  });

  it("switches scenario when a tab is clicked", () => {
    render(<AIScenarios />);
    fireEvent.click(screen.getByRole("radio", { name: "Slow" }));
    // Slow / proportional revenue change is +$6B.
    expect(screen.getAllByText("+$6B").length).toBeGreaterThan(0);
  });

  it("shows the crossover wage only for spread variants", () => {
    render(<AIScenarios />);
    expect(screen.queryByText(/workers earning below/i)).toBeNull();
    fireEvent.click(screen.getByRole("radio", { name: "Wages spread" }));
    expect(screen.getByText(/workers earning below/i)).toBeTruthy();
  });

  it("carries the corporate-tax scope note from the payload", () => {
    render(<AIScenarios />);
    expect(screen.getByText(/no corporate income tax/i)).toBeTruthy();
  });

  it("cites the model and data build", () => {
    render(<AIScenarios />);
    expect(screen.getByText(/populace_us_2024/)).toBeTruthy();
  });
});

describe("realizationBreakeven", () => {
  it("interpolates the zero crossing", () => {
    const rows = [
      { realizationRate: 0, revenueChange: -60 },
      { realizationRate: 0.25, revenueChange: 5 },
      { realizationRate: 1, revenueChange: 205 },
    ];
    // Crosses zero between 0 and 0.25: 60 / 65 of the way.
    expect(realizationBreakeven(rows)).toBeCloseTo(0.25 * (60 / 65), 5);
  });

  it("returns null when revenue never crosses zero", () => {
    expect(
      realizationBreakeven([
        { realizationRate: 0, revenueChange: 10 },
        { realizationRate: 1, revenueChange: 200 },
      ]),
    ).toBeNull();
  });

  it("handles the committed payload without error", async () => {
    const { default: data } = await import("../data/aiScenariosData.json");
    const breakeven = realizationBreakeven(data.sensitivities.realization);
    expect(breakeven).toBeGreaterThan(0.2);
    expect(breakeven).toBeLessThan(0.26);
  });
});
