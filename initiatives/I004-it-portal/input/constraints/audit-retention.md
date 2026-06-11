# Audit Retention & Storage — Questionnaire (scaffold)

Security / Compliance: use this file to record the audit retention policy and technical constraints required for the append-only audit store.

Questions:

1. Default retention period for audit records (suggested default: 1 year). Are there regulatory requirements requiring longer retention?
2. Is WORM / append-only storage required? If yes, which storage technologies are acceptable (e.g., Azure Blob immutability policy, CosmosDB with immutability pattern)?
3. Access control: who can read/export audit records and under what conditions?
4. Export format and frequency for compliance requests.
5. Encryption at rest and key management expectations.
6. Any location / data residency constraints for audit records.

Owner: Security / Compliance (TBD)
