#!/usr/bin/env python3
"""
get_latest_news.py — Fetch the latest available AI news dataset

Usage:
    python get_latest_news.py [--tier guest|pro_core|pro_plus]

When users ask for "today's AI news", "current AI news", or "latest AI news",
use this tool instead of get_news_dataset.py. This tool automatically
finds the most recent available data and includes freshness metadata.

Workflow:
1. Call /v1/data/resolve-latest to get freshness metadata
2. Check if we already have that date cached locally
3. If cached: use local data
4. If not cached: call /v1/data/download?date=xxx
5. Combine metadata + data and display to LLM
"""

import os
import sys
import json
import argparse

# Ensure lib directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import NetworkError
from lib.remote_client import resolve_latest, download_dataset, download_pro_dataset
from lib.data_store import get_cached, save_cached, record_delivery
from lib.compression import decompress
from lib.tool_output import format_latest_dataset, format_error


def main():
    parser = argparse.ArgumentParser(description="Fetch latest available AI news dataset")
    parser.add_argument("--tier", default="guest", help="Data tier (default: guest)")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    args = parser.parse_args()

    tier = args.tier
    base_url = args.base_url

    # Validate tier
    if tier not in ("guest", "pro_core", "pro_plus"):
        print(json.dumps({"status": "error", "message": f"Invalid tier: {tier}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        # Step 1: Resolve latest metadata
        if tier == "guest":
            metadata = resolve_latest(tier, base_url=base_url)
        else:
            api_key = os.getenv("AINEWS_ACCESS_TOKEN")
            metadata = resolve_latest(tier, base_url=base_url, api_key=api_key)

        resolved_date = metadata.get("resolved_date", "")
        if not resolved_date:
            print(format_error("Could not resolve latest date"))
            sys.exit(1)

        # Step 2: Check if we have this date cached locally
        cached_data_json = get_cached(resolved_date, tier)
        if cached_data_json:
            # Use cached data
            data = json.loads(cached_data_json)
        else:
            # Download fresh data
            if tier == "guest":
                raw_bytes = download_dataset(resolved_date, tier, base_url=base_url)
            else:
                api_key = os.getenv("AINEWS_ACCESS_TOKEN")
                raw_bytes = download_pro_dataset(resolved_date, tier, base_url=base_url, api_key=api_key)
            data_json_str = decompress(raw_bytes)
            save_cached(resolved_date, tier, data_json_str)
            data = json.loads(data_json_str)

        # Step 3: Combine metadata + data
        result = metadata.copy()
        result["data"] = data

        # Extract info for output
        freshness_status = result.get("freshness_status", "")
        days_behind = result.get("days_behind", 0)
        notice_for_user = result.get("notice_for_user", "")
        record_count = len(data.get("data", []))

        # Record delivery using the resolved date
        record_delivery(resolved_date, tier, record_count)

        # Format output for LLM
        output = format_latest_dataset(result, tier)
        print(output)

    except NetworkError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
