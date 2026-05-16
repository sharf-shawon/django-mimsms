# Tasks: Fix GitHub Release Failure

**Input**: Design documents from \`/specs/002-fix-github-release-failure/\`

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and configuration reading.

- [X] T001 Verify \`concurrency\` settings in \`.github/workflows/release.yml\`
- [X] T002 Verify \`permissions\` settings in \`.github/workflows/release.yml\`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core synchronization rules before running the release.

- [X] T003 Ensure \`fetch-depth: 0\` is correctly applied in \`.github/workflows/release.yml checkout step

**Checkpoint**: Foundation ready - workflow is prepared for strict synchronization.

---

## Phase 3: User Story 1 - Reliable Automatic Release (Priority: P1)

**Goal**: Successfully push version bumps and tags to main without non-fast-forward errors.

**Independent Test**: Triggering the release workflow results in a successful Semantic Release step.

### Implementation for User Story 1

- [X] T004 [US1] Update \`.github/workflows/release.yml\` to add \`workflow_dispatch\` trigger
- [X] T005 [US1] Update \`.github/workflows/release.yml\` to set \`concurrency: release\` at the workflow or job level
- [X] T006 [US1] Update \`.github/workflows/release.yml\` to explicitly use \`\${{ secrets.GITHUB_TOKEN }}\` in the Semantic Release action
- [X] T007 [US1] Update \`pyproject.toml\` to set \`vcs_provider = "github"\` in \`[tool.semantic_release]\`
- [X] T008 [US1] Update \`pyproject.toml\` to use the correct repository URLs in \`[project.urls]\`

**Checkpoint**: At this point, the release workflow should handle synchronization and permissions correctly.

---

## Phase 4: User Story 2 - Consistent Build Environment (Priority: P2)

**Goal**: Ensure all necessary dependencies are present for package generation.

**Independent Test**: Running the build command manually in a clean environment produces expected artifacts.

### Implementation for User Story 2

- [X] T009 [US2] Update \`pyproject.toml\` to prepend \`python -m pip install build && \` to the \`build_command\` in \`[tool.semantic_release]\`

**Checkpoint**: The build process within the release workflow is now self-sufficient.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [X] T010 [P] Review \`.github/workflows/release.yml\` for overall syntax and correctness.
- [X] T011 [P] Review \`pyproject.toml\` for overall syntax and correctness.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 and US2 can proceed in parallel.
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Opportunities

- T010 and T011 can run in parallel.
- US1 and US2 implementation steps modify different parts of the configuration (mostly) and can logically be verified together.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2.
2. Complete Phase 3 (US1) to resolve the primary non-fast-forward and 404 errors.
3. Validate by triggering a release.

### Incremental Delivery

1. Fix synchronization and URLs (US1).
2. Fix build dependencies (US2).
