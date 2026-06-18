"""Template loading and runtime event instantiation from event templates."""

from pathlib import Path
from typing import Any

from .workspace import WorkspaceError

try:
    import yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


class TemplateError(Exception):
    pass


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        raise TemplateError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    if _YAML_AVAILABLE:
        return yaml.safe_load(text)
    raise TemplateError(
        "PyYAML is not installed. Install it with: pip install pyyaml"
    )


def find_template(repo_root: Path, template_id: str) -> Path:
    """
    Locate a template file by its EVT-TPL-NNN id.
    Scans .brs2spec2/workflow/event-templates/.
    """
    templates_dir = repo_root / ".brs2spec2" / "workflow" / "event-templates"
    if not templates_dir.is_dir():
        raise TemplateError(f"Event templates directory not found: {templates_dir}")

    prefix = template_id.upper()
    matches = list(templates_dir.glob(f"{prefix}-*.yaml"))
    if not matches:
        raise TemplateError(
            f"No template file found for {template_id} in {templates_dir}"
        )
    if len(matches) > 1:
        raise TemplateError(
            f"Multiple template files match {template_id}: {[str(m) for m in matches]}"
        )
    return matches[0]


def load_template(path: Path) -> dict:
    """Load and return a template YAML as a dict."""
    data = _load_yaml(path)
    if not isinstance(data, dict):
        raise TemplateError(f"Template file is not a YAML mapping: {path}")
    if "event_template_id" not in data:
        raise TemplateError(
            f"Template missing required field 'event_template_id': {path}"
        )
    return data


def build_runtime_event(template: dict, event_id: str, created_at: str, notes: str = "") -> dict:
    """
    Build a runtime event dict from a template following the field mapping
    defined in template-instantiation-rules.md section 2.

    Raises TemplateError if mandatory fields are missing from the template.
    """
    _require_template_fields(template)

    # type → event_type + action (section 3 mapping)
    event_type, action = _map_type(template.get("type", ""))

    # inputs
    required_inputs = template.get("inputs", {}).get("required", []) or []
    optional_inputs = template.get("inputs", {}).get("optional", []) or []
    read_from = list(required_inputs) + list(optional_inputs)

    # outputs
    outputs = template.get("outputs", {})
    write_to = []
    if outputs.get("primary"):
        write_to.append(outputs["primary"])
    for sec in (outputs.get("secondary") or []):
        write_to.append(sec)

    event = {
        "event_id": event_id,
        "event_type": event_type,
        "action": action,
        "persona": template.get("persona", ""),
        "priority": template.get("priority", "normal"),
        "task": {
            "title": template.get("title", action),
            "objective": template.get("description", ""),
        },
        "read_from": read_from,
        "required_inputs": required_inputs,
        "optional_inputs": optional_inputs,
        "write_to": write_to,
        "meta": {
            "template_id": template["event_template_id"],
            "created_at": created_at,
            "created_by": "orchestrator",
            "notes": notes,
        },
    }

    # copy fields that must be verbatim — omitting any silently breaks validation
    for field in ("skill_ref", "persona_ref", "artifact_template_ref",
                  "must_include", "validation_rules", "on_success", "on_failure",
                  "blocked_by", "blocked_by_events", "gate_context"):
        if field in template:
            event[field] = template[field]

    return event


def _require_template_fields(template: dict) -> None:
    required = ["event_template_id", "type", "persona", "description"]
    missing = [f for f in required if not template.get(f)]
    if missing:
        raise TemplateError(
            f"Template '{template.get('event_template_id', '?')}' "
            f"is missing required fields: {missing}"
        )


# Section 3 mapping: template type string → (event_type, action)
_TYPE_MAP: dict[str, tuple[str, str]] = {
    "route_initiative":                 ("ROUTE_INITIATIVE",    "route_initiative"),
    "create_business_intake_summary":   ("CREATE_ARTIFACT",     "create_business_intake_summary"),
    "gate_business_intake_review":      ("WAIT_HUMAN",          "gate_business_intake_review"),
    "create_business_rules":            ("CREATE_ARTIFACT",     "create_business_rules"),
    "create_actors_and_personas":       ("CREATE_ARTIFACT",     "create_actors_and_personas"),
    "find_gaps_and_questions":          ("CREATE_ARTIFACT",     "find_gaps_and_questions"),
    "create_process_flows":             ("CREATE_ARTIFACT",     "create_process_flows"),
    "create_use_case_specs":            ("CREATE_ARTIFACT",     "create_use_case_specs"),
    "review_initial_architecture":      ("REVIEW_ARTIFACT",     "review_initial_architecture"),
    "create_architecture_rules":        ("CREATE_ARTIFACT",     "create_architecture_rules"),
    "review_existing_system_impact":    ("REVIEW_ARTIFACT",     "review_existing_system_impact"),
    "create_delivery_structure":        ("CREATE_ARTIFACT",     "create_delivery_structure"),
    "create_traceability_matrix":       ("CREATE_ARTIFACT",     "create_traceability_matrix"),
    "identify_software_modules":        ("CREATE_ARTIFACT",     "identify_software_modules"),
    "define_delivery_increments":       ("CREATE_ARTIFACT",     "define_delivery_increments"),
    "check_engineering_readiness":      ("VALIDATE_ARTIFACT",   "check_engineering_readiness"),
    "generate_initiative_context":      ("CREATE_ARTIFACT",     "generate_initiative_context"),
    "create_bdd_scenarios":             ("CREATE_ARTIFACT",     "create_bdd_scenarios"),
    "create_test_strategy":             ("CREATE_ARTIFACT",     "create_test_strategy"),
    "create_security_review":           ("CREATE_ARTIFACT",     "create_security_review"),
    "create_api_contract":              ("CREATE_ARTIFACT",     "create_api_contract"),
    "create_data_contract":             ("CREATE_ARTIFACT",     "create_data_contract"),
    "create_event_contract":            ("CREATE_ARTIFACT",     "create_event_contract"),
    "create_observability_plan":        ("CREATE_ARTIFACT",     "create_observability_plan"),
    "create_openspec_handoff":          ("GENERATE_HANDOFF",    "create_openspec_handoff"),
    "create_compact_handoff":           ("GENERATE_HANDOFF",    "create_compact_handoff"),
    "create_standalone_handoff":        ("GENERATE_HANDOFF",    "create_standalone_handoff"),
    "generate_test_stubs":              ("CREATE_ARTIFACT",     "generate_test_stubs"),
    "create_review_package":            ("CREATE_ARTIFACT",     "create_review_package"),
    "create_agile_planning_view":       ("CREATE_ARTIFACT",     "create_agile_planning_view"),
    "create_entity_model":              ("CREATE_ARTIFACT",     "create_entity_model"),
    "create_business_test_expectations":("CREATE_ARTIFACT",     "create_business_test_expectations"),
    "draft_architecture_from_brs":      ("CREATE_ARTIFACT",     "draft_architecture_from_brs"),
    "create_brs":                       ("CREATE_ARTIFACT",     "create_brs"),
    "create_threat_model":              ("CREATE_ARTIFACT",     "create_threat_model"),
    "map_capabilities_to_modules":      ("CREATE_ARTIFACT",     "map_capabilities_to_modules"),
    "create_test_plan_per_story":       ("CREATE_ARTIFACT",     "create_test_plan_per_story"),
    "senior_code_review":               ("REVIEW_ARTIFACT",     "senior_code_review"),
    "architecture_review_implementation":("REVIEW_ARTIFACT",   "architecture_review_implementation"),
    "spec_correction":                  ("REPAIR_ARTIFACT",     "spec_correction"),
    "gate_architecture_review":         ("WAIT_HUMAN",          "gate_architecture_review"),
    "gate_engineering_readiness_review":("WAIT_HUMAN",          "gate_engineering_readiness_review"),
    "create_use_case_diagram":          ("CREATE_ARTIFACT",     "create_use_case_diagram"),
    "create_requirements":              ("CREATE_ARTIFACT",     "create_requirements"),
}


def _map_type(type_str: str) -> tuple[str, str]:
    key = type_str.lower().strip()
    if key in _TYPE_MAP:
        return _TYPE_MAP[key]
    # direct event_type passthrough for well-known types used as the type: field
    _DIRECT = {
        "wait_human":        ("WAIT_HUMAN",       "wait_human"),
        "route_initiative":  ("ROUTE_INITIATIVE",  "route_initiative"),
        "raise_decision":    ("RAISE_DECISION",    "raise_decision"),
        "resolve_decision":  ("RESOLVE_DECISION",  "resolve_decision"),
        "retry_failed_task": ("RETRY_FAILED_TASK", "retry_failed_task"),
    }
    if key in _DIRECT:
        return _DIRECT[key]
    # fallback: treat as custom CREATE_ARTIFACT
    return ("CREATE_ARTIFACT", key)
