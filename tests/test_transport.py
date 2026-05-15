import httpx
import pytest

from django_mimsms.config import MiMSMSConfig
from django_mimsms.exceptions import (
    MiMSMSAPIError,
    MiMSMSHTTPError,
    MiMSMSResponseParseError,
    MiMSMSTransportError,
)
from django_mimsms.transport import Transport


@pytest.fixture
def config():
    return MiMSMSConfig(username="user", apikey="key", sender_name="SENDER")


@pytest.fixture
def transport(config):
    return Transport(config)


def test_transport_init(config):
    t = Transport(config)
    assert t.config == config
    assert isinstance(t._client, httpx.Client)
    assert isinstance(t._async_client, httpx.AsyncClient)


def test_transport_request_success(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 200, "status": "success", "trxnId": "123", "responseResult": "OK"}
        )
    )

    response = transport.request("POST", "/api/test", json={"foo": "bar"})
    assert response["statusCode"] == 200
    assert response["trxnId"] == "123"


def test_transport_request_http_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(return_value=httpx.Response(404))

    with pytest.raises(MiMSMSHTTPError) as exc:
        transport.request("POST", "/api/test")
    assert exc.value.status_code == 404


def test_transport_request_api_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 401, "status": "Authentication Failed", "responseResult": "Invalid API Key"}
        )
    )

    with pytest.raises(MiMSMSAPIError) as exc:
        transport.request("POST", "/api/test")
    assert exc.value.status_code == 401
    assert "Invalid API Key" in str(exc.value)


def test_transport_request_network_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(side_effect=httpx.ConnectError("fail"))

    with pytest.raises(MiMSMSTransportError):
        transport.request("POST", "/api/test")


@pytest.mark.asyncio
async def test_transport_arequest_success(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 200, "status": "success", "trxnId": "123", "responseResult": "OK"}
        )
    )

    response = await transport.arequest("POST", "/api/test")
    assert response["statusCode"] == 200


@pytest.mark.asyncio
async def test_transport_arequest_network_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(side_effect=httpx.ConnectError("fail"))

    with pytest.raises(MiMSMSTransportError):
        await transport.arequest("POST", "/api/test")


def test_transport_handle_response_invalid_json(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(return_value=httpx.Response(200, content=b"not json"))

    with pytest.raises(MiMSMSResponseParseError):
        transport.request("POST", "/api/test")


@pytest.mark.asyncio
async def test_transport_close(transport):
    transport.close()
    await transport.aclose()
    assert transport._client.is_closed
    assert transport._async_client.is_closed
