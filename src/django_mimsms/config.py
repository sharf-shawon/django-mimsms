from pydantic import BaseModel, ConfigDict


class MiMSMSConfig(BaseModel):
    """Configuration model for MiMSMS integration."""

    model_config = ConfigDict(populate_by_name=True)

    username: str
    apikey: str
    sender_name: str
    base_url: str = "https://api.mimsms.com"
    timeout: float = 30.0
    verify_ssl: bool = True
    default_transaction_type: str = "T"
    campaign_id: str | None = None
