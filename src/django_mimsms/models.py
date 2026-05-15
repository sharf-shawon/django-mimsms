from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

NonEmptyString = Annotated[str, StringConstraints(min_length=1)]


class MiMSMSBaseRequest(BaseModel):
    """Base model for MiMSMS requests."""

    model_config = ConfigDict(populate_by_name=True)

    username: NonEmptyString = Field(..., alias="UserName")
    apikey: NonEmptyString = Field(..., alias="ApiKey")


class MiMSMSResponse(BaseModel):
    """Base response model for MiMSMS API."""

    model_config = ConfigDict(populate_by_name=True)

    status_code: int = Field(..., alias="statusCode")
    status: str = Field(..., alias="status")
    trxn_id: str | None = Field(None, alias="trxnId")
    response_result: str | None = Field(None, alias="responseResult")


class SingleSmsRequest(MiMSMSBaseRequest):
    """Payload for sending a single SMS."""

    model_config = ConfigDict(populate_by_name=True)

    mobile_number: NonEmptyString = Field(..., alias="MobileNumber")
    sender_name: NonEmptyString = Field(..., alias="SenderName")
    transaction_type: str = Field(..., alias="TransactionType")
    message: NonEmptyString = Field(..., alias="Message")
    campaign_id: str | None = Field(None, alias="CampaignId")


class BulkSmsRequest(SingleSmsRequest):
    """Payload for sending one message to many recipients."""

    pass


class DynamicSmsItem(BaseModel):
    """Individual item for dynamic SMS."""

    model_config = ConfigDict(populate_by_name=True)

    mobile_number: NonEmptyString = Field(..., alias="MobNumber")
    message: NonEmptyString = Field(..., alias="Message")


class DynamicSmsRequest(MiMSMSBaseRequest):
    """Payload for sending dynamic SMS."""

    model_config = ConfigDict(populate_by_name=True)

    sender_name: NonEmptyString = Field(..., alias="SenderName")
    sms_data: list[DynamicSmsItem] = Field(..., alias="SmsData")
    transaction_type: str = Field("D", alias="TransactionType")


class BalanceResponse(MiMSMSResponse):
    """Response model for balance check."""

    pass


class DlrRequest(MiMSMSBaseRequest):
    """Payload for checking delivery status."""

    model_config = ConfigDict(populate_by_name=True)

    mobile_number: NonEmptyString = Field(..., alias="MobileNumber")
    trxn_id: NonEmptyString = Field(..., alias="trxnId")


class DlrResponse(MiMSMSResponse):
    """Response model for delivery report check."""

    operator_status: str | None = Field(None, alias="operatorStatus")
    dlr_code: str | None = Field(None, alias="dlrCode")
    receiver_mobile: str | None = Field(None, alias="receiverMobile")


class ErrorResponse(BaseModel):
    """API Error response model."""

    model_config = ConfigDict(populate_by_name=True)

    status_code: int = Field(..., alias="statusCode")
    status: str = Field(..., alias="status")
    response_result: str = Field(..., alias="responseResult")
