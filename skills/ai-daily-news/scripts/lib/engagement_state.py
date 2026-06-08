"""
engagement_state.py — L3 local engagement state

Responsibilities:
- Persist anonymous install_id
- Track feedback and survey delivery cooldowns
- Keep engagement state failures from blocking news delivery
"""

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from lib.runtime_paths import get_engagement_state_path

DEFAULT_SURVEY_COOLDOWN_DAYS = 30
DEFAULT_FEEDBACK_PROMPT_COOLDOWN_DAYS = 14
DEFAULT_UPGRADE_NOTICE_COOLDOWN_DAYS = 7
CLIENT_CAPABILITIES = "engagement_v1"


_EMPTY_STATE = {
    "install_id": None,
    "first_feedback_hint_shown": False,
    "feedback_prompt_cooldown_until": None,
    "survey_cooldown_until": None,
    "upgrade_notice_cooldown_until": None,
    "shown_delivery_ids": [],
    "shown_notice_delivery_ids": [],
    "submitted_delivery_ids": [],
    "dismissed_delivery_ids": [],
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return None


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_id_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    seen = set()
    result = []
    for item in value:
        if not isinstance(item, str) or not item:
            continue
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _new_state() -> dict:
    state = dict(_EMPTY_STATE)
    state["install_id"] = str(uuid.uuid4())
    return state


def _normalize_state(raw) -> dict:
    state = _new_state()
    if not isinstance(raw, dict):
        return state

    install_id = raw.get("install_id")
    if isinstance(install_id, str):
        try:
            uuid.UUID(install_id)
            state["install_id"] = install_id
        except ValueError:
            pass

    state["first_feedback_hint_shown"] = bool(raw.get("first_feedback_hint_shown", False))
    for key in ("feedback_prompt_cooldown_until", "survey_cooldown_until", "upgrade_notice_cooldown_until"):
        value = raw.get(key)
        state[key] = value if isinstance(value, str) and _parse_time(value) else None
    for key in ("shown_delivery_ids", "shown_notice_delivery_ids", "submitted_delivery_ids", "dismissed_delivery_ids"):
        state[key] = _normalize_id_list(raw.get(key))
    return state


def load_engagement_state() -> dict:
    path = get_engagement_state_path()
    if not path.exists():
        state = _new_state()
        save_engagement_state(state)
        return state
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        raw = {}
    state = _normalize_state(raw)
    save_engagement_state(state)
    return state


def save_engagement_state(state: dict) -> None:
    path = get_engagement_state_path()
    normalized = _normalize_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def get_or_create_install_id() -> str:
    state = load_engagement_state()
    return state["install_id"]


def get_client_capabilities() -> str:
    return CLIENT_CAPABILITIES


def is_survey_in_cooldown(state: dict, now: Optional[datetime] = None) -> bool:
    until = _parse_time(state.get("survey_cooldown_until"))
    if not until:
        return False
    return until > (now or _utc_now())


def is_feedback_prompt_in_cooldown(state: dict, now: Optional[datetime] = None) -> bool:
    until = _parse_time(state.get("feedback_prompt_cooldown_until"))
    if not until:
        return False
    return until > (now or _utc_now())


def has_seen_delivery(state: dict, delivery_id: str) -> bool:
    if not delivery_id:
        return False
    return any(
        delivery_id in state.get(key, [])
        for key in ("shown_delivery_ids", "submitted_delivery_ids", "dismissed_delivery_ids")
    )


def _append_unique(state: dict, key: str, value: str) -> None:
    if not value:
        return
    items = _normalize_id_list(state.get(key))
    if value not in items:
        items.append(value)
    state[key] = items


def _cooldown_until(days: int) -> str:
    return _format_time(_utc_now() + timedelta(days=days))


def mark_delivery_shown(state: dict, delivery_id: str, kind: str, cooldown_days: Optional[int] = None) -> dict:
    state = _normalize_state(state)
    _append_unique(state, "shown_delivery_ids", delivery_id)
    if kind == "survey":
        days = max(DEFAULT_SURVEY_COOLDOWN_DAYS, int(cooldown_days or DEFAULT_SURVEY_COOLDOWN_DAYS))
        state["survey_cooldown_until"] = _cooldown_until(days)
    elif kind == "feedback_prompt":
        days = max(1, int(cooldown_days or DEFAULT_FEEDBACK_PROMPT_COOLDOWN_DAYS))
        state["feedback_prompt_cooldown_until"] = _cooldown_until(days)
    return state


def is_upgrade_notice_in_cooldown(state: dict, now: Optional[datetime] = None) -> bool:
    until = _parse_time(state.get("upgrade_notice_cooldown_until"))
    if not until:
        return False
    return until > (now or _utc_now())


def mark_notice_delivery_shown(state: dict, delivery_id: str, kind: str, cooldown_days: Optional[int] = None) -> dict:
    state = _normalize_state(state)
    if kind == "upgrade_notice":
        _append_unique(state, "shown_notice_delivery_ids", delivery_id)
        days = max(1, int(cooldown_days or DEFAULT_UPGRADE_NOTICE_COOLDOWN_DAYS))
        state["upgrade_notice_cooldown_until"] = _cooldown_until(days)
    return state


def mark_survey_submitted(state: dict, cooldown_days: int = DEFAULT_SURVEY_COOLDOWN_DAYS) -> dict:
    state = _normalize_state(state)
    if state.get("shown_delivery_ids"):
        _append_unique(state, "submitted_delivery_ids", state["shown_delivery_ids"][-1])
    state["survey_cooldown_until"] = _cooldown_until(max(DEFAULT_SURVEY_COOLDOWN_DAYS, int(cooldown_days)))
    return state


def mark_delivery_dismissed(state: dict, delivery_id: str, kind: str, cooldown_days: Optional[int] = None) -> dict:
    state = _normalize_state(state)
    _append_unique(state, "dismissed_delivery_ids", delivery_id)
    if kind == "survey":
        days = max(DEFAULT_SURVEY_COOLDOWN_DAYS, int(cooldown_days or DEFAULT_SURVEY_COOLDOWN_DAYS))
        state["survey_cooldown_until"] = _cooldown_until(days)
    return state


def should_show_first_feedback_hint(state: dict) -> bool:
    return not bool(state.get("first_feedback_hint_shown"))


def mark_first_feedback_hint_shown(state: dict) -> dict:
    state = _normalize_state(state)
    state["first_feedback_hint_shown"] = True
    return state
