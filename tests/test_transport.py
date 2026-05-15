import pytest
import httpx
from django_mimsms.config import MiMSMSConfig
from django_mimsms.transport import Transport
from django_mimsms.exceptions import (
    MiMSMSAPIError,
    MiMSMSHTTPError,
    MiMSMSResponseParseError,
    MiMSMSTransportError,
)


@pytest.fixture
def config():
    return MiMSMSConfig(username="user", apikey="key", sender_name="SENDER")


@pytest.fixture
def transport(config):
    return Transport(config)


def test_transport_request_success(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(200, json={
            "statusCode": 200,
            "status": "success",
            "trxnId": "123",
            "responseResult": "OK"
        })
    )
    
    response = transport.request("POST", "/api/test", json={"foo": "bar"})
    assert response.status_code == 200
    assert response.trxn_id == "123"


def test_transport_request_api_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(200, json={
            "statusCode": 401,
            "status": "error",
            "responseResult": "Unauthorized"
        })
    )
    
    with pytest.raises(MiMSMSAPIError) as exc:
        transport.request("POST", "/api/test")
    assert exc.value.status_code == 401
    assert str(exc.value) == "Unauthorized"


def test_transport_request_http_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    
    with pytest.raises(MiMSMSHTTPError) as exc:
        transport.request("POST", "/api/test")
    assert exc.value.status_code == 500


def test_transport_request_api_error_code(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(200, json={
            "statusCode": 208,
            "status": "error",
            "responseResult": "Invalid Sender"
        })
    )
    
    with pytest.raises(MiMSMSAPIError) as exc:
        transport.request("POST", "/api/test")
    assert exc.value.status_code == 208
    assert str(exc.value) == "Invalid Sender"


def test_transport_request_transport_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        side_effect=httpx.ConnectError("Connection failed")
    )
    
    with pytest.raises(MiMSMSTransportError):
        transport.request("POST", "/api/test")


@pytest.mark.asyncio
async def test_transport_arequest_transport_error(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        side_effect=httpx.ConnectError("Connection failed")
    )
    
    with pytest.raises(MiMSMSTransportError):
        await transport.arequest("POST", "/api/test")


@pytest.mark.asyncio
async def test_transport_arequest_success(transport, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(200, json={
            "statusCode": 200,
            "status": "success",
            "trxnId": "123",
            "responseResult": "OK"
        })
    )
    
    response = await transport.arequest("POST", "/api/test")
    assert response.status_code == 200
    assert response.trxn_id == "123"


def test_transport_close(transport):
    transport.close()


@pytest.mark.asyncio
async def test_transport_aclose(transport):
    await transport.aclose()

def test_transport_handle_response_validation_error(transport, respx_mock):
    # Valid JSON but missing required fields for MiMSMSResponse
    respx_mock.post("https://api.mimsms.com/api/test").mock(
        return_value=httpx.Response(200, json={"wrong": "schema"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        transport.request("POST", "/api/test")
