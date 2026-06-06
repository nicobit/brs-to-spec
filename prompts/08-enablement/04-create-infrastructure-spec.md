# Prompt — Create Infrastructure Specification

Recommended environment:
- VS Code Copilot Chat
- Approved engineering LLM with access to existing IaC and cloud conventions

Owner:
- Architect / Cloud Engineer / Platform Engineer

Input files:
- `features/<feature-name>/enablement/enablement-scope.md`
- `features/<feature-name>/enablement/enablement-structure.md`
- `features/<feature-name>/enablement/technical-stories.md`
- `features/<feature-name>/input/architecture-draft.md`
- Existing IaC files if available

Task:
Create the infrastructure specification.

Output:
Create:

```text
features/<feature-name>/enablement/infrastructure-spec.md
```

Use this structure:

```markdown
# Infrastructure Specification

## 1. Scope

## 2. Existing Infrastructure to Reuse

## 3. New Infrastructure Needed

| Resource | Purpose | Environment | IaC location | Owner |
|---|---|---|---|---|

## 4. Azure / Cloud Resources

## 5. Network / Private Connectivity

## 6. Identity and Access

## 7. Secrets / Key Vault / Certificates

## 8. Data / Storage / Database

## 9. Messaging / Events

## 10. Naming / Tagging / Governance

## 11. Cost Considerations

## 12. Security Considerations

## 13. Environment Differences

## 14. IaC Approach

## 15. Validation Criteria

## 16. Risks and Open Questions
```

Rules:
- Prefer approved existing patterns.
- Do not invent unapproved cloud services.
- Identify what must be reviewed by platform/security.
