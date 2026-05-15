<!--
Sync Impact Report:
- Version change: [INITIAL] → 1.1.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] → I. Strict Type Safety & Pydantic Validation
  - [PRINCIPLE_2_NAME] → II. 100% Coverage & Network Isolation
  - [PRINCIPLE_3_NAME] → III. Django-Idiomatic Integration
  - [PRINCIPLE_4_NAME] → IV. Efficient Asynchronous Transport
  - [PRINCIPLE_5_NAME] → V. Minimalistic & Extensible Design
  - [NEW] → VI. Source of Truth for API Implementation
- Added sections: Core Principles, Governance
- Removed sections: None
- Templates requiring updates (✅ updated / ⚠ pending):
  - .specify/templates/plan-template.md ✅
  - .specify/templates/spec-template.md ✅ (Standard alignment)
  - .specify/templates/tasks-template.md ✅ (Standard alignment)
- Follow-up TODOs: None
-->

# django-mimsms Constitution

## Core Principles

### I. Strict Type Safety & Pydantic Validation
The codebase MUST be fully typed and pass `mypy` strict checks. All API request and response data MUST be validated using Pydantic v2 models to ensure structural integrity and early error detection. Follow PEP 8 and use `ruff` for consistent formatting and linting.

**Rationale**: Ensures maintainability, reduces runtime errors, and provides a clear contract for API interactions.

### II. 100% Coverage & Network Isolation
Every public method and edge case MUST be tested with `pytest`. 100% line and branch coverage is NON-NEGOTIABLE and enforced by CI. Tests MUST NOT make external network calls; use `respx` for deterministic HTTP mocking.

**Rationale**: Guarantees reliability and prevents regressions without dependency on third-party API availability.

### III. Django-Idiomatic Integration
Provide a consistent experience for both Django and plain Python users. Configuration MUST be loadable from Django settings, environment variables, or explicit constructor arguments. Exceptions MUST follow a clear, documented hierarchy (e.g., `MiMSMSException`).

**Rationale**: Minimizes friction for developers and ensures predictable behavior across different deployment environments.

### IV. Efficient Asynchronous Transport
Use `httpx` for all HTTP communication to support efficient, non-blocking requests. The package MUST be safe for use in background tasks and high-concurrency environments. Avoid import-time side effects and global mutable state.

**Rationale**: Optimizes resource usage and ensures the package scales with the host application.

### V. Minimalistic & Extensible Design
Keep the package focused on the MiMSMS API. Do not add unnecessary dependencies or complex abstractions. Follow the `src/` layout for clean module boundaries and ease of extension for future API endpoints.

**Rationale**: Lowers the barrier for contributions and simplifies long-term maintenance.

### VI. Source of Truth for API Implementation
All API implementations MUST align with the official MiMSMS documentation. The following URLs are the primary sources of truth:
- https://www.mimsms.com/api-documentation
- https://apidoc.mimsms.com/
- https://github.com/mimsms/mimsms-api-docs

Any ambiguity in implementation MUST be resolved by referring to these URLs as the primary sources of truth.

**Rationale**: Ensures consistency with the provider's standards and reduces maintenance overhead caused by guessing or outdated documentation.

## Governance
Constitution v1.1.0 supersedes all previous practices. All PRs MUST pass CI (Lint, Types, Tests). Versioning follows SemVer. Amendments require a version bump in this document.

1. **Compliance**: All code changes must align with core principles.
2. **Review**: Peer reviews should explicitly check for adherence to these standards.
3. **Evolution**: Principles can be updated as the project scales, provided they maintain or improve quality.

**Version**: 1.1.0 | **Ratified**: 2026-05-14 | **Last Amended**: 2026-05-15
