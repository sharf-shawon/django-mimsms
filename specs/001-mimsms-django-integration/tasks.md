# Tasks: Automatic Versioning and Deployment

**Input**: Design documents from `/specs/001-mimsms-django-integration/`

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for automatic versioning and deployment.

- [x] T001 Initialize `python-semantic-release` configuration in `pyproject.toml`
- [x] T002 [P] Create `src/django_mimsms/version.py` to store the version string

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration needed for versioning and CI/CD pipelines.

- [x] T003 Configure `python-semantic-release` to track `src/django_mimsms/version.py` and `pyproject.toml`
- [x] T004 [P] Create base `.github/workflows/release.yml` for the release pipeline

**Checkpoint**: Infrastructure ready for story-specific implementation.

---

## Phase 3: User Story 1 - SEO-Optimized Documentation (Priority: P1)

**Goal**: Enhance package discoverability and provide clear usage instructions.

**Independent Test**: Verify `README.md` contains targeted keywords and renders correctly with all sections.

- [x] T005 [P] [US1] Update `pyproject.toml` with SEO metadata (description, keywords, project URLs)
- [x] T006 [P] [US1] Generate `README.md` incorporating content from `quickstart.md` and SEO keywords
- [x] T007 [P] [US1] Add shields.io badges for PyPI, License, and CI status to `README.md`

**Checkpoint**: Documentation is SEO-optimized and ready for users.

---

## Phase 4: User Story 2 - Automatic Versioning (Priority: P1)

**Goal**: Automate version bumps and changelog generation using Conventional Commits.

**Independent Test**: Verify that PSR can correctly calculate the next version via dry-run in CI.

- [x] T008 [US2] Configure GitHub Actions permissions and environment for versioning in `.github/workflows/release.yml`
- [x] T009 [US2] Implement version bumping and changelog generation steps in `.github/workflows/release.yml`

**Checkpoint**: Versioning is automated on the main branch.

---

## Phase 5: User Story 3 - Automatic Deployment (Priority: P1)

**Goal**: Securely publish the package to PyPI upon successful tests and versioning.

**Independent Test**: Successful "publish" job run (verified via dry-run or test PyPI).

- [x] T010 [P] [US3] Add OIDC Trusted Publishing permissions to `.github/workflows/release.yml`
- [x] T011 [US3] Implement PyPI publication step in `.github/workflows/release.yml` dependent on test success

**Checkpoint**: Automated deployment pipeline is fully functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T012 [P] Run `ruff` and `mypy` to ensure code quality standards are maintained
- [x] T013 [P] Validate `README.md` rendering on GitHub and local preview
- [x] T014 [P] Perform final metadata verification in `pyproject.toml`

---

## Dependencies & Execution Order

### Phase Dependencies
- **Phase 1 (Setup)**: No dependencies.
- **Phase 2 (Foundational)**: Depends on Phase 1 completion.
- **User Stories (Phase 3-5)**: Depend on Phase 2 completion.
  - US1, US2, and US3 can proceed in parallel once Phase 2 is done.
- **Phase 6 (Polish)**: Depends on all user stories being complete.

### Parallel Opportunities
- T002, T004, T005, T006, T007, T010 are all parallelizable.
- Once Phase 2 is complete, US1, US2, and US3 implementation can run in parallel if multiple developers are available.

---

## Implementation Strategy

### MVP First (User Story 1 + 2)
1. Complete Setup and Foundational phases.
2. Implement US1 (Documentation) and US2 (Versioning).
3. Verify versioning works before adding deployment.

### Incremental Delivery
1. **Milestone 1**: Documentation optimized (US1).
2. **Milestone 2**: Automatic versioning active (US2).
3. **Milestone 3**: Full CI/CD with PyPI deployment (US3).
