# Enhancement 6.1 — Enrich the Repository Descriptor Template

## Problem

`input/repositories/_template.md` is currently thin. It contains:
- Identity (repo name, alias, URL, team)
- Technology (language, framework, runtime, database, infrastructure)
- Functional areas (FR-NNN list)
- Responsibility (what the repo owns)
- API contract surface (exposes/consumes)
- Relevant constraints (AR-NNN list)
- Notes

It does **not** contain:
- **Module map** — key folders with one-line responsibilities; the framework uses this to derive candidate file paths in coding-prompt.md
- **Build and test commands** — exact commands; these are the only reliable source for "Validation commands" in coding-prompt.md; guessing from tech stack name is unreliable
- **Coding standards** — patterns the AI must follow in this repo (not global AR-NNN rules — repo-specific conventions like "thin controllers", "use the existing base command class")
- **Files and areas not to touch** — explicit exclusions; currently missing entirely from the descriptor

Without these, the handoff skill's coding-prompt.md "Files to touch" is guessed from design.md narrative and "Validation commands" is guessed from the technology name. Both are overclaiming.

The `codebase-context.md` template (Enhancement 5.4) covers these same concerns for single-repo flat initiatives. For multi-repo initiatives, the per-repo descriptor should be the authoritative source.

---

## What needs to change

### Change 1 — Replace `.brs2spec/templates/repositories/_template.md`

Replace with the enriched version below. All existing sections are preserved and in the same order — new sections are appended after "Relevant constraints".

**New template content:**

```markdown
# Repository Descriptor — {{repo-name}}

> File name = folder name used in OpenSpec handoff subfolders (e.g. `api.md` → `F-XXX.X-slug/api/`)
> Do not rename this file after handoff generation has started — the folder name is derived from the file name.
> Fill what you know. Partial information is better than none — the framework will note gaps rather than block.

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
> This is the primary signal used to decide whether a story belongs in this repo's subfolder.
> If a story's FR-NNN appears here, this repo gets a subfolder for that story.
> If a story's FR-NNN is not listed here, the framework falls back to the Responsibility description to infer relevance.

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

## Module map

> Key folders and their single-line responsibility. Focus on where new code will likely go.
> This is used by the handoff skill to derive candidate file paths in coding-prompt.md.
> List only meaningful structural folders — not every directory.

| Folder | Responsibility |
|---|---|
| `{{src/Api/}}` | {{e.g. HTTP controllers and request/response models — keep thin}} |
| `{{src/Application/}}` | {{e.g. Use cases, commands, queries, orchestration logic}} |
| `{{src/Domain/}}` | {{e.g. Domain entities, value objects, domain rules — no infrastructure dependencies}} |
| `{{src/Infrastructure/}}` | {{e.g. Database adapters, external service clients, message bus}} |
| `{{tests/Unit/}}` | {{e.g. Unit tests — fast, no I/O}} |
| `{{tests/Integration/}}` | {{e.g. Integration tests — require running DB or service}} |

## Build and test commands

> Exact commands to run after implementation to verify the output is correct.
> These are copied **verbatim** into coding-prompt.md for every story in this repo — do not use placeholder names.
> Add a comment line before each command explaining what it does.

```bash
# Restore dependencies
{{dotnet restore}}

# Build
{{dotnet build}}

# Unit tests
{{dotnet test tests/Unit/ --logger "console;verbosity=normal"}}

# Integration tests (requires running DB or service)
{{dotnet test tests/Integration/ --filter Category=Integration}}

# Lint / format check
{{dotnet format --verify-no-changes}}
```

## Coding standards

> Patterns, naming conventions, and structural rules the coding agent must respect in this repo.
> Be specific — "use the repository pattern" is not enough; name the base class, interface, or example file.

| Pattern | Rule | Example location |
|---|---|---|
| {{e.g. Command pattern}} | {{All write operations go through a Command + Handler pair}} | {{`src/Application/Onboarding/CreateOnboardingCommand.cs`}} |
| {{e.g. Repository pattern}} | {{Data access only via IRepository<T> — no direct DbContext in application layer}} | {{`src/Infrastructure/Repositories/`}} |

## Files and areas not to touch

> Explicit exclusions — files or folders the coding agent must not modify.
> These are merged into the "What you must NOT do" section of every coding-prompt.md for this repo.

| Path / area | Reason |
|---|---|
| `{{src/Infrastructure/Migrations/}}` | {{e.g. DB migrations are managed manually — do not auto-generate}} |
| `{{src/Api/Program.cs}}` | {{e.g. Startup config — requires architect review before change}} |

## Relevant constraints

> Architecture rules (AR-NNN) from `architecture/architecture-rules.md` that apply specifically to this repo. Leave blank if none.

- {{AR-NNN — rule summary}}

## Notes

{{Any additional context useful for a coding agent working in this repo — e.g. monorepo structure, shared libraries, deployment pipeline specifics, known tech debt areas to avoid.}}
```

---

## Implementation steps

1. Open `.brs2spec/templates/repositories/_template.md` — replace entirely with the new template above.

## Quality bar

After this change:
- A developer fills one descriptor per repo; it is the single source of truth for that repo's structure, patterns, commands, and exclusions.
- The handoff skill can derive accurate module-map-based candidate file paths instead of guessing from design.md narrative.
- Validation commands in coding-prompt.md for Case B come verbatim from this descriptor — not inferred from the technology name.
- "What you must NOT do" in coding-prompt.md merges AR-NNN rules AND the repo-specific exclusions from this descriptor.
- `codebase-context.md` (Enhancement 5.4) remains valid for single-repo flat initiatives — the two templates cover the same concerns at different granularities.
