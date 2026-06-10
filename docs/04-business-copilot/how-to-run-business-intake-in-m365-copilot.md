# How to Run Business Intake in Microsoft 365 Copilot

Use this flow when business stakeholders need to analyze and structure an initiative in Microsoft 365 before handing it to engineering.

The flow produces three artifacts in SharePoint that engineering uses as an enriched starting point — instead of a raw BRS document.

## Overview

| Step | Prompt | Output | Required |
|---|---|---|---|
| 1 | Analyze BRS | Business summary — objectives, scope, requirements, constraints | Yes |
| 2 | Identify gaps and questions | Gaps, open questions, risky assumptions, unresolved dependencies | Yes |
| 3 | Draft epics and features | Prioritised epics with features — business perspective only | Optional |

Run the prompts in sequence. Each step builds on the previous one.

## Before you start

Place the following in a shared SharePoint location accessible to all participants:

- BRS document (Word or SharePoint page) — required
- Architecture document — optional, but recommended if available

---

## Step 1 — Analyze BRS

Open Microsoft 365 Copilot and run the prompt below. Provide the BRS document (and architecture document if available) as context.

!!! note "Inputs"
    - BRS document — required
    - Architecture document — optional

??? note "Prompt 1 — Analyze BRS and Produce Business Summary"

    **Suggested filename:** `sharepoint-output/01-business-summary.md`

    ```text
    # Role
    You are a business-facing Microsoft 365 Copilot assistant helping business stakeholders
    structure and understand their initiative before handing it to engineering.

    # Purpose
    Analyze the provided BRS document (and architecture document if available) and produce
    a structured business summary covering objectives, scope, requirements, and key constraints
    in plain business language.

    # Required output structure

    ## Business Summary — [Initiative Name]

    ### Executive Summary

    | Field | Value |
    |---|---|
    | Initiative | |
    | Business objective | |
    | Why now | |
    | Expected outcome | |
    | Primary constraint or risk | |

    ### Objectives

    | ID | Objective | Success measure | Source |
    |---|---|---|---|
    | OBJ-001 | | | |

    ### Scope

    | Area | In scope | Out of scope |
    |---|---|---|

    ### Requirements

    | ID | Requirement | Business value | Priority |
    |---|---|---|---|
    | REQ-001 | | | Must have / Should have / Nice to have |

    ### Key Constraints

    | Constraint | Source | Impact |
    |---|---|---|

    ### Integration Points

    | System / Process | Direction | Purpose |
    |---|---|---|

    ### Personas

    | Persona | Role | Key need |
    |---|---|---|

    ### Assumptions

    | ID | Assumption | Impact if wrong |
    |---|---|---|

    # Quality bar
    - Use business language — no engineering jargon.
    - Derive only from the provided documents — do not invent content.
    - Make scope boundaries explicit — in scope and out of scope.
    - Assign priority to every requirement.
    - Keep the executive summary short and decision-oriented.

    # Stop conditions
    If the BRS is missing or contains no requirements, stop.
    List what is missing and ask for it before continuing.
    ```

Save the Copilot response as `01-business-summary.md` in the SharePoint folder alongside the BRS document.

---

## Step 2 — Identify gaps and questions

Run the prompt below. Provide the business summary from step 1 as context (and the BRS document if needed for cross-reference).

!!! note "Inputs"
    - `sharepoint-output/01-business-summary.md` — required
    - BRS document — optional, for cross-reference
    - Architecture document — optional

??? note "Prompt 2 — Identify Gaps and Open Questions"

    **Suggested filename:** `sharepoint-output/02-gaps-and-questions.md`

    ```text
    # Role
    You are a business-facing Microsoft 365 Copilot assistant helping business stakeholders
    identify what is unclear, missing, or unresolved before engineering begins.

    # Context
    You have the business summary produced in step 1. Analyze it and identify gaps, open
    questions, risky assumptions, and unresolved dependencies — in plain business language.

    This is the same analysis engineering would do at the start of their workflow, but done
    earlier so business can resolve issues before handoff.

    # Required output structure

    ## Gaps and Open Questions — [Initiative Name]

    ### Summary
    [Brief statement of overall completeness and most critical items to resolve.]

    ### Gaps
    Things that are missing or incomplete in the current requirements.

    | ID | Gap | Area affected | Impact if unresolved | Suggested owner |
    |---|---|---|---|---|
    | GAP-001 | | | | |

    ### Open Questions
    Decisions that have not been made and must be resolved before or during delivery.

    | ID | Question | Why it matters | Impact if not resolved | Suggested owner | Needed before |
    |---|---|---|---|---|---|
    | Q-001 | | | | | |

    ### Risky Assumptions

    | ID | Assumption | Risk if wrong | Suggested owner |
    |---|---|---|---|
    | ASM-001 | | | |

    ### Unresolved Dependencies

    | ID | Dependency | Type | Status | Impact if delayed |
    |---|---|---|---|---|
    | DEP-001 | | System / Team / Decision | Unknown / In progress / Confirmed | |

    ### Recommended Actions

    | Priority | Action | Owner | Needed before |
    |---|---|---|---|
    | High | | | |

    # Quality bar
    - Surface real gaps — not invented ones.
    - Make the impact of each gap visible so stakeholders can prioritise.
    - Assign a suggested owner to every item.
    - Use business language throughout.
    - Keep recommended actions concrete and prioritised.

    # Stop conditions
    If the business summary from step 1 is missing, stop. Run step 1 first.
    ```

Save the Copilot response as `02-gaps-and-questions.md` in the SharePoint folder.

Review the output with business stakeholders. Resolve high-priority gaps and open questions before proceeding.

---

## Step 3 — Draft epics and features (optional)

Run this prompt only when the initiative is large enough to benefit from early delivery organisation. Skip for small or simple initiatives.

Provide the business summary and gaps document as context.

!!! note "Inputs"
    - `sharepoint-output/01-business-summary.md` — required
    - `sharepoint-output/02-gaps-and-questions.md` — recommended
    - BRS document — optional

??? note "Prompt 3 — Draft Epics and Features"

    **Suggested filename:** `sharepoint-output/03-epics-and-features.md`

    ```text
    # Role
    You are a business-facing Microsoft 365 Copilot assistant helping business stakeholders
    organise their initiative into a structured, prioritised delivery draft.

    # Context
    This is a business perspective draft — not a delivery plan and not an engineering backlog.
    It expresses how business thinks the initiative should be organised into meaningful chunks.
    Engineering will use it as one input to their planning and may adjust based on technical
    constraints. This output stops at feature level — no user stories, no tasks.

    # Purpose
    Produce a structured draft of epics and features from the business summary and gaps document.
    Each epic is a meaningful business outcome. Each feature is a capability that contributes
    to that outcome. Both must be in business language with no implementation detail.

    # Required output structure

    ## Epics and Features Draft — [Initiative Name]

    > Business perspective draft. Engineering will review and may adjust.
    > This is a starting point for alignment — not a delivery commitment.

    ### Summary

    | Field | Value |
    |---|---|
    | Total epics | |
    | Must-have epics | |
    | Should-have epics | |
    | Nice-to-have epics | |
    | Key dependencies or blockers | |

    ---

    ### Epic: [Epic Name]

    **Outcome:** [What changes for the business or user when this epic is done]
    **Business value:** [Who benefits and how]
    **Priority:** Must have / Should have / Nice to have

    **In scope:**
    - 

    **Out of scope:**
    - 

    **Dependencies or open questions:**
    - [Reference items from the gaps document]

    #### Feature: [Feature Name]

    **Capability:** [What the system or process will be able to do]
    **Business value:** [Who benefits and how]
    **Priority:** Must have / Should have / Nice to have
    **Acceptance notes:** [How business will know this feature is done — business language only]

    ---

    # Quality bar
    - Every epic must be outcome-oriented — what changes, not what gets built.
    - Every feature must be capability-oriented — what the system can do, not how.
    - Assign priority to every epic and every feature.
    - Make scope boundaries explicit for every epic.
    - No user stories, no tasks, no implementation detail, no story points.
    - Use business language throughout.

    # Anti-patterns
    - Do not name epics after technical components or project phases.
    - Do not mark everything as Must have.
    - Do not resolve open questions — reference them.

    # Stop conditions
    If requirements are too vague to derive meaningful epics, stop.
    List what is missing and recommend resolving gaps from step 2 first.
    ```

Save the Copilot response as `03-epics-and-features.md` in the SharePoint folder.

---

## Hand off to engineering

Once steps 1 and 2 are complete (and step 3 if applicable), share the SharePoint folder with IT or the engineering lead. They will:

- copy the business summary into the initiative workspace as the enriched BRS input
- use the gaps and questions as the starting point for their planning
- use the epics and features draft (if produced) as alignment context for delivery planning

Engineering work then continues in VS Code using these outputs as inputs.

## See also

- [Business Copilot Overview](README.md)
- [Delivery & Execution Modes](../02-delivery-and-execution-modes.md)
