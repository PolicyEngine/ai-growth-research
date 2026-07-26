# AI, the tax system, and the bottom of the distribution

*Draft — HELD, not sent.*

*PolicyEngine · prepared with the AV Tax Policy Roundtable of 30 July 2026 in mind*

## The point

The Budget Lab's [How potential AI futures would play out in the current tax
system](https://budgetlab.yale.edu/research/how-potential-ai-futures-would-play-out-current-tax-system)
(Iselin and Nunn, 20 July) asks what AI-driven growth does to federal receipts,
and finds the answer is less than you would hope, because growth skewed toward
capital is growth the tax base collects less of.

We ran their scenarios through PolicyEngine-US, deliberately adopting their
calibration so that what differs is model coverage rather than assumptions.
PolicyEngine carries the transfer system, the SPM poverty measure, and the state
codes their tax model does not. Three things follow that a revenue-only score
cannot show.

**1. The same growth path either cuts poverty by a point or raises it,
depending only on where the income lands.** In the Rapid scenario — 3.3% annual
real GDP growth either way — poverty falls 1.14 points if the gains split at
today's factor shares, and rises 0.07 points if they tilt to capital as
forecasters expect.

**2. The assumption with the least evidence behind it decides the household
outcome.** The Budget Lab is explicit that nobody knows whether AI compresses or
widens the wage distribution, so they span the range. Across that span in Rapid,
revenue moves 35% while poverty moves **3.41 points**, from 10.93% to 14.34%.

**3. Two definitional choices about the tax base matter more than the choice
between Slow, Moderate and Rapid.** How much AI capital income is realized, and
whether taxable retirement distributions count as capital, together range the
Rapid revenue estimate from −$61B to +$206B.

## Scenario results

Change against the same-year current-law baseline, 2030, $B. Baseline SPM
poverty 12.50%, net Gini 0.4570.

| Scenario | Revenue | Income tax | Payroll | State | Poverty | Δ pp | Net Gini |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Slow / shares fixed | +47 | +29 | +10 | +6 | 12.37% | −0.14 | 0.4573 |
| Slow / compressive | +3 | +3 | −1 | +1 | 12.38% | −0.13 | 0.4567 |
| Slow / proportional | +6 | +11 | −5 | +2 | 12.55% | +0.04 | 0.4577 |
| Slow / expansive | +9 | +18 | −10 | +3 | 12.65% | +0.15 | 0.4588 |
| Moderate / shares fixed | +288 | +177 | +61 | +36 | 11.86% | −0.65 | 0.4585 |
| Moderate / compressive | +126 | +64 | +33 | +15 | 11.51% | −0.99 | 0.4540 |
| Moderate / proportional | +142 | +112 | +7 | +21 | 12.39% | −0.11 | 0.4602 |
| Moderate / expansive | +161 | +161 | −20 | +28 | 13.25% | +0.75 | 0.4664 |
| Rapid / shares fixed | +578 | +357 | +121 | +71 | 11.36% | −1.14 | 0.4601 |
| Rapid / compressive | +176 | +96 | +34 | +24 | 10.93% | −1.58 | 0.4525 |
| Rapid / proportional | +206 | +189 | −16 | +34 | 12.58% | +0.07 | 0.4644 |
| Rapid / expansive | +238 | +287 | −69 | +48 | 14.34% | +1.83 | 0.4765 |

"Shares fixed" grows both factors at the scenario's GDP rate — the counterfactual
behind their finding that revenue gains would be roughly twice as large with
factor shares held at 2026 levels.

Both of their mechanisms reproduce. Within each scenario, moving compressive to
expansive raises income tax revenue through progressivity and lowers payroll
revenue as earnings cross the Social Security cap ($214,200 in 2030; at
baseline, 15.6% of wage income and 6.0% of workers sit above it).

The cap effect runs in both directions, which is worth stating because it is
easy to get backwards: under Rapid / compressive, aggregate labor income *falls*
0.94% and payroll receipts still *rise* $34B, because compression moves earnings
from above the cap to below it.

## What the tilt toward capital costs

| Scenario | Shares fixed | As forecast | Share kept |
| --- | --- | --- | --- |
| Slow | +$47B | +$6B | 13% |
| Moderate | +$288B | +$142B | 49% |
| Rapid | +$578B | +$206B | 36% |

Their "roughly twice as large" claim is specifically about Rapid. We get 2.8× —
the same finding, somewhat stronger, in the direction a missing corporate tax
line predicts.

Their most extreme case checks out too: for Slow with compressive labor
inequality they report the gain 82% lower than with shares and distribution
unchanged; we get 94% lower.

An independent cross-check: they report an average tax rate of 21%–34% on gross
factor income in Rapid. Our Rapid / proportional turns a $764B market income
increase into $206B of receipts — **26.9%**, inside their band, from a different
model on different microdata.

## The two assumptions that dominate

**Realization.** Their capital shock assumes AI does not change the realized
share of capital income; they flag this as a limitation. Since unrealized gains,
retained earnings and accruals inside retirement accounts never reach the
individual tax base, it is doing real work. Holding Rapid / proportional fixed
and varying only how much of the incremental capital flow lands on a tax return:

| Realized share | Revenue |
| --- | --- |
| 0% | −$61B |
| 25% | +$5B |
| 50% | +$72B |
| 75% | +$139B |
| 100% (their assumption) | +$206B |

Linear to within a percent, with **breakeven at 22.9%**. Below that, Rapid AI
growth is a net fiscal cost under current law: labor income still falls, and
there is not enough taxable capital income to offset it.

Poverty is flat across the entire sweep, 12.58% to 12.61%. Whether AI's capital
gains are taxable moves the federal balance sheet by a quarter-trillion dollars
and moves poor households essentially not at all.

**What counts as capital.** Taxable pension and IRA distributions are taxed at
ordinary rates. Counting them as capital — which the Budget Lab does, and we
followed — raises the revenue estimate and softens the "capital is taxed
lightly" conclusion:

| Scenario | Full capital set | Excl. retirement | Difference |
| --- | --- | --- | --- |
| Slow | +$6B | −$4B | −$10B, sign flips |
| Moderate | +$142B | +$97B | −$45B |
| Rapid | +$206B | +$101B | −$105B |

Excluding them halves the Rapid estimate and flips Slow negative.

## Who gains, in wage terms

The inequality parameter is a spread transform on log wages, so each variant has
a crossover wage: below it workers lose, above it they gain.

| Rapid variant | λ | Crossover |
| --- | --- | --- |
| Compressive | 0.928 | $119,073 — workers below this gain |
| Expansive | 1.072 | $169,086 — workers below this lose |

Under Rapid / expansive, that puts the great majority of workers on the losing
side of a scenario that raises federal receipts $238B.

## States

State income tax revenue under Rapid / proportional concentrates almost
entirely in a handful of states — California +$10.1B, New York +$3.8B, New
Jersey +$1.8B, Massachusetts and Maryland +$1.3B each. The nine states without a
broad income tax (TX, FL, TN, NV, SD, WY, AK, NH, WA on wage income) collect
essentially nothing from the capital shock.

Whatever AI does to the federal fiscal picture, it does almost nothing for the
states that would need it most to absorb displaced workers.

## Scope and method

We adopted their calibration exactly. Two inputs their report does not print —
the cumulative CBO baseline (1.0976, against their stated 9.7%) and the
pre-shock labor share (0.5550) — we recovered by inverting their published
formulas, reproducing all nine of their Table 1 derived values to within
0.005pp.

**We model and they do not:** SPM poverty, the transfer system (SNAP, SSI, TANF,
WIC, Medicaid, CHIP, ACA premium tax credits), and state tax and benefit codes.

**They model and we cannot:** the corporate income tax. Our totals are *not*
comparable to their headline $216B — compare to their individual income tax and
payroll lines. Our figures land in a similar range, but that is offsetting
scope, not agreement.

**Both static:** no labor supply response, no behavioural response, no change in
avoidance or enforcement.

**Known limits of ours.** The incremental capital flow is apportioned in
proportion to households' existing realized capital income; they apportion by
SCF-imputed assets, which reaches households holding wealth but realizing
nothing, so ours concentrates the shock more than theirs. Poverty is anchored,
not relative — SPM thresholds do not respond to the simulated distribution, so a
fully relative line would show larger increases. Gini is household-level and
unequivalized, so changes are meaningful but levels are not comparable to
published series.

**Diagnostics.** The net-income identity closes to $0.000B in every scenario,
and the labor shock hits its target aggregate to within 2e-16.

## Reproducibility

Everything above runs from open source against openly published microdata:
policyengine-us 1.764.6, policyengine 4.22.3, populace-us `populace_us_2024`
(certified build `populace-us-2024-buildo-sparse-rmloss100-22bd902`). The Budget
Lab notes their PUF-based data cannot be released publicly, so this is a
complement rather than a competitor: anyone can rerun these scenarios, or score
a different reform against them.

Code: `PolicyEngine/ai-inequality`, `analysis/ai_scenarios.py`.
Method notes: `analysis/AI_SCENARIOS.md`.
