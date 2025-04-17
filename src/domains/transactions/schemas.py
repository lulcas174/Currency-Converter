from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class TransactionBase(BaseModel):
    source_currency: str = Field(..., example="USD")
    source_amount: float = Field(..., example=100.0)
    target_currency: str = Field(..., example="EUR")
    conversion_rate: float = Field(..., example=0.85)
    timestamp: datetime = Field(..., example="2025-04-17T14:30:00Z")

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    target_value: float

    class Config:
        from_attributes = True
