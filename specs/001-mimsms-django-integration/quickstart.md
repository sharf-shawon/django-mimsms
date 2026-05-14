# Quickstart: MiMSMS Django Integration

## Installation

```bash
pip install django-mimsms
```

## Django Integration

### 1. Configure Settings
Add the following to your `settings.py`:

```python
MIMSMS_USERNAME = "your_username"
MIMSMS_APIKEY = "your_apikey"
MIMSMS_SENDER_NAME = "your_sender"
```

### 2. Send an SMS
```python
from django_mimsms import get_client

client = get_client()
response = client.send_sms(
    number="8801700000000",
    message="Hello from Django!"
)
print(response.trxnId)
```

## Plain Python Usage

```python
from django_mimsms import MiMSMSClient

client = MiMSMSClient(
    username="user",
    apikey="key",
    sender_name="SENDER"
)
balance = client.check_balance()
print(f"Balance: {balance}")
```

## Async Support

```python
async with MiMSMSClient(...) as client:
    response = await client.send_sms(...)
```
