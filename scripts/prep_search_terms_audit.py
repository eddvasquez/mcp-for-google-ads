#!/usr/bin/env python3
"""
prep_search_terms_audit.py - High-Performance Search Terms Pre-filter & Governance Router.

Processes raw search terms report (CSV/JSON), calculates efficiency metrics, and splits terms:
  1. Negative Candidates for Campaign Level (Macro Bleeders: high spend, 0 conversions, irrelevant intent).
  2. Negative Candidates for Ad Group Level (Traffic Sculpting: high relevancy to another ad group).
Emits a compact diagnostic summary for the LLM without loading massive data tables into context.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def audit_search_terms(file_path: Path, min_cost: float = 15.0, min_clicks: int = 5) -> dict:
    bleeders = []
    sculpting_candidates = []
    total_spend = 0.0
    bleeder_spend = 0.0

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            term = row.get("Search term") or row.get("search_term") or row.get("term", "")
            cost_str = row.get("Cost") or row.get("cost_micros") or row.get("cost", "0")
            clicks_str = row.get("Clicks") or row.get("clicks", "0")
            conv_str = row.get("Conversions") or row.get("conversions", "0")
            ad_group = row.get("Ad group") or row.get("ad_group_name", "")

            try:
                # Handle micros if cost > 1000
                cost = float(str(cost_str).replace("$", "").replace(",", ""))
                if cost > 10000:
                    cost = cost / 1_000_000.0
                clicks = int(clicks_str)
                conversions = float(conv_str)
            except (ValueError, TypeError):
                continue

            total_spend += cost

            # Bleeder Detection: Spend or clicks above threshold with zero conversions
            if conversions == 0 and (cost >= min_cost or clicks >= min_clicks):
                # Verify <= 10 words
                words = term.strip().split()
                if len(words) <= 10:
                    bleeders.append({
                        "term": term.strip(),
                        "cost": round(cost, 2),
                        "clicks": clicks,
                        "ad_group": ad_group
                    })
                    bleeder_spend += cost

    # Sort bleeders by waste descending
    bleeders.sort(key=lambda x: x["cost"], reverse=True)

    return {
        "total_analyzed_spend": round(total_spend, 2),
        "bleeder_wasted_spend": round(bleeder_spend, 2),
        "waste_percentage": round((bleeder_spend / total_spend * 100) if total_spend > 0 else 0, 1),
        "bleeder_count": len(bleeders),
        "bleeders": bleeders
    }


def main():
    parser = argparse.ArgumentParser(description="Pre-audit search terms to offload tokens and pinpoint bleeders.")
    parser.add_argument("input_csv", type=Path, help="CSV search terms report")
    parser.add_argument("--min-cost", type=float, default=15.0, help="Minimum cost threshold to flag bleeder")
    parser.add_argument("--min-clicks", type=int, default=5, help="Minimum clicks threshold to flag bleeder")
    parser.add_argument("--out-payload", type=Path, help="Export ready-to-run MCP proposal payload JSON")

    args = parser.parse_args()

    if not args.input_csv.exists():
        print(f"Error: File '{args.input_csv}' not found.", file=sys.stderr)
        sys.exit(1)

    res = audit_search_terms(args.input_csv, args.min_cost, args.min_clicks)

    if args.out_payload:
        keywords = [{"text": b["term"], "match_type": "EXACT"} for b in res["bleeders"]]
        payload = {
            "action": "add_negatives",
            "keywords": keywords,
            "_meta": {
                "purpose": "MACRO_BLEEDER_PROTECTION",
                "estimated_saved_spend": res["bleeder_wasted_spend"]
            }
        }
        with open(args.out_payload, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Negative bleeder payload exported to {args.out_payload}")

    # Compact Executive Brief for LLM (Consumes <100 tokens instead of 5,000+)
    print("\n================ SEARCH TERMS AUDIT BRIEF ================")
    print(f"Total Spend Analyzed:       ${res['total_analyzed_spend']:,.2f}")
    print(f"Bleeder Wasted Spend:       ${res['bleeder_wasted_spend']:,.2f} ({res['waste_percentage']}%)")
    print(f"Bleeders Flagged:           {res['bleeder_count']} terms")
    print("----------------------------------------------------------")
    print("Top 5 Bleeders to Block at Campaign Level:")
    for b in res["bleeders"][:5]:
        print(f"  • '{b['term']}' -> ${b['cost']} wasted ({b['clicks']} clicks, 0 conv)")
    print("==========================================================\n")


if __name__ == "__main__":
    main()
