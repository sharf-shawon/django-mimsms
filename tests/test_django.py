import pytest
from django.core.exceptions import ImproperlyConfigured

from django_mimsms.django import get_client, get_config_from_django


def test_get_config_from_django(settings):
    settings.MIMSMS_USERNAME = "dj_user"
    settings.MIMSMS_APIKEY = "dj_key"
    settings.MIMSMS_SENDER_NAME = "DJ_SENDER"

    config = get_config_from_django()
    assert config["username"] == "dj_user"
    assert config["apikey"] == "dj_key"
    assert config["sender_name"] == "DJ_SENDER"


def test_get_config_from_env(settings, monkeypatch):
    # Ensure settings are empty for required keys
    for key in ["MIMSMS_USERNAME", "MIMSMS_APIKEY", "MIMSMS_SENDER_NAME"]:
        if hasattr(settings, key):
            delattr(settings, key)

    monkeypatch.setenv("MIMSMS_USERNAME", "env_user")
    monkeypatch.setenv("MIMSMS_APIKEY", "env_key")
    monkeypatch.setenv("MIMSMS_SENDER_NAME", "ENV_SENDER")

    config = get_config_from_django()
    assert config["username"] == "env_user"
    assert config["apikey"] == "env_key"
    assert config["sender_name"] == "ENV_SENDER"


def test_get_client_success(settings):
    settings.MIMSMS_USERNAME = "dj_user"
    settings.MIMSMS_APIKEY = "dj_key"
    settings.MIMSMS_SENDER_NAME = "DJ_SENDER"

    client = get_client()
    assert client.config.username == "dj_user"


def test_get_client_missing_config(settings):
    if hasattr(settings, "MIMSMS_USERNAME"):
        del settings.MIMSMS_USERNAME
    if hasattr(settings, "MIMSMS_APIKEY"):
        del settings.MIMSMS_APIKEY
    if hasattr(settings, "MIMSMS_SENDER_NAME"):
        del settings.MIMSMS_SENDER_NAME

    with pytest.raises(ImproperlyConfigured):
        get_client()
