"""
Regenerate all AI inequality simulation data files using updated PolicyEngine-US.

Produces:
  src/data/capitalSweepData.json   - Capital income 1x-5x sweep
  src/data/capitalDoublingData.json - Detailed capital doubling with program breakdowns
  src/data/laborShiftData.json     - Labor-to-capital shift scenarios + UBI
  src/data/shiftSweepData.json     - Shift sweep with revenue decomposition
  src/data/mtrData.json            - Marginal tax rates by income source
  src/data/cliffData.json          - Household-level cliff analysis
"""

import json
import numpy as np
from policyengine_us import Microsimulation, CountryTaxBenefitSystem
from policyengine_core.reforms import Reform

YEAR = 2026
DATA_DIR = "src/data"

CAPITAL_INCOME_VARS = [
    "long_term_capital_gains",
    "short_term_capital_gains",
    "qualified_dividend_income",
    "taxable_interest_income",
    "rental_income",
]
LABOR_INCOME_VARS = [
    "employment_income",
    "self_employment_income",
]


def get_weights(sim):
    return sim.calc("person_weight", period=YEAR).values


def decile_shares(sim):
    """Compute income share by decile."""
    hni = sim.calc("household_net_income", period=YEAR, map_to="person")
    income = hni.values
    weights = get_weights(sim)

    sorted_idx = np.argsort(income)
    s_inc = income[sorted_idx]
    s_w = weights[sorted_idx]
    cum_w = np.cumsum(s_w)
    total_w = cum_w[-1]
    total_inc = (s_inc * s_w).sum()

    shares = []
    for d in range(10):
        lo = total_w * d / 10
        hi = total_w * (d + 1) / 10
        mask = (cum_w > lo) & (cum_w <= hi)
        if d == 0:
            mask = cum_w <= hi
        share = (s_inc[mask] * s_w[mask]).sum() / total_inc if total_inc else 0
        shares.append(round(float(share), 4))
    return shares


def basic_metrics(sim):
    """Compute core metrics from a simulation."""
    hni = sim.calc("household_net_income", period=YEAR, map_to="person")
    poverty = sim.calc("person_in_poverty", period=YEAR, map_to="person")
    weights = get_weights(sim)
    income = hni.values

    gini = float(hni.gini())
    poverty_rate = float(poverty.mean())

    # Market Gini (before taxes and transfers)
    market_inc = sim.calc("market_income", period=YEAR, map_to="person")
    market_gini = float(market_inc.gini())

    # Top/bottom 10% share
    sorted_idx = np.argsort(income)
    s_inc = income[sorted_idx]
    s_w = weights[sorted_idx]
    cum_w = np.cumsum(s_w)
    total_w = cum_w[-1]
    total_inc = (s_inc * s_w).sum()

    p90_idx = np.searchsorted(cum_w, total_w * 0.9)
    top10 = float((s_inc[p90_idx:] * s_w[p90_idx:]).sum() / total_inc)
    p10_idx = np.searchsorted(cum_w, total_w * 0.1)
    bottom10 = float((s_inc[:p10_idx] * s_w[:p10_idx]).sum() / total_inc)

    # Revenue
    fed_rev = float(sim.calc("income_tax", period=YEAR).sum() / 1e9)
    state_rev = float(sim.calc("state_income_tax", period=YEAR).sum() / 1e9)

    return {
        "marketGini": round(market_gini, 4),
        "netGini": round(gini, 4),
        "povertyRate": round(poverty_rate, 4),
        "fedRevenue": round(fed_rev),
        "stateRevenue": round(state_rev),
        "totalRevenue": round(fed_rev + state_rev),
        "top10Share": round(top10, 4),
        "bottom10Share": round(bottom10, 4),
        "meanNetIncome": float(hni.mean()),
    }


def scale_capital(sim, multiplier):
    """Scale positive capital income by multiplier on an existing sim."""
    for var in CAPITAL_INCOME_VARS:
        vals = sim.calc(var, period=YEAR).values
        sim.set_input(var, YEAR, np.where(vals > 0, vals * multiplier, vals))


def shift_labor_to_capital(sim, shift_pct):
    """Shift shift_pct% of labor income to capital, proportional to holdings."""
    weights = get_weights(sim)
    total_shifted = 0

    for var in LABOR_INCOME_VARS:
        vals = sim.calc(var, period=YEAR).values
        reduction = vals * (shift_pct / 100)
        sim.set_input(var, YEAR, vals - reduction)
        total_shifted += (reduction * weights).sum()

    cap_vals = {}
    cap_pos = {}
    for var in CAPITAL_INCOME_VARS:
        cap_vals[var] = sim.calc(var, period=YEAR).values
        cap_pos[var] = np.maximum(cap_vals[var], 0)

    total_pos_cap = sum((cap_pos[v] * weights).sum() for v in CAPITAL_INCOME_VARS)

    if total_pos_cap > 0:
        for var in CAPITAL_INCOME_VARS:
            addition = cap_pos[var] * (total_shifted / total_pos_cap)
            sim.set_input(var, YEAR, cap_vals[var] + addition)
    else:
        per_person = total_shifted / weights.sum()
        sim.set_input(
            "long_term_capital_gains",
            YEAR,
            cap_vals["long_term_capital_gains"] + per_person,
        )


def detailed_metrics(sim):
    """Extended metrics including program breakdowns."""
    m = basic_metrics(sim)
    m["income_tax_b"] = float(sim.calc("income_tax", period=YEAR).sum() / 1e9)
    m["employee_payroll_b"] = float(
        sim.calc("employee_payroll_tax", period=YEAR).sum() / 1e9
    )
    m["employer_payroll_b"] = float(
        sim.calc("employee_payroll_tax", period=YEAR).sum() / 1e9
    )
    m["eitc_cost_b"] = float(sim.calc("eitc", period=YEAR).sum() / 1e9)
    m["ctc_cost_b"] = float(sim.calc("ctc", period=YEAR).sum() / 1e9)
    m["snap_cost_b"] = float(sim.calc("snap", period=YEAR).sum() / 1e9)
    m["decile_shares"] = decile_shares(sim)
    return m


# ===== Capital Sweep =====
def gen_capital_sweep():
    print("Generating capitalSweepData.json...")
    multipliers = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0]
    labels = ["Baseline", "1.2x", "1.5x", "1.8x", "2x", "2.5x", "3x", "4x", "5x"]

    sweep = []
    deciles_by_key = {}

    for mult, label in zip(multipliers, labels):
        print(f"  Capital x{mult}...")
        sim = Microsimulation()
        if mult > 1.0:
            scale_capital(sim, mult)

        m = basic_metrics(sim)
        cap_total = sum(sim.calc(v, period=YEAR).sum() for v in CAPITAL_INCOME_VARS)
        lab_total = sum(sim.calc(v, period=YEAR).sum() for v in LABOR_INCOME_VARS)
        market = cap_total + lab_total
        cap_share = round(float(cap_total / market), 3) if market > 0 else 0

        sweep.append({
            "multiplier": mult,
            "capitalShare": cap_share,
            "label": label,
            **m,
        })

        ds = decile_shares(sim)
        if label == "Baseline":
            deciles_by_key["baseline"] = ds
        elif label == "2x":
            deciles_by_key["2x"] = ds
        elif label == "5x":
            deciles_by_key["5x"] = ds

    baseline_sim = Microsimulation()
    cap_total_b = sum(
        baseline_sim.calc(v, period=YEAR).sum() for v in CAPITAL_INCOME_VARS
    )
    lab_total_b = sum(
        baseline_sim.calc(v, period=YEAR).sum() for v in LABOR_INCOME_VARS
    )
    base_cap_share = round(
        float(cap_total_b / (cap_total_b + lab_total_b)) * 100
    )

    result = {
        "sweep": sweep,
        "deciles": {
            "labels": [f"D{i}" for i in range(1, 11)],
            **deciles_by_key,
        },
        "metadata": {
            "year": YEAR,
            "description": "Capital income multiplied 1x-5x (positive gains only, losses unchanged). Models AI increasing returns to capital without amplifying existing losses.",
            "baselineCapitalShare": f"{base_cap_share}%",
        },
    }
    with open(f"{DATA_DIR}/capitalSweepData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


# ===== Capital Doubling =====
def gen_capital_doubling():
    print("Generating capitalDoublingData.json...")
    baseline_sim = Microsimulation()
    baseline = detailed_metrics(baseline_sim)

    doubled_sim = Microsimulation()
    scale_capital(doubled_sim, 2.0)
    doubled = detailed_metrics(doubled_sim)

    # Compute total capital added
    cap_baseline = sum(
        baseline_sim.calc(v, period=YEAR).sum() for v in CAPITAL_INCOME_VARS
    )
    cap_doubled = sum(
        doubled_sim.calc(v, period=YEAR).sum() for v in CAPITAL_INCOME_VARS
    )
    total_added = float((cap_doubled - cap_baseline) / 1e9)

    # Revenue change
    rev_change = (doubled["fedRevenue"] + doubled["stateRevenue"]) - (
        baseline["fedRevenue"] + baseline["stateRevenue"]
    )

    doubled["revenue_change_b"] = rev_change
    doubled["income_tax_change_b"] = doubled["income_tax_b"] - baseline["income_tax_b"]
    doubled["employee_payroll_change_b"] = (
        doubled["employee_payroll_b"] - baseline["employee_payroll_b"]
    )
    doubled["employer_payroll_change_b"] = (
        doubled["employer_payroll_b"] - baseline["employer_payroll_b"]
    )
    doubled["eitc_change_b"] = doubled["eitc_cost_b"] - baseline["eitc_cost_b"]
    doubled["ctc_change_b"] = doubled["ctc_cost_b"] - baseline["ctc_cost_b"]
    doubled["snap_change_b"] = doubled["snap_cost_b"] - baseline["snap_cost_b"]

    # Rename for compatibility
    for d in [baseline, doubled]:
        d["market_gini"] = d.pop("marketGini")
        d["net_gini"] = d.pop("netGini")
        d["spm_poverty_rate"] = d.pop("povertyRate")
        d["mean_net_income"] = d.pop("meanNetIncome")
        d["fed_revenue_b"] = d.pop("fedRevenue")
        d["state_revenue_b"] = d.pop("stateRevenue")
        d.pop("totalRevenue", None)
        d.pop("top10Share", None)
        d.pop("bottom10Share", None)

    result = {
        "year": YEAR,
        "total_capital_added_b": total_added,
        "baseline": baseline,
        "doubled": doubled,
    }
    with open(f"{DATA_DIR}/capitalDoublingData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


# ===== Labor Shift =====
def gen_labor_shift():
    print("Generating laborShiftData.json...")
    shifts = [0, 10, 25, 50]
    labels = ["Baseline", "10% shift", "25% shift", "50% shift"]

    scenarios = []
    deciles_data = {}

    for pct, label in zip(shifts, labels):
        print(f"  {label}...")
        sim = Microsimulation()
        if pct > 0:
            shift_labor_to_capital(sim, pct)
        m = basic_metrics(sim)
        scenarios.append({
            "label": label,
            "shiftPct": pct,
            **m,
        })
        if label == "Baseline":
            deciles_data["baseline"] = decile_shares(sim)
        elif label == "50% shift":
            deciles_data["50pctShift"] = decile_shares(sim)

    # 50% shift + UBI
    print("  50% shift + UBI...")
    # Calculate extra tax revenue from 50% shift
    base_sim = Microsimulation()
    base_rev = base_sim.calc("income_tax", period=YEAR).sum()
    shift50_sim = Microsimulation()
    shift_labor_to_capital(shift50_sim, 50)
    shift50_rev = shift50_sim.calc("income_tax", period=YEAR).sum()
    extra_rev = shift50_rev - base_rev
    population = get_weights(base_sim).sum()

    # Even if revenue drops, use a modest UBI funded externally for comparison
    ubi_amount = max(round(float(extra_rev / population)), 100)

    reform = Reform.from_dict(
        {
            "gov.contrib.ubi_center.basic_income.amount.person.flat": {
                "2026-01-01.2028-12-31": ubi_amount
            },
        },
        "policyengine_us",
    )
    ubi_sim = Microsimulation(reform=reform)
    shift_labor_to_capital(ubi_sim, 50)
    ubi_m = basic_metrics(ubi_sim)
    scenarios.append({
        "label": "50% shift + UBI",
        "shiftPct": 50,
        **ubi_m,
    })
    deciles_data["50pctUBI"] = decile_shares(ubi_sim)

    result = {
        "scenarios": scenarios,
        "deciles": {
            "labels": [f"D{i}" for i in range(1, 11)],
            **deciles_data,
        },
        "metadata": {
            "year": YEAR,
            "description": "Employment and self-employment income reduced by X%, redistributed to capital income proportional to existing holdings at constant total income. Models AI-driven automation shifting labor income to capital owners.",
        },
    }
    with open(f"{DATA_DIR}/laborShiftData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


# ===== Shift Sweep =====
def gen_shift_sweep():
    print("Generating shiftSweepData.json...")
    shifts = [0, 10, 20, 30, 50, 100]
    labels = [
        "Baseline",
        "10% shift",
        "20% shift",
        "30% shift",
        "50% shift",
        "100% shift",
    ]

    baseline_sim = Microsimulation()
    base_det = detailed_metrics(baseline_sim)

    scenarios = []
    for pct, label in zip(shifts, labels):
        print(f"  {label}...")
        sim = Microsimulation()
        if pct > 0:
            shift_labor_to_capital(sim, pct)
        det = detailed_metrics(sim)

        rev_change = (det["fedRevenue"] + det["stateRevenue"]) - (
            base_det["fedRevenue"] + base_det["stateRevenue"]
        )

        scenarios.append({
            "shift_pct": pct,
            "label": label,
            "net_gini": det["netGini"],
            "market_gini": det["marketGini"],
            "spm_poverty_rate": det["povertyRate"],
            "fed_revenue_b": det["fedRevenue"],
            "revenue_change_b": rev_change,
            "income_tax_change_b": det["income_tax_b"] - base_det["income_tax_b"],
            "employee_payroll_change_b": det["employee_payroll_b"]
            - base_det["employee_payroll_b"],
            "employer_payroll_change_b": det["employer_payroll_b"]
            - base_det["employer_payroll_b"],
            "eitc_change_b": det["eitc_cost_b"] - base_det["eitc_cost_b"],
            "ctc_change_b": det["ctc_cost_b"] - base_det["ctc_cost_b"],
            "snap_change_b": det["snap_cost_b"] - base_det["snap_cost_b"],
        })

    result = {"year": YEAR, "scenarios": scenarios}
    with open(f"{DATA_DIR}/shiftSweepData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


# ===== MTR Data =====
def gen_mtr_data():
    print("Generating mtrData.json...")

    sources = [
        ("Emp", "employment_income"),
        ("Self-emp", "self_employment_income"),
        ("LTCG", "long_term_capital_gains"),
        ("STCG", "short_term_capital_gains"),
        ("Qual div", "qualified_dividend_income"),
    ]

    # Use household-level sums for consistent weighting
    baseline_sim = Microsimulation()
    baseline_hni = baseline_sim.calc("household_net_income", period=YEAR).sum()

    mtrs = []
    for label, var_name in sources:
        print(f"  MTR for {label}...")
        sim = Microsimulation()
        vals = sim.calc(var_name, period=YEAR)

        # 1% proportional bump
        raw = vals.values
        sim.set_input(var_name, YEAR, raw * 1.01)

        bumped_hni = sim.calc("household_net_income", period=YEAR).sum()
        # Map income to household level for consistent aggregation
        baseline_inc = baseline_sim.calc(
            var_name, period=YEAR, map_to="household"
        ).sum()
        bumped_inc = sim.calc(var_name, period=YEAR, map_to="household").sum()

        income_change = float(bumped_inc - baseline_inc)
        hni_change = float(bumped_hni - baseline_hni)
        mtr = 1 - (hni_change / income_change) if income_change != 0 else 0

        mtrs.append({
            "source": label,
            "key": var_name,
            "mtr": round(float(mtr), 4),
        })

    result = {
        "year": YEAR,
        "method": "dollar-weighted (1% proportional bump)",
        "note": "Dollar-weighted MTR weights each person's marginal rate by their income share, not headcount. Relevant for predicting revenue impact of income-type shifts.",
        "baseline": mtrs,
    }
    with open(f"{DATA_DIR}/mtrData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


# ===== Cliff Data (household-level) =====
def gen_cliff_data():
    print("Generating cliffData.json...")
    from policyengine_us import Simulation

    # Single parent, 1 child, federal minimum wage, Texas
    base_employment = 15080
    steps = 200

    def run_household(cap_income, cap_var="qualified_dividend_income"):
        situation = {
            "people": {
                "parent": {
                    "age": {YEAR: 30},
                    "employment_income": {YEAR: base_employment},
                    cap_var: {YEAR: cap_income},
                },
                "child": {"age": {YEAR: 5}},
            },
            "tax_units": {
                "tax_unit": {
                    "members": ["parent", "child"],
                    "filing_status": {YEAR: "HEAD_OF_HOUSEHOLD"},
                }
            },
            "spm_units": {"spm_unit": {"members": ["parent", "child"]}},
            "households": {
                "household": {
                    "members": ["parent", "child"],
                    "state_code": {YEAR: "TX"},
                }
            },
            "families": {"family": {"members": ["parent", "child"]}},
            "marital_units": {
                "marital_unit": {"members": ["parent"]},
                "child_marital_unit": {"members": ["child"]},
            },
        }
        sim = Simulation(situation=situation)
        return {
            "capitalIncome": round(float(cap_income)),
            "netIncome": round(float(sim.calculate("spm_unit_net_income", YEAR)[0])),
            "eitc": round(float(sim.calculate("eitc", YEAR)[0])),
            "snap": round(float(sim.calculate("snap", YEAR)[0])),
            "incomeTax": round(float(sim.calculate("income_tax", YEAR)[0])),
            "ssi": round(float(sim.calculate("ssi", YEAR)[0])),
        }

    max_cap = 30000
    cap_range = np.linspace(0, max_cap, steps + 1)

    print("  Running dividend scenarios...")
    dividends = [run_household(c, "qualified_dividend_income") for c in cap_range]
    print("  Running LTCG scenarios...")
    ltcg = [run_household(c, "long_term_capital_gains") for c in cap_range]

    result = {
        "dividends": dividends,
        "ltcg": ltcg,
        "household": {
            "description": f"Single parent, 1 child, federal minimum wage (${base_employment:,}/yr), Texas",
            "year": YEAR,
        },
    }
    with open(f"{DATA_DIR}/cliffData.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Done.")


if __name__ == "__main__":
    print(f"Regenerating all data for {YEAR}...\n")

    gen_capital_sweep()
    gen_capital_doubling()
    gen_labor_shift()
    gen_shift_sweep()
    gen_mtr_data()
    gen_cliff_data()

    print("\nAll data files regenerated!")
