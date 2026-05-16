# Data Model: Versioning and Release

This feature manages the project's versioning and release lifecycle.

## Entities

### Version
- **Source of Truth**: `src/django_mimsms/version.py` and `pyproject.toml`
- **Format**: Semantic Versioning (SemVer) `MAJOR.MINOR.PATCH`
- **Management**: Managed by `python-semantic-release` (PSR) based on Conventional Commits.

### Release
- **Platform**: GitHub Releases & PyPI
- **Artifacts**: Source Distribution (sdist) and Wheel (bdist_wheel)
- **Metadata**: Generated from `pyproject.toml` and `README.md` (SEO Optimized)
