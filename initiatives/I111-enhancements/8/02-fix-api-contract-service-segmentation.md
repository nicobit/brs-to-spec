# Enhancement 8.2 — Service-Boundary Segmentation in API Contract Skill

## Problem

`create-api-contract.md` reads `architecture/architecture-review.md` as an input but
has no rule to extract service boundaries from it. It says "fill the Endpoints table
with every endpoint derived from the BRS and architecture" — which causes the skill to
produce one flat list, collapsing endpoints from all services together.

For I005, the Impacted Components table in `architecture-review.md` (after Enhancement
8.1) will have four rows where `Type = Service` and `Exposes HTTP API? = Yes`:
- Loan Origination API
- AI Scoring Service
- Compliance Service
- Payment Gateway Adapter

The skill produced endpoints for only the first of these. The other three were not
covered because there was no rule telling the skill to iterate across services.

Additionally, outbound calls to external systems (Experian, HMRC, T24, DocuSign) were
not distinguished from inbound API endpoints. They are different: inbound endpoints are
contracts this team owns and defines; outbound calls are dependencies on contracts owned
by third parties.

**Dependency on Enhancement 8.1:** this enhancement requires that
`architecture/architecture-review.md` has an `## Impacted Components` table with `Type`
and `Exposes HTTP API?` columns. If that table does not exist (pre-8.1 run), a fallback
applies (see Change 1).

---

## What needs to change

### Change 1 — Add service identification step as the first generation step

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md`,
Generation steps section.

**Replace current step 2:**
```
2. Read all inputs listed above
```

**With:**
```
2. Read all inputs listed above. Then immediately apply the service identification rule:

### Service identification rule — mandatory before writing any endpoint content

Read `architecture/architecture-review.md`. Find the `## Impacted Components` table.

Filter rows where **both** of the following are true:
- `Type` = `Service` (not Database, Queue, Frontend, Gateway, or External)
- `Exposes HTTP API?` = `Yes`

These are the **API-owning services**. You must produce one `### <Component Name>`
endpoint subsection in the Endpoints section for each matching row — even if you do not
yet know all its endpoints (see stub rule below).

Also collect rows where `Type` = `External` — these go in the `## Outbound Integrations`
section, not in the Endpoints table.

**Stub rule:** if a service is in the Impacted Components table but its endpoints cannot
yet be determined from the BRS or architecture inputs, add the subsection with a stub row:

| Method | Path | Purpose | Auth | Caller (ACT-NNN) |
|---|---|---|---|---|
| _(TBD)_ | _(TBD)_ | Endpoints not yet defined — see open decision [ID or "raise OD"] | — | — |

Do not silently omit a service from the Endpoints section because its endpoints are
not yet known. A stub is better than a gap.

**Fallback — if `## Impacted Components` table does not exist in `architecture-review.md`:**
- Note at the top of the Endpoints section:
  `> Impacted Components table not found in architecture-review.md. Endpoints derived
  > from BRS prose and architecture narrative. Re-run after Enhancement 8.1 is applied
  > for accurate service segmentation.`
- Then proceed with the current behaviour (derive from BRS prose). Do not stop.
```

---

### Change 2 — Restructure the Endpoints section output format

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md`,
Generation steps section, step 4.

**Replace current step 4:**
```
4. Complete every section from the template in order: Metadata, API Summary, Endpoints,
   Request/Response Contract, Error Handling, Versioning and Compatibility, Open Questions
```

**With:**
```
4. Complete every section from the template in order: Metadata, API Summary, Endpoints,
   Outbound Integrations, Request/Response Contract, Error Handling, Versioning and
   Compatibility, Open Questions.

**Endpoints section structure:**

When multiple API-owning services were identified in step 2, structure the Endpoints
section with one subsection per service:

```markdown
## Endpoints

### Loan Origination API

| Method | Path | Purpose | Auth | Caller (ACT-NNN) |
|---|---|---|---|---|
| POST | /applications | Submit loan application | Public — OTP | ACT-001 Applicant |
| GET | /applications/{arn} | Get application status | OTP-verified | ACT-001, ACT-002 |

### AI Scoring Service

| Method | Path | Purpose | Auth | Caller (ACT-NNN or SYS-NNN) |
|---|---|---|---|---|
| POST | /score | Trigger scoring job | Internal — managed identity | SYS-001 Loan Origination API |
| GET | /score/{job-id}/status | Poll job status | Internal — managed identity | SYS-001 |
| GET | /score/{job-id}/explainability | Get explainability trace | Internal — managed identity | SYS-001 |

### Compliance Service

...

### Payment Gateway Adapter

...
```

**Outbound Integrations section — always present when External rows exist:**

```markdown
## Outbound Integrations

These are APIs owned by third parties that this initiative calls. They are not contracts
this team defines — they are dependencies. Contract details and SLAs must be confirmed
with each vendor.

| Integration | Direction | Protocol | Auth | Notes |
|---|---|---|---|---|
| Experian CreditExpert | Outbound | REST/HTTPS | API key (enterprise contract) | Circuit breaker required; fallback: REFER_TO_UNDERWRITER |
| HMRC Identity Verification | Outbound | REST/HTTPS | OAuth2 | Fallback TBD — see OD-002 |
| HM Treasury Sanctions | Outbound | REST/HTTPS | API key | Additional providers TBD — see OD-003 |
| DocuSign eSignature | Outbound | REST/HTTPS | OAuth2 (enterprise contract) | E-signature for offer acceptance |
| Temenos T24 | Outbound | REST/HTTPS (via internal adapter) | Managed identity | Contract details TBD — see OD-004 |
```

**When only one API-owning service exists:** use the flat Endpoints table from the
template — no `###` subsections needed.
```

---

### Change 3 — Update quality bar

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md`,
Quality bar section.

**Add to the existing list:**

```markdown
- read `architecture/architecture-review.md` Impacted Components table before writing
  any endpoint content — never derive service count from prose alone when the table exists
- produce one `### <Service Name>` endpoint subsection per row where Type=Service and
  Exposes HTTP API?=Yes — never merge endpoints from different services into a single
  flat table when multiple services exist
- document outbound integrations (Type=External rows) in `## Outbound Integrations`,
  not in the Endpoints table
- include a stub row for any service whose endpoints are not yet determinable — never
  silently omit a service identified in the Impacted Components table
```

---

### Change 4 — Update anti-patterns

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md`,
Anti-patterns section.

**Add:**

```markdown
- producing a single flat Endpoints table when the Impacted Components table identifies
  multiple HTTP-exposing services — each service must have its own `###` subsection
- including outbound calls to external systems (Experian, HMRC, T24, DocuSign) in the
  Endpoints table — those are third-party dependencies documented in Outbound Integrations
- silently omitting a service from the Endpoints section because its endpoints are not
  yet defined — use a stub row and reference the open decision
- reading `input/architecture.md` to identify services when `architecture-review.md`
  has an Impacted Components table — always read the review, not the raw input
```

---

### Change 5 — Update self-review checklist

**Location:** `skills/4-engineering-readiness/quality-gates/create-api-contract.md`,
Self-review checklist.

**Add:**

```markdown
- [ ] `architecture/architecture-review.md` Impacted Components table was read before
  writing the Endpoints section (or fallback noted if table absent).
- [ ] Every row where Type=Service and Exposes HTTP API?=Yes has its own `###` subsection
  in the Endpoints section.
- [ ] No endpoint from one service appears in another service's subsection.
- [ ] All Type=External rows appear in `## Outbound Integrations`, not in Endpoints.
- [ ] Any service with unknown endpoints has a stub row and an open decision reference —
  not silently omitted.
```

---

## Implementation steps

1. Open `.brs2spec/skills/4-engineering-readiness/quality-gates/create-api-contract.md`.
2. Replace step 2 in the Generation steps section with the expanded service identification
   rule (Change 1).
3. Replace step 4 with the restructured Endpoints section format and Outbound Integrations
   section (Change 2).
4. Add four bullets to the Quality bar section (Change 3).
5. Add four bullets to the Anti-patterns section (Change 4).
6. Add five items to the self-review checklist (Change 5).

---

## Quality bar

After this change, running the API contract skill on I005 (after Enhancement 8.1 has
produced the Impacted Components table) yields:

```
## Endpoints

### Loan Origination API
| POST | /applications | Submit loan application | Public — OTP | ACT-001 |
| GET  | /applications/{arn} | Get status | OTP-verified | ACT-001, ACT-002 |
| POST | /applications/{arn}/actions/offer | Generate offer | Internal | SYS-002 |
| POST | /applications/{arn}/disburse | Trigger disbursement | Internal | SYS-002 |

### AI Scoring Service
| POST | /score | Trigger scoring | Internal — managed identity | SYS-001 |
| GET  | /score/{job-id}/status | Poll status | Internal | SYS-001 |
| GET  | /score/{job-id}/explainability | Get trace | Internal | SYS-001 |

### Compliance Service
| POST | /aml-check | Run AML screening | Internal | SYS-001 |
| POST | /kyc-verify | Run KYC check | Internal | SYS-001 |
| GET  | /kyc-verify/{id}/status | Poll KYC status | Internal | SYS-001 |

### Payment Gateway Adapter
| POST | /disburse | Send disbursement to T24 | Internal | SYS-001 |
| GET  | /disburse/{id}/status | Poll disbursement | Internal | SYS-001 |

## Outbound Integrations
| Experian CreditExpert | Outbound | REST/HTTPS | ... |
| HMRC Identity Verification | Outbound | REST/HTTPS | ... |
| HM Treasury Sanctions | Outbound | REST/HTTPS | ... |
| DocuSign | Outbound | REST/HTTPS | ... |
| Temenos T24 | Outbound | REST/HTTPS | ... |
```

Four service sections from one table read. No prose inference. No invented services.
Outbound calls cleanly separated from owned contracts.
