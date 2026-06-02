#!/usr/bin/env python3
"""
get_news_dataset.py — Fetch AI news dataset for a specific date

IMPORTANT: Use get_latest_news for "today/current/latest" AI news queries.
This tool is for explicit date queries (YYYY-MM-DD), relative dates like
"yesterday", or "the day before yesterday".

With local time semantics:
- Date inputs are interpreted in the user's local timezone
- The tool resolves which canonical dataset corresponds to that local date
- Display emphasizes local time rather than canonical/UTC time

Usage:
    python get_news_dataset.py --date YYYY-MM-DD [--tier guest|pro_core|pro_plus] [--timezone TIMEZONE]
"""

import os
import sys
import json
import argparse

# Ensure lib directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import validate_date, NetworkError, get_client_timezone
from lib.remote_client import resolve_date, download_dataset, download_pro_dataset
from lib.compression import decompress
from lib.data_store import get_cached, save_cached, record_delivery
from lib.tool_output import format_dataset, format_resolved_date_dataset, format_error


def main():
    parser = argparse.ArgumentParser(
        description="Fetch AI news dataset for a specific date (local time semantics). "
        "Use get_latest_news for today/current/latest AI news."
    )
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format (required, interpreted as local date)")
    parser.add_argument("--tier", default="guest", help="Data tier (default: guest)")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    parser.add_argument("--timezone", default=None, help="Client timezone (IANA format, e.g., America/New_York)")
    args = parser.parse_args()

    requested_date = args.date
    tier = args.tier
    base_url = args.base_url

    # Validate date
    err = validate_date(requested_date)
    if err:
        print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        sys.exit(1)

    # Validate tier
    if tier not in ("guest", "pro_core", "pro_plus"):
        print(json.dumps({"status": "error", "message": f"Invalid tier: {tier}"}, ensure_ascii=False))
        sys.exit(1)

    # Get client timezone (from arg, env, or local system)
    client_timezone = args.timezone or get_client_timezone()

    try:
        # Step 1: Resolve local date to canonical date
        if tier == "guest":
            resolve_result = resolve_date(requested_date, client_timezone, tier, base_url=base_url)
        else:
            api_key = os.getenv("AINEWS_ACCESS_TOKEN")
            resolve_result = resolve_date(requested_date, client_timezone, tier, base_url=base_url, api_key=api_key)

        resolved_source_date = resolve_result.get("resolved_source_date", "")
        if not resolved_source_date:
            print(format_error("Could not resolve local date to canonical dataset"))
            sys.exit(1)

        # Step 2: Try cache for the canonical date first
        text = get_cached(resolved_source_date, tier)
        if not text:
            # Download using canonical date
            if tier == "guest":
                raw = download_dataset(resolved_source_date, tier, base_url=base_url)
            else:
                api_key = os.getenv("AINEWS_ACCESS_TOKEN")
                raw = download_pro_dataset(resolved_source_date, tier, base_url=base_url, api_key=api_key)
            text = decompress(raw)
            save_cached(resolved_source_date, tier, text)

        # Parse dataset
        data = json.loads(text)
        record_count = len(data.get("data", []))

        # Record delivery using canonical date
        record_delivery(resolved_source_date, tier, record_count)

        # Format output using resolve result + data
        result = resolve_result.copy()
        result["data"] = data

        output = format_resolved_date_dataset(result, tier)
        
        # Prepend response guidance if provided by L2
        guidance = resolve_result.get("response_guidance", {})
        guidance_text = guidance.get("text")
        if guidance_text:
            output = guidance_text + "\n\n" + output
            
        print(output)

    except NetworkError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == "__main__":
    main()
