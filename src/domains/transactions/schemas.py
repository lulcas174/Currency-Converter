from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Annotated
from uuid import UUID
from datetime import datetime

class TransactionCreate(BaseModel):
    source_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")
    source_amount: Annotated[Decimal, Field(..., gt=0)]  # Valor > 0
    target_currency: str = Field(..., pattern="^(BRL|USD|EUR|JPY)$")

class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    source_currency: str
    source_amount: Decimal
    target_currency: str
    target_value: Decimal
    conversion_rate: Decimal
    timestamp: datetime

    model_config = ConfigDict(
        json_encoders={
            Decimal: lambda v: str(v)
        },
        from_attributes=True
    )