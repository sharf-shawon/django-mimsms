# Quickstart: Fix GitHub Release Failure

This feature fixes the automated release pipeline by ensuring branch synchronization and correct token permissions.

## Verification Steps

### 1. Token Setup (If using GH_TOKEN)
Ensure your Personal Access Token (`GH_TOKEN`) has the **`repo`** scope (for Classic PAT) or **`Contents: Write`** (for Fine-grained PAT).

### 2. Trigger a Release
1. Commit a change with a Conventional Commit message (e.g., `feat: add new feature`).
2. Push to the `main` branch.
3. Navigate to **Actions** in your GitHub repository.
4. Monitor the **Release** workflow.

### 3. Verify Success
- The **Semantic Release and Publish** job should complete successfully.
- A new tag should be created in the repository.
- A new GitHub Release should be visible.
- The version in `pyproject.toml` should be updated.
- (If configured) The package should be published to PyPI.

## Troubleshooting
If you still see "non-fast-forward", check if any other workflows or users are pushing to `main` concurrently. The `concurrency` configuration should prevent this.
