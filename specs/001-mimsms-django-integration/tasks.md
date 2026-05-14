---
description: "Task list template for feature implementation"
---

# Tasks: MiMSMS Django Integration

**Input**: Design documents from `/specs/001-mimsms-django-integration/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY per the project constitution. Every task list MUST include test-first implementation tasks for every user story to ensure 100% coverage and network isolation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Initialize Python package with `pyproject.toml` supporting build, pytest, and ruff
- [ ] T002 Setup `.github/workflows/ci.yml` to enforce 100% coverage and strict type checking
- [ ] T003 Create `src/django_mimsms/__init__.py` and `src/django_mimsms/version.py`
- [ ] T004 Create custom exception hierarchy in `src/django_mimsms/exceptions.py`
- [ ] T005 Create `tests/conftest.py` with respx HTTP mocking configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Implement configuration model `MiMSMSConfig` in `src/django_mimsms/config.py` using Pydantic
- [ ] T007 Add unit tests for `MiMSMSConfig` (env vars, default values) in `tests/test_config.py`
- [ ] T008 Implement `MiMSMSResponse` and API Error Models in `src/django_mimsms/models.py`
- [ ] T009 Implement `httpx` based `Transport` abstraction in `src/django_mimsms/transport.py`
- [ ] T010 Add unit tests for `Transport` in `tests/test_transport.py` (mocking with respx)
- [ ] T011 Create base `MiMSMSClient` class in `src/django_mimsms/client.py` handling authentication
- [ ] T012 Implement Django settings loader and `get_client()` factory in `src/django_mimsms/django.py`
- [ ] T013 Add unit tests for Django integration in `tests/test_django.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Sending a single SMS (Priority: P1) 🎯 MVP

**Goal**: As a developer, I want to send a single SMS to a recipient using the MiMSMS API from my Django application so that I can notify users of important events.

**Independent Test**: Can be tested by calling the `send_sms` method with valid parameters and verifying the response against documented MiMSMS success fields.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Write test for successful single SMS sending in `tests/test_client.py`
- [ ] T015 [P] [US1] Write test for single SMS validation failure (invalid number) in `tests/test_client.py`

### Implementation for User Story 1

- [ ] T016 [P] [US1] Create `SingleSmsRequest` model in `src/django_mimsms/models.py`
- [ ] T017 [US1] Implement `send_sms` method in `MiMSMSClient` (`src/django_mimsms/client.py`)
- [ ] T018 [US1] Implement `send_sms_get` method in `MiMSMSClient` (`src/django_mimsms/client.py`)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Bulk SMS Sending (Priority: P1)

**Goal**: As a developer, I want to send a single message to multiple recipients at once so that I can perform bulk notifications efficiently.

**Independent Test**: Can be tested by calling `send_one_to_many` with a list of numbers and verifying that the API request payload is correctly formatted.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T019 [P] [US2] Write tests for bulk SMS (list of numbers and comma-separated) in `tests/test_client.py`
- [ ] T020 [P] [US2] Write tests for dynamic SMS sending in `tests/test_client.py`

### Implementation for User Story 2

- [ ] T021 [P] [US2] Create `BulkSmsRequest`, `DynamicSmsRequest`, and `DynamicSmsItem` models in `src/django_mimsms/models.py`
- [ ] T022 [US2] Implement `send_one_to_many` and `send_one_to_many_get` in `MiMSMSClient` (`src/django_mimsms/client.py`)
- [ ] T023 [US2] Implement `send_dynamic_sms` in `MiMSMSClient` (`src/django_mimsms/client.py`)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Balance and Delivery Status Lookup (Priority: P2)

**Goal**: As a developer, I want to check my account balance and the delivery status of sent messages so that I can monitor usage and verify delivery.

**Independent Test**: Can be tested by calling `check_balance` and `check_dlr` and verifying the parsed response models.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T024 [P] [US3] Write tests for checking balance (POST and GET) in `tests/test_client.py`
- [ ] T025 [P] [US3] Write tests for checking DLR status in `tests/test_client.py`

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create `BalanceResponse` and DLR models in `src/django_mimsms/models.py`
- [ ] T027 [US3] Implement `check_balance` and `check_balance_get` in `MiMSMSClient` (`src/django_mimsms/client.py`)
- [ ] T028 [US3] Implement `check_dlr` in `MiMSMSClient` (`src/django_mimsms/client.py`)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T029 [P] Complete `README.md` with usage examples
- [ ] T030 Confirm 100% test coverage using `pytest --cov`
- [ ] T031 Run type checking and linting `mypy src/` and `ruff check src/`
- [ ] T032 Verify packaging build process with `python -m build`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Can start after Foundational (Phase 2)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories
