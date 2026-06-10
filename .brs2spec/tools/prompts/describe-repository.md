# Prompt — Describe Repository

## Role

You are a solution architect analysing a code repository to produce a structured descriptor file for use in the brs-to-spec framework.

## When to use

Run this prompt **inside a target repository** when an initiative in your brs-to-spec workspace spans multiple repositories. The output is a descriptor file that you copy into `input/repositories/` in the initiative workspace. The file name you choose becomes the subfolder name in the OpenSpec handoff.

This prompt is a standalone utility — it is not part of the delivery workflow stages. Run it once per repository that the initiative touches.

## What to analyse

Read the following from the current repository (read what exists — skip gracefully if absent):

- `README.md` or `docs/` — purpose, ownership, high-level description
- `package.json`, `*.csproj`, `pyproject.toml`, `go.mod`, `pom.xml`, or equivalent — language, framework, runtime, dependencies
- `Dockerfile`, `docker-compose.yml`, `.azure/`, `infra/`, `terraform/` — infrastructure and deployment
- `src/` or top-level source structure — what the repo owns (API routes, UI components, database migrations, background workers)
- `openapi.yaml`, `swagger.json`, or equivalent — API contract surface if present
- `CODEOWNERS`, `OWNERS`, or CI config — owning team

## Output

Produce a filled descriptor file using the template below. Choose a short alias for the file name — this alias becomes the subfolder name in the handoff (e.g. `api`, `ui`, `db`, `worker`).

Tell the user: "Save this file as `input/repositories/{{alias}}.md` in your brs-to-spec initiative workspace."

## Template

```markdown
# Repository Descriptor — {{alias}}

> File name = folder name used in OpenSpec handoff subfolders (e.g. `api.md` → `F-XXX.X-slug/api/`)
> Do not rename this file after handoff generation has started — the folder name is derived from the file name.

## Identity

| Field | Value |
|---|---|
| Repository name | {{actual repo name}} |
| Short alias | {{alias — matches this file's name without extension}} |
| Remote URL / path | {{remote URL or leave blank}} |
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

> List the FR-NNN identifiers from the initiative BRS that this repository is responsible for delivering.
> This is the primary signal used to decide whether a story belongs in this repo's subfolder during handoff generation.
> If FR-NNN IDs are not yet known, leave this section with a note — fill it before running the handoff.

- {{FR-NNN — one line description of what this repo delivers for that requirement}}

## Responsibility

What this repository owns — one sentence per concern:

- {{e.g. Exposes the REST API surface for the Admin Portal}}
- {{e.g. Owns the application database schema and migrations}}
- {{e.g. Handles Azure AD authentication and RBAC enforcement}}

## API contract surface

> Only fill if this repo exposes or consumes APIs relevant to the initiative. Delete section if not applicable.

- Exposes: {{list of endpoint prefixes, e.g. /api/v1/environments}}
- Consumes: {{external APIs this repo calls}}

## Relevant constraints

> Architecture rules (AR-NNN) from the initiative's architecture/architecture-rules.md that apply specifically to this repo. Leave blank if not yet known.

- {{AR-NNN — rule summary}}

## Notes

{{Any additional context useful for scoping handoff tasks to this repo.}}
```

## Quality bar

A good descriptor:
- Has a short alias that clearly identifies the repo's role (not the full repo name)
- Lists at least one responsibility sentence so inference can fall back to it
- Has the Functional areas section filled or explicitly marked as "fill before handoff"
- Does not invent FR-NNN IDs — leave blank if the initiative BRS has not been read

## After producing the descriptor

Tell the user:
1. Save the file as `.brs2spec/tools/prompts/` is not the destination — save it to `input/repositories/{{alias}}.md` inside the initiative workspace
2. Repeat for each repository the initiative touches
3. The handoff prompt will read all files in `input/repositories/` and use them to generate per-repo subfolders
