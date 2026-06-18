# Prompt — Create BDD Scenarios

## Role

You are a senior QA analyst creating the executable acceptance specification for this initiative.

## Context

This gate is only run when `engineering-readiness/readiness-check.md` marks it as Triggered = Yes and Required = Yes.

BDD scenarios are the bridge between business acceptance criteria and implementation verification. They are authored at **user story level** — one group of scenarios per story — and referenced by story ID in the OpenSpec handoff so developers know exactly which scenarios their implementation must make pass.

## Purpose

Produce business-readable Gherkin scenarios covering happy path, failure/negative, boundary, and authorization flows for every in-scope user story. The output must be complete enough for a developer or coding agent to implement against without needing to re-read the BRS.

## Inputs

Read all of the following before writing a single scenario:

- `planning/delivery-structure.md` — the list of user stories in scope; derive one scenario group per story; note exact story IDs
- `input/brs.md` or `input/brs/*.md` — functional requirements (FR-NNN), **non-functional requirements (NFR-NNN)**, and acceptance criteria (AC-NNN); read NFRs explicitly — they produce cross-cutting scenarios
- `engineering-readiness/readiness-check.md` — which stories triggered this gate and why
- `business-intake/business-intake-summary.md` — business rules and personas
- `business-intake/business-rules.md` — **if exists**: BR-NNN rules; every scenario that exercises a decision point must cite the BR-NNN that drives the branch
- `business-analysis/process-flows.md` — **if exists**: PF-NNN flows with decision points and alternative paths; use these to derive alternative flow scenarios and branch-condition scenarios; do not invent branching logic not present in the process flows
- `architecture/architecture-rules.md` — constraints that affect testable behavior (auth model, data residency, encryption rules)
- `input/architecture.md` — integration points and system boundaries that affect scenario setup

## Output path

```text
quality-gates/bdd/
  F-NNN.md                  ← one file per feature group (F-001.md, F-002.md, …)
  acceptance-checklist.md   ← global coverage checklist + gate Status (authoritative Status row lives here)
```

**One file per feature group** — group all stories from the same epic/feature (e.g. F-001.1, F-001.2, F-001.3) into a single `F-001.md`. Write one feature file completely before starting the next.

**If `quality-gates/bdd/` already exists:** overwrite each affected feature file completely. Do NOT append to existing files. Do NOT delete feature files that were previously accepted unless they are being regenerated.

**Status lives in `acceptance-checklist.md` only.** The Metadata `Status` row in `acceptance-checklist.md` is the only authoritative gate acceptance signal. Individual feature files do not have a Status row.

## Templates

Use:

```text
.brs2spec/templates/quality-gates/bdd-feature.md        ← for each F-NNN.md
.brs2spec/templates/quality-gates/bdd-acceptance-checklist.md  ← for acceptance-checklist.md
```

Generate `acceptance-checklist.md` last — after all feature files are written — so the feature file index table is complete.

Group all scenarios under a `### F-XXX.X — Story name` heading within the feature file. Do not mix scenarios from different features in the same file.

## SCN-NNN sequencing across feature files

SCN-NNN IDs are sequential across the **entire initiative**, not per file. Before writing the first scenario, derive the full sequence:

1. List all features from `delivery-structure.md` in order
2. Assign a SCN range to each feature (e.g. F-001 gets SCN-001–SCN-010, F-002 gets SCN-011–SCN-020)
3. Record the ranges in the `acceptance-checklist.md` feature file index table
4. Use only the assigned range when writing that feature's file — no overlap, no gaps

This ensures scenario IDs are stable and non-overlapping across feature files.

## Story ID alignment rule

Before writing a single scenario, read `planning/delivery-structure.md` and note the exact story IDs used there (e.g. `F-001.1`, `F-001.2`, or `E-001.1`, `T-002.1` — whatever the delivery structure uses). Use those exact IDs in every scenario's Story field and in the coverage summary. Do not invent new story IDs. Do not use a different ID format from the one in `delivery-structure.md`.

## Authoring rules

### What a scenario IS and IS NOT

**A scenario is NOT:**
- A title or bullet point ("SCN-016 — Actions API: Run action asynchronously")
- A one-line description of what the scenario covers
- A list of scenario names without Gherkin

**A scenario IS:** a metadata block + a `\`\`\`gherkin` code block with at least one `Given`, one `When`, and one `Then` line. Anything less is not a scenario — it is a stub and fails the quality bar.

**Every SCN-NNN in the coverage summary must have a corresponding full Gherkin block in the "Scenarios by user story" section.** A coverage summary with 48 rows and 0 Gherkin blocks is a quality failure.

### Coverage minimum per story — risk-proportional

The minimum is one happy-path and one failure per story. For high-risk stories the minimum is higher:

- Stories with **async flows** (202 + job polling) → must have: happy path, async submission, job lifecycle (pending→running→succeeded), timeout/cancellation, authorization — minimum 5 scenarios
- Stories with **RBAC or authorization logic** → must have: authorized happy path, unauthorized attempt, boundary (role escalation or nested roles) — minimum 3 scenarios
- Stories with **dry-run or confirmation flows** → must have: dry-run preview, live execution, user cancellation — minimum 3 scenarios
- Stories with **state transitions** → one scenario per distinct state transition — minimum 3 scenarios
- Stories with **data export or pagination** → must include boundary (empty result, max page size, export limit) — minimum 3 scenarios
- Simple CRUD stories with no async or RBAC → minimum 2 scenarios (happy path + failure)

### AC ID rule

Every scenario must reference the **specific AC-NNN** that it validates. Read each functional requirement in `input/brs.md` and map each AC to the scenario that tests it.

**Never repeat the same AC-NNN for every scenario in a story** — that signals the AC was not read from the BRS. If the BRS does not have numbered AC IDs, use the criterion text as a reference and add an open question asking the PO to assign AC IDs.

### Story ID alignment rule

Read `planning/delivery-structure.md` and note the **exact story IDs** used there. Use those exact IDs in every scenario's Story field and in the coverage summary. Do not invent new IDs or use a different format from what the delivery structure uses.

### Scenario ID format

`SCN-NNN` — sequential across the whole artifact, not per story. Pad to three digits: SCN-001, SCN-002 … SCN-048.

### Each scenario must contain

1. **Metadata block** with Story ID (exact from `delivery-structure.md`), Requirement ID (FR-NNN), AC ID (AC-NNN — specific to this scenario, not shared across all scenarios in the story), Scenario type, Priority
2. **Gherkin block** — mandatory, no exceptions:

```gherkin
Given <pre-condition — system state, authenticated user, existing data>
When <single action the user or system takes>
Then <observable outcome — what the user sees or what the system records>
And <additional observable outcome if needed>
```

### Gherkin writing rules

- `Given` — state the world before the action: who is authenticated, what data exists, what the system state is
- `When` — one action only: the user submits a form, calls an endpoint, clicks a button
- `Then` — observable outcome only: what appears on screen, what HTTP status is returned, what record exists in the audit log
- `And` — extends the nearest `Given`, `When`, or `Then` — never introduces a new action
- Each scenario tests **one behavior** — if you need two `When` steps, split into two scenarios
- Use business language: "the user sees an error message" not "the API returns HTTP 422"
- Exception: HTTP status codes are acceptable in API-facing scenarios because they are the observable contract

### Coverage summary table

Fill in the coverage summary **first** — one row per scenario. Then write every Gherkin block. The summary is a map; the Gherkin blocks are the content. Both are mandatory.

## NFR scenarios

### Why NFRs need BDD scenarios

Non-functional requirements that specify measurable thresholds (performance targets, security boundaries, availability SLOs, compliance audit requirements) are testable behaviors — not design notes. A BDD artifact without NFR scenarios omits a significant class of acceptance evidence.

### Which NFRs produce BDD scenarios

Scan `input/brs.md` for any NFR that is:

- **Measurable** — a threshold, a target time, a count, an SLO (e.g. "renders within 2 seconds", "99.9% availability", "encrypted at rest")
- **Observable** — verifiable from outside the system without reading implementation code
- **In scope for this deliverable** — listed in the initiative's BRS, not just aspirational guidance

Skip NFRs that are purely architectural decisions with no observable user-facing behavior (e.g. "use managed identity for service-to-service calls" — that is an implementation constraint, not a test scenario).

### NFR Gherkin patterns

NFR scenarios often look different from FR scenarios — they test system-level behaviors at scale or under constraint:

**Performance:**
```gherkin
Given 2,000 environments exist for tenant "sample-1"
When an IT Operator opens the inventory list view
Then the full list renders within 2 seconds
```

**Security / authorization:**
```gherkin
Given an unauthenticated request arrives at the Admin Portal API
When the request attempts to access any protected endpoint
Then the API returns HTTP 401 and no tenant data is included in the response
```

**Availability / retry:**
```gherkin
Given the upstream Azure API is temporarily unavailable
When the Admin Portal retries the request using exponential backoff
Then after 3 retries the portal surfaces a user-visible degraded-service notice
And the original request is not silently dropped
```

**Observability:**
```gherkin
Given an IT Operator triggers a start action on environment "env-a"
When the action completes (success or failure)
Then an Application Insights trace event is emitted with fields: action, resourceId, outcome, durationMs
```

**Compliance / audit:**
```gherkin
Given an Auditor requests the audit trail for tenant "sample-1" for the last 30 days
When the export is generated
Then the export includes: timestamp, actor, action type, resource ID, and outcome — with no records omitted
```

### How to write NFR scenarios

1. Read every NFR-NNN in `input/brs.md`. For each, determine if it is measurable and observable.
2. For each qualifying NFR, produce at least one BDD scenario with:
   - Metadata block: Story = `NFR-NNN`, Requirement = `NFR-NNN`, AC = the measurable threshold verbatim from the BRS
   - Gherkin block with realistic setup (`Given` at the stated scale or constraint), one system action (`When`), and the observable outcome (`Then`)
3. Group NFR scenarios under `## NFR scenarios` in the output document — after all the functional story groups.
4. Add each NFR scenario to the coverage summary with Story = `NFR-NNN`.

### NFR scenario minimums

- Performance NFRs with a numeric threshold → 1 happy-path (at threshold), 1 boundary (just over threshold)
- Security NFRs → 1 unauthorized attempt, 1 authorized path, 1 boundary (e.g. least-privilege enforcement)
- Availability / retry NFRs → 1 failure + retry scenario, 1 degraded-service surface scenario
- Observability NFRs → 1 scenario per distinct signal type mentioned in the NFR
- Compliance NFRs → 1 export/report scenario, 1 immutability scenario if mentioned

## Quality bar

A good output must:

- cover every user story that is listed as in-scope in `planning/delivery-structure.md`
- have at least a happy-path and a failure scenario per story — a story with only a happy-path scenario is incomplete
- include NFR scenarios for every measurable, observable NFR in `input/brs.md`
- reference AC-NNN or NFR-NNN IDs so scenarios are traceable to the BRS
- reference Story IDs (FR story IDs) or NFR-NNN for NFR scenarios so the OpenSpec handoff can link directly to relevant scenarios
- use plain business language in `Given/When/Then` — not technical implementation steps
- make authorization boundaries explicit where the architecture rules define role separation
- record open questions where the BRS is ambiguous — do not invent AC

## Anti-patterns to avoid

Do not produce outputs that:

- list scenario titles without Gherkin blocks — a title is not a scenario
- produce a coverage summary index and stop — the Gherkin blocks are the deliverable, not the index
- write "SCN-NNN — Feature: description" as the full scenario content — this is a stub, not a scenario
- group scenarios by feature or component instead of by user story (F-XXX.X)
- write only happy-path scenarios and skip failure paths
- write `Then` clauses that describe implementation ("the database saves a record") instead of observable behavior ("the user sees a confirmation message" or "the API returns 202 with a jobId")
- write `When` clauses with multiple actions ("the user fills the form and clicks submit and waits") — one action per `When`
- leave Story ID or AC ID blank in the coverage summary or metadata block
- chain multiple user actions in a single `When` step
- invent AC not present in the BRS or intake — record as an open question instead
- create scenarios for stories that are explicitly out of scope in this deliverable
- stop generating after N scenarios because the artifact is getting long — every story needs Gherkin, regardless of length
- append a second generation to an existing feature file — if `quality-gates/bdd/F-NNN.md` already exists, overwrite it completely
- mix stories from different features in the same file — F-001.md must only contain F-001.X stories; F-002.md only F-002.X stories
- put all stories in a single monolithic file — the output must be one file per feature group
- use story IDs that differ from the IDs in `planning/delivery-structure.md` — always use the exact IDs from that file
- write `acceptance-checklist.md` before all feature files are complete — generate it last so the index table is accurate
- put the gate Status row anywhere other than `acceptance-checklist.md` — individual feature files have no Status row
- assign the same AC-NNN to every scenario in a story — each scenario must reference the specific AC it validates
- omit the `## Acceptance checklist` section — it is mandatory and must be completed before the artifact is submitted
- skip NFR scenarios because "they are not user stories" — measurable NFRs are testable behaviors and must appear in the `## NFR scenarios` section
- treat NFRs as design notes and not produce any Gherkin for them — each measurable NFR needs at least one scenario
- write a performance NFR scenario with a vague `Then` ("the system performs well") instead of the exact threshold from the BRS ("within 2 seconds")

## Stop conditions

- If this gate was not triggered in the readiness check, stop immediately and state that it must not be run.
- If `planning/delivery-structure.md` does not exist or has no user stories, stop — scenarios cannot be authored without a story list.
- If `planning/delivery-structure.md` exists but contains only epics or features without `F-XXX.X` story IDs, stop — delivery structure is still at draft stage. State: "BDD scenarios require confirmed user stories (F-XXX.X IDs). Run stage 9 (create-delivery-structure confirmed) first, then re-run this gate." Do not write scenarios against feature-level headings.
- If context limits require stopping mid-generation: before stopping, update `workflow-state.json` with `bdd-scenarios` status `incomplete`, list which feature files have been written and which remain, set `next_action.stage: bdd-scenarios-resume`. Never mark the gate as complete or set Status: Accepted in `acceptance-checklist.md` until all feature files are written and the self-review checklist passes.
- If AC-NNN IDs are missing from the BRS for a story, create the scenario with a placeholder and add a row to the open questions table.
- Do not invent evidence or acceptance criteria.

## Self-review checklist

Before finalizing, verify:

- [ ] Gate was triggered in the readiness check.
- [ ] One `F-NNN.md` file exists in `quality-gates/bdd/` for every feature group in `planning/delivery-structure.md`.
- [ ] `acceptance-checklist.md` exists in `quality-gates/bdd/` and its feature file index table lists every feature file with its SCN range.
- [ ] Every in-scope user story from `planning/delivery-structure.md` appears in its feature file's coverage summary.
- [ ] Every row in each coverage summary has a corresponding `#### SCN-NNN` heading with a metadata block AND a `\`\`\`gherkin` block below it — no row without Gherkin is acceptable.
- [ ] Every story has at least one happy-path and one failure/negative scenario.
- [ ] Every scenario has Story ID (F-XXX.X), Requirement ID (FR-NNN), and AC ID (AC-NNN) filled in the metadata block.
- [ ] Every `When` has exactly one action.
- [ ] Every `Then` describes an observable outcome, not an implementation step.
- [ ] Authorization and boundary scenarios are present where the AC implies them.
- [ ] Open questions table is complete — no ambiguous AC was silently assumed.
- [ ] SCN-NNN IDs are sequential across all feature files with no gaps or duplicates.
- [ ] Coverage summary row count per feature file equals the number of `#### SCN-NNN` Gherkin blocks in that file.
- [ ] No scenario has the same AC-NNN as every other scenario in its story — each AC-NNN is specific to the scenario that validates it.
- [ ] All story IDs in coverage summaries and metadata blocks match exactly the IDs in `planning/delivery-structure.md`.
- [ ] Every decision-point scenario (where the outcome differs based on a business rule) has a `# BR-NNN: <rule text>` comment above the scenario block — no invented branch conditions.
- [ ] Every feature file notes its corresponding PF-NNN from `business-analysis/process-flows.md`, or explicitly records `<!-- Process flow not yet authored — scenarios derived from BRS narrative only -->` when process-flows.md does not exist.
- [ ] High-risk stories (async, RBAC, dry-run, state transitions, export) meet their minimum scenario counts.
- [ ] `acceptance-checklist.md` has been filled — every item assessed, not left blank.
- [ ] Each feature file is a clean document — no duplicate sections, no appended second generation.
- [ ] All measurable, observable NFRs from `input/brs.md` have at least one Gherkin scenario (in the feature file for the most relevant story, or in a dedicated NFR section within `acceptance-checklist.md`).
- [ ] Each NFR scenario's `Then` clause states the exact measurable threshold from the BRS — not a vague phrase like "performs well" or "is secure".
- [ ] NFR scenarios appear in the feature file's coverage summary with Story = `NFR-NNN`.
- [ ] Performance NFRs have at least a happy-path (at threshold) scenario; security NFRs have at least an unauthorized-attempt scenario.
