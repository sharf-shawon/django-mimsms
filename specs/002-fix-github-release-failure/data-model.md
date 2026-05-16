# Data Model: Release Configuration

This feature does not introduce new database entities. It modifies the CI/CD pipeline configuration.

## GitHub Release Workflow (`.github/workflows/release.yml`)

| Component | Description |
|-----------|-------------|
| `test` job | Runs linting, type checking, and unit tests. |
| `release` job | Executes `python-semantic-release` and publishes to PyPI. |
| `id-token: write` | Required for OIDC/Trusted Publishers on PyPI. |
| `contents: write` | Required for pushing tags and version bumps. |

## Semantic Release Config (`pyproject.toml`)

| Setting | Value | Description |
|---------|-------|-------------|
| `upload_to_pypi` | `false` | We use a separate GH action step for publishing. |
| `upload_to_release` | `true` | Creates a GitHub Release with build artifacts. |
| `build_command` | `python -m build` | Generates sdist and wheel. |
