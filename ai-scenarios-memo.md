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
real GDP growth either way — poverty falls 1.09 points if the gains split at
today's factor shares, and rises 0.11 points if they tilt to capital as
forecasters expect.

**2. The assumption with the least evidence behind it decides the household
outcome.** The Budget Lab is explicit that nobody knows whether AI compresses or
widens the wage distribution, so they span the range. Across that span in Rapid,
revenue moves 36% while poverty moves **3.26 points**, from 10.59% to 13.85%.

**3. Two definitional choices about the tax base matter more than the choice
between Slow, Moderate and Rapid.** How much AI capital income is realized, and
whether taxable retirement distributions count as capital, together range the
Rapid revenue estimate from −$61B to +$211B.

## Scenario results

Change against the same-year current-law baseline, 2030, $B. Baseline SPM
poverty 12.13%, net Gini 0.4625.

| Scenario | Revenue | Income tax | Payroll | State | Poverty | Δ pp | Net Gini |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Slow / shares fixed | +47 | +29 | +10 | +6 | 11.99% | −0.14 | 0.4627 |
| Slow / compressive | +3 | +3 | −1 | +1 | 12.01% | −0.12 | 0.4622 |
| Slow / proportional | +6 | +11 | −5 | +2 | 12.17% | +0.04 | 0.4632 |
| Slow / expansive | +10 | +19 | −10 | +3 | 12.33% | +0.20 | 0.4643 |
| Moderate / shares fixed | +289 | +178 | +61 | +35 | 11.46% | −0.67 | 0.4640 |
| Moderate / compressive | +128 | +65 | +33 | +15 | 11.18% | −0.95 | 0.4596 |
| Moderate / proportional | +144 | +114 | +7 | +21 | 12.00% | −0.13 | 0.4656 |
| Moderate / expansive | +163 | +164 | −20 | +28 | 12.84% | +0.71 | 0.4718 |
| Rapid / shares fixed | +581 | +358 | +121 | +71 | 11.04% | −1.09 | 0.4654 |
| Rapid / compressive | +179 | +98 | +34 | +24 | 10.59% | −1.54 | 0.4581 |
| Rapid / proportional | +211 | +193 | −16 | +36 | 12.24% | +0.11 | 0.4699 |
| Rapid / expansive | +244 | +294 | −70 | +48 | 13.85% | +1.72 | 0.4820 |

"Shares fixed" grows both factors at the scenario's GDP rate — the counterfactual
behind their finding that revenue gains would be roughly twice as large with
factor shares held at 2026 levels.

Both of their mechanisms reproduce. Within each scenario, moving compressive to
expansive raises income tax revenue through progressivity and lowers payroll
revenue as earnings cross the Social Security cap ($214,200 in 2030; at
baseline, 15.8% of wage income and 5.7% of workers sit above it).

The cap effect runs in both directions, which is worth stating because it is
easy to get backwards: under Rapid / compressive, aggregate labor income *falls*
0.94% and payroll receipts still *rise* $34B, because compression moves earnings
from above the cap to below it.

## What the tilt toward capital costs

| Scenario | Shares fixed | As forecast | Share kept |
| --- | --- | --- | --- |
| Slow | +$47B | +$6B | 14% |
| Moderate | +$289B | +$144B | 50% |
| Rapid | +$581B | +$211B | 36% |

Their "roughly twice as large" claim is specifically about Rapid. We get 2.7× —
the same finding, somewhat stronger, in the direction a missing corporate tax
line predicts.

Their most extreme case checks out too: for Slow with compressive labor
inequality they report the gain 82% lower than with shares and distribution
unchanged; we get 93% lower.

An independent cross-check: they report an average tax rate of 21%–34% on gross
factor income in Rapid. Our Rapid / proportional turns a $760B market income
increase into $211B of receipts — **27.8%**, inside their band, from a different
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
| 25% | +$7B |
| 50% | +$74B |
| 75% | +$142B |
| 100% (their assumption) | +$211B |

Linear to within a percent, with **breakeven at 22.5%**. Below that, Rapid AI
growth is a net fiscal cost under current law: labor income still falls, and
there is not enough taxable capital income to offset it.

Poverty is flat across the entire sweep, 12.24% to 12.27%. Whether AI's capital
gains are taxable moves the federal balance sheet by more than a
quarter-trillion dollars and moves poor households essentially not at all.

**What counts as capital.** Taxable pension and IRA distributions are taxed at
ordinary rates. Counting them as capital — which the Budget Lab does, and we
followed — raises the revenue estimate and softens the "capital is taxed
lightly" conclusion:

| Scenario | Full capital set | Excl. retirement | Difference |
| --- | --- | --- | --- |
| Slow | +$6B | −$4B | −$10B, sign flips |
| Moderate | +$144B | +$98B | −$46B |
| Rapid | +$211B | +$106B | −$106B |

Excluding them halves the Rapid estimate and flips Slow negative.

## Who gains, in wage terms

The inequality parameter is a spread transform on log wages, so each variant has
a crossover wage: below it workers lose, above it they gain.

| Rapid variant | λ | Crossover |
| --- | --- | --- |
| Compressive | 0.928 | $118,287 — workers below this gain |
| Expansive | 1.072 | $168,205 — workers below this lose |

Under Rapid / expansive, that puts the great majority of workers on the losing
side of a scenario that raises federal receipts $244B.

## States

State revenue under Rapid / proportional concentrates almost entirely in a
handful of states — California +$10.0B, New York +$5.8B, New Jersey +$1.6B,
Massachusetts +$1.3B, Maryland +$1.2B.

Seven states collect **exactly nothing** from the capital shock: Florida,
Nevada, New Hampshire, South Dakota, Tennessee, Texas and Wyoming. Alaska
rounds to zero.

Washington is the instructive exception. It has no income tax either, but its
capital gains excise tax collects **+$1.1B** — more than all seven
zero-collecting states combined, many times over. A state that taxes capital
gains participates in an AI capital boom; a state that taxes only wages does
not participate in an economy where wages are the shrinking share.

Whatever AI does to the federal fiscal picture, it does almost nothing for most
of the states that would bear the cost of absorbing displaced workers — unless
they have a capital tax to collect it with.

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

**Levels versus changes.** PolicyEngine's absolute SPM poverty level sits above
the Census published rate — a known calibration gap, and one that moves whenever
BLS revises thresholds (as it did for 2019–2024 in July 2026). Every poverty
figure here is therefore reported as a change against a same-year baseline
computed on the identical threshold. Because the threshold is identical in
baseline and scenario, those changes are close to unaffected by the level gap;
the levels are context, the deltas are the result.

**Stability across data builds.** These results were first computed on the
prior populace build (build o, 22 July) and rerun on build p (28 July, with
revised capital gains calibration) under the identical model version — a
data-only change. Every revenue figure moved by less than 3%, every poverty
change by less than 0.11pp, and no conclusion changed. The recalibration's
visible effect is distributional: the baseline top-1% net income share rises
from 8.77% to 9.00%, and New York's state take under Rapid rises from $3.8B to
$5.8B as more of the gains land where they are taxed.

**Diagnostics.** The net-income identity closes to $0.000B in every scenario,
and the labor shock hits its target aggregate to within 2e-16.

## Reproducibility

Everything above runs from open source against openly published microdata:
policyengine-us 1.764.6, policyengine.py 5.0.1, populace-us `populace_us_2024`
(certified build `populace-us-2024-buildp-sparse-rmloss100-cae8640`). The
Budget Lab notes their PUF-based data cannot be released publicly, so this is a
complement rather than a competitor: anyone can rerun these scenarios, or score
a different reform against them.

Code: `PolicyEngine/ai-inequality`, `analysis/ai_scenarios.py`.
Method notes: `analysis/AI_SCENARIOS.md`.
