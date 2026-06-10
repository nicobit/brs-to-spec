# BDD Scenarios

## Metadata

| Field | Value |
|---|---|
| Initiative | I003-admin-portal |
| Gate | BDD scenarios |
| Triggered | Yes |
| Required | Yes |
| Owner | QA / Product |
| Artifact | quality-gates/bdd-scenarios.md |
| Status | Accepted |
| Reviewer | QA / Product |
| Review date | |

## Purpose

Produce executable Gherkin scenarios for every in-scope user story listed in `planning/delivery-structure.md`. Each scenario references the exact story ID (as used in the delivery structure), the requirement (FR-NNN or NFR-NNN), and the specific acceptance criterion (AC-NNN) where available. If an AC is missing, a placeholder is used and an open question added.

## Coverage Summary

| SCN | Story ID | Req | AC | Type | Priority |
|---:|---|---:|---|---|---|
| SCN-001 | E-001.1 | FR-001 | AC-004 | Happy path | P0 |
| SCN-002 | E-001.1 | FR-001 | AC-004 | Validation failure | P1 |
| SCN-003 | E-001.1 | FR-001 | AC-004 | Boundary (pagination) | P1 |
| SCN-004 | E-001.1 | FR-001 | AC-004 | Authorization | P1 |
| SCN-005 | E-001.2 | FR-001 | AC-004 | Happy path | P0 |
| SCN-006 | E-001.2 | FR-001 | AC-004 | Empty state | P1 |
| SCN-007 | E-001.2 | FR-001 | AC-004 | Pagination | P1 |
| SCN-008 | E-001.2 | FR-001 | AC-004 | Export boundary | P1 |
| SCN-009 | T-002.1 | FR-002 | AC-002 | Happy path | P0 |
| SCN-010 | T-002.1 | FR-002 | AC-002 | Invalid tenant | P1 |
| SCN-011 | T-002.1 | FR-002 | AC-002 | Persistence | P1 |
| SCN-012 | T-002.1 | FR-002 | AC-002 | Authorization | P1 |
| SCN-013 | T-002.2 | FR-002 | AC-002 | Happy path | P0 |
| SCN-014 | T-002.2 | FR-002 | AC-002 | No results UX | P1 |
| SCN-015 | T-002.2 | FR-002 | AC-002 | Performance | P1 |
| SCN-016 | T-002.2 | FR-002 | AC-002 | Authorization | P1 |
| SCN-017 | R-003.1 | FR-003 | AC-001 | Happy path | P0 |
| SCN-018 | R-003.1 | FR-003 | AC-001 | Invalid group | P1 |
| SCN-019 | R-003.1 | FR-003 | AC-001 | Nested roles | P1 |
| SCN-020 | R-003.1 | FR-003 | AC-001 | Audit linkage | P1 |
| SCN-021 | R-003.2 | FR-003 | AC-001 | Happy path | P0 |
| SCN-022 | R-003.2 | FR-003 | AC-001 | Validation error | P1 |
| SCN-023 | R-003.2 | FR-003 | AC-001 | Authorization | P1 |
| SCN-024 | R-003.2 | FR-003 | AC-001 | History paging | P1 |
| SCN-025 | O-004.1 | FR-004 | AC-002 | Short-op happy path | P0 |
| SCN-026 | O-004.1 | FR-004 | AC-002 | Async submission (202) | P0 |
| SCN-027 | O-004.1 | FR-004 | AC-002 | Job lifecycle | P1 |
| SCN-028 | O-004.1 | FR-004 | AC-002 | Idempotency | P1 |
| SCN-029 | O-004.2 | FR-004 | AC-002 | UI happy path | P0 |
| SCN-030 | O-004.2 | FR-004 | AC-002 | Cancel job | P1 |
| SCN-031 | O-004.2 | FR-004 | AC-002 | Progress UI | P1 |
| SCN-032 | O-004.2 | FR-004 | AC-002 | Authorization | P1 |
| SCN-033 | D-005.1 | FR-005 | AC-003 | Probe/link happy path | P0 |
| SCN-034 | D-005.1 | FR-005 | AC-003 | Link correctness | P1 |
| SCN-035 | D-005.1 | FR-005 | AC-003 | Boundary (query size) | P1 |
| SCN-036 | D-005.1 | FR-005 | AC-003 | Authorization | P1 |
| SCN-037 | D-005.2 | FR-005 | AC-003 | Recent errors | P0 |
| SCN-038 | D-005.2 | FR-005 | AC-003 | Backend unavailable | P1 |
| SCN-039 | D-005.2 | FR-005 | AC-003 | Limit/pagination | P1 |
| SCN-040 | D-005.2 | FR-005 | AC-003 | Authorization | P1 |
| SCN-041 | A-006.1 | FR-006 | AC-? | Happy path (append-only) | P0 |
| SCN-042 | A-006.1 | FR-006 | AC-? | Immutability negative | P1 |
| SCN-043 | A-006.1 | FR-006 | AC-? | Export masking | P1 |
| SCN-044 | A-006.1 | FR-006 | AC-? | Boundary (export size) | P1 |
| SCN-045 | A-006.2 | FR-006 | AC-? | UI happy path | P0 |
| SCN-046 | A-006.2 | FR-006 | AC-? | Authorization | P1 |
| SCN-047 | A-006.2 | FR-006 | AC-? | No-results negative | P1 |
| SCN-048 | A-006.2 | FR-006 | AC-? | Observability correlation | P1 |

## Scenarios by user story

### E-001.1 — Environment Inventory: Backend ingestion & paginated API (FR-001)

#### SCN-001
Metadata:
- Story: E-001.1
- FR: FR-001
- AC: AC-004
- Type: Happy path
- Priority: P0

```gherkin
Given an authenticated IT Operator with tenant "sample-1" and inventory items present
When the operator requests `GET /inventory?tenant=sample-1&page=1&pageSize=50`
Then the API returns `200 OK` with up to 50 inventory items including identifier and last-updated timestamp
And the response includes `totalCount` and `page` metadata
```

#### SCN-002
Metadata:
- Story: E-001.1
- FR: FR-001
- AC: AC-004
- Type: Validation failure
- Priority: P1

```gherkin
Given an authenticated user
When they call `GET /inventory?page=-1`
Then the API returns `400 Bad Request` with a validation error
```

#### SCN-003
Metadata:
- Story: E-001.1
- FR: FR-001
- AC: AC-004
- Type: Boundary (pagination)
- Priority: P1

```gherkin
Given 1,001 inventory items exist for tenant "sample-1"
When the operator requests `GET /inventory?tenant=sample-1&page=1&pageSize=1000`
Then the API returns `200 OK` with `items.length == 1000` and `totalCount >= 1001`
And a next-page link is present
```

#### SCN-004
Metadata:
- Story: E-001.1
- FR: FR-001
- AC: AC-004
- Type: Authorization
- Priority: P1

```gherkin
Given a user without inventory-read permission for tenant "sample-1"
When they call `GET /inventory?tenant=sample-1`
Then the API returns `403 Forbidden` and no inventory rows are returned
```

### E-001.2 — Environment Inventory: Frontend list, filters and pagination (FR-001)

#### SCN-005
Metadata:
- Story: E-001.2
- FR: FR-001
- AC: AC-004
- Type: Happy path
- Priority: P0

```gherkin
Given an IT Operator signed in with tenant "sample-1" selected
When they open the Inventory page
Then the UI displays a paginated list showing identifier, resource type, and last-updated for each row
And each row links to diagnostics and resource details
```

#### SCN-006
Metadata:
- Story: E-001.2
- FR: FR-001
- AC: AC-004
- Type: Empty state
- Priority: P1

```gherkin
Given no inventory items exist for tenant "empty-tenant"
When an operator opens the Inventory page
Then the UI shows an empty state with guidance to configure inventory sources
```

#### SCN-007
Metadata:
- Story: E-001.2
- FR: FR-001
- AC: AC-004
- Type: Pagination
- Priority: P1

```gherkin
Given more than 50 items exist for tenant "sample-1"
When the operator navigates to page 2
Then the UI loads page 2 within the performance SLO and shows the next set of items
```

#### SCN-008
Metadata:
- Story: E-001.2
- FR: FR-001
- AC: AC-004
- Type: Export boundary
- Priority: P1

```gherkin
Given the operator requests export of inventory for tenant "sample-1" with 10,000 items
When the export is generated
Then the system either returns a downloadable CSV or a link to the export and enforces maximum export size limits
```

### T-002.1 — Tenant & Stage Explorer: Backend mapping (FR-002)

#### SCN-009
Metadata:
- Story: T-002.1
- FR: FR-002
- AC: AC-002
- Type: Happy path
- Priority: P0

```gherkin
Given tenant mapping exists for "tenant-test-1" -> subscription "sub-001"
When a Support Engineer requests `GET /tenants/tenant-test-1/subscriptions`
Then the API returns `200 OK` with the expected subscription and resource group list
```

#### SCN-010
Metadata:
- Story: T-002.1
- FR: FR-002
- AC: AC-002
- Type: Invalid tenant
- Priority: P1

```gherkin
Given a malformed tenant identifier
When the client requests the mapping
Then the API returns `400 Bad Request` with validation details
```

#### SCN-011
Metadata:
- Story: T-002.1
- FR: FR-002
- AC: AC-002
- Type: Persistence
- Priority: P1

```gherkin
Given a tenant mapping is created for "tenant-test-3"
When the mapping is saved
Then subsequent queries return the new mapping and sample data
```

#### SCN-012
Metadata:
- Story: T-002.1
- FR: FR-002
- AC: AC-002
- Type: Authorization
- Priority: P1

```gherkin
Given a user lacks access to "tenant-test-2"
When they attempt to retrieve that tenant mapping
Then the API returns `403 Forbidden` and does not return tenant data
```

### T-002.2 — Tenant & Stage Explorer: Frontend selector and explorer (FR-002)

#### SCN-013
Metadata:
- Story: T-002.2
- FR: FR-002
- AC: AC-002
- Type: Happy path
- Priority: P0

```gherkin
Given multiple tenants and stages available
When the operator selects tenant "tenant-test-1" and stage "DEV"
Then the UI displays inventory scoped to that tenant and stage within the performance target
```

#### SCN-014
Metadata:
- Story: T-002.2
- FR: FR-002
- AC: AC-002
- Type: No results UX
- Priority: P1

```gherkin
Given a search yields no results
When the operator submits the search
Then the UI displays a `no results` message and suggestions to broaden filters
```

#### SCN-015
Metadata:
- Story: T-002.2
- FR: FR-002
- AC: AC-002
- Type: Performance
- Priority: P1

```gherkin
Given a large dataset
When the operator runs a free-text search
Then matching results are returned within 2 seconds
```

#### SCN-016
Metadata:
- Story: T-002.2
- FR: FR-002
- AC: AC-002
- Type: Authorization
- Priority: P1

```gherkin
Given a restricted role user
When they attempt a Platform Engineer action
Then the UI disables the action and shows an authorization tooltip
```

### R-003.1 — RBAC Management: Backend APIs (FR-003)

#### SCN-017
Metadata:
- Story: R-003.1
- FR: FR-003
- AC: AC-001
- Type: Happy path
- Priority: P0

```gherkin
Given a Platform Engineer with Admin privileges
When they call `POST /rbac/assign` to assign `Operator` to `alice@example.com` for tenant "tenant-test-1"
Then the API returns `200 OK` and the assignment is persisted
And an audit entry is created for the assignment
```

#### SCN-018
Metadata:
- Story: R-003.1
- FR: FR-003
- AC: AC-001
- Type: Invalid group
- Priority: P1

```gherkin
Given a request references a non-existent Azure AD group
When the assignment API is called
Then the API returns `400 Bad Request` with validation details
```

#### SCN-019
Metadata:
- Story: R-003.1
- FR: FR-003
- AC: AC-001
- Type: Nested roles
- Priority: P1

```gherkin
Given nested role mappings exist
When a role evaluation runs for a principal
Then the API returns effective permissions including nested roles
```

#### SCN-020
Metadata:
- Story: R-003.1
- FR: FR-003
- AC: AC-001
- Type: Audit linkage
- Priority: P1

```gherkin
Given a successful role change
When the API persists the change
Then an audit record is written containing `actor`, `timestamp`, `action`, and `target`
```

### R-003.2 — RBAC Management: Frontend role mapping and history (FR-003)

#### SCN-021
Metadata:
- Story: R-003.2
- FR: FR-003
- AC: AC-001
- Type: Happy path
- Priority: P0

```gherkin
Given the Platform Engineer opens the RBAC UI for tenant "tenant-test-1"
When they view role mappings
Then the UI lists current assignments and provides an edit control per mapping
```

#### SCN-022
Metadata:
- Story: R-003.2
- FR: FR-003
- AC: AC-001
- Type: Validation error
- Priority: P1

```gherkin
Given the user submits an invalid mapping payload
When the UI sends the request
Then validation errors are shown and invalid fields highlighted
```

#### SCN-023
Metadata:
- Story: R-003.2
- FR: FR-003
- AC: AC-001
- Type: Authorization
- Priority: P1

```gherkin
Given a user without mapping privileges
When they attempt to edit a mapping
Then the UI prevents the edit and shows `Not authorized`
```

#### SCN-024
Metadata:
- Story: R-003.2
- FR: FR-003
- AC: AC-001
- Type: History paging
- Priority: P1

```gherkin
Given a long assignment history exists
When the auditor paginates through history
Then the UI returns pages and preserves sorting/filters
```

### O-004.1 — Operational Actions: Backend action endpoints (FR-004)

#### SCN-025
Metadata:
- Story: O-004.1
- FR: FR-004
- AC: AC-002
- Type: Short-op happy path
- Priority: P0

```gherkin
Given an authorized IT Operator
When they call `POST /actions/start-environment/run` for a short action
Then the API returns `200 OK` with a success result and an audit entry is written
```

#### SCN-026
Metadata:
- Story: O-004.1
- FR: FR-004
- AC: AC-002
- Type: Async submission (202)
- Priority: P0

```gherkin
Given a long-running action is invoked
When the client posts to `POST /actions/reprovision/run`
Then the API returns `202 Accepted` with `job_id` and `status_url`
```

#### SCN-027
Metadata:
- Story: O-004.1
- FR: FR-004
- AC: AC-002
- Type: Job lifecycle
- Priority: P1

```gherkin
Given a job is created with `job_id`
When the client polls `GET /jobs/{job_id}`
Then the job transitions through `pending`, `running`, and `succeeded` and final result is returned
```

#### SCN-028
Metadata:
- Story: O-004.1
- FR: FR-004
- AC: AC-002
- Type: Idempotency
- Priority: P1

```gherkin
Given a client retries the same action with the same `Idempotency-Key`
When the server receives the retry
Then the server returns the same result and does not create duplicate side-effects
```

### O-004.2 — Operational Actions: Frontend confirmations & job polling (FR-004)

#### SCN-029
Metadata:
- Story: O-004.2
- FR: FR-004
- AC: AC-002
- Type: UI happy path
- Priority: P0

```gherkin
Given an authorized user triggers a short action from the UI
When the UI submits and receives `200 OK`
Then the UI displays a success notification and refreshes resource status
```

#### SCN-030
Metadata:
- Story: O-004.2
- FR: FR-004
- AC: AC-002
- Type: Cancel job
- Priority: P1

```gherkin
Given a long-running job is `running`
When the user requests cancellation
Then the UI shows cancellation progress and the job transitions to `cancelled`
```

#### SCN-031
Metadata:
- Story: O-004.2
- FR: FR-004
- AC: AC-002
- Type: Progress UI
- Priority: P1

```gherkin
Given the status endpoint reports progress
When the UI polls the `status_url`
Then the UI displays incremental progress and updates until completion
```

#### SCN-032
Metadata:
- Story: O-004.2
- FR: FR-004
- AC: AC-002
- Type: Authorization
- Priority: P1

```gherkin
Given a user without action permission
When they attempt to trigger an action in the UI
Then the UI disables the control and shows `Not authorized`
```

### D-005.1 — Diagnostics Links: Backend probe & link generation (FR-005)

#### SCN-033
Metadata:
- Story: D-005.1
- FR: FR-005
- AC: AC-003
- Type: Happy path
- Priority: P0

```gherkin
Given diagnostic data exists for a resource
When the operator requests diagnostics link
Then the API returns a health status and a pre-populated Log Analytics URL
```

#### SCN-034
Metadata:
- Story: D-005.1
- FR: FR-005
- AC: AC-003
- Type: Link correctness
- Priority: P1

```gherkin
Given a diagnostics link is provided
When the operator clicks the link
Then Log Analytics opens with the correct subscription and resource context
```

#### SCN-035
Metadata:
- Story: D-005.1
- FR: FR-005
- AC: AC-003
- Type: Boundary (query size)
- Priority: P1

```gherkin
Given a very long query template
When the diagnostics link is generated
Then the system encodes or truncates the query per limits and returns a working link
```

#### SCN-036
Metadata:
- Story: D-005.1
- FR: FR-005
- AC: AC-003
- Type: Authorization
- Priority: P1

```gherkin
Given the user lacks telemetry-read privileges
When they request a diagnostics link
Then the API returns `403 Forbidden` and does not expose query parameters
```

### D-005.2 — Diagnostics UI: recent errors & traces (FR-005)

#### SCN-037
Metadata:
- Story: D-005.2
- FR: FR-005
- AC: AC-003
- Type: Happy path
- Priority: P0

```gherkin
Given recent errors exist for an environment
When the Support Engineer opens the diagnostics panel
Then the UI lists the most recent 50 events with timestamps and links to traces
```

#### SCN-038
Metadata:
- Story: D-005.2
- FR: FR-005
- AC: AC-003
- Type: Backend unavailable
- Priority: P1

```gherkin
Given the telemetry backend is temporarily unavailable
When the operator opens diagnostics
Then the UI shows an `unavailable` message and a retry option
```

#### SCN-039
Metadata:
- Story: D-005.2
- FR: FR-005
- AC: AC-003
- Type: Limit/pagination
- Priority: P1

```gherkin
Given the diagnostics panel is requested with `limit=50`
When more events exist
Then the UI displays the last 50 events and shows pagination controls
```

#### SCN-040
Metadata:
- Story: D-005.2
- FR: FR-005
- AC: AC-003
- Type: Authorization
- Priority: P1

```gherkin
Given a user without support privileges
When they open diagnostics
Then sensitive fields are masked and some links are hidden per policy
```

### A-006.1 — Audit & Change History: Backend append-only store (FR-006)

#### SCN-041
Metadata:
- Story: A-006.1
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Happy path
- Priority: P0

```gherkin
Given an authorized action is performed by "alice@example.com"
When the action completes
Then an immutable audit entry is written containing actor, timestamp, action, and resource
```

#### SCN-042
Metadata:
- Story: A-006.1
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Immutability negative
- Priority: P1

```gherkin
Given an existing audit entry
When a user attempts to modify it
Then the system rejects the modification and returns `403 Forbidden`
```

#### SCN-043
Metadata:
- Story: A-006.1
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Export masking
- Priority: P1

```gherkin
Given an auditor requests an export containing PII
When the export is generated
Then PII fields are masked per export privacy rules and masking summary is included
```

#### SCN-044
Metadata:
- Story: A-006.1
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Boundary (export size)
- Priority: P1

```gherkin
Given a request to export a very large audit range
When the export would exceed size limits
Then the API returns `413 Payload Too Large` or provides a paged export mechanism
```

### A-006.2 — Audit & Change History: Frontend timeline and export (FR-006)

#### SCN-045
Metadata:
- Story: A-006.2
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Happy path
- Priority: P0

```gherkin
Given multiple audit entries exist for an environment
When the auditor opens the audit timeline and filters by resource
Then the UI displays entries with actor, timestamp, and action details
```

#### SCN-046
Metadata:
- Story: A-006.2
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Authorization
- Priority: P1

```gherkin
Given a user without auditor privileges
When they attempt to access export functionality
Then the UI hides export controls and shows `Not authorized`
```

#### SCN-047
Metadata:
- Story: A-006.2
- FR: FR-006
- AC: AC-? (placeholder)
- Type: No-results negative
- Priority: P1

```gherkin
Given the auditor applies a filter that yields no results
When they run the filter
Then the UI displays `no entries found` and suggests widening the date range
```

#### SCN-048
Metadata:
- Story: A-006.2
- FR: FR-006
- AC: AC-? (placeholder)
- Type: Observability correlation
- Priority: P1

```gherkin
Given an end-to-end execution of a start action
When traces are sampled across services
Then observability traces include a correlation id and can be correlated from UI to backend services
```

## NFR Scenarios

### NFR-003 — Performance: Inventory list render within threshold
Metadata:
- Requirement: NFR-003
- Type: Performance
- Priority: P1

```gherkin
Given 2,000 environments exist for tenant "sample-1"
When an IT Operator opens the inventory list view
Then the UI renders within 2 seconds for the requested page
```

### NFR-001 — Security: Unauthorized requests blocked
Metadata:
- Requirement: NFR-001
- Type: Security
- Priority: P1

```gherkin
Given an unauthenticated request
When it attempts to access a protected Admin Portal endpoint
Then the API returns `401 Unauthorized` and no tenant data is exposed
```

### NFR-004 — Observability: Trace emission for actions
Metadata:
- Requirement: NFR-004
- Type: Observability
- Priority: P2

```gherkin
Given an IT Operator triggers a start action
When the action completes
Then an Application Insights trace is emitted with `action`, `resourceId`, `outcome`, and `durationMs`
```

### NFR-005 — Compliance: Audit export completeness
Metadata:
- Requirement: NFR-005
- Type: Compliance
- Priority: P2

```gherkin
Given an Auditor requests audit trail for tenant "sample-1" for the last 30 days
When the export is generated
Then the export includes timestamp, actor, action type, resource ID, outcome, and provenance metadata
```

## Open Questions

- AC-006 for `FR-006` (Audit) is not defined in the BRS — PO must confirm expected audit fields and exact AC ID to reference.
- Confirm default `pageSize` and max export sizes for CSV and diagnostic bundles.
- Confirm export privacy rules: masking/encryption requirements for exported audit/diagnostic data.
- Provide representative tenant IDs and subscription IDs for automated test fixtures (`tenant-test-1..3`, `sub-001..sub-003`).

## Evidence

- Link scenario IDs from `openspec/changes/*/proposal.md` `Acceptance Criteria` sections.

## Acceptance checklist

- [ ] Gate was triggered in `engineering-readiness/readiness-check.md`.
- [ ] All in-scope story IDs from `planning/delivery-structure.md` appear in the coverage summary (exact match).
- [ ] Every coverage summary row has a matching `#### SCN-NNN` metadata block and a ` ```gherkin` block.
- [ ] Each story has at least the required minimum scenarios (happy path + negative; async/RBAC/export stories have additional scenarios).
- [ ] Each scenario metadata includes Story ID (exact), FR-NNN or NFR-NNN, and AC-NNN (or placeholder) where applicable.
- [ ] NFR scenarios present for measurable NFRs and reference exact thresholds from BRS.
- [ ] All `When` steps contain a single action and `Then` steps are observable outcomes.
- [ ] Open questions recorded for missing ACs or ambiguous acceptance criteria.
- [ ] Coverage summary row count equals the number of `SCN-` blocks.

--

Self-review checklist: verify the above acceptance checklist before setting `Status: Accepted`.
