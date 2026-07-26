"""Tests for the AI scenario website export shape."""

import pytest

from analysis.website_exports import (
    AI_SCENARIO_DESCRIPTION,
    ai_scenarios_website_payload,
)


def _scenario_row(label="Rapid / proportional", **overrides):
    row = {
        "scenario": {
            "name": "Rapid",
            "label": label,
            "inequality": "proportional",
            "hold_shares_fixed": False,
            "realization_rate": 1.0,
            "gdp_growth": 0.0717,
            "capital_growth": 0.1728,
            "labor_growth": -0.0094,
            "inequality_lambda": 1.0,
        },
        "diagnostics": {"labor_crossover_income": None},
        "total_rev_change_b": 205.7,
        "fed_income_tax_change_b": 180.2,
        "payroll_change_b": -16.1,
        "fed_capital_gains_tax_change_b": 40.0,
        "benefits_change_b": 3.2,
        "refundable_credits_change_b": -1.1,
        "state_tax_change_b": 22.4,
        "snap_change_b": 1.0,
        "eitc_change_b": -0.4,
        "market_income_change_b": 764.0,
        "net_income_change_b": 558.3,
        "spm_poverty_rate": 0.1258,
        "net_gini": 0.4644,
        "market_gini": 0.5200,
        "net_top_1_share": 0.1400,
        "net_top_10_share": 0.3100,
        "net_bottom_20_share": 0.0400,
        "decile_shares": [0.01 * i for i in range(1, 11)],
    }
    row.update(overrides)
    return row


def _result(**overrides):
    result = {
        "year": 2030,
        "metadata": {
            "corporate_tax_scope_note": "no corporate tax",
            "policyengine_version": "4.22.3",
            "country_model_package": "policyengine-us",
            "country_model_version": "1.764.6",
            "data_package": "populace-data",
            "data_version": "0.1.0",
            "dataset_name": "populace_us_2024",
            "certified_data_build_id": "build-id",
            "capital_income_vars": ["long_term_capital_gains"],
        },
        "baseline": {
            "spm_poverty_rate": 0.1250,
            "net_gini": 0.4570,
            "market_gini": 0.5150,
            "net_top_1_share": 0.1350,
            "decile_shares": [0.01 * i for i in range(1, 11)],
            "context": {"modelled_labor_share": 0.7507},
        },
        "scenarios": [_scenario_row()],
        "sensitivities": {"realization": [_scenario_row("Rapid / realization 50%")]},
    }
    result.update(overrides)
    return result


class TestAIScenarioPayload:
    def test_carries_year_and_description(self):
        payload = ai_scenarios_website_payload(_result())
        assert payload["year"] == 2030
        assert payload["metadata"]["year"] == 2030
        assert payload["metadata"]["description"] == AI_SCENARIO_DESCRIPTION

    def test_carries_provenance_so_charts_can_cite_the_build(self):
        metadata = ai_scenarios_website_payload(_result())["metadata"]
        assert metadata["countryModelVersion"] == "1.764.6"
        assert metadata["dataPackage"] == "populace-data"
        assert metadata["datasetName"] == "populace_us_2024"
        assert metadata["certifiedDataBuildId"] == "build-id"

    def test_scope_note_survives_into_the_payload(self):
        metadata = ai_scenarios_website_payload(_result())["metadata"]
        assert metadata["corporateTaxScopeNote"] == "no corporate tax"

    def test_scenario_fields_are_camel_cased(self):
        scenario = ai_scenarios_website_payload(_result())["scenarios"][0]
        assert scenario["revenueChange"] == pytest.approx(205.7)
        assert scenario["payrollChange"] == pytest.approx(-16.1)
        assert scenario["capitalGrowth"] == pytest.approx(0.1728)
        assert scenario["label"] == "Rapid / proportional"

    def test_poverty_and_gini_changes_are_computed_against_baseline(self):
        scenario = ai_scenarios_website_payload(_result())["scenarios"][0]
        assert scenario["povertyRateChange"] == pytest.approx(0.1258 - 0.1250)
        assert scenario["netGiniChange"] == pytest.approx(0.4644 - 0.4570)

    def test_baseline_block_carries_levels_and_context(self):
        baseline = ai_scenarios_website_payload(_result())["baseline"]
        assert baseline["povertyRate"] == pytest.approx(0.1250)
        assert baseline["context"]["modelled_labor_share"] == pytest.approx(0.7507)

    def test_sensitivities_are_serialized_with_the_same_shape(self):
        payload = ai_scenarios_website_payload(_result())
        realization = payload["sensitivities"]["realization"]
        assert len(realization) == 1
        assert realization[0]["label"] == "Rapid / realization 50%"
        assert "povertyRateChange" in realization[0]

    def test_missing_sensitivities_key_is_tolerated(self):
        payload = ai_scenarios_website_payload(_result(sensitivities=None))
        assert payload["sensitivities"] == {}

    def test_none_valued_fields_are_dropped(self):
        """A null crossover is the proportional case, not missing data."""
        scenario = ai_scenarios_website_payload(_result())["scenarios"][0]
        assert "laborCrossoverIncome" not in scenario

    def test_crossover_is_carried_when_present(self):
        row = _scenario_row()
        row["diagnostics"]["labor_crossover_income"] = 61_500.0
        payload = ai_scenarios_website_payload(_result(scenarios=[row]))
        assert payload["scenarios"][0]["laborCrossoverIncome"] == pytest.approx(
            61_500.0
        )

    def test_empty_scenario_list_produces_an_empty_payload_not_an_error(self):
        payload = ai_scenarios_website_payload(_result(scenarios=[]))
        assert payload["scenarios"] == []
        assert payload["baseline"]["povertyRate"] == pytest.approx(0.1250)
