# Codebase Context

> **Owner:** Engineering Lead / Developer
> **Purpose:** Describe the existing repository so coding agents know where to work, which patterns to follow, and how to validate their output.
> **When to fill:** Before handoff generation. Can be filled incrementally — partial information is better than none.

## Repository overview

<!-- Brief description of the repository — what it does, its main layers, and its technology stack -->

| Field | Value |
|---|---|
| Repository name | |
| Primary language / framework | |
| Architecture style | e.g. Layered / Clean / Hexagonal / Microservices |
| Database technology | |
| Test framework | |
| Build tool | |

## Folder structure

<!-- Key folders only — not every directory. Focus on where new code will likely go. -->

```text
src/
  Api/             — HTTP controllers and request/response models
  Application/     — use cases, commands, queries
  Domain/          — entities, value objects, domain rules
  Infrastructure/  — DB, external service adapters
tests/
  Unit/
  Integration/
  E2E/
```

## Patterns to follow

<!-- Coding patterns, naming conventions, and structural rules the AI must respect -->
<!-- Be specific — "use the repository pattern" is not enough; name the base class or interface -->

| Pattern | Description | Example location |
|---|---|---|
| Command pattern | All write operations go through a Command + Handler | `src/Application/Onboarding/CreateOnboardingCommand.cs` |
| Repository pattern | Data access via IRepository<T> | `src/Infrastructure/Repositories/` |

## Files and areas NOT to touch

<!-- Explicit exclusions — files that must not be modified by the coding agent -->

| Path / area | Reason |
|---|---|
| `src/Infrastructure/Migrations/` | DB migrations are managed manually — do not auto-generate |
| `src/Api/Program.cs` | Startup config — requires architect review before change |

## Existing capabilities map

<!-- Which business capabilities already exist and where their code lives -->
<!-- Fill only for capabilities relevant to this initiative -->

| Capability | Module / path |
|---|---|
| Customer authentication | `src/Application/Auth/` + `src/Api/Controllers/AuthController.cs` |
| Notification sending | `src/Infrastructure/Notifications/` |

## Validation commands

<!-- Exact commands to run after implementation to verify the output is correct -->
<!-- These are copied verbatim into coding-prompt.md for each story -->

```bash
# Build
# dotnet build

# Unit tests
# dotnet test tests/Unit/ --logger "console;verbosity=normal"

# Integration tests (requires running DB)
# dotnet test tests/Integration/ --filter Category=Integration

# Lint / format check
# dotnet format --verify-no-changes
```

## Known constraints

<!-- Any additional constraints a coding agent must know that are not in architecture-rules.md -->
<!-- e.g. third-party SDK versions, deprecated patterns still in use, pending migrations -->

- {{constraint}}
