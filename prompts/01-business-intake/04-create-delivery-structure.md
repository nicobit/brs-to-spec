# Prompt — Create Delivery Structure

## Purpose

Create a delivery structure from the BRS that preserves the business view while preparing for modular delivery.

This prompt must not produce only a flat list of epics and features.

For small and medium initiatives, it may create a lightweight capability/feature structure.

For large initiatives, it must identify business capabilities and candidate software modules so that the work can later be organized into vertical deliverables.

## Output file

```text
business-intake/delivery-structure.md
```

## Output structure

```markdown
# Delivery Structure

## 1. Delivery Mode Assumption
Fast Path / Standard Path / Enterprise Path / Enterprise + Modular Delivery

## 2. Business Capabilities
| Capability ID | Capability | Business value | Related requirements | Priority | Notes |
|---|---|---|---|---|---|

## 3. Candidate Software Modules
| Module ID | Module name | Responsibility | Module type | Related capabilities | Notes |
|---|---|---|---|---|---|

Module type examples:
- Domain module
- Integration module
- UI module
- API module
- Data module
- Workflow module
- Reporting module
- Platform/enabler module

## 4. Capability-to-Module Map
| Capability | Modules involved | Main module | Dependency notes |
|---|---|---|---|

## 5. Candidate Delivery Slices
| Slice ID | Business slice | Capabilities included | Modules involved | Notes |
|---|---|---|---|---|

## 6. Items Requiring Architecture Alignment
| Item | Reason | Owner | Blocking? |
|---|---|---|---|

## 7. Recommendation
```

## Rules

- Do not jump directly from BRS to detailed user stories.
- Do not create a flat feature-only backlog for large initiatives.
- Preserve the business capability view.
- Add software modules only as a bridge to engineering execution.
- Do not call every technical layer a bounded context.
- A bounded context is only appropriate when there is a clear domain model boundary.
- Detailed module specs are created later only if Modular Delivery is selected.
