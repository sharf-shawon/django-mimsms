from typing import Any

from pydantic import ValidationError

from django_mimsms.config import MiMSMSConfig
from django_mimsms.exceptions import MiMSMSValidationError
from django_mimsms.models import (
    BulkSmsRequest,
    DlrRequest,
    DynamicSmsItem,
    DynamicSmsRequest,
    MiMSMSBaseRequest,
    MiMSMSResponse,
    SingleSmsRequest,
)
from django_mimsms.transport import Transport


class MiMSMSClient:
    """Core client for the MiMSMS API."""

    def __init__(
        self,
        username: str,
        apikey: str,
        sender_name: str,
        **options: Any,
    ) -> None:
        self.config = MiMSMSConfig(
            username=username, apikey=apikey, sender_name=sender_name, **options
        )
        self.transport = Transport(self.config)

    def send_sms(
        self,
        number: str,
        message: str,
        transaction_type: str | None = None,
        campaign_id: str | None = None,
    ) -> MiMSMSResponse:
        """Send a single SMS via JSON POST."""
        try:
            payload = SingleSmsRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                mobile_number=number,
                sender_name=self.config.sender_name,
                transaction_type=transaction_type or self.config.default_transaction_type,
                message=message,
                campaign_id=campaign_id or self.config.campaign_id,
            )
            return self.transport.request(
                "POST",
                "/api/SmsSending/SMS",
                json=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def send_sms_get(
        self,
        number: str,
        message: str,
        transaction_type: str | None = None,
        campaign_id: str | None = None,
    ) -> MiMSMSResponse:
        """Send a single SMS via query-string GET."""
        try:
            payload = SingleSmsRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                mobile_number=number,
                sender_name=self.config.sender_name,
                transaction_type=transaction_type or self.config.default_transaction_type,
                message=message,
                campaign_id=campaign_id or self.config.campaign_id,
            )
            return self.transport.request(
                "GET",
                "/api/SmsSending/Send",
                params=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def send_one_to_many(
        self,
        numbers: list[str] | str,
        message: str,
        transaction_type: str | None = None,
        campaign_id: str | None = None,
    ) -> MiMSMSResponse:
        """Send bulk SMS via JSON POST."""
        numbers_str = ",".join(numbers) if isinstance(numbers, list) else numbers

        try:
            payload = BulkSmsRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                mobile_number=numbers_str,
                sender_name=self.config.sender_name,
                transaction_type=transaction_type or self.config.default_transaction_type,
                message=message,
                campaign_id=campaign_id or self.config.campaign_id,
            )
            return self.transport.request(
                "POST",
                "/api/SmsSending/OneToMany",
                json=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def send_one_to_many_get(
        self,
        numbers: list[str] | str,
        message: str,
        transaction_type: str | None = None,
        campaign_id: str | None = None,
    ) -> MiMSMSResponse:
        """Send bulk SMS via query-string GET."""
        numbers_str = ",".join(numbers) if isinstance(numbers, list) else numbers

        try:
            payload = BulkSmsRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                mobile_number=numbers_str,
                sender_name=self.config.sender_name,
                transaction_type=transaction_type or self.config.default_transaction_type,
                message=message,
                campaign_id=campaign_id or self.config.campaign_id,
            )
            return self.transport.request(
                "GET",
                "/api/SmsSending/SendOneToMany",
                params=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def send_dynamic_sms(
        self,
        messages: list[dict[str, str]],
        transaction_type: str = "D",
    ) -> MiMSMSResponse:
        """Send dynamic SMS via JSON POST."""
        try:
            sms_data = [
                DynamicSmsItem(mobile_number=m["number"], message=m["text"])
                for m in messages
            ]
            payload = DynamicSmsRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                sms_data=sms_data,
                transaction_type=transaction_type,
            )
            return self.transport.request(
                "POST",
                "/api/SmsSending/DSMS",
                json=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def check_balance(self) -> float:
        """Check account balance via JSON POST."""
        payload = MiMSMSBaseRequest(
            username=self.config.username,
            apikey=self.config.apikey,
        )
        response = self.transport.request(
            "POST",
            "/api/SmsSending/balanceCheck",
            json=payload.model_dump(by_alias=True),
        )
        try:
            val = float(response.response_result)
            import math

            return val if not math.isnan(val) else 0.0
        except (ValueError, TypeError):
            return 0.0

    def check_balance_get(self) -> float:
        """Check account balance via query-string GET."""
        payload = MiMSMSBaseRequest(
            username=self.config.username,
            apikey=self.config.apikey,
        )
        response = self.transport.request(
            "GET",
            "/api/SmsSending/balanceCheck",
            params=payload.model_dump(by_alias=True),
        )
        try:
            val = float(response.response_result)
            import math

            return val if not math.isnan(val) else 0.0
        except (ValueError, TypeError):
            return 0.0

    def check_dlr(self, trxn_id: str) -> MiMSMSResponse:
        """Check delivery report for a transaction."""
        try:
            payload = DlrRequest(
                username=self.config.username,
                apikey=self.config.apikey,
                trxn_id=trxn_id,
            )
            return self.transport.request(
                "GET",
                "/api/SmsSending/DlrCheck",
                params=payload.model_dump(by_alias=True),
            )
        except ValidationError as e:
            raise MiMSMSValidationError(str(e)) from e

    def _get_auth_params(self) -> dict[str, str]:
        """Get authentication parameters."""
        return {
            "UserName": self.config.username,
            "Apikey": self.config.apikey,
        }

    def close(self) -> None:
        """Close the underlying transport."""
        self.transport.close()

    async def aclose(self) -> None:
        """Close the underlying transport asynchronously."""
        await self.transport.aclose()

    def __enter__(self) -> "MiMSMSClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> "MiMSMSClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()
