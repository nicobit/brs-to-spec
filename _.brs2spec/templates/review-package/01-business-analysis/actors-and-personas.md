# Actors and Personas

> **Consumer:** Business analysts, architects, QA, UX
> **Purpose:** Explicit catalog of every human and system actor who interacts with this initiative
> **Generated from:** `input/brs.md`, `business-intake/business-intake-summary.md`, `architecture/architecture-review.md`

## Metadata

| Field | Value |
|---|---|
| Initiative |  |
| Version |  |
| Last updated |  |

## Human actors

<!-- One row per human role that directly interacts with the system. -->
<!-- Derive from: BRS actors/roles section; user story "As a..." statements in delivery-structure.md. -->

| Actor ID | Name | Description | Goals | Permissions / access level |
|---|---|---|---|---|
| ACT-001 | | | | |

## System actors

<!-- External systems that send or receive data from this initiative. -->
<!-- Derive from: architecture-review.md integration points; BRS integration requirements. -->

| Actor ID | Name | System type | Direction | Protocol / interface |
|---|---|---|---|---|
| SYS-001 | | API / Queue / DB / File | Inbound / Outbound / Both | REST / gRPC / AMQP / etc. |

## Actor × feature matrix

<!-- Which features each actor is involved in. -->
<!-- Derive from: planning/delivery-structure.md features; cross-reference with actor goals above. -->

| Actor | Features involved | Primary or supporting? |
|---|---|---|
| ACT-001 | F-001, F-002 | Primary |

## Authorization boundaries

<!-- Role-based access summary: what each actor can and cannot do. -->
<!-- Derive from: BRS authorization rules; business-intake/business-rules.md BR-NNN rules where category = security. -->

| Actor | Can do | Cannot do | Rule source |
|---|---|---|---|
| ACT-001 | | | BR-NNN / BRS §N |
