# Architecture Rules

| Rule ID | Rule | Why it matters | Evidence / source |
|---|---|---|---|
| AR-01 | Reuse approved identity verification services. | avoids architectural drift and preserves approved controls | architecture review |
| AR-02 | Route onboarding changes through the existing API gateway. | preserves contract control and cross-cutting protections | architecture review |
| AR-03 | Emit audit events for status changes and approval actions. | preserves compliance and operational traceability | architecture review |
| AR-04 | Keep document storage behind service-layer controls. | prevents direct client access and enforces authorization | architecture review |
