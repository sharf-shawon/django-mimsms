# Tasks: Fix GitHub Release Failure

**Input**: Design documents from `/specs/002-fix-github-release-failure/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Tests are optional for this CI/CD infrastructure fix. Validation is performed by triggering the workflow.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and configuration audit.

- [x] T001 [P] Verify workflow triggers and jobs in `.github/workflows/release.yml`
- [x] T002 [P] Audit `tool.semantic_release` settings in `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 Update `permissions` in `.github/workflows/release.yml` to include `id-token: write` and `contents: write`
- [x] T004 Configure `actions/checkout@v4` with `fetch-depth: 0` in `.github/workflows/release.yml`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Reliable Automatic Release (Priority: P1) 🎯 MVP

**Goal**: Successfully push version bumps and tags to the main branch without non-fast-forward errors.

**Independent Test**: Push to `main` triggers a successful release run and creates a new tag on GitHub.

### Implementation for User Story 1

- [x] T005 [US1] Explicitly set `ref: main` in checkout step of `.github/workflows/release.yml` to fix push rejection
- [x] T006 [US1] Add `workflow_dispatch` trigger to `.github/workflows/release.yml` for manual testing
- [x] T007 [US1] Set `concurrency` group in `.github/workflows/release.yml` to prevent race conditions on the main branch
- [x] T008 [US1] Configure `vcs_provider = "github"` and `branch = "main"` in `pyproject.toml`

**Checkpoint**: At this point, User Story 1 should be fully functional; releases should tag successfully.

---

## Phase 4: User Story 2 - Consistent Build Environment (Priority: P2)

**Goal**: Ensure all necessary dependencies are present for package generation and PyPI publication.

**Independent Test**: The `release` job successfully generates artifacts and publishes to PyPI using Trusted Publishers.

### Implementation for User Story 2

- [x] T009 [US2] Update `build_command` in `pyproject.toml` to ensure `build` package is installed before building
- [x] T010 [US2] Configure `pypa/gh-action-pypi-publish` step in `.github/workflows/release.yml` to use OIDC (Trusted Publishers)

**Checkpoint**: User Story 2 is complete; the package is automatically published to PyPI.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates.

- [x] T011 [P] Review `README.md` for any outdated release instructions
- [x] T012 [P] Verify manual steps in `quickstart.md` against the final implementation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all user stories being complete

### Parallel Opportunities

- T001 and T002 can run in parallel.
- T011 and T012 can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Complete Phase 3 (US1) to resolve the primary git push rejection.
3. Validate by triggering a release (even if PyPI publish fails).

### Incremental Delivery

1. Fix git sync issues (US1).
2. Fix PyPI publication (US2).
