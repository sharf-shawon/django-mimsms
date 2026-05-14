# Client Contract: MiMSMSClient

The `MiMSMSClient` is the primary interface for interacting with the MiMSMS API.

## Initialization

```python
client = MiMSMSClient(
    username="my_user",
    apikey="my_key",
    sender_name="SENDER",
    **options
)
```

## Public Methods

### `send_sms`
Sends a single SMS via JSON POST.
- **Args**: `number`, `message`, `transaction_type`, `campaign_id`
- **Returns**: `MiMSMSResponse`
- **Raises**: `MiMSMSException`

### `send_one_to_many`
Sends a single message to multiple recipients via JSON POST.
- **Args**: `numbers` (List[str] or str), `message`, `transaction_type`, `campaign_id`
- **Returns**: `MiMSMSResponse`

### `send_dynamic_sms`
Sends personalized messages to multiple recipients.
- **Args**: `messages` (List[Dict[str, str]]), `transaction_type`
- **Returns**: `MiMSMSResponse`

### `check_balance`
Checks the current account balance.
- **Returns**: `float` (parsed from `responseResult`)

### `check_dlr`
Queries delivery status for a transaction.
- **Args**: `trxn_id`
- **Returns**: `DlrStatus`

## GET Variants (Optional)

### `send_sms_get`
### `send_one_to_many_get`
### `check_balance_get`
These follow the same signature as their POST counterparts but use query string serialization.
