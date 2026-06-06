# Architecture Draft — Onboarding Approval

## Document Metadata
- Source document: Example architecture draft
- Version: 0.1
- Date: Example
- Author: Architecture
- Architecture owner: Tech Lead
- Status: Draft

## Original Structure

Existing application has:
- React frontend
- .NET backend API
- SQL Server database
- Existing audit service
- Existing role-based authorization

The proposed design should reuse:
- existing API conventions
- existing audit service
- existing role-based authorization

## Components / Systems Mentioned

- React frontend
- .NET backend API
- SQL Server
- Audit service
- Authorization service / role model

## Security / Authorization Notes

The design should reuse existing role-based authorization.

## Audit / Logging / Observability Notes

The design should reuse the existing audit service.

## Architecture Assumptions Found in Original Document

- Existing audit service can support onboarding status changes.
- Existing authorization model can represent Relationship Manager and Compliance roles.

## Open Questions Found in Original Document

- Exact audit event payload not defined.
- Exact database schema not defined.
