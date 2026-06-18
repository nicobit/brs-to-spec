# Prompt 05 — Enrich OpenSpec Handoff and Add Validators

## Context

You are working on the `.b2s` framework at the root of this repository.

Technical specification artifacts and their workflow actions exist from prompts 01-04.
This prompt does two things:
1. Updates `create-openspec-handoff` skill to consume technical specifications when present
2. Adds shallow validators for the new artifact types

Before making changes, read these files in full:
- `.b2s/skills/engineering-lead/create-openspec-handoff.md`
- `.b2s/scripts/b2s_engine/validation.py`
- `.b2s/artifact-templates/exposed-api-spec.md`
- `.b2s/artifact-templates/consumed-api-spec.md`
- `.b2s/artifact-templates/database-schema-spec.md`
- `.b2s/artifact-templates/integration-spec.md`

---

## Step 1 — Update create-openspec-handoff skill

In `.b2s/skills/engineering-lead/create-openspec-handoff.md`, find the section that
lists optional inputs to read. Add instructions for consuming technical specifications:

After the existing optional-input reading instructions, add:

```
If `technical-specifications/api/exposed/` exists and contains files:
  - Read each exposed API spec file
  - For each story, find the endpoint(s) in the exposed API specs that the story implements
  - Populate Section 6 (Implementation Context) → API Impact with the exact endpoint path,
    method, request fields, response fields, and error codes from the spec — not invented values
  - Populate Section 7 (Constraints) with the auth mechanism and SLA from the spec

If `technical-specifications/api/consumed/` exists and contains files:
  - Read each consumed API spec file for external systems this story calls
  - Populate Section 6 → Impacted Components with the external system's endpoint path,
    auth mechanism, and timeout from the consumed spec
  - Populate Section 7 (Constraints) with PII minimisation rules from the consumed spec

If `technical-specifications/database/` exists and contains files:
  - Read the database schema spec for the domain this story writes to
  - Populate Section 6 → Data Impact with the exact table name, column names, types,
    and constraints from the schema spec — not invented column names
  - Note any PII columns and their retention period

If `technical-specifications/integrations/` exists and contains files:
  - Read the integration spec for each external system this story calls
  - Populate Section 8 (Dependencies) with the integration's timeout, retry policy,
    and fallback behaviour from the integration spec
```

---

## Step 2 — Add validators for technical specification artifacts

In `.b2s/scripts/b2s_engine/validation.py`, add three new validator functions
and register them in `VALIDATORS_BY_ARTIFACT`.

### Validator: _validate_exposed_api_spec_directory

Add after `_validate_story_package_directory`. Validates files under
`technical-specifications/api/exposed/`.

Checks (implement each as a named check following the existing pattern):

| Check name | What it verifies |
|---|---|
| `exposed_api_has_endpoints` | File contains a table row with METHOD and /v1/ path |
| `exposed_api_has_auth` | "Auth mechanism" row is present and not a placeholder |
| `exposed_api_has_contract_mode` | "Contract mode" row is present with a valid value |
| `exposed_api_has_sla` | SLA table is present with at least one row |
| `exposed_api_no_placeholders` | No `{{`, `}}`, `NNN`, `TBD`, `TODO` in file |
| `exposed_api_has_story_ref` | At least one `F-\d{3}\.\d+` reference in endpoint table |

### Validator: _validate_consumed_api_spec_directory

Validates files under `technical-specifications/api/consumed/`.

| Check name | What it verifies |
|---|---|
| `consumed_api_has_endpoints` | File contains at least one endpoint row |
| `consumed_api_has_auth` | "Auth mechanism" row is present and not a placeholder |
| `consumed_api_has_fallback` | "Fallback behaviour" row present with actionable value (not TBD) |
| `consumed_api_has_pii_section` | "PII and Data Residency" section present |
| `consumed_api_no_placeholders` | No `{{`, `}}`, `TBD`, `TODO` |

### Validator: _validate_integration_spec_directory

Validates files under `technical-specifications/integrations/`.

| Check name | What it verifies |
|---|---|
| `integration_has_timeout` | "Timeout per request" row present with a numeric value (ms) |
| `integration_has_retry` | "Max retries" row present with a numeric value |
| `integration_has_fallback` | "Fallback behaviour" row present and not placeholder |
| `integration_has_events` | "Success event" and "Failure event" rows present |
| `integration_no_placeholders` | No `{{`, `}}`, `TBD`, `TODO` |

### Register in VALIDATORS_BY_ARTIFACT

Add entries to the `VALIDATORS_BY_ARTIFACT` dict:

```python
"technical-specifications/api/exposed/": _validate_exposed_api_spec_directory,
"technical-specifications/api/consumed/": _validate_consumed_api_spec_directory,
"technical-specifications/integrations/": _validate_integration_spec_directory,
```

---

## Step 3 — Add test fixtures and tests

### Fixture: shallow-exposed-api-spec

Create `.b2s/tests/fixtures/shallow-exposed-api-spec/`:
- `.b2s/state/workflow-state.json`: `active_action: create-exposed-api-specs`
- `technical-specifications/api/exposed/v1-api.md`: minimal file with no endpoints, no auth, placeholders

### Fixture: valid-exposed-api-spec

Create `.b2s/tests/fixtures/valid-exposed-api-spec/`:
- `.b2s/state/workflow-state.json`: `active_action: create-exposed-api-specs`
- `technical-specifications/api/exposed/v1-applications-api.md`: complete file with:
  - `POST /v1/applications` endpoint, F-001.1 story ref
  - Auth: OAuth2 client credentials
  - Contract mode: product
  - SLA table with p99 values
  - No placeholders

### Tests in test_engine_fixtures.py

Add `TechnicalSpecValidatorTests` class with:
- `test_validate_exposed_api_spec_fails_for_shallow`: asserts fail + specific check names in failures
- `test_validate_exposed_api_spec_passes_for_valid`: asserts overall pass

---

## Done criteria

- [ ] `create-openspec-handoff` skill reads and applies all four technical-specifications/ input types
- [ ] `_validate_exposed_api_spec_directory` implemented with 6 checks
- [ ] `_validate_consumed_api_spec_directory` implemented with 5 checks
- [ ] `_validate_integration_spec_directory` implemented with 5 checks
- [ ] All three validators registered in `VALIDATORS_BY_ARTIFACT`
- [ ] Two fixtures created (shallow and valid)
- [ ] `TechnicalSpecValidatorTests` class added with 2 tests
- [ ] All tests pass (existing 55 + 2 new = 57 minimum)
