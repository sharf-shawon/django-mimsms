import httpx
import pytest

from django_mimsms.client import MiMSMSClient
from django_mimsms.exceptions import MiMSMSResponseParseError, MiMSMSValidationError


@pytest.fixture
def client():
    return MiMSMSClient(username="user", apikey="key", sender_name="SENDER")


def test_send_sms_success(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/SMS").mock(
        return_value=httpx.Response(
            200,
            json={
                "statusCode": 200,
                "status": "success",
                "trxnId": "trxn_123",
                "responseResult": "SMS Sent Successfully",
            },
        )
    )

    response = client.send_sms(number="8801700000000", message="Test message")
    assert response.status_code == 200
    assert response.trxn_id == "trxn_123"


def test_send_sms_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.send_sms(number="", message="Test")


def test_send_sms_parse_error(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/SMS").mock(
        return_value=httpx.Response(200, json={"statusCode": 200, "status": "ok"})
    )
    # MiMSMSResponse requires status, statusCode etc.
    # But let's trigger it by returning something that fails model_validate
    respx_mock.post("https://api.mimsms.com/api/SmsSending/SMS").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.send_sms(number="8801700000000", message="Test")


def test_send_sms_get_success(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/Send").mock(
        return_value=httpx.Response(
            200,
            json={
                "statusCode": 200,
                "status": "success",
                "trxnId": "trxn_456",
                "responseResult": "SMS Sent Successfully",
            },
        )
    )

    response = client.send_sms_get(number="8801700000000", message="Test GET")
    assert response.status_code == 200
    assert response.trxn_id == "trxn_456"


def test_send_one_to_many_success(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/OneToMany").mock(
        return_value=httpx.Response(
            200,
            json={
                "statusCode": 200,
                "status": "success",
                "trxnId": "trxn_bulk",
                "responseResult": "Bulk SMS Sent Successfully",
            },
        )
    )

    response = client.send_one_to_many(numbers=["8801700000000", "8801700000001"], message="Test bulk")
    assert response.status_code == 200


def test_send_dynamic_sms_success(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/DSMS").mock(
        return_value=httpx.Response(
            200,
            json={
                "statusCode": 200,
                "status": "success",
                "trxnId": "trxn_dynamic",
                "responseResult": "Dynamic SMS Sent Successfully",
            },
        )
    )

    response = client.send_dynamic_sms(
        messages=[
            {"number": "8801700000000", "text": "Hi A"},
            {"number": "8801700000001", "text": "Hi B"},
        ]
    )
    assert response.status_code == 200


def test_check_balance_success(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/balanceCheck").mock(
        return_value=httpx.Response(200, json={"statusCode": 200, "status": "success", "responseResult": "100.50"})
    )

    balance = client.check_balance()
    assert balance == 100.50


def test_check_balance_get_success(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/balanceCheck").mock(
        return_value=httpx.Response(200, json={"statusCode": 200, "status": "success", "responseResult": "100.50"})
    )

    balance = client.check_balance_get()
    assert balance == 100.50


def test_send_one_to_many_get_success(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/SendOneToMany").mock(
        return_value=httpx.Response(
            200,
            json={
                "statusCode": 200,
                "status": "success",
                "trxnId": "trxn_bulk_get",
                "responseResult": "Bulk SMS Sent Successfully",
            },
        )
    )

    response = client.send_one_to_many_get(numbers=["8801700000000", "8801700000001"], message="Test bulk GET")
    assert response.status_code == 200


def test_send_one_to_many_string_input(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/OneToMany").mock(
        return_value=httpx.Response(200, json={"statusCode": 200, "status": "success", "responseResult": "OK"})
    )

    response = client.send_one_to_many(numbers="8801700000000,8801700000001", message="Test bulk string")
    assert response.status_code == 200


def test_client_context_manager(client):
    with client as c:
        assert isinstance(c, MiMSMSClient)


@pytest.mark.asyncio
async def test_client_async_context_manager(client):
    async with client as c:
        assert isinstance(c, MiMSMSClient)


def test_check_balance_parse_error(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/balanceCheck").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 200, "status": "success", "responseResult": "not-a-number"}
        )
    )

    balance = client.check_balance()
    assert balance == 0.0


def test_send_one_to_many_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.send_one_to_many(numbers=[], message="Test")


def test_send_one_to_many_get_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.send_one_to_many_get(numbers="", message="Test")


def test_send_dynamic_sms_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.send_dynamic_sms(messages=[{"number": "", "text": ""}])


def test_send_sms_get_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.send_sms_get(number="", message="Test")


def test_check_dlr_validation_error(client):
    with pytest.raises(MiMSMSValidationError):
        client.check_dlr(trxn_id="", number="")


def test_check_balance_parse_error_literal(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/balanceCheck").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 200, "status": "success", "responseResult": "not-a-number"}
        )
    )
    assert client.check_balance() == 0.0


def test_check_balance_get_parse_error_literal(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/balanceCheck").mock(
        return_value=httpx.Response(
            200, json={"statusCode": 200, "status": "success", "responseResult": "not-a-number"}
        )
    )
    assert client.check_balance_get() == 0.0


def test_check_dlr_actual_call(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/DlrApi").mock(
        return_value=httpx.Response(200, json={"statusCode": 200, "status": "success", "operatorStatus": "Delivered"})
    )
    res = client.check_dlr(trxn_id="foo", number="8801700000000")
    assert res.operator_status == "Delivered"


def test_client_auth_params_coverage(client):
    res = client._get_auth_params()
    assert "UserName" in res
    assert "ApiKey" in res


def test_send_sms_get_parse_error(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/Send").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.send_sms_get(number="8801700000000", message="Test")


def test_send_one_to_many_parse_error(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/OneToMany").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.send_one_to_many(numbers=["8801700000000"], message="Test")


def test_send_one_to_many_get_parse_error(client, respx_mock):
    respx_mock.get("https://api.mimsms.com/api/SmsSending/SendOneToMany").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.send_one_to_many_get(numbers=["8801700000000"], message="Test")


def test_send_dynamic_sms_parse_error(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/DSMS").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.send_dynamic_sms(messages=[{"number": "8801700000000", "text": "Hi"}])


def test_check_dlr_parse_error(client, respx_mock):
    respx_mock.post("https://api.mimsms.com/api/SmsSending/DlrApi").mock(
        return_value=httpx.Response(200, json={"wrong": "data"})
    )
    with pytest.raises(MiMSMSResponseParseError):
        client.check_dlr(trxn_id="foo", number="8801700000000")
