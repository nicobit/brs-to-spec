# Prompt 07 - Port Artifact Templates

## Goal

Port the artifact templates needed by `.b2s` from `.brs2spec2`.

## Files to create

Create `.b2s/artifact-templates/` and copy/adapt the templates needed for the
first thin slice:

- business-intake-summary
- requirements
- use-case diagram
- delivery structure
- readiness check

Add more templates if they are needed by the stage graph.

## Requirements

- preserve output structure and headings from `.brs2spec2`
- update framework-relative paths from `.brs2spec2` to `.b2s` where needed
- keep the artifacts business/output compatible with the current `.brs2spec2` target

## Verification

Verify:

1. templates exist at `.b2s/artifact-templates/`
2. template structure matches `.brs2spec2` output expectations
3. no stale `.brs2spec2` path references remain unless intentionally preserved
