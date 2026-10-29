#!/usr/bin/env python3
"""
prep_keywords_batch.py - High-Performance Batch Keyword Preprocessor & Zero-Token Offloader.

Takes raw keyword text or CSV, normalizes strings, enforces the Google Ads hard constraint
(max 10 words per term), strips invalid characters, validates match types, and outputs either:
  1. A minimal JSON payload ready for MCP editing_prepare_keywords.
  2. A summary audit to stdout (saving thousands of LLM context tokens).
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def clean_keyword_text(text: str) -> tuple[str, str]:
    """Clean keyword string and detect match type if wrapped in [] or ""."""
    raw = text.strip()
    match_type = "BROAD"
    if raw.startswith("[") and raw.endswith("]"):
        match_type = "EXACT"
        raw = raw[1:-1].strip()
    elif raw.startswith('"') and raw.endswith('"'):
        match_type = "PHRASE"
        raw = raw[1:-1].strip()

    # Remove invalid Google Ads characters (@ % , * + etc unless part of domain)
    cleaned = re.sub(r'[\@\%\*\+\=\<\>\?\|\^]+', ' ', raw)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned, match_type


def process_keywords(file_path: Path, target_match: str | None = None) -> dict:
    valid_keywords = []
    rejected = []
    seen = set()

    lines = []
    if file_path.suffix.lower() == ".csv":
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    lines.append(row[0])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        cleaned, detected_match = clean_keyword_text(line)
        if not cleaned:
            continue

        match_type = target_match.upper() if target_match else detected_match

        # Hard Rule: Max 10 words
        words = cleaned.split()
        if len(words) > 10:
            rejected.append({
                "raw": line,
                "reason": f"Exceeds 10 words limit ({len(words)} words found)"
            })
            continue

        key = (cleaned.lower(), match_type)
        if key in seen:
            continue
        seen.add(key)

        valid_keywords.append({
            "text": cleaned,
            "match_type": match_type
        })

    return {
        "total_read": len(lines),
        "total_valid": len(valid_keywords),
        "total_rejected": len(rejected),
        "rejected": rejected,
        "keywords": valid_keywords
    }


def main():
    parser = argparse.ArgumentParser(description="Preprocess and validate keywords for MCP Google Ads.")
    parser.add_argument("input_file", type=Path, help="Path to input TXT or CSV file")
    parser.add_argument("--action", choices=["add", "add_negatives"], default="add")
    parser.add_argument("--match-type", choices=["EXACT", "PHRASE", "BROAD"], help="Force match type")
    parser.add_argument("--campaign-id", help="Target Campaign ID (Macro Bleeder Protection)")
    parser.add_argument("--ad-group-id", help="Target Ad Group ID (Traffic Sculpting)")
    parser.add_argument("--out", type=Path, help="Save MCP payload JSON to this path")

    args = parser.parse_args()

    if not args.input_file.exists():
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    result = process_keywords(args.input_file, args.match_type)

    payload = {
        "action": args.action,
        "campaign_id": args.campaign_id,
        "ad_group_id": args.ad_group_id,
        "keywords": result["keywords"]
    }

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Payload saved to {args.out}")

    # Compact output for the LLM / Terminal (Zero Token Waste)
    print("\n--- BATCH KEYWORD SUMMARY ---")
    print(f"Total entries processed: {result['total_read']}")
    print(f"Valid keywords prepared: {result['total_valid']}")
    print(f"Rejected (>10 terms):    {result['total_rejected']}")
    if result["total_rejected"] > 0:
        print("\nSample rejected items:")
        for r in result["rejected"][:3]:
            print(f"  - '{r['raw']}' -> {r['reason']}")
    print("------------------------------")


if __name__ == "__main__":
    main()
