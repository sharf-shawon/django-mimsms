# Quickstart: Publishing to PyPI via GitHub Actions

Follow these steps to successfully publish `django-mimsms` to PyPI.

## Step 1: Configure PyPI Trusted Publishers

1. Log in to your [PyPI account](https://pypi.org/manage/account/).
2. Go to **Publishing** > **Add a new publisher**.
3. Select **GitHub**.
4. Fill in the details:
   - **Owner**: `sharf-shawon`
   - **Repository**: `django-mimsms`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi` (optional, but recommended)
5. Click **Add**.

## Step 2: Update GitHub Workflow Permissions

Ensure your `.github/workflows/release.yml` has the necessary permissions:

```yaml
permissions:
  id-token: write
  contents: write
```

## Step 3: Fix "Non-Fast-Forward" Error

The Semantic Release step might fail if the runner's branch is behind. Update the checkout step to ensure it's on the correct branch:

```yaml
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: main  # Explicitly use main branch
```

## Step 4: Verify `pyproject.toml`

Ensure `python-semantic-release` is configured to build artifacts but not upload them (since we use a separate action):

```toml
[tool.semantic_release]
upload_to_pypi = false
upload_to_release = true
build_command = "python -m build"
```

## Step 5: Trigger a Release

1. Commit your changes.
2. Ensure you use [Conventional Commits](https://www.conventionalcommits.org/) (e.g., `feat: something`, `fix: something`).
3. Push to `main`.
4. The workflow will automatically trigger, bump the version, create a tag, and publish to PyPI.
