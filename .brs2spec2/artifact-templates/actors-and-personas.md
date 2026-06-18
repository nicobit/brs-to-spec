# Actors and Personas

## Metadata

| Field | Value |
|---|---|
| Initiative ID | {{initiative_id}} |
| Created at | {{date}} |
| Created by event | {{event_id}} |
| Status | Draft |

## Human Actors (ACT-NNN)

| ACT-NNN | Name | Description | Primary Goal | Permissions | Restrictions | BRS Source |
|---|---|---|---|---|---|---|
| {{ACT-NNN}} | {{Name from use-cases.puml}} | {{role description}} | {{primary goal in this initiative}} | {{what they can do}} | {{what they cannot do}} | {{FR-NNN / UC-NNN}} |

One row per human actor. Name must match exactly the actor label used in use-cases.puml.

## Systems (SYS-NNN)

| SYS-NNN | Name | Type | Description | Integration | BRS Source |
|---|---|---|---|---|---|
| {{SYS-NNN}} | {{System name from BRS}} | {{External / Internal Automated}} | {{what this system does}} | {{API / event / batch}} | {{FR-NNN / §Section}} |

One row per external or automated system referenced in requirements.md.

## Interaction Matrix

| Actor | Initiates | Reads | Modifies | Approves / Rejects | Receives |
|---|---|---|---|---|---|
| {{ACT-NNN / SYS-NNN}} | {{UC-NNN list}} | {{artifact or data}} | {{artifact or data}} | {{UC-NNN list}} | {{notifications or outputs}} |

---
*Set Status: Accepted after review. Do not self-accept.*
