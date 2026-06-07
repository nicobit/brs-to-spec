# Architecture Review

## Summary

The feature fits the existing onboarding platform if it reuses the identity provider, API gateway, document storage service, and audit event pipeline.

## Constraints

- no new identity system
- no direct client write access to document storage
- approval events must be auditable
