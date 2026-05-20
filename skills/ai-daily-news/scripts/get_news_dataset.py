#!/usr/bin/env python3
"""
get_news_dataset.py — Fetch AI news dataset for a specific date

IMPORTANT: Use get_latest_news for "today/current/latest" AI news queries.
This tool is ONLY for explicit date queries (YYYY-MM-DD).

Usage:
    python get_news_dataset.py --date YYYY-MM-DD [--tier guest|pro_core|pro_plus]
"""

import os
import sys
import json
import argparse

# Ensure lib directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import validate_date, NetworkError
from lib.remote_client import download_dataset, download_pro_dataset
from lib.compression import decompress
from lib.data_store import get_cached, save_cached, record_delivery
from lib.tool_output import format_dataset, format_error


def main():
    parser = argparse.ArgumentParser(
        description="Fetch AI news dataset for a specific explicit date. "
        "Use get_latest_news for today/current/latest AI news."
    )
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format (required)")
    parser.add_argument("--tier", default="guest", help="Data tier (default: guest)")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    args = parser.parse_args()

    date = args.date
    tier = args.tier
    base_url = args.base_url

    # Validate date
    err = validate_date(date)
    if err:
        print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        sys.exit(1)

    # Validate tier
    if tier not in ("guest", "pro_core", "pro_plus"):
        print(json.dumps({"status": "error", "message": f"Invalid tier: {tier}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        # Try cache first
        text = get_cached(date, tier)
        if not text:
            # Download
            if tier == "guest":
                raw = download_dataset(date, tier, base_url=base_url)
            else:
                api_key = os.getenv("AINEWS_ACCESS_TOKEN")
                raw = download_pro_dataset(date, tier, base_url=base_url, api_key=api_key)
            text = decompress(raw)
            save_cached(date, tier, text)

        data = json.loads(text)
        record_count = len(data.get("data", []))
        record_delivery(date, tier, record_count)

        # Format output
        output = format_dataset(data, date, tier)
        print(output)

    except NetworkError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
