# Data Spec — {{F-XXX.X}}: {{User Story Name}}

> Distilled from `quality-gates/data-contract.md` for this user story only.
> Only tables created or modified by this story appear here.
> Full schema DDL, retention schedule, and Legal sign-off are in `quality-gates/data-contract.md`.
> Delete this file if this story has no schema changes.

## {{table_name}} — {{created | modified}}

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|

Indexes:
<!-- list indexes relevant to this story and their purpose -->

Constraints:
<!-- FK, unique, check constraints introduced by this story -->

Migration notes:
<!-- zero-downtime approach if altering an existing table; "new table" if creating -->

---

## PII handling (this story)

| Field | Table | Sensitivity | Control | Do not... |
|---|---|---|---|---|

<!-- Only fields touched by this story. -->
