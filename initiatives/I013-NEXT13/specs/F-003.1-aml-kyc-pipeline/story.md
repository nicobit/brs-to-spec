# F-003.1 — AML Screening and KYC Verification

## Metadata

| Field | Value |
|---|---|
| Story ID | F-003.1 |
| Epic | E-003 — Compliance Screening |
| Feature | F-003 — AML / KYC Pipeline |
| Priority | Must |
| Increment | D1 |
| AC references | AC-007 |
| FR references | FR-012, FR-013 |

## 1. User Story

As the **System**,
I want to run AML screening and KYC verification before any offer is generated,
so that NEXT13 complies with UK anti-money laundering regulations and FCA requirements before committing to a lending decision.

### Business Goal

AML and KYC checks are non-negotiable regulatory requirements for UK regulated lending. An offer generated before AML/KYC clearance would constitute a regulatory breach and expose NEXT13 to FCA enforcement and financial penalties. This story gates the offer generation pipeline behind compliance screening.

### Scope

**In scope:**
- AML screening via HMRC/HM Treasury AML provider
- KYC identity verification
- Gate logic: no offer generated until both checks pass
- On AML match or KYC failure: set `COMPLIANCE_HOLD` and route to compliance queue
- Emitting `compliance.screening.completed` audit event with check results

**Out of scope:**
- Offer generation (E-005)
- Compliance officer review UI (F-003.2 handles the hold and routing)
- DocuSign document signing

## 2. Source Traceability

| Source Type | Reference | Description |
|---|---|---|
| Requirement | FR-012 | System shall perform AML screening before offer generation |
| Requirement | FR-013 | System shall perform KYC identity verification before offer generation |
| Architecture Constraint | ARCH-C-001 | PII must remain in UK; AML/KYC providers must be UK-compliant |
| Architecture Constraint | ARCH-C-004 | Compliance check results must be stored in immutable audit log |

## 3. Business Rules Applied

| Rule ID | Rule | Impact on This Story |
|---|---|---|
| BR-015 | AML and KYC checks must both pass before offer generation | Gate logic: offer pipeline blocked until both return CLEAR |
| BR-016 | AML MATCH or KYC FAIL sets COMPLIANCE_HOLD; human review required | Any non-CLEAR result must trigger COMPLIANCE_HOLD and routing to F-003.2 |
| BR-017 | AML/KYC results must not be stored in modifiable storage | Results go to immutable audit store only; application stores only the hold status |

## 4. Acceptance Criteria

### AC-007 — AML and KYC checks executed before offer generation

**Given** an application has a Scored recommendation of Approve
**When** the compliance pipeline processes the application
**Then** AML screening is executed first
**And** KYC verification is executed after AML returns CLEAR
**And** if both return CLEAR, the application status advances to `Compliant`
**And** a `compliance.screening.completed` event is emitted with both check results and ARN
**And** the offer generation pipeline is unblocked

Traceability:
- Requirements: FR-012, FR-013
- Business Rules: BR-015, BR-016, BR-017
- BDD Scenario: SCN-F003-001

### AC-008 — AML match sets COMPLIANCE_HOLD

**Given** AML screening returns a MATCH for the applicant
**When** the compliance pipeline processes the result
**Then** the application status is set to `COMPLIANCE_HOLD`
**And** the application is routed to the compliance officer queue (F-003.2)
**And** the offer generation pipeline is blocked for this application

## 5. BDD Scenarios

```gherkin
# F-003.1 — AML Screening and KYC Verification
# AC-007 — Both checks clear before offer

Feature: AML and KYC compliance screening before offer generation

  Scenario: AML CLEAR and KYC PASS — application advances to Compliant
    Given application "NEXT-20260617-000001" has recommendation "Approve"
    And AML screening returns "CLEAR" for the applicant
    And KYC verification returns "PASS" for the applicant
    When the compliance pipeline completes
    Then the application status is set to "Compliant"
    And a "compliance.screening.completed" event is emitted with both check results
    And the offer generation pipeline is unblocked for this application

  Scenario: AML MATCH blocks offer and sets COMPLIANCE_HOLD
    Given application "NEXT-20260617-000002" has recommendation "Approve"
    And AML screening returns "MATCH" for the applicant
    When the compliance pipeline processes the AML result
    Then the application status is set to "COMPLIANCE_HOLD"
    And the application is enqueued in the compliance officer queue
    And the offer generation pipeline is blocked for this application
    And KYC verification is NOT executed

  Scenario: KYC FAIL after AML CLEAR sets COMPLIANCE_HOLD
    Given application "NEXT-20260617-000003" has recommendation "Approve"
    And AML screening returns "CLEAR"
    And KYC verification returns "FAIL"
    When the compliance pipeline processes the KYC result
    Then the application status is set to "COMPLIANCE_HOLD"
    And the application is enqueued in the compliance officer queue
    And the offer generation pipeline is blocked for this application

  Scenario: AML provider unavailable — conservative COMPLIANCE_HOLD
    Given the HMRC AML provider returns HTTP 503
    When the compliance pipeline attempts AML screening
    Then the application status is set to "COMPLIANCE_HOLD"
    And a "compliance.aml.provider_unavailable" alert event is emitted
    And the application is routed to compliance queue for manual review

  Scenario: Authorization — only System role can trigger compliance screening
    Given a request to run compliance screening arrives with an Underwriter token
    When the compliance pipeline checks the caller role
    Then the request is rejected with HTTP 403
    And no compliance check is executed
```

## 6. Implementation Context

### Impacted Components

| Component | Type | Expected Change |
|---|---|---|
| Compliance Screening Pipeline | Worker | New compliance worker consuming scored Approve applications |
| HMRC/AML Provider Client | External Integration | New `aml_client.py` wrapping HMRC AML API |
| KYC Verification Client | External Integration | New `kyc_client.py` wrapping KYC provider API |
| Application Database | PostgreSQL | Status: Scored → Compliant or COMPLIANCE_HOLD |
| Compliance Officer Queue | Message Queue | Receives COMPLIANCE_HOLD applications with reason |
| Immutable Audit Store | Event log | Stores compliance.screening.completed with full check results |

### Data Impact

No compliance check results stored on application record (BR-017). Only status (`Compliant` or `COMPLIANCE_HOLD`) and `compliance_hold_reason` (varchar, nullable) stored on application.

All detailed check results go to immutable audit store only.

### API Impact

AML and KYC providers are external. HMRC AML endpoint per government integration contract. KYC provider per ARCH-C-003 enterprise procurement.

## 7. Constraints

The coding agent must respect these constraints without exception:

- AML must execute before KYC — sequential, not parallel (regulatory requirement: AML match short-circuits)
- Any non-CLEAR/PASS result from either check must produce COMPLIANCE_HOLD — no exceptions
- Do not store AML or KYC results on the applications table — immutable audit store only (BR-017)
- Provider unavailability must also produce COMPLIANCE_HOLD (conservative default — do not approve on error)
- All PII transmitted to AML/KYC providers must be minimised (ARCH-C-001)
- Audit event must be emitted for every check outcome (CLEAR, MATCH, PASS, FAIL, error)

## 8. Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| F-002.2 — Scoring Result | Story | Yes | Compliance runs only for Approve recommendations |
| HMRC AML Provider | External | Yes | API credentials and endpoint required |
| KYC Provider | External | Yes | API credentials and endpoint required |
| F-003.2 — COMPLIANCE_HOLD Routing | Story | No | Consumer of compliance queue; can be stubbed |
| Immutable Audit Store | Platform | Yes | Must be available for check result events |

## 9. Implementation Tasks

| Task ID | Task | Area | Depends On | Validation |
|---|---|---|---|---|
| T-001 | Implement `AMLClient` wrapping HMRC AML API with retry and timeout | Integration | HMRC API creds | Unit test: CLEAR, MATCH, and provider error paths |
| T-002 | Implement `KYCClient` wrapping KYC provider API with retry and timeout | Integration | KYC API creds | Unit test: PASS, FAIL, and provider error paths |
| T-003 | Implement compliance pipeline worker: AML first, then KYC if CLEAR | Worker | T-001, T-002 | Integration test: CLEAR+PASS → Compliant; MATCH → COMPLIANCE_HOLD |
| T-004 | Implement COMPLIANCE_HOLD routing: update status + enqueue to compliance queue | Worker | T-003 | Test: compliance queue receives message with ARN and reason |
| T-005 | Emit `compliance.screening.completed` to immutable audit store | Worker | T-003 | Audit event contains ARN, AML result, KYC result, timestamp |
| T-006 | Provider unavailability → conservative COMPLIANCE_HOLD + alert event | Worker | T-001, T-002 | Test: mocked 503 → COMPLIANCE_HOLD + alert event |

## 10. Test Expectations

- [ ] Unit: AML client — CLEAR, MATCH, provider error (503) paths
- [ ] Unit: KYC client — PASS, FAIL, provider error paths
- [ ] Unit: AML match short-circuits — KYC not called when AML returns MATCH
- [ ] Unit: Provider error → conservative COMPLIANCE_HOLD (not Compliant)
- [ ] Integration: CLEAR + PASS → status = Compliant → offer pipeline unblocked
- [ ] Integration: MATCH → COMPLIANCE_HOLD → compliance queue message sent
- [ ] Integration: KYC FAIL after CLEAR → COMPLIANCE_HOLD → compliance queue message sent
- [ ] Audit: compliance.screening.completed event emitted for every outcome
- [ ] Security: AML/KYC API keys not in logs; PII minimised in outbound requests

## 11. Definition of Done

This story is complete only when:
- [ ] All acceptance criteria (AC-007, AC-008) are implemented and verifiable
- [ ] All BDD scenarios are covered by automated tests
- [ ] AML-before-KYC sequencing enforced (test proves KYC not called on AML MATCH)
- [ ] Conservative COMPLIANCE_HOLD on provider errors verified
- [ ] No compliance results stored on applications table (audit store only)
- [ ] Traceability matrix updated: FR-012, FR-013 → F-003.1
- [ ] All architecture constraints (ARCH-C-001, ARCH-C-004) respected
- [ ] Coding prompt reviewed and signed off by lead engineer

## 12. Coding-Agent Prompt

```
Story: F-003.1 — AML Screening and KYC Verification
Initiative: I013-NEXT13 (UK Regulated Personal Lending Origination)

Goal:
Implement the compliance screening pipeline for NEXT13. For every Approve-recommended
application: run AML screening first (HMRC AML provider). If CLEAR: run KYC verification.
If both CLEAR/PASS: set status Compliant, unblock offer pipeline. If AML MATCH, KYC FAIL,
or provider error: set COMPLIANCE_HOLD, route to compliance queue, block offer pipeline.
Emit compliance.screening.completed to immutable audit store.

Files / components likely impacted:
- src/integrations/aml_client.py — new HMRC AML API client
- src/integrations/kyc_client.py — new KYC provider client
- src/workers/compliance_worker.py — new compliance pipeline worker
- src/events/schemas.py — ComplianceScreeningCompletedEvent
- tests/integrations/test_aml_client.py — new test file
- tests/integrations/test_kyc_client.py — new test file
- tests/workers/test_compliance_worker.py — new test file

Constraints (must not be violated):
- AML executes BEFORE KYC. If AML returns MATCH: set COMPLIANCE_HOLD immediately,
  do NOT call KYC. AML MATCH short-circuits (BR-016).
- Any non-CLEAR/PASS outcome, including provider errors, must produce COMPLIANCE_HOLD.
  Do not approve on uncertainty — conservative default (BR-016).
- Do NOT store AML or KYC results on the applications table. Only status and
  compliance_hold_reason on the application. Detailed results go to immutable audit store only (BR-017).
- PII minimisation: send only minimum required fields to AML/KYC providers (ARCH-C-001).
- API keys for AML and KYC providers must never appear in logs or error messages.

Expected implementation steps:
1. AMLClient: POST to HMRC_AML_ENDPOINT; 5s timeout; 3 retries on 5xx.
   Returns: "CLEAR" | "MATCH" | raises AMLProviderError on persistent failure.
2. KYCClient: POST to KYC_PROVIDER_ENDPOINT; 5s timeout; 3 retries on 5xx.
   Returns: "PASS" | "FAIL" | raises KYCProviderError on persistent failure.
3. Compliance Worker for each Approve application:
   a. Call AMLClient. If MATCH or AMLProviderError: COMPLIANCE_HOLD("AML_MATCH" or "AML_UNAVAILABLE").
   b. If CLEAR: call KYCClient. If FAIL or KYCProviderError: COMPLIANCE_HOLD("KYC_FAIL" or "KYC_UNAVAILABLE").
   c. If both CLEAR/PASS: set status = Compliant; emit compliance.screening.completed.
4. COMPLIANCE_HOLD path: set status = COMPLIANCE_HOLD; set compliance_hold_reason; enqueue to compliance queue.
5. Emit compliance.screening.completed event for every outcome (success or hold).

Tests to add:
- Unit aml_client: CLEAR, MATCH, HTTP 503 after 3 retries → AMLProviderError
- Unit kyc_client: PASS, FAIL, HTTP 503 after 3 retries → KYCProviderError
- Unit compliance_worker: AML MATCH → KYC not called; COMPLIANCE_HOLD set
- Unit compliance_worker: AML CLEAR + KYC FAIL → COMPLIANCE_HOLD
- Unit compliance_worker: AMLProviderError → conservative COMPLIANCE_HOLD
- Integration: CLEAR + PASS → status Compliant
- Integration: MATCH → status COMPLIANCE_HOLD + compliance queue message
- Audit: compliance.screening.completed event for all outcomes

What NOT to change:
- Scoring thresholds or ML inference (F-002.2 owns those)
- Offer generation pipeline (E-005 owns that)
- Compliance officer review UI (F-003.2 owns that)

Validation checklist before marking complete:
- [ ] AML-before-KYC sequencing: KYC not called on AML MATCH
- [ ] Provider error → conservative COMPLIANCE_HOLD
- [ ] No AML/KYC results stored on applications table
- [ ] compliance.screening.completed event emitted for all outcomes
- [ ] Compliance queue receives message on COMPLIANCE_HOLD
- [ ] API keys not in logs
- [ ] All unit and integration tests pass
```

---
*Status: Draft — set to Accepted only after human review.*
