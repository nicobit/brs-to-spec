# Open Decisions

> Managed by orchestrator only. Domain personas raise decisions via result file `open_decisions_raised`. Never write to this file in persona mode.

## Decision Catalog

| DEC-NNN | Question | Owner | Blocking | Raised By | Status |
|---|---|---|---|---|---|
| DEC-001 | | human / architect / product-owner | Yes / No | EVT-NNN | Open / Resolved |

---

<!-- Decision entries are appended by the orchestrator during event processing. -->
<!-- Format per decision: -->

## DEC-NNN

**Question:** {{the specific decision or question that must be answered}}  
**Owner:** {{who must answer — human / architect / product-owner / qa-analyst}}  
**Blocking:** {{true / false}}  
**Blocking what:** {{which events or stages are blocked until this is resolved}}  
**Raised by:** {{EVT-NNN}}  
**Raised at:** {{ISO timestamp}}  
**Status:** Open

<!-- When resolved, add: -->
<!-- **Resolution:** {{the decision made}} -->
<!-- **Resolved at:** {{ISO timestamp}} -->
<!-- **Resolved by:** {{who resolved it}} -->
<!-- **Status:** Resolved -->
