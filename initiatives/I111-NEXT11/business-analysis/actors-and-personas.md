# Actors and Personas

## Actor Catalog

| ID | Actor | Description |
|---|---|---|
| ACT-001 | Applicant | End-customer who submits loan applications via the portal or mobile web |
| ACT-002 | Underwriter | Bank staff who reviews referred or large applications and makes final decisions |
| ACT-003 | Compliance | Compliance team members who review AML/KYC holds and regulatory issues |

## Personas

### Applicant (Persona A-Applicant)

- Typical goals: quickly submit an application, receive decision or next steps, sign offers.
- Tech profile: desktop and mobile web users, moderate digital literacy.
- Acceptance criteria: clear error messages, ARN provided, decision timeline communicated.

### Underwriter (Persona U-Underwriter)

- Typical goals: review flagged applications, make decisions with supporting evidence, record rationale.
- Tech profile: internal web app users, needs fast access to credit and AI explanations.
- Acceptance criteria: actionable queues, audit trail of actions, AI explanation available.

### Compliance Officer (Persona C-Compliance)

- Typical goals: investigate AML/KYC holds, approve or escalate compliance cases, ensure regulatory controls.
- Tech profile: internal tools with access to full application snapshots.
- Acceptance criteria: immutable audit logs, reproducible decision evidence, data access controls.
