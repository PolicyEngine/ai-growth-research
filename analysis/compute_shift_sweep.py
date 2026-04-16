"""Sensitivity sweep of labor→capital shift at multiple magnitudes.

Runs the shift at 0%, 10%, 20%, ..., 100% and records:
  - Net income Gini and market Gini
  - SPM poverty rate
  - Revenue decomposition: income tax, payroll, EITC, CTC, SNAP
"""

import gc
import json
import os
from importlib.metadata import PackageNotFoundError, version

import numpy as np

from .constants import CAPITAL_INCOME_VARS, YEAR
from .fiscal import net_fiscal_impact, revenue_components
from .labor_capital_shift import _apply_shift
from .metrics import extract_results as _extract_results
from .microdata_export import (
    write_microdata_manifest,
    write_scenario_household_microdata,
)
from .policyengine_runtime import managed_us_microsimulation, policyengine_bundle

SHIFT_LEVELS = [pct / 100 for pct in range(0, 101, 10)]
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "outputs", "shift_sweep.json")
MICRODATA_OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "outputs", "shift_sweep_microdata"
)
MODEL_URL = "https://www.policyengine.org/us/model"
SHIFT_SWEEP_DESCRIPTION = (
    "Positive employment and self-employment income are reduced by the selected "
    "share, and the same weighted total is redistributed to positive capital "
    "income in proportion to existing holdings. This is a static current-law "
    "microsimulation; it is not a behavioral forecast."
)


def _package_version(package_name):
    try:
        return version(package_name)
    except PackageNotFoundError:
        return None


POLICYENGINE_PACKAGE = "policyengine"
POLICYENGINE_VERSION = (
    _package_version(POLICYENGINE_PACKAGE)
    or _package_version("policyengine-core")
    or "unknown"
)
POLICYENGINE_US_VERSION = _package_version("policyengine-us") or "unknown"


def _baseline_facts(sim):
    """Return high-level baseline totals used in the website explainer."""
    try:
        employment_income = sim.calculate("employment_income", period=YEAR)
        self_employment_income = sim.calculate(
            "self_employment_income", period=YEAR
        )
        employment_raw = np.asarray(employment_income, dtype=float)
        employment_weights = np.asarray(employment_income.weights, dtype=float)
        self_employment_raw = np.asarray(self_employment_income, dtype=float)
        self_employment_weights = np.asarray(
            self_employment_income.weights,
            dtype=float,
        )
        positive_labor_income = float(
            (np.where(employment_raw > 0, employment_raw, 0) * employment_weights).sum()
            + (
                np.where(self_employment_raw > 0, self_employment_raw, 0)
                * self_employment_weights
            ).sum()
        )

        positive_capital_income = 0.0
        for var in CAPITAL_INCOME_VARS:
            values = sim.calculate(var, period=YEAR)
            raw = np.asarray(values, dtype=float)
            weights = np.asarray(values.weights, dtype=float)
            positive_capital_income += float(
                (np.where(raw > 0, raw, 0) * weights).sum()
            )

        household_weight = np.asarray(
            sim.calculate("household_weight", period=YEAR), dtype=float
        )
        household_positive_capital = np.zeros_like(household_weight, dtype=float)
        for var in CAPITAL_INCOME_VARS:
            household_values = np.asarray(
                sim.calculate(var, period=YEAR, map_to="household"),
                dtype=float,
            )
            household_positive_capital += np.where(
                household_values > 0, household_values, 0
            )

        households_with_positive_capital_income_share = float(
            household_weight[household_positive_capital > 0].sum()
            / household_weight.sum()
        )

        return {
            "labor_income_t": positive_labor_income / 1e12,
            "positive_labor_income_t": positive_labor_income / 1e12,
            "positive_capital_income_t": positive_capital_income / 1e12,
            "households_with_positive_capital_income_share": (
                households_with_positive_capital_income_share
            ),
        }
    except Exception:
        return {}


def _metadata(baseline):
    bundle = policyengine_bundle(baseline)
    return {
        "year": YEAR,
        "description": SHIFT_SWEEP_DESCRIPTION,
        "model_url": MODEL_URL,
        "policyengine_package": POLICYENGINE_PACKAGE,
        "policyengine_version": (
            bundle.get("policyengine_version") or POLICYENGINE_VERSION
        ),
        "country_model_package": (
            bundle.get("model_package") or "policyengine-us"
        ),
        "country_model_version": (
            bundle.get("model_version") or POLICYENGINE_US_VERSION
        ),
        "policyengine_us_version": (
            bundle.get("model_version") or POLICYENGINE_US_VERSION
        ),
        "data_package": bundle.get("data_package"),
        "data_version": bundle.get("data_version"),
        "dataset_name": (
            bundle.get("runtime_dataset")
            or getattr(getattr(baseline, "dataset", None), "name", None)
        ),
        "dataset_uri": bundle.get("runtime_dataset_uri"),
        "policyengine_bundle": bundle or None,
        "baseline_facts": _baseline_facts(baseline),
    }


def run_shift_sweep(
    shift_levels=None,
    microsim_factory=managed_us_microsimulation,
    verbose=False,
    microdata_output_dir=MICRODATA_OUTPUT_DIR,
):
    """Run the labor→capital shift sweep and return website/export-ready rows.

    Each shift level is simulated from a fresh baseline microsimulation. This
    avoids retaining many live PolicyEngine branches in memory at once, which
    becomes expensive when sweeping the full 0–100% grid.
    """
    if shift_levels is None:
        shift_levels = SHIFT_LEVELS

    baseline = microsim_factory()
    if verbose:
        print("\nComputing baseline metrics...")
    base_metrics = _extract_results(baseline, "Baseline")
    base_rev = revenue_components(baseline)
    metadata = _metadata(baseline)
    microdata_files = []
    if microdata_output_dir:
        if verbose:
            print(f"Writing baseline household microdata to {microdata_output_dir}...")
        microdata_files.append(
            write_scenario_household_microdata(
                baseline,
                microdata_output_dir,
                "Baseline",
                0,
            )
        )
    del baseline

    scenarios = []

    scenarios.append({
        "shift_pct": 0,
        "label": "Baseline",
        "net_gini": base_metrics["net_gini"],
        "net_gini_including_health_benefits": (
            base_metrics["net_gini_including_health_benefits"]
        ),
        "market_gini": base_metrics["market_gini"],
        "net_top_10_share": base_metrics["top_10_share"],
        "net_top_1_share": base_metrics["top_1_share"],
        "net_top_0_1_share": base_metrics["top_0_1_share"],
        "market_top_10_share": base_metrics["market_top_10_share"],
        "market_top_1_share": base_metrics["market_top_1_share"],
        "market_top_0_1_share": base_metrics["market_top_0_1_share"],
        "spm_poverty_rate": base_metrics["spm_poverty_rate"],
        "fed_revenue_b": base_metrics["fed_revenue"] / 1e9,
        "revenue_change_b": 0.0,
        "income_tax_change_b": 0.0,
        "employee_payroll_change_b": 0.0,
        "employer_payroll_change_b": 0.0,
        "eitc_change_b": 0.0,
        "ctc_change_b": 0.0,
        "snap_change_b": 0.0,
    })

    for pct in shift_levels:
        if pct == 0.0:
            continue
        label = f"{int(pct * 100)}% shift"
        if verbose:
            print(f"\nComputing {label} metrics...")

        sim = microsim_factory()
        branch, _ = _apply_shift(sim, f"sweep_{int(pct * 100)}", pct)
        metrics = _extract_results(branch, label)
        rev = revenue_components(branch)
        delta = net_fiscal_impact(rev, base_rev)
        if microdata_output_dir:
            if verbose:
                print(f"  Writing household microdata for {label}...")
            microdata_files.append(
                write_scenario_household_microdata(
                    branch,
                    microdata_output_dir,
                    label,
                    int(pct * 100),
                )
            )

        scenarios.append({
            "shift_pct": int(pct * 100),
            "label": label,
            "net_gini": metrics["net_gini"],
            "net_gini_including_health_benefits": (
                metrics["net_gini_including_health_benefits"]
            ),
            "market_gini": metrics["market_gini"],
            "net_top_10_share": metrics["top_10_share"],
            "net_top_1_share": metrics["top_1_share"],
            "net_top_0_1_share": metrics["top_0_1_share"],
            "market_top_10_share": metrics["market_top_10_share"],
            "market_top_1_share": metrics["market_top_1_share"],
            "market_top_0_1_share": metrics["market_top_0_1_share"],
            "spm_poverty_rate": metrics["spm_poverty_rate"],
            "fed_revenue_b": metrics["fed_revenue"] / 1e9,
            "revenue_change_b": delta["total_change"] / 1e9,
            "income_tax_change_b": delta["income_tax_change"] / 1e9,
            "employee_payroll_change_b": delta["employee_payroll_change"] / 1e9,
            "employer_payroll_change_b": delta["employer_payroll_change"] / 1e9,
            "eitc_change_b": delta["eitc_change"] / 1e9,
            "ctc_change_b": delta["ctc_change"] / 1e9,
            "snap_change_b": delta["snap_change"] / 1e9,
        })

        if verbose:
            print(f"  Net Gini: {metrics['net_gini']:.4f}  Market Gini: {metrics['market_gini']:.4f}")
            print(f"  Poverty: {metrics['spm_poverty_rate']:.2%}")
            print(f"  Revenue change: ${delta['total_change']/1e9:+.1f}B")

        del branch
        del sim
        gc.collect()

    if microdata_output_dir:
        write_microdata_manifest(
            microdata_output_dir,
            metadata,
            microdata_files,
        )

    return {"year": YEAR, "metadata": metadata, "scenarios": scenarios}


def main():
    print("=" * 60)
    print("LABOR→CAPITAL SHIFT SWEEP")
    print("=" * 60)

    result = run_shift_sweep(verbose=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")

    # Print summary table
    print("\n" + "=" * 75)
    print(f"{'Shift':>7} {'Market Gini':>12} {'Net Gini':>10} {'Poverty':>9} {'Rev Chg':>10}")
    print("-" * 75)
    for s in result["scenarios"]:
        print(
            f"{s['shift_pct']:>6}%"
            f"  {s['market_gini']:.4f}"
            f"  {s['net_gini']:.4f}"
            f"  {s['spm_poverty_rate']:.2%}"
            f"  ${s['revenue_change_b']:>+.1f}B"
        )


if __name__ == "__main__":
    main()
