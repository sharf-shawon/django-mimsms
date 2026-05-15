# django-mimsms

A production-ready Django package for the MiMSMS bulk SMS API used in Bangladesh. Supports both plain Python and Django environments.

## Features

- **Strict Type Safety**: Fully typed with `mypy` strict checks and Pydantic v2 validation.
- **Async Support**: Efficient non-blocking I/O using `httpx`.
- **Django Integration**: Configuration via standard Django settings.
- **100% Test Coverage**: Comprehensive test suite with deterministic network isolation (`respx`).
- **Multiple API Support**: Single SMS, Bulk SMS (One-to-Many), and Dynamic SMS (DSMS).

## Installation

```bash
pip install django-mimsms
```

## Django Setup

1. Add the following to your `settings.py`:

```python
MIMSMS_USERNAME = "your_username"
MIMSMS_APIKEY = "your_apikey"
MIMSMS_SENDER_NAME = "your_sender"
```

2. Send an SMS:

```python
from django_mimsms import get_client

client = get_client()
response = client.send_sms(
    number="8801700000000",
    message="Hello from Django!"
)
print(response.trxn_id)
```

## Plain Python Usage

```python
from django_mimsms.client import MiMSMSClient

client = MiMSMSClient(
    username="user",
    apikey="key",
    sender_name="SENDER"
)
balance = client.check_balance()
print(f"Balance: {balance}")
```

## Async Usage

```python
async with MiMSMSClient(...) as client:
    response = await client.send_sms(...)
```

## License

MIT
