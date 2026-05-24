"""
tool_output.py — Tool output formatting

Responsibilities:
- Format dataset structure into LLM-readable Markdown
- Handle _ads display (only show on first delivery)
- Keep thin: rely on _data_dictionary for field explanations, don't hardcode too much
- Preserve full record data so LLM can use source-specific extension fields
"""

import json
from lib.data_store import has_seen_ads, mark_ads_shown


def _render_ads(ads: dict) -> list[str]:
    """Render ads in a backward-compatible way."""
    if not ads or has_seen_ads():
        return []

    lines = ["---"]

    content = ads.get("content")
    if content:
        lines.append(str(content))

    items = ads.get("items", [])
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            item_content = item.get("content")
            if item_content:
                lines.append(str(item_content))
            item_url = item.get("url")
            if item_url:
                lines.append(str(item_url))

    lines.extend(["---", ""])
    mark_ads_shown()
    return lines


def _format_scalar(value) -> str:
    """Format scalar values for markdown output."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _flatten_markdown_fields(value, prefix: str = "") -> list[tuple[str, str]]:
    """
    Flatten nested dict/list data into dotted markdown field paths.

    Examples:
    - {"a": {"b": 1}} -> [("a.b", "1")]
    - {"tags": ["x", "y"]} -> [("tags", "[\"x\", \"y\"]")]
    """
    if isinstance(value, dict):
        rows = []
        for key, nested_value in value.items():
            key_str = str(key)
            next_prefix = f"{prefix}.{key_str}" if prefix else key_str
            rows.extend(_flatten_markdown_fields(nested_value, next_prefix))
        if not rows and prefix:
            rows.append((prefix, "{}"))
        return rows

    if isinstance(value, list):
        if not prefix:
            return [("value", json.dumps(value, ensure_ascii=False))]

        simple_list = all(not isinstance(item, (dict, list)) for item in value)
        if simple_list:
            return [(prefix, json.dumps(value, ensure_ascii=False))]

        rows = []
        for index, item in enumerate(value):
            next_prefix = f"{prefix}[{index}]"
            rows.extend(_flatten_markdown_fields(item, next_prefix))
        if not rows:
            rows.append((prefix, "[]"))
        return rows

    if not prefix:
        return [("value", _format_scalar(value))]
    return [(prefix, _format_scalar(value))]


def _render_full_dataset_markdown(data: dict) -> list[str]:
    """Render the full dataset as schema-preserving markdown."""
    lines = [
        "## Full Dataset Markdown",
        "",
        "This section preserves the full dataset content in markdown field form.",
        "",
    ]

    sections = [
        ("Dataset Meta", data.get("_meta", {})),
        ("Data Dictionary", data.get("_data_dictionary", {})),
        ("Ads", data.get("_ads", {})),
    ]

    for heading, section_value in sections:
        lines.append(f"### {heading}")
        lines.append("")
        for field_path, field_value in _flatten_markdown_fields(section_value):
            lines.append(f"- {field_path}: {_format_scalar(field_value)}")
        lines.append("")

    records = data.get("data", [])
    lines.append("### Records")
    lines.append("")
    for index, record in enumerate(records, 1):
        lines.append(f"#### Record {index}")
        lines.append("")
        for field_path, field_value in _flatten_markdown_fields(record):
            lines.append(f"- {field_path}: {_format_scalar(field_value)}")
        lines.append("")

    return lines


def _render_dataset_content(data: dict) -> list[str]:
    """Render the shared dataset body for dated and latest responses."""
    meta = data.get("_meta", {})
    ads = data.get("_ads", {})

    lines = []
    lines.append(f"- Source: {meta.get('source', meta.get('dataset_name', 'news_dataset'))}")
    lines.append(f"- Schema: {meta.get('schema_version', 'v1')}")
    lines.append(f"- Language: {meta.get('normalization_language', 'en')}")
    lines.append(f"- Records: {len(data.get('data', []))}")
    generated_at = meta.get("generated_at")
    if generated_at:
        lines.append(f"- Generated At: {generated_at}")
    lines.append("")

    lines.extend(_render_ads(ads))
    lines.extend(_render_full_dataset_markdown(data))

    return lines


def format_dataset(data: dict, date: str, tier: str) -> str:
    """
    Format news_dataset.v1 into Markdown output.

    Parameters:
        data: Full dataset JSON (contains _meta, _data_dictionary, _ads, data)
        date: Date string
        tier: Tier name

    Returns:
        Markdown string
    """
    lines = []
    lines.append(f"# AI Daily News — {date} ({tier})")
    lines.append("")
    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)


def format_error(error_msg: str) -> str:
    """Format error output"""
    return f"Error: {error_msg}"


def format_latest_dataset(result: dict, tier: str) -> str:
    """
    Format the wrapped latest dataset response.

    Parameters:
        result: The wrapped response from L2 (contains dataset_ref, resolved_date,
                freshness_status, days_behind, notice_for_user, data)
        tier: Tier name

    Returns:
        Markdown string with freshness metadata and dataset content
    """
    dataset_ref = result.get("dataset_ref", "latest")
    resolved_date = result.get("resolved_date", "")
    freshness_status = result.get("freshness_status", "")
    days_behind = result.get("days_behind", 0)
    notice_for_user = result.get("notice_for_user", "")
    data = result.get("data", {})

    # Check for local time enhancement
    display_notice = result.get("display_notice")
    generated_at_local = result.get("generated_at_local")
    client_timezone = result.get("client_timezone")
    resolved_source_date = result.get("resolved_source_date", resolved_date)
    display_mode = result.get("display_mode")

    # First, format the freshness metadata section (IMPORTANT: LLM must see this first)
    lines = []
    lines.append(f"# AI Daily News — Latest Available ({tier})")
    lines.append("")

    if display_mode == "local_time" and display_notice:
        # Prefer local time display for enhanced responses
        lines.append("## Freshness Information (Local Time)")
        lines.append("")
        lines.append(f"- **Notice**: {display_notice}")
        if generated_at_local:
            lines.append(f"- **Generated At (Local)**: {generated_at_local}")
        if client_timezone:
            lines.append(f"- **Your Timezone**: {client_timezone}")
        lines.append(f"- **Resolved Canonical Date**: {resolved_source_date}")
        lines.append("")
    else:
        # Legacy display mode
        lines.append("## Freshness Information")
        lines.append("")
        lines.append(f"- **Resolved Date**: {resolved_date}")
        lines.append(f"- **Freshness Status**: {freshness_status}")
        lines.append(f"- **Days Behind**: {days_behind}")
        lines.append(f"- **Notice**: {notice_for_user}")
        lines.append(f"- **Dataset Ref**: {dataset_ref}")
        lines.append("")

    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)


def format_resolved_date_dataset(result: dict, tier: str) -> str:
    """
    Format the wrapped local date resolved dataset response.

    Parameters:
        result: The wrapped response from L2 (contains requested_local_date,
                resolved_source_date, display_notice, data)
        tier: Tier name

    Returns:
        Markdown string with local date metadata and dataset content
    """
    requested_local_date = result.get("requested_local_date", "")
    resolved_source_date = result.get("resolved_source_date", "")
    client_timezone = result.get("client_timezone", "")
    generated_at_local = result.get("generated_at_local", "")
    display_notice = result.get("display_notice", "")
    data = result.get("data", {})

    lines = []
    lines.append(f"# AI Daily News — {requested_local_date} (Local Time, {tier})")
    lines.append("")
    lines.append("## Date Resolution Information")
    lines.append("")
    lines.append(f"- **Notice**: {display_notice}")
    lines.append(f"- **Requested Local Date**: {requested_local_date}")
    lines.append(f"- **Your Timezone**: {client_timezone}")
    lines.append(f"- **Resolved Canonical Date**: {resolved_source_date}")
    if generated_at_local:
        lines.append(f"- **Generated At (Local)**: {generated_at_local}")
    lines.append("")

    lines.extend(_render_dataset_content(data))

    return "\n".join(lines)
