from typing import Any

import httpx
from pydantic import ValidationError

from django_mimsms.config import MiMSMSConfig
from django_mimsms.exceptions import (
    MiMSMSAPIError,
    MiMSMSHTTPError,
    MiMSMSResponseParseError,
    MiMSMSTransportError,
)
from django_mimsms.models import MiMSMSResponse


class Transport:
    """Handles HTTP communication with the MiMSMS API."""

    def __init__(
        self,
        config: MiMSMSConfig,
        client: httpx.Client | None = None,
        async_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.config = config
        self._client = client or httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            verify=config.verify_ssl,
        )
        self._async_client = async_client or httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            verify=config.verify_ssl,
        )

    def request(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> MiMSMSResponse:
        """Perform a synchronous request."""
        try:
            response = self._client.request(method, path, json=json, params=params)
            return self._handle_response(response)
        except httpx.HTTPError as e:
            raise MiMSMSTransportError(f"HTTP transport error: {str(e)}") from e

    async def arequest(
        self,
        method: str,
        path: str,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> MiMSMSResponse:
        """Perform an asynchronous request."""
        try:
            response = await self._async_client.request(method, path, json=json, params=params)
            return self._handle_response(response)
        except httpx.HTTPError as e:
            raise MiMSMSTransportError(f"HTTP transport error: {str(e)}") from e

    def _handle_response(self, response: httpx.Response) -> MiMSMSResponse:
        """Parse and handle the API response."""
        if not (200 <= response.status_code < 300):
            raise MiMSMSHTTPError(
                f"HTTP error {response.status_code}",
                status_code=response.status_code,
                response_body=response.text,
            )

        try:
            data = response.json()
            mimsms_response = MiMSMSResponse.model_validate(data)

            # Functional error check (status codes like 401, 208 returned with HTTP 200)
            # MiMSMS usually returns success as 200 or 100
            if mimsms_response.status_code not in [200, 100]:
                raise MiMSMSAPIError(
                    mimsms_response.response_result,
                    status_code=mimsms_response.status_code,
                    trxn_id=mimsms_response.trxn_id,
                )

            return mimsms_response
        except (ValueError, ValidationError) as e:
            raise MiMSMSResponseParseError(f"Failed to parse API response: {str(e)}") from e

    def close(self) -> None:
        """Close the sync client."""
        self._client.close()

    async def aclose(self) -> None:
        """Close the async client."""
        await self._async_client.aclose()
