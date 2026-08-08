"""Rank states by how exposed their own-source revenue is to the AI shock.

The scenario run already stores per-state deltas; what it does not store is the
2030 per-state baseline those deltas should be measured against. This script
runs one baseline simulation to get those levels, joins them to the deltas in
`ai_scenarios.json`, and writes a normalized exposure ranking.

SCOPE, and it decides how the ranking may be read
-------------------------------------------------
`household_state_tax_before_refundable_credits` adds exactly two things at
policyengine-us 1.764.6: `state_income_tax_before_refundable_credits` and
`state_use_tax`. So the channel measured here is **state income tax** (plus a
small use-tax component), net of refundable state credits and state-funded
benefits.

It is *not* state own-source revenue in the budgetary sense. General sales
tax, property tax, corporate income tax, severance taxes and fees are outside
the model. Nationally those are roughly half of state and local own-source
revenue, and they are exactly the bases that no-income-tax states rely on.

A state that scores near zero here is therefore making a statement about the
**income-tax channel**, not about budgetary resilience: Texas and Florida
collect through sales taxes this model does not carry, so their true exposure
to an AI boom is unmeasured rather than absent. The one informative
zero-income-tax case is Washington, whose capital-gains excise is modelled and
so does register.

Usage:
    python -m analysis.compute_state_exposure
"""

from __future__ import annotations

import json
import os

from .ai_scenarios import TARGET_YEAR
from .fiscal import state_revenue_components
from .policyengine_runtime import managed_us_microsimulation

SCENARIOS_PATH = os.path.join(
    os.path.dirname(__file__), "outputs", "ai_scenarios.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "outputs", "state_exposure.json"
)
WEBSITE_OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "src", "data", "stateExposureData.json"
)
BASELINE_CACHE = os.path.join(
    os.path.expanduser("~"),
    ".policyengine-runs",
    "ai-inequality-state-baseline-2030.json",
)

#: Cells to rank. The wage-spread variants bracket the range the Budget Lab
#: spans, so a state's exposure is reported as a band rather than a point.
VARIANTS = ["compressive", "proportional", "expansive"]

#: States whose modelled "income tax" reaches capital income only, so the
#: percentage is a share of a narrow instrument rather than of a broad tax.
#: Verified from the variable composition at policyengine-us 1.764.6:
#: `wa_income_tax_before_refundable_credits` adds exactly
#: `wa_capital_gains_tax` and `wa_millionaires_tax` — no wage income tax.
#: Low-rate broad-base states (AZ, LA, MS) are NOT in this category: their
#: percentages are comparable, they simply tax at lower rates.
CAPITAL_ONLY_INCOME_TAX_STATES = {"WA"}

SCOPE_NOTE = (
    "State income tax (plus use tax) net of refundable state credits and "
    "state-funded benefits. Sales, property, corporate and severance taxes are "
    "outside the model, so a low score means low exposure through the "
    "income-tax channel, not budgetary resilience."
)


def baseline_state_levels(year=TARGET_YEAR, verbose=True):
    """Per-state baseline own-source levels, cached so this runs once."""
    if os.path.exists(BASELINE_CACHE):
        if verbose:
            print("baseline state levels ... (cached)", flush=True)
        with open(BASELINE_CACHE) as handle:
            return json.load(handle)

    if verbose:
        print("baseline state levels ... (running simulation)", flush=True)
    sim = managed_us_microsimulation()
    per_state = state_revenue_components(sim, year=year)

    os.makedirs(os.path.dirname(BASELINE_CACHE), exist_ok=True)
    with open(BASELINE_CACHE, "w") as handle:
        json.dump(per_state, handle, default=float)
    return per_state


def _baseline_net(state_totals):
    """Baseline modelled state net own-source revenue, $B."""
    return (
        state_totals.get("household_state_tax_before_refundable_credits", 0.0)
        - state_totals.get("household_refundable_state_tax_credits", 0.0)
        - state_totals.get("household_state_benefits", 0.0)
    ) / 1e9


def build(year=TARGET_YEAR, verbose=True):
    with open(SCENARIOS_PATH) as handle:
        scenarios = json.load(handle)

    rows_by_label = {r["scenario"]["label"]: r for r in scenarios["scenarios"]}
    baseline = baseline_state_levels(year=year, verbose=verbose)

    states = {}
    for variant in VARIANTS:
        row = rows_by_label.get(f"Rapid / {variant}")
        if row is None:
            continue
        for code, delta in row["state_deltas"].items():
            if not isinstance(delta, dict):
                continue
            entry = states.setdefault(
                code,
                {
                    "state": code,
                    "baseline_net_revenue_b": _baseline_net(baseline.get(code, {})),
                    "_households": baseline.get(code, {}).get(
                        "household_weight", 0.0
                    ),
                    "deltas_b": {},
                    "exposure_pct": {},
                },
            )
            change = delta.get("state_net_change_b", 0.0)
            entry["deltas_b"][variant] = change
            base = entry["baseline_net_revenue_b"]
            entry["exposure_pct"][variant] = (
                None if base <= 0 else 100.0 * change / base
            )

    ranked = []
    for entry in states.values():
        pcts = [v for v in entry["exposure_pct"].values() if v is not None]
        entry["exposure_pct_proportional"] = entry["exposure_pct"].get("proportional")
        entry["exposure_pct_min"] = min(pcts) if pcts else None
        entry["exposure_pct_max"] = max(pcts) if pcts else None

        # Three buckets, because the percentage means different things in each.
        # A state with no modelled base is unmeasured, not unexposed. A state
        # whose modelled income tax reaches only capital income has a narrow
        # denominator, so its percentage is not comparable to a broad-base
        # state's — that is a fact about the instrument, not about the rate.
        households = entry.pop("_households", 0.0)
        base = entry["baseline_net_revenue_b"]
        entry["modelled_base_per_household"] = (
            (base * 1e9 / households) if households > 0 else 0.0
        )
        if base <= 0:
            kind = "none"
        elif entry["state"] in CAPITAL_ONLY_INCOME_TAX_STATES:
            kind = "capital_only"
        else:
            kind = "broad"
        entry["modelled_base_kind"] = kind
        entry["comparable_percentage"] = kind == "broad"
        ranked.append(entry)

    ranked.sort(
        key=lambda e: (
            e["exposure_pct_proportional"] is None,
            -(e["exposure_pct_proportional"] or 0.0),
        )
    )

    payload = {
        "year": year,
        "scope_note": SCOPE_NOTE,
        "metadata": {
            k: scenarios["metadata"].get(k)
            for k in (
                "policyengine_version",
                "country_model_version",
                "certified_data_build_id",
            )
        },
        "states": ranked,
    }

    with open(OUTPUT_PATH, "w") as handle:
        json.dump(payload, handle, indent=2, default=float)

    # Trimmed payload for the site: drop nothing, it is already small.
    with open(WEBSITE_OUTPUT_PATH, "w") as handle:
        json.dump(payload, handle, indent=2, default=float)

    if verbose:
        _report(payload)
    return payload


def _report(payload):
    print(f"\nSTATE EXPOSURE TO THE AI CAPITAL SHOCK (Rapid, {payload['year']})")
    print(f"scope: {payload['scope_note']}\n")
    header = (
        f"{'state':6s} {'baseline $B':>12s} {'Δ prop $B':>10s} "
        f"{'% of base':>10s} {'range across λ':>18s}"
    )
    print(header)
    print("-" * len(header))
    shown = 0
    for e in payload["states"]:
        if not e["comparable_percentage"]:
            continue
        shown += 1
        if shown > 15:
            break
        print(
            f"{e['state']:6s} {e['baseline_net_revenue_b']:>12.1f} "
            f"{e['deltas_b'].get('proportional', 0.0):>10.2f} "
            f"{e['exposure_pct_proportional']:>9.2f}% "
            f"{e['exposure_pct_min']:>8.2f}% – {e['exposure_pct_max']:.2f}%"
        )

    narrow = [
        e for e in payload["states"] if e["modelled_base_kind"] == "capital_only"
    ]
    if narrow:
        print("\nCapital-only modelled income tax — percentage NOT comparable:")
        for e in narrow:
            print(
                f"  {e['state']}: {e['deltas_b'].get('proportional', 0.0):+.2f}B, "
                f"which is {e['exposure_pct_proportional']:.1f}% of a "
                f"${e['baseline_net_revenue_b']:.1f}B modelled base — but that "
                f"base is the capital-gains and millionaires taxes alone, not "
                f"the state's budget. The dollar delta is the meaningful figure."
            )

    zero = [e["state"] for e in payload["states"] if e["modelled_base_kind"] == "none"]
    print(
        f"\nNo modelled base at all ({len(zero)}): {', '.join(sorted(zero))}"
        "\n  -> unmeasured through this channel, NOT low exposure: these states"
        "\n     fund themselves through sales and other taxes outside the model."
    )


if __name__ == "__main__":
    build()
