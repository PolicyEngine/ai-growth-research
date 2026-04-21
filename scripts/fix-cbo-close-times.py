"""Fix CBO market close times: year+3 -> year+4 to account for growing publication lag."""

import datetime
import subprocess
import requests

def get_api_key():
    result = subprocess.run(
        ["/Users/maxghenis/.claude/manage-secret.sh", "get", "MANIFOLD_API_KEY"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

API_KEY = get_api_key()

markets = [
    ("what-will-the-us-top-1-posttaxtrans", 2023),
    ("what-will-the-us-top-1-posttaxtrans-NCQuChy06E", 2024),
    ("what-will-the-us-top-1-posttaxtrans-ysldt9uplQ", 2025),
    ("what-will-the-us-top-1-posttaxtrans-y2OE028spN", 2026),
    ("what-will-the-us-top-1-posttaxtrans-q80ucQCUAz", 2027),
]

for slug, year in markets:
    r = requests.get(f"https://api.manifold.markets/v0/slug/{slug}")
    data = r.json()
    market_id = data["id"]
    question = data["question"]

    new_close = datetime.datetime(year + 4, 6, 28, 23, 59, 59)
    close_ms = int(new_close.timestamp() * 1000)
    new_resolve_year = year + 4

    # Update close time
    resp = requests.post(
        f"https://api.manifold.markets/v0/market/{market_id}/close",
        headers={"Authorization": f"Key {API_KEY}", "Content-Type": "application/json"},
        json={"closeTime": close_ms},
    )

    # Update description with corrected lag info
    desc = (
        "Resolves to the share of after-tax income (including transfers) received by "
        "the top 1% of households, as published by the Congressional Budget Office in "
        "\"The Distribution of Household Income\" report.\n\n"
        f"**Resolution source:** CBO's Distribution of Household Income report for {year}. "
        "CBO typically publishes with a ~3-4 year lag (e.g., 2022 data published January 2026).\n\n"
        "**Baseline:** In 2022, the top 1% received 14.6% of after-tax income (CBO, January 2026). "
        "The 2019 figure was 13.7%.\n\n"
        f"**Resolution date:** When CBO publishes the relevant report (expected ~{new_resolve_year}).\n\n"
        "Source: https://www.cbo.gov/publication/61911"
    )

    resp2 = requests.post(
        f"https://api.manifold.markets/v0/market/{market_id}/update",
        headers={"Authorization": f"Key {API_KEY}", "Content-Type": "application/json"},
        json={"descriptionMarkdown": desc},
    )

    close_str = new_close.strftime("%b %Y")
    status = "OK" if resp.status_code == 200 else f"ERR {resp.status_code}"
    print(f"[{status}] {question} -> closes {close_str}, resolves ~{new_resolve_year}")
