"""Normalization helpers for staged `.b2s` action records."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


_DEFAULT_ACTION_FIELDS: dict[str, Any] = {
    "prompt_family": "b2s",
    "policy_refs": [],
    "template_mode": "strict",
    "compatibility": {},
    "iteration_mode": None,
    "item_source": None,
    "item_pattern": None,
}

_DEFAULT_INPUTS = {
    "required": [],
    "optional": [],
}

_DEFAULT_OUTPUTS = {
    "primary": None,
    "secondary": [],
}

_DEFAULT_VALIDATION_RULES = {
    "required": [],
    "optional": [],
}


def _merge_dict_defaults(source: dict[str, Any] | None, defaults: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(defaults)
    if source:
        for key, value in source.items():
            merged[key] = deepcopy(value)
    return merged


def normalize_action(action: dict[str, Any]) -> dict[str, Any]:
    """Return a canonical action dict with backward-compatible defaults applied."""
    normalized = deepcopy(action)

    for key, value in _DEFAULT_ACTION_FIELDS.items():
        normalized.setdefault(key, deepcopy(value))

    normalized["policy_refs"] = list(normalized.get("policy_refs") or [])
    normalized["conditions"] = list(normalized.get("conditions") or [])
    normalized["must_include"] = list(normalized.get("must_include") or [])

    normalized["inputs"] = _merge_dict_defaults(normalized.get("inputs"), _DEFAULT_INPUTS)
    normalized["inputs"]["required"] = list(normalized["inputs"].get("required") or [])
    normalized["inputs"]["optional"] = list(normalized["inputs"].get("optional") or [])

    normalized["outputs"] = _merge_dict_defaults(normalized.get("outputs"), _DEFAULT_OUTPUTS)
    normalized["outputs"]["secondary"] = list(normalized["outputs"].get("secondary") or [])

    normalized["validation_rules"] = _merge_dict_defaults(
        normalized.get("validation_rules"),
        _DEFAULT_VALIDATION_RULES,
    )
    normalized["validation_rules"]["required"] = list(normalized["validation_rules"].get("required") or [])
    normalized["validation_rules"]["optional"] = list(normalized["validation_rules"].get("optional") or [])

    normalized["compatibility"] = _merge_dict_defaults(normalized.get("compatibility"), {})
    normalized["human_gate"] = _merge_dict_defaults(normalized.get("human_gate"), {"required": False})
    normalized["status_model"] = _merge_dict_defaults(normalized.get("status_model"), {})
    normalized["on_pass"] = _merge_dict_defaults(normalized.get("on_pass"), {"update_state": {}})
    normalized["on_pass"]["update_state"] = dict(normalized["on_pass"].get("update_state") or {})

    return normalized


def normalize_actions(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize every action in the registry."""
    return [normalize_action(action) for action in actions]
