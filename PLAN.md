You are a senior Python/Django engineer. Generate a complete, production-ready Django package named `django-mimsms` that provides full support for the MiMSMS bulk SMS API used in Bangladesh.

The implementation must be based on the public MiMSMS source API documentation and sandbox:

- MiMSMS API docs: https://www.mimsms.com/api-documentation
- MiMSMS docs repository: https://github.com/mimsms/mimsms-api-docs
- MiMSMS raw OpenAPI-style JSON: https://raw.githubusercontent.com/mimsms/mimsms-api-docs/refs/heads/main/mimsms-api.json
- MiMSMS sandbox: https://apidoc.mimsms.com

The docs show that MiMSMS uses:
- Base URL: `https://api.mimsms.com`
- JSON requests and JSON responses
- POST and some GET query-string variants
- Authentication through `UserName` and `Apikey`
- Required request fields such as `MobileNumber`, `SenderName`, `TransactionType`, `Message`
- Optional `CampaignId`, mandatory for promotional traffic
- `TransactionType` values:
  - `T` = transactional
  - `P` = promotional
  - `D` = dynamic
- `trxnId` as the transaction identifier used for later query/DLR lookups
- documented error/status code behavior and DLR/operator statuses. [page:1]

Design the package so it is usable from:
- plain Python code,
- Django projects,
- background jobs and task queues,
- automated test environments with mocked HTTP.

Use the following stack exactly:
- Python 3.12
- Django 5.x
- httpx for HTTP transport
- pydantic v2 for request/response models and validation
- pytest for testing
- pytest-cov for coverage
- respx for HTTP mocking
- ruff for formatting and linting
- mypy for type checking
- GitHub Actions for CI/CD

Do not use Django REST Framework unless absolutely necessary. Keep the package focused on a reusable API client and Django integration layer.

## Goals

Build a fully typed, robust, and well-tested Django package that:

1. Implements every public MiMSMS endpoint surfaced by the docs and sandbox.
2. Supports both JSON-body and query-string request styles where documented.
3. Provides a Django-friendly settings loader and optional service wrapper.
4. Includes deterministic, isolated tests with no live network dependency.
5. Achieves 100% line and branch test coverage enforced by CI.
6. Includes documentation and examples for all user-facing features.

## Documented MiMSMS surface to support

Implement support for the following API operations, matching the documented endpoint paths and request styles. [page:1]

### SMS sending
1. `POST /api/SmsSending/SMS`
   - Send a single SMS as JSON.
   - Required fields: `UserName`, `Apikey`, `MobileNumber`, `SenderName`, `TransactionType`, `Message`.
   - Support optional `CampaignId`.
   - Validate international phone number formatting guidance from the docs.
   - Response parsing must handle the documented JSON response fields:
     - `statusCode`
     - `status`
     - `trxnId`
     - `responseResult`

2. `POST /api/SmsSending/OneToMany`
   - Send one message to multiple recipients.
   - Accept either a list of numbers or a comma-separated string.
   - Normalize and validate numbers before sending.
   - Support the documented promotional/transactional constraints.

3. `POST /api/SmsSending/DSMS`
   - Send dynamic SMS.
   - Accept `SmsData` as a list of per-recipient payloads.
   - Each item must include `MobNumber` and `Message`.
   - `TransactionType` must be `D`.

### Query-string / plain HTTP variants
4. `GET /api/SmsSending/Send`
   - Query-string equivalent for sending a single SMS.
   - Serialize parameters exactly as documented.

5. `GET /api/SmsSending/SendOneToMany`
   - Query-string equivalent for sending one message to many recipients.
   - Serialize parameters exactly as documented.

### Balance
6. `POST /api/SmsSending/balanceCheck`
   - JSON request with `UserName` and `Apikey`.
   - Parse balance from `responseResult`.

7. `GET /api/SmsSending/balanceCheck`
   - Query-string variant of balance check.

### DLR / status lookup
8. Implement a delivery report lookup method based on the documented DLR/status workflow and the `trxnId` returned by send requests.
   - If the raw JSON spec includes an explicit DLR endpoint, implement it exactly.
   - If the docs are incomplete, provide a clean abstraction that maps to the documented DLR usage with the most faithful endpoint path available in the spec.
   - Parse operator statuses such as Delivered, Undelivered, Subscriber Busy, System failure, SMSC Timeout-abort, etc., as structured data.

## Package architecture

Create a `src/`-layout package with clean module boundaries:

- `src/django_mimsms/__init__.py`
- `src/django_mimsms/client.py`
- `src/django_mimsms/config.py`
- `src/django_mimsms/exceptions.py`
- `src/django_mimsms/models.py`
- `src/django_mimsms/transport.py`
- `src/django_mimsms/service.py`
- `src/django_mimsms/django.py`
- `src/django_mimsms/version.py`

Also include:
- `tests/`
- `.github/workflows/ci.yml`
- `pyproject.toml`
- `README.md`
- `LICENSE`

## Client requirements

Implement a top-level client class, e.g. `MiMSMSClient`, that exposes methods such as:

- `send_sms(...)`
- `send_one_to_many(...)`
- `send_dynamic_sms(...)`
- `send_sms_get(...)`
- `send_one_to_many_get(...)`
- `check_balance(...)`
- `check_dlr(...)` or the closest documented equivalent

The client must:
- use `httpx.Client` internally,
- accept dependency injection of the HTTP client/transport,
- support timeouts and TLS verification configuration,
- set `Content-Type: application/json` and `Accept: application/json` where required,
- support base URL overrides,
- be safe for reuse across requests,
- expose raw responses when needed and parsed typed results by default.

## Configuration requirements

Create a `MiMSMSConfig` model with validation and environment support.

Required config fields:
- `username`
- `apikey`
- `sender_name`
- `base_url` defaulting to `https://api.mimsms.com`
- `timeout`
- `verify_ssl`
- `default_transaction_type`
- optional `campaign_id`

Provide configuration loading from:
- explicit constructor arguments,
- Django settings,
- environment variables.

Django settings keys must include:
- `MIMSMS_USERNAME`
- `MIMSMS_APIKEY`
- `MIMSMS_SENDER_NAME`
- `MIMSMS_BASE_URL`
- `MIMSMS_TIMEOUT`
- `MIMSMS_VERIFY_SSL`
- `MIMSMS_DEFAULT_TRANSACTION_TYPE`
- `MIMSMS_CAMPAIGN_ID` optional

## Validation requirements

Use pydantic v2 models to validate and normalize all requests and responses.

Validate:
- usernames and API keys are present,
- sender name is present,
- phone numbers are non-empty and normalized,
- list inputs are normalized to comma-separated values only when appropriate,
- `TransactionType` is one of `T`, `P`, `D`,
- `CampaignId` is required for promotional SMS,
- dynamic SMS items each include a destination and message,
- query-style methods produce the exact documented parameter names,
- unexpected or malformed responses raise explicit parse errors.

## Response models

Create typed models for:
- send response
- balance response
- DLR response
- operator status result
- API error response

Map the documented MiMSMS response fields:
- `statusCode`
- `status`
- `trxnId`
- `responseResult`

For error handling, support the documented error status map including:
- 401 unauthorized variants
- 208 invalid sender ID
- 205 invalid message content
- 206 invalid mobile number
- 209 SMS length over max
- 221 sending failed
- 213 parameter mismatch
- 216 insufficient balance
- 210 invalid campaign ID
- 207 invalid transaction type
- 500 internal server error. [page:1]

## Error handling requirements

Create a strong exception hierarchy:
- `MiMSMSException`
- `MiMSMSConfigurationError`
- `MiMSMSValidationError`
- `MiMSMSTransportError`
- `MiMSMSHTTPError`
- `MiMSMSAPIError`
- `MiMSMSResponseParseError`

The client must:
- raise typed exceptions for HTTP failures, transport failures, invalid payloads, and malformed API responses,
- preserve the original exception as the cause,
- include status codes and response bodies when appropriate,
- avoid leaking sensitive credentials in exception messages.

## Django integration requirements

Implement a Django integration layer that provides:
- a settings-based client factory,
- an optional service class that can be injected into views, tasks, or management commands,
- a helper for creating a singleton-style client from Django settings,
- no import-time side effects.

The package should work with:
- `from django_mimsms import get_client`
- `MiMSMSService` or equivalent service wrapper
- explicit client injection for testability

## Transport requirements

Use `httpx` and design a small transport abstraction so tests can mock every network path cleanly.

Support:
- `POST` with JSON body,
- `GET` with query parameters,
- timeout configuration,
- SSL verification configuration,
- custom headers,
- deterministic serialization order where useful for tests.

Do not implement retries unless they are well justified and fully tested. If retries are implemented, they must be configurable and covered.

## Testing requirements

Use `pytest`, `pytest-cov`, and `respx`.

Write tests for:
- every public method,
- every validation rule,
- all response parsers,
- all exception branches,
- both JSON and GET variants,
- Django settings loading,
- transport injection,
- edge cases such as:
  - empty recipient list,
  - invalid mobile numbers,
  - invalid transaction type,
  - missing campaign ID for promotional SMS,
  - malformed JSON responses,
  - non-2xx HTTP responses,
  - API error payloads,
  - balance parsing,
  - DLR/operator status parsing.

Testing rules:
- no external network calls,
- deterministic fixtures,
- minimal duplication,
- tests must exercise both success and failure cases for all branches.

Coverage rules:
- enforce 100% line coverage,
- enforce 100% branch coverage where feasible with pytest-cov,
- fail the build if coverage falls below 100%.

## CI/CD requirements

Create a GitHub Actions workflow that runs on push and pull request.

The workflow must:
- install Python 3.12,
- install package dependencies,
- run `ruff format --check`,
- run `ruff check`,
- run `mypy`,
- run `pytest --cov --cov-branch --cov-fail-under=100`,
- build the package,
- optionally run `python -m build`,
- optionally upload coverage artifacts.

Use a matrix only if it remains simple and useful. The primary goal is a reliable, fast, reproducible CI pipeline.

## Packaging requirements

Use modern packaging standards in `pyproject.toml`.

Include:
- build backend,
- project metadata,
- dependencies,
- optional extras such as `test`, `dev`, and `django`,
- tool configuration for ruff, mypy, and pytest.

Prefer:
- `setuptools` or `hatchling` if it simplifies packaging,
- pinned or constrained development dependencies,
- a clean `src` layout,
- semantic versioning.

## Documentation requirements

Write a README that includes:
- installation instructions,
- configuration examples for Django and plain Python,
- examples for all endpoints,
- a note that MiMSMS supports JSON and some GET/query-string variants,
- explanation of `trxnId`,
- explanation of transaction types `T`, `P`, and `D`,
- explanation of promotional SMS constraints and approved campaign IDs,
- notes on response/status handling,
- notes on error codes and DLR/operator statuses,
- testing and CI expectations.

## Quality requirements

The generated code must:
- be fully typed,
- follow PEP 8,
- avoid wildcard imports,
- avoid global mutable state,
- avoid hardcoded credentials,
- avoid side effects at import time,
- have docstrings for public classes and methods,
- separate transport, validation, and service logic cleanly,
- be easy to extend if MiMSMS adds endpoints later.

## Acceptance criteria

The package is complete only if:
- all documented MiMSMS API operations are implemented,
- the Django integration is functional,
- the tests pass without network access,
- coverage is 100% and enforced in CI,
- linting and type checking pass,
- the package can be built and installed,
- the README is clear and accurate,
- there are no TODOs, stubs, or placeholder implementations.

## Output format

Return:
1. All source files with complete code.
2. All test files with complete tests.
3. All config files.
4. Documentation.
5. The CI workflow.

Do not summarize the code. Do not leave any section partial.
