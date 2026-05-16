# Data Model: CI/CD Fix

This feature modifies the CI/CD pipeline infrastructure.

## Components

### Release Workflow
- **File**: `.github/workflows/release.yml`
- **Responsibility**: Orchestrates testing, versioning, and deployment.
- **Key Settings**: Concurrency, Permissions, Checkout depth.

### Semantic Release Configuration
- **File**: `pyproject.toml`
- **Responsibility**: Defines how versioning and VCS interaction (commits/tags) are handled.
