# Research: Fix GitHub Release Failure

## Root Cause Analysis

### non-fast-forward (rejected)
- **Problem**: The GitHub Actions runner attempts to push a version bump and tag, but the remote `main` branch has commits that the runner doesn't have.
- **Why it happens**:
    - **Race Condition**: Another PR was merged or a commit was pushed to `main` between the time the `release` job started and when PSR tried to push.
    - **Concurrency**: Multiple release workflows running in parallel.
    - **Partial Checkout**: Although `fetch-depth: 0` is used, the checkout might be tracking a specific SHA rather than the branch head in some contexts.

### Permission Issues
- **Problem**: User provided a classic token `GH_TOKEN` with "no added permissions".
- **Impact**: `python-semantic-release` REQUIRES `contents: write` to push commits and tags. Without this, even a fast-forward push would fail (though likely with a different error message like "403 Forbidden" or "Protected branch hook declined").

## Decisions

### 1. Concurrency Management
- **Decision**: Move `concurrency` to the workflow level or ensure the job-level concurrency is strict.
- **Rationale**: Prevents overlapping release attempts which are the primary source of non-fast-forward errors in automated pipelines.

### 2. Git Synchronization
- **Decision**: Ensure the branch is explicitly up-to-date before PSR runs.
- **Action**: Although `python-semantic-release` action handles checkout, sometimes a manual `git pull origin main --rebase` or similar is needed if the environment has diverged. However, the PSR action usually handles this if configured correctly.
- **Alternative**: Use the built-in `GITHUB_TOKEN` which is better integrated for internal actions, provided permissions are set.

### 3. Token Scopes
- **Decision**: Advise the user that `GH_TOKEN` MUST have `repo` scope (for classic PAT) or `contents: write` (for fine-grained PAT).
- **Alternative**: Prefer the built-in `GITHUB_TOKEN` with `permissions: contents: write` in the YAML, which is more secure and less prone to configuration drift.

## Alternatives Considered

- **Force Push**: Absolutely rejected. Would destroy history and bypass safety checks.
- **Disable Commits**: Only release tags. Rejected because we want the version bump in `pyproject.toml` and the `CHANGELOG.md` to be persisted in the repo.
