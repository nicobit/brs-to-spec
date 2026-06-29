# Epic Clarifications

Use one YAML file per epic inside an initiative workspace:

```text
input/clarifications/E-001.yaml
```

Suggested shape:

```yaml
epic_id: E-001
status:
  resolution_mode: partial
  last_updated: 2026-06-27
source_context:
  implementation_contract: epics/E-001-<slug>/implementation-contract.md
  ui_specification: architecture/ui-specification.md
answers:
  - question_id: UIQ-002
    route: /apply
    page: Application Form
    topic: auth_provider
    answer: Azure AD B2C
    impact: Route guard uses B2C redirect login.
    resolved_by: human
    resolved_at: 2026-06-27
unresolved:
  - question_id: UIQ-007
    reason: Waiting for external contract
```
