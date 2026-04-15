import React, { useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { IconArrowsExchange, IconInfoCircle } from "@tabler/icons-react";
import sweepData from "../data/shiftSweepData.json";
import { TOOLTIP_STYLE } from "../utils/chartStyles";
import { niceTicks } from "../utils/chartTicks";
import { policyEngineLabel } from "../utils/modelMetadata";
import "./AnalysisSection.css";
import "./ShiftSweep.css";

const bFmt = (value) => `$${value >= 0 ? "+" : ""}${value.toFixed(0)}B`;
const bTooltipFmt = (value) =>
  `$${value >= 0 ? "+" : ""}${value.toFixed(1)}B`;
const axisPctFmt = (value) => `${Math.round(value * 100)}%`;
const shareTooltipFmt = (value) => `${(value * 100).toFixed(1)}%`;
const shareFmt = (value) => {
  const pct = value * 100;
  if (Math.abs(pct) >= 10) {
    return `${pct.toFixed(0)}%`;
  }
  if (Math.abs(pct) >= 1) {
    return `${pct.toFixed(1)}%`;
  }
  return `${pct.toFixed(2)}%`;
};

const metadata = sweepData.metadata ?? {};
const docsUrl = metadata.model_url ?? "https://www.policyengine.org/us/model";
const modelLabel = policyEngineLabel(metadata);

const PROPORTION_TICKS = [0, 0.2, 0.4, 0.6, 0.8, 1];

const CONCEPTS = {
  market: {
    label: "Market income",
    color: "#DD6B20",
    description: "pre-tax, pre-transfer household market income",
  },
  net: {
    label: "Net income",
    color: "#319795",
    description: "household net income after taxes and transfers",
  },
};

const MEASURES = {
  gini: {
    label: "Gini coefficient",
    field: "Gini",
    axisLabel: "Gini coefficient",
    valueFormatter: (value) => value.toFixed(4),
    tooltipFormatter: (value) => value.toFixed(4),
    description:
      "Inequality on a 0-1 scale, where higher values mean income is more concentrated.",
  },
  top10: {
    label: "Top 10% share",
    field: "Top10",
    axisLabel: "Share of income",
    valueFormatter: shareFmt,
    tooltipFormatter: shareTooltipFmt,
    description: "Share of household income received by the top 10% of households.",
  },
  top1: {
    label: "Top 1% share",
    field: "Top1",
    axisLabel: "Share of income",
    valueFormatter: shareFmt,
    tooltipFormatter: shareTooltipFmt,
    description: "Share of household income received by the top 1% of households.",
  },
  top0_1: {
    label: "Top 0.1% share",
    field: "Top0_1",
    axisLabel: "Share of income",
    valueFormatter: shareFmt,
    tooltipFormatter: shareTooltipFmt,
    description: "Share of household income received by the top 0.1% of households.",
  },
  revenue: {
    label: "Net federal revenue change",
    field: "Revenue",
    dataKey: "revenue",
    color: "#2C6496",
    axisLabel: "Change vs baseline ($B)",
    valueFormatter: bFmt,
    tooltipFormatter: bTooltipFmt,
    description:
      "Federal effect including income tax, employee payroll tax, employer payroll tax, and EITC, CTC, and SNAP changes.",
  },
};

const MEASURE_OPTIONS = ["gini", "top10", "top1", "top0_1", "revenue"];
const CONCEPT_OPTIONS = ["market", "net"];

const chartData = sweepData.scenarios.map((scenario) => ({
  shift: scenario.shift_pct,
  label: scenario.label,
  marketGini: scenario.market_gini,
  netGini: scenario.net_gini,
  marketTop10: scenario.market_top_10_share,
  marketTop1: scenario.market_top_1_share,
  marketTop0_1: scenario.market_top_0_1_share,
  netTop10: scenario.net_top_10_share,
  netTop1: scenario.net_top_1_share,
  netTop0_1: scenario.net_top_0_1_share,
  revenue: scenario.revenue_change_b,
}));

const shiftTicks = niceTicks(
  chartData[0].shift,
  chartData[chartData.length - 1].shift,
  11,
);
const shift50 = sweepData.scenarios.find((scenario) => scenario.shift_pct === 50);
const shift100 = sweepData.scenarios.find(
  (scenario) => scenario.shift_pct === 100,
);

function metricConfig(measureKey, conceptKey) {
  const measure = MEASURES[measureKey];
  if (measureKey === "revenue") {
    return measure;
  }

  const concept = CONCEPTS[conceptKey];
  return {
    ...measure,
    label: `${concept.label} ${measure.label}`,
    dataKey: `${conceptKey}${measure.field}`,
    color: concept.color,
    description: `${measure.description} Uses ${concept.description}.`,
  };
}

function yTicksForConfig(config) {
  if (config.dataKey !== "revenue") {
    return PROPORTION_TICKS;
  }

  const values = chartData.map((point) => point[config.dataKey]);
  const min = Math.min(0, ...values);
  const max = Math.max(0, ...values);
  return niceTicks(min, max, 6);
}

function summaryForMetric(measureKey, conceptKey, config) {
  const basePoint = chartData[0];
  const endPoint = chartData[chartData.length - 1];
  const startValue = basePoint?.[config.dataKey];
  const endValue = endPoint?.[config.dataKey];

  if (measureKey === "gini") {
    return (
      <>
        {config.label} rises from {startValue.toFixed(3)} at baseline to{" "}
        {endValue.toFixed(3)} at a 100% shift.{" "}
        {conceptKey === "net"
          ? "Current law dampens the shock, but it does not come close to offsetting it."
          : "This is the pre-tax, pre-transfer distributional effect of routing labor income through existing capital holdings."}
      </>
    );
  }

  if (measureKey !== "revenue") {
    const direction = endValue >= startValue ? "rises" : "falls";
    return (
      <>
        {config.label} {direction} from {config.valueFormatter(startValue)} at
        baseline to {config.valueFormatter(endValue)} at a 100% shift. This
        shows how quickly the distribution concentrates when labor income is
        rerouted through existing capital holdings.
      </>
    );
  }

  return (
    <>
      Net federal revenue change reaches {bFmt(shift50?.revenue_change_b ?? 0)}
      {" "}at a 50% shift and {bFmt(shift100?.revenue_change_b ?? 0)} at a
      100% shift. Payroll-tax losses outweigh the income-tax gains all the way
      across the sweep.
    </>
  );
}

function ShiftSweep() {
  const [selectedMeasure, setSelectedMeasure] = useState("gini");
  const [selectedConcept, setSelectedConcept] = useState("net");
  const config = metricConfig(selectedMeasure, selectedConcept);
  const yTicks = yTicksForConfig(config);
  const isRevenue = selectedMeasure === "revenue";

  return (
    <div id="shift-sweep" className="analysis-section">
      <div className="analysis-header">
        <div className="analysis-icon-wrapper">
          <IconArrowsExchange size={28} stroke={1.5} />
        </div>
        <h2>Labor-to-capital shift experiment</h2>
        <p className="analysis-subtitle">
          Sweep the shock from 0% to 100% of positive labor income shifted into
          positive capital income, and switch the chart between inequality, top
          shares, and fiscal outcomes.
        </p>
      </div>

      <div className="analysis-card">
        <div className="analysis-controls">
          <div className="shift-sweep-controls">
            <div className="shift-sweep-control-group">
              <div className="shift-sweep-label">Measure</div>
              <div
                className="analysis-tabs shift-sweep-tabs"
                role="radiogroup"
                aria-label="Measure"
              >
                {MEASURE_OPTIONS.map((key) => (
                  <button
                    key={key}
                    type="button"
                    role="radio"
                    aria-checked={selectedMeasure === key}
                    className={`analysis-tab ${selectedMeasure === key ? "active" : ""}`}
                    onClick={() => setSelectedMeasure(key)}
                  >
                    {MEASURES[key].label}
                  </button>
                ))}
              </div>
            </div>
            {!isRevenue && (
              <div className="shift-sweep-control-group">
                <div className="shift-sweep-label">Income concept</div>
                <div
                  className="analysis-tabs shift-sweep-tabs"
                  role="radiogroup"
                  aria-label="Income concept"
                >
                  {CONCEPT_OPTIONS.map((key) => (
                    <button
                      key={key}
                      type="button"
                      role="radio"
                      aria-checked={selectedConcept === key}
                      className={`analysis-tab ${selectedConcept === key ? "active" : ""}`}
                      onClick={() => setSelectedConcept(key)}
                    >
                      {CONCEPTS[key].label}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
          <p className="shift-sweep-description">{config.description}</p>
        </div>

        <h3 className="analysis-chart-title">{config.label} by shift level</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart
            data={chartData}
            margin={{ left: 20, right: 30, top: 10, bottom: 35 }}
          >
            <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
            <XAxis
              type="number"
              dataKey="shift"
              domain={[shiftTicks[0], shiftTicks[shiftTicks.length - 1]]}
              ticks={shiftTicks}
              tickFormatter={(value) => `${value}%`}
              tick={{ fontSize: 12 }}
              label={{
                value: "Share of labor income shifted to capital",
                position: "bottom",
                offset: 0,
                style: { fontSize: 13 },
              }}
            />
            <YAxis
              ticks={yTicks}
              domain={isRevenue ? [yTicks[0], yTicks[yTicks.length - 1]] : [0, 1]}
              tickFormatter={isRevenue ? bFmt : axisPctFmt}
              tick={{ fontSize: 12 }}
              label={{
                value: config.axisLabel,
                angle: -90,
                position: "insideLeft",
                offset: -10,
                style: { fontSize: 13 },
              }}
            />
            {isRevenue && (
              <ReferenceLine y={0} stroke="#718096" strokeDasharray="4 4" />
            )}
            <Tooltip
              contentStyle={TOOLTIP_STYLE}
              formatter={(value) => [
                config.tooltipFormatter(value),
                config.label,
              ]}
              labelFormatter={(value) =>
                chartData.find((row) => row.shift === value)?.label ??
                `${value}% shift`
              }
            />
            <Line
              type="monotone"
              dataKey={config.dataKey}
              name={config.label}
              stroke={config.color}
              strokeWidth={3}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>

        <div className="analysis-callout">
          <IconInfoCircle size={20} stroke={1.5} />
          <div>{summaryForMetric(selectedMeasure, selectedConcept, config)}</div>
        </div>

        <p className="analysis-metadata">
          {modelLabel}, {metadata.year ?? sweepData.year} baseline.{" "}
          <a
            className="shift-sweep-link"
            href={docsUrl}
            target="_blank"
            rel="noreferrer"
          >
            Learn more about the model
          </a>
          .
        </p>
      </div>
    </div>
  );
}

export default ShiftSweep;
