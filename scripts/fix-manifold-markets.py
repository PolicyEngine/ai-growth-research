"""
Fix all 19 Manifold Markets: remove self-promotional text, fix broken links,
fix wrong FRED series.

Changes:
1. ALL markets: Remove "Why this matters" paragraph (self-promotional PE link)
2. Wage ratio markets: Fix broken EPI source URL
3. Labor share markets: Fix FRED series (PRS85006173 index → MPU4910141 percentage)
"""

import json
import subprocess
import time
import datetime

import requests


def get_api_key():
    result = subprocess.run(
        ["/Users/maxghenis/.claude/manage-secret.sh", "get", "MANIFOLD_API_KEY"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


API_KEY = get_api_key()

# All 19 market URLs from the JSON file
with open("/Users/maxghenis/repos/ai-inequality/scripts/manifold-market-urls.json") as f:
    MARKET_URLS = json.load(f)


def slug_from_url(url):
    """Extract slug from Manifold URL."""
    return url.split("/")[-1]


def get_market(slug):
    """Fetch market data from Manifold API."""
    resp = requests.get(f"https://api.manifold.markets/v0/slug/{slug}")
    if resp.status_code == 200:
        return resp.json()
    print(f"  ERROR fetching {slug}: {resp.status_code}")
    return None


def update_market(market_id, description_md):
    """Update a market's description via the Manifold API."""
    headers = {
        "Authorization": f"Key {API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        f"https://api.manifold.markets/v0/market/{market_id}/update",
        headers=headers,
        json={"descriptionMarkdown": description_md},
    )
    return resp.status_code == 200 or (resp.status_code == 200 and resp.json().get("success"))


def get_close_time(slug, year):
    """Get the close time based on when data is actually published."""
    def close_time_ms(y, m, d=28):
        dt = datetime.datetime(y, m, d, 23, 59, 59)
        return int(dt.timestamp() * 1000)

    if "top-1-posttaxtrans" in slug:
        return close_time_ms(year + 3, 6)
    elif "supplemental-pover" in slug or "child-poverty" in slug:
        return close_time_ms(year + 1, 12)
    elif "nonfarm-business" in slug:
        return close_time_ms(year + 1, 6)
    elif "9010-hourly-wage" in slug:
        return close_time_ms(year + 1, 6)
    elif "robot-or-a" in slug:
        return close_time_ms(year, 12, 31)
    return close_time_ms(year + 1, 12)


def build_fixed_description(slug, question):
    """Build the corrected description for each market type."""

    # Determine year from question
    year = None
    for y in range(2023, 2031):
        if str(y) in question:
            year = y
            break

    if "top-1-posttaxtrans" in slug:
        resolve_year = year + 3 if year else 2028
        return (
            "Resolves to the share of after-tax income (including transfers) received by "
            "the top 1% of households, as published by the Congressional Budget Office in "
            "\"The Distribution of Household Income\" report.\n\n"
            f"**Resolution source:** CBO's Distribution of Household Income report for {year}. "
            "CBO typically publishes with a ~3-year lag (e.g., 2022 data published January 2026).\n\n"
            "**Baseline:** In 2022, the top 1% received 14.6% of after-tax income (CBO, January 2026). "
            "The 2019 figure was 13.7%.\n\n"
            f"**Resolution date:** When CBO publishes the relevant report (expected ~{resolve_year}).\n\n"
            "Source: https://www.cbo.gov/publication/61911"
        )

    elif "supplemental-pover" in slug:
        resolve_year = year + 1 if year else 2028
        return (
            "Resolves to the overall SPM poverty rate for the United States, as published by "
            "the U.S. Census Bureau in \"Poverty in the United States\" (P60 report).\n\n"
            f"**Resolution source:** Census Bureau P60 report for {year}. "
            "Census publishes ~9 months after the reference year (e.g., 2024 data published September 2025).\n\n"
            "**Baseline:** In 2024, the SPM poverty rate was 12.9% (Census Bureau, September 2025). "
            "In 2023 it was also 12.9%.\n\n"
            f"**Resolution date:** ~September {resolve_year} (expected Census publication).\n\n"
            "Source: https://www.census.gov/library/publications/2025/demo/p60-287.html"
        )

    elif "child-poverty" in slug:
        resolve_year = year + 1 if year else 2028
        return (
            "Resolves to the SPM poverty rate for children under 18, as published by "
            "the U.S. Census Bureau in \"Poverty in the United States\" (P60 report).\n\n"
            f"**Resolution source:** Census Bureau P60 report for {year}. "
            "Census publishes ~9 months after the reference year.\n\n"
            "**Baseline:** In 2024, the SPM child poverty rate was 13.4% (Census Bureau, September 2025). "
            "In 2021 it fell to 5.2% due to the expanded CTC, then rose to 12.4% in 2022 when it expired.\n\n"
            f"**Resolution date:** ~September {resolve_year} (expected Census publication).\n\n"
            "Source: https://www.census.gov/library/publications/2025/demo/p60-287.html"
        )

    elif "nonfarm-business" in slug:
        resolve_year = year + 1 if year else 2028
        return (
            "Resolves to the annual labor share of income in the nonfarm business sector, "
            "as published by the Bureau of Labor Statistics (Productivity and Costs release).\n\n"
            f"**Resolution source:** BLS Productivity and Costs, FRED series MPU4910141. "
            "BLS publishes annual data ~3 months after the reference year.\n\n"
            "**Baseline:** In 2024, the labor share was 58.3% (BLS). "
            "The long-run average (1947-2024) is ~62%. It has trended downward since ~2000.\n\n"
            f"**Resolution date:** ~March {resolve_year} (expected BLS publication).\n\n"
            "Source: https://fred.stlouisfed.org/series/MPU4910141"
        )

    elif "9010-hourly-wage" in slug:
        resolve_year = year + 1 if year else 2028
        return (
            "Resolves to the ratio of 90th percentile to 10th percentile hourly wages "
            "in the United States, as published by the Economic Policy Institute (EPI) "
            "using BLS Current Population Survey (CPS) Outgoing Rotation Group data.\n\n"
            "**Resolution source:** EPI State of Working America Data Library, "
            "hourly wage percentile ratios. EPI publishes ~3-4 months after the reference year.\n\n"
            "**Baseline:** In 2024, the 90/10 ratio was approximately 4.4 "
            "(90th percentile ~$62.75/hr, 10th percentile ~$14.26/hr).\n\n"
            f"**Resolution date:** ~Q1 {resolve_year} (expected EPI publication).\n\n"
            "Source: https://data.epi.org/wages/hourly_wage_percentile_ratios/line/year/national/wage_ratio/wage_percentile_ratios"
        )

    elif "robot-or-a" in slug:
        return (
            f"Resolves YES if any country (population >1 million) enacts legislation that "
            "explicitly taxes the use of robots, AI systems, or automation equipment, "
            f"or imposes a dedicated levy on firms that automate jobs, by December 31, {year}.\n\n"
            "**What counts:** A tax specifically targeting automation/AI/robots — not general "
            "capital gains taxes, corporate taxes, or investment tax credit changes. "
            "South Korea's 2017 reduction of automation investment tax credits would NOT count "
            "as it was a credit reduction, not a dedicated tax.\n\n"
            "**What doesn't count:** Proposals, bills that don't pass, or taxes on AI companies "
            "(as opposed to taxes on the act of automating).\n\n"
            "**Baseline:** As of February 2026, no country has enacted a dedicated robot/automation tax. "
            "The EU rejected a robot tax proposal in 2017.\n\n"
            "Source: https://en.wikipedia.org/wiki/Robot_tax"
        )

    return None


def main():
    print(f"Fixing {len(MARKET_URLS)} markets...\n")

    for i, url in enumerate(MARKET_URLS):
        slug = slug_from_url(url)
        market = get_market(slug)
        if not market:
            continue

        market_id = market["id"]
        question = market["question"]
        print(f"[{i+1}/{len(MARKET_URLS)}] {question}")

        new_desc = build_fixed_description(slug, question)
        if new_desc is None:
            print(f"  SKIP: no fix needed")
            continue

        success = update_market(market_id, new_desc)
        if success:
            print(f"  FIXED")
        else:
            print(f"  ERROR updating")

        time.sleep(0.5)

    print("\nDone!")


if __name__ == "__main__":
    main()
