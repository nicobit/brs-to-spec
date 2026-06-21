# Golden Action Examples

This page shows compact examples of fully enriched `.b2s` actions.

These are reference shapes, not the only valid way to author actions.

## Business intake

```yaml
- action_id: create-business-intake-summary
  stage_id: "2-business-intake"
  persona: product-owner
  prompt_family: b2s
  skill_ref: ".b2s/skills/product-owner/create-business-intake-summary.md"
  artifact_template_ref: ".b2s/artifact-templates/business-intake-summary.md"
  policy_refs:
    - ".b2s/policies/business/business-glossary-guidance.md"
    - ".b2s/policies/business/business-writing-guidelines.md"
  inputs:
    required:
      - "input/brs.md"
      - "routing/routing-decision.md"
    optional:
      - "input/brs/*.md"
      - "input/architecture.md"
  outputs:
    primary: "business-intake/business-intake-summary.md"
    secondary: []
  validation_profile: structured-document
  validation_rules:
    required: []
    optional: []
  human_gate:
    required: true
    gate_id: "business-intake-review"
    owner: "product-owner"
```

## Requirements

```yaml
- action_id: create-requirements
  stage_id: "2b-business-analysis"
  persona: product-owner
  prompt_family: speckit
  skill_ref: ".b2s/skills/product-owner/create-requirements.md"
  artifact_template_ref: ".b2s/artifact-templates/requirements.md"
  policy_refs:
    - ".b2s/policies/requirements/definition-of-ready.md"
    - ".b2s/policies/requirements/requirement-writing-standard.md"
  inputs:
    required:
      - "business-intake/business-intake-summary.md"
      - "input/brs.md"
    optional:
      - "input/brs/*.md"
      - "routing/routing-decision.md"
  outputs:
    primary: "business-analysis/requirements.md"
    secondary: []
  validation_profile: catalog
  validation_rules:
    required:
      - "requirement_has_id"
      - "requirement_is_testable"
    optional: []
  human_gate:
    required: false
```

## Architecture review

```yaml
- action_id: review-initial-architecture
  stage_id: "3-planning"
  persona: architect
  prompt_family: b2s
  skill_ref: ".b2s/skills/architect/review-initial-architecture.md"
  artifact_template_ref: ".b2s/artifact-templates/architecture-review.md"
  policy_refs:
    - ".b2s/policies/architecture/architecture-principles.md"
    - ".b2s/policies/architecture/technology-standards.md"
  inputs:
    required:
      - "business-analysis/requirements.md"
      - "business-analysis/gaps-and-questions.md"
      - "business-intake/business-intake-summary.md"
      - "routing/routing-decision.md"
      - "input/brs.md"
    optional:
      - "input/architecture.md"
      - "business-analysis/business-rules.md"
  outputs:
    primary: "architecture/architecture-review.md"
    secondary: []
  validation_profile: analytical-review
  validation_rules:
    required:
      - "architecture_lists_impacted_systems"
      - "architecture_lists_constraints"
      - "architecture_lists_risks"
    optional: []
  human_gate:
    required: true
    gate_id: "architecture-review"
    owner: "architect"
```

## AI coding handoff

```yaml
- action_id: create-openspec-handoff
  stage_id: "5-handoff"
  persona: engineering-lead
  prompt_family: hve
  skill_ref: ".b2s/skills/engineering-lead/create-openspec-handoff.md"
  artifact_template_ref: ".b2s/artifact-templates/openspec-handoff.md"
  policy_refs:
    - ".b2s/policies/handoff/coding-constraints.md"
    - ".b2s/policies/testing/testing-expectations.md"
    - ".b2s/policies/handoff/ai-handoff-constraints.md"
  inputs:
    required:
      - "engineering-readiness/initiative-context.md"
      - "engineering-readiness/readiness-check.md"
      - "planning/delivery-structure.md"
      - "architecture/architecture-rules.md"
      - "quality-gates/nfr-assessment.md"
    optional:
      - "quality-gates/bdd-scenarios.md"
      - "quality-gates/api-contract.md"
      - "quality-gates/data-contract.md"
      - "quality-gates/test-strategy.md"
      - "technical-specifications/api/exposed/"
      - "technical-specifications/data/"
  outputs:
    primary: "specs/"
    secondary: []
  validation_profile: artifact-package
  validation_rules:
    required: []
    optional: []
  human_gate:
    required: false
```
