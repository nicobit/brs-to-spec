# Open Questions — Decisions and Next Actions

Date: 2026-06-22
Source: automated decision proposals (recorded by agent)

This document records proposed answers for the active open questions (OQ-001..OQ-005), the chosen owner, rationale, and the next actionable step to make the decision authoritative.

---

OQ-001 — What is the approved AI model vendor / approach for risk scoring?

- Decision: Wave‑1 will use a third‑party managed scoring provider (example: Experian / PowerCurve or equivalent) to meet time‑to‑market and SLA needs. Wave‑2 will evaluate an in‑house/custom model migration.
- Owner: Head of AI
- Rationale: Third‑party provider reduces integration and validation time, provides proven SLAs and explainability metadata for regulatory needs.
- Requirements: vendor must expose explainability metadata, model version, and meet SLA p95 response ≤ 60s for scoring calls.
- Next action: Head of AI produces a one‑page vendor acceptance checklist (SLAs, explainability fields, security/data sharing terms) and records vendor selection (or a shortlist) in `initiatives/I093-I3/input/decisions/vendor-selection.md`.

---

OQ-002 — Does the cooling‑off period waiver require a separate legal sign‑off flow?

- Decision: No separate mandatory legal workflow for routine waivers. Product+Ops may allow waivers under defined thresholds; Legal must sign off on any exception that changes T&Cs or statutory rights.
- Owner: Legal (with Product)
- Rationale: Avoid heavy legal gating for low‑risk waivers while preserving legal oversight for exceptions that impact obligations.
- Next action: Legal publishes a waiver policy (thresholds + required approval steps). Document to be added under `initiatives/I093-I3/input/policies/waiver-policy.md`.

---

OQ-003 — What is the fallback for HMRC KYC API when unavailable — manual verification or auto‑refer?

- Decision: When HMRC is unavailable, do NOT auto‑approve. Mark application as `REFER_TO_UNDERWRITER` (or `COMPLIANCE_REVIEW`) and surface manual verification steps for Compliance.
- Owner: Compliance (ops)
- Rationale: Manual review preserves regulatory safety and prevents incorrect approvals when authoritative KYC is unavailable.
- Next action: Compliance defines a manual verification checklist and SLA for human review; add checklist to `initiatives/I093-I3/input/checklists/hmrc-kvc-fallback.md` and update stories that reference FR-013.

---

OQ-004 — What AML database providers beyond HM Treasury are required (Dow Jones, others)?

- Decision: Include HM Treasury sanctions list as primary, and add one commercial provider (e.g., Dow Jones / Refinitiv World‑Check) for broader coverage. Provider list must be configurable and adapters pluggable.
- Owner: Compliance + Procurement
- Rationale: Combining public and paid data sources improves screening coverage and reduces false negatives; procurement evaluates licensing and cost.
- Next action: Procurement and Compliance evaluate provider options and record approved provider(s) and API requirements in `initiatives/I093-I3/input/decisions/aml-provider-decision.md`.

---

OQ-005 — Is the T24 payment gateway contract already defined or does it need API negotiation?

- Decision: Assume no final contract exists. Implement an internal payment gateway API contract (v1) and negotiate Temenos/T24 specifics in parallel. Provide a T24 facade stub for dev/testing.
- Owner: IT Architecture / Integrations
- Rationale: Parallelise integration work so development can proceed with a stable facade while contractual negotiation completes.
- Next action: IT Architecture drafts the T24 integration contract (API schema + error semantics) and a stub harness for dev/testing; place artifacts under `initiatives/I093-I3/input/integrations/t24/`.

---

Recording notes
- These decisions are recorded as agent-proposed defaults to unblock planning and validation. They require sign‑off from the named owners to be authoritative. Owners should update repository input artifacts above to capture approvals and evidence.

If you want, I can: (A) create the specific decision files referenced above, (B) update `planning/fr-coverage.md` with explicit OQ-ID propagation (already attempted), or (C) raise a human approval gate entry under `.b2s/tmp/` (requires CLI). Choose one and I'll proceed.
