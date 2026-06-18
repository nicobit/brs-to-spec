# Software Modules

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I111-NEXT11 |
| Created at | 2026-06-18 |
| Created by | Delivery Lead |
| Status | Draft |

## Module Catalog

| MOD-NNN | Name | Type | Responsibility | Technology | Team |
|---|---|---|---|---|---|
| MOD-001 | Intake API | New | Application intake, validation, ARN assignment | Node.js / Express | Product Engineering |
| MOD-002 | AI Scoring Service | New | Model scoring, explainability payload | Python / FastAPI | AI Platform |
| MOD-003 | Integrations Layer | New | Connectors for Experian, HMRC, DocuSign, Temenos | Java / Spring Boot | Integrations Team |

## Module Boundaries

| Module Pair | Contract Type | Owner | Sync/Async | Notes |
|---|---|---|---|---|
| MOD-001 <-> MOD-002 | API | Product Engineering / AI Platform | Async | Scoring via event-driven request/response with correlation ID |
| MOD-001 <-> MOD-003 | API | Product Engineering / Integrations | Sync | Integrations layer abstracts external provider retries and circuit breakers |

## Functional Area Mapping

| Functional Area | Primary Module | Supporting Modules | Source |
|---|---|---|---|
| Application Intake | MOD-001 | MOD-003 | delivery-structure / architecture-review |
| AI Scoring | MOD-002 | MOD-001, MOD-003 | architecture-review |

## Ownership and Dependencies

| Module | Team / Domain | Cross-Team Dependencies | Risk |
|---|---|---|---|
| MOD-001 | Product Engineering | MOD-002, MOD-003 | Medium |
| MOD-002 | AI Platform | MOD-001, Data Platform | High |

---
*Set Status: Draft.*
