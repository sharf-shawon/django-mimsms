# django-mimsms: MiMSMS SMS API Integration for Django & Python

[![PyPI version](https://img.shields.io/pypi/v/django-mimsms.svg)](https://pypi.org/project/django-mimsms/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/mimsms/django-mimsms/actions/workflows/ci.yml/badge.svg)](https://github.com/mimsms/django-mimsms/actions)

Seamlessly integrate **MiMSMS.com SMS API** into your Django and Python applications. This package provides a robust, type-safe, and asynchronous client for sending SMS, bulk messages, and tracking delivery reports in Bangladesh.

## Key Features

- **Strict Type Safety**: Fully typed with `mypy` strict checks and Pydantic v2 validation.
- **Async Support**: Efficient non-blocking I/O using `httpx`.
- **Django Integration**: Configuration via standard Django settings.
- **100% Test Coverage**: Comprehensive test suite with deterministic network isolation (`respx`).
- **Multiple API Support**: Single SMS, Bulk SMS (One-to-Many), and Dynamic SMS (DSMS).

## Installation

Install the package via `pip` or `uv`:

```bash
# Using pip
pip install django-mimsms

# Using uv
uv add django-mimsms
```

## Django Integration

### 1. Add to `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...,
    "django_mimsms",
]
```

### 2. Configure Settings

Add your MiMSMS credentials to your `settings.py`:

```python
# settings.py
MIMSMS_API_KEY = "your_api_key"
MIMSMS_SENDER_ID = "your_sender_id"
MIMSMS_USERNAME = "your_username"
```

### 3. Usage

```python
from django_mimsms import send_sms

# Send a simple SMS
response = send_sms(
    to="88017XXXXXXXX",
    message="Hello from Django!",
)

print(response.trxnId)
```

## Plain Python Usage

If you're not using Django, you can use the `MiMSMSClient` directly:

```python
import asyncio
from django_mimsms import MiMSMSClient

async def main():
    client = MiMSMSClient(
        api_key="your_api_key",
        username="your_username",
        sender_id="your_sender_id"
    )
    
    response = await client.send_sms(
        to="88017XXXXXXXX",
        message="Hello from Python!",
    )
    print(response.trxnId)

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Features

### Bulk SMS
Send the same message to multiple recipients:

```python
from django_mimsms import send_bulk_sms

send_bulk_sms(
    numbers=["88017XXXXXXXX", "88018XXXXXXXX"],
    message="Bulk message testing",
)
```

### Dynamic SMS
Send different messages to different recipients in one call:

```python
from django_mimsms import send_dynamic_sms

messages = [
    {"to": "88017XXXXXXXX", "message": "Hi Alice!"},
    {"to": "88018XXXXXXXX", "message": "Hi Bob!"},
]

send_dynamic_sms(messages)
```

## License

MIT
