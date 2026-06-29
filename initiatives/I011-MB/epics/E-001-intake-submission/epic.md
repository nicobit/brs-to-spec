# E-001 — Intake & Submission

## Metadata

| Field | Value |
|---|---|
| Epic ID | E-001 |
| Initiative ID | I011-MB |
| Wave | Wave 1 |
| Priority | Must |
| Increment | D1 |
| Created at | 2026-06-28 |
| Created by | delivery-lead |
| Status | Draft |

---

## Business Objective

Provide a reliable, low-friction applicant intake capability that collects required personal and financial information, issues an Application Reference Number (ARN), and triggers downstream scoring and observability events. Failure to deliver this epic prevents automated scoring and creates operational load for manual intake.

---

## Scope

**In scope:**
- Applicant Portal application submission form and status lookup (ARN flow)
- Intake API to receive and validate application payloads
- Confirmation email generation and ARN issuance
- Emitting submission observability events for scoring pipeline

**Out of scope:**
- Underwriter UI and decisioning workflows (covered in E-004)
- Offer generation and e-sign flows (covered in E-005)

---

## High-Level Acceptance Criteria

- AC-E-001: When an applicant submits a valid application, the system returns an ARN and confirmation email within 2 minutes (FR-003, FR-004).
- AC-E-002: Client- and server-side validation prevents incomplete submissions (FR-002).
- AC-E-003: Submissions trigger AI pre-screening within 60 seconds (FR-006) and emit observability events (FR-030).

---

## Source Traceability

| Source | Reference | Notes |
|---|---|---|
| BRS | FR-001 | Application submission fields and constraints |
| Requirement | FR-002 | Inline validation |
| Requirement | FR-003 | Application Reference Number |
| Requirement | FR-004 | Confirmation email |
| Requirement | FR-005 | Status retrieval |
| Requirement | FR-006 | Trigger AI pre-screening |
| Requirement | FR-030 | Observability events |
| NFR | NFR-001 | Intake form render within 2 seconds |
| NFR | NFR-003 | Support 500 concurrent submissions (scalability) |

---

## Impacted Systems

| System / Module | Change Type | Notes |
|---|---|---|
| Applicant Portal | Frontend / Changed | Form fields and submission flow; status lookup by ARN |
| Intake API (new) | New service | Validate, persist, emit events, return ARN |
| Email service | Integration | Send confirmation email within SLA |
| ExplainabilityStore / Scoring pipeline | Integration (event consumer) | Submission triggers scoring pipeline via events |

---

## Dependencies

| Dependency | Type | Blocking? | Notes |
|---|---|---|---|
| E-002 Scoring service | Epic | No | Scoring consumes submission events; intake must emit events correctly |
| Experian integration | External | No | Credit report used downstream; intake only triggers request via scoring |

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| High submission volume causing degraded intake performance | Medium | High | Rate-limit, autoscale intake API, load test to NFR-003 |
| Missing or ambiguous repository mapping for frontend builds | Medium | Medium | Resolve G-UI-001 and provide repository inventory before story generation |

---

## Foundation / Setup

Provision `nb-repo` intake service scaffold, configure CI pipeline for intake service, and add feature flag for new submission flow. Ensure UK-region storage and encryption per ARCH-C-001.

---

## Stories

| Story ID | Title | Layers | Priority | Increment | Readiness |
|---|---|---|---|---|---|
| S-001.1 | Implement Intake API POST /applications | Backend API | Must | D1 | Not Ready |
| S-001.2 | Applicant Portal: Application Form UI | Frontend | Must | D1 | Not Ready |
| S-001.3 | Confirmation Email & ARN display | Backend API | Must | D1 | Not Ready |
| S-001.4 | Status retrieval API and UI (/applications/status) | Backend API / Frontend | Must | D2 | Not Ready |
| S-001.5 | Infrastructure: Provision intake service and storage | Infrastructure | Must | D1 | Not Ready |
| S-001.6 | Integration: Experian / Email provider adapters | Integrations | Must | D1 | Not Ready |

---

## Advisory Reviews

*This section will be populated by advisory review personas if enabled.*

---
*Status: Draft — set to Accepted only after epic review gate.*
