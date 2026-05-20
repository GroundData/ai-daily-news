"""
remote_client.py — L3 HTTP client

Responsibilities:
- Communicate with L2 API (Manifest, download, remote execution)
- Unified timeout and error handling
- Auto-follow 302 redirects (urllib default behavior)
"""

import json
import os
import urllib.request
import urllib.error
from typing import Optional

DEFAULT_SERVICE_URL = os.getenv("AINEWS_SERVICE_URL", "https://api.ainewparadigm.cn")
DEFAULT_TIMEOUT = 30  # Downloads may take longer


def _build_headers(api_key: Optional[str] = None) -> dict:
    headers = {
        "X-Client": "ai-daily-news-l3",
        "Accept": "application/json",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def fetch_manifest(
    base_url: Optional[str] = None,
    timeout: int = 10,
) -> dict:
    """Fetch Manifest"""
    url = f"{base_url or DEFAULT_SERVICE_URL}/v1/manifest"
    try:
        req = urllib.request.Request(url, headers=_build_headers())
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise NetworkError(f"Manifest HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Manifest error: {e}")


def download_dataset(
    date: str,
    tier: str = "guest",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """
    Download dataset file.

    Returns gzip-compressed byte data.
    Auto-follow L2's 302 redirects to CDN.
    """
    url = (
        f"{base_url or DEFAULT_SERVICE_URL}/v1/data/download"
        f"?product_name=news_dataset&schema_version=v1"
        f"&date={date}&tier={tier}"
    )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        # urllib.request.urlopen defaults allow_redirects=True
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise NetworkError(f"Dataset not found for date={date}, tier={tier}")
        raise NetworkError(f"Download HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Download error: {e}")


def download_pro_dataset(
    date: str,
    tier: str = "pro_core",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> bytes:
    """Download paid dataset (requires Token)"""
    url = (
        f"{base_url or DEFAULT_SERVICE_URL}/v1/data/download/pro"
        f"?product_name=news_dataset&schema_version=v1"
        f"&date={date}&tier={tier}"
    )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError(f"Dataset not found for date={date}, tier={tier}")
        raise NetworkError(f"Pro download HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Pro download error: {e}")


def invoke_capability(
    capability_name: str,
    params: dict,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 60,
) -> dict:
    """Invoke remote capability"""
    url = f"{base_url or DEFAULT_SERVICE_URL}/v1/execute"
    payload = json.dumps({"capability_name": capability_name, "params": params}).encode("utf-8")

    headers = _build_headers(api_key)
    headers["Content-Type"] = "application/json"

    try:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise NetworkError(f"Execute HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Execute error: {e}")


def resolve_latest(
    tier: str = "guest",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """
    Resolve the latest available date and get freshness metadata only.

    Returns metadata without actual data. Then call download_dataset with
    the resolved_date to get the actual data.
    """
    if tier == "guest":
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )
    else:
        url = (
            f"{base_url or DEFAULT_SERVICE_URL}/v1/data/resolve-latest/pro"
            f"?product_name=news_dataset&schema_version=v1&tier={tier}"
        )

    headers = _build_headers(api_key)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise NetworkError("Invalid or missing access token")
        if e.code == 403:
            raise NetworkError(f"Tier {tier} not included in your subscription")
        if e.code == 404:
            raise NetworkError("No available dataset found")
        raise NetworkError(f"Resolve latest HTTP error: {e.code}")
    except Exception as e:
        raise NetworkError(f"Resolve latest error: {e}")


# Import errors from schemas
from lib.schemas import NetworkError
