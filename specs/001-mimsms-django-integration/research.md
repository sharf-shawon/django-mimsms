# Research: MiMSMS Django Integration

## MiMSMS API Analysis

### Authentication
- **Method**: Authentication via `UserName` and `Apikey` in request body (JSON) or query string (GET).
- **Base URL**: `https://api.mimsms.com`

### Endpoints
1.  **Single SMS (JSON)**: `POST /api/SmsSending/SMS`
2.  **Bulk SMS (One-to-Many)**: `POST /api/SmsSending/OneToMany`
3.  **Dynamic SMS (DSMS)**: `POST /api/SmsSending/DSMS`
4.  **Single SMS (GET)**: `GET /api/SmsSending/Send`
5.  **Bulk SMS (GET)**: `GET /api/SmsSending/SendOneToMany`
6.  **Balance Check (JSON)**: `POST /api/SmsSending/balanceCheck`
7.  **Balance Check (GET)**: `GET /api/SmsSending/balanceCheck`

### Request Models
- **Common Fields**: `UserName`, `Apikey`
- **SMS Fields**: `MobileNumber`, `SenderName`, `TransactionType` (T/P/D), `Message`, `CampaignId` (optional/mandatory for P)
- **One-to-Many**: `MobileNumber` (comma separated or list)
- **DSMS**: `SmsData` (list of `MobNumber` and `Message`)

### Response Models
- **Fields**: `statusCode`, `status`, `trxnId`, `responseResult`
- **Error Codes**: 401 (Auth), 208 (Invalid Sender), 206 (Invalid Number), 216 (Insufficient Balance), etc.

## Technology Best Practices

### httpx Transport
- **Decision**: Use `httpx.Client` (sync) and `httpx.AsyncClient` (async) via a shared transport layer.
- **Rationale**: Original requirement specified `httpx`. Providing both sync and async capabilities ensures maximum flexibility.

### Django Settings Loader
- **Decision**: Use a lazy settings loader in `django_mimsms.django`.
- **Rationale**: Avoids import-time side effects. Provides a `get_client()` factory that initializes from `settings.MIMSMS_*`.

### Pydantic v2 Validation
- **Decision**: Use `pydantic.BaseModel` with `Field` for alias mapping (e.g., `UserName` -> `username`).
- **Rationale**: MiMSMS uses PascalCase in API, while Python prefers snake_case. Pydantic aliases handle this cleanly.

### Testing with respx
- **Decision**: Use `respx` to mock `httpx` calls.
- **Rationale**: Lightweight and integrates perfectly with `pytest` and `httpx`. Ensures 100% network isolation.

## Decision Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transport | httpx | Modern, async-ready, requested in requirements. |
| Validation | Pydantic v2 | Robust, fast, excellent type support. |
| Structure | src/ layout | Standard for modern Python packages. |
| Mocking | respx | Native to httpx ecosystem. |
