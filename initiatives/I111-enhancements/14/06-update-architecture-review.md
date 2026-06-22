# Prompt 06 — Update Architecture Review to Seed Integration List

## Context

You are working on the `.b2s` framework at the root of this repository.

The architecture review is the first place external systems are identified.
Currently it lists them in the "Impacted Systems" table but does not produce
a structured integration list that downstream skills can consume reliably.

This prompt updates:
1. The `architecture-review.md` artifact template to include an explicit Integration Inventory section
2. The `review-initial-architecture` skill to populate this section
3. The architecture review skill prompt to produce `api_contract_mode` as a recommendation

Before making changes, read these files in full:
- `.b2s/artifact-templates/architecture-review.md`
- `.b2s/skills/architect/review-initial-architecture.md`

---

## Step 1 — Update architecture-review.md artifact template

Read `.b2s/artifact-templates/architecture-review.md` in full.

Add a new section **Integration Inventory** after the existing "Brownfield Impact" section:

```markdown
## Integration Inventory

List every external system this initiative integrates with. This section seeds
`technical-specifications/api/consumed/` and `technical-specifications/integrations/`.

| System | Direction | Protocol | Auth | Enterprise contract | Spec available | Stories |
|---|---|---|---|---|---|---|
| {{system name}} | {{consumed / exposed / bidirectional}} | {{HTTPS / AMQP}} | {{OAuth2 / API key}} | {{yes — ARCH-C-NNN / no}} | {{yes / no / partial}} | {{F-NNN.N, F-NNN.N}} |

## API Contract Mode Recommendation

| Field | Value |
|---|---|
| Recommended api_contract_mode | {{product / internal / coordinated}} |
| Rationale | {{one sentence explaining why}} |
| External consumers identified | {{yes / no}} |
| Parallel teams sharing API surface | {{yes / no}} |
```

---

## Step 2 — Update review-initial-architecture skill

Read `.b2s/skills/architect/review-initial-architecture.md` in full.

Add instructions to populate the two new sections:

**For Integration Inventory:**
- List every external system mentioned in the BRS or architecture input
- Determine direction from context: "call Experian" = consumed, "expose API to partner" = exposed
- Set `Spec available` to `yes` if the provider's API documentation is referenced in the BRS,
  `partial` if only partially described, `no` if unknown
- Map each system to the stories that use it using delivery-structure.md if available

**For API Contract Mode Recommendation:**
- Recommend `product` if: the BRS mentions external consumers, partner integrations, or public APIs
- Recommend `coordinated` if: multiple teams are mentioned or the architecture review identifies shared API surfaces
- Recommend `internal` if: all API consumers are internal to this initiative
- State the rationale explicitly

---

## Step 3 — Update create-exposed-api-specs skill input

Read `.b2s/skills/engineering-lead/create-exposed-api-specs.md` (created in prompt 03).

Add `architecture/architecture-review.md` Integration Inventory as the primary source
for identifying which exposed APIs to generate specs for. The skill should:
1. Read the Integration Inventory table — find rows where direction = `exposed` or `bidirectional`
2. Read the API Contract Mode Recommendation — use it to set `contract_mode` in each spec
3. Only generate specs for systems where the initiative is the producer

---

## Step 4 — Verify

Run the full test suite:

```
python -m pytest .b2s/tests/ -q
```

All existing tests must pass. The template change does not affect existing initiatives
because `repair-state` does not re-read template content — it reads actual artifact files.

---

## Done criteria

- [ ] `architecture-review.md` template has Integration Inventory section with correct columns
- [ ] `architecture-review.md` template has API Contract Mode Recommendation section
- [ ] `review-initial-architecture` skill populates both new sections
- [ ] `create-exposed-api-specs` skill reads Integration Inventory as primary input
- [ ] All existing tests pass
