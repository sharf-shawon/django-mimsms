# Research: Automatic Versioning, Deployment, and SEO

## Automatic Versioning and Deployment

### Decision: `python-semantic-release` (PSR)
- **Rationale**: PSR automates the entire release process: version bumping, changelog generation, and PyPI publishing based on Conventional Commits. It integrates perfectly with GitHub Actions and ensures that versioning only happens after tests pass on the `main` branch.
- **Alternatives considered**:
  - `setuptools_scm`: Good for tag-based versioning but doesn't automate the bumping or changelog.
  - Manual bumping: Error-prone and doesn't satisfy the "automatic" requirement.

### Deployment: PyPI Trusted Publishing
- **Rationale**: Modern, secure method using OpenID Connect (OIDC). Eliminates the need for storing PyPI tokens in GitHub Secrets.
- **Workflow**:
  1. Test job (Lints + Tests).
  2. Release job (PSR) runs only if Test job succeeds and on `main` branch.

## SEO Optimization

### Keywords
- Primary: `django-mimsms`, `mimsms sms api`, `django sms integration`
- Secondary: `bulk sms bangladesh`, `mimsms.com python`, `dynamic sms api`, `sms gateway django`

### Strategies
- **README Title**: Use a descriptive title: `django-mimsms: MiMSMS SMS API Integration for Django & Python`.
- **PyPI Description**: Ensure the first paragraph is keyword-rich and explains the value proposition clearly.
- **Badges**: Use PyPI, License, and CI status badges to build trust.
- **Metadata**: Populate `project.urls` in `pyproject.toml` (Documentation, Repository, Bug Tracker).

## Implementation Details

### GitHub Actions Workflow
- Name: `CI/CD`
- Triggers: `push` to `main`, `pull_request` to `main`.
- Jobs:
    - `test`: Run `ruff`, `mypy`, `pytest`.
    - `release`: Depends on `test`. Runs only on `main` branch. Uses `python-semantic-release/python-semantic-release@v9`.

### Versioning Setup
- PSR requires `pyproject.toml` configuration to know where to bump the version (e.g., `src/django_mimsms/version.py`).
