"""Unit tests for the AI scenario calibration and shock math.

No PolicyEngine dependency: everything here is the arithmetic that sits
between the published forecasts and the microsimulation inputs.
"""

import dataclasses

import numpy as np
import pytest

from analysis.ai_scenarios import (
    BASELINE_LABOR_SHARE,
    CAPITAL_INCOME_VARS,
    CAPITAL_INCOME_VARS_EXCL_RETIREMENT,
    CBO_CUMULATIVE_GROWTH_FACTOR,
    INEQUALITY_VARIANTS,
    LABOR_INCOME_VARS,
    PASSTHROUGH_VAR,
    RETIREMENT_INCOME_VARS,
    AIScenario,
    build_scenario,
    default_scenario_grid,
    rescale_labor_income,
)

# Published Table 1 from Iselin & Nunn, The Budget Lab, 2026-07-20:
# annual GDP growth, 2030 labor share, and the three derived cumulative
# growth rates the report prints.
BUDGET_LAB_TABLE_1 = {
    "Slow": {
        "annual_gdp_growth": 0.020,
        "target_labor_share": 0.550,
        "gdp_growth": 0.0059,
        "capital_growth": 0.0172,
        "labor_growth": -0.0032,
        "lambda_compressive": 0.994,
        "lambda_expansive": 1.006,
    },
    "Moderate": {
        "annual_gdp_growth": 0.026,
        "target_labor_share": 0.538,
        "gdp_growth": 0.0358,
        "capital_growth": 0.0754,
        "labor_growth": 0.0041,
        "lambda_compressive": 0.964,
        "lambda_expansive": 1.036,
    },
    "Rapid": {
        "annual_gdp_growth": 0.033,
        "target_labor_share": 0.513,
        "gdp_growth": 0.0717,
        "capital_growth": 0.1728,
        "labor_growth": -0.0094,
        "lambda_compressive": 0.928,
        "lambda_expansive": 1.072,
    },
}

# The report rounds to two decimal places in percent, so agreement to half a
# basis point is as close as the published table can pin us.
TOLERANCE = 5e-5


class TestCalibration:
    """The two calibration constants we recovered must stay recovered."""

    def test_scenario_inputs_match_published_survey_values(self):
        for name, expected in BUDGET_LAB_TABLE_1.items():
            scenario = build_scenario(name)
            assert scenario.annual_gdp_growth == expected["annual_gdp_growth"]
            assert scenario.target_labor_share == expected["target_labor_share"]

    def test_calibration_reproduces_budget_lab_table_1(self):
        """All nine derived growth rates, from two recovered constants."""
        for name, expected in BUDGET_LAB_TABLE_1.items():
            scenario = build_scenario(name)
            assert scenario.gdp_growth == pytest.approx(
                expected["gdp_growth"], abs=TOLERANCE
            ), f"{name} GDP growth"
            assert scenario.capital_growth == pytest.approx(
                expected["capital_growth"], abs=TOLERANCE
            ), f"{name} capital growth"
            assert scenario.labor_growth == pytest.approx(
                expected["labor_growth"], abs=TOLERANCE
            ), f"{name} labor growth"

    def test_inequality_lambda_reproduces_published_values(self):
        for name, expected in BUDGET_LAB_TABLE_1.items():
            compressive = build_scenario(name, inequality="compressive")
            expansive = build_scenario(name, inequality="expansive")
            assert compressive.inequality_lambda == pytest.approx(
                expected["lambda_compressive"], abs=1e-3
            ), f"{name} compressive lambda"
            assert expansive.inequality_lambda == pytest.approx(
                expected["lambda_expansive"], abs=1e-3
            ), f"{name} expansive lambda"

    def test_recovered_constants_are_the_least_squares_fit(self):
        """Guard against someone nudging the constants to fix one scenario.

        Re-derives the pre-shock labor share from the published capital and
        labor growth rates and checks the module constant is the best fit.
        """

        def sse(theta_l0):
            theta_k0 = 1 - theta_l0
            total = 0.0
            for expected in BUDGET_LAB_TABLE_1.values():
                gy = (
                    1 + expected["annual_gdp_growth"]
                ) ** 5 / CBO_CUMULATIVE_GROWTH_FACTOR - 1
                theta_l1 = expected["target_labor_share"]
                gk = ((1 - theta_l1) * (1 + gy) - theta_k0) / theta_k0
                gl = (theta_l1 * (1 + gy) - theta_l0) / theta_l0
                total += (gk - expected["capital_growth"]) ** 2
                total += (gl - expected["labor_growth"]) ** 2
            return total

        grid = np.linspace(0.50, 0.60, 10001)
        best = float(grid[int(np.argmin([sse(t) for t in grid]))])
        assert best == pytest.approx(BASELINE_LABOR_SHARE, abs=1e-4)

    def test_labor_and_capital_shares_sum_to_one(self):
        scenario = build_scenario("Rapid")
        assert scenario.baseline_labor_share + scenario.baseline_capital_share == 1
        assert scenario.target_labor_share + scenario.target_capital_share == 1

    def test_rapid_scenario_shrinks_labor_income(self):
        """The report's headline mechanism: labor income falls under Rapid."""
        assert build_scenario("Rapid").labor_growth < 0
        assert build_scenario("Slow").labor_growth < 0
        assert build_scenario("Moderate").labor_growth > 0

    def test_capital_growth_exceeds_gdp_growth_in_every_scenario(self):
        for name in BUDGET_LAB_TABLE_1:
            scenario = build_scenario(name)
            assert scenario.capital_growth > scenario.gdp_growth


class TestScenarioVariants:
    def test_hold_shares_fixed_grows_both_factors_at_gdp_rate(self):
        scenario = build_scenario("Rapid", hold_shares_fixed=True)
        assert scenario.labor_growth == pytest.approx(scenario.gdp_growth)
        assert scenario.capital_growth == pytest.approx(scenario.gdp_growth)

    def test_hold_shares_fixed_raises_labor_growth(self):
        """The counterfactual exists to show what the tilt costs labor."""
        tilted = build_scenario("Rapid")
        fixed = build_scenario("Rapid", hold_shares_fixed=True)
        assert fixed.labor_growth > tilted.labor_growth
        assert fixed.capital_growth < tilted.capital_growth

    def test_realization_rate_scales_capital_growth_only(self):
        full = build_scenario("Rapid", realization_rate=1.0)
        half = build_scenario("Rapid", realization_rate=0.5)
        assert half.capital_growth == pytest.approx(full.capital_growth)
        assert half.effective_capital_growth == pytest.approx(
            full.effective_capital_growth / 2
        )
        assert half.labor_growth == pytest.approx(full.labor_growth)

    def test_zero_realization_removes_the_capital_shock(self):
        scenario = build_scenario("Rapid", realization_rate=0.0)
        assert scenario.effective_capital_growth == 0.0

    def test_proportional_and_none_have_unit_lambda(self):
        assert build_scenario("Rapid", inequality="proportional").inequality_lambda == 1
        assert build_scenario("Rapid", inequality="none").inequality_lambda == 1

    def test_invalid_inequality_variant_raises(self):
        with pytest.raises(ValueError, match="inequality must be one of"):
            build_scenario("Rapid", inequality="sideways")

    def test_out_of_range_realization_rate_raises(self):
        with pytest.raises(ValueError, match="realization_rate"):
            build_scenario("Rapid", realization_rate=-0.5)

    def test_unknown_scenario_name_raises(self):
        with pytest.raises(KeyError, match="Unknown scenario"):
            build_scenario("Instantaneous")

    def test_default_grid_covers_every_scenario_and_variant(self):
        grid = default_scenario_grid()
        assert len(grid) == len(BUDGET_LAB_TABLE_1) * (len(INEQUALITY_VARIANTS) + 1)
        for name in BUDGET_LAB_TABLE_1:
            variants = {s.inequality for s in grid if s.name == name}
            assert variants == set(INEQUALITY_VARIANTS) | {"none"}
            assert sum(1 for s in grid if s.name == name and s.hold_shares_fixed) == 1

    def test_labels_are_unique_within_the_grid(self):
        labels = [s.label for s in default_scenario_grid()]
        assert len(labels) == len(set(labels))

    def test_to_dict_round_trips_derived_values(self):
        scenario = build_scenario("Moderate", inequality="expansive")
        payload = scenario.to_dict()
        assert payload["gdp_growth"] == pytest.approx(scenario.gdp_growth)
        assert payload["inequality_lambda"] == pytest.approx(scenario.inequality_lambda)
        assert payload["label"] == scenario.label


class TestLaborRescaling:
    """The log-spread transform that carries the inequality channel."""

    incomes = np.array([15_000.0, 42_000.0, 68_000.0, 150_000.0, 900_000.0])
    weights = np.array([3.0, 5.0, 4.0, 2.0, 1.0])

    def _aggregate(self, values):
        return float((values * self.weights).sum())

    def test_proportional_hits_target_aggregate(self):
        out = rescale_labor_income(self.incomes, self.weights, 0.05, 1.0)
        assert self._aggregate(out) == pytest.approx(
            self._aggregate(self.incomes) * 1.05
        )

    def test_proportional_scales_every_record_equally(self):
        out = rescale_labor_income(self.incomes, self.weights, 0.05, 1.0)
        np.testing.assert_allclose(out / self.incomes, 1.05)

    @pytest.mark.parametrize("lam", [0.90, 0.97, 1.03, 1.10])
    def test_spread_transform_hits_target_aggregate(self, lam):
        """mu1 must be pinned so the aggregate lands on target for any lambda."""
        out = rescale_labor_income(self.incomes, self.weights, -0.01, lam)
        assert self._aggregate(out) == pytest.approx(
            self._aggregate(self.incomes) * 0.99
        )

    def test_expansive_lambda_widens_the_log_distribution(self):
        out = rescale_labor_income(self.incomes, self.weights, 0.0, 1.10)
        before = np.std(np.log(self.incomes))
        after = np.std(np.log(out))
        assert after > before
        assert after == pytest.approx(before * 1.10)

    def test_compressive_lambda_narrows_the_log_distribution(self):
        out = rescale_labor_income(self.incomes, self.weights, 0.0, 0.90)
        before = np.std(np.log(self.incomes))
        after = np.std(np.log(out))
        assert after < before
        assert after == pytest.approx(before * 0.90)

    def test_expansive_lambda_raises_the_top_share(self):
        out = rescale_labor_income(self.incomes, self.weights, 0.0, 1.10)
        top_before = self.incomes[-1] * self.weights[-1] / self._aggregate(self.incomes)
        top_after = out[-1] * self.weights[-1] / self._aggregate(out)
        assert top_after > top_before

    def test_ordering_is_preserved(self):
        for lam in (0.90, 1.0, 1.10):
            out = rescale_labor_income(self.incomes, self.weights, 0.03, lam)
            assert np.all(np.diff(out) > 0)

    def test_nonpositive_values_pass_through_unchanged(self):
        values = np.array([-5_000.0, 0.0, 50_000.0])
        weights = np.array([1.0, 1.0, 1.0])
        out = rescale_labor_income(values, weights, 0.10, 1.05)
        assert out[0] == -5_000.0
        assert out[1] == 0.0
        assert out[2] != 50_000.0

    def test_target_aggregate_ignores_nonpositive_records(self):
        values = np.array([-5_000.0, 0.0, 50_000.0])
        weights = np.array([1.0, 1.0, 1.0])
        out = rescale_labor_income(values, weights, 0.10, 1.0)
        assert out[2] == pytest.approx(55_000.0)

    def test_all_nonpositive_input_is_a_no_op(self):
        values = np.array([-1_000.0, 0.0])
        weights = np.array([1.0, 1.0])
        out = rescale_labor_income(values, weights, 0.10, 1.05)
        np.testing.assert_array_equal(out, values)

    def test_input_array_is_not_mutated(self):
        original = self.incomes.copy()
        rescale_labor_income(self.incomes, self.weights, 0.05, 1.05)
        np.testing.assert_array_equal(self.incomes, original)

    def test_weights_affect_the_scale_factor(self):
        """Reweighting the top earner changes where the aggregate lands."""
        heavy = np.array([3.0, 5.0, 4.0, 2.0, 50.0])
        out_light = rescale_labor_income(self.incomes, self.weights, 0.0, 1.10)
        out_heavy = rescale_labor_income(self.incomes, heavy, 0.0, 1.10)
        assert not np.allclose(out_light, out_heavy)


class TestIncomeVariableSets:
    def test_labor_and_capital_sets_do_not_overlap(self):
        assert not set(LABOR_INCOME_VARS) & set(CAPITAL_INCOME_VARS)

    def test_passthrough_is_in_the_capital_set(self):
        """Its labor portion is handled inside the capital loop, not the labor one."""
        assert PASSTHROUGH_VAR in CAPITAL_INCOME_VARS
        assert PASSTHROUGH_VAR not in LABOR_INCOME_VARS

    def test_retirement_exclusion_removes_exactly_the_retirement_vars(self):
        assert set(CAPITAL_INCOME_VARS) - set(
            CAPITAL_INCOME_VARS_EXCL_RETIREMENT
        ) == set(RETIREMENT_INCOME_VARS)

    def test_capital_set_has_no_duplicates(self):
        assert len(CAPITAL_INCOME_VARS) == len(set(CAPITAL_INCOME_VARS))


class TestScenarioConstruction:
    def test_scenario_is_hashable_and_frozen(self):
        scenario = build_scenario("Rapid")
        assert hash(scenario) is not None
        with pytest.raises(dataclasses.FrozenInstanceError):
            scenario.name = "Other"

    def test_custom_baseline_share_changes_derived_growth(self):
        default = build_scenario("Rapid")
        alternative = AIScenario(
            name="Rapid",
            annual_gdp_growth=0.033,
            target_labor_share=0.513,
            baseline_labor_share=0.60,
        )
        assert alternative.capital_growth != pytest.approx(default.capital_growth)
