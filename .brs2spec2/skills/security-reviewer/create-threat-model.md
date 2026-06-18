# Skill — Create Threat Model

## Identity

| Field | Value |
|---|---|
| skill_id | sec-create-threat-model |
| persona | security-reviewer |
| event_types | CREATE_THREAT_MODEL |
| produces | quality-gates/threat-model.md |

## When this skill is used

After `CREATE_SECURITY_REVIEW` completes. Triggered when the security review identifies a significant attack surface that requires systematic threat enumeration — typically for initiatives that introduce new service boundaries, external API exposure, or sensitive data processing.

Not always triggered — only when the security review calls for it or when the architecture introduces new trust boundaries.

## Role for this task

You are a senior security architect performing a structured threat model using the STRIDE methodology — identifying threats per component boundary, rating them, and specifying mitigations.

## Prerequisites check

Before starting, verify:
- [ ] `quality-gates/security-review.md` exists
- [ ] `architecture/architecture-review.md` exists
- [ ] `input/architecture.md` is readable
- [ ] `input/brs.md` is readable

## Instructions

### Step 1 — Define trust boundaries

From the architecture review and architecture document, identify every trust boundary:
- User ↔ Application boundary
- Application ↔ Database boundary
- Application ↔ External system boundary
- Service ↔ Service boundary (internal)
- Admin ↔ Application boundary

### Step 2 — Enumerate threats per boundary using STRIDE

For each trust boundary, evaluate each STRIDE threat category:

**S — Spoofing**: can an attacker impersonate a legitimate entity at this boundary?
**T — Tampering**: can data be modified in transit or at rest at this boundary?
**R — Repudiation**: can an actor deny performing an action at this boundary?
**I — Information Disclosure**: can sensitive data leak at this boundary?
**D — Denial of Service**: can the service be made unavailable at this boundary?
**E — Elevation of Privilege**: can a lower-privileged entity gain higher privileges at this boundary?

### Step 3 — For each identified threat, document

1. **THR-NNN ID** — sequential
2. **Boundary** — where the threat applies
3. **STRIDE category** — S / T / R / I / D / E
4. **Threat description** — specific attack scenario
5. **DREAD score** — Damage (1-3) + Reproducibility (1-3) + Exploitability (1-3) + Affected users (1-3) + Discoverability (1-3) = total /15
6. **Risk level** — Critical (11-15) / High (7-10) / Medium (4-6) / Low (1-3)
7. **Existing mitigation** — what already protects against this threat
8. **Required mitigation** — what additional control is needed
9. **Owner** — who implements the mitigation
10. **Status** — Open / Mitigated / Accepted

### Step 4 — Write the artifact

The output must start with `## Metadata` and `| **Status** | **In progress** |`.

## Output requirements

The artifact must contain:
- Metadata table with Status, Initiative ID, creation date
- Trust boundary map (Mermaid `graph LR` or table)
- THR-NNN threat catalog: ID, Boundary, STRIDE, Threat, DREAD, Risk, Mitigation Required, Owner, Status
- Mitigation summary: all required mitigations with priority order
- Accepted threats: threats explicitly accepted with justification

## Done criteria

- [ ] Every identified trust boundary has been assessed for all 6 STRIDE categories
- [ ] Every threat has a DREAD score and risk level
- [ ] Required mitigations have owners
- [ ] Accepted threats have explicit justification
- [ ] `Status: In progress` in the Metadata table
- [ ] Result file written with `status: pass` and `artifacts_written` listing `quality-gates/threat-model.md`

## Stop conditions

- If the initiative has no new trust boundaries (very rare): produce the artifact with a statement confirming the assessment was performed and no new threats identified.
- Do not invent threats without a plausible attack scenario.
