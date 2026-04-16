"""Shared fiscal helpers for analysis scenarios."""

from .constants import YEAR


def revenue_components(sim):
    """Return federal revenue/cost totals (in dollars) for a sim/branch."""
    income_tax = float(
        sim.calculate("income_tax", map_to="household", period=YEAR).sum()
    )
    employee_payroll = float(
        sim.calculate(
            "employee_social_security_tax", map_to="household", period=YEAR
        ).sum()
        + sim.calculate(
            "employee_medicare_tax", map_to="household", period=YEAR
        ).sum()
    )
    employer_payroll = float(
        sim.calculate(
            "employer_social_security_tax", map_to="household", period=YEAR
        ).sum()
        + sim.calculate(
            "employer_medicare_tax", map_to="household", period=YEAR
        ).sum()
    )
    eitc = float(sim.calculate("eitc", map_to="household", period=YEAR).sum())
    ctc = float(sim.calculate("ctc", map_to="household", period=YEAR).sum())
    snap = float(sim.calculate("snap", map_to="household", period=YEAR).sum())
    return {
        "income_tax": income_tax,
        "employee_payroll": employee_payroll,
        "employer_payroll": employer_payroll,
        "eitc": eitc,
        "ctc": ctc,
        "snap": snap,
    }


def net_fiscal_impact(components, baseline_components):
    """Net revenue change vs baseline (positive = government gains)."""
    delta_income_tax = components["income_tax"] - baseline_components["income_tax"]
    delta_employee_payroll = (
        components["employee_payroll"] - baseline_components["employee_payroll"]
    )
    delta_employer_payroll = (
        components["employer_payroll"] - baseline_components["employer_payroll"]
    )
    delta_eitc = -(components["eitc"] - baseline_components["eitc"])
    delta_ctc = -(components["ctc"] - baseline_components["ctc"])
    delta_snap = -(components["snap"] - baseline_components["snap"])
    total = (
        delta_income_tax
        + delta_employee_payroll
        + delta_employer_payroll
        + delta_eitc
        + delta_ctc
        + delta_snap
    )
    return {
        "income_tax_change": delta_income_tax,
        "employee_payroll_change": delta_employee_payroll,
        "employer_payroll_change": delta_employer_payroll,
        "eitc_change": delta_eitc,
        "ctc_change": delta_ctc,
        "snap_change": delta_snap,
        "total_change": total,
    }


def compute_ubi_amount(extra_budget, total_population):
    """Convert fiscal space into a flat per-person annual payment."""
    if extra_budget <= 0 or total_population <= 0:
        return 0.0
    return extra_budget / total_population
