from typing import Any


class MiMSMSError(Exception):
    """Base exception for all django-mimsms errors."""

    def __init__(self, message: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(message, *args)


class MiMSMSConfigurationError(MiMSMSError):
    """Raised when configuration is missing or invalid."""


class MiMSMSValidationError(MiMSMSError):
    """Raised when request data fails Pydantic validation."""


class MiMSMSTransportError(MiMSMSError):
    """Raised when a network or transport error occurs."""


class MiMSMSHTTPError(MiMSMSTransportError):
    """Raised when an HTTP error status code is returned."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code
        self.response_body = response_body


class MiMSMSAPIError(MiMSMSError):
    """Raised when the MiMSMS API returns a functional error."""

    def __init__(
        self,
        message: str,
        status_code: int,
        trxn_id: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code
        self.trxn_id = trxn_id


class MiMSMSResponseParseError(MiMSMSError):
    """Raised when the API response cannot be parsed."""
