# Decision Tree

```text
Are the inputs already engineering-ready?
  Yes → Fast Path → OpenSpec directly
  No
    ↓
Do you have Word/SharePoint/Confluence inputs?
  Yes → Input Preparation
  No
    ↓
Is the request small or medium?
  Yes → Standard Path
  No
    ↓
Is there a formal BRS, approval, or architecture impact?
  Yes → Enterprise Path
  No → Standard Path
    ↓
Is it large, multi-quarter, multi-team, or likely to saturate AI coding context?
  Yes → Enterprise + Modular Delivery
  No → Enterprise Path
```

## Over-processing warning

Do not use the full framework for:
- one-file changes,
- simple bug fixes,
- clear engineering requests.

## Under-processing warning

Do not go directly to OpenSpec if:
- the BRS is ambiguous,
- architecture is unclear,
- business approval is needed,
- multiple systems are impacted.
