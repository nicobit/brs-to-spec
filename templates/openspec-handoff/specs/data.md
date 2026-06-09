# Data Spec — {{Deliverable ID}}: {{Deliverable Name}}

> Distilled from `quality-gates/data-contract.md` for this increment only.
> Full schema DDL, retention schedule, and Legal sign-off are in the source gate artifact.

## Tables created or modified in this increment

### {{table_name}}

| Column | Type | PII | Encrypted | Notes |
|---|---|---|---|---|

Indexes:
<!-- list indexes and rationale -->

Constraints:
<!-- FK, unique, check constraints -->

Migration notes:
<!-- zero-downtime migration approach if altering an existing table -->

---

## PII handling

| Field | Table | Sensitivity | Control | Do not... |
|---|---|---|---|---|

Encryption: <!-- key management approach, e.g. Azure Key Vault field-level for email/phone -->
Logging: <!-- which fields must never appear in logs or traces -->

## Residency

| Requirement | Value |
|---|---|
| Primary region | |
| Backup region | |
| Regulatory basis | |

## Retention (this increment)

| Data type | Retention | Deletion mechanism |
|---|---|---|

## Subject access / deletion

<!-- How DELETE /profiles/{id} works — soft-delete, purge schedule, export endpoint -->
