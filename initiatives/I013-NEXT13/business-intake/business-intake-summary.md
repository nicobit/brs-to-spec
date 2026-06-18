# Business Intake Summary

> Produced by: product-owner
> Primary consumer: Product Owner, business analyst, delivery lead
> Purpose: confirm business scope, intent, gaps, and reviewable boundaries before architecture and planning
> Downstream use: architecture review, delivery planning, readiness
> Do not include: implementation tasks or detailed engineering design
> Keep concise, business-facing, and decision-oriented.

## Metadata

| Field | Value |
|---|---|
| Initiative | I013-NEXT13 - AI-Powered Loan Origination Platform |
| Version | 1.0 |
| Status | Draft |
| Created at | 2026-06-16 |
| Created by | product-owner |

## Executive Summary

| Field | Summary |
|---|---|
| Initiative | AI-Powered Loan Origination Platform |
| Business objective | Replace the bank's manual personal-loan process with an AI-assisted, auditable digital platform that delivers faster, more consistent, and compliant decisions. |
| Why now | The current process is slow, inconsistent, and weak on auditability while fintech competitors already offer faster digital-first lending journeys. |
| Main outcome expected | Straight-through eligible applications should reach a decision within 30 minutes while preserving human oversight for complex and compliance-sensitive cases. |
| Primary risk or constraint | The initiative is constrained by FCA, AML, KYC, GDPR, UK-only data residency, explainable AI requirements, and several external and internal integrations. |

## Source Document Inventory

| Source | Type | Coverage / purpose | Owner | Notes |
|---|---|---|---|---|
| input/brs.md | Business Requirements Specification | Primary source for objectives, scope, FRs, NFRs, constraints, and answered open questions | Head of Retail Lending | Main business source; includes 5 objectives, 30 FRs, 7 NFRs, and 5 answered open questions |
| input/architecture.md | High-level architecture note | Proposed deployment topology, components, integrations, data architecture, and security model | Architect review pending | Used as supporting brownfield and delivery context, not as the primary source of business requirements |
| routing/routing-decision.md | Routing decision | Selected delivery and execution modes plus required next actions | orchestrator | Confirms OpenSpec plus Enterprise+Modular path |

## Objectives

| Objective ID | Objective | Success measure | Source reference |
|---|---|---|---|
| OBJ-001 | Reduce average decision time for straight-through cases from 5-10 days to under 30 minutes. | At least 70% of applications reach a decision in 30 minutes or less. | input/brs.md |
| OBJ-002 | Improve consistency of underwriter outcomes. | Variance in approval rate across underwriters is reduced by at least 50%. | input/brs.md |
| OBJ-003 | Achieve a full regulatory audit trail for every loan decision. | 100% of decisions have an immutable audit trail within 24 hours of go-live. | input/brs.md |
| OBJ-004 | Comply with AML, KYC, and GDPR requirements throughout the process. | Zero regulatory findings in the first post-launch compliance audit. | input/brs.md |
| OBJ-005 | Enable an end-to-end digital journey for eligible applicants. | At least 60% of approved loans are disbursed without human intervention. | input/brs.md |

## Scope

| Area | In scope | Out of scope | Source reference |
|---|---|---|---|
| Loan products | Personal loans from 1,000 to 50,000 with 12-84 month terms | Mortgages and business loans | input/brs.md |
| Application intake | Online application submission, validation, ARN generation, confirmation, and status retrieval | Paper or email-based submission continuation | input/brs.md |
| Decisioning | AI pre-screening, risk scoring, straight-through decisions, and referral logic | Black-box AI decisioning approaches | input/brs.md |
| Compliance | AML screening, KYC verification, compliance hold handling, and related notifications | Additional AML providers beyond HM Treasury at this stage | input/brs.md |
| Human review | Underwriter queue, dashboard, approvals, declines, and requests for more information | Fully removing underwriter oversight for complex or borderline cases | input/brs.md |
| Offer lifecycle | Loan offer generation, portal and email presentation, e-signature acceptance, and cooling-off communications | Separate legal sign-off flow for cooling-off waiver | input/brs.md |
| Disbursement | Disbursement trigger, payment payload, confirmation handling, retry, and operations alerting | Direct debit setup in this phase | input/brs.md |
| Experience surfaces | Applicant self-service portal, underwriter dashboard, and admin dashboard | Mobile native app in this phase | input/brs.md |
| Platform controls | Observability, immutable audit logging, and operational reporting | Savings or current account products | input/brs.md |

## Requirements

| Requirement ID | Summary | Business value | Source reference | Acceptance / validation reference |
|---|---|---|---|---|
| FR-001 | Allow applicants to submit a personal loan application online with required identity, employment, income, amount, purpose, and term fields. | Creates the digital front door and removes manual intake dependency. | input/brs.md | Submission form captures all mandatory fields and blocks missing data. |
| FR-002 | Validate mandatory fields inline before submission and block incomplete applications. | Improves data quality and reduces avoidable underwriting rework. | input/brs.md | Invalid or incomplete submissions show inline errors and cannot be submitted. |
| FR-003 | Assign and display a unique Application Reference Number immediately after submission. | Enables traceability and self-service tracking for applicants and staff. | input/brs.md | Every submitted application receives a unique ARN shown to the applicant. |
| FR-004 | Send an email confirmation within 2 minutes of submission including ARN and estimated decision timeline. | Provides reassurance and reduces inbound status queries. | input/brs.md | Confirmation email is sent within the stated SLA. |
| FR-005 | Allow applicants to retrieve application status using ARN and date of birth without account registration. | Supports low-friction self-service and lowers service-center load. | input/brs.md | Status lookup works with ARN plus DOB and does not require account creation. |
| FR-006 | Trigger AI pre-screening within 60 seconds of submission. | Speeds up the decisioning pipeline and supports fast straight-through processing. | input/brs.md | AI assessment starts within 60 seconds of submission. |
| FR-007 | Produce a risk score from 0-1000 and a recommendation of AUTO_APPROVE, REFER_TO_UNDERWRITER, or AUTO_DECLINE. | Standardizes initial decision recommendations and supports consistency. | input/brs.md | Scoring result includes both numeric score and one allowed recommendation. |
| FR-008 | Use applicant data, credit bureau data, debt-to-income, loan-to-income, employment stability, and credit history length in scoring. | Ensures decision recommendations are based on defined business factors. | input/brs.md | Model inputs include each listed factor. |
| FR-009 | Integrate with Experian CreditExpert API for every application within 30 seconds and refer to underwriter if unavailable. | Preserves credit-based risk assessment while defining a safe fallback. | input/brs.md | Credit lookup completes within SLA or routes to REFER_TO_UNDERWRITER on failure. |
| FR-010 | Allow AUTO_APPROVE applications of 10,000 or less to proceed directly to offer generation after AML/KYC clearance. | Maximizes straight-through throughput for lower-risk cases. | input/brs.md | Eligible applications bypass underwriter review only after compliance clearance. |
| FR-011 | Notify AUTO_DECLINE applicants within 5 minutes with a decline reason category and enforce a 30-day cooling-off reapplication period. | Provides timely customer communication and consistent decline handling. | input/brs.md | Decline notice excludes score detail and reapplication is blocked for 30 days. |
| FR-012 | Perform AML screening against HM Treasury sanctions and PEP sources before any offer is generated. | Prevents non-compliant lending activity before offer issuance. | input/brs.md | AML screening completes before offer generation and within 60 seconds. |
| FR-013 | Perform KYC identity verification against HMRC using NI number, name, and date of birth. | Confirms applicant identity and supports regulatory compliance. | input/brs.md | Identity check uses the stated matching fields. |
| FR-014 | Flag failed AML or KYC cases as COMPLIANCE_HOLD, route them to compliance, notify the applicant, and block offer generation. | Ensures compliance exceptions are handled safely and visibly. | input/brs.md | Failed checks route to compliance hold and suppress offer generation. |
| FR-015 | Place REFER_TO_UNDERWRITER cases and AUTO_APPROVE cases above 10,000 into the underwriter queue within 2 minutes of scoring. | Preserves human oversight where risk or amount thresholds require it. | input/brs.md | Eligible cases appear in queue within the SLA. |
| FR-016 | Show applicant summary, AI result, bureau summary, ratios, employment verification, and AML/KYC status in the underwriter dashboard. | Gives underwriters the context needed for consistent decisions. | input/brs.md | Dashboard exposes each required field set for queued applications. |
| FR-017 | Allow underwriters to approve with conditions, decline with mandatory reason, or request additional information. | Supports controlled human decisioning and exception handling. | input/brs.md | Each action is available with the required data capture. |
| FR-018 | Record every underwriter action with actor, timestamp, action, rationale or conditions, and presented AI recommendation as immutable history. | Creates defensible audit evidence for human-in-the-loop decisions. | input/brs.md | Underwriter actions are stored immutably with all required attributes. |
| FR-019 | Escalate unactioned underwriter queue items to the team lead after 4 business hours. | Reduces operational delays and missed service expectations. | input/brs.md | Escalation notification is triggered after the SLA breach. |
| FR-020 | Generate a loan offer document for every approved application with amount, APR, monthly repayment, total repayable, term, and key terms. | Standardizes approved-offer communication and legal content. | input/brs.md | Offer document contains all required financial and legal fields. |
| FR-021 | Present the loan offer through the self-service portal and email with 14-day validity. | Gives customers clear and accessible offer access. | input/brs.md | Offer is available in both channels and expires after 14 days. |
| FR-022 | Allow digital acceptance through DocuSign and log timestamp and IP address. | Enables legally trackable remote acceptance. | input/brs.md | Acceptance is captured through DocuSign with timestamp and IP address. |
| FR-023 | Enforce a 14-day cooling-off period after acceptance and send reminders on day 7 and day 13. | Meets customer-protection obligations and keeps applicants informed. | input/brs.md | Cooling-off logic and reminder schedule are enforced. |
| FR-024 | Trigger a disbursement instruction to Temenos T24 via the internal payment gateway after acceptance and cooling-off completion or waiver. | Completes the lending journey without manual disbursement handoff. | input/brs.md | Disbursement request is sent only when prerequisite states are satisfied. |
| FR-025 | Include account number, sort code, loan amount, reference number, and value date in the disbursement instruction. | Ensures the receiving banking flow has complete settlement data. | input/brs.md | Payload contains all required fields. |
| FR-026 | Receive disbursement confirmation, mark status DISBURSED, retry once if confirmation is delayed beyond 2 minutes, then alert operations. | Maintains operational reliability and visible exception handling. | input/brs.md | Confirmation updates state, retry runs once, then alert triggers if still unresolved. |
| FR-027 | Notify applicants by email and portal when disbursement is confirmed, including expected value date. | Closes the customer loop at funding completion. | input/brs.md | Notifications are sent with the expected value date. |
| FR-028 | Maintain an immutable audit log of every application state transition including previous and new state, triggering actor, timestamp, and data snapshot. | Provides complete regulatory and operational traceability. | input/brs.md | Every state transition is stored as immutable audit history. |
| FR-029 | Provide admin dashboard metrics for volume by status, average decision time, AI recommendation distribution, underwriter rates, and AML/KYC hold rates with 5-minute refresh. | Supports operational control, oversight, and performance monitoring. | input/brs.md | Dashboard shows each listed metric and refresh cadence. |
| FR-030 | Emit structured observability events for submission, scoring, compliance results, underwriter decisions, offer acceptance, and disbursement. | Supports monitoring, troubleshooting, and downstream analytics. | input/brs.md | Events are emitted with ARN, timestamp, status, and actor. |
| NFR-001 | Load the application intake form within 2 seconds on a standard broadband connection. | Protects customer conversion and digital experience quality. | input/brs.md | Form load time remains within 2 seconds under stated conditions. |
| NFR-002 | Complete the AI scoring pipeline end-to-end within 90 seconds under normal load. | Keeps the core value proposition of rapid decisions credible. | input/brs.md | End-to-end scoring remains within 90 seconds. |
| NFR-003 | Support 500 concurrent application submissions. | Ensures the platform can handle expected demand. | input/brs.md | Load testing demonstrates 500 concurrent submissions. |
| NFR-004 | Encrypt all PII at rest with AES-256 and in transit with TLS 1.3. | Protects customer data and supports compliance obligations. | input/brs.md | Data protection controls are enforced for storage and transport. |
| NFR-005 | Keep the audit log write-once and tamper-evident. | Preserves trust in regulatory and forensic audit records. | input/brs.md | Audit storage prevents mutation and demonstrates tamper evidence. |
| NFR-006 | Achieve 99.9% uptime during business hours from 08:00 to 20:00 GMT. | Supports operational reliability during critical service windows. | input/brs.md | Availability reporting demonstrates the SLA target. |
| NFR-007 | Implement circuit breakers with fallback behavior for Experian, HMRC, DocuSign, and T24 integrations. | Reduces outage blast radius and keeps the platform operationally safe. | input/brs.md | Circuit-breaker and fallback behavior exist for each listed integration. |

## Capabilities

| Capability | Outcome | Related requirements | Notes |
|---|---|---|---|
| Digital application intake | Applicants can submit and track loan applications online without branch or email dependency. | FR-001, FR-002, FR-003, FR-004, FR-005, NFR-001 | Core customer-entry capability |
| AI-assisted decisioning | Applications are scored quickly with consistent recommendation outputs and defined fallbacks. | FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, NFR-002, NFR-007 | Must remain explainable under FCA constraints |
| Compliance screening | AML and KYC checks are embedded before offer generation and exceptions are safely routed. | FR-012, FR-013, FR-014 | Strong regulatory dependency |
| Human underwriting workflow | Borderline, high-value, or fallback cases move into a controlled underwriter process. | FR-015, FR-016, FR-017, FR-018, FR-019 | Preserves human oversight |
| Offer and acceptance management | Approved applicants receive offers and can accept digitally within the policy window. | FR-020, FR-021, FR-022, FR-023 | Customer-facing and compliance-sensitive |
| Disbursement orchestration | Accepted applications progress to core banking disbursement with retry and alert handling. | FR-024, FR-025, FR-026, FR-027 | Depends on internal payment gateway contract |
| Audit, observability, and administration | The platform exposes audit trails, metrics, and events for oversight and operations. | FR-028, FR-029, FR-030, NFR-004, NFR-005, NFR-006 | Cross-cutting platform capability |

## Existing-System Context

| Area | Current-state note | Why it matters | Source reference |
|---|---|---|---|
| Manual loan-processing workflow | The bank currently processes personal loan applications manually through paper or email with multi-day turnaround. | The initiative is replacing an existing operational process rather than launching a net-new business function. | input/brs.md |
| Temenos T24 core banking | Disbursement must integrate with the existing Temenos T24 environment through an internal payment gateway. | Existing banking dependencies create contract and sequencing sensitivity. | input/brs.md, input/architecture.md |
| Experian enterprise integration | Credit bureau checks must use Experian CreditExpert under an existing enterprise contract. | External vendor dependency shapes fallback rules and readiness needs. | input/brs.md, input/architecture.md |
| DocuSign enterprise integration | E-signature must use DocuSign under an existing enterprise contract. | Offer acceptance design is constrained by current tooling. | input/brs.md, input/architecture.md |
| Azure identity and hosting model | Underwriter and admin users are expected to authenticate through Azure AD, and services are proposed on Azure UK regions. | Existing enterprise platform choices affect delivery and compliance boundaries. | input/architecture.md |

## Gaps and Questions

| ID | Question / gap | Impact if unresolved | Owner | Needed before |
|---|---|---|---|---|
| GAP-001 | The BRS answers the major open questions, but the T24 payment gateway contract still needs to be concretely defined for implementation. | Delivery teams may block on API shape, validation rules, and error handling if the contract is not clarified during planning. | IT Architecture | Architecture review and engineering readiness |

## Risks and Assumptions

| ID | Type | Description | Impact | Owner / follow-up |
|---|---|---|---|---|
| RSK-001 | Risk | Explainable AI requirements may constrain model choice and slow delivery if the chosen approach cannot satisfy FCA scrutiny. | High | Head of AI and architecture review |
| RSK-002 | Risk | Integration latency or downtime across Experian, HMRC, DocuSign, or T24 could erode the promised decision-time outcomes. | High | Engineering and architecture planning |
| RSK-003 | Risk | Compliance-hold and manual-verification volumes may be higher than expected, increasing pressure on underwriters or compliance teams. | Medium | Product and operations planning |
| RSK-004 | Assumption | HMRC KYC fallback is manual verification rather than automatic decline or approval. | Medium | Preserve in business rules and process flows |
| RSK-005 | Assumption | HM Treasury is the only AML data source in scope for this phase. | Medium | Confirm in compliance design and readiness checks |
| RSK-006 | Assumption | Cooling-off waiver does not require a separate legal sign-off workflow. | Medium | Preserve in offer and process-flow outputs |

## Consolidation Notes

| Topic | Overlap / conflict / assumption | Resolution or current position |
|---|---|---|
| Initiative identifier | The source BRS metadata lists Initiative ID `I005` while the active workspace is `I013-NEXT13`. | This intake artifact uses the active workspace ID for framework traceability and treats the BRS document ID as source-origin metadata. |
| Open-question handling | The BRS contains five open-question rows, but each row also includes an answer. | Answered items were treated as resolved context and assumptions, not as unresolved gaps. |
| Architecture ownership | The architecture input is marked draft and pending architect review. | Business scope is derived from the BRS; architecture details are used only as supporting delivery context at this stage. |

## PO Review Checklist

- [x] Objectives are understandable and measurable
- [x] Scope boundaries are explicit
- [x] Requirements are traceable to source documents
- [x] Existing-system context is visible when relevant
- [x] Open questions have clear impact and owners
- [x] Risks and assumptions are reviewable without engineering detail
