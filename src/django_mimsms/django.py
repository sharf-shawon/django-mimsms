import os
from typing import Any

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django_mimsms.client import MiMSMSClient


def get_config_from_django() -> dict[str, Any]:
    """Load configuration from Django settings."""
    config = {}
    
    mapping = {
        "MIMSMS_USERNAME": "username",
        "MIMSMS_APIKEY": "apikey",
        "MIMSMS_SENDER_NAME": "sender_name",
        "MIMSMS_BASE_URL": "base_url",
        "MIMSMS_TIMEOUT": "timeout",
        "MIMSMS_VERIFY_SSL": "verify_ssl",
        "MIMSMS_DEFAULT_TRANSACTION_TYPE": "default_transaction_type",
        "MIMSMS_CAMPAIGN_ID": "campaign_id",
    }
    
    for setting_key, config_key in mapping.items():
        value = getattr(settings, setting_key, None)
        if value is not None:
            config[config_key] = value
            
    # Fallback to env vars if not in settings
    for setting_key, config_key in mapping.items():
        if config_key not in config:
            value = os.environ.get(setting_key)
            if value is not None:
                config[config_key] = value

    return config


def get_client() -> MiMSMSClient:
    """
    Factory function to create a MiMSMSClient using Django settings.
    """
    config = get_config_from_django()
    
    required = ["username", "apikey", "sender_name"]
    missing = [key for key in required if key not in config]
    
    if missing:
        raise ImproperlyConfigured(
            f"MiMSMS configuration missing required settings: {', '.join(missing)}"
        )
        
    return MiMSMSClient(**config)
