"""Bridge our scenario results to a Budget Lab-comparable revenue total.

Our headline covers the household sector across federal and state, net of the
whole transfer system. Theirs covers federal individual income tax plus payroll
plus a corporate wedge, with no states and no non-tax benefits. Quoting the two
side by side is wrong without an explicit bridge, so this builds one.

Every adjustment uses either our own run output or a parameter The Budget Lab
publishes in its methodology document ("Methodology: How potential AI futures
interact with the current tax system", 20 July 2026):

  Corporate wedge.  They layer a single aggregate number onto their
  microsimulation total, not attributed to households:

      dR_CIT = X * (R_CIT_CBO / Y0_K) = X * tau_stat * eta * kappa

  with tau_stat = 21%, kappa ~ 0.50 (NIPA C-corp share of capital income),
  a CBO 2030 CIT anchor of ~$486B, and eta ~ 1 "in practice". Applying their
  formula to OUR capital flow X estimates what their corporate line would add
  to our estimate. It is emphatically not PolicyEngine modelling corporate tax
  — it is their wedge, borrowed, and it inherits every assumption they list
  (constant statutory rate, constant avoidance gap, constant corporate-form
  share).

  Their capital base.  The same identity inverts to recover the realized
  taxable capital income their run starts from, which is otherwise unpublished
  and is the single most useful cross-check on our own capital aggregate.

Usage:
    python analysis/reconcile_budget_lab.py [ai_scenarios.json]
"""

import json
import os
import sys

# Budget Lab methodology parameters, 20 July 2026.
CIT_STATUTORY_RATE = 0.21
CCORP_SHARE_OF_CAPITAL = 0.50  # kappa, via NIPA
CIT_EFFECTIVE_ADJUSTMENT = 1.0  # eta, "falls out to roughly one in practice"
CBO_2030_CIT_ANCHOR_B = 486.0

#: Effective rate applied to the excess capital flow.
CIT_WEDGE_RATE = CIT_STATUTORY_RATE * CIT_EFFECTIVE_ADJUSTMENT * CCORP_SHARE_OF_CAPITAL

#: Their published totals. Only figures stated in the report text are used;
#: per-instrument values appear solely in charts and are not read off them.
THEIR_RAPID_MAX_ALL_IN_B = 216.0  # Rapid + expansive, "a maximum of $216 billion"
THEIR_MODERATE_RANGE_B = (85.0, 127.0)
THEIR_CBO_2030_TOTAL_REVENUE_B = 6595.0

DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "outputs", "ai_scenarios.json"
)


def their_implied_capital_base_b():
    """Invert the wedge identity for their baseline realized capital income."""
    return CBO_2030_CIT_ANCHOR_B / CIT_WEDGE_RATE


def federal_refundable_credits_b(row):
    """Federal share of refundable credits (total less the state share)."""
    return row.get("refundable_credits_change_b", 0.0) - row.get(
        "state_refundable_credits_change_b", 0.0
    )


def bridge(row, baseline_capital_b):
    """Walk our total to a Budget Lab-comparable total, in $B."""
    ours_total = row["total_rev_change_b"]

    fed_iit_gross = row.get("fed_income_tax_change_b", 0.0)
    fed_refundable = federal_refundable_credits_b(row)
    fed_iit_net = fed_iit_gross - fed_refundable
    payroll = row.get("payroll_change_b", 0.0)

    # Excess capital income actually routed into our taxable base.
    excess_capital = baseline_capital_b * row["scenario"]["effective_capital_growth"]
    cit_wedge = excess_capital * CIT_WEDGE_RATE

    return {
        "ours_total": ours_total,
        "fed_iit_gross": fed_iit_gross,
        "fed_refundable": fed_refundable,
        "fed_iit_net": fed_iit_net,
        "payroll": payroll,
        "household_federal_tax_only": fed_iit_net + payroll,
        "excess_capital": excess_capital,
        "cit_wedge": cit_wedge,
        "comparable_total": fed_iit_net + payroll + cit_wedge,
    }


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PATH
    with open(path) as handle:
        data = json.load(handle)

    rows = {row["scenario"]["label"]: row for row in data["scenarios"]}
    baseline_capital_b = data["baseline"]["context"]["positive_capital_income_t"] * 1000

    print("=" * 84)
    print("BRIDGING OUR TOTALS TO A BUDGET LAB-COMPARABLE BASIS")
    print(f"  our run: {data['metadata']['certified_data_build_id']}")
    print(
        f"  their corporate wedge rate: {CIT_WEDGE_RATE:.3f}"
        f"  (21% statutory x eta 1.0 x kappa 0.50)"
    )
    print("=" * 84)

    theirs_capital = their_implied_capital_base_b()
    print("\nCAPITAL BASE CROSS-CHECK (2030 realized taxable capital income, $B)")
    print(f"  theirs, implied by their wedge identity   {theirs_capital:>10,.0f}")
    print(f"  ours, positive capital income             {baseline_capital_b:>10,.0f}")
    print(
        f"  ratio ours/theirs                         {baseline_capital_b / theirs_capital:>10.2f}"
    )
    print("  Their value is derived from published parameters, not stated;")
    print("  it moves inversely with eta, which they report only as ~1.")

    header = (
        f"\n{'scenario':22s} {'ours':>8s} {'fed IIT':>9s} {'payroll':>8s} "
        f"{'hh fed':>8s} {'+CIT':>7s} {'compar.':>9s}"
    )
    print(header)
    print("-" * (len(header) - 1))
    for label in (
        "Slow / proportional",
        "Moderate / proportional",
        "Moderate / expansive",
        "Rapid / proportional",
        "Rapid / expansive",
    ):
        row = rows.get(label)
        if row is None:
            continue
        b = bridge(row, baseline_capital_b)
        print(
            f"{label:22s} {b['ours_total']:>+8.0f} {b['fed_iit_net']:>+9.0f} "
            f"{b['payroll']:>+8.0f} {b['household_federal_tax_only']:>+8.0f} "
            f"{b['cit_wedge']:>+7.0f} {b['comparable_total']:>+9.0f}"
        )
    print("\n  ours     = household total, federal + state, net of all transfers")
    print("  fed IIT  = federal individual income tax after refundable credits")
    print("  hh fed   = fed IIT + payroll (their microsimulation's coverage)")
    print("  +CIT     = their wedge formula applied to our capital flow")
    print("  compar.  = the column to set beside their published totals")

    print("\nAGAINST THEIR PUBLISHED FIGURES")
    rapid_exp = rows.get("Rapid / expansive")
    if rapid_exp:
        b = bridge(rapid_exp, baseline_capital_b)
        print(
            f"  Rapid + expansive: ours {b['comparable_total']:+,.0f}B  vs "
            f"theirs {THEIR_RAPID_MAX_ALL_IN_B:+,.0f}B"
            f"   ({b['comparable_total'] / THEIR_RAPID_MAX_ALL_IN_B:.2f}x)"
        )
        print(
            f"    as a share of CBO 2030 revenue: ours "
            f"{b['comparable_total'] / THEIR_CBO_2030_TOTAL_REVENUE_B:.1%}"
            f"  vs theirs "
            f"{THEIR_RAPID_MAX_ALL_IN_B / THEIR_CBO_2030_TOTAL_REVENUE_B:.1%}"
        )
    lo, hi = THEIR_MODERATE_RANGE_B
    mod = [
        bridge(rows[f"Moderate / {v}"], baseline_capital_b)["comparable_total"]
        for v in ("compressive", "proportional", "expansive")
        if f"Moderate / {v}" in rows
    ]
    if mod:
        print(
            f"  Moderate range: ours {min(mod):+,.0f}B to {max(mod):+,.0f}B  vs "
            f"theirs {lo:+,.0f}B to {hi:+,.0f}B"
        )

    print("\nWHAT REMAINS NON-COMPARABLE EVEN AFTER THE BRIDGE")
    print("  - Their capital flow is apportioned by SCF-imputed total wealth;")
    print("    ours by existing realized capital income, which concentrates it")
    print("    more at the top. They say a narrower base would do exactly that.")
    print("  - Their pass-through split is active/passive-aware (passive 25/75")
    print("    labor/capital, active 75/25 below the 99.99th wage percentile).")
    print("    PolicyEngine-US carries no active/passive flag, so ours applies")
    print("    the single 75/25 active rule and under-assigns passive")
    print("    pass-through to capital.")
    print("  - Their microdata is the 2015 IRS PUF aged to 2030; ours is")
    print("    populace-us, a survey-based file with imputation.")
    print("  - The wedge inherits their constant-rate assumptions wholesale.")


if __name__ == "__main__":
    main()
