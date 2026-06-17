# Actors and Personas

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by | product-owner |
| Status | Draft |

## Human Actors (ACT-NNN)

| ACT-NNN | Name | Description | Primary Goal | Permissions | Restrictions | BRS Source |
|---|---|---|---|---|---|---|
| ACT-001 | Name from use-cases.puml | Role description | Primary goal in this initiative | What they can do | What they cannot do | FR-NNN / UC-NNN |

One row per human actor. Name must match the actor label used in `use-cases.puml`.

## Systems (SYS-NNN)

| SYS-NNN | Name | Type | Description | Integration | BRS Source |
|---|---|---|---|---|---|
| SYS-001 | System name | External / Internal Automated | What this system does | API / event / batch | FR-NNN / BRS section |

## Interaction Matrix

| Actor | Initiates | Reads | Modifies | Approves / Rejects | Receives |
|---|---|---|---|---|---|
| ACT-001 / SYS-001 | UC-NNN list | Artifact or data | Artifact or data | UC-NNN list | Notifications or outputs |

---
*Set Status: Accepted only by workflow or human approval when applicable. Never self-accept.*
