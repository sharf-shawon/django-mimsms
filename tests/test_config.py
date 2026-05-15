from django_mimsms.config import MiMSMSConfig


def test_mimsms_config_defaults():
    config = MiMSMSConfig(
        username="user",
        apikey="key",
        sender_name="SENDER"
    )
    assert config.username == "user"
    assert config.apikey == "key"
    assert config.sender_name == "SENDER"
    assert config.base_url == "https://api.mimsms.com"
    assert config.timeout == 30.0
    assert config.verify_ssl is True
    assert config.default_transaction_type == "T"
    assert config.campaign_id is None


def test_mimsms_config_overrides():
    config = MiMSMSConfig(
        username="user",
        apikey="key",
        sender_name="SENDER",
        base_url="https://alt.example.com",
        timeout=10.0,
        verify_ssl=False,
        default_transaction_type="P",
        campaign_id="CAMP123"
    )
    assert config.base_url == "https://alt.example.com"
    assert config.timeout == 10.0
    assert config.verify_ssl is False
    assert config.default_transaction_type == "P"
    assert config.campaign_id == "CAMP123"
