# Feature Specification: MiMSMS Django Integration

**Feature Branch**: `001-mimsms-django-package`

**Created**: 2026-05-14

**Status**: Draft

**Input**: User description: "Build a django package according to the @PLAN.md that will provide a easy, reusable django and python integration for mimsms.com..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sending a single SMS (Priority: P1)

As a developer, I want to send a single SMS to a recipient using the MiMSMS API from my Django application so that I can notify users of important events.

**Why this priority**: Core functionality of the package.

**Independent Test**: Can be tested by calling the `send_sms` method with valid parameters and verifying the response against documented MiMSMS success fields.

**Acceptance Scenarios**:

1. **Given** valid MiMSMS credentials and a recipient number, **When** I call `send_sms`, **Then** the message is sent successfully and a `trxnId` is returned.
2. **Given** an invalid mobile number, **When** I call `send_sms`, **Then** a validation error is raised before any API call is made.

---

### User Story 2 - Bulk SMS Sending (Priority: P1)

As a developer, I want to send a single message to multiple recipients at once so that I can perform bulk notifications efficiently.

**Why this priority**: Essential for promotional and informational campaigns.

**Independent Test**: Can be tested by calling `send_one_to_many` with a list of numbers and verifying that the API request payload is correctly formatted.

**Acceptance Scenarios**:

1. **Given** a list of valid recipient numbers, **When** I call `send_one_to_many`, **Then** the API receives a comma-separated list of numbers and returns a success status.

---

### User Story 4 - Extensive Live Test Script (Priority: P2)

As a developer, I want a comprehensive live test script that verifies all API endpoints against the real MiMSMS server so that I can confirm production readiness.

**Why this priority**: Operational verification and troubleshooting.

**Independent Test**: Running the script should prompt for credentials, execute all API methods, and produce a summarized report of success/failure for each endpoint.

**Acceptance Scenarios**:

1. **Given** valid credentials and a receiver number, **When** I run the script, **Then** it tests Balance (POST/GET), SMS (POST/GET), Bulk (POST/GET), Dynamic SMS, and DLR lookup.
2. **Given** missing credentials, **When** I run the script, **Then** it prompts the user to enter them.

---

### Edge Cases

- **Missing CampaignId**: Ensure promotional traffic raises an error if `CampaignId` is missing.
- **API Failure**: Ensure non-2xx responses from MiMSMS are mapped to specific exceptions (e.g., `MiMSMSAPIError`).
- **Malformed JSON**: Ensure unexpected response formats raise a `MiMSMSResponseParseError`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support MiMSMS SMS sending via both POST (JSON) and GET (query-string) endpoints.
- **FR-002**: System MUST support bulk SMS and dynamic SMS (different message per recipient).
- **FR-003**: System MUST provide a Django-friendly settings loader that automatically reads `MIMSMS_*` configuration from `settings.py`.
- **FR-004**: System MUST validate all request payloads (phone numbers, transaction types, etc.) using Pydantic v2.
- **FR-005**: System MUST provide a top-level client factory for both plain Python and Django environments.
- **FR-006**: System MUST implement a delivery report (DLR) lookup mechanism using transaction identifiers.
- **FR-007**: System MUST handle all documented MiMSMS error codes (e.g., 401, 208, 206) with typed exceptions.

### Key Entities *(include if feature involves data)*

- **MiMSMSConfig**: Represents authentication and transport settings.
- **SmsRequest**: Represents the payload for sending a message.
- **MiMSMSResponse**: Represents the structured response from the API, including status and transaction ID.
- **DlrStatus**: Represents the delivery report status for a specific transaction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developer can send an SMS with fewer than 5 lines of code in a standard Django project.
- **SC-002**: 100% of line and branch coverage achieved in automated tests.
- **SC-003**: Zero external network calls made during the test suite (verified by `respx`).
- **SC-004**: System correctly parses and returns structured data for all documented MiMSMS response fields.
- **SC-005**: Package passes all strict type checking (`mypy`) and linting (`ruff`) gates.

## Assumptions

- The MiMSMS API remains stable according to the provided documentation links.
- Users of the package have a valid MiMSMS `UserName` and `Apikey`.
- The package targets Python 3.12+ and Django 5.x+.
- Phone number normalization follows the international formatting guidance provided by MiMSMS.
