# Delivery Skeleton

Overview:

- High-level waves and milestones to support initial planning and epic assignment.

Waves:

- Wave 1 — Intake & Verification (0-4 weeks): EPIC-001, EPIC-003
- Wave 2 — Decisioning & Underwriting (3-8 weeks): EPIC-002
- Wave 3 — Disbursement & Settlement (6-12 weeks): EPIC-004
- Wave 4 — Observability & Ops (1-12 weeks): EPIC-005 (ongoing)

Milestones:

- M1 — Migrate intake form to staging and enable ARN assignment
- M2 — Integrate Experian and HMRC checks in sandbox
- M3 — Deploy AI scoring to staging
- M4 — End-to-end acceptance and disbursement smoke tests

Repository mapping guidance:

- Map EPIC-001 to `repo/application-intake` (frontend + API)
- Map EPIC-002 to `repo/decisioning` (AI & orchestration)
- Map EPIC-003 to `repo/compliance` (integrations)
- Map EPIC-004 to `repo/disbursement` (payments)
- Map EPIC-005 to `repo/observability` (logging/metrics)
