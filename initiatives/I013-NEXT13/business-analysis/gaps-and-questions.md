# Gaps and Questions

## Metadata

| Field | Value |
|---|---|
| Initiative ID | I013-NEXT13 |
| Created at | 2026-06-16 |
| Created by | product-owner |
| Status | Draft |

## Gap Catalog

| GAP-NNN | Category | Description | Impact | Severity | Suggested Resolution | Owner | BRS Source |
|---|---|---|---|---|---|---|---|
| GAP-001 | Missing specification / Integration | The T24 payment gateway API contract is not concretely defined (payload, retries, error semantics). | Delivery teams may block on integration details and timeline. | Blocking | Negotiate or publish the internal payment gateway contract; provide API schema and error semantics. | IT Architecture | input/brs.md / input/architecture.md |
| GAP-002 | Documentation / Architecture | Architecture notes are draft and pending architect review; some component responsibilities and deployment constraints need confirmation. | Minor scheduling risk and potential design rework if assumptions change. | Medium | Conduct architecture review and explicitly record decisions and owners. | Architect / Delivery Lead | input/architecture.md |

## Critical Path

### Blocking Gaps

| GAP-NNN | Description | Impact | Owner |
|---|---|---|---|
| GAP-001 | T24 payment gateway contract incomplete | Blocks Payment Gateway Adapter design and D3 scope | IT Architecture |

### High-Severity Gaps

| GAP-NNN | Description | Default Assumption (if proceeding) | Owner |
|---|---|---|---|

### Low-Severity Gaps

| GAP-NNN | Description | Assumption | Risk if assumption is wrong |
|---|---|---|---|
| GAP-002 | Architecture draft pending review | Assume proposed component responsibilities and Azure UK region deployment will be accepted | Possible design and schedule adjustments after review |

## Coverage Summary

| Category | Count |
|---|---|
| Blocking gaps | 1 |
| High-severity gaps | 0 |
| Low-severity gaps | 1 |
| Total gaps | 2 |

---

*Blocking gaps must be resolved or explicitly accepted with assumptions before downstream planning can proceed.*
