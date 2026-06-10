# Repository Descriptor — {{repo-name}}

> File name = folder name used in OpenSpec handoff subfolders (e.g. `api.md` → `F-XXX.X-slug/api/`)
> Do not rename this file after handoff generation has started — the folder name is derived from the file name.

## Identity

| Field | Value |
|---|---|
| Repository name | {{actual-repo-name, e.g. admin-portal-api}} |
| Short alias | {{matches this file's name without extension, e.g. api}} |
| Remote URL / path | {{e.g. github.com/org/admin-portal-api}} |
| Owning team | {{team or squad name}} |

## Technology

| Field | Value |
|---|---|
| Language | {{e.g. TypeScript, C#, Python}} |
| Framework | {{e.g. NestJS, ASP.NET Core, FastAPI}} |
| Runtime | {{e.g. Node 20, .NET 8, Python 3.12}} |
| Database | {{e.g. PostgreSQL 15, Azure Cosmos DB, none}} |
| Infrastructure | {{e.g. Azure App Service, AKS, Azure Functions}} |

## Functional areas

> List the FR-NNN identifiers from `input/brs.md` that this repository is responsible for delivering.
> This is the primary signal Copilot uses to decide whether a story belongs in this repo's subfolder.
> If a story's FR-NNN appears here, this repo gets a subfolder for that story.
> If a story's FR-NNN is not listed here, Copilot falls back to the Responsibility description to infer relevance.

- {{FR-NNN — one line description of what this repo delivers for that requirement}}
- {{FR-NNN — …}}

## Responsibility

What this repository owns — one sentence per concern:

- {{e.g. Exposes the REST API surface for the Admin Portal}}
- {{e.g. Owns the application database schema and migrations}}
- {{e.g. Handles Azure AD authentication and RBAC enforcement}}

## API contract surface

> Only fill if this repo exposes or consumes APIs relevant to the initiative. Delete section if not applicable.

- Exposes: {{list of endpoint prefixes, e.g. `/api/v1/environments`, `/api/v1/actions`}}
- Consumes: {{external APIs this repo calls, e.g. Azure Resource Manager, Azure AD Graph}}

## Relevant constraints

> Architecture rules (AR-NNN) from `architecture/architecture-rules.md` that apply specifically to this repo. Leave blank if none.

- {{AR-NNN — rule summary}}

## Notes

{{Any additional context useful for Copilot when scoping handoff tasks to this repo — e.g. monorepo structure, shared libraries, deployment pipeline specifics.}}
