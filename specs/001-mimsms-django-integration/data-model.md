# Data Model: MiMSMS Django Integration

## Configuration Model

### MiMSMSConfig (Pydantic)
- `username`: str
- `apikey`: str
- `sender_name`: str
- `base_url`: str (default: `https://api.mimsms.com`)
- `timeout`: float (default: 30.0)
- `verify_ssl`: bool (default: True)
- `default_transaction_type`: str (default: `T`)
- `campaign_id`: Optional[str]

## Request Models

### SmsRequest (Base)
- `UserName`: str (alias: `username`)
- `Apikey`: str (alias: `apikey`)

### SingleSmsRequest (SmsRequest)
- `MobileNumber`: str
- `SenderName`: str
- `TransactionType`: str
- `Message`: str
- `CampaignId`: Optional[str]

### BulkSmsRequest (SingleSmsRequest)
- `MobileNumber`: str (comma-separated numbers)

### DynamicSmsRequest (SmsRequest)
- `SmsData`: List[DynamicSmsItem]
- `TransactionType`: str (fixed: `D`)

### DynamicSmsItem
- `MobNumber`: str
- `Message`: str

## Response Models

### MiMSMSResponse
- `statusCode`: int
- `status`: str
- `trxnId`: Optional[str]
- `responseResult`: str

### BalanceResponse
- `statusCode`: int
- `status`: str
- `responseResult`: str (containing balance)

## Error Mapping (Exceptions)

- `MiMSMSException`: Base exception
- `MiMSMSAPIError`: Raised for statusCode != 200 or 100
- `MiMSMSValidationError`: Pydantic validation failures
- `MiMSMSTransportError`: httpx failures
