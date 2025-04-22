from pydantic import BaseModel, Field, ConfigDict, field_serializer
from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated
from uuid import UUID
from datetime import datetime


class TransactionCreate(BaseModel):
    source_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")
    source_amount: Annotated[Decimal, Field(..., gt=0)]
    target_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")


class TransactionResponse(BaseModel):
    transaction_id: UUID
    user_id: UUID
    source_currency: str
    source_amount: Decimal
    target_currency: str
    target_value: Decimal
    conversion_rate: Decimal
    timestamp: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transaction_id": "uuid",
                "user_id": "uuid",
                "source_currency": "BRL",
                "source_amount": "original amount",
                "target_currency": "USD",
                "target_value": "converted amount",
                "conversion_rate": "exchange rate",
                "timestamp": "date and time",
            }
        },
    )

    @field_serializer("source_amount", "target_value", "conversion_rate")
    def serialize_decimal(self, value: Decimal, _info):
        return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    @field_serializer("timestamp")
    def serialize_timestamp(self, dt: datetime, _info):
        return dt.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transactions": [
                    {
                        "transaction_id": "uuid",
                        "user_id": "uuid",
                        "source_currency": "USD",
                        "source_amount": "original amount",
                        "target_currency": "EUR",
                        "target_value": "converted amount",
                        "conversion_rate": "exchange rate",
                        "timestamp": "date and time",
                    },
                    {
                        "transaction_id": "uuid",
                        "user_id": "uuid",
                        "source_currency": "EUR",
                        "source_amount": "original amount",
                        "target_currency": "JPY",
                        "target_value": "converted amount",
                        "conversion_rate": "exchange rate",
                        "timestamp": "date and time",
                    },
                ]
            }
        },
    )

    @field_serializer("transactions")
    def serialize_transactions(self,
                               transactions: list[TransactionResponse],
                               _info):
        return [transaction.model_dump() for transaction in transactions]
