# Decision Tree

Use this document to find your entry point and delivery mode before opening any prompt.

For automated routing, run `.brs2spec/00-start.md` — it asks five questions and scores the decision for you.

---

## Step 1 — What kind of situation are you entering?

```
Do you have a formal BRS document?
│
├── Yes → Entry mode: BRS-first
│         First prompt: .brs2spec/skills/0-input-preparation/01-convert-brs-word-to-markdown.md
│
├── No, but you are changing an existing system
│         → Entry mode: Existing-system enhancement
│         First prompt: .brs2spec/skills/2-business-intake/01-create-business-intake-summary.md
│
├── No, scope is narrow (single story or bug fix)
│         → Entry mode: Small change / bug fix
│         First prompt: .brs2spec/skills/1-routing/01-select-delivery-and-execution-mode.md
│
└── No, scope spans multiple capabilities or teams
          → Entry mode: Large modular initiative
          First prompt: .brs2spec/skills/0-input-preparation/03-normalize-input-package.md
```

---

## Step 2 — How much workflow control do you need?

Score each criterion. Sum the scores to find your delivery mode.

| Criterion | 0 | 1 | 2 | Your score |
|---|---|---|---|---|
| Requirement ambiguity | Clear and complete | Some gaps | Significant gaps or conflicts | |
| Architecture impact | None | Touches existing components | New boundaries or services | |
| Compliance / audit relevance | None | Informally relevant | Formally required | |
| Business criticality | Low | Medium | High or customer-facing | |
| Number of teams | One | Two | Three or more | |
| Delivery size | Single story | 2–5 stories | 6+ stories or multi-quarter | |
| Brownfield regression risk | None | Low | Significant existing behavior affected | |
| **Total** | | | | |

| Total score | Delivery mode |
|---|---|
| 0–3 | **Fast Path** — minimal artifacts, engineering-ready scope |
| 4–7 | **Standard** — some clarification needed, one team |
| 8–11 | **Enterprise** — formal BRS, architecture impact, compliance |
| 12–14 | **Enterprise + Modular Delivery** — multi-team, multi-quarter |

Override is always allowed with explicit justification in the routing decision.

---

## Step 3 — Which downstream engineering format will you use?

| Situation | Execution mode |
|---|---|
| OpenSpec is available in your project | OpenSpec |
| No OpenSpec | Standalone |
| Business stakeholders review and approve in M365 | Business Copilot |

---

## Full delivery flow

<div class="dt-flow">

  <!-- START -->
  <div class="dt-start-node">
    <span class="dt-start-icon">▶</span> Start here
  </div>

  <!-- PHASE 1: Entry mode -->
  <div class="dt-connector"></div>
  <div class="dt-phase-label">Phase 1 — Entry mode</div>
  <div class="dt-gate">
    <div class="dt-gate-icon">?</div>
    <div class="dt-gate-text">Do you have a formal BRS document?</div>
  </div>
  <div class="dt-branch-bar dt-bar-four"></div>
  <div class="dt-row dt-four">
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-yes">Yes</div>
      <div class="dt-card dt-card-entry">
        <div class="dt-card-icon">📄</div>
        <div class="dt-card-title">BRS-first</div>
        <div class="dt-card-desc">Start from a formal requirements document</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">No — existing system</div>
      <div class="dt-card dt-card-entry">
        <div class="dt-card-icon">🔧</div>
        <div class="dt-card-title">Existing-system enhancement</div>
        <div class="dt-card-desc">Changing a live service, contract, or module</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">No — narrow scope</div>
      <div class="dt-card dt-card-entry">
        <div class="dt-card-icon">⚡</div>
        <div class="dt-card-title">Small change or bug fix</div>
        <div class="dt-card-desc">Single story or fix — may qualify for Fast Path</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">No — large scope</div>
      <div class="dt-card dt-card-entry">
        <div class="dt-card-icon">🏗️</div>
        <div class="dt-card-title">Large modular initiative</div>
        <div class="dt-card-desc">Spans multiple teams, capabilities, or increments</div>
      </div>
    </div>
  </div>

  <!-- PHASE 2: Delivery mode -->
  <div class="dt-merge-bar dt-bar-four"></div>
  <div class="dt-connector"></div>
  <div class="dt-phase-label">Phase 2 — Delivery mode</div>
  <div class="dt-gate">
    <div class="dt-gate-icon">#</div>
    <div class="dt-gate-text">Score 7 criteria — max 14 points</div>
  </div>
  <div class="dt-branch-bar dt-bar-four"></div>
  <div class="dt-row dt-four">
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-score" style="background:#dff6f3;color:#0f766e;border-color:#0f766e">Score 0–3</div>
      <div class="dt-card dt-card-fast">
        <div class="dt-card-title">Fast Path</div>
        <div class="dt-card-desc">Clear scope, minimal artifacts, engineering-ready</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-score" style="background:#eff6ff;color:#1d4ed8;border-color:#1d4ed8">Score 4–7</div>
      <div class="dt-card dt-card-std">
        <div class="dt-card-title">Standard</div>
        <div class="dt-card-desc">Some clarification needed, one team</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-score" style="background:#fef9c3;color:#92400e;border-color:#ca8a04">Score 8–11</div>
      <div class="dt-card dt-card-ent">
        <div class="dt-card-title">Enterprise</div>
        <div class="dt-card-desc">Formal BRS, architecture impact, compliance</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-score" style="background:#fce7f3;color:#9d174d;border-color:#be185d">Score 12–14</div>
      <div class="dt-card dt-card-mod">
        <div class="dt-card-title">Enterprise + Modular</div>
        <div class="dt-card-desc">Multi-team, multi-quarter, modular delivery</div>
      </div>
    </div>
  </div>

  <!-- PHASE 3: Execution mode -->
  <div class="dt-merge-bar dt-bar-four"></div>
  <div class="dt-connector"></div>
  <div class="dt-phase-label">Phase 3 — Execution mode</div>
  <div class="dt-gate">
    <div class="dt-gate-icon">?</div>
    <div class="dt-gate-text">Which engineering contract format will you use?</div>
  </div>
  <div class="dt-branch-bar dt-bar-three"></div>
  <div class="dt-row dt-three">
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">OpenSpec available</div>
      <div class="dt-card dt-card-os">
        <div class="dt-card-icon">📐</div>
        <div class="dt-card-title">OpenSpec handoff</div>
        <div class="dt-card-desc">openspec/changes/D1-.../</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">No OpenSpec</div>
      <div class="dt-card dt-card-sa">
        <div class="dt-card-icon">📦</div>
        <div class="dt-card-title">Standalone handoff</div>
        <div class="dt-card-desc">standalone-delivery/D1-.../</div>
      </div>
    </div>
    <div class="dt-col">
      <div class="dt-branch-tick"></div>
      <div class="dt-badge dt-badge-no">M365 review</div>
      <div class="dt-card dt-card-bc">
        <div class="dt-card-icon">☁️</div>
        <div class="dt-card-title">Business Copilot</div>
        <div class="dt-card-desc">SharePoint / Word / Teams intake</div>
      </div>
    </div>
  </div>

  <!-- PHASE 4: Pipeline -->
  <div class="dt-merge-bar dt-bar-three"></div>
  <div class="dt-connector"></div>
  <div class="dt-phase-label">Phase 4 — Delivery pipeline</div>

  <div class="dt-pipeline">
    <div class="dt-pipe-step">
      <div class="dt-pipe-num">1</div>
      <div class="dt-pipe-body">
        <div class="dt-pipe-title">Engineering Readiness Check</div>
        <div class="dt-pipe-desc">Proceed / not-proceed decision with evidence. Triggers conditional quality gates.</div>
      </div>
    </div>
    <div class="dt-pipe-arrow">↓</div>
    <div class="dt-pipe-step">
      <div class="dt-pipe-num">2</div>
      <div class="dt-pipe-body">
        <div class="dt-pipe-title">Conditional Quality Gates</div>
        <div class="dt-pipe-desc">BDD scenarios · API / Data / Event contracts · Security review · Observability plan — only if triggered.</div>
      </div>
    </div>
    <div class="dt-pipe-arrow">↓</div>
    <div class="dt-pipe-step">
      <div class="dt-pipe-num">3</div>
      <div class="dt-pipe-body">
        <div class="dt-pipe-title">Implementation</div>
        <div class="dt-pipe-desc">One approved task at a time from the handoff artifact.</div>
      </div>
    </div>
    <div class="dt-pipe-arrow">↓</div>
    <div class="dt-pipe-step">
      <div class="dt-pipe-num">4</div>
      <div class="dt-pipe-body">
        <div class="dt-pipe-title">Code · Architecture · Security Review</div>
        <div class="dt-pipe-desc">Review against the approved source artifacts, not the raw BRS.</div>
      </div>
    </div>
    <div class="dt-pipe-arrow">↓</div>
    <div class="dt-pipe-gate">
      <div class="dt-gate-inline">
        <span class="dt-gate-icon-sm">?</span> Is the spec correct?
      </div>
      <div class="dt-pipe-outcomes">
        <div class="dt-outcome dt-outcome-yes">
          <span class="dt-outcome-badge">Yes</span>
          <span class="dt-outcome-text">✓ Done</span>
        </div>
        <div class="dt-outcome dt-outcome-no">
          <span class="dt-outcome-badge">No</span>
          <span class="dt-outcome-text">Spec Correction → back to Implementation</span>
        </div>
      </div>
    </div>
  </div>

</div>

---

## Minimum artifact set by delivery mode

| Artifact | Fast Path | Standard | Enterprise | Enterprise + Modular |
|---|---|---|---|---|
| `input/input-package.md` | Required | Required | Required | Required |
| `routing/routing-decision.md` | Required | Required | Required | Required |
| `business-intake/business-intake-summary.md` | Optional | Required | Required | Required |
| `architecture/architecture-review.md` | Skip | Optional | Required | Required |
| `architecture/architecture-rules.md` | Skip | Optional | Required | Required |
| `planning/delivery-structure.md` | Skip | Required | Required | Required |
| `planning/delivery-increments.md` | Skip | Skip | Skip | Required |
| `planning/traceability-matrix.md` | Skip | Optional | Required | Required |
| `engineering-readiness/readiness-check.md` | Required if risk exists | Required | Required | Required |
| `engineering-readiness/initiative-context.md` | Required if risk exists | Required | Required | Required |
| Quality gates | Triggered only | Triggered only | Triggered only | Triggered only |
| Handoff artifact | Required | Required | Required | Required |

---

## Common mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Skipping readiness on Fast Path because "it's small" | Missing triggered gate, contract drift | Always run readiness when regression, security, or contract risk exists |
| Choosing Enterprise + Modular by default | Over-processing, context bloat | Score the criteria — reach 12+ before choosing this path |
| Running all prompts sequentially | Unnecessary artifacts, slower delivery | Use routing to exclude prompts not needed for the selected mode |
| Treating quality gates as optional | Governed boundary without contract | Gates are conditional, not optional — if triggered they are required |
| Implementing without `initiative-context.md` | Cross-session constraint drift | Generate context after readiness; load it before every implementation session |
